# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import chardet

account_id = "beebees@qq.com"
account_pwd = "Beemans912"
bundle_name = "BeemansTest"
bundle_id = "com.beemans.tests.com"
cert_save_path = "E:\\CERT"
img_path = "C:\\beenice.certSigningRequest"


class Test(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.wait = 300
        self.driver.implicitly_wait(self.wait)
        self.url = "https://itunesconnect.apple.com/WebObjects/iTunesConnect.woa/ra/ng/app/1190040404"
        self.verificationErrors = []
        self.accept_next_alert = True
        
    def testSettingInfo(self):
        driver = self.driver
        driver.get(self.url + "/ios/versioninfo")
        driver.switch_to.frame("aid-auth-widget-iFrame");
        driver.find_element_by_xpath("//*[@id='appleId']").clear()
        driver.find_element_by_xpath("//*[@id='appleId']").send_keys(account_id)
        driver.find_element_by_id("pwd").clear()
        driver.find_element_by_id("pwd").send_keys(account_pwd)
        time.sleep(1.0)
        driver.find_element_by_id("sign-in").click()  
        driver.switch_to.default_content()
        time.sleep(5.0)
        driver.find_element_by_xpath("//*[@id='verlocHeader']/div/a").click()
        while self.is_element_present(By.XPATH, "//*[@id='applocalizations']/div/table/tbody") == False:
            print "test"
            driver.find_element_by_xpath("//*[@id='verlocHeader']/div/a").click()
            time.sleep(1.0)  
            
        time.sleep(5.0)
        #driver.find_element_by_xpath("//*[@id='verlocHeader']/div/a").click()
        #time.sleep(1.0)
        
        table = driver.find_element_by_xpath("//*[@id='applocalizations']/div/table/tbody")
        trList = table.find_elements_by_xpath(".//tr") 
        index = 0
        xpath_str = ""
        
        for element in trList:
            if element.text.find(u"美国") > -1:
                print "find"
                print index
                driver.execute_script("$('#verlocHeader table tbody tr:gt(0):eq(%s) td').click();"%(index-1))
                #driver.find_element_by_xpath("//div[@id='applocalizations']/div/table/tbody/tr[21]/td").click()
                break
            index += 1
        time.sleep(5.0)
        #driver.find_element_by_xpath("//*[@id='verlocHeader']/div/a").click()
        #print "if out", xpath_str
        #driver.find_element_by_xpath(xpath_str).click()
        #print "if out", xpath_str
        time.sleep(1.0)
        driver.find_element_by_id("mainDropTrayFileSelect").clear()
        driver.find_element_by_id("mainDropTrayFileSelect").send_keys(u"D:\\桌面\\09fa513d269759ee48d2ee55b1fb43166c22dfaa.jpg")        
        driver.find_element_by_id("mainDropTrayFileSelect").clear()
        driver.find_element_by_id("mainDropTrayFileSelect").send_keys(u"D:\\桌面\\09fa513d269759ee48d2ee55b1fb43166c22dfaa.jpg") 
        driver.find_element_by_id("mainDropTrayFileSelect").clear()
        driver.find_element_by_id("mainDropTrayFileSelect").send_keys(u"D:\\桌面\\09fa513d269759ee48d2ee55b1fb43166c22dfaa.jpg") 
        #描述
        descripte = u"这里肯定有10个字符了吧"
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[4]/div/span/span/textarea").clear()
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[4]/div/span/span/textarea").send_keys(descripte)
        #关键词
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[5]/div[1]/span/input").send_keys("Test-Test")
        #ICON
        driver.find_element_by_xpath("(//input[@type='file'])[5]").clear()
        driver.find_element_by_xpath("(//input[@type='file'])[5]").send_keys(u"D:\\桌面\\AppIcon\\@1024.png")   
        
        #手动发布
        driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div[1]/form/div/div[7]/div[2]/div[1]/div/div/span/a").click()
        #存储
        driver.find_element_by_xpath("//div[@id='appVerionInfoHeaderId']/div[2]/button[1]").click()
        time.sleep(5.0)
        
        
    def is_element_present(self, how, what):
        try:
            self.driver.implicitly_wait(1)
            element = self.driver.find_element(by=how, value=what)
            return element.is_displayed()
        except NoSuchElementException as e: 
            self.driver.implicitly_wait(self.wait)
            return False
        self.driver.implicitly_wait(self.wait)
        return True    
        
    def check_display_click(self, webelement):
        while(not webelement.is_displayed()):
            time.sleep(1.0)
        webelement.click()    
    
    def tearDown(self):
        #self.driver.close()
        #self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()    