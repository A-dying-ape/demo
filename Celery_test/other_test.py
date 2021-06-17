from myCelery.tasks import add


# 根据任务ID获取想要的信息
task_id = "ba8fb2bb-0ea8-49c9-a7a0-3daddda5ddb9"
print(add.AsyncResult(task_id).get())  # 用propagate来覆盖异常
print(add.AsyncResult(task_id).status)
print(add.AsyncResult(task_id).traceback)
print(add.AsyncResult(task_id).children)