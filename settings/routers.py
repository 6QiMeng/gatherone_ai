# -*- coding: utf-8 -*-
from settings.base import configs
from fastapi import FastAPI


def router_init(app: FastAPI):
    pass
    # from apps.finance.views import FinanceRouter
    # from apps.account.views import AccountRouter
    # from apps.contract.views import ContractRouter
    # from apps.customer.views import CustomerRouter
    # from apps.system.views import SystemRouter
    # from apps.approval.views import ApprovalRouter
    # from apps.marketing.views import MarketingRouter
    # from apps.message.views import MessageRouter
    # from apps.report.views import ReportRouter
    # from apps.common.views import CommonRouter
    # from apps.assignment.views import AssignMentRouter
    #
    # # 注册路由
    # # 财务管理
    # app.include_router(FinanceRouter, prefix=f'{configs.API_VERSION_STR}/finance')
    # # 公共
    # app.include_router(CommonRouter, prefix=f'{configs.API_VERSION_STR}/common')
    # # 开户管理
    # app.include_router(AccountRouter, prefix=f'{configs.API_VERSION_STR}/accounts')
    # # 合同
    # app.include_router(ContractRouter, prefix=f'{configs.API_VERSION_STR}/contracts')
    # # 客户
    # app.include_router(CustomerRouter, prefix=f'{configs.API_VERSION_STR}/customer')
    # # 系统管理
    # app.include_router(SystemRouter, prefix=f'{configs.API_VERSION_STR}/systems')
    # # 审批管理
    # app.include_router(ApprovalRouter, prefix=f'{configs.API_VERSION_STR}/approvals')
    # # 营销管理
    # app.include_router(MarketingRouter, prefix=f'{configs.API_VERSION_STR}/markets')
    # # 消息提醒
    # app.include_router(MessageRouter, prefix=f'{configs.API_VERSION_STR}/messages')
    # # 报表管理
    # app.include_router(ReportRouter, prefix=f'{configs.API_VERSION_STR}/reports')
    # # 任务管理
    # app.include_router(AssignMentRouter, prefix=f'{configs.API_VERSION_STR}/assignments')
