# -*- coding: utf-8 -*-
import sys
import inspect
from settings.db import BaseModel
from sqlalchemy import Column, VARCHAR, Integer, Boolean, JSON, Enum
from sqlalchemy.orm import class_mapper


class Menu(BaseModel):
    __tablename__ = 'tb_menus'

    menu_path = Column(VARCHAR(50), comment='菜单路由')
    menu_name = Column(VARCHAR(50), comment='菜单名称')

    def __repr__(self):
        return '<Menu>{}:{}'.format(self.menu_name, self.menu_path)


class Action(BaseModel):
    __tablename__ = 'tb_actions'

    action_code = Column(VARCHAR(50), comment='行为代码')
    action_name = Column(VARCHAR(50), comment='行为名称')

    def __repr__(self):
        return '<Action>{}:{}'.format(self.action_code, self.action_name)


class Permission(BaseModel):
    __tablename__ = 'tb_permissions'

    permission_code = Column(VARCHAR(50), comment='权限代码')
    permission_name = Column(VARCHAR(50), comment='权限名称')

    def __repr__(self):
        return '<Permission>{}'.format(self.permission_name)


class Company(BaseModel):
    __tablename__ = 'tb_companies'

    name = Column(VARCHAR(20), comment='公司中文名')
    en_name = Column(VARCHAR(100), default='', comment='公司中文名')
    corp = Column(JSON, default=[], comment='法人id')

    def __repr__(self):
        return '<Company>{}'.format(self.name)


class Department(BaseModel):
    __tablename__ = 'tb_departments'

    company_id = Column(Integer, comment='公司id')
    name = Column(VARCHAR(20), comment='部门名称')
    leader = Column(JSON, default=[], comment='负责人id列表')

    def __repr__(self):
        return '<Department>{}'.format(self.name)


# 角色表
class Role(BaseModel):
    __tablename__ = 'tb_roles'

    department_id = Column(Integer, nullable=True, comment='部门id')
    name = Column(VARCHAR(20), comment='角色名称')
    permissions = Column(JSON, default=[], comment='权限id列表')

    def __repr__(self):
        return '<Role>{}'.format(self.name)


# 用户表
class User(BaseModel):
    __tablename__ = 'tb_users'

    mobile = Column(VARCHAR(11), unique=True, comment='手机号')
    real_name = Column(VARCHAR(20), default='', comment='真实姓名')
    email = Column(VARCHAR(50), default='', comment='电子邮箱')
    avatar_url = Column(VARCHAR(200), default='', comment='头像')
    is_active = Column(Boolean, default=1, comment='状态，是否可用，0-不可用，1-可用')
    role_id = Column(Integer, default=0, comment='角色id')
    is_superuser = Column(Boolean, default=False, comment='是否是超级管理员')
    assistant = Column(JSON, default=[], comment='助理id列表')

    def __repr__(self):
        return '<User>{}:{}'.format(self.real_name, self.mobile)


# 模块表
class Modules(BaseModel):
    __tablename__ = 'tb_modules'
    module_code = Column(VARCHAR(50), comment="模块代码")
    module_name = Column(VARCHAR(50), comment="模块名称")


# 操作日志
class OperateLog(BaseModel):
    __tablename__ = 'tb_operate_logs'

    module = Column(VARCHAR(100), default='', comment='系统模块')
    request_path = Column(VARCHAR(100), default='', comment='请求地址')
    request_user_id = Column(Integer, comment='操作人员')
    request_ip = Column(VARCHAR(50), default='', comment='操作IP')
    request_address = Column(VARCHAR(50), default='', comment='操作地址')
    request_status = Column(Enum('Success', 'Error'), default='Success', comment='操作状态')
    spent_time = Column(Integer, default=0, comment='消耗时间(毫秒)')
    session_id = Column(VARCHAR(100), default='', comment='会话编号')
    request_method = Column(VARCHAR(50), default='', comment='请求方式')
    required_params = Column(JSON(), nullable=True, comment='请求参数')
    return_params = Column(JSON(), nullable=True, comment='返回参数')
    operation = Column(VARCHAR(50), default='', comment='操作方法')

    def __repr__(self):
        return '<OperateLog>{}:{}:{}'.format(self.request_user_id, self.request_path, self.request_status)


classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
custom_models = []
for name, cls in classes:
    try:
        class_mapper(cls)
        custom_models.append(cls)
    except:
        continue
