from fastapi import APIRouter, Request, UploadFile, File, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from sqlalchemy import or_
from libs.baidu.mian import BaiDuAPI
from utils.resp import MyResponse, RET
from utils.common import QueryResult, CommonQueryParams
from settings.log import log_error, log_info
from settings.db import get_db, MyPagination
from apps.voice.model import VoiceModel

VoiceRouter = APIRouter(tags=["AI语音平台"])


@cbv(VoiceRouter)
class VoiceView:
    requests: Request

    @VoiceRouter.get("/voices")
    async def voice_to_text_get(self, common_query: CommonQueryParams = Depends(), db: Session = Depends(get_db)):
        where = [VoiceModel.is_delete == 0]
        if common_query.q:
            where.extend(
                or_(
                    VoiceModel.file_name.ilike(f'%{common_query.q}%'),
                    VoiceModel.translate.ilike(f'%{common_query.q}%')
                )
            )
        query = db.query(VoiceModel).filter(*where)
        paginator = MyPagination(query, common_query.page, common_query.page_size)
        return MyResponse(data=paginator.data, total=paginator.counts)

    @VoiceRouter.get("/voices/{pk}")
    async def voice_to_text_get_one(self, pk: int, db: Session = Depends(get_db)):
        where = [VoiceModel.is_delete == 0, VoiceModel.id == pk, VoiceModel.user_id == self.requests.state.user.user_id]
        res = db.query(VoiceModel).filter(*where).first()
        return MyResponse(data=QueryResult.row_dict(res))

    @VoiceRouter.post('/voices', description="语音转文字")
    async def voice_to_text_post(self, file: UploadFile = File(...), db: Session = Depends(get_db)):
        """
        语音转文字接口
        """
        try:
            file_size = file.size
            content = await file.read()
            file_type = file.filename.split('.')[-1]
            if file_type not in ['pcm', 'wav', 'amr', 'm4a'] or file_size > 1024 * 1024 * 10:
                raise Exception("非法文件识别")
            res = BaiDuAPI().voice_to_text(content, file_type)
            if res.get("err_no") != 0:
                raise Exception("第三方接口调用失败")
            file_obj = VoiceModel(
                file_name=file.filename,
                translate=res.get("result", ''),
                user_id=self.requests.state.user.user_id
            )
            db.add(file_obj)
            db.commit()
        except Exception as e:
            log_error(f'语音转文字失败，原因：{e.__str__()}')
            return MyResponse(code=RET.DATA_ERR, msg="语音转文字失败，保障音频m4a格式,文件大小在10mb，请稍后重试！")
        return MyResponse(data=res.get("result", ''))
