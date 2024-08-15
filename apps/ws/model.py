from settings.db import BaseModel
from sqlalchemy import Column, INTEGER, VARCHAR


class TalkModel(BaseModel):
    __tablename__ = 'tb_talks'
    __cn_tablename__ = '会话概括'
    user_id = Column(INTEGER, comment="用户id")


class TalkModelDetail(BaseModel):
    __tablename__ = 'tb_talk_detail'
    __cn_tablename__ = '会话详细'

    talk_id = Column(INTEGER, comment="会话主表id")
    content = Column(VARCHAR(10000), comment="对话内容")

