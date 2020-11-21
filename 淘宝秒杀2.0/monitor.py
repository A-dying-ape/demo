import time
import json
import spike_goods
import threading
from selenium import webdriver


def check_cookie():
    count = 0
    temp_list = []
    with open("cookies.txt", "r") as f:
        while True:
            flag = True
            cookie = f.readline()
            if cookie:
                cookie = eval(cookie)
                for c in cookie:
                    if c.get('expiry'):
                        end_time = c.get('expiry')
                        if end_time <= int(time.time()):
                            flag = False
                count += 1
                if flag:
                    temp_list.append(cookie)
            else:
                break
    return flag, temp_list, count


def login(url, log_show, cookie):
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.get(url)
    driver.delete_all_cookies()
    for c in cookie:
        driver.add_cookie(c)
    driver.refresh()
    time.sleep(1)
    try:
        driver.switch_to.frame("sufei-dialog-content")
    except:
        try:
            driver.find_element_by_xpath("//*[@id=\"login-info\"]/span[1]/a[1]").get_attribute("text")
        except:
            log_show("cookie过期，请重新登录！")
            return
    else:
        log_show("抢单页面遇到滑块,请过一会儿再尝试登录！")
        return
    while True:
        try:
            cur_time = driver.find_element_by_xpath("//*[@id=\"J_DetailMeta\"]/div[1]/div[1]/div/div[4]/div/div/div[3]/div[2]/div").text
            print(cur_time)
        except:
            log_show("-"*15 + "开始秒杀!" + "-"*15)
            with open("ip_pool", "r") as f:
                ip_pool = f.read()
            ip_pool = json.loads(ip_pool)
            cookie_list = []
            with open("cookies.txt", "r") as f:
                while True:
                    content = f.readline()
                    temp_dict = {}
                    if content:
                        for l in eval(content):
                            temp_dict[l.get("name")] = l.get("value")
                        cookie_list.append(temp_dict)
                    else:
                        break
            spike_goods.run(url, ip_pool, cookie_list, log_show)
            break


def run_login(url, log_show, messagebox):
    flag, cookies_list, count = check_cookie()
    if flag is False:
        log_show("cookie池已经过期，请重新登陆获取cookie!")
        return
    else:
        if count > 0:
            pass
        else:
            messagebox.showwarning(title="提示", message="读取的cookie缓存为空，请检查！")
            return
    threading.Thread(target=login, args=(url, log_show, cookies_list[0])).start()