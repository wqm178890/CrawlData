# -*- coding: utf-8 -*-
from automatormonkey.monkeyrunnercore.MonkeyRunner import rMonkeyRunner
from automatormonkey.monkeyrunnercore.info.Enum import *
deviceName = '1'
device = rMonkeyRunner(__file__, deviceName)
FLAG.SCREENSHOT = False

device.closeApp('com.tencent.mm')
device.startActivity('com.tencent.mm/com.tencent.mm.ui.LauncherUI')
device.sleep(2.0)
device.click(UIELEMENT.TEXT, u'通讯录')
device.sleep(1.0)
device.click(UIELEMENT.TEXT, u'公众号')
device.sleep(1.0)
device.click(UIELEMENT.DESC, u'添加')