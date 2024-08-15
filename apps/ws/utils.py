from starlette.websockets import WebSocket
from utils.common import SingletonType
from settings.log import log_error
from libs.spark.main import OpenAI_obj


class WebsocketServer(metaclass=SingletonType):
    users = dict()

    async def connect(self, websocket: WebSocket, user_id: int):
        """
        添加用户到聊天室，产品经理单独一个房间
        """
        await websocket.accept()
        try:
            if user_id in self.users.keys():
                self.users[user_id].close()
        except Exception as e:
            log_error(f'{user_id}连接错误,原因{e.__str__()}')
        finally:
            self.users[user_id] = websocket

    async def disconnect(self, user_id: int):
        self.users.pop(user_id, '')

    async def __send_personal_message(self, message, user_id: int):

        websocket = self.users.get(user_id)
        try:
            res = OpenAI_obj.ask_question('user', message)
            if websocket:
                for i in res:
                    if i.code == 0:
                        await websocket.send_json({'msg': i.choices[0].delta.content})
                    else:
                        await websocket.send_json({'msg': "回复出现错误，请稍后重试~"})
        except Exception as e:
            log_error(f'发送失败，原因：{e.__str__()}')

    async def __broadcast_to_room(self, message) -> None:
        """
        广播到所有人
        """
        for k, v in self.users.items():
            v.send_text(message)

    async def to_do(self, websocket: WebSocket, user_id: int):
        while True:
            message = await websocket.receive_text()
            try:
                await self.__send_personal_message(message, user_id)
            except Exception as e:
                log_error(f'初始化任务失败，原因{e.__str__()}')
