# -*- coding: utf-8 -*-
# pylint: disable=c0103
# pylint: disable=c0111
# pylint: disable=c0301

import unittest
import time
from xml.etree import ElementTree
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

import sys, getopt
reload(sys)
sys.setdefaultencoding("utf8")

opts, args = getopt.getopt(sys.argv[1:], "h", ["ai=", "ap=", "bi=", "xml="])

account_id = "bee@qq.com"
account_pwd = "Beemans"
app_id = "1208915267"
xml_path = u"/Users/xxx/Desktop/appPay.xml"

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
        app_id = value
    elif op == "--xml":
        print value
        xml_path = value

class ParserXml():
    def __init__(self, xml_path):
        self.product = []
        self.appid = app_id
        self.account = account_id
        self.password = account_pwd
        self.xml_path = xml_path

    def read_xml(self):
        root = ElementTree.parse(self.xml_path)

        nodes = root.find('productIDs')
        nodes = nodes.findall('productID')
        for node in nodes:
            app_name = {}
            app_name['name'] = node.find('name').text
            app_name['pID']  = node.find('pID').text
            app_name['describe']  = node.find('describe').text
            app_name['rank']  = node.find('rank').text
            app_name['screenshot'] = node.find('screenshot').text
            self.product.append(app_name)

    def __str__(self):
        sysoStr = ""
        for app_name in self.product:
            sysoStr += "name:" + app_name['name'].encode("utf-8")
            sysoStr += "\t\tpID:" + app_name['pID']
            sysoStr += "\t\tdescribe:" + app_name['describe'].encode("utf-8")
            sysoStr += "\t\trank:" + app_name['rank'].encode("utf-8")
            sysoStr += "\t\tscreenshot:" + app_name['screenshot']
            sysoStr += "\n"
        return sysoStr

parser_xml = ParserXml(xml_path)
parser_xml.read_xml()
print(parser_xml)

class Apppurchase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.wait = 300
        self.driver.implicitly_wait(self.wait)
        self.url = "https://itunesconnect.apple.com/WebObjects/iTunesConnect.woa/ra/ng/app/%s/addons"%(parser_xml.appid)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_a_purchase(self):
        driver = self.driver
        driver.get(self.url)
        sleeptimes = 0
        #帐号登录
        while True:
            try:
                driver.switch_to.frame("aid-auth-widget-iFrame")
                break
            except e:
                sleeptimes += 1
                if sleeptimes > 60:
                    print "pageLoad Timeout"
                    return
                time.sleep(1.0)
  
        driver.find_element_by_xpath("//*[@id='appleId']").clear()
        driver.find_element_by_xpath("//*[@id='appleId']").send_keys(parser_xml.account)
        driver.find_element_by_id("pwd").clear()
        driver.find_element_by_id("pwd").send_keys(parser_xml.password)
        time.sleep(1.0)
        driver.find_element_by_id("sign-in").click()  
        driver.switch_to.default_content()
        #登录结束
        
        for app_name in parser_xml.product:        
            self.check_display_click(driver.find_element_by_xpath("id('iapwrapper')/div[1]/div[3]/div[1]/div[1]/h1/a"))

            sleeptimes = 0
            while self.is_element_present(By.XPATH, "id('iapwrapper')/div[1]/div[7]/div/div/div/div[2]/div[1]/div/div/span/a") is False:
                print "wait page loaded"
                time.sleep(1.0)
                sleeptimes += 1
                driver.find_element_by_xpath("id('iapwrapper')/div[1]/div[3]/div[1]/div[1]/h1/a").click()
                if sleeptimes > 60:
                    print "page loaded timeout"
                    return

            driver.find_element_by_xpath("id('iapwrapper')/div[1]/div[7]/div/div/div/div[2]/div[1]/div/div/span/a").click()
            time.sleep(1.0)
            driver.find_element_by_xpath("//div[@id='iapwrapper']/div/div[7]/div/div/div/div[3]/div[2]/button[2]").click()
            time.sleep(2.0)

            while self.is_element_present(By.XPATH, "(//input[@type='file'])[2]") == False:
                print "wait page loaded"
                time.sleep(1.0)
                sleeptimes += 1
                if sleeptimes > 60:
                    print "page loaded timeout"
                    return

            #参考名称
            driver.find_element_by_xpath("(//input[@type='text'])[2]").clear()
            driver.find_element_by_xpath("(//input[@type='text'])[2]").send_keys(u"%s" % (app_name['name']))

            #产品ID
            driver.find_element_by_xpath("(//input[@type='text'])[3]").clear()
            driver.find_element_by_xpath("(//input[@type='text'])[3]").send_keys(u"%s" % (app_name['pID']))

            time.sleep(3.0)
            #价格设置
            size = driver.execute_script("return $('#tierSelectionID div table tbody tr td').size()")
            for i in range(0, size):
                text = driver.execute_script("return $('#tierSelectionID div table tbody tr:eq(%d) td').text()"%(i))
                if text.find(app_name["rank"]) > -1:
                    driver.execute_script("$('#tierSelectionID div table tbody tr:eq(%d) td').click()" %( i ))
                    break

            #显示名称
            driver.find_element_by_xpath("(//input[@type='text'])[6]").clear()
            driver.find_element_by_xpath("(//input[@type='text'])[6]").send_keys(u"%s" % (app_name['name']))

            #描述
            driver.find_element_by_xpath("//div[@id='iapwrapper']/div/form/div[10]/div[2]/div[2]/div/div[3]/div/span/span/textarea").clear()
            driver.find_element_by_xpath(
                "//div[@id='iapwrapper']/div/form/div[10]/div[2]/div[2]/div/div[3]/div/span/span/textarea"
            ).send_keys(u"%s" % (app_name['describe']))
            
            #屏幕快照
            driver.find_element_by_xpath("(//input[@type='file'])[2]").clear()
            driver.find_element_by_xpath("(//input[@type='file'])[2]").send_keys(app_name['screenshot'])
            
            #审核备注

            #存储
            time.sleep(5.0)
            sleeptimes = 0
            while driver.find_element_by_xpath("id('buttonGroupHeader')/button[1]").is_enabled() is False:
                sleeptimes += 1
                if sleeptimes > 60:
                    return
            driver.find_element_by_xpath("id('buttonGroupHeader')/button[1]").click()
            time.sleep(0.2)
            sleeptimes = 0
            while driver.find_element_by_xpath("id('buttonGroupHeader')/button[1]/span[1]").is_displayed():
                time.sleep(1.0)
                sleeptimes += 1
                if sleeptimes > 60:
                    print 'save time out'
                    return
            time.sleep(5.0)
            driver.find_element_by_link_text("App 内购买项目").click()
            time.sleep(2.0)
            try:
                driver.find_element_by_xpath("id('main-ui-view')/div[4]/div/div[2]/div[4]/div/div/div/div[2]/div[1]/button").click()
            except NoSuchElementException as e:
                pass

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
        self.driver.close()
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
#    unittest.main()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(unittest.makeSuite(Apppurchase))
