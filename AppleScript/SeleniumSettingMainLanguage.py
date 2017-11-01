# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, sys, os,getopt
from xml.etree import ElementTree

import chardet
reload(sys)
sys.setdefaultencoding("utf8")

opts, args = getopt.getopt(sys.argv[1:], "h", ["path=", "o="])

#xml_path = u"/Users/nd/Documents/test.xml"
xml_path = u"C:\\Users\\wqm\\Desktop\\audit.xml"
cert_save_path = u"/Users"

for op, value in opts:
    print op
    if op == "--path":
        print value
        xml_path = value
    elif op == "--o":
        print value
        cert_save_path = value

class ParserXml():
    def __init__(self, xml_path):
        self.appid = ""
        self.account = ""
        self.password = ""
        self.app_names = []
        self.xml_path = xml_path
        self.main_lang = ""
        self.main_category = ""
        self.minor_category = ""
        self.describe = ""
        self.technical_support = "http://wallbase.fr/"
        self.audit_information = {}
        self.note = ""
        self.icon_address = ""
        self.screenshot_address = ""

    def read_xml(self):
        root = ElementTree.parse(self.xml_path)

        self.appid = root.find('appId').text
        self.account = root.find('account').text
        self.password = root.find('password').text

        self.main_category = root.find('mainCategory').text
        self.minor_category = root.find('minorCategory').text

        self.describe = root.find("describe").text
        self.technical_support = root.find('technicalSupport').text

        self.main_lang = root.find("mainLang").text

        auditInformation = root.find('auditInformation')
        self.audit_information['copyright'] = auditInformation.find('copyright').text
        self.audit_information['firstName'] = auditInformation.find('firstName').text
        self.audit_information['secondName'] = auditInformation.find('secondName').text
        self.audit_information['telPhone'] = auditInformation.find('telPhone').text
        self.audit_information['email'] = auditInformation.find('email').text

        self.note = root.find("note").text
        self.icon_address = root.find("iconAddress").text
        self.screenshot_address = root.find('screenShotAddress').text

        nodes = root.find('appNames')
        nodes = nodes.findall('appName')
        app_name = []
        for node in nodes:
            app_name = {}
            app_name['type'] = node.attrib['type']
            app_name['name'] = node.find('name').text
            app_name['keyword'] = node.find('keyword').text
            self.app_names.append(app_name)

    def __str__(self):
        return u'%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s' %\
               (self.appid, self.account, self.password, self.app_names, self.main_category, self.minor_category, self.technical_support, self.audit_information, self.note, self.icon_address, self.screenshot_address)


# account_id = "beebees@qq.com"
# account_pwd = "Beemans912"
# appid = "1190040404"
# phone_number = "+86 18950222580"
# email_address = "bee5hito@qq.com"
# family_name = "lv"
# name = "liang"



parser_xml = ParserXml(xml_path)
parser_xml.read_xml()

