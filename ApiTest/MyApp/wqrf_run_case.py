import json
import re
import unittest
import time

import requests

from A_WQRFhtmlRunner import HTMLTestRunner

import sys, os, django

path = '../ApiTest'
sys.path.append(path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ApiTest.settings")
django.setup()
from MyApp.models import *
from MyApp.views import global_datas_replace, encryption


def do_step(step_id, tmp_datas):
    '请求数据准备'
    ## 计算项目id
    step = DB_step.objects.filter(id=step_id)[0]
    # 拿到step
    project_id = DB_project.objects.filter(id=step.Case_id)[0].project_id
    # 初始化请求方式
    api_method = step.api_method
    # 初始化url
    api_url = step.api_url
    # url添加全局变量
    api_url = global_datas_replace(project_id, api_url)
    ## 取出证书开关
    api_cert = step.api_cert
    ## 初始化域名
    api_host = step.api_host
    ## 域名添加全局变量
    api_host = global_datas_replace(project_id, api_host)
    ## 请求体初始化
    api_body = step.api_body
    ## 请求体添加全局变量
    api_body = global_datas_replace(project_id, api_body)
    ## 请求方式初始化
    api_method = step.api_method
    ## 请求头初始化
    api_header = step.api_header
    ## 请求头添加全局变量
    if api_header == '':
        api_header = '{}'
    else:
        api_header = global_datas_replace(project_id, api_header)
    ## 返回值处理方式初始化
    get_path = step.get_path
    get_zz = step.get_zz
    assert_zz = step.assert_zz
    assert_qz = step.assert_qz
    assert_path = step.assert_path
    ## 公共请求头初始化
    ts_project_headers = step.public_header.split(',')  # 获取公共请求头
    ## Mock返回值初始化
    mock_res = step.mock_res
    ## 是否mock判断
    if mock_res not in ['', None, 'None']:
        res = mock_res
    ## 请求体类型初始化
    api_body_method = step.api_body_method

    ## 占位符变量替换
    # url 处理
    rlist_url = re.findall(r"##(.*?)##", api_url)
    for i in rlist_url:
        api_url = api_url.replace("##" + i + "##", str(eval(i)))

    # header 处理
    rlist_header = re.findall(r"##(.*?)##", api_header)
    for i in rlist_header:
        api_header = api_header.replace("##" + i + "##", repr(str(eval(i))))
    # 请求体 处理
    if api_body_method == 'none':
        pass
    elif api_body_method == 'form-data' or api_body_method == 'x-www-form-urlencoded':
        rlist_body = re.findall(r"##(.*?)##", api_body)
        for i in rlist_body:
            api_body = api_body.replace("##" + i + "##", str(eval(i)))

    elif api_body_method == 'Json':
        rlist_body = re.findall(r"##(.*?)##", api_body)
        for i in rlist_body:
            api_body = api_body.replace("##" + i + "##", repr(eval(i)))

    else:
        rlist_body = re.findall(r"##(.*?)##", api_body)
        for i in rlist_body:
            api_body = api_body.replace("##" + i + "##", str(eval(i)))
    ## 域名额外处理-全局域名
    if api_host[:4] == '全局域名':
        project_host_id = api_host.split('-')[1]
        api_host = DB_project_host.objects.filter(id=project_host_id)[0].host
    ## header转换为字段
    try:
        header = json.loads(api_header)  # 处理header
    except:
        header = eval(api_header)
    # 在这遍历公共请求头,并把其加入到header的字典中
    for i in ts_project_headers:
        if i == '':
            continue
        project_header = DB_project_header.objects.filter(id=i)[0]
        header[project_header.key] = project_header.value
    ## 最终url生成
    if api_host[-1] == '/' and api_url[0] == '/':
        url = api_host[:-1] + api_url
    elif api_host[-1] != '/' and api_url[0] != '/':
        url = api_host + '/' + api_url
    else:
        url = api_host + api_url
    ## 登录态融合
    api_login = step.api_login
    if api_login == 'no':
        login_res = {}
    else:
        Case_id = step.Case_id
        global login_res_list
        try:
            eval('login_res_list')
        except:
            login_res_list = []
        for i in login_res_list:
            if i['Case_id'] == Case_id:
                print('找到了')
                login_res = i
                break
        else:
            print('没找到要创建')
            from MyApp.views import project_login_send_for_other
            login_res = project_login_send_for_other(project_id)
            login_res['Caes_id'] = Case_id
            login_res_list.append(login_res)
        print(login_res)

    ## url插入
    if '?' not in url:
        url += '?'
        if type(login_res) == dict:
            for i in login_res.keys():
                url += i + '=' + login_res[i] + '&'
    else:
        if type(login_res) == dict:
            for i in login_res.keys():
                url += '&' + i + '=' + login_res[i]
    ## header插入
    if type(login_res) == dict:
        header.update(login_res)
    ## 加密策略
    step_encryption = step.sign
    if step_encryption == 'yes':
        url, api_body = encryption(url, api_body_method, api_body, project_id)
    ## 证书融合
    if api_cert == 'yes':
        cert_name = 'MyApp/static/Certs/%s' % DB_project.objects.filter(id=project_id)[0].cert
    else:
        cert_name = ''
    ## 数据库写入请求数据
    r_step = DB_wqrf_step_report.objects.get_or_create(id=step_id)
    r_step.request_data = json.dumps({
        'url': url,
        "method": api_method,
        "api_body": api_body,
        "api_body_method": api_body_method
    })
    r_step.save()

    '执行请求'


    ## none请求
    if api_body_method == 'none' or api_body_method == 'null':
        if type(login_res) == dict:
            response = requests.request(api_method.upper(), url, headers=header, data={}, cert=cert_name)
        else:
            response = login_res.request(api_method.upper(), url, headers=header, data={}, cert=cert_name)

    ## form-data请求
    elif api_body_method == 'form-data':
        files = []
        payload = ()
        for i in eval(api_body):
            payload += ((i[0], i[1]),)

        if type(login_res) == dict:
            for i in login_res.keys():
                payload += ((i, login_res[i]),)

            response = requests.request(api_method.upper(), url, headers=header, data=payload, files=files,
                                        cert=cert_name)
        else:
            response = login_res.request(api_method.upper(), url, headers=header, data=payload, files=files,
                                         cert=cert_name)

    ## x-www-form-urlencoded请求
    elif api_body_method == 'x-www-form-urlencoded':
        header['Content-Type'] = 'application/x-www-form-urlencoded'

        payload = ()
        for i in eval(api_body):
            payload += ((i[0], i[1]),)

        if type(login_res) == dict:
            for i in login_res.keys():
                payload += ((i, login_res[i]),)

        if type(login_res) == dict:
            response = requests.request(api_method.upper(), url, headers=header, data=payload, cert=cert_name)
        else:
            response = login_res.request(api_method.upper(), url, headers=header, data=payload, cert=cert_name)

    ## GraphQL请求
    elif api_body_method == 'GraphQL':
        header['Content-Type'] = 'application/json'
        query = api_body.split('*WQRF*')[0]
        graphql = api_body.split('*WQRF*')[1]
        try:
            eval(graphql)
        except:
            graphql = '{}'
        payload = '{"query":"%s","variables":%s}' % (query, graphql)
        if type(login_res) == dict:
            response = requests.request(api_method.upper(), url, headers=header, data=payload, cert=cert_name)
        else:
            response = login_res.request(api_method.upper(), url, headers=header, data=payload, cert=cert_name)

    ## raw的五种请求
    else:  # 这时肯定是raw的五个子选项：
        if api_body_method == 'Text':
            header['Content-Type'] = 'text/plain'

        if api_body_method == 'JavaScript':
            header['Content-Type'] = 'text/plain'

        if api_body_method == 'Json':
            api_body = json.loads(api_body)
            for i in login_res.keys():
                api_body[i] = login_res[i]
            api_body = json.dumps(api_body)
            header['Content-Type'] = 'text/plain'

        if api_body_method == 'Html':
            header['Content-Type'] = 'text/plain'

        if api_body_method == 'Xml':
            header['Content-Type'] = 'text/plain'
        if type(login_res) == dict:
            response = requests.request(api_method.upper(), url, headers=header, data=api_body.encode('utf-8'),
                                        cert=cert_name)
        else:
            response = login_res.request(api_method.upper(), url, headers=header, data=api_body.encode('utf-8'),
                                         cert=cert_name)
    response.encoding = "utf-8"
    res = response.text  # 最终结果文案

    '结果处理'
    # 新建临时变量列表
    tmp_d = {}
    ## 对返回res提取-路径法
    if get_path != '':
        for i in get_path.split('\n'):
            key = i.split('=')[0].rstrip()
            path = i.split('=')[1].lstrip()
            py_path = ""
            for j in path.split('/'):
                if j != '':
                    if j[0] != '[':
                        py_path += '["%s"]' % j
                    else:
                        py_path += j
            value = eval("%s%s" % (json.loads(res), py_path))
            tmp_d[key] = value
    ## 对返回res提取-正则法
    if get_zz != '': # 说明有设置
        for i in get_zz.split('\n'):
            key = i.split('=')[0].rstrip()
            zz = i.split('=')[1].lstrip()
            value = re.findall(zz, res)[0]
            tmp_d[key] = value
    ## 对返回值断言-路径法
    ## 对返回值断言-正则
    ## 对返回值断言-全值检测


def main_request(case_id):
    '入口主函数'
    tmp_datas = {}  # 临时变量列表
    steps = DB_step.objects.filter(case_id=case_id)
    for i in steps:
        tmp_d = do_step(i.id, tmp_datas)  # tmp_d为单步骤临时变量, 列表
        tmp_datas.update(tmp_d)
