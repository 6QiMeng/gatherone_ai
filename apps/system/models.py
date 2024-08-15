from sqlalchemy import Column, VARCHAR
from settings.db import BaseModel


class UserModel(BaseModel):
    __tablename__ = 'tb_users'
    __cn_tablename__ = '用户表'

    mobile = Column(VARCHAR(20), unique=True, comment='手机号')
    real_name = Column(VARCHAR(20), default='', comment='真实姓名')
    email = Column(VARCHAR(50), default='', comment='电子邮箱')
    avatar_url = Column(VARCHAR(200), default='', comment='头像')
    password = Column(VARCHAR(500), default='', comment='密码')
