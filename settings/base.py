import os
import datetime
from functools import lru_cache
from typing import Optional
from pydantic.v1 import BaseSettings, Field

from logging.handlers import WatchedFileHandler


class MyWatchHandler(WatchedFileHandler):
    def __init__(self, file_path, mode='a', encoding=None, delay=False, errors=None):
        filepath = self.filepath = './logs'
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        self.filename = f"{datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')}.log"
        file_name = os.path.join(self.filepath, self.filename)
        super().__init__(file_name, mode=mode, encoding=encoding, delay=delay, errors=errors)

    def emit(self, record):
        """
        每天分割文件，每天一个新的日志文件
        """
        current_file_name = f"{datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')}.log"
        if current_file_name != self.filename:
            self.filename = current_file_name
            self.baseFilename = os.path.abspath(os.path.join(self.filepath, self.filename))
            if self.stream:
                self.stream.flush()
                self.stream.close()
            self.stream = self._open()
            self._statstream()
        self.reopenIfNeeded()
        super().emit(record)


class Settings(BaseSettings):
    """System configurations."""

    # 系统环境
    ENVIRONMENT: Optional[str] = Field(None, env="ENVIRONMENT")

    # 系统安全秘钥
    SECRET_KEY: Optional[str] = Field(None, env="SECRET_KEY")

    # API版本号
    API_VERSION_STR: Optional[str] = "/api/v1"

    # token过期时间8小时
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = 60 * 60 * 8

    # 算法
    ALGORITHM: Optional[str] = "HS256"

    # 产品名称
    PRODUCTION_NAME: Optional[str] = "gatherone_oa"

    # 允许访问的源
    ALLOW_ORIGINS: Optional[list] = [
        '*'
    ]

    # 阿里云
    ACCESS_KEY_ID: Optional[str] = Field(None, env="ACCESS_KEY_ID")
    ACCESS_KEY_SECRET: Optional[str] = Field(None, env="ACCESS_KEY_SECRET")
    BUCKET_NAME: Optional[str] = Field(None, env="BUCKET_NAME")
    END_POINT: Optional[str] = Field(None, env="END_POINT")
    ALIOSS_URL: Optional[str] = Field(None, env="ALIOSS_URL")
    OSS_PREFIX: Optional[str] = Field(None, env="OSS_PREFIX")

    # 加载.env文件的配置
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True

    # REDIS存储
    REDIS_STORAGE = {
        'code': 1  # 所有验证码都存储在1号库
    }



