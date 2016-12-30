# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import chardet
class Test(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(300)
        self.base_url = "https://itunesconnect.apple.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.switch_to.frame("aid-auth-widget-iFrame");
        driver.find_element_by_id("appleId").clear()
        driver.find_element_by_id("appleId").send_keys("beebees@qq.com")
        driver.find_element_by_id("pwd").clear()
        driver.find_element_by_id("pwd").send_keys("Beemans912")
        driver.find_element_by_id("sign-in").click()        
        driver.switch_to.default_content()
        driver.find_element_by_css_selector("#main-nav > li.ng-scope > a > img").click()
        time.sleep(5.0)
        self.check_display_click(driver.find_element_by_css_selector("a.new-button.ng-isolate-scope"))
        self.check_display_click(driver.find_element_by_link_text(u"新建 App"))
        time.sleep(5.0)
        driver.find_element_by_xpath("(//input[@type='text'])[4]").send_keys("TESTss")
        Select(driver.find_element_by_xpath("//div[@id='main-ui-view']/div[3]/div/div/div/div/div/div[2]/form/div/div[5]/span/select")).select_by_visible_text(u"简体中文")
        Select(driver.find_element_by_xpath("//div[@id='main-ui-view']/div[3]/div/div/div/div/div/div[2]/form/div/div[6]/span/select")).select_by_visible_text("beebeeZhuTi - com.ZhuTi.5hito")
        driver.find_element_by_xpath("//div[@id='main-ui-view']/div[3]/div/div/div/div/div/div[2]/form/div/div[6]/label/span/a").click()        
        driver.find_element_by_xpath("(//input[@type='text'])[7]").send_keys("dddddddd")
        driver.find_element_by_css_selector("a.checkboxstyle").click()
        driver.find_element_by_css_selector("button.primary.ng-binding").click()
        driver.find_element_by_css_selector("button.ng-binding").click()   
        time.sleep(10.0)
        print driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[3]/div[1]/div/div/div/div/div[2]/div/p").text
        time.sleep(20.0)
        print driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[5]/div/div[3]/div/div[3]/div[1]/form/div[6]/div[2]/div/div[1]/div[4]/div").text
        
    def check_display_click(self, webelement):
        while(not webelement.is_displayed()):
            time.sleep(1.0)
        webelement.click()    
    
    def tearDown(self):
        self.driver.close()
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
