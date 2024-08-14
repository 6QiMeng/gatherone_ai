from google.protobuf.json_format import MessageToDict
from munch import DefaultMunch
from starlette.requests import Request
from starlette.middleware.cors import CORSMiddleware
from rpc.auth.rpc_client import verifyToken
from fastapi.middleware.wsgi import WSGIMiddleware
from utils.constant import RET
from utils.resp import MyResponse


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
        """
        验证token
        """
        if request.url.path not in ['/docs', '/openapi.json']:
            Authorization = request.headers.get('Authorization')
            if not Authorization or not Authorization.startswith('Bearer '):
                return MyResponse(code=RET.SESSION_ERR, msg='未提供有效的身份令牌')
            token = Authorization.split(' ')[1]
            verify_res = verifyToken(token=token)
            if verify_res.code != 0:
                return MyResponse(code=verify_res.code, msg=verify_res.msg)
            user_info = MessageToDict(
                verify_res.data,
                including_default_value_fields=True,
                preserving_proto_field_name=True
            )
            setattr(request.state, 'user', DefaultMunch.fromDict(user_info))
        response = await call_next(request)
        return response

    WSGIMiddleware(app)
