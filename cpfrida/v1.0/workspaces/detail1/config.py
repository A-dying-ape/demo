# !/usr/bin/env python
# coding=utf-8


import os


# 项目根目录
project_path = r"E:\workspace\wx_project\备份\v1.0"
# 工作空间等待js响应最大时长
timeout = 150
# frida远程IP端口
frida_host = r"114.114.114.114:10402"
# adb远程IP端口
adb_host = r"114.114.114.114:10702"
# app英文包名
app_name_en = r"com.tencent.mm"
# app中文包名
app_name_ch = r"微信"
# 当app卡死要激活的UI
app_ui = r"com.tencent.mm/com.tencent.mm.ui.LauncherUI"
# 工作空间的uuid路径
uuid_path = os.path.join(os.path.join(os.path.join(project_path, "workspaces"), r"detail1"), "uuid")
# hook脚本路径
hook_script = os.path.join(os.path.join(project_path, "hookscript"), r"vx_hooker_8018.js")
# 请求地址
get_url={"comment": "http://114.114.114.114:8182/comment/8015/task?uuid={}&host={}", "detail": "http://114.114.114.114:8181/detail/8015/task?uuid={}&host={}", "livebarrage": "http://114.114.114.114:8187/livedanmu/8015/task?uuid={}&ip={}", "liveinfo": "http://114.114.114.114:8187/live/8015/task?uuid={}&host={}", "livecontribution": "http://114.114.114.114:8187/liveonlineuser/8015/task?uuid={}&host={}", "livegoods": "http://114.114.114.114:8187/liveproduct/8015/task?uuid={}&host={}", "livesquare": "http://114.114.114.114:8186/livesquare/8015/task?uuid={}&host={}", "product": "http://114.114.114.114:8180/product/8015/task?uuid={}&ip={}", "topic": "http://114.114.114.114:8181/topic/8015/task?uuid={}&host={}", "videogoods": "http://114.114.114.114:8185/videoproduct/8015/task?uuid={}&host={}", "hourlist": "http://114.114.114.114:8186/liverank/8015/task?uuid={}&host={}", "videourl": "http://114.114.114.114:8184/videourl/7012/task?uuid={}&host={}"}
# 回调池
post_url={"comment": "http://114.114.114.114:8182/comment/8015/callback?uuid={}&host={}", "detail": "http://114.114.114.114:8181/detail/8015/callback?uuid={}&host={}", "livebarrage": "http://114.114.114.114:8187/livedanmu/8015/callback?uuid={}&ip={}", "liveinfo": "http://114.114.114.114:8187/live/8015/callback?uuid={}&host={}", "livecontribution": "http://114.114.114.114:8187/live/8015/callback?uuid={}&host={}", "livegoods": "http://114.114.114.114:8187/live/8015/callback?uuid={}&host={}", "livesquare": "http://114.114.114.114:8186/livesquare/8015/callback?uuid={}&host={}", "product": "http://114.114.114.114:8180/product/8015/callback?uuid={}&ip={}", "topic": "http://114.114.114.114:8181/topic/8015/callback?uuid={}&host={}", "videogoods": "http://114.114.114.114:8185/videoproduct/8015/callback?uuid={}&host={}", "hourlist": "http://114.114.114.114:8186/liverank/8015/callback?uuid={}&host={}", "videourl": "http://114.114.114.114:8184/videourl/7012/callback?uuid={}&host={}"}
# 登录的微信username
username = r""
# 消息通知
inform_url = r"https://open.feishu.cn/open-apis/bot/v2/hook/1234"
