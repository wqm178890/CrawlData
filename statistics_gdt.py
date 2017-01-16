# -*- coding:utf-8 -*-

import time
import xlsxwriter
import xlrd, csv

    
APP_NAME = 0
ACTIVENESS = 4
AD_SHOW = 3
AD_CLICK = 4
AD_INCOME = 5
AD_EARNING = 6
START = u'开屏'
SOURCE = u'原生'
BANNER = u'Banner'

class gdtdata:
    def __init__(self, name):
        self.name = name
        self.show = 0.0
        self.click = 0.0
        self.income = 0.0
        self.earning = 0.0    
        
    def __repr__(self): 
        return "%.2f, %.2f, %.2f, %.2f\n"%(self.show, self.click, self.income, self.earning)
    
class write_xls:
    def __init__(self, filename):
        self.filename = filename
        self.workbook_write = xlsxwriter.Workbook(filename)
        #self.worksheet = self.workbook_write.add_worksheet('final_data')
        self.worksheets = {}
        self.nrows_list = {}
        #worksheet.write(0, 0, '应用名')
    
    def add_worksheet(self, name):
        worksheet = self.workbook_write.add_worksheet(name)
        self.worksheets[name] = worksheet
        self.nrows_list[name] = 0
        
    def write(self, row, col, text, name):
        worksheet = self.worksheets[name]
        worksheet.write(row, col, text)
        
    def write_data(self, data, name):
        worksheet = self.worksheets[name]
        row = self.nrows_list[name]
        col = 0
        for text in data:
            worksheet.write(row, col, text)
            col += 1     
        self.nrows_list[name] = row + 1
    
    def get_row(self, name):
        return self.nrows_list[name]
        
    def close(self):
        self.workbook_write.close()
        

def collect_gdt():
    localtime = time.localtime(time.time())
    str_data = time.strftime("%Y_%m_%d", localtime)    
    row = 0
    workbook = xlsxwriter.Workbook('E:\GDT_REPORT\\test.xlsx')
    worksheet = workbook.add_worksheet('gdt')
    filename_list = ['report_%s.csv'%str_data, 'report_%s(1).csv'%str_data, 'report_%s(2).csv' % str_data]
    first_file = True
    for filename in filename_list:
        first_row_data = 0
        filepath = "E:\\GDT_REPORT\\%s" % (filename)
        file_data = open(filepath, 'rb')
        reader = csv.reader(file_data)
        for row_data in reader:
            if first_file == False:
                if first_row_data == 0:
                    first_row_data += 1
                    continue
            first_file = False
            col = 0
            for i in row_data:
                #print unicode(i, "utf-8")
                i = i.replace(',', '')
                if row == 0:
                    worksheet.write(row, col, unicode(i, "utf-8"))
                else:
                    if col < 3 or col > 6:
                        worksheet.write(row, col, unicode(i, "utf-8"))
                    else:
                        worksheet.write(row, col, float(i))
                col += 1
            row += 1
    workbook.close()


