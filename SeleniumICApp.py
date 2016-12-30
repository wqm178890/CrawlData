# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import unittest,time, re
import hashlib

import sys, getopt

print "start"
opts, args = getopt.getopt(sys.argv[1:], "h", ["ai=", "ap=", "bi=", "csr=", "o="])

def get_md5(str):
    m = hashlib.md5()
    m.update(str)
    md5 = m.hexdigest()
    return md5 

account_id = "beebees@qq.com"
account_pwd = "Beemans912"
bundle_name = "BeemansTest"
bundle_id = "com.beemans.tests.com"
cert_save_path = "E:\\CERT"
cert_file_path = "C:\\beenice.certSigningRequest"

for op, value in opts:
    print op
    if op == "--ai":
        print value
        account_id = value
    elif op == "--ap":
        print value
        account_pwd = value
    elif op == "--bi":
        print value
        bundle_id = value
        bundle_name = get_md5(bundle_id)
    elif op == "--csr":
        print value
        cert_file_path = value
    elif op == "--o":
        print value
        cert_save_path = value


class FirstStript(unittest.TestCase):
    
    def setUp(self):
        self.fp = webdriver.FirefoxProfile()
        self.fp.set_preference("browser.download.folderList", 2)
        self.fp.set_preference("browser.download.manager.showWhenStarting", False)
        self.fp.set_preference("browser.download.dir", cert_save_path)
        self.fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
        self.verificationErrors = []
        self.driver = webdriver.Firefox(firefox_profile=self.fp)# ("localhost", 4444, "*chrome", "https://developer.apple.com/")
        self.driver.implicitly_wait(220)

    def test_create_app(self):
        driver = self.driver
        driver.get("https://itunesconnect.apple.com/itc/static/login?appIdKey=e0b80c3bf78523bfe80974d320935bfa30add02e1bff88ec2166c6bd5a706c42&view=1&path=%2FWebObjects%2FiTunesConnect.woa%3F")
        driver.find_element_by_xpath("//*[@id='appleId']").clear()
        driver.find_element_by_xpath("//*[@id='appleId']").send_keys(account_id)
        driver.find_element_by_id("pwd").clear()
        driver.find_element_by_id("pwd").send_keys(account_pwd)
        driver.find_element_by_id("sign-in").click()
        driver.find_element_by_css_selector("#main-nav > li.ng-scope > a > img").click()
        driver.find_element_by_css_selector("a.new-button.ng-isolate-scope").click()
        driver.find_element_by_link_text(u"新建 App").click()
        driver.find_element_by_css_selector("a.checkboxstyle").click()
        driver.find_element_by_xpath("(//input[@type='text'])[4]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[4]").send_keys("TESTER")
        Select(driver.find_element_by_xpath("//div[@id='main-ui-view']/div[3]/div/div/div/div/div/div[2]/form/div/div[5]/span/select")).select_by_visible_text(u"简体中文")
        Select(driver.find_element_by_xpath("//div[@id='main-ui-view']/div[3]/div/div/div/div/div/div[2]/form/div/div[6]/span/select")).select_by_visible_text("BeemansTest - com.beemans.tests.com")
        driver.find_element_by_xpath("(//input[@type='text'])[7]").send_keys("COMBEEMANS")
        driver.find_element_by_css_selector("button.primary.ng-binding").click()
        driver.find_element_by_css_selector("button.primary.ng-binding").click()
        time.sleep(10.0)

    def atest_a_create_bundleid(self):
        driver = self.driver
        driver.get("https://developer.apple.com/account/ios/identifier/bundle/create")
        driver.find_element_by_id("accountname").send_keys(account_id)
        driver.find_element_by_id("accountpassword").send_keys(account_pwd)
        driver.find_element_by_id("submitButton2").submit()
        driver.find_element_by_name("appIdName").send_keys(bundle_name)
        driver.find_element_by_name("explicitIdentifier").clear()
        driver.find_element_by_name("explicitIdentifier").send_keys(bundle_id)
        driver.find_element_by_xpath("//div[@id='subcontent']/div[2]/div/div[3]/form/div[2]/a[2]").click()
       # print  driver.find_element_by_xpath("//div[@id='subcontent']/div[2]/div/div[3]/form/div[2]/a[2]").is_enabled()
        driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[2]/div[2]/div/div[3]/form/div[3]/a[3]/span").click()
    
    def atest_b_first_stript(self):
        self.driver.get('https://developer.apple.com/account/ios/certificate/create')
        driver = self.driver
        driver.find_element_by_id("accountname").send_keys(account_id)
        driver.find_element_by_id("accountpassword").send_keys(account_pwd)
        driver.find_element_by_id("submitButton2").submit()
        driver.find_element_by_id("type-production-2").click() 
        driver.find_element_by_xpath("//div[@id='subcontent']/div[2]/div/div[4]/a[3]/span").click()

        option_element = driver.find_element_by_xpath("//select[@id='identifier']/option[2]")
        options = Select(driver.find_element_by_id("identifier")).options
        select_text = ""
        print bundle_id
        for option in options:
            if option.text.find(bundle_id) > -1:
                select_text = option.text
                break
            print option.text        
        #select.select_by_visible_text("4W7UWM98DG.%s"%(bundle_id))
        
        Select(driver.find_element_by_id("identifier")).select_by_visible_text(select_text)
        #Select(driver.find_element_by_id("identifier")).select_by_visible_text("com.NewXYAssistant.app")
       
        driver.find_element_by_xpath("//div[@id='subcontent']/div[2]/div/div[4]/a[3]/span").click()
        time.sleep(2.0)
        driver.find_element_by_xpath("//div[@id='subcontent']/div[2]/div/div[4]/a[3]/span").click()
        driver.find_element_by_name("upload").send_keys(cert_file_path)
        #driver.type("name=upload", u"D:\\桌面\\键盘连点器_201611181452.Q")
        driver.find_element_by_xpath("//div[@id='subcontent']/div[2]/div/div[4]/a[3]/span").click()
        
        time.sleep(10.0)
    
    def atest_c_first_stript(self):
        self.driver.get('https://developer.apple.com/account/ios/profile/production/create')
        driver = self.driver
        driver.find_element_by_id("accountname").send_keys(account_id)
        driver.find_element_by_id("accountpassword").send_keys(account_pwd)
        driver.find_element_by_id("submitButton2").submit()     
        driver.find_element_by_id("type-production").click()
        driver.find_element_by_xpath("//div[@id='subcontent']/div[2]/div/div[3]/div[2]/form/div/div[2]/div/label/h3").click()
        driver.find_element_by_xpath("//div[@id='subcontent']/div[2]/div/div[3]/div[2]/form/div[2]/a[2]/span").click()

        option_element = driver.find_element_by_xpath("//select[@name='appIdId']/option[2]")
        options = Select(driver.find_element_by_name("appIdId")).options
        select_text = ""
        print bundle_id
        for option in options:
            if option.text.find(bundle_id) > -1:
                select_text = option.text
                break
            print option.text        
        
        Select(driver.find_element_by_name("appIdId")).select_by_visible_text(select_text)
        driver.find_element_by_xpath("//div[@id='subcontent']/div[2]/div/div[3]/form/div[2]/a[3]/span").click()
        time.sleep(2.0)
        driver.find_element_by_xpath("//input[@name='certificateIds']").click()
        driver.find_element_by_xpath("//div[@id='subcontent']/div[2]/div/div[3]/form/div[2]/a[3]/span").click()
        time.sleep(2.0)
        driver.find_element_by_name("provisioningProfileName").clear()
        driver.find_element_by_name("provisioningProfileName").send_keys(bundle_name)
        driver.find_element_by_xpath("//div[@id='subcontent']/div[2]/div/div[3]/div[3]/a[3]/span").click()
        time.sleep(2.0)
        driver.find_element_by_xpath("//div[@id='subcontent']/div[2]/div/div[3]/div[2]/div[2]/a/span").click()  
        time.sleep(10.0)
    
    def tearDown(self):
        self.driver.close()
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
        
    def check_display_click(self, webelement):
        while(not webelement.is_displayed()):
            time.sleep(1.0)
        webelement.click()
        
   

if __name__ == "__main__":
    unittest.main()
    #runner = unittest.TextTestRunner(verbosity=2)
    #result = runner.run(unittest.makeSuite(FirstStript))    
    #suite = unittest.TestLoader.loadTestsFromTestCase(FirstStript)
    #unittest.TextTestRunner(verbosity=2).run(suite)
