from fastapi import FastAPI
from middlewares import middleware_init
from settings.routers import router_init


def create_app():
    app = FastAPI()

    # 初始化中间件
    middleware_init(app)

    # 初始化路由
    router_init(app)

    return app
