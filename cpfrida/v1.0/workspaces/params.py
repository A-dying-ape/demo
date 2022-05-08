# !/usr/bin/env python
# coding=utf-8
# @Time    : 2022/04/20
# @Author  : XQE
# @Software: PyCharm


import config


class FixedParams(object):
    # 微信的cookie
    vx_cookie = None
    # cookie本地缓存
    cookie_file = config.uuid_path.replace("uuid", "cookie")
    # 当前设备微信号的username
    username = config.username
    # 直播广场参数构造
    live_square_param = {
        "YBJ": [],
        "YBI": False,
        "YBK": 0,
        "includeUnKnownField": False,
        "YBD": 88890,
        "YBF": False,
        "YBE": "推荐",
        "object_id": 0,
        "YBH": False,
        "YBG": False
    }
    # 小时榜地区映射表
    area_tab = {
        "华南赛区": 1,
        "华北赛区": 2,
        "东北赛区": 3,
        "华东赛区": 4,
        "华中赛区": 5,
        "西南赛区": 6,
        "西北赛区": 7
    }
    # 带货中心商品一级分类映射表
    categoryId = {
        '全部': '0',
        '合作商品': '999',
        '幸福读书': '7190886376830668636',
        '食品生鲜': '11099070301657575487',
        '服饰鞋包': '16579416177373560313',
        '个护美妆': '17007902228422672609',
        '图书': '12377324634086192020',
        '家清日用': '8261345894708739273',
        '其他': '12379480883574690382'
    }
    # 带货中心二级分类映射表
    sortId = {
        '推荐': 0,
        '高佣金': 1,
        '价格': 2,
        '销量': 3
    }
    # 带货中心二级分类价格映射表
    orderType = {
        '升序': 2,
        '降序': 1
    }
    # 带货中心商品来源映射表
    srcPlatformInfo = {
        '全部': 0,
        '爱逛': 1,
        '微盟': 2,
        '魔筷': 3,
        '唯品会': 7,
        '当当': 12,
        '有赞': 13,
        '小程序联盟': 14
    }
    # 业务休眠
    sleep_time = {
        "comment": {
            "begin": 0,
            "end": 0
        },
        "detail": {
            "begin": 5,
            "end": 5
        },
        "hourlist": {
            "begin": 300,
            "end": 300,
            "each": 5
        },
        "livebarrage": {
            "begin": 10,
            "end": 10
        },
        "liveinfo": {
            "begin": 30,
            "end": 40
        },
        "livecontribution": {
            "begin": 0,
            "end": 0
        },
        "livegoods": {
            "begin": 3,
            "end": 3
        },
        "livesquare": {
            "begin": 120,
            "end": 180
        },
        "product": {
            "begin": 3,
            "end": 3
        },
        "topic": {
            "begin": 16,
            "end": 16
        },
        "videogoods": {
            "begin": 3,
            "end": 3
        },
        "videourl": {
            "begin": 0,
            "end": 0
        },
    }
    # 告警通知
    inform_text = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "设备风控通知",
                    "content": [
                        [
                            {
                                "tag": "text",
                                "text": "设备："
                            },
                            {
                                "tag": "text",
                                "text": "device",
                            },
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "状态："
                            },
                            {
                                "tag": "a",
                                "text": "点击查看设备状态",
                                "href": "http://youwant_device.xiguaji.com:8444/home/index"
                            },
                            {
                                "tag": "a",
                                "text": "点击查看设备回调情况",
                                "href": "http://inner_wxtoken.xiguaji.com/Monitor/GetWxVideoDeviceList"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "操作描述："
                            },
                            {
                                "tag": "text",
                                "text": "当前设备hook回调的数据多次异常，设备存在被风控的风险，现在自动剔除运维名单，请确认后手动添加回运维名单中。"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "异常详情："
                            },
                            {
                                "tag": "text",
                                "text": "err_msg"
                            }
                        ]
                    ]
                }
            }
        }
    }