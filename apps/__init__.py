# -*- coding: utf-8 -*-
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from middlewares import middleware_init
from settings.routers import router_init


def create_app():
    app = FastAPI()

    # 初始化中间件
    middleware_init(app)

    # 初始化路由
    router_init(app)

    # 注册静态文件目录
    # os.makedirs('./static', exist_ok=True)
    # app.mount("/api/v1/static", StaticFiles(directory="static"), name="static")
    return app
