from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import re
import time
from utils import excel


gsku_list = []
path_list = []


def login(driver):
    driver.get("https://passport.shop.jd.com/login/index.action")
    driver.maximize_window()
    while True:
        time.sleep(0.5)
        if len(driver.get_cookies()) >= 20:
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#chosen-item1302")))
            except:
                print("获取京麦首页失败,检查是否验证码没输入！！！")
            else:
                print("登录成功！！！")
                break


def get_store_id(driver):
    time.sleep(1)
    driver.find_element_by_css_selector("#chosen-item1302").click()
    driver.find_element_by_css_selector("#chosen-item1201").click()
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"pop-tabs\"]/div/div/div[1]/div[2]/div/table/tbody/tr[2]/td")))
        store_id = driver.find_element_by_xpath("//*[@id=\"pop-tabs\"]/div/div/div[1]/div[2]/div/table/tbody/tr[2]/td").text.strip()
    except:
        print("获取商家ID失败")
        return
    driver.find_element_by_css_selector("#chosen-item1302").click()
    return store_id


def get_tr(driver, num=1):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tbl_type2 > tbody > tr:nth-child(1)")))
    except:
        print("获取在售商品管理页第%s页失败！！！" % str(num))
        return
    time.sleep(1)
    tr_list = driver.find_elements_by_xpath("//*[@id='tbl_type2']/tbody/tr")
    for tr in tr_list:
        try:
            tr.find_element_by_xpath("./td[3]/a")
        except:
            try:
                tr.find_element_by_xpath("./td[6]/div/p").text.strip()
            except:
                if tr.find_element_by_xpath("./td[6]/div/div").text.strip() != "上架待审核":
                    url = tr.find_element_by_xpath("./td[2]/div[2]/div[2]/div/p/a").get_attribute("href")
                    get_sku(driver, url)
            else:
                if tr.find_element_by_xpath("./td[6]/div/p").text.strip() != "上架待审核":
                    url = tr.find_element_by_xpath("./td[2]/div[2]/div[2]/div/p/a").get_attribute("href")
                    get_sku(driver, url)
    if driver.find_element_by_xpath("//*[@id=\"pane-onSale\"]/div/div[3]/button[2]").get_attribute("disabled"):
        return
    else:
        driver.find_element_by_xpath("//*[@id=\"pane-onSale\"]/div/div[3]/button[2]").click()
        num += 1
        get_tr(driver, num)


def get_sku(driver, url):
    js = "window.open('%s')" % url
    driver.execute_script(js)
    driver.switch_to.window(driver.window_handles[1])
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#choose-attr-1")))
    except:
        time.sleep(2)
        curl = driver.current_url
        sku = re.findall("\d{14}", curl)
        if len(sku) > 0:
            gsku_list.append(str(sku[0]))
        else:
            print("当前商品详情页异常，没有找到sku！！！" + url)
    if len(driver.find_elements_by_xpath("//*[@id=\"choose-attrs\"]/div")) <= 1:
        pass
    else:
        div_list = driver.find_elements_by_xpath("//*[@id=\"choose-attrs\"]/div")[1:-1]
        count = None
        for div in div_list:
            div.find_element_by_xpath("./div[@class='dd']/div[1]").click()
            count = len(div.find_elements_by_xpath("./div[@class='dd']/div"))
        sku_first = driver.find_elements_by_xpath("//*[@id=\"choose-attr-1\"]/div[@class='dd']/div")
        for sf in sku_first:
            sku = int(sf.get_attribute("data-sku"))
            if count is not None:
                for i in range(count):
                    gsku_list.append(str(sku))
                    sku += 1
            else:
                gsku_list.append(str(sku))
    driver.close()
    driver.switch_to_window(driver.window_handles[0])


def save_xls(temp_list, flag_xls):
    eme = excel.MakeExcel("POP商品导入", "PopGoodsImportTemplate(1)({})".format(str(flag_xls)))
    xls_path = eme.make_base_excel([["POP店铺商品编号（SKU编码）", "商家商品标识", "商品条码"]])
    path_list.append(os.path.abspath('.').replace("\\", "/") + "/" + xls_path)
    eme.white_excel_content(temp_list)


