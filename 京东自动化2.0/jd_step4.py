from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


l = ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']


def get_bucket(driver):
    driver.find_element_by_css_selector(".topbar__whse-icon").click()
    time.sleep(0.5)
    driver.find_element_by_css_selector(".chg-btn").click()
    time.sleep(2)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.level-1:nth-child(7) > div:nth-child(1) > span:nth-child(2)")))
        time.sleep(3)
        driver.find_element_by_css_selector("li.level-1:nth-child(2) > div:nth-child(1) > span:nth-child(2)").click()
        time.sleep(0.5)
        driver.find_element_by_css_selector(".is-opened > ul:nth-child(2) > li:nth-child(1) > span:nth-child(2)").click()
        time.sleep(3)
    except:
        print("获取云物流首页失败")
        driver.refresh()
        time.sleep(3)
        get_bucket(driver)


def search_item(driver, page=1):
    time.sleep(20)
    flag = True
    try:
        driver.switch_to.frame("nest-other-iframe")
        driver.find_element_by_css_selector("#queryForm").click()
        time.sleep(15)
        total_page = int(driver.find_element_by_css_selector("#purchaseTable_pager_count").text)
        driver.find_element_by_css_selector("#purchaseTable_pager_goto").clear()
        driver.find_element_by_css_selector("#purchaseTable_pager_goto").send_keys(page)
        driver.find_element_by_css_selector("#purchaseTable_pager_goto_btn").click()
        time.sleep(10)
    except:
        print("获取采购入库详情页失败，重新获取！！！")
        driver.refresh()
        search_item(driver, page)
    else:
        try:
            tr_list = driver.find_elements_by_xpath("//*[@id=\"purchaseTable\"]/tbody/tr")
            for tr in tr_list:
                if tr.find_element_by_xpath("./td[14]").text == "初始":
                    tr.find_element_by_xpath("./td[17]/div/a[2]").click()
                    time.sleep(30)
                    driver.find_element_by_css_selector("#inboundPurchaseReceiveNewTable > thead:nth-child(1) > tr:nth-child(1) > th:nth-child(1) > input:nth-child(1)").click()
                    time.sleep(1)
                    driver.find_element_by_css_selector("#completeAsnWithoutContainer").click()
                    time.sleep(3)
                    driver.find_element_by_css_selector(".btn-ok").click()
                    time.sleep(50)
                    driver.refresh()
                    flag = False
        except:
            print("网络很差，平台很卡，打开验收表单失败，重新刷新网页！！！")
            search_item(driver, page)
        if flag:
            page += 1
        print(page, total_page)
        if int(total_page) < page:
            print("验收完成！！！")
            return
        else:
            search_item(driver, page)


def login(driver):
    driver.get("https://ups.jclps.com/login?ReturnUrl=http%3A%2F%2Fjwms.jclps.com%2F%3FloginType%3Dtenant")
    driver.maximize_window()
    while True:
        time.sleep(0.5)
        if len(driver.get_cookies()) >= 7:
            print("商家后台登录成功")
            break
    time.sleep(10)


def up_paper(driver, sid):
    driver.switch_to.frame("nest-other-iframe")
    try:
        driver.find_element_by_css_selector("#queryPutaway").click()
        time.sleep(5)
        tr_list = driver.find_elements_by_xpath("//*[@id=\"putawayTable\"]/tbody/tr")
        for tr in tr_list:
            tr.find_element_by_xpath("./td[@class='opera']/a").click()
            time.sleep(30)
            tr_list1 = driver.find_elements_by_xpath("//*[@id=\"inboundPutawayOperateTable\"]/tbody/tr")
            for tr1 in tr_list1:
                text = tr1.find_element_by_xpath("./td[11]").get_attribute("title")
                if list(text) == l:
                    tr1.find_element_by_xpath("./td[11]/input").send_keys(sid)
            time.sleep(0.5)
            driver.find_element_by_css_selector("#savePutawayBtn").click()
            time.sleep(60)
            driver.find_element_by_css_selector(".btn-ok").click()
            time.sleep(3)
    except:
        print("上架完成，继续上架！！！")
        driver.refresh()
        time.sleep(15)
        up_paper(driver, sid)


def get_uppaper(driver):
    driver.switch_to.default_content()
    try:
        driver.find_element_by_css_selector("li.level-1:nth-child(2) > div:nth-child(1) > span:nth-child(2)").click()
        time.sleep(1)
        driver.find_element_by_css_selector(".is-opened > ul:nth-child(2) > li:nth-child(4) > span:nth-child(2)").click()
        time.sleep(10)
    except:
        print("打开纸单上架失败，重新打开")
        driver.refresh()
        time.sleep(15)
        up_paper(driver)


def get_save_id(driver):
    time.sleep(5)
    driver.switch_to.default_content()
    driver.find_element_by_css_selector("li.level-1:nth-child(1) > div:nth-child(1) > span:nth-child(2)").click()
    time.sleep(1)
    driver.find_element_by_css_selector(".is-opened > ul:nth-child(2) > li:nth-child(2) > div:nth-child(1) > span:nth-child(2)").click()
    time.sleep(1)
    driver.find_element_by_css_selector("li.is-opened:nth-child(2) > ul:nth-child(2) > li:nth-child(3) > span:nth-child(1)").click()
    time.sleep(10)
    driver.switch_to.frame("nest-other-iframe")
    sid = driver.find_element_by_css_selector("#locationInfoTable > tbody:nth-child(2) > tr:last-child > td:nth-child(3)").text
    return sid


def run4(driver):
    login(driver)
    get_bucket(driver)
    search_item(driver)
    sid = get_save_id(driver)
    get_uppaper(driver)
    up_paper(driver, sid)
    driver.quit()
