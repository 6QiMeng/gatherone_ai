# -*- coding: utf-8 -*-
"""
统一队列任务启动接口
"""


# 充值任务提交
def recharge_task(func, args=None, kwargs=None, task_id=None, producer=None, link=None, link_error=None, **options):
    func.apply_async(args=args, kwargs=kwargs, task_id=task_id, producer=producer, link=link, link_error=link_error,
                     queue='crm_charge', **options)


# 清零任务提交
def reset_task(func, args=None, kwargs=None, task_id=None, producer=None, link=None, link_error=None, **options):
    func.apply_async(args=args, kwargs=kwargs, task_id=task_id, producer=producer, link=link, link_error=link_error,
                     queue='crm_reset', **options)


def email_task(func, args=None, kwargs=None, task_id=None, producer=None, link=None, link_error=None, **options):
    func.apply_async(args=args, kwargs=kwargs, task_id=task_id, producer=producer, link=link, link_error=link_error,
                     queue='email_task', **options)


# 本系统共用队列
def common_task(func, args=None, kwargs=None, task_id=None, producer=None, link=None, link_error=None, **options):
    func.apply_async(args=args, kwargs=kwargs, task_id=task_id, producer=producer, link=link, link_error=link_error,
                     queue='crm_common', **options)
