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
bundle_name = u"流程测试媒体4"
bundle_id = "com.beemans.tests1.com"
xml_path = "/Users/haizon/Desktop/"

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
        bundle_name = u'%s'%value
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
        
        print "进入点击媒体管理"
        time.sleep(10.0)
        driver.find_element_by_link_text(u"媒体管理").click()
        time.sleep(2.0)
        print "进入点击新建媒体"
        driver.find_element_by_link_text(u"新建媒体").click()
        time.sleep(2.0)
        print "点击选择ios"
        driver.find_element_by_xpath("(//span[@name='osType'])[2]").click()
        print "设置应用名"
        driver.find_element_by_css_selector("input.w-program").clear()
        driver.find_element_by_css_selector("input.w-program").send_keys(bundle_name)
        print "设置关键词"
        driver.find_element_by_css_selector("input.w-keyword").clear()
        driver.find_element_by_css_selector("input.w-keyword").send_keys(u"壁纸,桌面,主题,锁屏,新闻,资讯,风景")
        print "选择媒体类别"
        driver.find_element_by_css_selector("span.mylistbox-text").click()
        time.sleep(1.0)
        driver.execute_script("$(\"div[class='popupContent'] div div:eq(7)\").click();")
        
        time.sleep(2.0)
        print "选择媒体分类"
        driver.find_element_by_xpath("//tr[4]/td/span[2]").click()
        time.sleep(1.0)
        driver.execute_script("$(\"div[class='popupContent'] div div:eq(3)\").click();")
        print "输入媒体简介"
        time.sleep(2.0)
        driver.find_element_by_css_selector("textarea.textarea-summary").clear()
        driver.find_element_by_css_selector("textarea.textarea-summary").send_keys(u"#用户体验NO.1的壁纸应用      #Appstore最具人气壁纸，长期盘踞免费榜前列                         #Appstore连续热门搜索推荐#超过99%用户5星好评，千万用户首选")
        print "输入包名"
        time.sleep(2.0)
        driver.find_element_by_xpath("(//input[@type='text'])[3]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[3]").send_keys(bundle_id)
        print "选择未上架"
        time.sleep(2.0)
        driver.find_element_by_xpath("(//span[@name='marketType'])[2]").click()
        time.sleep(2.0)
        print "下一步"
        driver.execute_script("$(\"a[class='btn-green']\").click()")
        time.sleep(2.0)
        
        appid = driver.find_element_by_xpath("//tr[3]/td/span").text
        
        #driver.find_element_by_link_text(u"下一步").click()
        driver.execute_script("$(\"a[class='btn-green']\").click()")
        time.sleep(2.0)
        
        
        
        file_object = open('%sGDTAppkey.txt'%xml_path, 'w')
        file_object.write("%s"%(appid))
        file_object.close()
    
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
    result = runner.run(unittest.makeSuite(SeleniumCreateAd))
