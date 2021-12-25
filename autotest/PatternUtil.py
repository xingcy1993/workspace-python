# coding=utf-8

import re
import sys
import jsonpath
import traceback


"""
 * @ClassName: PatternUtil   
 * @Description:python解决《预期结果与实际结果比对》、《解决接口依赖问题》
 * @author: xingchunyu
 * @date:   xxxx年xx月xx日 上午/下午xx:xx:xx    
"""
class PatternUtil:

    def __init__(self):
        pass

    #预期结果与实际结果比对
    def compareResult(self, expResult, actResult):
        try:
            #初始化
            result = False   #返回值   False为比对不成功；True为比对成功
            list = []   #存储flag的列表
            pattern = r"([\$\.\w]+)=(\w+)"   #正则表达式-处理预期结果的值
            #对预期结果进行拆分，存入列表中
            list_expResult = expResult.split(';')
            #逐一结果比对
            for i in range(0,len(list_expResult)):
                if re.search(pattern, list_expResult[i]).group(2) == 'True':
                    value1 = True
                else:
                    value1 = re.search(pattern, list_expResult[i]).group(2)

                value2 = (re.search(pattern, list_expResult[i]).group(1))[0]
                if value1 == jsonpath.jsonpath(actResult, value2):
                    list.append(True)
                else:
                    list.append(False)
            #得到返回值
            if False not in list:
                result = True
        finally:
            pass
        return result


    #发送请求后-解决接口被依赖的处理
    def storeResponseValue(self, depKey, actResult, dict):
        try:
            #初始化
            pattern = r'([/\w\W]+):([\$\.\w]+)'   #正则表达式-解决接口被依赖的处理
            #对预期结果进行拆分，存入列表中
            list_depKey = depKey.split(';')
            for i in range(0, len(list_depKey)):
                if re.search(pattern, list_depKey[i]):
                    dict[re.search(pattern, list_depKey[i]).group()] = jsonpath.jsonpath(actResult, re.search(pattern, list_depKey[i]).group(2))[0]
        finally:
            pass
        return dict



    #发送请示前-依赖处理
    def handlerReqDataOfDep(self, reqData, dict):
        try:
            #初始化
            value = None    #依赖值
            pattern = r"(/[\w\W]+):([\$\\.\w]+)"    #正则表达式：发送请示前 - 依赖处理
            #对请求参数进行拆分，存入列表中
            list_depKey = reqData.split('&')
            for i in range(0, len(list_depKey)):
                if re.search(pattern, list_depKey[i]):
                    value = dict[re.search(pattern, reqData).group()]
                    reqData = reqData.replace(re.search(pattern, reqData).group(), value)
                else:
                    value = value
        finally:
            pass
        return reqData, dict




if __name__ == '__main__':
    pass
    """1.compareResult()方法
    actResult = {'success':'1',"ok":'2'}
    expResult = "$.success=1;$.ok=2"
    print PatternUtil().compareResult(expResult, actResult)
    """

    """2.compareResult()方法
    depKey = r'/admin-service/login.do:$.magicX'
    actResult = {"magicX":"357bae3047a814f3e5b312a1e81d66c6"}
    print PatternUtil().storeResponseValue(depKey, actResult)
    """

    #"""3.handlerReqDataOfDep()方法
    dict = {"/admin-service/login.do:$.magicX": "f086899619a0fe5be6247fdb2f8f290b"}
    reqData = r'magicX=/admin-service/login.do:$.magicX'
    rs = PatternUtil().handlerReqDataOfDep(reqData, dict)
    reqData = rs[0]
    dict = rs[1]
    print(reqData)
    #"""
