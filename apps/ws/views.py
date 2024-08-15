from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect
from settings.log import log_error,log_info
from apps.ws.utils import WebsocketServer

WSRouter = APIRouter(tags=['ws'])


@WSRouter.websocket('/{user_id}')
async def websocket_endpoint(user_id: int, websocket: WebSocket):
    """
    备用方案，广播,所有人都能接到消息
    """
    try:
        await WebsocketServer().connect(websocket=websocket, user_id=user_id)
        await WebsocketServer().to_do(websocket=websocket, user_id=user_id)
    except WebSocketDisconnect as e:
        log_info(f'{user_id}:已断开')
        await WebsocketServer().disconnect(user_id=user_id)
    except Exception as e:
        msg = f"websocket 异常: {e.__str__()}"
        log_error(msg)
