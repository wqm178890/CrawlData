# -*- coding:utf-8 -*-

import time
import xlsxwriter
import xlrd, csv

import codecs

def collect_gdt(filepath):
    data = []
    row = 0
    first_file = True
    #for filename in filename_list:
    first_row_data = 0
    #filepath = "E:\\GDT_REPORT\\%s" % (file_name)
    file_data = open(filepath, 'rb')

        #reader = csv.reader( (line.replace('\0', '') for line in f))
    reader = csv.reader(file_data)
    for row_data in reader:
        list_data = []
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
                continue
            else:
                if col < 3 or col > 6:
                    list_data.append(unicode(i, "utf-8"))
                else:
                    list_data.append(i)

            col += 1
        if len(list_data) > 0:
            data.append(list_data)
        row += 1
    print data
    return data

collect_gdt("E:\\GDT_REPORT\\report_2017_01_08.csv")