def collect_umeng():
    localtime = time.localtime(time.time())
    str_data = time.strftime("%Y_%m_%d", localtime)    
    workbook = xlrd.open_workbook(r'E:\GDT_REPORT\%s_umeng.xlsx'%str_data)
    sheet = workbook.sheet_by_index(0)

    workbook_test = xlrd.open_workbook(r'E:\GDT_REPORT\test.xlsx')
    sheet_test = workbook_test.sheet_by_index(0)

    workbook_write = write_xls('%s\\%s_statistics.xlsx' %('E:\\GDT_REPORT', str_data))
    workbook_write.add_worksheet(START)
    workbook_write.add_worksheet(SOURCE)
    workbook_write.add_worksheet(BANNER)
    workbook_write.write_data([u'应用名', u'广告类型',u'元收益/用户', u'日活跃数', u'广告展示数', u'点击量', u'总收入', u'千次展示收益', u'点击率'], START)
    workbook_write.write_data([u'应用名', u'广告类型',u'元收益/用户', u'日活跃数', u'广告展示数', u'点击量', u'总收入', u'千次展示收益', u'点击率'], SOURCE)
    workbook_write.write_data([u'应用名', u'广告类型',u'元收益/用户', u'日活跃数', u'广告展示数', u'点击量', u'总收入', u'千次展示收益', u'点击率'], BANNER)
    total_income = 0
    for i in range(1, sheet.nrows):
        app_name = sheet.cell_value(i, APP_NAME)
        activeness = sheet.cell_value(i, ACTIVENESS)

        ad_type_start = gdtdata(u'开屏')
        ad_type_source = gdtdata(u'原生')
        ad_type_banner = gdtdata('Banner')
        for row in range(0, sheet_test.nrows):
            if sheet_test.cell_value(row, 2) == '%s(iOS)'%(app_name):
                ad_type = sheet_test.cell_value(row, 1)
                total_income += sheet_test.cell_value(row, AD_INCOME)
                if ad_type == u'开屏':
                    ad_type_start = add_ad_num(ad_type_start, sheet_test, row)
                elif ad_type == u'原生':
                    ad_type_source = add_ad_num(ad_type_source, sheet_test, row)
                elif ad_type == 'Banner':
                    ad_type_banner = add_ad_num(ad_type_banner, sheet_test, row)
               # print sheet_test.cell_value(row, 2)
        if activeness == 0:
            continue
        if ad_type_start.income > 0:
            workbook_write.write_data(get_data_list(ad_type_start, app_name, u'开屏', 
                                                   activeness), START)
        if i == sheet.nrows - 1:
            s_row = workbook_write.get_row(START)
            s_total_row = s_row + 1
            data_list = [u'总计', u'开屏', '=ROUND(G%d/D%d, 4)'%(s_total_row, s_total_row), '=SUM(D2:D%d)'%s_row, '=SUM(E2:E%d)'%s_row, '=SUM(F2:F%d)'%s_row,
                         '=SUM(G2:G%d)'%s_row, '=ROUND(G%d/E%d * 1000, 2)'%(s_total_row, s_total_row), '=TEXT(F%d/E%d, "0.00%%")' %(s_total_row, s_total_row)]
            workbook_write.write_data(data_list, START)
            workbook_write.write(s_total_row+1, 0, u'今日收入', START)
            print total_income
            workbook_write.write(s_total_row+1, 1, total_income, START)
            
        if ad_type_source.income > 0:
            
            workbook_write.write_data(get_data_list(ad_type_source, app_name, u'原生', 
                                                   activeness), SOURCE)
        if i == sheet.nrows - 1:
            s_row = workbook_write.get_row(SOURCE)
            s_total_row = s_row + 1
            data_list = [u'总计', u'原生', '=ROUND(G%d/D%d, 4)'%(s_total_row, s_total_row), '=SUM(D2:D%d)'%s_row, '=SUM(E2:E%d)'%s_row, '=SUM(F2:F%d)'%s_row,
                         '=SUM(G2:G%d)'%s_row, '=ROUND(G%d/E%d * 1000, 2)'%(s_total_row, s_total_row), '=TEXT(F%d/E%d, "0.00%%")' %(s_total_row, s_total_row)]
            workbook_write.write_data(data_list, SOURCE)            
        if ad_type_banner.income > 0:
            workbook_write.write_data(get_data_list(ad_type_banner, app_name, 'Banner', 
                                                   activeness), BANNER)
        if i == sheet.nrows - 1:
            s_row = workbook_write.get_row(BANNER)
            s_total_row = s_row + 1
            data_list = [u'总计', u'Banner', '=ROUND(G%d/D%d, 4)'%(s_total_row, s_total_row), '=SUM(D2:D%d)'%s_row, '=SUM(E2:E%d)'%s_row, '=SUM(F2:F%d)'%s_row,
                         '=SUM(G2:G%d)'%s_row, '=ROUND(G%d/E%d * 1000, 2)'%(s_total_row, s_total_row), '=TEXT(F%d/E%d, "0.00%%")' %(s_total_row, s_total_row)]
            workbook_write.write_data(data_list, BANNER)        
    workbook_write.close()

def get_data_list(data, app_name, type_name, activeness):
    rate_click = '=TEXT(%d/%d, "0.00%%")' %(data.click, data.show)
    earning = '=ROUND(%f/%d * 1000, 2)'%(data.income, data.show)
    return [app_name, type_name, float('%.4f'%(data.income/activeness)), activeness, data.show, data.click, data.income, earning, rate_click]
                
def add_ad_num(gdtdata, sheet, row):
    gdtdata.show += sheet.cell_value(row, AD_SHOW)
    gdtdata.click += sheet.cell_value(row, AD_CLICK)
    gdtdata.income += sheet.cell_value(row, AD_INCOME)
    gdtdata.earning += sheet.cell_value(row, AD_EARNING)
    return gdtdata


#collect_umeng()
    