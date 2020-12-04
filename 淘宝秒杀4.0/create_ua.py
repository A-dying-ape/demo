from faker import Factory


def user_agent():
    """生成不同的谷歌浏览器的user-agent"""
    fc = Factory.create()
    return fc.chrome()