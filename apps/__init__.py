from fastapi import FastAPI
from middlewares import middleware_init
from settings.routers import router_init
from settings.db import create_tb


def create_app():
    app = FastAPI()

    # 初始化中间件
    middleware_init(app)

    # 初始化路由
    router_init(app)

    # 创建表
    create_tb()

    return app
