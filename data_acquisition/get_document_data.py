import xlrd
import os
from currency.data_processing import Data_processing
#获取文件数据
class Get_document_data():
    def table_data(self,tset_case_address,):
        data=xlrd.open_workbook(tset_case_address)         #打开文件
        table=data.sheet_by_name('Sheet1')                                                   #获取表格数据
        datas=[]                                                                             #创建变量准备接受数据
        for i in range(table.nrows):                                                         #按表格行数循环遍历
            datas.append(table.row_values(i))                                                #将每行数据放进提前准备好的列表
        return datas

    def sheet_data(self,datas,rootPath):             #用例数据格式化
        yongli_list=[]
        yongli=[]
        data=[]
        start_number=self.other_information(rootPath)[1]
        for i in datas:                                                                      #遍历每条用例
            a=Data_processing().remove_data(i)                                                   #删除所有空元素
            data.append(a)                                                                   #将删除完空元素的用例放到新的列表中
        for i in data[start_number:]:                                                                   #遍历每条用例，去掉标题从第文档二行开始遍历
            datas=i
            a=['丨']
            datas=['间隔符'if i in a else i for i in datas]                                  #用‘间隔符’替换所有‘丨’（其实不需要）
            datas=[str(i)for i in datas]                                                     #遍历把用例中的所有数据转为字符串类型
            datas='丨'.join(datas)                                                            #将列表转换为字符串，且每个元素用‘，’隔开
            datas=datas.split('间隔符')                                                      #将字符串中的‘间隔符’作为分割点，放入列表中
            yongli_list.append(datas)
        yongli_list2=[]
        for i in yongli_list:
            yongli1=Data_processing().remove_data(i)
            yongli_list2.append(yongli1)
        for y in yongli_list2:
            temporary=[]
            for j in y:
                result=j.split('丨')                                                      #将所有字符串中以‘，’为分割点，把所有数据放入列表
                if result[0]=='':
                    del result[0]
                temporary.append(result)                                                 #将每条操作放入一个用例列表内
            yongli.append(temporary)                                                     #将每条用例列表放入一个大列表内
        return yongli                                                                    #返回一个三维列表，第一级是用例列表--第二级是操作列表--第三级是元素列表

    def configuration_file(self,rootPath):                            #读取所有设备配置文件信息
        configuration=open(r'%s\configuration file.txt'%(rootPath),encoding='UTF-8-sig').read()    #打开读取配置文件 需转码
        data=configuration.split('\n')                                                               #以换行为间隔符将数据放入data列表
        device_information=data[:6]                                                         #只取前面6行数据（设备信息）
        device_data=[]
        appPackage_appActivity=[]
        test_case_configuration_list=[]
        for i in device_information:                                                        #遍历设备信息列表
            device_data.append(i.split('='))                                                #将设备信息以‘=’作为分隔符放入二维列表
        for i in device_data:                                                               #遍历新的设备信息列表
            if i[0]=='platformName':                                                        #判断列表第一位是否是'platformName'
                platformName=i[1].split('、')                                               #是则将第二位以‘、’为分隔符放入platformName列表
            elif i[0]=='platformVersion':
                platformVersion=i[1].split('、')
            elif i[0]=='deviceName':
                deviceName=i[1].split('、')
            elif i[0]=='测试机用例配置':                                                     #获取每台测试机运行的用例开始条数与结束条数
                data_list=i[1].split('、')
                for k in data_list:
                    data=k.split(',')
                    test_case_configuration=[data[0],[int(data[1].split('-')[0]),int(data[1].split('-')[1])]]     #test_case_configuration为列表[[‘设备编号’, [开始条数，结束条数]]]
                    test_case_configuration_list.append(test_case_configuration)
            else:
                appPackage_appActivity.append(i[1])                                         #将appPackage、appActivity信息放入appPackage_appActivity列表
        return [platformName,platformVersion,deviceName,appPackage_appActivity,test_case_configuration_list]             #返回四个列表（二维列表）

    def address_information(self,rootPath):              #读取所有地址配置文件信息和运行方式信息
        address=open(r'%s\configuration file.txt'%(rootPath),encoding='UTF-8-sig').read()     #读取配置文件
        data=address.split('\n')[6:11]                                                          #取地址信息并将信息以换行为间隔符分割放入地址列表
        address_list=[]
        for i in data:
            address_list.append(i.split('='))                                                   #将每个地址用‘=’为间隔符分割
        case_address=address_list[0][1]                                                         #在列表中取用例地址
        report_address=address_list[1][1]                                                       #在列表中取报告地址
        screenshot_address=address_list[2][1]                                                   #在列表中取截图地址
        journal_address=address_list[3][1]                                                      #在列表中取日志地址
        peration_mode=address_list[4][1]                                                        #在列表中取运行方式(appium/airtest)
        return [case_address,report_address,screenshot_address,journal_address]    #将四个地址放入列表返回

    def other_information(self,rootPath):                                                                #获取其他配置信息，运行方式、从第几条开始等
        other=open(r'%s\configuration file.txt'%(rootPath),encoding='UTF-8-sig').read().split('\n')[10:]
        other_information_list=[]                                                       #other_information_list[运行方式、从第几条开始、发送者邮件、接受者邮件]
        for data in other:
            other_information_list.append(data.split('='))
        peration_mode=other_information_list[0][1]
        start_number=int(other_information_list[1][1])
        login_email=other_information_list[3][1]
        login_pwd=other_information_list[4][1]
        email_server_address=other_information_list[2][1]
        if other_information_list[5][1].find('、') == -1:                                #接收者邮箱使用‘、’分割
            recipient_email=[other_information_list[5][1]]
        else:
            recipient_email=other_information_list[5][1].split('、')
        email_address=[recipient_email,email_server_address,login_email,login_pwd]

        return [peration_mode,start_number,email_address]
        #返回格式['运行方式', '从第几条开始',  [ ['接受者邮件1','接受者邮件2'],邮箱服务器地址，登陆用户名/发送者邮箱，邮箱登陆密码]]


