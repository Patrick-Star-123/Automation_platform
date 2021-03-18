import sys,os,time
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from data_acquisition.get_document_data import *
from function import appium_driver
from function import link_mobile_phone
from function.intermediate import Intermediate,Appium_run,Airtest_run,Finishing_touches

class Run_:
    def __init__(self):
        self.startime=time.time()                                                        #获取测试开始时间
        self.address=Get_document_data().address_information(rootPath)                   #获取配置文件地址,用例地址[0]、报告存放地址[1]、截图存放地址、[2]、日志存放地址[3]
        tset_case_address=self.address[0]                                                #获取用例地址
        table_data=Get_document_data().table_data(tset_case_address)
        self.test_case=Get_document_data().sheet_data(table_data,rootPath)               #取出用例数据
        equipment_number_list=link_mobile_phone.Connect().equipment_number()             #取出设备编号列表
        device_information=Get_document_data().configuration_file(rootPath)              #获取设备信息列表[platformName,platformVersion,deviceName,appPackage_appActivity,test_case_configuration_list]
        self.other_information=Get_document_data().other_information(rootPath)           #获取其他配置信息，运行方式[0],开始编号[1]
        self.number_of_devices=len(equipment_number_list)                                #取出设备数量
        self.app_packagename=device_information[3][0]                                    #取出APP包名
        self.test_case_configuration_list=device_information[4]                          #取出设备的用例配置列表（设备列表格式：[[‘设备编号’, [开始条数，结束条数]]]）
        print('数据初始化成功')

    def run_(self):
        if self.other_information[0]=='airtest':                                                                    #判断运行方式是否为airtest
            dev_poco=Intermediate().operation_mode_judgment(self.app_packagename,self.address)                      #初始化APP、驱动并连接设备
            test_result=Airtest_run().airtest_run(self.test_case,dev_poco[1],dev_poco[0],dev_poco[2],
                                      self.app_packagename,self.address,
                                      self.test_case_configuration_list,rootPath)                                   #调用airtest运行
            Finishing_touches().finishing_touches(test_result,self.startime,self.address,self.number_of_devices,dev_poco[2],rootPath,self.other_information)    #收尾工作，生成并打包测试报告，发送邮件


        elif self.other_information[0]=='appium':                                                                   #判断运行方式是否为appium
            app_driver = appium_driver.Appium_get_driver().establish_ssession(self.device_information[0],
                                                                              self.device_information[1],
                                                                              self.device_information[2],
                                                                              self.device_information[3])            # 启动链接并获得drover对象（前提是已连接设备）
            Appium_run().appium_run(self.test_case,app_driver,self.other_information,
                                    self.app_packagename,self.address,
                                    self.number_of_devices,self.startime,
                                    self.test_case_configuration_list)                                               #调用appium运行
            print('建立ssession成功')
        else:
            print('配置文件运行方式配置异常')

Run_().run_()

