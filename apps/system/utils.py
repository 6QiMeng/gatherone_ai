# -*- coding: utf-8 -*-
import wrapt
from typing import Callable
from sqlalchemy import func, JSON, and_
from sqlalchemy.orm import Session, aliased
from apps.system.models import Permission, User, Role
from settings.db import SessionLocal
from utils.constant import RET, error_map
from utils.resp import MyResponse


# 权限初始化
def permission_init():
    # 将所有模型的增删改查权限添加到数据库
    from apps.account.models import custom_models as account_models
    from apps.approval.models import custom_models as approval_models
    from apps.common.models import custom_models as common_models
    from apps.contract.models import custom_models as contract_models
    from apps.customer.models import custom_models as customer_models
    from apps.finance.models import custom_models as finance_models
    from apps.marketing.models import custom_models as marketing_models
    from apps.message.models import custom_models as message_models
    from apps.report.models import custom_models as report_models
    from apps.system.models import custom_models as system_models, Action
    all_model = [*account_models, *approval_models, *common_models, *contract_models, *customer_models, *finance_models,
                 *marketing_models, *message_models, *report_models, *system_models]
    with SessionLocal() as db:
        actions = db.query(Action.action_code, Action.action_name)
        action_data = {i[0]: i[1] for i in actions}
        # 构造权限数据
        init_data = [
            {'permission_code': model.__name__ + ':' + code, 'permission_name': model.TABLE + ':' + action}
            for model in all_model
            for code, action in action_data.items() if hasattr(model, 'TABLE')
        ]
        # 清空并充置权限
        db.execute(f'TRUNCATE TABLE {Permission.__tablename__}')
        db.execute(
            Permission.__table__.insert(),
            init_data
        )  # 插入数据权限
        db.execute(f'UPDATE TABLE tb_roles SET permissions = "[]"')
        db.commit()


def admin_required(wrapped):
    @wrapt.decorator
    async def wrapper(wrapped, instance, args, kwargs):
        # 在这里添加自定义逻辑
        user = kwargs['self'].request.state.user
        if not user.is_superuser:
            return MyResponse(code=RET.PER_ERR, msg=error_map[RET.PER_ERR])
        return await wrapped(*args, **kwargs)

    return wrapper(wrapped)


def permission_required(model, action: str) -> Callable:
    """
    需要接口db参数依赖（非必传）
    model  模型类
    actions   INSERT/DELETE/UPDATE/SELECT/EXPORT
    """

    @wrapt.decorator
    async def wrapper(wrapped, instance, args, kwargs):
        # 在这里添加自定义逻辑
        db: Session = kwargs.get('db', SessionLocal())
        user = kwargs['self'].request.state.user
        if not user.is_superuser:
            subquery = db.query(User.role_id).filter(User.id == user.user_id).subquery('tu')
            user_alias = aliased(User, subquery)
            subquery2 = db.query(user_alias, Role.permissions).join(Role, user_alias.role_id == Role.id).subquery('tur')
            query = db.query(func.count(1)).select_from(subquery2).join(
                Permission, and_(func.json_contains(subquery2.c.permissions, Permission.id.cast(JSON)),
                                 Permission.permission_code == f'{str(model.__name__)}:{action}'))
            has_permission = query.scalar()
            if not has_permission:
                return MyResponse(code=RET.PER_ERR, msg=error_map[RET.PER_ERR])
        return await wrapped(*args, **kwargs)

    return wrapper
