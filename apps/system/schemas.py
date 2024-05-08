# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field


class AllotRoleModel(BaseModel):
    """
    角色权限，例子
    """
    role_id: int
    permissions: list[int]
