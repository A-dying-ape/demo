import requests
from workspace.login import Login
from setting import PROXY, HEADERS


session = requests.session()


if __name__ == '__main__':
    lg = Login(session, HEADERS ,PROXY)
    lg.run()