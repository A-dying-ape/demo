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


def get_cookie(ap, updata_log):
    driver = login(ap)
    while True:
        driver = re_login(ap, driver)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"J_SiteNavLogin\"]/div[1]/div[2]/a")))
        if len(driver.get_cookies()) > 12:
            try:
                user_name = driver.find_element_by_xpath("//*[@id=\"J_SiteNavLogin\"]/div[1]/div[2]/a").get_attribute("text")
            except:
                text = ">>登陆成功, 账号:%s" % ap.get("account")
                updata_log.emit(text)
            else:
                text = ">>登录成功！当前用户:%s, 账号:%s" % (user_name, ap.get("account"))
                updata_log.emit(text)
            with open("cookies.txt", "a", encoding="gbk") as f1:
                f1.write(str(driver.get_cookies()) + "\n")
            with open("pay_pwd.txt", "a", encoding='gbk') as f2:
                f2.write(str(user_name) + "||" + ap.get("pay") + ap.get("account") + "\n")
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
                text = ">>登陆成功, 账号:%s" % ap.get("account")
                updata_log.emit(text)
            else:
                text = ">>登录成功！当前用户:%s, 账号:%s" % (user_name, ap.get("account"))
                updata_log.emit(text)
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
        driver = re_login(ap, driver)
    except:
        driver = login(ap)
    return driver


def main(q, updata_log):
    count = 0
    while True:
        if q.empty():
            time.sleep(0.5)
            if count >= 5:
                break
            count += 1
        else:
            # updata_log.emit(str(q.get()))
            get_cookie(q.get(), updata_log)


def run_cookie(account_list, updata_log, login_count):
    t_list = []
    for a in account_list:
        temp_dict = {}
        account = a.split("||")[0]
        password = a.split("||")[1]
        pay = a.split("||")[2].replace("\n", "")
        temp_dict["account"] = account
        temp_dict["password"] = password
        temp_dict["pay"] = pay
        q.put(temp_dict)
    login_count.emit(str(q.qsize()))
    if q.qsize() <= 6:
        for i in range(q.qsize()):
            t_list.append(threading.Thread(target=main, args=(q, updata_log)))
        for t in t_list:
            t.start()
    else:
        for i in range(6):
            t_list.append(threading.Thread(target=main, args=(q, updata_log)))
        for t in t_list:
            t.start()
