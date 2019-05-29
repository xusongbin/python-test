
# selenium自动化控制浏览器

# 请下载Firefox控制驱动，https://github.com/mozilla/geckodriver/releases
# 将驱动放在虚拟环境下，...\venv\Scripts\geckodriver.exe
# 将驱动放在运行环境下，...\Python36\geckodriver.exe

import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def test_baidu():
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # driver = webdriver.Chrome('E:\Program Files\Python36\chromedriver.exe', chrome_options=chrome_options)
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument('--headless')
    driver = webdriver.Firefox(executable_path='geckodriver', firefox_options=firefox_options)
    # driver = webdriver.Firefox(executable_path='geckodriver')
    driver.get('https://www.baidu.com/')
    print(driver.title)
    driver.find_element_by_id('kw').send_keys('elenium')
    driver.find_element_by_id('su').click()
    # print(driver.page_source)
    # sleep(3)
    driver.close()


def test_baiduyunpan():
    driver = webdriver.Firefox('geckodriver.exe')
    driver.get('https://pan.baidu.com/')
    sleep(1)
    driver.find_element_by_id('TANGRAM__PSP_4__footerULoginBtn').click()
    sleep(0.5)
    driver.find_element_by_id('TANGRAM__PSP_4__userName').clear()
    driver.find_element_by_id('TANGRAM__PSP_4__userName').send_keys(u'17778166830')
    driver.find_element_by_id('TANGRAM__PSP_4__password').clear()
    driver.find_element_by_id('TANGRAM__PSP_4__password').send_keys(u'123')
    driver.find_element_by_id('TANGRAM__PSP_4__submit').click()
    sleep(10)
    driver.close()


def test_taobao():
    driver = webdriver.Firefox('geckodriver.exe')
    driver.maximize_window()
    driver.get('https://login.taobao.com/')
    locator = (By.ID, 'J_Quick2Static')
    try:
        element = WebDriverWait(driver, 10, 0.1).until(EC.presence_of_element_located((By.ID, "J_Quick2Static")))
        element.click()
        element = WebDriverWait(driver, 10, 0.1).until(EC.presence_of_element_located((By.ID, "TPL_username_1")))
        element.clear()
        element.send_keys(u'17778166830')
        element = WebDriverWait(driver, 10, 0.1).until(EC.presence_of_element_located((By.ID, "TPL_password_1")))
        element.clear()
        element.send_keys(u'xsb13015611926--')
        element = WebDriverWait(driver, 10, 0.1).until(EC.presence_of_element_located((By.ID, "J_SubmitStatic")))
        element.click()
    except:
        pass
    sleep(1000)
    driver.close()


if __name__ == '__main__':
    test_baidu()
