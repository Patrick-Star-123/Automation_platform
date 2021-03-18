import time
import os
import shutil

class Report_generation():
                                                                        #读取模板信息
    def replace(self,data,report_address,test_duration,number_of_devices,equipment_number,rootPath):      #将测试结果替换进报告模板
        self.template_address='%s\\测试报告模板（勿删）.html'%(rootPath)
        shutil.copyfile(self.template_address,'%s\\%s_report.html'%(report_address,equipment_number))
        self.report_address='%s\\%s_report.html'%(report_address,equipment_number)
        with open(self.report_address, encoding='utf-8') as f:                                  #打开报告模板html文件
            self.html = f.read()
        through=0
        failure=0
        for i in data:                                                                          # 测试结果数据结构data=[['test1', '登陆', '登陆', '点击切换登陆方式',id, -1, 'D:\\work\\MobileErp\\report\\Error_screenshot\\test1.png']]
            if i[5]==1:
                through+=1                                                                      #i[5]==1则说明通过，通过数+1
            else:
                failure+=1                                                                      #否则失败数+1

        Failure_rate=failure/len(data)*100                                                      #计算失败率 失败数÷总数×100
        Failure_rate='%s'%(format(Failure_rate,'.1f')+'%')                                      #将失败率保留一位小数

        table = ''
        self.html = self.html.replace('&1&', 'v-3.5')                                           #替换模板中的版本号
        self.html = self.html.replace('&2&', str(len(data)))                                    #替换模板中的用例数
        self.html = self.html.replace('&3&', str(through))                                      #替换模板中的通过数
        self.html = self.html.replace('&4&', str(failure))                                      #替换模板中的失败数
        self.html = self.html.replace('&5&', Failure_rate)                                      #替换模板中的失败率
        self.html = self.html.replace('&6&', str(equipment_number))                             #替换模板中的设备编号
        self.html = self.html.replace('&7&', time.strftime('%x'))                               #替换模板中的测试时间（当前时间）
        self.html = self.html.replace('&8&', '%s分钟'%(test_duration))                           #替换模板中的测试时长
        for i in data:
            if i[5]==1:                                                                          #如果测试通过则将通过模板放入table变量
                table += """
                                    <div class="tr">
				                        <p>%s</span>
				                        <p>%s</span>
				                        <p>%s</span>
				                        <p>无</span>
				                        <p>通过</span>
				                        <p class="p5">通过</span>
				                        <p>%s</span>
				                        <p>无</span>
		                            </div>
                                   """%(i[0],i[1],i[2],i[4])
            else:                                                                               #测试失败替换失败的模板
                table += """
                                    <div class="tr">
				                        <p>%s</span>
				                        <p>%s</span>
				                        <p>%s</span>
				                        <p>%s</span>
				                        <p>通过</span>
				                        <p class="p6">失败</span>
				                        <p>%s</span>
				                        <p><a href=%s>查看图片</a></span>
		                            </div>
                                                   """%(i[0],i[1],i[2],i[3],i[4],i[6])
        self.html = self.html.replace('&tests&', table)                                         #用table变量替换模板预先准备好的'&tests&
        return [str(len(data)),through,failure,Failure_rate,equipment_number,time.strftime('%x'),test_duration]
        #[用例数，通过数，失败数，失败率，设备号，当前测试时间，测试时长]

    def __del__(self):
        with open(self.report_address, 'w', encoding='utf-8') as f:                             #保存
            f.write(self.html)


