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

    def test_a_create_bundleid(self):
        driver = self.driver
        driver.get("https://developer.apple.com/account/ios/identifier/bundle/create")
        driver.find_element_by_id("accountname").send_keys(account_id)
        driver.find_element_by_id("accountpassword").send_keys(account_pwd)
        driver.find_element_by_id("submitButton2").submit()
        driver.find_element_by_name("appIdName").send_keys(bundle_name)
        driver.find_element_by_name("explicitIdentifier").clear()
        driver.find_element_by_name("explicitIdentifier").send_keys(bundle_id)
        time.sleep(1.0)
        driver.find_element_by_xpath("//*[@id='subcontent']/div[2]/div/div[3]/form/div[2]/button").click()
        time.sleep(2.0)
       # print  driver.find_element_by_xpath("//div[@id='subcontent']/div[2]/div/div[3]/form/div[2]/a[2]").is_enabled()
        driver.find_element_by_xpath("//*[@id='subcontent']/div[2]/div/div[3]/form/div[3]/button[2]").click()
        time.sleep(2.0)
        fo = open("%s/BundleId_Success.txt" % cert_save_path, "w")
        time.sleep(2.0)
        fo.write("Success")

    def tearDown(self):
        self.driver.close()
        #self.driver.quit()
        self.assertEqual([], self.verificationErrors)
        
    def check_display_click(self, webelement):
        while(not webelement.is_displayed()):
            time.sleep(1.0)
        webelement.click()
        
   

if __name__ == "__main__":
#unittest.main()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(unittest.makeSuite(FirstStript))
    #suite = unittest.TestLoader.loadTestsFromTestCase(FirstStript)
#unittest.TextTestRunner(verbosity=2).run(suite)
