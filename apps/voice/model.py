from settings.db import BaseModel
from sqlalchemy import Column, INTEGER, VARCHAR, JSON


class VoiceModel(BaseModel):
    __tablename__ = 'speech_recognition'
    __cn_tablename__ = '语音识别'


