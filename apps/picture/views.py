from fastapi import APIRouter, Request
from fastapi_utils.cbv import cbv
from apps.picture.define import TextToImageSchema
from settings.db import configs
from apps.picture.word_to_picture import main, parser_Message
from utils.constant import RET, error_map
from utils.resp import MyResponse

PictureRouter = APIRouter(tags=["文生图"])


@cbv(PictureRouter)
class PhotoView:
    requests: Request

    @PictureRouter.post('/word_to_picture', description="生成AI文生图")
    async def text_to_image(self, data: TextToImageSchema):
        res = main(
            data.desc, appid=configs.SPARKAI_APP_ID,
            apikey=configs.SPARKAI_API_KEY,
            apisecret=configs.SPARKAI_API_SECRET
        )
        code, data = parser_Message(res)
        if code != RET.OK:
            return MyResponse(code=code, msg=error_map[RET.THIRD_ERR])
        return MyResponse(code=code, msg="生成AI文生图成功", data={"img_url": data})
