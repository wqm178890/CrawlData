# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import hashlib
import sys, getopt
reload(sys)
sys.setdefaultencoding('utf8')

opts, args = getopt.getopt(sys.argv[1:], "h", ["ai=", "ap=", "bi=", "csr=", "o=", "n="])

def get_md5(str):
    m = hashlib.md5()
    m.update(str)
    md5 = m.hexdigest()
    return md5

account_id = "beegoleft@qq.com"
account_pwd = "Beemans918"
bundle_name = "BeemansTest"
bundle_id = "beemans.5hito.app-310"
cert_save_path = "/Users/nd/Desktop"
cert_file_path = "C:\\beenice.certSigningRequest"
appname = "TEST"

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
    elif op == "--n":
    	appname = value
    	print appname

class Test(unittest.TestCase):
    def setUp(self):
        self.wait = 60
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(self.wait)
        self.base_url = "https://itunesconnect.apple.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    
    def test_(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.switch_to.frame("aid-auth-widget-iFrame");
        driver.find_element_by_id("appleId").clear()
        driver.find_element_by_id("appleId").send_keys(account_id)
        driver.find_element_by_id("pwd").clear()
        driver.find_element_by_id("pwd").send_keys(account_pwd)
        time.sleep(1.0)
        driver.find_element_by_id("sign-in").click()        
        driver.switch_to.default_content()
        driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/a/div[1]/img").click()
        time.sleep(10.0)
        self.check_display_click(driver.find_element_by_css_selector("a.new-button.ng-isolate-scope"))
        #self.check_display_click(driver.find_element_by_link_text(u"新建 App"))
        times = 1
        while(self.is_element_present(By.LINK_TEXT, u"新建 App") == False):
            time.sleep(1.0)
            print "Test"
            times = times + 1
            if times > 100:
            	raise Exception(u"请求超时")
            self.check_display_click(driver.find_element_by_css_selector("a.new-button.ng-isolate-scope"))

            #self.check_display_click(driver.find_element_by_link_text(u"新建 App"))
        self.check_display_click(driver.find_element_by_link_text(u"新建 App"))

        time.sleep(5.0)
        driver.find_element_by_xpath("(//input[@type='text'])[4]").send_keys(u"%s-%s"%(appname,get_md5(bundle_id)))
        Select(driver.find_element_by_xpath("//div[@id='main-ui-view']/div[3]/div/div/div/div/div/div[2]/form/div/div[5]/span/select")).select_by_visible_text(u"英文（澳大利亚）")

        option_element = driver.find_element_by_xpath("//div[@id='main-ui-view']/div[3]/div/div/div/div/div/div[2]/form/div/div[6]/span/select")
        #driver.find_element_by_xpath("//div[@id='main-ui-view']/div[3]/div/div/div/div/div/div[2]/form/div/div[6]/span/select").click()
        time.sleep(1.0)
        #driver.find_element_by_xpath("//div[@id='main-ui-view']/div[3]/div/div/div/div/div/div[2]/form/div/div[6]/span/select").click()
        options = Select(driver.find_element_by_xpath("//div[@id='main-ui-view']/div[3]/div/div/div/div/div/div[2]/form/div/div[6]/span/select")).options
        select_text = "ERRORSTR"
        print bundle_id
        for option in options:
            if option.text.find(bundle_id) > -1:
                select_text = option.text
                print select_text
                break
            print option.text
        if "ERRORSTR" == select_text:
        	raise Exception("Error: not found bundle id")
        	return
        
        Select(driver.find_element_by_xpath("//div[@id='main-ui-view']/div[3]/div/div/div/div/div/div[2]/form/div/div[6]/span/select")).select_by_visible_text(select_text)
        driver.find_element_by_xpath("//div[@id='main-ui-view']/div[3]/div/div/div/div/div/div[2]/form/div/div[6]/label/span/a").click()        
        driver.find_element_by_xpath("(//input[@type='text'])[7]").send_keys(u"%s"%bundle_name)
        driver.find_element_by_css_selector("a.checkboxstyle").click()
        driver.find_element_by_css_selector("button.primary.ng-binding").click()
        driver.find_element_by_css_selector("button.ng-binding").click()   
        time.sleep(10.0)
        #print driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[3]/div[1]/div/div/div/div/div[2]/div/p").text
        #time.sleep(20.0)
        times = 0
        while(self.is_element_present(By.XPATH, "id('appStorePageContent')/div[3]/div[1]/form/div[6]/div[2]/div/div[1]/div[4]/div") is False):
            if times > 60:
                raise Exception(u"请求超时或者ID/NAME已经被使用过")
            times = times + 1
            time.sleep(1.0)
        str_id = driver.find_element_by_xpath("id('appStorePageContent')/div[3]/div[1]/form/div[6]/div[2]/div/div[1]/div[4]/div").text
        print str_id
        fo = open("%s/AppId.txt" % cert_save_path, "w")
        fo.write(str_id)
        
    def check_display_click(self, webelement):
        while(not webelement.is_displayed()):
            time.sleep(1.0)
        webelement.click()
    
    def tearDown(self):
        self.driver.close()
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    def is_element_present(self, how, what):
        try:
            self.driver.implicitly_wait(1)
            element = self.driver.find_element(by=how, value=what)
            self.driver.implicitly_wait(self.wait)
            return element.is_displayed()
        except NoSuchElementException as e:
            self.driver.implicitly_wait(self.wait)
            return False
        #self.driver.implicitly_wait(self.wait)
        #return True

if __name__ == "__main__":
#    unittest.main()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(unittest.makeSuite(Test))
