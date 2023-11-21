# -*- coding: utf-8 -*-
from settings.base import configs
from kombu import Exchange, Queue

MQ_USERNAME = configs.MQ_USERNAME
MQ_PASSWORD = configs.MQ_PASSWORD
MQ_VIRTUAL_HOST = configs.MQ_VIRTUAL_HOST
MQ_HOST = configs.MQ_HOST
# worker
broker_url = f'amqp://{MQ_USERNAME}:{MQ_PASSWORD}@{MQ_HOST}/{MQ_VIRTUAL_HOST}'
# result_store
result_backend = f'redis://:{configs.REDIS_PASSWORD}@{configs.REDIS_HOST}:{configs.REDIS_PORT}/15'
# 用于存储计划的 Redis 服务器的 URL，默认为 broker_url的值
redbeat_redis_url = f'redis://:{configs.REDIS_PASSWORD}@{configs.REDIS_HOST}:{configs.REDIS_PORT}/14'
# 时区
timezone = 'Asia/Shanghai'
# UTC
enable_utc = False
# celery内容等消息的格式设置，默认json
accept_content = ['application/json', ]
task_serializer = 'json'
result_serializer = 'json'
# 为任务设置超时时间，单位秒。超时即中止，执行下个任务。
task_time_limit = 60
# 为存储结果设置过期日期，默认1天过期。如果beat开启，Celery每天会自动清除。
# 设为0，存储结果永不过期
result_expires = 300
# Worker并发数量，一般默认CPU核数，可以不设置
worker_concurrency = 5
# 每个worker执行了多少任务就会死掉，默认是无限的
# 防止内存泄漏
worker_max_tasks_per_child = 20
# 断开重连
broker_connection_retry_on_startup = True
# 定时任务
beat_scheduler = 'redbeat.RedBeatScheduler'
# 任务前缀
# redbeat_key_prefix = 'redbeat'
# RedBeat 使用分布式锁来防止多个实例同时运行。要禁用此功能，请设置：
# redbeat_lock_key = None
# # 配置交换机
# exchanges = {
#     'crm_charge': Exchange('crm_charge', type='direct'),
#     'crm_reset': Exchange('crm_reset', type='direct'),
#     'crm_common': Exchange('crm_common', type='direct'),
#     'crm_email': Exchange('crm_email', type='direct'),
# }
# # 配置队列
# queues = (
#     Queue(name='crm_charge', exchange=exchanges['crm_charge'], routing_key='crm_charge'),  # 充值队列
#     Queue(name='crm_reset', exchange=exchanges['crm_reset'], routing_key='crm_reset'),  # 清零队列
#     Queue(name='crm_common', exchange=exchanges['crm_common'], routing_key='crm_common'),  # 本系统异步队列
#     Queue(name='crm_email', exchange=exchanges['crm_email'], routing_key='crm_email'),  # 电子邮件队列
# )
# beat_schedule = {}
