from selenium import webdriver
import jd_step1
import jd_step2
import jd_step3
import jd_step4
import jd_step5


def run():
    driver1 = webdriver.Chrome(executable_path="chromedriver.exe")
    print("-" * 55)
    print("*" * 20 + "第一步开始！！！" + "*" * 20)
    sku_list = list(set(jd_step1.run1(driver1)))
    print("*" * 20 + "第一步结束！！！" + "*" * 20)
    print("-" * 55)
    print("*" * 20 + "第二步开始！！！" + "*" * 20)
    dc_id = jd_step2.run2(driver1, sku_list)
    print("*" * 20 + "第二步结束！！！" + "*" * 20)
    print("-" * 55)
    print("*" * 20 + "第三步开始！！！" + "*" * 20)
    driver2 = webdriver.Firefox(executable_path="geckodriver.exe")
    jd_step3.run3(driver1, driver2, sku_list, dc_id)
    print("*" * 20 + "第三步结束！！！" + "*" * 20)
    print("-" * 55)
    print("*" * 20 + "第四步开始！！！" + "*" * 20)
    jd_step4.run4(driver2)
    print("*" * 20 + "第四步结束！！！" + "*" * 20)
    print("-" * 55)
    print("*" * 20 + "第五步开始！！！" + "*" * 20)
    jd_step5.run5(driver1)
    print("*" * 30 + "第五步结束！！！" + "*" * 30)
    print("-" * 55)
    driver1.quit()
    input("按回车确认结束！")


if __name__ == '__main__':
    run()