#-*- coding: utf-8 -*-
'''
邮件发送带附件
'''

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, time

def send_email():
    localtime = time.localtime(time.time())
    today_date = time.strftime("%Y_%m_%d", localtime)
    
    msg = MIMEMultipart()
    
    att1 = MIMEText(open('E:/GDT_REPORT/%s_statistics.xlsx'%(today_date), 'rb').read(), 'base64', 'utf-8')
    att1['Content-Type'] = 'application/octet-stream'
    att1['Content-Disposition'] = 'attachment;filename="%s_statistics.xlsx"'%(today_date)  #邮件中附件显示名
    msg.attach(att1)
    
    att3 = MIMEText(open('E:/GDT_REPORT/%s_umeng.xlsx'%(today_date), 'rb').read(), 'base64', 'utf-8')
    att3['Content-Type'] = 'application/octet-stream'
    att3['Content-Disposition'] = 'attachment;filename="%s_umeng.xlsx"'%(today_date)  #邮件中附件显示名
    msg.attach(att3)    
    
    att2 = MIMEText(u'This is the EXCEL data for today, please check.','plain')
    msg.attach(att2)
    #邮件头
    email_list = ['wqm178890290@163.com', 'haizon@qq.com', 'fdzclsc@163.com', '1533681095@qq.com']
    msg['to'] = ','.join(email_list)
    msg['from'] = '178890290@qq.com'
    msg['subject'] = '今日报告_%s'%(today_date)
    
    #发送邮件
    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        #server.connect('smtp.qq.com')
        server.login('178890290', 'pbciujuyihqgcbba')
        server.sendmail(msg['from'], email_list, msg.as_string())
        server.quit()
        print u'发送成功'
    except Exception, e:
        print str(e)
        
#send_email()
