"""项目控制"""
# 开启日志调试
debug = True
# 开启控制台输出
console = False
# 刷新js响应休眠时间
refresh_js_time = 0.1
# frida对象创建失败休眠时间
each_create_frida_time = 5
# 获取hook参数休眠时间
get_hook_params_time = 2
# hook返回异常数据休眠时间
hook_message_err_time = 5

"""手机运维时长"""
# 连接手机 项目休眠时间
connect_phone_time = 1
# 关闭app 项目休眠时间
stop_app_time = 1
# 重启app 项目休眠时间
restart_app_time = 7
# 重启手机 项目休眠时长
reboot_phone_time = 60

"""业务"""
# 业务休眠
business_sleep_time = {
    # 视频评论
    "comment": {
        "begin": 0,
        "end": 0
    },
    # 博主主页
    "detail": {
        "begin": 8,
        "end": 8
    },
    # 小时榜
    "hourlist": {
        "begin": 300,
        "end": 300,
        "each": 5
    },
    # 弹幕信息
    "livebarrage": {
        "begin": 15,
        "end": 15
    },
    # 直播间详情
    "liveinfo": {
        "begin": 30,
        "end": 40
    },
    # 直播贡献度
    "livecontribution": {
        "begin": 0,
        "end": 0
    },
    # 直播带货
    "livegoods": {
        "begin": 0,
        "end": 0
    },
    # 直播广场
    "livesquare": {
        "begin": 180,
        "end": 300
    },
    # 云函数商品
    "product": {
        "begin": 0,
        "end": 0
    },
    # 活动话题
    "topic": {
        "begin": 17,
        "end": 20
    },
    # 视频挂链
    "videogoods": {
        "begin": 0,
        "end": 0
    },
    # 视频播放
    "videourl": {
        "begin": 0,
        "end": 0
    },
}

"""监控"""
# 进程池运行最大时长
main_process_pool_run_time = 60 * 60 * 6
# 达到最大时长的前两分钟(建议监控设置为一分钟巡查一次)
restart_phone_time = main_process_pool_run_time - 60 * 2
