from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
import random
from utils import excel


path_list = []


def save_xls(temp_list, flag_xls):
    eme = excel.MakeExcel("采购单导入模板", "采购单导入模板({})".format(str(flag_xls)))
    xls_path = eme.make_base_excel([["事业部编号", "供应商编号", "入库库房编号", "商家采购单号", "Clps事业部商品编码", "商家商品编码", "商品数量", "商家包装规格编码", "包装单位编码", "是否需要提供装卸业务", "单据类型编号", "是否按板回传"]])
    path_list.append(os.path.abspath('.').replace("\\", "/") + "/" + xls_path)
    eme.white_excel_content(temp_list)


def order_no():
    order_id = ""
    name_str = "abcdefghijklmnopqrstuvwxyz01234546789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in random.sample(name_str, 16):
        order_id += i
    return order_id


def handle_xls(sku_list, dc_id, sc_id, bc_id, flag_xls=1):
    if len(sku_list) <= 500:
        temp_list = []
        order_id = order_no()
        for sl in sku_list:
            sl_list = []
            sl_list.append(dc_id)
            sl_list.append(sc_id)
            sl_list.append(bc_id)
            sl_list.append(order_id)
            sl_list.append("")
            sl_list.append(sl)
            sl_list.append("5")
            sl_list.append("")
            sl_list.append("")
            sl_list.append("")
            sl_list.append("")
            sl_list.append("")
            temp_list.append(sl_list)
        save_xls(temp_list, flag_xls)
    else:
        order_id = order_no()
        temp_list = []
        flag_count = 1
        for sl in sku_list:
            sl_list = []
            sl_list.append(dc_id)
            sl_list.append(sc_id)
            sl_list.append(bc_id)
            sl_list.append(order_id)
            sl_list.append("")
            sl_list.append(sl)
            sl_list.append("5")
            sl_list.append("")
            sl_list.append("")
            sl_list.append("")
            sl_list.append("")
            sl_list.append("")
            temp_list.append(sl_list)
            if flag_count % 500 == 0:
                order_id = order_no()
                save_xls(temp_list, flag_xls)
                flag_xls += 1
                temp_list = []
            flag_count += 1
        save_xls(temp_list, flag_xls)


def get_supplier_code(driver1):
    driver1.refresh()
    try:
        WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#top_104202")))
        time.sleep(1)
    except:
        print("未找到基础资料！！！")
        driver1.refresh()
        get_supplier_code(driver1)
    else:
        driver1.find_element_by_css_selector("#top_104202").click()
    time.sleep(1)
    driver1.find_element_by_css_selector("#li_104197 > div").click()
    time.sleep(0.5)
    driver1.find_element_by_xpath("//*[@id=\"902\"]").click()
    time.sleep(3)
    try:
        driver1.switch_to.frame("mainIframe")
    except:
        driver1.switch_to.default_content()
        driver1.refresh()
        time.sleep(2)
        get_supplier_code(driver1)
    try:
        sc_id = driver1.find_element_by_css_selector("#supplier-table > tbody > tr > td.center.sorting_1").text
    except:
        get_supplier_code(driver1)
    time.sleep(0.5)
    driver1.refresh()
    return sc_id


def login(driver2):
    driver2.get("https://ups.jclps.com/login?ReturnUrl=http%3A%2F%2Fjwms.jclps.com%2F%3FloginType%3Dtenant")
    driver2.maximize_window()
    while True:
        time.sleep(0.5)
        if len(driver2.get_cookies()) >= 7:
            print("商家后台登录成功")
            break
    time.sleep(10)


def get_bucket_code(driver2):
    try:
        WebDriverWait(driver2, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.level-1:nth-child(2) > div:nth-child(1) > span:nth-child(2)")))
        time.sleep(2)
    except:
        print("未找到我的仓库！！！")
        driver2.refresh()
        time.sleep(10)
        get_bucket_code(driver2)
    else:
        driver2.find_element_by_css_selector("li.level-1:nth-child(2) > div:nth-child(1) > span:nth-child(2)").click()
        time.sleep(0.5)
        driver2.find_element_by_css_selector(".is-opened > ul:nth-child(2) > li:nth-child(1) > span:nth-child(2)").click()
        time.sleep(1)
        bc_id = driver2.find_element_by_css_selector(".is-scrolling-none > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > div:nth-child(1)").text
        return bc_id


def submit_xls(driver, path, sku_list, dc_id, sc_id, bc_id):
    time.sleep(5)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#top_8960")))
    except:
        print("未找到业务管理！！！")
    else:
        driver.find_element_by_css_selector("#top_8960").click()
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"9670\"]")))
        time.sleep(1)
    except:
        print("未找到采购入库！！！")
    else:
        driver.find_element_by_xpath("//*[@id=\"9670\"]").click()
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[@id=\"9680\"]").click()
    try:
        driver.switch_to.frame("mainIframe")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#batchImportLink")))
        time.sleep(2)
    except:
        print("未找到入库批量导入按钮！！！")
        driver.refresh()
        time.sleep(3)
        submit_xls(driver, path, sku_list, dc_id, sc_id, bc_id)
    else:
        driver.find_element_by_css_selector("#batchImportLink").click()
        time.sleep(1)
        driver.find_element_by_css_selector("#batchImportPoFiles").send_keys(path)
        try:
            driver.find_element_by_css_selector("#batchImportPoBtn").click()
        except:
            driver.refresh()
            time.sleep(3)
            submit_xls(driver, path, sku_list, dc_id, sc_id, bc_id)
        time.sleep(1)
        try:
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#lblSysInfo")))
        except:
            print("采购单导入超时！！！")
        else:
            time.sleep(60)
            fail_count = int(driver.find_element_by_xpath("//*[@id=\"batchImportModel\"]/div/div/div[2]/div/label/label[3]").text)
            print("采购单导入结果：失败%d" % fail_count)
            if int(fail_count) > 0:
                fail_list = []
                tr_list = driver.find_elements_by_css_selector("#poBatchImport-table > tbody > tr")
                for tr in tr_list:
                    i = tr.find_element_by_xpath("./td[8]").text.strip()
                    fail_list.append(i)
                print(fail_list)
                em = excel.MakeExcel("采购单导入模板", path.split("/")[-1][:-4])
                temp_list = em.read_sheet(fail_list)
                os.remove(path)
                driver.refresh()
                handle_xls(temp_list, dc_id, sc_id, bc_id, flag_xls=int(path.split("/")[-1][:-4][-2]))
        driver.refresh()


def run3(driver1, driver2, sku_list, dc_id):
    sc_id = get_supplier_code(driver1)
    login(driver2)
    bc_id = get_bucket_code(driver2)
    handle_xls(sku_list, dc_id, sc_id, bc_id)
    for path in path_list:
        submit_xls(driver1, path, sku_list, dc_id, sc_id, bc_id)