class Test(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.wait = 300
        self.driver.implicitly_wait(self.wait)
        self.url = "https://itunesconnect.apple.com/WebObjects/iTunesConnect.woa/ra/ng/app/%s"%(parser_xml.appid)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_b_SelectMainLanguage(self):
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
        driver.find_element_by_xpath("//*[@id='appleId']").send_keys(parser_xml.account)
        driver.find_element_by_id("pwd").clear()
        driver.find_element_by_id("pwd").send_keys(parser_xml.password)
        time.sleep(1.0)
        driver.find_element_by_id("sign-in").click()
        driver.switch_to.default_content()
        #
        time.sleep(5.0)
        while self.is_element_present(By.XPATH, "(//input[@type='text'])[2]") == False:
            time.sleep(1.0)

        driver.find_element_by_xpath("//div[@id='main-ui-view']/div[5]/div/div[2]/div[1]/ul/li[1]/a[1]").click()
        sleeptimes = 0

        while self.is_element_present(By.ID, "mainDropTrayFileSelect") == False:
            print "wait page loaded"
            time.sleep(1.0)
            sleeptimes += 1
            if sleeptimes > 60:
                print "page loaded timeout"
                return
        time.sleep(2.0)

        sleeptimes = 0
        driver.find_element_by_xpath("//*[@id='verlocHeader']/div/a").click()
        while self.is_element_present(By.XPATH, "//*[@id='applocalizations']/div/table/tbody") == False:
            print "add country"
            driver.find_element_by_xpath("//*[@id='verlocHeader']/div/a").click()
            time.sleep(1.0)
            sleeptimes += 1
            if sleeptimes > 60:
                print "add country time out"
                return

        table = driver.find_element_by_xpath("//*[@id='applocalizations']/div/table/tbody")
        trList = table.find_elements_by_xpath(".//tr")
        index = 0
        for element in trList:
            print element.text, parser_xml.main_lang
            if element.text.find(parser_xml.main_lang) > -1:
                print "find"
                print index
                driver.execute_script("$('#verlocHeader table tbody tr:gt(0):eq(%s) td').click();"%(index-1))
                break
            index += 1
        time.sleep(1.0)
        #存储
        driver.find_element_by_xpath("//div[@id='appVerionInfoHeaderId']/div[2]/button[1]").click()
        time.sleep(5.0)

        sleeptimes = 0
        while driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[5]/div/div[3]/div[1]/div[2]/div[2]/button[1]/span[1]").is_displayed():
            time.sleep(1.0)
            sleeptimes += 1
            if sleeptimes > 60:
                print 'save time out'
                return
        #跳转到App信息
        driver.find_element_by_xpath("id('main-ui-view')/div[5]/div/div[2]/ul/li[1]/a").click()
        time.sleep(5.0)

        sleeptimes = 0
        while self.is_element_present(By.XPATH, "(//input[@type='text'])[2]") == False:
            sleeptimes += 1
            if sleeptimes > 60:
                print "pageLoad Timeout"
                return
            time.sleep(1.0)

        #选择主语言
        option_element = driver.find_element_by_xpath("id('appStorePageContent')/div[3]/div[1]/form/div[6]/div[2]/div/div[2]/div[1]/span/select")
        options = Select(driver.find_element_by_xpath("id('appStorePageContent')/div[3]/div[1]/form/div[6]/div[2]/div/div[2]/div[1]/span/select")).options
        select_text = ""
        for option in options:
            if option.text.find(parser_xml.main_lang) > -1:
                select_text = option.text
                break
            print option.text
        Select(driver.find_element_by_xpath("id('appStorePageContent')/div[3]/div[1]/form/div[6]/div[2]/div/div[2]/div[1]/span/select")).select_by_visible_text(select_text)
        sleeptimes = 0
        while self.is_element_present(By.XPATH, "(//input[@type='text'])[2]") == False:
            sleeptimes += 1
            if sleeptimes > 60:
                print "pageLoad Timeout"
                return
            time.sleep(1.0)
        #保存
        if driver.find_element_by_css_selector("button").is_enabled():
            driver.find_element_by_css_selector("button").click()

        sleeptimes = 0
        while driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[5]/div/div[3]/div[1]/div[2]/div[2]/button[1]/span[1]").is_displayed():
            time.sleep(1.0)
            sleeptimes += 1
            if sleeptimes > 60:
                print 'save time out'
                return

        #跳转到准备提交
        driver.find_element_by_xpath("//div[@id='main-ui-view']/div[5]/div/div[2]/div[1]/ul/li[1]/a[1]").click()
        sleeptimes = 0
        while self.is_element_present(By.ID, "mainDropTrayFileSelect") == False:
            print "wait page loaded"
            time.sleep(1.0)
            sleeptimes += 1
            if sleeptimes > 60:
                print "page loaded timeout"
                return
        time.sleep(2.0)

        sleeptimes = 0
        driver.find_element_by_xpath("//*[@id='verlocHeader']/div/a").click()
        while self.is_element_present(By.XPATH, "//*[@id='applocalizations']/div/table/tbody") == False:
            print "add country"
            driver.find_element_by_xpath("//*[@id='verlocHeader']/div/a").click()
            time.sleep(1.0)
            sleeptimes += 1
            if sleeptimes > 60:
                print "add country time out"
                return

        table = driver.find_element_by_xpath("//*[@id='applocalizations']/div/table/tbody")
        trList = table.find_elements_by_xpath(".//tr")
        index = 0
        for element in trList:
            driver.execute_script("$('#verlocHeader table tbody tr:gt(0):eq(1) td span').click();")
            index += 1
        time.sleep(1.0)

        time.sleep(2.0)
        driver.find_element_by_xpath("id('appStorePageContent')/div[3]/div[1]/div[4]/div/div/div/div[2]/div/button[2]").click()

        time.sleep(2.0)
        #保存
        if driver.find_element_by_css_selector("button").is_enabled():
            driver.find_element_by_css_selector("button").click()

        sleeptimes = 0
        while driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[5]/div/div[3]/div[1]/div[2]/div[2]/button[1]/span[1]").is_displayed():
            time.sleep(1.0)
            sleeptimes += 1
            if sleeptimes > 60:
                print 'save time out'
                return

        fo = open("%s/SettingLanguage.txt" % cert_save_path, "w")
        fo.write("Success")
    
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
#         self.driver.close()
#         self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
#unittest.main()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(unittest.makeSuite(Test))
