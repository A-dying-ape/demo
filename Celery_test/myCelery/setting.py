# 官方文档：https://docs.celeryproject.org/en/stable/userguide/routing.html
### 基础配置 ###

# 使用Redis作为消息代理
BROKER_URL = 'redis://:@127.0.0.1:6379/1'
# BROKER_URL = 'redis://:123456@127.0.0.1:6379/1'
# 把任务结果存在了Redis
CELERY_RESULT_BACKEND = 'redis://:@127.0.0.1:6379/0'
# CELERY_RESULT_BACKEND = 'redis://:123456@127.0.0.1:6379/0'
# 任务序列化和反序列化使用msgpack方案
CELERY_TASK_SERIALIZER = 'msgpack'
# 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
CELERY_RESULT_SERIALIZER = 'json'
# 任务过期时间
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
# 指定接受的内容类型
CELERY_ACCEPT_CONTENT = ['json', 'msgpack']
# 指定时间为utc
TIMEZONE = 'asia/shanghai'
ENABLE_UTC = False
# 配置路由
TASK_ROUTES = {'queue': 'my_queue'}


