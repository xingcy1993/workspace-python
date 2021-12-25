# coding=utf-8

import sys
import time
import json
import unittest
import paramunittest    #解决unittest传参问题
from Retry import *   #测试用例失败重试（报告去重）
from ExcelUtil import *
from MysqlUtil import *
from PatternUtil import *
from HttpReqUtil import *
from HTMLTestRunner import HTMLTestRunner    #解决unittest问题


#初始化
dict = {}  # 存储所有接口依赖的key、value


"""
 * @ClassName:  ParametrizedTestCase   
 * @Description:解决unittest传参问题
 * @author: xingchunyu
 * @date:   xxxx年xx月xx日 上午/下午xx:xx:xx    
"""
class ParametrizedTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param
        # self.param2 = param2

    @staticmethod
    def parametrize(testcase_klass, param=None):
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite


"""
 * @ClassName: auto_test   
 * @Description:unittest执行测试用例功能
 * @author: xingchunyu
 * @date:   xxxx年xx月xx日 上午/下午xx:xx:xx    
"""
@Retry(max_n=3)
class auto_test(ParametrizedTestCase):
    # 测试用例模板
    def test(self):
        #初始化
        actResult = None   #实际结果
        list_testResult = []   #测试执行结果列表
        #初始化-测试用例数据
        id = self.param[0][0]   #用例id
        isExec = self.param[0][1]   #用例是否执行。执行：YES，不执行：NO
        testCase = self.param[0][2]   #用例名称
        reqType = self.param[0][3]   #请求类型。POST/GET
        reqHost = self.param[0][4]   #请求host
        reqInterface = self.param[0][5]   #请求接口
        reqData = self.param[0][6]   #请求参数
        expResult = self.param[0][7]   #预期结果
        isDep = self.param[0][8]   #接口是否被依赖
        depKey = self.param[0][9]   #依赖值内容
        dict = self.param[1]
        #初始化-url、headers
        reqUrl = reqHost + reqInterface   #请求url
        headers = HttpReqUtil().httpReqConfig(reqData)   #请求headers

        #打印报告中
        print("\n用例编号:" + id)
        print("用例名称:" + testCase)
        print("请求接口:" + reqUrl)
        print("接口预期值:" + expResult)
        print("请求参数_处理前:" + reqData)

        """发送请示前-依赖处理"""
        rs = PatternUtil().handlerReqDataOfDep(reqData, dict)
        reqData = rs[0]
        dict = rs[1]
        print("请求参数_处理后:" + reqData)

        """发送请求"""
        if isExec == 'YES':
            if reqType == 'GET':
                actResult = HttpReqUtil().sendGet()
            elif reqType == 'POST':
                actResult = HttpReqUtil().sendPost(reqUrl, reqData, headers)
            print("接口实际值:" + json.dumps(actResult))
        else:
            pass
        """发送请求后-解决接口被依赖的处理"""
        if isDep == 'YES':
            dict = PatternUtil().storeResponseValue(depKey, actResult, dict)

        """预期值与实际值对比"""
        result = PatternUtil().compareResult(expResult, actResult)

        """测试结果存储到mysql"""
        #组装测试执行结果
        list_testResult.append(testCase)
        list_testResult.append(reqType)
        list_testResult.append(reqUrl)
        list_testResult.append(reqData)
        list_testResult.append(expResult)
        list_testResult.append(json.dumps(actResult))
        list_testResult.append(result)
        #存储到mysql中，返回是否落库成功
        success_flag = MysqlUtil().interface_test_updata(list_testResult)
        if success_flag:
            print("落库是否成功:成功")
        else:
            print("落库是否成功:未成功")

if __name__ == '__main__':
    # 初始化
    list_testCaseData = []    #测试用例列表
    if 'win' in sys.platform:
        fileName = r"E:\workspace-python\app_testcase.xlsx"  # 测试报告excel文件路径
    else:
        fileName = r'/data/git/workspace-python/app_testcase.xlsx'
    # 获取测试用例数据列表
    excelutil = ExcelUtil(fileName)
    list_testCaseData = excelutil.ExcelUtil_read(fileName)
    # 定义报告路径地址
    path_scr = sys.path[0]
    now = time.strftime("%Y-%m-%d-%H %M %S", time.localtime(time.time()))
    if 'win' in sys.platform:
        report_path = path_scr + '\\' + 'report' + '\\' + now + '.html'
    else:
        report_path = '/data/git/report' + '//' + now + '.html'
    print(report_path)
    # 执行用例
    with open(report_path, 'wb') as report:
        # 创建suit对象
        suit = unittest.TestSuite()
        # 添加用例+传参
        for i in range(0, len(list_testCaseData)):
            param = []   #初始化传参列表
            #判断：测试用例数据列表中-isExec用例是否执行字段。YES时执行用例
            if list_testCaseData[i][1] == 'YES':
                param.append(list_testCaseData[i])   #执行用例-传参列表追加测试用例数据
                param.append(dict)    #执行用例-传参列表param追加dict(存储依赖的key、value)
                suit.addTest(ParametrizedTestCase.parametrize(auto_test, param=param))
        # 加入报告打印信息
        # unittest.TextTestRunner(stream=report,verbosity=2).run(suit)   #常规报告
        runner = HTMLTestRunner(stream=report, title=u'测试报告', description=u'用例执行情况', verbosity=2)  # 优化报告
        # 执行用例
        runner.run(suit)