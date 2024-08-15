import jwt
import time
from settings.base import configs


class JwtTokenUtil:
    AUTH_HEADER_KEY = "Authorization"
    TOKEN_PREFIX = "Bearer "
    EXPIRATION_TIME = configs.ACCESS_TOKEN_EXPIRE_MINUTES  # token过期时间  默认8小时

    @staticmethod
    def generate_jwt(payload, expiry=EXPIRATION_TIME, secret=None):
        """
        生成jwt
        :param payload: dict 载荷
        :param expiry: datetime 有效期
        :param secret: 密钥
        :return: jwt
        """
        _payload = {'exp': int(time.time()) + expiry}
        _payload.update(payload)
        if not secret:
            secret = configs.SECRET_KEY
        token = jwt.encode(payload=_payload, key=secret, algorithm='HS256')
        return token

    @staticmethod
    def verify_jwt(token, secret=None):
        """
        检验jwt
        :param token: jwt
        :param secret: 密钥
        :return: dict: payload
        """
        if not secret:
            secret = configs.SECRET_KEY

        try:
            payload = jwt.decode(token, secret, algorithms=['HS256'])
        except jwt.PyJWTError:
            payload = None

        return payload