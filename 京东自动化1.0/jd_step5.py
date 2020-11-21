from selenium.webdriver.support.select import Select
import time


def get_search(driver):
    driver.find_element_by_css_selector("#top_104202").click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id=\"li_9250\"]/a").click()
    time.sleep(3)
    driver.switch_to.frame("mainIframe")
    Select(driver.find_element_by_css_selector("#shopGoodsList_shopGoods-table_length > label > select")).select_by_index(3)
    time.sleep(3)
    get_tr(driver)
    driver.find_element_by_css_selector("#shopGoodsList_handleJdDeliver").click()
    time.sleep(1)
    driver.find_element_by_css_selector("body > div.bootbox.modal.fade.in > div > div > div.modal-footer > button.btn.btn-primary").click()
    time.sleep(40)
    result = driver.find_element_by_css_selector("#lblSysInfo").text
    print("京东打标结果" + result)


def get_tr(driver):
    if driver.find_element_by_css_selector("#shopGoodsList_shopGoods-table_paginate > ul > li.next > a").get_attribute("class") == "next disabled":
        return
    tr_list = driver.find_elements_by_css_selector("#shopGoodsList_shopGoods-table > tbody > tr")
    for tr in tr_list:
        if tr.find_element_by_xpath("./td[10]/input").get_attribute("disabled") is None:
            if tr.find_element_by_xpath("./td[10]/input").get_attribute("checked") is None:
                tr.find_element_by_xpath("./td[10]/input").click()
    driver.find_element_by_css_selector("#shopGoodsList_shopGoods-table_paginate > ul > li.next > a").click()
    time.sleep(3)
    get_tr(driver)


def run5(driver):
    get_search(driver)
