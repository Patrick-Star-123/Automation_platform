from airtest.core.api import *
import time
class Back_to_home:
    def back(self,poco,app_packagename):
        if poco(text="确认").exists()==True:
            poco(text="确认").click()
        elif poco(text="确定").exists()==True:
            poco(text="确定").click()
        elif poco(text="知道了").exists()==True:
            poco(text="知道了").click()
        elif poco(text="首页").exists()==True:
            poco(text="首页").click()
        x=0
        while True:
            x+=1
            try:
                poco("android.widget.LinearLayout").offspring("android:id/content").offspring("com.shenjia.serve:id/host_fragment").offspring("com.shenjia.serve:id/btnNav").offspring("工作台").child("com.shenjia.serve:id/icon").wait(5).click()
                print('已回到主页')
                break
            except Exception:
                keyevent('BACK')
                print('操作返回')
            if x==7:
                print('返回首页异常，重启APP')
                stop_app(app_packagename)
                start_app(app_packagename)
                print('已重启APP')
                time.sleep(7)
