# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from selenium.webdriver.common.action_chains import ActionChains

import sys, getopt
reload(sys)
sys.setdefaultencoding("utf8")

opts, args = getopt.getopt(sys.argv[1:], "h", ["ai=", "ap=", "bn=", "bi=", "o="])

account_id = "2772636960@qq.com"
account_pwd = "Beemans91"
bundle_name = u"流程测试媒体4"
bundle_id = "com.beemans.tests1.com"
xml_path = "/Users/haizon/Desktop/BeemansSVN/PT/PTAppKit/AutoBuildIpa/PY/"

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
        self.wait = 30
        self.accept_next_alert = True
    
    def test_selenium_umeng_appkey(self):
        driver = self.driver
        driver.get("http://mobile.umeng.com/apps")

        driver.find_element_by_id("umengLoginBtn").click()
        driver.switch_to.frame("alibaba-login-box");
        while self.is_element_present(By.XPATH, '//*[@id="fm-login-id"]') == False:
            print "check"
            time.sleep(1.0)
        time.sleep(1.0)
        driver.find_element_by_xpath("//*[@id='fm-login-id']").clear()
        driver.find_element_by_xpath("//*[@id='fm-login-id']").send_keys("funkingwo2513@qq.com")
        driver.find_element_by_xpath("//*[@id='fm-login-password']").clear()
        driver.find_element_by_xpath("//*[@id='fm-login-password']").send_keys("hk_112358")

        driver.find_element_by_id("fm-login-submit").click()
        time.sleep(2.0)
        # driver.switch_to.default_content()
        # time.sleep(5.0)

       # self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        if self.is_element_present(By.XPATH, "/html/body/div[6]/div[3]/div/button[2]") == False:
            dragger = self.driver.find_element_by_id("nc_1_n1z")
            action = ActionChains(self.driver)
            action.click_and_hold(dragger).move_to_element(dragger).perform(); #鼠标左键按下不放
            action.reset_actions()
            action.move_by_offset(268, 0).perform(); #移动一个位移

            # action.reset_actions()
            #
            # time.sleep(d[index]); #等待停顿时间

            #action.release().perform(); #鼠标左键松开
            action.reset_actions()
            time.sleep(5.0)
            driver.find_element_by_id("fm-login-submit").click()
            if self.is_element_present(By.LINK_TEXT, "刷新") == True:
                driver.find_element_by_link_text("刷新").click()
                time.sleep(2.0)
                dragger = self.driver.find_element_by_id("nc_1_n1z")
                action = ActionChains(self.driver)
                action.click_and_hold(dragger).move_to_element(dragger).perform(); #鼠标左键按下不放
                action.reset_actions()
                action.move_by_offset(268, 0).perform(); #移动一个位移

                # action.reset_actions()
                #
                # time.sleep(d[index]); #等待停顿时间

                #action.release().perform(); #鼠标左键松开
                action.reset_actions()
                time.sleep(5.0)
                driver.find_element_by_id("fm-login-submit").click()
        self.driver.switch_to.default_content()

        if self.is_element_present(By.XPATH, "/html/body/div[6]/div[3]/div/button[2]") == True:
            print "check"
            driver.find_element_by_xpath("/html/body/div[6]/div[3]/div/button[2]").click()
        
        driver.find_element_by_xpath("id('doc')/div[1]/div/div/div[2]/div[2]/div[3]/a/span[2]").click()
        time.sleep(5.0)
        driver.find_element_by_xpath("id('mainContainer')/div/div[1]/div/div[2]/div/a/b").click()
        time.sleep(5.0)
        driver.find_element_by_id("app_name").clear()
        driver.find_element_by_id("app_name").send_keys(bundle_name)
        time.sleep(2.0)
        driver.find_element_by_id("app_platform_iphone").click()
        time.sleep(2.0)
  
        driver.find_element_by_xpath("id('category_selection_list')/div/select").click()
        time.sleep(5.0)
        Select(driver.find_element_by_xpath("id('category_selection_list')/div/select")).select_by_visible_text(u"工具")
        time.sleep(1.0)
        driver.find_element_by_id("app_platform_android").click()
        time.sleep(1.0)
        driver.find_element_by_id("app_platform_iphone").click()
        time.sleep(1.0)
        driver.find_element_by_xpath("id('category_selection_list')/div/select").click()
        time.sleep(5.0)
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
        try:
            self.driver.implicitly_wait(1)
            element = self.driver.find_element(by=how, value=what)
            return element.is_displayed()
        except WebDriverException as e:
            self.driver.implicitly_wait(self.wait)
            return False
        self.driver.implicitly_wait(self.wait)
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
        print ""
        #self.driver.close()
        #self.driver.quit()
#self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
#    unittest.main()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(unittest.makeSuite(SeleniumUmengAppkey))
