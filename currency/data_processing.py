import random

class Data_processing:
    def remove_data(self,data):  #剔除空元素
        while data[-1]=='':
            del(data[-1])
        return data
    def append_data(self,sign,title,j):      #将测试结果数据添加进列表
        single_result=[]
        single_result.append(title[0])                                                  #将编号放入单条结果列表
        single_result.append(title[1])                                                  #将模块放入单条结果列表
        single_result.append(title[2])                                                  #将标题放入单条结果列表
        single_result.append(j[0])                                                      #将错误步骤放入单条结果列表
        single_result.append(j[2])                                                      #将错误按钮类型放入单次结果列表（如id、xpath）
        single_result.append(sign)                                                      #将测试结果标记放入单条结果列表
        return single_result                                                            #返回单条结果列表[用例编号，模块名，标题名，错误步骤，错误按钮类型，测试结果]

    def random_value(self,str,length):
        value=''.join(random.sample(str,length))                               #从指定字符串中提取指定数量字符生成一个新的字符串
        return value

    def reorganize_strings(self,str,random_number):
        a=[str.split("'")[0],"'",random_number,"'",str.split("'")[2]]
        value=''.join(a)
        return value

    def result_screening(self,test_result,test_case):               #结果筛选，取出测试失败的用例数据
        test_failure_list=[]
        for i in test_result:
            if i[5]==-1:
                test_failure_list.append(i)
        if len(test_failure_list)>0:
            retry_list=[]
            for failure_data in test_failure_list:
                for case_data in test_case:
                    if failure_data[0]==case_data[0][0]:
                        retry_list.append(case_data)
            return retry_list                                           #返回需要重新测试的用例数据
        else:
            return 'null'
    def results_summary(self,first_results,retrying_results):       #结果统计，将重试过的测试结果数据第一次的数据做对比，将重试后的结果替换到最终的结果列表中
        for retry_data in retrying_results:
            for first_data in first_results:
                if first_data[0]==retry_data[0]:
                    index=first_results.index(first_data)
                    first_results[index]=retry_data
        return first_results                                        #返回最后重试过的结果列表