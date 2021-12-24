# coding=utf-8

import sys
import json
import requests
import traceback

"""
 * @ClassName:  HttpReqUtil   
 * @Description:python基于requests发送请求
 * @author: xingchunyu
 * @date:   xxxx年xx月xx日 上午/下午xx:xx:xx    
"""
class HttpReqUtil:

    def __init__(self):
        pass

    #发送get请求
    def sendGet(self, url, data):
        try:
            #初始化
            response = None   #响应值
            # 发送gett请求
            response = requests.get(url=url, params=data)
            #json类型响应值转换字符串类型
            if response.status_code == 200:
                response = response.json()
            else:
                response["message"] = "response error,status_code=" + str(response.status_code)
        except Exception as e:
            print(e.args)
            print(traceback.format_exc())
        finally:
            pass
        return response


    #发送post请求
    def sendPost(self, url, data, headers):
        try:
            #初始化
            response = None   #响应值
            #配置headers
            headers = self.httpReqConfig(data)
            #发送post请求
            response = requests.post(url, data=data, headers=headers)
            #json类型响应值转换字符串类型
            if response.status_code == 200:
                response = response.json()
            else:
                response["message"] = "response error,status_code=" + str(response.status_code)
        except Exception as e:
            print(e.args)
            print(traceback.format_exc())
        finally:
            pass
        return response


    #判断请求参数是否为json
    def isJsonString(self, param):
        try:
            #初始化
            isJsonString = True   #是否json字符串标识
            #json格式字符串转为json
            json.loads(param)
        except Exception as e:
            isJsonString = False
        finally:
            pass
        return isJsonString


    #http请求配置（headers）
    def httpReqConfig(self, param):
        try:
            #初始化
            headers = None   #headers
            #判断请求参数是否为json格式字符串，返回boolean类型
            isJsonString = self.isJsonString(param)
            #配置header
            if isJsonString:
                headers = {
                    "Content-Type": "application/json; charset=UTF-8",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"
                }
            else:
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"
                }
        except Exception as e:
            print(e.args)
            print(traceback.format_exc())
        finally:
            pass
        return headers



if __name__ == '__main__':

    url = r'http://10.1.6.1/admin-service/login.do'
    data = "userName=query01&userPassword=56389779689e8f3ddd533c1b05470bea"
    headers = HttpReqUtil().httpReqConfig(data)
    response = HttpReqUtil().sendPost(url, data, headers)
    print(response)
    print(response['success'])



