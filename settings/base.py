# -*- coding: utf-8 -*-
import io
import os
from contextlib import contextmanager
from functools import lru_cache
from io import StringIO
from dotenv.main import DotEnv
from pydantic import BaseSettings, Field
from typing import Optional


def my_get_stream(self):
    """重写python-dotenv读取文件的方法，使用utf-8，支持读取包含中文的.env配置文件"""
    if isinstance(self.dotenv_path, StringIO):
        yield self.dotenv_path
    elif os.path.isfile(self.dotenv_path):
        with io.open(self.dotenv_path, encoding='utf-8') as stream:
            yield stream
    else:
        if self.verbose:
            print("File doesn't exist %s", self.dotenv_path)
        yield StringIO('')


DotEnv._get_stream = contextmanager(my_get_stream)


class Settings(BaseSettings):
    """System configurations."""

    # 系统环境
    ENVIRONMENT: Optional[str] = Field(None, env="ENVIRONMENT")

    # 系统安全秘钥
    SECRET_KEY: Optional[str] = Field(None, env="SECRET_KEY")

    # API版本号
    API_VERSION_STR = "/api/v1"

    # token过期时间8小时
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 60 * 8

    # 算法
    ALGORITHM = "HS256"

    # 产品名称
    PRODUCTION_NAME = "gatherone_xxx"

    # 允许访问的源
    ALLOW_ORIGINS = [
        '*'
    ]

    # 阿里云
    ACCESSKEY_ID: Optional[str] = Field(None, env="ACCESSKEY_ID")
    ACCESSKEY_SECRET: Optional[str] = Field(None, env="ACCESSKEY_SECRET")
    BUCKET_NAME: Optional[str] = Field(None, env="BUCKET_NAME")
    END_POINT: Optional[str] = Field(None, env="END_POINT")
    TEMPLATE_CODE: Optional[str] = Field(None, env="TEMPLATE_CODE")
    AILOSS_URL: Optional[str] = Field(None, env="AILOSS_URL")
    OSS_PREFIX: Optional[str] = Field(None, env="OSS_PREFIX")

    # 微信
    WX_BASE_URL: Optional[str] = Field(None, env="WX_BASE_URL")
    APP_ID: Optional[str] = Field(None, env="APP_ID")
    APP_SECRET: Optional[str] = Field(None, env="APP_SECRET")

    TIANAPI_KEY: Optional[str] = Field(None, env='TIANAPI_KEY')

    # REDIS存储
    REDIS_STORAGE = {
        'invitation_code': 1,  # 邀请码
        'email_code': 2,  # 邮箱验证码
        'login_info': 3,  # 登录信息
        'sms_code': 4,  # 手机验证码
    }

    # 加载.env文件的配置
    class Config:
        env_file = ".env"
        case_sensitive = True


