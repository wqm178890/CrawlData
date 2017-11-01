# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import sys, getopt
opts, args = getopt.getopt(sys.argv[1:], "h", ["ai=", "ap=", "bi=", "ver=", "o="])

def get_md5(str):
    m = hashlib.md5()
    m.update(str)
    md5 = m.hexdigest()
    return md5

account_id = "beebees@qq.com"
account_pwd = "Beemans912"
version = "2.1"
bundle_id = "1194650584"
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
    elif op == "--ver":
        print value
        version = value
    elif op == "--o":
        print value
        cert_save_path = value

class Createversion(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.wait = 30
        self.driver.implicitly_wait(self.wait)
        self.url = "https://itunesconnect.apple.com/WebObjects/iTunesConnect.woa/ra/ng/app/%s" % (bundle_id)
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_createversion(self):
        driver = self.driver
        driver.get(self.url)

        sleeptimes = 0
        #帐号登录
        while True:
            try:
                driver.switch_to.frame("aid-auth-widget-iFrame")
                break
            except:
                sleeptimes += 1
                if sleeptimes > 60:
                    print "pageLoad Timeout"
                    return
                time.sleep(1.0)

        driver.find_element_by_xpath("//*[@id='appleId']").clear()
        driver.find_element_by_xpath("//*[@id='appleId']").send_keys(account_id)
        driver.find_element_by_id("pwd").clear()
        driver.find_element_by_id("pwd").send_keys(account_pwd)
        time.sleep(1.0)
        driver.find_element_by_id("sign-in").click()
        driver.switch_to.default_content()
        #
        sleeptimes = 0
        while self.is_element_present(By.XPATH, "(//input[@type='text'])[2]") == False:
            sleeptimes += 1
            if sleeptimes > 60:
                print "pageLoad Timeout"
                return
            time.sleep(1.0)
        time.sleep(10.0)
        driver.find_element_by_link_text(u"版本或平台").click()
        time.sleep(2.0)
        driver.find_element_by_link_text("iOS").click()
        time.sleep(5.0)
        driver.find_element_by_xpath("(//input[@type='text'])[5]").send_keys(version)
        time.sleep(10.0)
        driver.find_element_by_xpath("id('main-ui-view')/div[5]/div/div[4]/div/div/div/div[3]/div/button[2]").click()
    
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
        self.driver.close()
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
#    unittest.main()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(unittest.makeSuite(Createversion))
