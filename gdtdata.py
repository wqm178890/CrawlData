# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re,xlsxwriter
import statistics_gdt, SendEmail

account_id = "beebees@qq.com"
account_pwd = "Beemans912"
bundle_name = "BeemansTest"
bundle_id = "com.beemans.tests.com"
cert_save_path = "E:\\GDT_REPORT"
cert_file_path = "C:\\beenice.certSigningRequest"

class Test(unittest.TestCase):
    def setUp(self):
        self.wait = 300
        self.fp = webdriver.FirefoxProfile()
        self.fp.set_preference("browser.download.folderList", 2)
        self.fp.set_preference("browser.download.manager.showWhenStarting", False)
        self.fp.set_preference("browser.download.dir", cert_save_path)
        self.fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-download")
        self.verificationErrors = []
        self.driver = webdriver.Firefox(firefox_profile=self.fp)        
        self.driver.implicitly_wait(self.wait)
        self.base_url = "http://e.qq.com"
        self.verificationErrors = []
        
        self.accept_next_alert = True
    
    def get_data(self, account, pwd):
        driver = self.driver
        driver.get(self.base_url + "/dev/index.html")
        driver.find_element_by_link_text(u"登录").click()

        driver.switch_to.frame("ui_ptlogin")
        time.sleep(5.0)
        driver.find_element_by_id("switcher_plogin").click()
        driver.find_element_by_id("u").clear()
        driver.find_element_by_id("u").send_keys(account)
        driver.find_element_by_id("p").clear()
        time.sleep(2.0)
        driver.find_element_by_id("p").send_keys(pwd) 
        time.sleep(2.0)
        driver.find_element_by_id("login_button").click() 
        if self.is_element_present(By.ID, "login_button"):
            driver.find_element_by_id("login_button").click()
        driver.switch_to.default_content()
        time.sleep(5.0)
        while self.is_element_present(By.LINK_TEXT, u"下载报告") == False:
            time.sleep(1.0)
        time.sleep(10.0)
        driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[3]/div/div/ul/li[1]/span").click()
        while self.is_element_present(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/ul/li/span") == False:
            time.sleep(1.0)              
            driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[3]/div/div/ul/li[1]/span").click()
        time.sleep(2.0)
        driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div/ul/li/span").click()
        time.sleep(5.0)
        
        #媒体
        driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[3]/div/div/ul/li[2]/span").click()
        time.sleep(2.0)
        driver.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/div/ul/li/span").click()
        driver.find_element_by_link_text(u"查询").click()
        time.sleep(5.0)
        driver.find_element_by_link_text(u"下载报告").click()
        time.sleep(10.0)
    
    def test_a_(self):
        self.get_data("2045571685", "Beemans91")
    
    def test_b_(self):
        self.get_data("2772636960@qq.com", "Beemans91")
    
    def test_c_(self):
        self.get_data("haizon@qq.com", "5x10xngha")
    
    def test_d_umeng(self):
        driver = self.driver
        driver.get("http://mobile.umeng.com/apps")
        #driver.find_element_by_id("doc").click()
        driver.find_element_by_id("umengLoginBtn").click()
        while self.is_element_present(By.CSS_SELECTOR, "input[type=\"text\"]") == False:
            time.sleep(1.0)
        time.sleep(1.0)
        driver.find_element_by_css_selector("input[type=\"text\"]").clear()
        driver.find_element_by_css_selector("input[type=\"text\"]").send_keys("178890290@qq.com")
        driver.find_element_by_css_selector("input[type=\"password\"]").clear()
        driver.find_element_by_css_selector("input[type=\"password\"]").send_keys("qawsedrft123")        
        driver.find_element_by_id("submitForm").click()
        time.sleep(2.0)
        #element = driver.find_element_by_link_text(u"授权应用列表")
        while self.is_element_present(By.LINK_TEXT, u'授权应用列表') == False:
            time.sleep(1.0)

        element = driver.find_element_by_link_text(u"授权应用列表")
        time.sleep(3.0)
        element.click()
        while self.is_element_present(By.XPATH, "//table") == False:
            time.sleep(1.0)  
        time.sleep(10.0)
        driver.find_element_by_link_text(u'在一页内显示').click()
        time.sleep(10.0)
        table = driver.find_element_by_xpath("//table")

        localtime = time.localtime(time.time())
        filename = time.strftime("%Y_%m_%d", localtime)
        workbook = xlsxwriter.Workbook('%s\\%s_umeng.xlsx' %(cert_save_path, filename))
        worksheet = workbook.add_worksheet('umeng')        
        #插入头部信息
        thead = table.find_element_by_xpath(".//thead") 
        thead_tr = table.find_element_by_xpath(".//tr")  
        thead_th_list = thead_tr.find_elements_by_xpath(".//th")
        for i in range(0, len(thead_th_list)):
            if i < 1:
                continue
            worksheet.write(0, i-1, thead_th_list[i].text)
        
        #插入数据
        tbody = table.find_element_by_xpath(".//tbody")
        tr_list = tbody.find_elements_by_xpath(".//tr")
        
        row = 1
        for tr in tr_list:
            col = 0
            td_list = tr.find_elements_by_xpath(".//td")
            info = ""
            for td in td_list:
                #info += td.text + "\t\t"
                col += 1
                if col < 2:
                    continue
                text = td.text
                if col > 2 and col < 10:
                    text = int(td.text.strip())
                worksheet.write(row, col - 2, text)
            #print info
            row += 1
        workbook.close()     
        
    def test_z_collect_data(self):
        statistics_gdt.collect_gdt()
        statistics_gdt.collect_umeng()
        SendEmail.send_email()
    
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
        #self.driver.close()
        #self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

