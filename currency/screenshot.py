import os
from airtest.core.android import adb
class Screenshot:                   #截图发送到电脑

    def air_screenshot(self,title,screenshot_address,dev,equipment_number,retrying_label):
        if retrying_label=='First run':
            screenshot_name=title[0]                                                               #取出截图名称（用例编号）
        elif retrying_label=='retry run':
            screenshot_name='%s_retry'%(title[0])
        dev.shell(r'screencap /sdcard/shenjia_screenshot/%s.png'%(screenshot_name))                     #截图并放入新文件夹
        adb.ADB(equipment_number).pull(remote=r'/sdcard/shenjia_screenshot/%s.png'%(screenshot_name),local=r'%s\%s\shenjia_screenshot'%(screenshot_address,equipment_number)) #将截图存入PC
        dev.shell(r'rm /sdcard/shenjia_screenshot/%s.png'%(screenshot_name))                            #删除手机的截图
        screenshot_address=f'{screenshot_address}\{equipment_number}\shenjia_screenshot\{screenshot_name}.png'
        return screenshot_address

    def app_screenshot(self,title,screenshot_address,dev):              #在airtest下ADB有冲突无法使用故单独区分
        screenshot_name=f'{title[0]}'
        os.system(r'adb shell screencap \sdcard\shenjia_screenshot\%s.png'%(screenshot_name))   #截图放入新文件夹
        os.system(r'adb pull \sdcard/shenjia_screenshot %s'%(screenshot_address))               #将截图存入PC
        os.system(r'adb shell rm \sdcard/shenjia_screenshot\%s.png'%(screenshot_name))          #删除手机的截图
        screenshot_address=f'{screenshot_address}\{screenshot_name}.png'
        return screenshot_address



