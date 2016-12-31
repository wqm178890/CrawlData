# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, sys
import chardet
reload(sys)
sys.setdefaultencoding("utf8")

account_id = "beebees@qq.com"
account_pwd = "Beemans912"
appid = "1190040404"
appname = u"这是一个用来跑测试流程的应用"
img_path = "C:\\beenice.certSigningRequest"
indextype = u"工具"
subtype = u"旅游"
icon_path = u"D:\\桌面\\AppIcon\\@1024.png"


class Test(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.wait = 300
        self.driver.implicitly_wait(self.wait)
        self.url = "https://itunesconnect.apple.com/WebObjects/iTunesConnect.woa/ra/ng/app/%s"%(appid)
        self.verificationErrors = []
        self.accept_next_alert = True
        
    def testSettingInfo(self):
        driver = self.driver
        driver.get(self.url)
        #帐号登录
        driver.switch_to.frame("aid-auth-widget-iFrame");
        driver.find_element_by_xpath("//*[@id='appleId']").clear()
        driver.find_element_by_xpath("//*[@id='appleId']").send_keys(account_id)
        driver.find_element_by_id("pwd").clear()
        driver.find_element_by_id("pwd").send_keys(account_pwd)
        time.sleep(1.0)
        driver.find_element_by_id("sign-in").click()  
        driver.switch_to.default_content()
        #
        time.sleep(5.0)
        while self.is_element_present(By.XPATH, "(//input[@type='text'])[2]") == False:
            time.sleep(1.0)
        
        #define APP信息
        
        #应用名称
        driver.find_element_by_xpath("(//input[@type='text'])[2]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[2]").send_keys(appname)      

        #类别
        Select(driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div/form/div[6]/div[2]/div/div[2]/div[2]/span/span/select")).select_by_visible_text(indextype)
        Select(driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div/form/div[6]/div[2]/div/div[2]/div[2]/div[3]/span/span/select")).select_by_visible_text(subtype)
        
        #保存
        if driver.find_element_by_css_selector("button").is_enabled(): 
            driver.find_element_by_css_selector("button").click()
        time.sleep(2.0)
        print "正在保存", driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[5]/div/div[3]/div[1]/div[2]/div[2]/button[1]/span[1]").is_displayed()
        
        #end APP信息
        print u"end app信息"..
        
        #define 准备提交
       # driver.get(self.url + "/ios/versioninfo")
        driver.find_elements_by_xpath("//div[@id='main-ui-view']div[5]/div/div[2]/div[1]/ul/li[1]/a[1]").click()
        while self.is_element_present(By.XPATH, "//*[@id='applocalizations']/div/table/tbody") == False:
            time.sleep(1.0)      
        time.sleep(2.0)
        driver.find_element_by_id("mainDropTrayFileSelect").clear()
        driver.find_element_by_id("mainDropTrayFileSelect").send_keys(u"D:\\桌面\\test1.jpg") 
        driver.find_element_by_id("mainDropTrayFileSelect").send_keys(u"D:\\桌面\\test2.jpg") 
        driver.find_element_by_id("mainDropTrayFileSelect").send_keys(u"D:\\桌面\\test3.jpg") 
        driver.find_element_by_id("mainDropTrayFileSelect").send_keys(u"D:\\桌面\\test4.jpg")

        #描述
        descripte = u"* Wallpaper collection, create your personal wallpaper gallery\n* Featured Ultra HD Wallpapers, each of them are Well recommended for you\n* Adaptation iPhone4, iPhone4s, iPhone5, iPhone6, iPhone6s, iPhone6s plus other models"
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[4]/div/span/span/textarea").clear()
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[4]/div/span/span/textarea").send_keys(descripte)
        
        #关键词
        keyvalue = u"ios10,壁纸大全,超高清动态壁纸,icon,图片,搜狗,百度,主题,电脑,美图,墙纸,美女,苹果手机助手,360,iphone,ipad,美图,玩图,美颜相机,爱壁纸,鲜柚壁纸,lol,主题,桌面"
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[5]/div[1]/span/input").clear()
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[5]/div[1]/span/input").send_keys(keyvalue)

        #技术支持网址
        driver.find_element_by_xpath("(//input[@type='text'])[3]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[3]").send_keys("http://wallbase.fr/")    
        
        #选择最新构建版本
        driver.find_element_by_link_text(u"请在提交 App 前先选择一个构建版本。").click()
        driver.find_element_by_css_selector("a.radiostyle").click()        
        
        #ICON
        driver.find_element_by_xpath("(//input[@type='file'])[5]").clear()
        driver.find_element_by_xpath("(//input[@type='file'])[5]").send_keys(icon_path) 
        
        #版权
        driver.find_element_by_xpath("(//input[@type='text'])[6]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[6]").send_keys(u"beenice")        
        
        #手动发布
        driver.find_element_by_xpath("//div[@id='appStorePageContent']/div[3]/div[1]/form/div/div[7]/div[2]/div[1]/div/div/span/a").click()
        
        
        #添加国家
        driver.find_element_by_xpath("//*[@id='verlocHeader']/div/a").click()
        while self.is_element_present(By.XPATH, "//*[@id='applocalizations']/div/table/tbody") == False:
            print "test"
            driver.find_element_by_xpath("//*[@id='verlocHeader']/div/a").click()
            time.sleep(1.0)
        
        table = driver.find_element_by_xpath("//*[@id='applocalizations']/div/table/tbody")
        trList = table.find_elements_by_xpath(".//tr") 
        
        #澳大利亚
        index = 0
        for element in trList:
            if element.text.find(u"澳大利亚") > -1:
                print "find"
                print index
                driver.execute_script("$('#verlocHeader table tbody tr:gt(0):eq(%s) td').click();"%(index-1))
                break
            index += 1
        time.sleep(1.0)
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[4]/div/span/span/textarea").clear()
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[4]/div/span/span/textarea").send_keys(descripte)
        
        #英国
        index = 0
        for element in trList:
            if element.text.find(u"英国") > -1:
                print "find"
                print index
                driver.execute_script("$('#verlocHeader table tbody tr:gt(0):eq(%s) td').click();"%(index-1))
                break
            index += 1        
        time.sleep(1.0)
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[4]/div/span/span/textarea").clear()
        driver.find_element_by_xpath("//div[@id='localizationSection']/div[2]/div[4]/div/span/span/textarea").send_keys(descripte)
        
        #存储
        driver.find_element_by_xpath("//div[@id='appVerionInfoHeaderId']/div[2]/button[1]").click()
        time.sleep(5.0)        
        
        print "正在保存", driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[5]/div/div[3]/div[1]/div[2]/div[2]/button[1]/span[1]").is_displayed()
        #end define 准备提交
        
        
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