class DevConfig(Settings):
    class Config:
        env_file = ".env"
        # env_file_encoding = 'utf-8'
        case_sensitive = True

    """Development configurations."""
    MQ_HOST: Optional[str] = Field(None, env="DEV_MQ_HOST")
    MQ_PORT: Optional[str] = Field(None, env="DEV_MQ_PORT")
    MQ_USERNAME: Optional[str] = Field(None, env="DEV_MQ_USERNAME")
    MQ_PASSWORD: Optional[str] = Field(None, env="DEV_MQ_PASSWORD")
    MQ_VIRTUAL_HOST: Optional[str] = Field(None, env="DEV_MQ_VIRTUAL_HOST")

    # redis
    REDIS_HOST: Optional[str] = Field(None, env="DEV_REDIS_HOST")
    REDIS_PORT: Optional[int] = Field(None, env="DEV_REDIS_PORT")
    REDIS_PASSWORD: Optional[str] = Field(None, env="DEV_REDIS_PASSWORD")
    REDIS_CHANNEL: Optional[str] = Field(None, env="DEV_REDIS_CHANNEL")

    # Mysql
    MYSQL_SERVER: Optional[str] = Field(None, env="DEV_MYSQL_SERVER")
    MYSQL_USER: Optional[str] = Field(None, env="DEV_MYSQL_USER")
    MYSQL_PASSWORD: Optional[str] = Field(None, env="DEV_MYSQL_PASSWORD")
    MYSQL_DB_NAME: Optional[str] = Field(None, env="DEV_MYSQL_DB_NAME")
    MYSQL_PORT: Optional[int] = Field(None, env="DEV_MYSQL_PORT")

    # 星火服务
    SPARKAI_URL: Optional[str] = Field(None, env="DEV_SPARKAI_URL")
    SPARKAI_APP_ID: Optional[str] = Field(None, env="DEV_SPARKAI_APP_ID")
    SPARKAI_API_KEY: Optional[str] = Field(None, env="DEV_SPARKAI_API_KEY")
    SPARKAI_API_SECRET: Optional[str] = Field(None, env="DEV_SPARKAI_API_SECRET")
    SPARKAI_DOMAIN: Optional[str] = Field(None, env="DEV_SPARKAI_DOMAIN")

    # 百度服务
    BAI_DU_API_KEY: Optional[str] = Field(None, env="DEV_BAI_DU_API_KEY")
    BAI_DU_SECRET_KEY: Optional[str] = Field(None, env="DEV_BAI_DU_SECRET_KEY")

    # 认证服务
    AUTH_RPC_SERVER: Optional[str] = Field(None, env="DEV_AUTH_RPC_SERVER")

    # 钉钉消息提醒
    BUG_DD_TOKEN: Optional[str] = Field(None, env="DEV_BUG_DD_TOKEN")
    BUG_DD_SECRET: Optional[str] = Field(None, env="DEV_BUG_DD_SECRET")

    # Consul
    CONSUL_HOST: Optional[str] = Field(None, env="DEV_CONSUL_HOST")
    CONSUL_PORT: Optional[str] = Field(None, env="DEV_CONSUL_PORT")

    # 短信模版id
    SMS_TEMPLATE_ID: Optional[str] = Field(None, env="DEV_SMS_TEMPLATE_ID")


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
    REDIS_PASSWORD: Optional[str] = Field(None, env="PROD_REDIS_PASSWORD")
    REDIS_CHANNEL: Optional[str] = Field(None, env="PROD_REDIS_CHANNEL")

    # Mysql
    MYSQL_SERVER: Optional[str] = Field(None, env="PROD_MYSQL_SERVER")
    MYSQL_USER: Optional[str] = Field(None, env="PROD_MYSQL_USER")
    MYSQL_PASSWORD: Optional[str] = Field(None, env="PROD_MYSQL_PASSWORD")
    MYSQL_DB_NAME: Optional[str] = Field(None, env="PROD_MYSQL_DB_NAME")
    MYSQL_PORT: Optional[int] = Field(None, env="PROD_MYSQL_PORT")

    # 星火服务
    SPARKAI_URL: Optional[str] = Field(None, env="PROD_SPARKAI_URL")
    SPARKAI_APP_ID: Optional[str] = Field(None, env="PROD_SPARKAI_APP_ID")
    SPARKAI_API_KEY: Optional[str] = Field(None, env="PROD_SPARKAI_API_KEY")
    SPARKAI_API_SECRET: Optional[str] = Field(None, env="PROD_SPARKAI_API_SECRET")
    SPARKAI_DOMAIN: Optional[str] = Field(None, env="PROD_SPARKAI_DOMAIN")

    # 百度服务
    BAI_DU_API_KEY: Optional[str] = Field(None, env="PROD_BAI_DU_API_KEY")
    BAI_DU_SECRET_KEY: Optional[str] = Field(None, env="PROD_BAI_DU_SECRET_KEY")

    # 认证服务
    SSO_RPC_SERVER: Optional[str] = Field(None, env="PROD_SSO_RPC_SERVER")

    # 钉钉消息提醒
    BUG_DD_TOKEN: Optional[str] = Field(None, env="PROD_BUG_DD_TOKEN")
    BUG_DD_SECRET: Optional[str] = Field(None, env="PROD_BUG_DD_SECRET")

    #  Consul
    CONSUL_HOST: Optional[str] = Field(None, env="PROD_CONSUL_HOST")
    CONSUL_PORT: Optional[str] = Field(None, env="PROD_CONSUL_PORT")

    # 短信模版id
    SMS_TEMPLATE_ID: Optional[str] = Field(None, env="PROD_SMS_TEMPLATE_ID")


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