class DevConfig(Settings):
    """Development configurations."""
    MQ_HOST: Optional[str] = Field(None, env="DEV_MQ_HOST")
    MQ_PORT: Optional[str] = Field(None, env="DEV_MQ_PORT")
    MQ_USERNAME: Optional[str] = Field(None, env="DEV_MQ_USERNAME")
    MQ_PASSWORD: Optional[str] = Field(None, env="DEV_MQ_PASSWORD")
    MQ_VIRTUAL_HOST: Optional[str] = Field(None, env="DEV_MQ_VIRTUAL_HOST")

    # redis
    REDIS_HOST: Optional[str] = Field(None, env="DEV_REDIS_HOST")
    REDIS_PORT: Optional[int] = Field(None, env="DEV_REDIS_PORT")
    REDIS_USERNAME: Optional[str] = Field(None, env="DEV_REDIS_USERNAME")
    REDIS_PASSWORD: Optional[str] = Field(None, env="DEV_REDIS_PASSWORD")

    # Mysql
    MYSQL_SERVER: Optional[str] = Field(None, env="DEV_MYSQL_SERVER")
    MYSQL_USER: Optional[str] = Field(None, env="DEV_MYSQL_USER")
    MYSQL_PASSWORD: Optional[str] = Field(None, env="DEV_MYSQL_PASSWORD")
    MYSQL_DB_NAME: Optional[str] = Field(None, env="DEV_MYSQL_DB_NAME")
    MYSQL_PORT: Optional[int] = Field(None, env="DEV_MYSQL_PORT")

    EMAIL: Optional[str] = Field(None, env="DEV_EMAIL")
    EMAIL_PWD: Optional[str] = Field(None, env="DEV_EMAIL_PWD")

    # 发送邮件
    # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 指定邮件后端
    EMAIL_HOST: Optional[str] = Field(None, env="DEV_EMAIL_HOST")
    EMAIL_PORT: Optional[str] = Field(None, env="DEV_EMAIL_PORT")
    SENDER: Optional[str] = Field(None, env="DEV_SENDER")
    PASSWORD: Optional[str] = Field(None, env="DEV_PASSWORD")
    EMAIL_FROM_NAME: Optional[str] = Field(None, env="DEV_EMAIL_FROM_NAME")
    EMAIL_USE_SSL = 997

    # 回调相关
    API_RPC_SERVER: Optional[str] = Field(None, env="DEV_API_RPC_SERVER")
    API_KEY: Optional[str] = Field(None, env="DEV_API_KEY")

    # 认证服务
    AUTH_RPC_SERVER: Optional[str] = Field(None, env="DEV_AUTH_RPC_SERVER")

    # 钉钉消息提醒
    BUG_DD_TOKEN: Optional[str] = Field(None, env="DEV_BUG_DD_TOKEN")
    BUG_DD_SECRET: Optional[str] = Field(None, env="DEV_BUG_DD_SECRET")


class ProdConfig(Settings):
    """Production configurations."""
    MQ_HOST: Optional[str] = Field(None, env="PROD_MQ_HOST")
    MQ_PORT: Optional[str] = Field(None, env="PROD_MQ_PORT")
    MQ_USERNAME: Optional[str] = Field(None, env="PROD_MQ_USERNAME")
    MQ_PASSWORD: Optional[str] = Field(None, env="PROD_MQ_PASSWORD")
    MQ_VIRTUAL_HOST: Optional[str] = Field(None, env="PROD_MQ_VIRTUAL_HOST")

    # redis
    REDIS_HOST: Optional[str] = Field(None, env="PROD_REDIS_HOST")
    REDIS_PORT: Optional[int] = Field(None, env="PROD_REDIS_PORT")
    REDIS_USERNAME: Optional[str] = Field(None, env="PROD_REDIS_USERNAME")
    REDIS_PASSWORD: Optional[str] = Field(None, env="PROD_REDIS_PASSWORD")

    # Mysql
    MYSQL_SERVER: Optional[str] = Field(None, env="PROD_MYSQL_SERVER")
    MYSQL_USER: Optional[str] = Field(None, env="PROD_MYSQL_USER")
    MYSQL_PASSWORD: Optional[str] = Field(None, env="PROD_MYSQL_PASSWORD")
    MYSQL_DB_NAME: Optional[str] = Field(None, env="PROD_MYSQL_DB_NAME")
    MYSQL_PORT: Optional[int] = Field(None, env="PROD_MYSQL_PORT")

    EMAIL: Optional[str] = Field(None, env="PRO_EMAIL")
    EMAIL_PWD: Optional[str] = Field(None, env="PRO_EMAIL_PWD")

    # 回调相关
    API_RPC_SERVER: Optional[str] = Field(None, env="PROD_API_RPC_SERVER")
    API_KEY: Optional[str] = Field(None, env="PROD_API_KEY")

    # 认证服务
    SSO_RPC_SERVER: Optional[str] = Field(None, env="PROD_SSO_RPC_SERVER")

    # 钉钉消息提醒
    BUG_DD_TOKEN: Optional[str] = Field(None, env="PROD_BUG_DD_TOKEN")
    BUG_DD_SECRET: Optional[str] = Field(None, env="PROD_BUG_DD_SECRET")


class FactoryConfig:
    """Returns a config instance dependending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state

    def __call__(self):

        if self.env_state == "development":
            return DevConfig()

        elif self.env_state == "production":
            return ProdConfig()


@lru_cache()
def get_configs():
    """加载一下环境文件"""
    from dotenv import load_dotenv
    load_dotenv(encoding='utf-8')
    return FactoryConfig(Settings().ENVIRONMENT)()


configs = get_configs()
