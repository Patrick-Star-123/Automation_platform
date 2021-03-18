#coding:utf-8
#目录：获取设备编号、给设备安装测试包
import os
class Connect:
    def equipment_number(self):     #获取设备编号
        # os.system('adb connect 172.16.3,114')                             #可以通过局域网连接手机，但目前会报错暂未找到处理方案
        device_information=os.popen('adb devices').read()                   #获取设备信息
        device_information=device_information.strip().split('\n')           #将设备信息以列表形式存放
        equipment_numbers=[]
        for i in range(1,len(device_information)):                          #通过设备信息列表长度取循环次数，并从下标1开始计算（下标0位为标题）
            equipment_numbers.append(device_information[i].split('\t')[0])   #获取每个设备编号，并将所有编号放进列表
        if equipment_numbers[0]=='* daemon started successfully *':
            equipment_numbers.remove(equipment_numbers[0])
        if equipment_numbers[0]=='List of devices attached ':
            equipment_numbers.remove(equipment_numbers[0])
        # print(equipment_numbers)
        return equipment_numbers

    def install_app(self,equipment_numbers):  #给所有设备安装测试包
        for i in equipment_numbers:
            os.system(r'adb -s %s install -r C:\Users\Administrator\Desktop\develop\app\serve\测试\shenjia2.6.4_2021-03-15_debug.apk'%(i))    #安装测试包
            print('设备【%s】安装成功'%(i))                                                                                                    #打印日志

# Connect().install_app(Connect().equipment_number())