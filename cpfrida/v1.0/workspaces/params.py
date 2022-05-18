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

    """小时榜"""
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
    """带货中心"""
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

    """消息通知"""
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
                                "text": "业务信息："
                            },
                            {
                                "tag": "text",
                                "text": "business",
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
                                "text": "当前设备hook回调的数据多次异常，设备存在被风控的风险，请留意此设备"
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
