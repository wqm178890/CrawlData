# -*- coding: utf-8 -*-
import xlrd
import MySQLdb
import sys

DBName = 'crawldata'
DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PWD = '123456'
DB_PORT = 3306

path = 'D:/Color.xlsx'
bk = xlrd.open_workbook(path)
xranges = range(bk.nsheets)
type = sys.getfilesystemencoding()

def insert(_sql):
    try:
        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PWD, db=DBName, charset="utf8")
        cur = conn.cursor()
        cur.execute('SET NAMES UTF8')
        conn.select_db(DBName)
        cur.execute(_sql)
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print e

def insert_sql(_data):
    _sql = 'INSERT ignore INTO color (en_name, cn_name, hex, rgb) values %s' % (_data)
    return _sql

def insert_data(en_name, cn_name, _hex, rgb):
    data_str = '(\'%s\',\'%s\',\'%s\',\'%s\'),' % (en_name, cn_name, _hex, rgb)
    return data_str

sh = bk.sheet_by_name('Sheet1')
nrows = sh.nrows
ncols = sh.ncols    
print nrows, ":", ncols
values = sh.cell_value(2, 3)
print values
data = ""
for i in range(1, nrows):
    tag = sh.cell_value(i, 0)
    name = sh.cell_value(i, 2)
    account = sh.cell_value(i, 3)
    data += insertData(name, tag, account)
data = data.rstrip(',')
sql = insertSql(data)
sql = sql.encode('utf-8')
print sql.decode('utf-8').encode(type)
insert(sql)

    


