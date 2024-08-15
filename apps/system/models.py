from settings.db import BaseModel
from sqlalchemy import Column, VARCHAR


# 用户
class UserModel(BaseModel):
    __tablename__ = 'ai_users'

    mobile = Column(VARCHAR(20), unique=True, comment='手机号')
    user_name = Column(VARCHAR(20), default='', comment='姓名')
    avatar_url = Column(VARCHAR(200), default='', comment='头像')
    password = Column(VARCHAR(500), default='', comment='密码')
