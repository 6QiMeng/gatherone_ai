from fastapi import FastAPI
from apps.ws.views import WSRouter
from settings.base import configs


def router_init(app: FastAPI):
    # 注册路由，例子
    from apps.system.views import SystemRouter
    from apps.voice.view import VoiceRouter

    app.include_router(SystemRouter, prefix=f'{configs.API_VERSION_STR}/systems')
    app.include_router(WSRouter, prefix=f'{configs.API_VERSION_STR}/ws')
    app.include_router(VoiceRouter, prefix=f'{configs.API_VERSION_STR}/voice')

