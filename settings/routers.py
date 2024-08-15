from fastapi import FastAPI
from settings.base import configs


def router_init(app: FastAPI):
    # 注册路由
    from apps.picture.views import PictureRouter
    from apps.system.views import SystemRouter

    app.include_router(PictureRouter, prefix=f'{configs.API_VERSION_STR}/picture')
    app.include_router(SystemRouter, prefix=f'{configs.API_VERSION_STR}/system')
