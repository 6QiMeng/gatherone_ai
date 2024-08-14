from fastapi import APIRouter, Request
from fastapi_utils.cbv import cbv

VoiceRouter = APIRouter(tags=["AI语音平台"])


@cbv(VoiceRouter)
class VoiceView:
    requests: Request

    @VoiceRouter.post('/', description="语音转文字")
    async def voice_to_text_post(self, ):
        pass
