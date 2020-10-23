from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os


def check_cookie():
    flag = True
    temp_list = []
    with open("cookies.txt", "r") as f:
        while True:
            cookie = f.readline()
            if cookie:
                cookie = eval(cookie)
                temp_list.append(cookie)
                if cookie.get('expiry'):
                    end_time = cookie.get('expiry')
                    if end_time <= int(time.time()):
                        flag = False
            else:
                break
    return flag, temp_list


def login():
    driver1 = webdriver.Chrome(executable_path="./chromedriver.exe")
    driver1.get("https://login.1688.com/member/signin.htm?tracelog=member_signout_signin")
    driver1.maximize_window()
    while True:
        time.sleep(2)
        cookies = driver1.get_cookies()
        if len(cookies) > 15:
            print("账号已登录!")
            cookies = driver1.get_cookies()
            for c in cookies:
                with open("cookies.txt", "a") as f:
                    f.write(str(c) + '\n')
            break
    driver1.quit()


def get_info(cookie_list):
    options = Options()
    options.add_argument('headless')
    driver2 = webdriver.Chrome(executable_path="./chromedriver.exe")
    # driver2.get("https://work.1688.com/?tracelog=login_target_is_blank_1688")
    driver2.delete_all_cookies()
    info_list = []
    with open("./url.txt", "r") as f:
        while True:
            url = f.readline()
            if url:
                driver2.get(url)
                for c in cookie_list:
                    driver2.add_cookie(c)
                driver2.refresh()
                for i in range(15):
                    time.sleep(0.3)
                    driver2.execute_script('document.documentElement.scrollTop = 2000')
                try:
                    title = driver2.find_element_by_xpath("//*[@id=\"mod-detail-title\"]/h1").text + ","
                    img_list = driver2.find_elements_by_xpath("//*[@id=\"desc-lazyload-container\"]//img")
                except:
                    print("请用正常浏览请登录账号完成滑块反爬！")
                else:
                    temp_list = []
                    for i in img_list:
                        temp_list.append(i.get_attribute("src"))
                    for i in temp_list:
                        title += (i + ",")
                    print(title[:-1] + "\n")
                    info_list.append(title[:-1] + "\n")
            else:
                break
    with open("img.csv", "a") as f:
        for i in info_list:
            f.write(i)
    driver2.quit()
    print("图片已采集并保存在img.csv文件中！")


if __name__ == '__main__':
    if os.path.exists("cookies.txt"):
        flag, cookie_list = check_cookie()
        if flag:
            get_info(cookie_list)
        else:
            os.remove("cookies.txt")
            login()
    else:
        login()
        flag, cookie_list = check_cookie()
        get_info(cookie_list)