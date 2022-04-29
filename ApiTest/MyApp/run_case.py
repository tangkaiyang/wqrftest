import json
import re
import unittest
import time

import requests

from A_WQRFhtmlRunner import HTMLTestRunner


class Test(unittest.TestCase):
    '测试类'

    def demo(self, step):
        time.sleep(3)
        print(step.api_url)
        # 提取所有请求数据
        api_method = step.api_method
        api_url = step.api_url
        api_host = step.api_host
        api_header = step.api_header
        api_body_method = step.api_body_method
        api_body = step.api_body
        get_path = step.get_path
        get_zz = step.get_zz
        assert_zz = step.assert_zz
        assert_qz = step.assert_qz
        assert_path = step.assert_path
        # 检查是否需要进行替换占位符的
        rlist_url = re.findall(r"##(.+?)##", api_url)
        for i in rlist_url:
            api_url = api_url.replace("##" + i + "##", eval(i))
        rlist_header = re.findall(r"##(.+?)##", api_header)
        for i in rlist_header:
            api_header = api_header.replace("##" + i + "##", eval(i))
        rlist_body = re.findall(r"##(.+?)##", api_body)
        for i in rlist_body:
            api_body = api_body.replace("##" + i + "##", eval(i))

        # 实际发送请求
        header = json.loads(api_header)  # 处理header
        # 拼接完整url
        if api_host[-1] == '/' and api_url[0] == '/':  # 都有/
            url = api_host[:-1] + api_url
        elif api_host[-1] != '/' and api_url[0] != '/':  # 都没有
            url = api_host + '/' + api_url
        else:
            url = api_host + api_url

        if api_body_method == 'none' or api_body_method == 'null':
            response = requests.request(api_method.upper(), url, headers=header, data={})

        elif api_body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(api_body):
                payload[i[0]] = i[1]
            response = requests.request(api_method.upper(), url, headers=header, data=payload, files=files)

        elif api_body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(api_body):
                payload[i[0]] = i[1]
            response = requests.request(api_method.upper(), url, headers=header, data=payload)

        else:
            if api_body_method == 'Text':
                header['Content-Type'] = 'text/plain'
            if api_body_method == 'JavaScript':
                header['Content-Type'] = 'application/javascript'
            if api_body_method == 'Json':
                header['Content-Type'] = 'application/json'
            if api_body_method == 'Html':
                header['Content-Type'] = 'text/html'
            if api_body_method == 'Xml':
                header['Content-Type'] = 'text/xml'
            response = requests.request(api_method.upper(), url, headers=header, data=api_body.encode('utf-8'))
        # 设置返回编码
        response.encoding = 'utf-8'
        res = response.text
        # 对返回值res进行提取:
        if get_path != '':  # 说明有设置
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
                exec('self.%s = value' % key)
        # 对返回值res进行断言:
        if get_zz != '':  # 说明有设置
            for i in get_zz.split('\n'):
                key = i.split('=')[0].rstrip()
                zz = i.split('=')[1].lstrip()
                value = re.findall(zz, res)[0]
                exec('self.%s = "%s"' % (key, value))


def make_defself(step):
    def tool(self):
        Test.demo(self, step)

    setattr(tool, "__doc__", u"%s" % step.name)
    return tool


def make_def(steps):
    for i in range(len(steps)):
        setattr(Test, 'test_' + str(steps[i].index).zfill(3), make_defself(steps[i]))


def run(Case_id, Case_name, steps):
    # print(steps)
    suit = unittest.makeSuite(Test)
    filename = 'MyApp/templates/Reports/%s.html' % Case_id
    with open(filename, 'wb') as fp:
        runner = HTMLTestRunner(fp, title='接口测试平台测试报告: %s' % Case_name, description='用例描述')
        runner.run(suit)


if __name__ == '__main__':
    run()
