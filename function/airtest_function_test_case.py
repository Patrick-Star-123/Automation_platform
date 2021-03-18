import time
from airtest.core.api import *
from currency.data_processing import Data_processing
class Poco_test:


    def run_case(self,case,poco,rootPath):
        if case[5]=='':
            time_value=2
        else:
            time_value=eval(case[5])
        #判断1
        if case[1]=='点击':  #判断操作类型（动作）
            print(case[0])
            a=0
            time.sleep(time_value)
            for i in range(5):
                try:
                    eval(case[3])                   #还原poco代码并执行
                    break
                except:
                    print('重新寻找按钮:%s,%s'%(case[0],case[3]))
                    time.sleep(2)
                    a+=1
                    if a==5:
                        raise Exception('未找到元素')
        #判断2
        elif case[1]=='输入':
            print(case[0])
            a=0
            time.sleep(time_value)
            for i in range(5):
                try:
                    eval(case[3])                   #还原poco代码并执行
                    break
                except:
                    print('重新寻找输入框:%s,%s'%(case[0],case[3]))
                    time.sleep(2)
                    a+=1
                    if a==5:
                        raise Exception('未找到元素')

        elif case[1]=='输入随机数':
            random_number=Data_processing().random_value('1234567890',int(eval(case[4])))
            runnable_code=Data_processing().reorganize_strings(case[3],random_number)
            print(case[0])
            a=0
            time.sleep(time_value)
            for i in range(5):
                try:
                    eval(runnable_code)                   #还原poco代码并执行
                    break
                except:
                    print('重新寻找输入框:%s,%s'%(case[0],case[3]))
                    time.sleep(2)
                    a+=1
                    if a==5:
                        raise Exception('未找到元素')
        #判断3
        elif case[1]=='滑动':
            print(case[0])
            a=0
            time.sleep(time_value)
            for i in range(5):
                try:
                    eval(case[3])                   #还原poco代码并执行
                    break
                except:
                    print('重新寻找滑动元素:%s,%s'%(case[0],case[3]))
                    print(case[3])
                    time.sleep(2)
                    a+=1
                    if a==5:
                        raise Exception('未找到元素')
        #判断4
        elif case[1]=='坐标点击':
            print(case[0])
            time.sleep(time_value)
            xy=poco.get_screen_size()
            coordinate=eval(case[4])
            try:
                    width=xy[0]
                    height=xy[1]
                    x=coordinate[0]/width
                    y=coordinate[1]/height
                    poco.click([x,y])
                    print('坐标点击：',x,',',y)
            except:
                    width=xy[0]
                    height=xy[1]
                    x=coordinate[0]/width
                    y=coordinate[1]/height
                    print('坐标点击异常，坐标：',x,',',y)
                    raise Exception('坐标点击异常')
        #判断5
        elif case[1]=='截图点击':
            print(case[0])
            time.sleep(time_value)
            a=0
            for i in range(2):
                try:
                    touch(Template(r"%s\button_screenshot\%s"%(rootPath,case[3])))
                    break
                except:
                    print(r'图像识别异常,图片名称%s'%(case[3]))
                    a+=1
                    if a==2:
                        raise Exception('图像识别异常')
        #判断6
        elif case[1]=='截图滑动':
            print(case[0])
            time.sleep(time_value)
            if '\n' in case[4]:
                coordinate=case[4].split('\n')
            a=0
            for i in range(2):
                try:
                    swipe(Template(r"%s\button_screenshot\%s"%(rootPath,case[3]), record_pos=eval(coordinate[0]), resolution=eval(coordinate[1])), vector=eval(coordinate[2]))
                    break
                except:
                    print(r'图像识别异常,图片地址%s'%(case[3]))
                    a+=1
                    if a==2:
                        raise Exception('图像识别异常')
        #判断7
        elif case[1]=='按键点击':
            print(case[0])
            time.sleep(time_value)
            try:
                keyevent(case[3])
            except:
                    print('按键点击异常')
                    raise Exception('按键点击异常')
        #判断8
        elif case[1]=='断言':
            print(case[0])
            a=0
            for i in range(5):
                time.sleep(time_value)
                Assertion=eval(case[3])                   #还原poco代码并执行
                if Assertion==True:
                    break
                elif Assertion==False:
                    print('重新寻找断言元素:%s,%s'%(case[0],case[3]))
                    time.sleep(2)
                    a+=1
                    if a==5:
                        raise Exception('未找到元素')
        #判断9
        elif case[1]=='假断言':
            print(case[0])
            time.sleep(time_value)
            Assertion=eval(case[3])                   #还原poco代码并执行
            if Assertion==False:
                pass
            elif Assertion==True:
                print('出现异常元素')
                raise Exception('出现异常元素')
        else:
            raise Exception('动作填写错误')


