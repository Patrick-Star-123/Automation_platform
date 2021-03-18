import smtplib,zipfile,os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

class Email():
    def send_email(self,email_information,screenshot_address,report_address,test_result):
        #设置服务器所需信息
        mail_host = email_information[1]        #163邮箱服务器地址
        mail_user = email_information[2]        #163用户名
        mail_psw = email_information[3]         #密码(部分邮箱为授权码)
        sender = email_information[2]           #邮件发送方邮箱地址
        receivers = email_information[0]        #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发

        #设置email信息
        message = MIMEMultipart()               #邮件对象
        message['Subject'] = Header("移动ERP自动化测试报告", 'utf-8').encode()   #邮件主题
        message['From'] = sender                #信息发送方
        message['To'] = receivers[0]            #信息接受方
        #添加邮件正文
        number_of_cases=test_result[0]
        through=test_result[1]
        failure=test_result[2]
        Failure_rate=test_result[3]
        equipment_number=test_result[4]
        current_time=test_result[5]
        test_duration=test_result[6]
        message.attach(MIMEText('用例数：%s，'
                                '通过数：%s，'
                                '失败数：%s，'
                                '失败率：%s，'
                                '设备号：%s，'
                                '测试时间：%s，'
                                '测试用时：%s分钟'%(
            number_of_cases,through,failure,Failure_rate,equipment_number,current_time,test_duration), 'plain', 'utf-8'))
        #添加附件1
        att1 = MIMEText(open(r'%s\%s_report.html'%(report_address,equipment_number),'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1['Content-Disposition'] = 'attachment;filename="%s_report.html"'%(equipment_number)
        message.attach(att1)

        #添加附件2
        if failure!=0:
            screenshot_path=self.compressed_files(screenshot_address,equipment_number)
            if screenshot_path != 'null':
                att2 = MIMEText(open(screenshot_path,'rb').read(), 'base64', 'utf-8')
                att2["Content-Type"] = 'application/octet-stream'
                att2['Content-Disposition'] = 'attachment;filename="%s_screenshot.zip"'%(equipment_number)
                message.attach(att2)

        #登录并发送邮件
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host,25)               #连接到服务器
            smtpObj.login(mail_user,mail_psw)           #登录到服务器
            smtpObj.sendmail(
                sender,receivers,message.as_string())   #发送
            smtpObj.quit()                              #退出
            print('已向以下账户发送邮件：','\n','\n'.join(email_information[0]))
        except smtplib.SMTPException as e:
            print('邮件发送异常',e)                            #打印错误

    def compressed_files(self,screenshot_address,equipment_number):
        newfile=os.path.join(screenshot_address,equipment_number,equipment_number+'异常图片.zip')
        screenshot_path=os.path.join(screenshot_address,equipment_number,'shenjia_screenshot')
        #创建zip压缩文件（空文件），并生成对象
        dirpath='文件路径'
        dir__list=[]
        filename_list=[]
        for dirpath,dir__list,filename_list in os.walk(screenshot_path):
            dirpath=dirpath
            dir__list=dir__list
            filename_list=filename_list
        # 使用os.walk（）获取指定文件的路径名、文件夹内的所有文件夹列表，所有文件列表
        if len(filename_list)==0:
            print('未找到截图')
            return 'null'
        else:
            zipobj=zipfile.ZipFile(newfile,'w')
            for filename in filename_list:
            #遍历文件名列表取出文件名
                zipobj.write(dirpath+'\\'+filename,filename)
                #将文件逐一压缩，并对压缩文件重命名（可以避免压缩后的文件含根目录）
            zipobj.close()
            return newfile
