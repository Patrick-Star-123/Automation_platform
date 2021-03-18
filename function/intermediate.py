import shutil,os,time
from function import airtest_driver
from function import appium_function_test_case
from function import airtest_function_test_case
from function import back_to_home
from currency.data_processing import Data_processing
from currency.screenshot import Screenshot
from currency.report_generation import Report_generation
from currency.send_mail import Email


class Intermediate:
    def operation_mode_judgment(self,app_packagename,address):
        dev_poco=airtest_driver.Airtest_get_driver().adb_connect(app_packagename)   #链接手机打开APP，并获取设备编号、 poco驱动对象、dev对象(用来运行shell指令）
        try:
            shutil.rmtree(address[2]+'\\'+dev_poco[2])                                  #删除当前已存在的截图目录
        except Exception as e:
            print(e)
        try:
            os.system(r'md %s\%s\shenjia_screenshot'%(address[2],dev_poco[2]))          #在电脑创建保存截图的文件夹
            dev_poco[0].shell(r'mkdir /sdcard/shenjia_screenshot')                       #在手机创建保存截图的文件夹
            print('临时文件夹创建成功')
        except Exception as e:
            a=str(e)
            if "File exists" in a:
               print('文件夹已存在')
            else:
                raise (e)

        return dev_poco                                                          #[dev,poco,uuid]

class Airtest_run:
    def airtest_run(self,test_case_list,poco,dev,equipment_number,
                    app_packagename,address,
                    test_case_configuration_list,rootPath):                                     #获取开始和结束的用例编号并调用执行用例
        for test_case_configuration in test_case_configuration_list:
            if equipment_number==test_case_configuration[0]:                                    #test_case_configuration_list格式['b6254d85', [1, 10]]
                start_value=test_case_configuration[1][0]-1                                     #用例从第几条开始的值
                end_value=test_case_configuration[1][1]                                         #用例结束的值
                test_case=test_case_list[start_value:end_value]
                Run_tag='First_run'                                                             #首次运行标记
                test_result=Airtest_run().run_case(test_case,poco,dev,equipment_number,
                    app_packagename,address,
                    rootPath,Run_tag)
                return test_result
            else:
                print('运行结束或配置文件有多余的机型配置')



    def run_case(self,test_case,poco,dev,equipment_number,
                    app_packagename,address,
                    rootPath,Run_tag):
        test_result=[]                                                                          #测试结果列表
        for i in test_case:                                                                     #执行每条用例 i[0]为标题列表，i[1]为操作步骤列表
            title=i[0]                                                                          #取出用例标题列表
            print('开始执行:%s'%(title[0]))
            try:                                                                                #异常处理
                for j in i[1:]:                                                                 #执行用例的每一步操作，
                    airtest_function_test_case.Poco_test().run_case(j, poco,rootPath)           #调用用例执行方法，j为元素列表，pocp为驱动
                single_result=Data_processing().append_data(1,title,j)                          #获取单条用例结果，1为通过，title标题信息，j报告内所需用例信息
            except Exception as error:                                                          #捕获异常
                single_result=Data_processing().append_data(-1,title,j)                         #获取单条用例结果，-1为失败，title标题信息，j报告内所需用例信息
                screenshot_address=Screenshot().air_screenshot(title,address[2],dev,equipment_number,'First run')        #调用截图方法，传入标题、截图保存地址、设备标号（是一个列表）多个设备需单独处理
                single_result.append(screenshot_address)                                        #将截图地址放入单条结果列表（只有失败才会执行）
                print('用例%s执行异常'%(title[0]))
                print(error)
            else:
                print('用例%s执行成功'%(title[0]))

            test_result.append(single_result)                                                   #所有用例执行完毕，将所有单条结果列表放入总测试结果列表
            back_to_home.Back_to_home().back(poco,app_packagename)

        retry_list=Data_processing().result_screening(test_result,test_case)                    #获取测试失败的用例

        if retry_list!='null':
            retrying_results=[]
            for retry_data in retry_list:                                                           #重新运行测试失败的用例
                title=retry_data[0]                                                                 #取出用例标题列表
                print('重试失败用例:%s'%(title[0]))
                try:                                                                                #异常处理
                    for j in retry_data[1:]:                                                        #执行用例的每一步操作，
                        airtest_function_test_case.Poco_test().run_case(j, poco,rootPath)           #调用用例执行方法，j为元素列表，pocp为驱动
                    single_result=Data_processing().append_data(1,title,j)                          #获取单条用例结果，1为通过，title标题信息，j报告内所需用例信息
                except Exception as error:                                                          #捕获异常
                    single_result=Data_processing().append_data(-1,title,j)                         #获取单条用例结果，-1为失败，title标题信息，j报告内所需用例信息
                    screenshot_address=Screenshot().air_screenshot(title,address[2],dev,equipment_number,'retry run')        #调用截图方法，传入标题、截图保存地址、设备标号（是一个列表）多个设备需单独处理
                    single_result.append(screenshot_address)                                        #将截图地址放入单条结果列表（只有失败才会执行）
                    print('用例%s执行异常'%(title[0]))
                    print(error)
                else:
                    print('用例%s执行成功'%(title[0]))

                retrying_results.append(single_result)                                                   #所有用例执行完毕，将所有单条结果列表放入总测试结果列表
                back_to_home.Back_to_home().back(poco,app_packagename)
            test_result=Data_processing().results_summary(test_result,retrying_results)            #获取重试后的最终结果

        return test_result


class Appium_run:   #暂时废弃，太久没维护
    def appium_run(self,test_case,app_driver,other_information,app_packagename,address,number_of_devices,startime,test_case_configuration_list):
        test_result=[]                                                                          #测试结果列表
        for i in test_case:                                                                     #执行每条用例 i[0]为标题列表，i[1]为操作步骤列表
            title=i[0]                                                                          #取出用例标题列表
            try:                                                                                #异常处理
                for j in i[1:]:                                                                 #执行用例的每一步操作
                    appium_function_test_case.Appium_test().run_case(j, app_driver)             #调用用例执行方法，j为元素列表
                single_result=Data_processing().append_data(1,title,j)                          #获取单条用例结果，1为通过，title标题信息，j报告内所需用例信息
            except BaseException as error:                                                      #捕获异常
                single_result=Data_processing().append_data(-1,title,j)                         #获取单条用例结果，-1为失败，title标题信息，j报告内所需用例信息
                screenshot_address=Screenshot().app_screenshot(title,address[2])                #调用截图方法，传入标题、截图保存地址
                single_result.append(screenshot_address)                                        #将截图地址放入单条结果列表（只有失败才会执行）
                print('用例%s执行异常'%(title[0]))
            else:
                print('用例%s执行成功'%(title[0]))

            test_result.append(single_result)                                                   #所有用例执行完毕，将所有单条结果列表放入总测试结果列表

class Finishing_touches:
    def finishing_touches(self,test_result,startime,address,number_of_devices,equipment_number,rootPath,other_information):
        overtime=time.time()                                                                    #取出测试结束时间
        test_duration=format((overtime-startime)/60,'.1f')                                      #换算成分钟并取小数点后一位
        test_result=Report_generation().replace(test_result,address[1],test_duration,number_of_devices,equipment_number,rootPath)      #测试完毕调用报告生成方法，传入报告数据、报告存放地址
        Email().send_email(other_information[2],address[2],address[1],test_result)
