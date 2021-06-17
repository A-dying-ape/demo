from celery import Celery
from datetime import timedelta
from celery.schedules import crontab


# celery -A [文件名] worker -l [日志等级] -P [eventlet/gevent等多任务] -c [指定同时任务数量] -Q 指定队列[默认celery]
# 使用celery help来获取更多的参数说明
# celery -A tasks worker -l info -P eventlet -c 8 -Q my_queue,celery 运行任务队列
# 实例化celery,参数是对于的文件名（好像不是很严格）,include是对应的任务文件
app = Celery(__name__, include=["myCelery.tasks", ])
# 导入Celery相关配置
app.config_from_object('myCelery.setting')
# 定时任务
# app.conf.beat_schedule = {
#     "each10s_task": {
#         "task": "myCelery.tasks.add",
#         "schedule": timedelta(seconds=10),  # 每10秒钟执行一次
#         "args": (10, 10)
#     },
#     "each1m_task": {
#         "task": "tasks.add",
#         "schedule": crontab(minute=1),  # 每1分钟执行一次
#         "args": (10, 10)
#     },
#     "each1hours_task": {
#         "task": "tasks.add",
#         "schedule": crontab(hour=1),  # 每1小时执行一次
#         "args": (10, 10)
#     },
# }
