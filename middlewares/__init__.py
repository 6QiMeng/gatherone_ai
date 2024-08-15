from starlette.requests import Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from utils.constant import RET
from utils.resp import MyResponse
from settings.base import configs
from apps.system.utils import JwtTokenUtil
from settings.db import SessionLocal
from apps.system.models import UserModel
from munch import DefaultMunch


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
        if request.url.path not in [
            '/docs',
            '/openapi.json',
            f"{configs.API_VERSION_STR}/system/sms_codes",  # 发送验证码
            f"{configs.API_VERSION_STR}/system/register",  # 注册
            f"{configs.API_VERSION_STR}/system/pwd_login",  # 密码登录
            f"{configs.API_VERSION_STR}/system/sms_login",  # 验证码登录
            f"{configs.API_VERSION_STR}/system/forget_pwd",  # 重置密码
        ]:
            Authorization = request.headers.get('Authorization')
            if not Authorization or not Authorization.startswith('Bearer '):
                return MyResponse(code=RET.SESSION_ERR, msg='未提供有效的身份令牌')
            token = Authorization.split(' ')[1]
            payload = JwtTokenUtil.verify_jwt(token)
            if not payload:
                return RET.SESSION_ERR, '身份令牌已过期'
            with SessionLocal() as db:
                user = db.query(UserModel).filter(UserModel.id == payload.get("user_id")).first()
            setattr(request.state, 'user', DefaultMunch.fromDict(user.to_dict()))
        response = await call_next(request)
        return response

    WSGIMiddleware(app)
