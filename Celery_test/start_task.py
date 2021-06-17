# coding=utf-8
import time
from myCelery.tasks import add
from threading import Thread
from celery import group
from celery import chain


# 借助线程实现异步
def func_async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def get_result(result):
    print('Task Done:')
    print('  -->failed: {0}'.format(result.failed()))
    print('  -->successful: {0}'.format(result.successful()))
    print('  -->result: {0}'.format(result.get(propagate=False)))  # 获取结果，propagate=False如果异常不传递异常
    print('  -->result: {0}'.format(result.result))
    print('  -->status: {0}'.format(result.status))
    print('  -->traceback: {0}'.format(result.traceback))
    print('  -->children: {0}'.format(result.children))
    print('  -->task_id: {0}'.format(result.task_id))
    return result.ready()


@func_async
def by_chain():
    # 可以将任务链接在一起，以便在一个任务返回后又调用另一个任务,串行
    res = chain(add.s(10) | add.s(20))(10)  # add(add(10, 10), 20)
    print("**********链式处理结果：{0}***********".format(res.get()))
    print("**********链式处理父的结果：{0}***********".format(res.parent.get()))  # 一个parent对应一个父结果


@func_async
def by_group():
    # 并行调用任务列表，它返回一个特殊的结果实例，该实例使您可以将结果作为一个组进行检查，并按顺序检索返回值。
    res_list = group(add.s(i, i) for i in range(3, 10))().get()  # 分组处理
    print("########分组处理结果：{0}#########".format(res_list))


@func_async
def listen(result):
    print(result.task_id)
    while not result.ready():
        time.sleep(1)
    else:
        return get_result(result)


if __name__ == '__main__':
    # 启动数个任务,异步启动，不影响主程序
    # r1 = add.delay(1, 1)
    r2 = add.apply_async((2, 2), queue='my_queue', countdown=5)  # 指定任务队列和延后运行时间
    # d1 = delete.delay("task1")
    # d2 = delete.s("task2")
    # res = d2.delay()
    # d3 = delete.apply_async(("task3", ), queue='my_queue', countdown=10)
    # task_list = [r1, r2, d1, d3]
    # # 程序异步执行监听以上任务
    # for ts in task_list:
    #     listen(ts)
    # # 异步调用分组处理
    # by_group()
    # # 代表程序异步执行主逻辑
    # for i in range(10):
    #     time.sleep(2)
    #     print("程序继续走！！！")
    # print("-->signature result: {0}".format(res.get()))
    # ##异步调用链条处理,要和分组处理错开
    # # by_chain()