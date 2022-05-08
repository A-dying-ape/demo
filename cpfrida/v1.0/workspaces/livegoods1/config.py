# !/usr/bin/env python
# coding=utf-8


import os


# 项目根目录
project_path = r"E:\workspace\wx_project\备份\vx_pro_v5.0"
# 工作空间等待js响应最大时长
timeout = 150
# frida远程IP端口
frida_host = r"172.23.10.158:10454"
# adb远程IP端口
adb_host = r"172.23.10.158:10454"
# app英文包名
app_name_en = r"com.tencent.mm"
# app中文包名
app_name_ch = r"微信"
# 当app卡死要激活的UI
app_ui = r"com.tencent.mm/com.tencent.mm.ui.LauncherUI"
# 工作空间的uuid路径
uuid_path = os.path.join(os.path.join(os.path.join(project_path, "workspaces"), r"livegoods1"), "uuid")
# hook脚本路径
hook_script = os.path.join(os.path.join(project_path, "hookscript"), r"vx_hooker_8018.js")
# 请求地址
get_url = {"livegoods": "http://172.23.10.70:8187/liveproduct/8015/task?uuid={}&host={}"}
# 回调地址
post_url = {"detail": "http://172.23.10.70:8181/detail/8018/callback?uuid={}&ip={}", "topic": "http://172.23.10.70:8181/topic/8018/callback?uuid={}&host={}", "comment": "http://172.23.10.70:8182/comment/8018/callback?uuid={}&host={}", "livebarrage": "http://172.23.10.70:8187/livedanmu/8018/callback?uuid={}&ip={}", "liveinfo": "http://172.23.10.70:8187/live/8018/callback?uuid={}&host={}", "livecontribution": "http://172.23.10.70:8187/live/8018/callback?uuid={}&host={}", "livegoods": "http://172.23.10.70:8187/live/8018/callback?uuid={}&host={}", "livesquare": "http://172.23.10.70:8186/livesquare/8018/callback?uuid={}&host={}", "product": "http://172.23.10.70:8180/product/8018/callback?uuid={}&ip={}", "videogoods": "http://172.23.10.70:8185/videoproduct/8018/callback?uuid={}&host={}", "hourlist": "http://172.23.10.70:8186/liverank/8018/callback?uuid={}&host={}", "videourl": "http://172.23.10.70:8184/videourl/7012/callback?uuid={}&host={}"}
# 登录的微信username
username = r"v2_060000231003b20faec8c7e58d10c2d1c602ef3db0772ca223f45f0531b6505a14cf6f8d9134@finder"
# 消息通知
inform_url = r"https://open.feishu.cn/open-apis/bot/v2/hook/97b44a2e-1b80-4dea-bda7-6ebf2309e6ac"
