import time
import sys
sys.path.append("..")
from myCelery.start_celery import app
from celery.utils.log import get_task_logger


# 日志模块
logger = get_task_logger(__name__)


# 任务一
@app.task(name="add.task")
def add(x, y):
    z = x + y
    # 假设这里在执行下载任务花时久
    time.sleep(5)
    logger.info('***add result is {0} !'.format(z))
    return z


# 任务二
@app.task(name='del.task')
def delete(s):
    # 假设这里在执行删除任务花时久
    time.sleep(5)
    logger.info('***{0} already delete !'.format(s))
    return "%s already delete !" % s