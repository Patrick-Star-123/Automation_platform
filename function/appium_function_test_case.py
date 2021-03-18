

class Appium_test:

    def run_case(self,case,Driver):       #遍历用例选择对应的操作
        if case[1]=='点击':                              #判断操作类型（动作）
            Appium_test().click(case,Driver)                 #动作为点击 调用点击方法
        elif case[1]=='输入':
            Appium_test().sendkeys(case,Driver)              #动作为输入 调用输入方法
        else:
            raise Exception('动作填写错误')

    def click(self,case,Driver):          #点击方法
        if case[2]=='id':
            Driver.find_element_by_id(case[3]).click()                  #按钮数据类型为id的点击
        elif case[2]=='xpath':
            Driver.find_element_by_xpath(case[3]).click()               #按钮数据类型为xpath的点击
        else:
            raise Exception('按钮地址类型填写错误')

    def sendkeys(self,case,Driver):      #输入方法
        if case[2]=='id':
            Driver.find_element_by_id(case[3]).send_keys(str(case[4]))       #按钮数据类型为id的输入,输入的纯数字需转换为字符串
        elif case[2]=='xpath':
            Driver.find_element_by_xpath(case[3]).send_keys(case[4])    #按钮数据类型为xpath的输入
        else:
            raise Exception('按钮地址类型填写错误')