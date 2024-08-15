from settings.db import BaseModel
from sqlalchemy import Column, INTEGER, VARCHAR, JSON


class VoiceModel(BaseModel):
    __tablename__ = 'tb_speech_recognition'
    __cn_tablename__ = '语音识别'

    file_name = Column(VARCHAR(200), default='', comment="上传的音频文件名字")
    file_url = Column(VARCHAR(200), default='', comment="上传的音频文件地址")
    translate = Column(VARCHAR(5000), default='', comment="翻译结果")
    user_id = Column(INTEGER, comment="用户id")
