# -*- coding: utf-8 -*-

import hashlib
import urllib
import urllib2
import json
import MySQLdb
import unicodedata
import hashlib, re, urlparse
import CsvExcelParser

class MySqlDBParser():

    def __init__(self):
        self.DBName = 'statistic'
        self.DB_HOST = '59.110.0.42'
        self.DB_USER = 'remote'
        self.DB_PWD = 'Combeemans91'
        self.DB_PORT = 3306
        self.conn = None

    def connect_db(self):
        try:
            self.conn = MySQLdb.connect(host=self.DB_HOST, port=self.DB_PORT, user=self.DB_USER, passwd=self.DB_PWD, db=self.DBName, charset="utf8")
        except MySQLdb.Error, e:
            print e

    def close_db(self):
        try:
            self.conn.close()
        except MySQLdb.Error, e:
            print e

    def insert_data(self, sql):
        try:
            self.conn = MySQLdb.connect(host=self.DB_HOST, port=self.DB_PORT, user=self.DB_USER, passwd=self.DB_PWD, db=self.DBName, charset="utf8")
            cur = self.conn.cursor()
            cur.execute('SET NAMES UTF8')
            cur.execute('set global max_allowed_packet = 2*1024*1024*10')
            self.conn.select_db(self.DBName)
            count = cur.execute(sql)
            results = cur.fetchall()
            self.conn.commit()
            cur.close()
            self.conn.close()
        except MySQLdb.Error, e:
            print e

    def get_google_table(self):
        google_table = []
        google_table.append("date_time")
        google_table.append("app_name")
        google_table.append("request_times")
        google_table.append("match_request_times")
        google_table.append("match_rate")
        google_table.append("show_times")
        google_table.append("show_rate")
        google_table.append("click_times")
        google_table.append("click_rate")
        google_table.append("admob_cpm")
        google_table.append("cpm")
        google_table.append("incomes")
        google_table.append("eligibility_show_times")
        google_table.append("measurable_show_times")
        google_table.append("visible_show_times")
        google_table.append("measurable_rate")
        google_table.append("visible_rate")
        return google_table

    def get_gdt_table(self):
        gdt_table = []
        gdt_table.append("date_time")
        gdt_table.append("ad_type")
        gdt_table.append("app_name")
        gdt_table.append("ad_show")
        gdt_table.append("ad_click")
        gdt_table.append("cpm")
        gdt_table.append("incomes")
        gdt_table.append("click_rate")
        return gdt_table

    def get_insert_sql(self, table, data, table_name):
        keys = ""
        values = ""
        for key in table:
            keys += key + ","

        keys = keys.rstrip(',')
        print keys
        for data_list in data:
            value = ""

            for string in data_list:
                if string.isdigit():
                    value += string + ","
                else:
                    value += "\"" + string + "\","

            value = value.rstrip(',')
            print value
            values += "(%s)," % value

        values = values.rstrip(',')

        sql = "insert ignore into %s (%s) values %s;" % (table_name, keys, values)
        print sql
        return sql

if __name__ == '__main__':
    parser = MySqlDBParser()
    data = CsvExcelParser.collect_gdt("E:\\GDT_REPORT\\report_2017_01_08.csv")
    sql = parser.get_insert_sql(parser.get_gdt_table(), data, "gdt_data")
    parser.insert_data(sql)







