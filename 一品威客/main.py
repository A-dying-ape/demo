import requests
from workspace.login import Login
from workspace.type_menu import Type_Menu
from workspace.promsg import Pro_Msg
from setting import DEMAND_ADDR


session = requests.session()


if __name__ == '__main__':
    # 登陆
    lg = Login(session)
    lg.run()
    # 获取分类信息
    for addr in DEMAND_ADDR:
        tm = Type_Menu(session, addr)
        sort_list = tm.run()
        # 获取项目信息
        pm = Pro_Msg(session, sort_list)
        pm.run()

