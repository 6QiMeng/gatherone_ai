# -*- coding: utf-8 -*-
import datetime
from itertools import groupby
from operator import itemgetter
from fastapi_utils.cbv import cbv
from fastapi import Depends, APIRouter, Query
from sqlalchemy import desc, case, literal_column, func, or_
from sqlalchemy.orm import Session
from starlette.requests import Request
from apps.system.schemas import AllotRoleModel
from settings.base import configs
from settings.db import get_db, MyPagination
from utils.common import CommonQueryParams
from apps.system.models import Permission, User, OperateLog, Modules, Role
from utils.resp import MyResponse
from apps.system.utils import permission_required, admin_required, permission_init

SystemRouter = APIRouter(tags=['系统管理'])


@cbv(SystemRouter)
class LogServer:
    request: Request

    # 日志列表
    @SystemRouter.get('/log', description="日志列表")
    @permission_required(OperateLog, 'SELECT')
    async def GetLog(self, request_status: str = Query(None), common_query: CommonQueryParams = Depends(),
                     start_time: str = Query(None),
                     end_time: str = Query(None),
                     db: Session = Depends(get_db)):
        # 过滤掉日志记录查询接口请求
        query = [OperateLog.is_delete == False,
                 OperateLog.request_path.notin_([f'{configs.API_VERSION_STR}/systems/log', '/favicon.ico', '/', ''])]
        if common_query.q:
            user_id = db.query(User.id).filter(User.real_name.ilike(f'%{common_query.q}%'))
            query.append(or_(
                OperateLog.request_user_id.in_(user_id),
                OperateLog.request_path.like(f'%{common_query.q}%'),
                OperateLog.request_address.like(f'%{common_query.q}%')
            ))
        if request_status:
            query.append(OperateLog.request_status == request_status)
        if start_time and end_time:
            end_time = (datetime.datetime.strptime(end_time + " 00:00:00", "%Y-%m-%d %H:%M:%S") +
                        datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            query.append(OperateLog.created_time.between(start_time, end_time))
        anonymous_user = case([(OperateLog.request_user_id.is_(None), '匿名用户')],
                              else_=User.real_name)
        query = db.query(OperateLog.id, OperateLog.created_time, OperateLog.session_id, OperateLog.request_path,
                         Modules.module_name.label("module_name"),
                         anonymous_user.label("request_user"), OperateLog.request_status, OperateLog.spent_time,
                         (literal_column("CONCAT(spent_time, '毫秒')")).label("formatted_spent_time")).outerjoin(
            Modules, Modules.module_code == OperateLog.module).outerjoin(
            User, User.id == OperateLog.request_user_id).filter(*query)
        query = query.order_by(desc(OperateLog.id))
        obj = MyPagination(query, common_query.page, common_query.page_size)
        return MyResponse(total=obj.counts, data=obj.data)

    # 日志详情
    @SystemRouter.get('/log/{pk}', description="日志详情")
    @permission_required(OperateLog, 'SELECT')
    async def GetLogDetail(self, pk: int, common_query: CommonQueryParams = Depends(),
                           db: Session = Depends(get_db)):
        anonymous_user = case([(OperateLog.request_user_id.is_(None), '匿名用户')],
                              else_=User.real_name)
        query = db.query(OperateLog,
                         Modules.module_name.label("module_name"),
                         anonymous_user.label("request_user"),
                         (literal_column("CONCAT(spent_time, '毫秒')")).label("formatted_spent_time"),
                         OperateLog.request_address.label("login_message")).outerjoin(
            Modules, Modules.module_code == OperateLog.module).outerjoin(
            User, User.id == OperateLog.request_user_id).filter(OperateLog.id == pk)
        obj = MyPagination(query, common_query.page, common_query.page_size)
        return MyResponse(total=obj.counts, data=obj.data)
