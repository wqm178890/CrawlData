# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import sys, getopt
reload(sys)
sys.setdefaultencoding("utf8")

opts, args = getopt.getopt(sys.argv[1:], "h", ["ai=", "ap=", "bn=", "bi=", "o="])

account_id = "2772636960@qq.com"
account_pwd = "Beemans91"
bundle_name = u"流程测试媒体3"
bundle_id = "com.beemans.tests1.com"
xml_path = "E:/"

for op, value in opts:
    print op
    if op == "--ai":
        print value
        account_id = value
    elif op == "--ap":
        print value
        account_pwd = value
    elif op == "--bn":
        print value
        bundle_name = value
    elif op == "--bi":
        print value
        bundle_id = value
    elif op == "--o":
        print value
        xml_path = value



class SeleniumCreateAd(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://e.qq.com"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_selenium_create_ad(self):
        driver = self.driver
        driver.get(self.base_url + "/dev/index.html")
        driver.find_element_by_link_text(u"登录").click()

        driver.switch_to.frame("ui_ptlogin")
        time.sleep(5.0)
        driver.find_element_by_id("switcher_plogin").click()
        driver.find_element_by_id("u").clear()
        driver.find_element_by_id("u").send_keys(account_id)
        driver.find_element_by_id("p").clear()
        time.sleep(2.0)
        driver.find_element_by_id("p").send_keys(account_pwd) 
        time.sleep(2.0)
        driver.find_element_by_id("login_button").click() 
        if self.is_element_present(By.ID, "login_button"):
            driver.find_element_by_id("login_button").click()
        driver.switch_to.default_content()
        time.sleep(5.0)
        
        
        driver.find_element_by_link_text(u"媒体管理").click()
        time.sleep(2.0)
        driver.find_element_by_link_text(u"新建媒体").click()
        time.sleep(2.0)
        driver.find_element_by_xpath("(//span[@name='osType'])[2]").click()
        driver.find_element_by_css_selector("input.w-program").clear()
        driver.find_element_by_css_selector("input.w-program").send_keys(bundle_name)
        driver.find_element_by_css_selector("input.w-keyword").clear()
        driver.find_element_by_css_selector("input.w-keyword").send_keys(u"壁纸,桌面,主题,锁屏,新闻,资讯,风景")
        driver.find_element_by_css_selector("span.mylistbox-text").click()
        time.sleep(1.0)
        driver.execute_script("$(\"div[class='popupContent'] div div:eq(7)\").click();")
        
        time.sleep(2.0)
        driver.find_element_by_xpath("//tr[4]/td/span[2]").click()
        time.sleep(1.0)
        driver.execute_script("$(\"div[class='popupContent'] div div:eq(3)\").click();")
        driver.find_element_by_css_selector("textarea.textarea-summary").clear()
        driver.find_element_by_css_selector("textarea.textarea-summary").send_keys(u"#用户体验NO.1的壁纸应用      #Appstore最具人气壁纸，长期盘踞免费榜前列                         #Appstore连续热门搜索推荐#超过99%用户5星好评，千万用户首选")
        driver.find_element_by_xpath("(//input[@type='text'])[3]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[3]").send_keys(bundle_id)
        driver.find_element_by_xpath("(//span[@name='marketType'])[2]").click()
        driver.find_element_by_link_text(u"下一步").click()
        time.sleep(2.0)
        appid = driver.find_element_by_xpath("//tr[3]/td/span").text
        
        driver.find_element_by_link_text(u"下一步").click()
        time.sleep(2.0)
        
        #开屏
        driver.find_element_by_link_text(u"广告位管理").click()
        time.sleep(2.0)
        driver.find_element_by_link_text(u"新建广告位").click()
        time.sleep(2.0)
        driver.find_element_by_css_selector("td > span.mylistbox-text").click()
        time.sleep(1.0)
        size = driver.execute_script("return $(\"div[class='mylistbox'] div div div div\").size()")
        for i in range(0, size):
            option = driver.execute_script("return $(\"div[class='mylistbox'] div div div div:eq(%d)\").text()"%(i))
            if option == bundle_name:
                driver.execute_script("$(\"div[class='mylistbox'] div div div div:eq(%d)\").click()"%(i))
                break
        time.sleep(1.0)
        
        driver.find_element_by_css_selector("input.basic-ipt").clear()
        driver.find_element_by_css_selector("input.basic-ipt").send_keys(u"开屏")        
        driver.find_element_by_xpath("//div[4]/span").click()
        driver.find_element_by_link_text(u"创建").click()
        time.sleep(2.0)
        Alert(driver).accept()
        time.sleep(5.0)
        coopen_id = driver.find_element_by_xpath("//tr[2]/td[1]/div/p[2]").text
        
        #原生列表
        
        driver.find_element_by_link_text(u"广告位管理").click()
        time.sleep(2.0)
        driver.find_element_by_link_text(u"新建广告位").click()
        time.sleep(2.0)
        driver.find_element_by_css_selector("td > span.mylistbox-text").click()
        time.sleep(1.0)
        size = driver.execute_script("return $(\"div[class='mylistbox'] div div div div\").size()")
        for i in range(0, size):
            option = driver.execute_script("return $(\"div[class='mylistbox'] div div div div:eq(%d)\").text()"%(i))
            if option == bundle_name:
                driver.execute_script("$(\"div[class='mylistbox'] div div div div:eq(%d)\").click()"%(i))
                break
        time.sleep(1.0)
        
        driver.find_element_by_css_selector("input.basic-ipt").clear()
        driver.find_element_by_css_selector("input.basic-ipt").send_keys(u"原生列表广告")        
        driver.find_element_by_xpath("//tr[3]/td/div[5]/span").click()
        driver.find_element_by_link_text(u"创建").click()
        time.sleep(2.0)
        Alert(driver).accept()
        time.sleep(2.0)
        Alert(driver).accept()        
        time.sleep(5.0)   
        source_list_id = driver.find_element_by_xpath("//tr[2]/td[1]/div/p[2]").text
        
        #原生详情
        driver.find_element_by_link_text(u"广告位管理").click()
        time.sleep(2.0)
        driver.find_element_by_link_text(u"新建广告位").click()
        time.sleep(2.0)
        driver.find_element_by_css_selector("td > span.mylistbox-text").click()
        time.sleep(1.0)
        size = driver.execute_script("return $(\"div[class='mylistbox'] div div div div\").size()")
        for i in range(0, size):
            option = driver.execute_script("return $(\"div[class='mylistbox'] div div div div:eq(%d)\").text()"%(i))
            if option == bundle_name:
                driver.execute_script("$(\"div[class='mylistbox'] div div div div:eq(%d)\").click()"%(i))
                break
        time.sleep(1.0)
        
        driver.find_element_by_css_selector("input.basic-ipt").clear()
        driver.find_element_by_css_selector("input.basic-ipt").send_keys(u"原生详情大图")        
        driver.find_element_by_xpath("//tr[3]/td/div[5]/span").click()
        time.sleep(1.0)
        driver.find_element_by_xpath("//tr[2]/td/div[4]/span").click()
        driver.find_element_by_link_text(u"创建").click()
        time.sleep(2.0)
        Alert(driver).accept()
        time.sleep(2.0)
        Alert(driver).accept()        
        time.sleep(5.0)        
        source_detail_id = driver.find_element_by_xpath("//tr[2]/td[1]/div/p[2]").text
        
        file_object = open('%sresult.xml'%xml_path, 'w')
        file_object.write("<?xml version=\"1.0\"?><values><key>应用</key><value>%s</value><key>开屏</key><value>%s</value><key>原生列表</key><value>%s</value><key>原生详情</key><value>%s</value></values>"%(appid, coopen_id, source_list_id, source_detail_id))
        file_object.close( )        
    
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
        #self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
