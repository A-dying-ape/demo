import time
import threading
import queue
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


q = queue.Queue()


def check_cookie():
    flag = True
    temp_list = []
    with open("cookies.txt", "r") as f:
        while True:
            cookie = f.readline()
            if cookie:
                cookie = eval(cookie)
                for c in cookie:
                    if c.get('expiry'):
                        end_time = c.get('expiry')
                        if end_time <= int(time.time()):
                            flag = False
                if flag:
                    temp_list.append(cookie)
            else:
                break
    return flag, temp_list


def snap_up(driver, log_show, user_name):
    try:
        driver.find_element_by_xpath("//*[@id=\"J_LinkBuy\"]").click()
        star_time = time.time()
    except:
        try:
            driver.find_element_by_xpath("//*[@id=\"J_LinkBuy\"]").click()
            star_time = time.time()
        except:
            text = "%s提交订单失败！" % user_name
            log_show(text)
            return
    else:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"submitOrderPC_1\"]/div/a")))
            end_time = time.time()
            driver.find_element_by_xpath("//*[@id=\"submitOrderPC_1\"]/div/a").click()
        except:
            text = "%s提交订单失败！" % user_name
            log_show(text)
            return
        else:
            use_time = end_time - star_time
            text = "%s抢单成功！用时%s秒" % (user_name, use_time)
            log_show(text)
            with open("pay_pwd.txt", "r") as f:
                while True:
                    content = f.readline()
                    if content:
                        if user_name == content.split("||")[0]:
                            check_pay = content.split("||")[1]
                    else:
                        break
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"lightPayForm\"]")))
                form = driver.find_element_by_xpath("//*[@id=\"lightPayForm\"]")
                form.find_element_by_xpath("//*[@id=\"payPassword_rsainput\"]").send_keys(check_pay)
                form.find_element_by_xpath("//*[@id=\"J_authSubmit\"]").click()
            except:
                text = "%s支付失败！" % user_name
                log_show(text)
            else:
                text = "%s支付成功！" % user_name
                log_show(text)
            return


def login(url, log_show, q):
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.get(url)
    driver.delete_all_cookies()
    for c in q.get():
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
            user_name = driver.find_element_by_xpath("//*[@id=\"login-info\"]/span[1]/a[1]").get_attribute("text")
            snap_up(driver, log_show, user_name)
            break


def run_login(url, log_show, messagebox):
    t_list = []
    flag, cookies_list = check_cookie()
    for cookies in cookies_list:
        q.put(cookies)
    if flag is False:
        log_show("cookie池已经过期，请重新登陆获取cookie!")
    else:
        flag = q.qsize()
        if flag <= 0:
            messagebox.showwarning(title="提示", message="读取的cookie缓存为空，请检查！")
        elif flag <= 6:
            for i in range(flag):
                t_list.append(threading.Thread(target=login, args=(url, log_show, q)))
            for t in t_list:
                t.start()
        else:
            flag = 6
            for i in range(flag):
                t_list.append(threading.Thread(target=login, args=(url, log_show, q)))
            for t in t_list:
                t.start()


if __name__ == '__main__':
    flag, cookies_list = check_cookie()
    if flag is False:
        print("cookie池已经过期，请重新登陆获取cookie!")
    else:
        url = "https://detail.tmall.com/item.htm?id=617488668593&ut_sk=1.X2WoDOe11iwDAJdJ3Z1%20V6eG_21380790_1604369930861.Copy.1&sourceType=item&price=1899&suid=E13FEBA6-42FE-4C94-A3D3-A9CB64EABB8E&shareUniqueId=4948054649&un=16ef415968f2f78503b7e2ef4c729fdd&share_crt_v=1&spm=a2159r.13376460.0.0&sp_tk=RHRaSWNRb3YxNWc=&cpp=1&shareurl=true&short_name=h.4cu4zuv&bxsign=scdxy0HxOHSkeqYUmJJeM4kVZipHK0h7iVEYFx197WyszlKDJ1U2amFeIkiThVH0JTjQJyt-469ULMuq_RygaIEOBQj9A4cd-I19GDYIORGnSI&sm=80f6eb"
        login(cookies_list, url)