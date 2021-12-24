# coding=utf-8

import sys
import time
import json
import random
import unittest
import paramunittest    #解决unittest传参问题
from Retry import *
from MysqlUtil import *
from ExcelUtil import *
from HttpReqUtil import *
from PatternUtil import *
from HTMLTestRunner import HTMLTestRunner    #解决unittest问题




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


@Retry(max_n=2)
class auto_test(ParametrizedTestCase):
    # 测试用例模板
    def test(self):
        test_value = random.randint(1,10)
        value = self.param
        print(str(test_value) + '是否小于等于' + str(value))
        self.assertLessEqual(test_value, value)


if __name__ == '__main__':
    # 初始化
    list_testCaseData = []    #测试用例列表
    fileName = r"E:\workspace-python\app_testcase.xlsx"  # 测试报告excel文件路径
    # 获取测试用例数据列表
    list_testCaseData = [5, 5]
    # 定义报告路径地址
    path_scr = sys.path[0]
    now = time.strftime("%Y-%m-%d-%H %M %S", time.localtime(time.time()))
    report_path = path_scr + '\\' + 'report' + '\\' + now + '.html'
    # 执行用例
    with open(report_path, 'wb') as report:
        # 创建suit对象
        suit = unittest.TestSuite()
        # 添加用例+传参
        for i in range(0, len(list_testCaseData)):
            suit.addTest(ParametrizedTestCase.parametrize(auto_test, param=list_testCaseData[i]))
        # 加入报告打印信息
        # unittest.TextTestRunner(stream=report,verbosity=2).run(suit)   #常规报告
        runner = HTMLTestRunner(stream=report, title=u'测试报告', description=u'用例执行情况', verbosity=2)  # 优化报告
        # 执行用例
        runner.run(suit)