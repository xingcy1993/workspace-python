# coding = utf-8

import sys
import pymysql
import traceback
import datetime



"""
 * @ClassName: MysqlUtil   
 * @Description:python基于pymysql操作mysql
 * @author: xingchunyu
 * @date:   xxxx年xx月xx日 上午/下午xx:xx:xx    
"""
class MysqlUtil:

    def __init__(self):
        pass

    #连接数据库。返回db对象
    def connect_mysql(self, host, user, password, database):
        try:
            #初始化
            db = None   #mysql数据库对象
            #连接mysql数据库
            db = pymysql.connect(host=host,
                                 user=user,
                                 password=password,
                                 database=database,
                                 charset='utf8')
        except Exception as e:
            print("mysql数据库连接失败")
            print(e.args)
            print(traceback.format_exc())
        finally:
            pass
        return db


    #数据库查询
    def query_mysql(self, host, user, password, database, sql):
        try:
            #初始化
            results = None
            #连接数据库
            db = self.connect_mysql(host,user,password,database)
            #使用cursor()方法获取操作游标
            cursor = db.cursor()
            #数据库查询
            try:
                cursor.execute(sql)   #执行SQL语句
                results = cursor.fetchall()   #获取查询结果列表
            except Exception as e:
                print("mysql数据库查询sql不成功")
                print(e.args)
                print(traceback.format_exc())
            #关闭数据库
            db.close()
        except Exception as e:
            print(e.args)
            print(traceback.format_exc())
        finally:
            pass
        return results


    #数据库更新操作
    def update_mysql(self, host, user, password, database, sql):
        try:
            #初始化
            results = None
            #连接数据库
            db = self.connect_mysql(host,user,password,database)
            #使用cursor()方法获取操作游标
            cursor = db.cursor()
            #数据库更新操作
            try:
                cursor.execute(sql)   #执行SQL语句
                db.commit()   #提交到数据库执行
            except Exception as e:
                db.rollback()
                print("mysql数据库更新不成功，发生错误进行回滚")
                print(e.args)
                print(traceback.format_exc())
            #关闭数据库
            db.close()
        except Exception as e:
            print(e.args)
            print(traceback.format_exc())
        finally:
            pass
        return results


    #接口自动化测试-执行结果落库
    def interface_test_updata(self, list_testResult):
        try:
            #初始化
            flag = False   #是否落库成功
            host = 'localhost'
            user = 'root'
            password = '123456'
            database = 'autotest'
            sql = "INSERT INTO interface(testCase,reqType,reqUrl,reqData,expResult,actResult,result,INSERT_TIME) VALUES('%s','%s','%s','%s','%s','%s','%s',(str_to_date('%s','%%Y-%%m-%%d %%H:%%i:%%S')))" % (
                list_testResult[0], list_testResult[1], list_testResult[2], list_testResult[3], list_testResult[4], list_testResult[5], list_testResult[6], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            #执行结果落库
            self.update_mysql(host, user, password, database, sql)
            flag = True
        except Exception as e:
            print(e.args)
            print(traceback.format_exc())
        finally:
            pass
        return flag


if __name__ == '__main__':
    list_testResult = ['1','http10161adminservicelogindo','2','2','2','2','2']
    MysqlUtil().interface_test_updata(list_testResult)





