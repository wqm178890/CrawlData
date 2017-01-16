# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


import sys, getopt
reload(sys)
sys.setdefaultencoding("utf8")

opts, args = getopt.getopt(sys.argv[1:], "h", ["ai=", "ap=", "bn=", "bi=", "o="])

account_id = "2772636960@qq.com"
account_pwd = "Beemans91"
bundle_name = u"流程测试媒体3"
bundle_id = "com.beemans.tests1.com"
xml_path = "E:/"

for op, value in opts:
    print op
    if op == "--ai":
        print value
        account_id = value
    elif op == "--ap":
        print value
        account_pwd = value
    elif op == "--bn":
        print value
        bundle_name = u'%s' % value
    elif op == "--bi":
        print value
        bundle_id = value
    elif op == "--o":
        print value
        xml_path = value

class SeleniumUmengAppkey(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://mobile.umeng.com/apps"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_selenium_umeng_appkey(self):
        driver = self.driver
        driver.get("http://mobile.umeng.com/apps")

        driver.find_element_by_id("umengLoginBtn").click()
        while self.is_element_present(By.CSS_SELECTOR, "input[type=\"text\"]") == False:
            time.sleep(1.0)
        time.sleep(1.0)
        driver.find_element_by_css_selector("input[type=\"text\"]").clear()
        driver.find_element_by_css_selector("input[type=\"text\"]").send_keys("fdzclsc@163.com")
        driver.find_element_by_css_selector("input[type=\"password\"]").clear()
        driver.find_element_by_css_selector("input[type=\"password\"]").send_keys("linshucan090608")
        driver.find_element_by_id("submitForm").click()
        time.sleep(5.0)
        driver.find_element_by_xpath("id('doc')/div[1]/div/div/div[2]/div[2]/div[3]/a/span[2]").click()
        time.sleep(5.0)
        driver.find_element_by_xpath("id('mainContainer')/div/div[1]/div/div[2]/div/a/b").click()
        time.sleep(5.0)
        driver.find_element_by_id("app_name").clear()
        driver.find_element_by_id("app_name").send_keys(bundle_name)
        time.sleep(2.0)
        driver.find_element_by_id("app_platform_iphone").click()
        time.sleep(2.0)
        driver.find_element_by_id("app_platform_android").click()
        time.sleep(1.0)
        driver.find_element_by_id("app_platform_iphone").click()
        time.sleep(1.0)
        driver.find_element_by_xpath("id('category_selection_list')/div/select").click()
        time.sleep(1.0)
        Select(driver.find_element_by_xpath("id('category_selection_list')/div/select")).select_by_visible_text(u"工具")
        driver.find_element_by_id("app_description").clear()
        driver.find_element_by_id("app_description").send_keys(u"这是一个描述")
        driver.find_element_by_xpath(u"//input[@value='提交并获取AppKey']").click()
        time.sleep(4.0)
        uemng_key = driver.find_element_by_xpath("id('mainContainer')/div/div/div[2]/div[1]/div[1]/div[1]/span").text
        file_object = open('%sUmengAppKey.txt' % xml_path, 'w')
        file_object.write(uemng_key)
        file_object.close()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        #self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
