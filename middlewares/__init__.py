# -*- coding: utf-8 -*-
import json
import threading
import random
import string
import time
from google.protobuf.json_format import MessageToDict
from munch import DefaultMunch
from starlette.requests import Request
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.cors import CORSMiddleware
from libs.open.open import OpenAPIRequest
from apps.system.models import OperateLog
from micro_server.rpc.auth.rpc_client import verifyToken
from settings.db import SessionLocal
from settings.log import log_info, log_error
from fastapi.middleware.wsgi import WSGIMiddleware
from utils.constant import RET
from utils.resp import MyResponse
from libs.ali.dingding import dd


def middleware_init(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["GET", 'POST', 'PUT', 'DELETE'],
        allow_headers=["*"],
    )

    # 校验token
    @app.middleware('http')
    async def auth_verify(request: Request, call_next):
        if request.url.path in ['/docs', '/openapi.json']:
            pass
        else:
            Authorization = request.headers.get('Authorization')
            if not Authorization or not Authorization.startswith('Bearer '):
                return MyResponse(code=RET.SESSION_ERR, msg='未提供有效的身份令牌')
            token = Authorization.split(' ')[1]
            verify_res = verifyToken(token=token)

            if verify_res.code != 0:
                return MyResponse(code=verify_res.code, msg=verify_res.msg)
            user_info = MessageToDict(
                verify_res.data, including_default_value_fields=True, preserving_proto_field_name=True)
            setattr(request.state, 'user', DefaultMunch.fromDict(user_info))
        response = await call_next(request)
        return response

    def insert_data(request, log_str, response_data, formatted_process_time):
        path_parts = request.url.path.split("/")
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        user_ip = request.client.host
        user_id = request.state.user.user_id if hasattr(request.state, 'user') else None
        query_params_dict = dict(request.query_params)
        handler = request.scope.get("endpoint", None)
        request_path = request.url.path
        request_method = request.method
        session_id = request.state.user.session_id if hasattr(request.state, 'user') else None
        if callable(handler):
            if hasattr(handler, '__name__'):
                operation = f"{handler.__module__}/{handler.__name__}"
            else:
                operation = handler.__module__
        else:
            if handler is not None:
                operation = f"{handler.__module__}/{handler}"
            else:
                operation = "default_operation"
        user_ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else user_ip
        ip_info: dict = OpenAPIRequest.ip_parse(user_ip)
        keys_to_extract = ['country', 'ip']
        address_info = '/'.join([ip_info.get(key, '') for key in keys_to_extract]) if ip_info else ""
        if len(path_parts) < 4:
            modules = path_parts[-1]
        else:
            modules = path_parts[3]
        msg_start_index = log_str.find("msg=") + len("msg=")
        msg_value = log_str[msg_start_index:]
        if msg_value == "成功" or "http_status_code=200" in log_str or "self_status_code=0" in log_str:
            request_status = "Success"
        else:
            request_status = "Error"
        data_to_insert = [
            {"request_path": request_path, "module": modules, "required_params": query_params_dict,
             "request_method": request_method, "request_ip": user_ip,
             "request_address": address_info, "operation": operation,
             "request_user_id": user_id, "session_id": session_id, "return_params": response_data,
             "request_status": request_status, "spent_time": formatted_process_time}
        ]
        try:
            with SessionLocal() as db:
                db.bulk_insert_mappings(OperateLog, data_to_insert)
                db.commit()
        except Exception as e:
            log_error(f"Error: {e}")

    @app.middleware('http')
    async def log_requests(request, call_next):
        idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)
        log_str = f"rid={idem} start request {request.method} " \
                  f"request_user={request.state.user.real_name if hasattr(request.state, 'user') else '匿名用户'} " \
                  f"path={request.url.path} " \
                  f"completed_in={formatted_process_time}ms "
        content_type = response.headers.get('content-type', '')
        response_data = {}
        if 'application/json' not in content_type:
            log_str += f"http_status_code={response.status_code} "
        else:
            response_body = [chunk async for chunk in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))
            json_res = json.loads(b''.join(response_body).decode())
            log_str += f"http_status_code={response.status_code} msg={json_res['detail']}" if 'detail' in json_res else \
                f"self_status_code={json_res.get('code')} msg={json_res.get('msg')}"
            if json_res.get('code') == RET.SERVER_ERR:
                title = 'xxx系统服务端错误'
                msg = json_res['detail'] if 'detail' in json_res else json_res.get('msg')
                err_msg = f"### {title}\n- 请求地址：{request.url.path}\n- 异常：{msg}\n"
                dd.send_err_message(title=title, content=err_msg)
            for key, value in json_res.items():
                response_data[key] = value
        log_info(log_str)
        threading.Thread(
            target=insert_data,
            args=(request, log_str, response_data, formatted_process_time)
        ).start()
        return response

    WSGIMiddleware(app)
