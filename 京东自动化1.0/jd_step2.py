from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import os
import time
from utils import excel


path_list = []


def get_department_code(driver):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#top_104202")))
        time.sleep(1)
    except:
        print("未找到基础资料！！！")
        driver.refresh()
        time.sleep(3)
        get_department_code(driver)
    else:
        driver.find_element_by_css_selector("#top_104202").click()
    time.sleep(1)
    driver.find_element_by_css_selector("#li_104197 > div").click()
    time.sleep(0.5)
    driver.find_element_by_xpath("//*[@id=\"9000\"]").click()
    time.sleep(2)
    driver.switch_to.frame("mainIframe")
    dc_id = driver.find_element_by_css_selector("#dept-table > tbody > tr > td.center.sorting_1").text
    time.sleep(0.5)
    driver.refresh()
    return dc_id


def get_search_page(driver):
    time.sleep(1)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#top_104202")))
        time.sleep(1)
    except:
        print("未找到基础资料！！！")
        driver.refresh()
        get_search_page(driver)
    else:
        driver.find_element_by_css_selector("#top_104202").click()
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"9250\"]")))
        time.sleep(1)
    except:
        print("未找到商品店铺管理！！！")
        driver.refresh()
        get_search_page(driver)
    else:
        driver.find_element_by_xpath("//*[@id=\"9250\"]").click()


def save_xls(temp_list, flag_xls):
    eme = excel.MakeExcel("商品物流属性导入", "GoodsLogisticsTemplate(2)({})".format(str(flag_xls)))
    xls_path = eme.make_base_excel([["事业部商品编码（若此列不为空，以此编码获取的商品为准）", "事业部编码（事业部商品编码为空时必填）", "商家商品编号（事业部商品编码为空时必填）", "长(mm)（必填，大于0）", "宽(mm)（必填，大于0）", "高(mm)（必填，大于0）", "净重(kg)", "毛重(kg)（必填，大于0）"]])
    path_list.append(os.path.abspath('.').replace("\\", "/") + "/" + xls_path)
    eme.white_excel_content(temp_list)


def search_sign(driver, sku_list, dc_id):
    if len(sku_list) <= 500:
        temp_list = []
        try:
            driver.switch_to.frame("mainIframe")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#shopGoodsList_isvGoodsNo")))
            time.sleep(3)
        except:
            print("商品店铺商品管理页面加载失败！！！")
        else:
            sl = ",".join(sku_list)
            driver.find_element_by_css_selector("#shopGoodsList_isvGoodsNo").clear()
            driver.find_element_by_css_selector("#shopGoodsList_isvGoodsNo").send_keys(sl)
            Select(driver.find_element_by_css_selector("#shopGoodsList_shopGoods-table_length > label > select")).select_by_index(3)
            driver.find_element_by_css_selector("#shopGoodsList_queryShopGoodsForm").click()
            time.sleep(20)
            while True:
                try:
                    tr_list = driver.find_elements_by_css_selector("#shopGoodsList_shopGoods-table > tbody > tr")
                except:
                    print(str(sl) + "未查询到任何信息！！！")
                else:
                    for tr in tr_list:
                        sl_list = []
                        try:
                            sign = tr.find_element_by_xpath("./td[4]").text
                            sl = tr.find_element_by_xpath("./td[6]").text
                        except:
                            search_sign(driver, sku_list, dc_id)
                        sl_list.append(sign)
                        sl_list.append(dc_id)
                        sl_list.append(str(sl))
                        sl_list.append("100")
                        sl_list.append("100")
                        sl_list.append("100")
                        sl_list.append("")
                        sl_list.append("1")
                        temp_list.append(sl_list)
                    try:
                        driver.find_element_by_xpath("//*[@id=\"shopGoodsList_shopGoods-table_paginate\"]/ul/li[@class='next disabled']")
                    except:
                        element = driver.find_element_by_xpath("//*[@id=\"shopGoodsList_shopGoods-table_paginate\"]/ul/li[5]/a")
                        driver.execute_script("arguments[0].click();", element)
                        time.sleep(1)

                    else:
                        break
            save_xls(temp_list, 1)
    else:
        temp_list = []
        flag_count = 1
        flag_xls = 1
        try:
            driver.switch_to.frame("mainIframe")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#shopGoodsList_isvGoodsNo")))
            time.sleep(3)
        except:
            print("商品店铺商品管理页面加载失败！！！")
        else:
            sl = ",".join(sku_list)
            driver.find_element_by_css_selector("#shopGoodsList_isvGoodsNo").clear()
            driver.find_element_by_css_selector("#shopGoodsList_isvGoodsNo").send_keys(sl)
            Select(driver.find_element_by_css_selector("#shopGoodsList_shopGoods-table_length > label > select")).select_by_index(3)
            driver.find_element_by_css_selector("#shopGoodsList_queryShopGoodsForm").click()
            time.sleep(30)
            while True:
                try:
                    tr_list = driver.find_elements_by_css_selector("#shopGoodsList_shopGoods-table > tbody > tr")
                except:
                    print(str(sl) + "未查询到任何信息！！！")
                else:
                    for tr in tr_list:
                        sl_list = []
                        try:
                            sign = tr.find_element_by_xpath("./td[4]").text
                            sl = tr.find_element_by_xpath("./td[6]").text
                        except:
                            search_sign(driver, sku_list, dc_id)
                        sl_list.append(sign)
                        sl_list.append(dc_id)
                        sl_list.append(str(sl))
                        sl_list.append("100")
                        sl_list.append("100")
                        sl_list.append("100")
                        sl_list.append("")
                        sl_list.append("1")
                        temp_list.append(sl_list)
                        if flag_count % 500 == 0:
                            save_xls(temp_list, flag_xls)
                            flag_xls += 1
                            temp_list = []
                        flag_count += 1
                    try:
                        driver.find_element_by_xpath("//*[@id=\"shopGoodsList_shopGoods-table_paginate\"]/ul/li[@class='next disabled']")
                    except:
                        driver.find_element_by_xpath("//*[@id=\"shopGoodsList_shopGoods-table_paginate\"]/ul/li[5]/a").click()
                        time.sleep(1)
                    else:
                        break
            save_xls(temp_list, flag_xls)


def submit_xls(driver, path):
    driver.switch_to.default_content()
    driver.find_element_by_xpath("//*[@id='920']").click()
    driver.switch_to.frame("mainIframe")
    time.sleep(2)
    driver.find_element_by_css_selector("#goodsList_importGoodsAttributeForm").click()
    time.sleep(1)
    driver.find_element_by_css_selector("#importAttributeFile").send_keys(path)
    try:
        driver.find_element_by_css_selector("#goodsAttributeList_importBtn").click()
    except:
        driver.refresh()
        get_search_page(driver)
        submit_xls(driver, path)
    time.sleep(1)
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#importGoodsNews")))
    except:
        print("物流属性导入超时！！！")
    else:
        time.sleep(30)
        result = driver.find_element_by_css_selector("#importGoodsNews").text
        print("物流属性导入结果：" + result)
        time.sleep(1)
    driver.refresh()
    get_search_page(driver)


def run2(driver, sku_list):
    dc_id = get_department_code(driver)
    get_search_page(driver)
    search_sign(driver, sku_list, dc_id)
    for path in path_list:
        submit_xls(driver, path)
        if len(path_list) > 1:
            time.sleep(305)
    return dc_id