def handle_sku():
    sku_list = list(set(gsku_list))
    if len(sku_list) <= 500:
        temp_list = []
        for sl in sku_list:
            sl_list = []
            sl_list.append(str(sl))
            sl_list.append(str(sl))
            sl_list.append(str(sl))
            temp_list.append(sl_list)
        save_xls(temp_list, 1)
    else:
        temp_list = []
        flag_count = 1
        flag_xls = 1
        for sl in sku_list:
            sl_list = []
            sl_list.append(str(sl))
            sl_list.append(str(sl))
            sl_list.append(str(sl))
            temp_list.append(sl_list)
            if flag_count % 500 == 0:
                save_xls(temp_list, flag_xls)
                flag_xls += 1
                temp_list = []
            flag_count += 1
        save_xls(temp_list, flag_xls)


def login_bucket(driver):
    driver.get("https://ups.jclps.com/login?ReturnUrl=http%3A%2F%2Fb.jclps.com%2F")
    driver.maximize_window()
    while True:
        time.sleep(0.5)
        if len(driver.get_cookies()) >= 5:
            print("云仓登录成功")
            break


def submit_xls(driver, store_id, path):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#top_104202")))
        time.sleep(5)
    except:
        print("未找到基础资料！！！")
        driver.refresh()
        time.sleep(2)
        submit_xls(driver, store_id, path)
    else:
        driver.find_element_by_css_selector("#top_104202").click()
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"9250\"]")))
        time.sleep(1)
    except:
        print("未找到店铺商品管理！！！")
        driver.refresh()
        time.sleep(2)
        submit_xls(driver, store_id, path)
    else:
        driver.find_element_by_xpath("//*[@id=\"9250\"]").click()
    try:
        driver.switch_to.frame("mainIframe")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#buttonset")))
        time.sleep(1)
    except:
        print("未找到新增店铺商品！！！")
        driver.refresh()
        time.sleep(2)
        submit_xls(driver, store_id, path)
    else:
        driver.find_element_by_css_selector("#buttonset").click()
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#shopGoodsList_batchMaintainShopGoods")))
        time.sleep(1)
    except:
        print("未找到批量维护POP店铺商品！！！")
        driver.refresh()
        time.sleep(2)
        submit_xls(driver, store_id, path)
    else:
        try:
            time.sleep(1)
            driver.find_element_by_css_selector("#shopGoodsList_batchMaintainShopGoods").click()
        except:
            print("批量维护POP店铺商品点击失败！！！")
            driver.refresh()
            time.sleep(2)
            submit_xls(driver, store_id, path)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#shopGoodsList_popGoodsImport_popVendorId")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#shopGoodsList_popGoodsListFile")))
        time.sleep(1)
    except:
        print("导入POP店铺商品窗口打开失败！！！")
        driver.refresh()
        time.sleep(2)
        submit_xls(driver, store_id, path)
    else:
        driver.find_element_by_css_selector("#shopGoodsList_popGoodsImport_popVendorId").send_keys(store_id)
        time.sleep(1)
        driver.find_element_by_css_selector("#shopGoodsList_popGoodsListFile").send_keys(path)
        driver.find_element_by_css_selector("#shopGoodsList_popGoodsImportBtn").click()
        time.sleep(1)
        try:
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#lblSysInfo")))
        except:
            print("POP导入超时！！！")
        else:
            time.sleep(40)
            result = driver.find_element_by_css_selector("#lblSysInfo").text
            print("POP导入结果：" + result)
            time.sleep(3)
        driver.refresh()


def run1(driver):
    login(driver)
    store_id = get_store_id(driver)
    get_tr(driver)
    handle_sku()
    login_bucket(driver)
    for path in path_list:
        submit_xls(driver, store_id, path)
    return gsku_list
