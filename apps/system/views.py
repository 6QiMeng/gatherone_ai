import random
from fastapi import Depends, APIRouter, Query
from fastapi_utils.cbv import cbv
from starlette.requests import Request
from sqlalchemy.orm import Session
from settings.db import get_db, RedisManage
from apps.system.models import UserModel
from utils.resp import MyResponse
from utils.constant import CodeType, RET
from utils.common import RequestsHandler
from settings.log import log_error
from settings.base import configs
from core.customer_consul import AIConsul
from core.micro_service import get_service_path

SystemRouter = APIRouter(tags=["系统中心"])


@cbv(SystemRouter)
class UserServer:
    request: Request

    @SystemRouter.get("/sms_codes", description="发送短信验证码")
    async def send_sms_code(
            self,
            code_type: str = Query(...),
            mobile: str = Query(..., regex=r'^1[3-9]\d{9}$'),
            db: Session = Depends(get_db),
    ):
        user = db.query(UserModel).filter(
            UserModel.mobile == mobile,
            UserModel.is_delete == False
        ).first()
        if code_type in [CodeType.REGISTER, CodeType.UPDATE_MOBILE]:
            if user:
                return MyResponse(code=RET.USER_ERR, msg="该手机号已被注册")
        if code_type in [CodeType.FORGET_PWD, CodeType.LOGIN]:
            if not user:
                return MyResponse(code=RET.USER_ERR, msg="该手机号不存在")
        # 调用发送验证码的推送服务
        try:
            sms_code = '%06d' % random.randint(0, 999999)
            # 将验证码存储到redis
            res, err = RedisManage.storage_sms_code(code_type, mobile, sms_code)
            if not res:
                return MyResponse(code=RET.CODE_ERR, msg=err)
            # 调用消息推送服务 发送短信
            my_consul = AIConsul()
            # 获取推送服务地址
            server_host, server_port = my_consul.discover_service('push')
            if not server_host or not server_port:
                return MyResponse(code=RET.SERVER_ERR, msg='推送服务异常')
            # 获取请求uri
            uri = get_service_path('push', 'message_push')
            # 发送网络请求
            url = f"http://{server_host}:{server_port}{uri}"
            # 消息内容
            message_content = {
                "data_content": {"code": sms_code},
                "template_id": configs.SMS_TEMPLATE_ID,
                "phone": mobile,
                "app_secret": configs.ACCESS_KEY_SECRET,
                "app_key": configs.ACCESS_KEY_ID
            }
            handler = RequestsHandler()
            handler.post(
                url=url,
                json={
                    "message_type": "sms",
                    "message_weight": "1",
                    "message_content": message_content
                }
            )
        except Exception as e:
            log_error(f'发生错误,原因：{e.__str__()}')
            return MyResponse(code=RET.SERVER_ERR, msg='推送服务网络异常')
        return MyResponse(msg="验证码发送成功")
