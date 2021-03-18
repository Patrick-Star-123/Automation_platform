import time


class Acquisition_time:     #获取时间
    def current_time(self):       #当前时间
        data=time.localtime()                           #获取当前时间数据
        times=time.strftime('%Y-%m-%d %H:%M:%S', data)  #将时间格式化
        times=str(times)                                #将时间转化为字符串
        return times
