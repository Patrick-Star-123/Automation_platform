
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.core.api import *

class Airtest_get_driver:
    def adb_connect(self,app_packagename):
        auto_setup(basedir=False,logdir=False)              #自动设置生成截图
        dev=connect_device('Android:///638c1c6b')
        # dev = device()
        equipment_number=str(dev.uuid)
        print(equipment_number)
        if equipment_number=='172.26.17.210:5555':          #无线链接运行时可以返回设备编号而不是IP地址
            equipment_number='b6254d85'
        poco=AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)     #获取poco驱动
        start_app(app_packagename)                          #打开APP
        return [dev,poco,equipment_number]

# Airtest_get_driver().adb_connect('com.shenjia.serve')