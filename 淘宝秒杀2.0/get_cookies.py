from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import threading
import queue


q = queue.Queue()


def get_cookie(ap, log_show):
    driver = login(ap)
    while True:
        driver = re_login(ap, driver)
        time.sleep(1)
        if len(driver.get_cookies()) > 12:
            try:
                user_name = driver.find_element_by_xpath("//*[@id=\"J_SiteNavLogin\"]/div[1]/div[2]/a").get_attribute("text")
            except:
                text = "登陆成功, 账号:%s" % ap.get("account")
                log_show(text)
            else:
                text = "登录成功！当前用户:%s, 账号:%s" % (user_name, ap.get("account"))
                log_show(text)
            with open("cookies.txt", "a", encoding="gbk") as f1:
                f1.write(str(driver.get_cookies()) + "\n")
            with open("pay_pwd.txt", "a", encoding='gbk') as f2:
                f2.write(str(user_name) + "||" + ap.get("pay") + "\n")
            driver.quit()
            break
        else:
            slider = driver.find_element_by_xpath("//*[@id=\"nc_1_n1z\"]")
            action = ActionChains(driver)
            action.drag_and_drop_by_offset(slider, 280, 0).perform()
            driver.find_element_by_xpath("//*[@id=\"login-form\"]/div[4]/button").click()
            try:
                user_name = driver.find_element_by_xpath("//*[@id=\"J_SiteNavLogin\"]/div[1]/div[2]/a").get_attribute("text")
            except:
                text = "登陆成功, 账号:%s" % ap.get("account")
                log_show(text)
            else:
                text = "登录成功！当前用户:%s, 账号:%s" % (user_name, ap.get("account"))
                log_show(text)
            with open("cookies.txt", "a", encoding="gbk") as f:
                f.write(str(driver.get_cookies()) + "\n")
                driver.quit()
                break


def re_login(ap, driver):
    driver.get("https://login.taobao.com/member/login.jhtml")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"login-form\"]/div[4]/button")))
        driver.find_element_by_xpath("//*[@id=\"fm-login-id\"]").send_keys(ap.get("account"))
        driver.find_element_by_xpath("//*[@id=\"fm-login-password\"]").send_keys(ap.get("password"))
        driver.find_element_by_xpath("//*[@id=\"login-form\"]/div[4]/button").click()
    except:
        re_login(ap, driver)
    return driver


def login(ap):
    options = Options()
    options.add_argument('headless')
    try:
        driver = webdriver.Chrome("chromedriver.exe", options=options)
        driver.maximize_window()
        driver = re_login(ap, driver)
    except:
        driver = login(ap)
    return driver


def main(q, log_show):
    count = 0
    while True:
        if q.empty():
            time.sleep(0.5)
            if count >= 5:
                break
            count += 1
        else:
            get_cookie(q.get(), log_show)


def run_cookie(path, messagebox, log_show):
    flag = 0
    t_list = []
    with open(path, "r", encoding="utf-8") as f:
        while True:
            temp_dict = {}
            content = f.readline()
            if content:
                account = content.split("||")[0]
                password = content.split("||")[1]
                pay = content.split("||")[2].replace("\n", "")
                temp_dict["account"] = account
                temp_dict["password"] = password
                temp_dict["pay"] = pay
                q.put(temp_dict)
                flag += 1
            else:
                break
    if flag <= 0:
        messagebox.showwarning(title="提示", message="读取的%s文件为空，请检查！" % path)
    elif flag <= 6:
        for i in range(flag):
            t_list.append(threading.Thread(target=main, args=(q, log_show)))
        for t in t_list:
            t.start()
    else:
        flag = 6
        for i in range(flag):
            t_list.append(threading.Thread(target=main, args=(q, log_show)))
        for t in t_list:
            t.start()