from appium import webdriver
import time
#使用appium操作手机


class Appium_get_driver:
    def establish_ssession(self,platformName,platformVersion,deviceName,appPackage_appActivity):       #建立ssession
        di={}
        di['platformName']=platformName[0]                                      #声明系统
        di['platformVersion']=platformVersion[0]                                #声明系统版本号
        di['deviceName']=deviceName[0]                                          #声明设备名称
        di['appPackage']=appPackage_appActivity[0]                              #声明包名
        di['appActivity']=appPackage_appActivity[1]                             #声明appActivity
        print('运行前请先确认是否已打开Appium服务')
        driver = webdriver.Remote('http://localhost:4723/wd/hub', di)       #建立ssession
        driver.implicitly_wait(10)
        return driver                                                       #返回driver对象
