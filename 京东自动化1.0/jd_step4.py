from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time


cw = "1-A-01-01-2"
l = ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']


def get_bucket(driver):
    driver.find_element_by_css_selector(".topbar__whse-icon").click()
    time.sleep(0.5)
    driver.find_element_by_css_selector(".chg-btn").click()
    time.sleep(2)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.level-1:nth-child(7) > div:nth-child(1) > span:nth-child(2)")))
        time.sleep(3)
    except:
        print("获取云物流首页失败")
        driver.refresh()
        time.sleep(3)
        get_bucket(driver)
    else:
        driver.find_element_by_css_selector("li.level-1:nth-child(2) > div:nth-child(1) > span:nth-child(2)").click()
        time.sleep(0.5)
        driver.find_element_by_css_selector(".is-opened > ul:nth-child(2) > li:nth-child(1) > span:nth-child(2)").click()
        time.sleep(3)


def search_item(driver, page=1):
    time.sleep(5)
    flag = True
    Select(driver.find_element_by_css_selector("#purchaseTable_pager_size")).select_by_index(4)
    time.sleep(5)
    driver.find_element_by_css_selector("#purchaseTable_pager_goto").clear()
    driver.find_element_by_css_selector("#purchaseTable_pager_goto").send_keys(page)
    driver.find_element_by_css_selector("#purchaseTable_pager_goto_btn").click()
    time.sleep(8)
    tr_list = driver.find_elements_by_xpath("//*[@id=\"purchaseTable\"]/tbody/tr")
    for tr in tr_list:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#purchaseTable")))
        except:
            print("网络很差，平台很卡，打开失败")
            search_item(driver)
        else:
            if tr.find_element_by_xpath("./td[14]").text == "初始":
                tr.find_element_by_xpath("./td[17]/div/a[2]").click()
                time.sleep(8)
                driver.find_element_by_css_selector("#inboundPurchaseReceiveNewTable > thead:nth-child(1) > tr:nth-child(1) > th:nth-child(1) > input:nth-child(1)").click()
                driver.find_element_by_css_selector("#completeAsnWithoutContainer").click()
                time.sleep(3)
                driver.find_element_by_css_selector(".btn-ok").click()
                driver.refresh()
                flag = False
                break
    if flag:
        page += 1
    if (len(tr_list) < 100) and flag:
        return
    search_item(driver, page)


def up_paper(driver):
    driver.find_element_by_css_selector("li.is-active:nth-child(2) > ul:nth-child(2) > li:nth-child(4) > span:nth-child(2)").click()
    time.sleep(1)
    driver.switch_to.frame("nest-other-iframe")
    time.sleep(1)
    driver.find_element_by_css_selector("#queryPutaway").click()
    time.sleep(1)
    tr_list = driver.find_elements_by_xpath("//*[@id=\"putawayTable\"]/tbody/tr")
    for tr in tr_list:
        tr.find_element_by_xpath("./td[@class='opera']/a").click()
        time.sleep(60)
        tr_list1 = driver.find_elements_by_xpath("//*[@id=\"inboundPutawayOperateTable\"]/tbody/tr")
        for tr1 in tr_list1:
            text = tr1.find_element_by_xpath("./td[11]").get_attribute("title")
            if list(text) == l:
                tr1.find_element_by_xpath("./td[11]/input").send_keys(cw)
        time.sleep(0.5)
        driver.find_element_by_css_selector("#savePutawayBtn").click()
        time.sleep(10)
        driver.find_element_by_css_selector(".btn-ok").click()
        time.sleep(3)


def run4(driver):
    get_bucket(driver)
    driver.switch_to.frame("nest-other-iframe")
    search_item(driver)
    driver.switch_to.default_content()
    up_paper(driver)
    driver.quit()
