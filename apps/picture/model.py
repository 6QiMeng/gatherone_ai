from settings.db import BaseModel
from sqlalchemy import Column, INTEGER, VARCHAR, JSON


class TextToImageModel(BaseModel):
    __tablename__ = 'ai_word_to_picture'
    __cn_tablename__ = 'AI文生图'

    user_id = Column(INTEGER(), comment="提交人id")
    img_url = Column(VARCHAR(255), default="", comment="图片")


