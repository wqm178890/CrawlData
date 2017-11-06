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
#        self.ipad_screensho_address = ""

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
#        self.ipad_screensho_address = root.find('ipadScreenShotAddress').text
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
        
    def setting_appInfo(self):
        driver = self.driver
        driver.get(self.url)
        #
        # sleeptimes = 0
        # #帐号登录
        # while True:
        #     try:
        #         driver.switch_to.frame("aid-auth-widget-iFrame")
        #         break
        #     except:
        #         sleeptimes += 1
        #         if sleeptimes > 60:
        #             print "pageLoad Timeout"
        #             return
        #         time.sleep(1.0)
        # driver.find_element_by_xpath("//*[@id='appleId']").clear()
        # driver.find_element_by_xpath("//*[@id='appleId']").send_keys(parser_xml.account)
        # driver.find_element_by_id("pwd").clear()
        # driver.find_element_by_id("pwd").send_keys(parser_xml.password)
        # time.sleep(1.0)
        # driver.find_element_by_id("sign-in").click()
        # driver.switch_to.default_content()
        # #
        time.sleep(5.0)
        
        sleeptimes = 0
        while self.is_element_present(By.XPATH, "(//input[@type='text'])[2]") == False:
            sleeptimes += 1
            if sleeptimes > 60:
                print "pageLoad Timeout"
                return
            time.sleep(1.0)
        option_element = driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div[7]/div[2]/div/div[2]/div[2]/span/span/select")
        options = Select(driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div[7]/div[2]/div/div[2]/div[2]/span/span/select")).options
        select_text = ""
        for option in options:
            if option.text.find(parser_xml.main_category) > -1:
                select_text = option.text
                break
            print option.text
        Select(driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div[7]/div[2]/div/div[2]/div[2]/span/span/select")).select_by_visible_text(select_text)
        for appinfo in parser_xml.app_names:
            #添加国家
            sleeptimes = 0
            driver.find_element_by_xpath("id('locHeader')/div/a").click()
            while self.is_element_present(By.XPATH, "//*[@id='applocalizations']/div/table/tbody") == False:
                print "add country"
                driver.find_element_by_xpath("id('locHeader')/div/a").click()
                time.sleep(1.0)
                sleeptimes += 1
                if sleeptimes > 60:
                    print "add country time out"
                    return

            table = driver.find_element_by_xpath("//*[@id='applocalizations']/div/table/tbody")
            trList = table.find_elements_by_xpath(".//tr")

            #澳大利亚
            index = 0
            for element in trList:
                if element.text.find(appinfo['type']) > -1:
                    print "find"
                    print index
                    driver.execute_script("$('#locHeader table tbody tr:gt(0):eq(%s) td').click();"%(index-1))
                    break
                index += 1
            time.sleep(1.0)

            #应用名称
            driver.find_element_by_xpath("//*[@id='localizationSection']/div[2]/div[1]/div/span/input").clear()
            driver.find_element_by_xpath("//*[@id='localizationSection']/div[2]/div[1]/div/span/input").send_keys(appinfo['name'])
            time.sleep(10.0)

        #保存
        btn_element = driver.find_element_by_xpath("//*[@id='appStorePageInfoHeaderId']/div[2]/button")
        if btn_element.is_enabled():
           btn_element.click()

        time.sleep(2.0)
        sleeptimes = 0
        while driver.find_element_by_xpath("id('appStorePageInfoHeaderId')/div[2]/button/span[1]").is_displayed():
            time.sleep(1.0)
            sleeptimes += 1
            if sleeptimes > 60:
                print 'save time out'
                return

        if driver.find_element_by_xpath("id('appStorePageContent')/div[3]/div[1]/form/div[2]/p[1]").text.find('您输入的 App 名称已被使用') > -1:
            print 'name had be named'
        else:
            return

        for appinfo in parser_xml.app_names:
            #添加国家
            sleeptimes = 0
            driver.find_element_by_xpath("id('locHeader')/div/a").click()
            while self.is_element_present(By.XPATH, "//*[@id='applocalizations']/div/table/tbody") == False:
                print "add country"
                driver.find_element_by_xpath("id('locHeader')/div/a").click()
                time.sleep(1.0)
                sleeptimes += 1
                if sleeptimes > 60:
                    print "add country time out"
                    return

            table = driver.find_element_by_xpath("//*[@id='applocalizations']/div/table/tbody")
            trList = table.find_elements_by_xpath(".//tr")

            #澳大利亚
            index = 0
            for element in trList:
                if element.text.find(appinfo['type']) > -1:
                    print "find"
                    print index
                    driver.execute_script("$('#locHeader table tbody tr:gt(0):eq(%s) td').click();"%(index-1))
                    break
                index += 1
            time.sleep(1.0)

            #应用名称
            driver.find_element_by_xpath("//*[@id='localizationSection']/div[2]/div[1]/div/span/input").clear()
            driver.find_element_by_xpath("//*[@id='localizationSection']/div[2]/div[1]/div/span/input").send_keys('%s-%s'%(appinfo['name'], time.time()))
            time.sleep(2.0)

        #保存
        btn_element = driver.find_element_by_xpath("//*[@id='appStorePageInfoHeaderId']/div[2]/button")
        #保存
        if btn_element.is_enabled():
           btn_element.click()
        time.sleep(2.0)
        sleeptimes = 0
        while driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[5]/div/div[3]/div[1]/div[2]/div[2]/button[1]/span[1]").is_displayed():
            time.sleep(1.0)
            sleeptimes += 1
            if sleeptimes > 60:
                print 'save time out'
                return

        option_element = driver.find_element_by_xpath("id('appStorePageContent')/div[3]/div[1]/form/div[6]/div[2]/div/div[2]/div[1]/span/select")
        options = Select(driver.find_element_by_xpath("id('appStorePageContent')/div[3]/div[1]/form/div[6]/div[2]/div/div[2]/div[1]/span/select")).options
        select_text = ""
        for option in options:
            if option.text.find(parser_xml.main_lang) > -1:
                select_text = option.text
                break
            print option.text

        Select(driver.find_element_by_xpath("id('appStorePageContent')/div[3]/div[1]/form/div[6]/div[2]/div/div[2]/div[1]/span/select")).select_by_visible_text(select_text)
        fo = open("%s/SettingAppInfo.txt" % cert_save_path, "w")
        fo.write("Success")

    def setting_prince(self):
        driver = self.driver
        driver.get(self.url + "/pricing")

        #
        # sleeptimes = 0
        # #帐号登录
        # while True:
        #     try:
        #         driver.switch_to.frame("aid-auth-widget-iFrame")
        #         break
        #     except:
        #         sleeptimes += 1
        #         if sleeptimes > 60:
        #             print "pageLoad Timeout"
        #             return
        #         time.sleep(1.0)
        # driver.find_element_by_xpath("//*[@id='appleId']").clear()
        # driver.find_element_by_xpath("//*[@id='appleId']").send_keys(parser_xml.account)
        # driver.find_element_by_id("pwd").clear()
        # driver.find_element_by_id("pwd").send_keys(parser_xml.password)
        # time.sleep(1.0)
        # driver.find_element_by_id("sign-in").click()
        # driver.switch_to.default_content()
        # #
        # time.sleep(5.0)


        sleeptimes = 0
        while self.is_element_present(By.XPATH, "//*[@id='main-ui-view']/div[4]/div/div[3]/div[2]/div[1]/div[4]/div/table/tbody/tr[2]/td[1]/div[1]/div[1]") is False:
            sleeptimes += 1
            if sleeptimes > 60:
                print "pageLoad Timeout"
                return
            time.sleep(1.0)
        driver.execute_script("$(\"div[class='popupmenuinner'] table tbody tr:eq(0) td\").click();")

        time.sleep(2.0)
        #保存
        btn_element = driver.find_element_by_xpath("//*[@id='appVerionInfoHeaderId']/div[2]/button")
        if btn_element.is_enabled():
           btn_element.click()

        time.sleep(2.0)
        sleeptimes = 0
        while driver.find_element_by_xpath("id('appVerionInfoHeaderId')/div[2]/button/span[1]").is_displayed():
            time.sleep(1.0)
            sleeptimes += 1
            if sleeptimes > 60:
                print 'save time out'
                return

    def test_a_SettingInfo(self):
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
        
        #define 获取名字，邮箱
        name_str = driver.find_element_by_xpath("//*[@id='itc-user-profile-controls-js']/div[1]/div[1]/div/h3").text
        family_name = name_str.split(" ")[1]
        name = name_str.split(" ")[0]
        driver.find_element_by_xpath("//*[@id='itc-user-profile-controls-js']/div[1]/div[2]").click()
        time.sleep(2.0)
        email_address = driver.find_element_by_xpath("//*[@id='itc-user-profile-controls-js']/div[2]/header/div/div/p").text
        print 'family_name:', family_name
        print 'name:', name
        print 'email_address:', email_address
        #define APP信息
        
        #应用名称
        # driver.find_element_by_xpath("(//input[@type='text'])[2]").clear()
        # driver.find_element_by_xpath("(//input[@type='text'])[2]").send_keys(parser_xml.app_names[0]['name'])

        #类别
        Select(driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div[7]/div[2]/div/div[2]/div[2]/span/span/select")).select_by_visible_text(parser_xml.main_category)
        #子类别
        #Select(driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div/form/div[6]/div[2]/div/div[2]/div[2]/div[3]/span/span/select")).select_by_visible_text(parser_xml.minor_category)

        time.sleep(2.0)
        btn_element = driver.find_element_by_xpath("//*[@id='appStorePageInfoHeaderId']/div[2]/button")
        #保存
        if btn_element.is_enabled():
           btn_element.click()
        time.sleep(4.0)
        sleeptimes = 0
        while driver.find_element_by_xpath("id('appStorePageInfoHeaderId')/div[2]/button/span[1]").is_displayed():
            time.sleep(1.0)
            sleeptimes += 1
            if sleeptimes > 60:
                print 'save time out'
                return

        #end APP信息
        print u"end app信息"
        
        #define 准备提交
        pic_first_add = False
       # driver.get(self.url + "/ios/versioninfo")
        time.sleep(1.0)
        driver.find_element_by_xpath("//div[@id='main-ui-view']/div[4]/div/div[2]/div[1]/ul/li[1]/a[1]").click()
        sleeptimes = 0
        while self.is_element_present(By.ID, "mainDropTrayFileSelect") == False:
            print "wait page loaded"
            time.sleep(1.0)
            sleeptimes += 1
            if sleeptimes > 60:
                print "page loaded timeout"
                return
        time.sleep(2.0)

        #切换到5.5英寸屏
        driver.find_element_by_xpath("//*[@id='localizationSection']/div[2]/div[3]/div[1]/div[1]/div/div[1]/ul/li[2]/a").click()
        #上传前先清空原有的图片
        time.sleep(10.0)
        if driver.find_element_by_xpath("//*[@id='containerVersPg']/span/div[1]/p[4]/a[1]").is_displayed() == False:
            driver.find_element_by_xpath("//*[@id='localizationSection']/div[2]/div[3]/div[1]/div[1]/div/div[6]/div[3]/div/a").click()
            driver.find_element_by_xpath("//*[@id='localizationSection']/div[2]/div[3]/div[1]/div[1]/div/div[6]/div[3]/div/a").click()
            time.sleep(2.0)
            driver.find_element_by_xpath("//*[@id='main-ui-view']/div[4]/div/div[3]/div[5]/div[1]/div/div/div/div/div[2]/div/button[2]").click()
            time.sleep(2.0)
        
        #sub defind 图片上传
        for parent,dirnames,filenames in os.walk(parser_xml.screenshot_address):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for filename in filenames:                        #输出文件信息
                file_path = os.path.join(parent,filename) #输出文件路径信息
                print file_path
                if file_path.find('png') < 0 and file_path.find('jpg') < 0:
                    continue
                driver.find_element_by_id("mainDropTrayFileSelect").clear()
                driver.find_element_by_id("mainDropTrayFileSelect").send_keys(os.path.join(parent,filename))
                time.sleep(10.0)
                sleeptimes = 0
                while driver.find_element_by_id("mainDropTrayFileSelect").is_enabled() == False:
                    print "image load"
                    time.sleep(1.0)
                    sleeptimes += 1
                    if sleeptimes > 60:
                        print "upload image timeout"
                        return

                if pic_first_add == False:
                    sleeptimes = 0
                    while driver.find_element_by_xpath("//div[@id='main-ui-view']/div[4]/div/div[3]/div[5]/div[2]/div/div/div/div[2]/div/button").is_displayed() is False:
                        sleeptimes += 1
                        time.sleep(1.0)
                        if sleeptimes > 10:
                            break
                    if driver.find_element_by_xpath("//div[@id='main-ui-view']/div[4]/div/div[3]/div[5]/div[2]/div/div/div/div[2]/div/button").is_displayed():
                        driver.find_element_by_xpath("//div[@id='main-ui-view']/div[4]/div/div[3]/div[5]/div[2]/div/div/div/div[2]/div/button").click()
                    pic_first_add = True
        #end sub defind 图片上传

        

        #描述
        #descripte = u"* Wallpaper collection, create your personal wallpaper gallery\n* Featured Ultra HD Wallpapers, each of them are Well recommended for you\n* Adaptation iPhone4, iPhone4s, iPhone5, iPhone6, iPhone6s, iPhone6s plus other models"
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[4]/div/span/span/textarea").clear()
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[4]/div/span/span/textarea").send_keys(parser_xml.describe)
        
        #关键词
        #keyvalue = u"ios10,壁纸大全,超高清动态壁纸,icon,图片,搜狗,百度,主题,电脑,美图,墙纸,美女,苹果手机助手,360,iphone,ipad,美图,玩图,美颜相机,爱壁纸,鲜柚壁纸,lol,主题,桌面"
        driver.find_element_by_xpath("//*[@id='localizationSection']/div[2]/div[5]/div[1]/span/input").clear()
        driver.find_element_by_xpath("//*[@id='localizationSection']/div[2]/div[5]/div[1]/span/input").send_keys(parser_xml.app_names[0]['keyword'])

        #技术支持网址
        driver.find_element_by_xpath("//*[@id='localizationSection']/div[2]/div[5]/div[2]/span/input").clear()
        driver.find_element_by_xpath("//*[@id='localizationSection']/div[2]/div[5]/div[2]/span/input").send_keys(parser_xml.technical_support)
        
        #选择最新构建版本
        # driver.find_element_by_link_text(u"请在提交 App 前先选择一个构建版本。").click()
        # time.sleep(5.0)
        # c_xpath = "//div[@id='appStorePageContent']/div[3]/div[1]/form/div/div[2]/div[1]/div/div/div/div/div[1]/div[2]/table/tbody/tr[1]/td[1]/div/span/a"
        # # sleeptimes = 0
        # # while driver.find_element_by_xpath(c_xpath) == False:
        # #     print "choice new version"
        # #     sleeptimes += 1
        # #     time.sleep(1.0)
        # #     if sleeptimes > 60:
        # #         return
        #
        # driver.find_element_by_xpath(c_xpath).click()
        # time.sleep(1.0)
        # driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div/form/div/div[2]/div/div/div/div/div/div[2]/div/button[2]").click()

        #ICON
        driver.find_element_by_xpath("(//input[@type='file'])[5]").clear()
        driver.find_element_by_xpath("(//input[@type='file'])[5]").send_keys(parser_xml.icon_address)
        
        #分级
        driver.find_element_by_link_text("编辑").click()
        driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div/form/div/div[3]/div/div/div[3]/div/div/div/div/div/table/tbody/tr/td[3]/div/span/a").click()
        driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div/form/div/div[3]/div/div/div[3]/div/div/div/div/div/table/tbody/tr[2]/td[3]/div/span/a").click()
        driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div/form/div/div[3]/div/div/div[3]/div/div/div/div/div/table/tbody/tr[3]/td[2]/div/span/a").click()
        driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div/form/div/div[3]/div/div/div[3]/div/div/div/div/div/table/tbody/tr[4]/td[2]/div/span/a").click()
        driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div/form/div/div[3]/div/div/div[3]/div/div/div/div/div/table/tbody/tr[5]/td[3]/div/span/a").click()
        driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div/form/div/div[3]/div/div/div[3]/div/div/div/div/div/table/tbody/tr[6]/td[3]/div/span/a").click()
        driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div/form/div/div[3]/div/div/div[3]/div/div/div/div/div/table/tbody/tr[7]/td[3]/div/span/a").click()
        driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div/form/div/div[3]/div/div/div[3]/div/div/div/div/div/table/tbody/tr[8]/td[3]/div/span/a").click()
        driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div/form/div/div[3]/div/div/div[3]/div/div/div/div/div/table/tbody/tr[9]/td[4]/div/span/a").click()
        driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div/form/div/div[3]/div/div/div[3]/div/div/div/div/div/table/tbody/tr[10]/td[3]/div/span/a").click()
        driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div/form/div/div[3]/div/div/div[3]/div/div/div/div/div/table/tbody/tr[11]/td[2]/div/span/a").click()
        driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div/form/div/div[3]/div/div/div[3]/div/div/div/div/div/table/tbody/tr[13]/td[2]/div/span/a").click()
        driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div/form/div/div[3]/div/div/div[3]/div/div/div/div/div/table/tbody/tr[14]/td[2]/div/span/a").click()
#        driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div/form/div/div[3]/div/div/div[3]/div/div/div/div/div[5]/div/button[2]").click()
        time.sleep(5.0)
        driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[3]/div/div[1]/div[3]/div[1]/div/div/div/div[5]/div/button[2]").click()
        
        #姓氏
        driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[3]/div/div[2]/div[3]/div[3]/div[1]/div[1]/span/input").clear()
        driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[3]/div/div[2]/div[3]/div[3]/div[1]/div[1]/span/input").send_keys(parser_xml.audit_information['firstName'])
        
        #名
        driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[3]/div/div[2]/div[3]/div[3]/div[1]/div[2]/span/input").clear()
        driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[3]/div/div[2]/div[3]/div[3]/div[1]/div[2]/span/input").send_keys(parser_xml.audit_information['secondName'])
        
        #电话
        driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[3]/div/div[2]/div[3]/div[3]/div[6]/div[2]/span/input").clear()
        driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[3]/div/div[2]/div[3]/div[3]/div[6]/div[2]/span/input").send_keys(parser_xml.audit_information['telPhone'])
        
        #邮箱
        driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[3]/div/div[2]/div[3]/div[3]/div[6]/div[3]/span/input").clear()
        driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[3]/div/div[2]/div[3]/div[3]/div[6]/div[3]/span/input").send_keys(parser_xml.audit_information['email'])
        
        #版权
        driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[3]/div/div[2]/div[1]/span/input").clear()
        driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[3]/div/div[2]/div[1]/span/input").send_keys(parser_xml.audit_information['copyright'])

        #app审核信息
        #姓氏
        driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[6]/div[1]/div[2]/div/div[1]/div[3]/div[1]/span/input").clear()
        driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[6]/div[1]/div[2]/div/div[1]/div[3]/div[1]/span/input").send_keys(parser_xml.audit_information['firstName'])
        #名
        driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[6]/div[1]/div[2]/div/div[1]/div[3]/div[2]/span/input").clear()
        driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[6]/div[1]/div[2]/div/div[1]/div[3]/div[2]/span/input").send_keys(parser_xml.audit_information['secondName'])
        #电话
        driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[6]/div[1]/div[2]/div/div[2]/div[3]/span/input").clear()
        driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[6]/div[1]/div[2]/div/div[2]/div[3]/span/input").send_keys(parser_xml.audit_information['telPhone'])
        #邮箱
        driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[6]/div[1]/div[2]/div/div[2]/div[4]/span/input").clear()
        driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[6]/div[1]/div[2]/div/div[2]/div[4]/span/input").send_keys(parser_xml.audit_information['email'])

        #备注
        if parser_xml.note is not None:
            driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[6]/div[2]/div/span/span/textarea").clear()
            driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[6]/div[2]/div/span/span/textarea").send_keys(parser_xml.note)
        
        #演示帐户
        driver.find_element_by_xpath("//*[@id='appStorePageContent']/div[3]/div[1]/form/div/div[6]/div[1]/div[1]/div/div[1]/div/span/a").click()
        
        #手动发布
        driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div[1]/form/div/div[7]/div[2]/div[1]/div/div/span/a").click()

#         #添加国家
#         sleeptimes = 0
#         driver.find_element_by_xpath("//*[@id='verlocHeader']/div/a").click()
#         while self.is_element_present(By.XPATH, "//*[@id='applocalizations']/div/table/tbody") == False:
#             print "add country"
#             driver.find_element_by_xpath("//*[@id='verlocHeader']/div/a").click()
#             time.sleep(1.0)
#             sleeptimes += 1
#             if sleeptimes > 60:
#                 print "add country time out"
#                 return
#
#         table = driver.find_element_by_xpath("//*[@id='applocalizations']/div/table/tbody")
#         trList = table.find_elements_by_xpath(".//tr")
#
#         #简体中文
#         index = 0
#         for element in trList:
#             if element.text.find(parser_xml.app_names[0]['type']) > -1:
#                 print "find"
#                 print index
#                 driver.execute_script("$('#verlocHeader table tbody tr:gt(0):eq(%s) td').click();"%(index-1))
#                 break
#             index += 1
#         time.sleep(1.0)
#         driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[4]/div/span/span/textarea").clear()
#         driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[4]/div/span/span/textarea").send_keys(parser_xml.describe)
#
#         #关键词
#         driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[5]/div[1]/span/input").clear()
#         driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[5]/div[1]/span/input").send_keys(parser_xml.app_names[1]['keyword'])
#
#         #技术支持网址
# #        driver.find_element_by_xpath("(//input[@type='text'])[3]").clear()
# #        driver.find_element_by_xpath("(//input[@type='text'])[3]").send_keys(parser_xml.technical_support)
#         driver.find_element_by_xpath("//*[@id='localizationSection']/div[2]/div[5]/div[2]/span/input").clear()
#         driver.find_element_by_xpath("//*[@id='localizationSection']/div[2]/div[5]/div[2]/span/input").send_keys(parser_xml.technical_support)
#
#         time.sleep(10.0)
        #添加国家
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
        #英国
        index = 0
        for element in trList:
            if element.text.find(parser_xml.app_names[1]['type']) > -1:
                print "find"
                print index
                driver.execute_script("$('#verlocHeader table tbody tr:gt(0):eq(%s) td').click();"%(index-1))
                break
            index += 1        
        time.sleep(1.0)
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[4]/div/span/span/textarea").clear()
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[4]/div/span/span/textarea").send_keys(parser_xml.describe)
        
        #关键词
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[5]/div[1]/span/input").clear()
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[5]/div[1]/span/input").send_keys(parser_xml.app_names[1]['keyword'])

        #技术支持网址
#        driver.find_element_by_xpath("(//input[@type='text'])[3]").clear()
#        driver.find_element_by_xpath("(//input[@type='text'])[3]").send_keys(parser_xml.technical_support)
        driver.find_element_by_xpath("//*[@id='localizationSection']/div[2]/div[5]/div[2]/span/input").clear()
        driver.find_element_by_xpath("//*[@id='localizationSection']/div[2]/div[5]/div[2]/span/input").send_keys(parser_xml.technical_support)

        time.sleep(10.0)
        #添加国家
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
        #澳大利亚
        index = 0
        for element in trList:
            if element.text.find(parser_xml.app_names[2]['type']) > -1:
                print "find"
                print index
                driver.execute_script("$('#verlocHeader table tbody tr:gt(0):eq(%s) td').click();"%(index-1))
                break
            index += 1
        time.sleep(1.0)
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[4]/div/span/span/textarea").clear()
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[4]/div/span/span/textarea").send_keys(parser_xml.describe)

        #关键词
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[5]/div[1]/span/input").clear()
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[5]/div[1]/span/input").send_keys(parser_xml.app_names[2]['keyword'])

        #技术支持网址
#        driver.find_element_by_xpath("(//input[@type='text'])[3]").clear()
#        driver.find_element_by_xpath("(//input[@type='text'])[3]").send_keys(parser_xml.technical_support)
        driver.find_element_by_xpath("//*[@id='localizationSection']/div[2]/div[5]/div[2]/span/input").clear()
        driver.find_element_by_xpath("//*[@id='localizationSection']/div[2]/div[5]/div[2]/span/input").send_keys(parser_xml.technical_support)

        #存储
        driver.find_element_by_xpath("//div[@id='appVerionInfoHeaderId']/div[2]/button[1]").click()
        time.sleep(5.0)        

        while driver.find_element_by_xpath("//div[@id='appVerionInfoHeaderId']/div[2]/button[1]/span[1]").is_displayed():
            time.sleep(1.0)
            sleeptimes += 1
            if sleeptimes > 60:
                print 'save time out'
                return
       # print "正在保存", driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[5]/div/div[3]/div[1]/div[2]/div[2]/button[1]/span[1]").is_displayed()
        #end define 准备提交
        self.setting_appInfo()
        self.setting_prince()
        fo = open("%s/SettingDetailInfo.txt" % cert_save_path, "w")
        fo.write("Success")
    
        time.sleep(5)
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
