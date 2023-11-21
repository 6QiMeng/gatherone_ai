# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import threading
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

# 设置环境变量
os.environ.setdefault('GatherOne xxx', 'settings.base.configs')


def make_celery():
    # 实例化
    app = Celery(
        'gatherone_crm', include=[

        ]
    )
    # 加载celery配置文件
    app.config_from_object('my_celery.config')

    return app


celery_app = make_celery()


# 异常处理函数
def handle_task_failure(sender=None, task_id=None, exception=None, args=None, kwargs=None, traceback=None, einfo=None,
                        **extra):
    from libs.ali.dingding import dd
    # 在这里处理任务执行失败的情况
    title = 'xxx系统Celery异步任务执行失败'
    err_msg = f"### {title}\n- 触发任务：{sender}\n- 任务ID：{task_id}\n- 异常：{exception}\n- 参数：{args}，{kwargs}\n- 堆栈追踪：{traceback}"
    t = threading.Thread(target=dd.send_err_message,
                         kwargs={'title': title, 'content': err_msg})
    t.start()


if __name__ == '__main__':
    args = ['worker', '--loglevel=INFO']
    celery_app.worker_main(argv=args)
