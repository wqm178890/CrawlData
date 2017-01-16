# -*- coding: utf-8 -*-
from xml.etree import ElementTree

class ParserXml():
    def __init__(self, xml_path):
        self.appid = ""
        self.account = ""
        self.password = ""
        self.app_names = []
        self.xml_path = xml_path
        self.main_category = ""
        self.minor_category = ""
        self.describe = ""
        self.technical_support = "http://wallbase.fr/"
        self.audit_information = {}
        self.note = ""
        self.icon_address = ""
        self.screenshot_address = ""

    def read_xml(self):
        root = ElementTree.parse(self.xml_path)

        self.appid = root.find('appId').text
        self.account = root.find('account').text
        self.password = root.find('password').text

        self.main_category = root.find('mainCategory').text
        self.minor_category = root.find('minorCategory').text

        self.describe = root.find("describe").text
        self.technical_support = root.find('technicalSupport').text

        auditInformation = root.find('auditInformation')
        self.audit_information['copyright'] = auditInformation.find('copyright').text
        self.audit_information['firstName'] = auditInformation.find('firstName').text
        self.audit_information['secondName'] = auditInformation.find('secondName').text
        self.audit_information['telPhone'] = auditInformation.find('telPhone').text
        self.audit_information['email'] = auditInformation.find('email').text

        self.note = root.find("note").text
        self.icon_address = root.find("iconAddress").text
        self.screenshot_address = root.find('screenShotAddress').text

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

if __name__ == '__main__':
    parser_xml = ParserXml("C:\\Users\\wqm\\Desktop\\test.xml")
    parser_xml.read_xml()
    print parser_xml.note is None
    parser_xml.appid
