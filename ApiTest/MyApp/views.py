import json

import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from MyApp.models import *


# Create your views here.
@login_required()
def welcome(request):
    print('进来了!!')
    # return HttpResponse('进来了!!!')
    return render(request, "welcome.html")


def case_list(request):
    return render(request, "case_list.html")


@login_required
def home(request, log_id=''):
    print(request.user.id)
    return render(request, 'welcome.html', {"whichHTML": "home.html", "oid": request.user.id, "ooid": log_id})


def child(request, eid, oid, ooid):
    print(eid)
    res = child_json(eid, oid, ooid)
    return render(request, eid, res)


# 控制不同的也没返回不同的数据:数据分发器
def child_json(eid, oid="", ooid=""):
    res = {}
    if eid == "home.html":
        date = DB_home_href.objects.all()
        home_log = DB_apis_log.objects.filter(user_id=oid)[::-1]
        if ooid == '':
            res = {"hrefs": date, "home_log": home_log}
        else:
            log = DB_apis_log.objects.filter(id=ooid)[0]
            res = {"hrefs": date, "home_log": home_log, "log": log}
    if eid == "project_list.html":
        date = DB_project.objects.all()
        res = {"projects": date}
    if eid == "P_apis.html":
        print(DB_project.objects.all())
        print(oid)
        print(DB_project.objects.filter(id=oid))
        project = DB_project.objects.filter(id=oid)[0]
        apis = DB_apis.objects.filter(project_id=oid)
        res = {"project": project, "apis": apis}
    if eid == "P_cases.html":
        project = DB_project.objects.filter(id=oid)[0]
        res = {"project": project}
    if eid == "P_project_set.html":
        project = DB_project.objects.filter(id=oid)[0]
        res = {"project": project}

    return res


def login(request):
    return render(request, "login.html")


# 开始登录
def login_action(request):
    u_name = request.GET['username']
    p_word = request.GET['password']

    from django.contrib import auth
    user = auth.authenticate(username=u_name, password=p_word)

    if user is not None:
        auth.login(request, user)
        request.session['user'] = u_name
        return HttpResponse('成功')
    else:
        return HttpResponse('失败')


# 注册
def register_action(request):
    u_name = request.GET['username']
    p_word = request.GET['password']

    from django.contrib.auth.models import User
    try:
        user = User.objects.create_user(username=u_name, password=p_word)
        user.save()
        return HttpResponse("注册成功!")
    except:
        return HttpResponse("注册失败~用户名已存在")


# 推出登录
def logout(request):
    from django.contrib import auth
    auth.logout(request)
    return HttpResponseRedirect('/login/')


def pei(request):
    tucao_text = request.GET['tucao_text']

    DB_tucao.objects.create(user=request.user.username, text=tucao_text)
    return HttpResponse('')


def api_help(request):
    return render(request, 'welcome.html', {"whichHTML": "help.html", "oid": ""})


def project_list(request):
    return render(request, 'welcome.html', {'whichHTML': "project_list.html", "oid": ""})


# 删除项目
def delete_project(request):
    id = request.GET['id']
    DB_project.objects.filter(id=id).delete()
    DB_apis.objects.filter(project_id=id).delete()
    return HttpResponse('')


def add_project(request):
    project_name = request.GET['project_name']
    DB_project.objects.create(name=project_name, remark='', user=request.user.username, other_user='')
    return HttpResponse('')


def open_apis(request, id):
    project_id = id
    return render(request, 'welcome.html', {"whichHTML": "P_apis.html", "oid": project_id})


def open_cases(request, id):
    project_id = id
    return render(request, 'welcome.html', {"whichHTML": "P_cases.html", "oid": project_id})


def open_project_set(request, id):
    project_id = id
    return render(request, 'welcome.html', {"whichHTML": "P_project_set.html", "oid": project_id})


def save_project_set(request, id):
    project_id = id
    name = request.GET['name']
    remark = request.GET['remark']
    other_user = request.GET['other_user']
    DB_project.objects.filter(id=project_id).update(name=name, remark=remark, other_user=other_user)

    return HttpResponse('')


# 新增接口
def project_api_add(request, Pid):
    project_id = Pid
    DB_apis.objects.create(project_id=project_id, body_method='none')
    return HttpResponseRedirect('/apis/%s/' % project_id)


# 删除接口
def project_api_del(request, id):
    project_id = DB_apis.objects.filter(id=id)[0].project_id
    DB_apis.objects.filter(id=id).delete()
    return HttpResponseRedirect('/apis/%s/' % project_id)


# 保存备注
def save_bz(request):
    api_id = request.GET['api_id']
    bz_value = request.GET['bz_value']
    DB_apis.objects.filter(id=api_id).update(des=bz_value)
    return HttpResponse('')


# 备注详情
def get_bz(request):
    api_id = request.GET['api_id']
    bz_value = DB_apis.objects.filter(id=api_id)[0].des
    return HttpResponse(bz_value)


# 保存接口
def Api_save(request):
    # 提取所有数据
    api_name = request.GET['api_name']
    api_id = request.GET['api_id']
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    ts_body_method = request.GET['ts_body_method']
    # ts_api_body = request.GET['ts_api_body']
    if ts_body_method == '返回体':
        api = DB_apis.objects.filter(id=api_id)[0]
        ts_body_method = api.last_body_method
        ts_api_body = api.last_body
    else:
        ts_api_body = request.GET['ts_api_body']
    # 保存数据
    DB_apis.objects.filter(id=api_id).update(
        name=api_name,
        api_method=ts_method,
        api_url=ts_url,
        api_header=ts_header,
        api_host=ts_host,
        body_method=ts_body_method,
        api_body=ts_api_body
    )
    # 返回
    return HttpResponse('success')


# 获取接口内容
def get_api_data(request):
    api_id = request.GET['api_id']
    api = DB_apis.objects.filter(id=api_id).values()[0]
    return HttpResponse(json.dumps(api), content_type="application/json")


# 调试层发送请求
def Api_send(request):
    # 提取所有数据
    api_id = request.GET['api_id']
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    ts_api_body = request.GET['ts_api_body']
    api_name = request.GET['api_name']
    ts_body_method = request.GET['ts_body_method']
    print(ts_body_method)
    if ts_body_method == '返回体':
        api = DB_apis.objects.filter(id=api_id)[0]
        ts_body_method = api.last_body_method
        ts_api_body = api.last_api_body

        if ts_body_method in ['', None]:
            return HttpResponse('请先选择好请求体编码格式和请求体,再点击send按钮发送请求!')
    else:
        ts_api_body = request.GET['ts_api_body']
        api = DB_apis.objects.filter(id=api_id)
        api.update(last_body_method=ts_body_method, last_api_body=ts_api_body)

    # 发送请求获取返回值
    try:
        header = json.loads(ts_header)  # 处理header
    except:
        return HttpResponse('请求头不符合json格式')
    # 写入到数据库请求记录表中
    DB_apis_log.objects.create(user_id=request.user.id,
                               api_method=ts_method,
                               api_url=ts_url,
                               api_header=ts_header,
                               api_host=ts_host,
                               body_method=ts_body_method,
                               api_body=ts_api_body, )
    # 拼接完整url
    if ts_host and ts_host[-1] == '/':
        ts_host = ts_host[:-1]
    if ts_url and ts_url[0] != '/':
        ts_url = '/' + ts_url
    url = ts_host + ts_url
    try:
        if ts_body_method == 'none':
            response = requests.request(ts_method.upper(), url, headers=header, data={})
        elif ts_body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(ts_api_body):
                payload[i[0]] = i[1]
            response = requests.request(ts_method.upper(), url, headers=header, data=payload, files=files)
        elif ts_body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(ts_api_body):
                payload[i[0]] = i[1]
            response = requests.request(ts_method.upper(), url, headers=header, data=payload)
        else:
            if ts_body_method == 'Text':
                header['Content-Type'] = 'text/plain'
            if ts_body_method == 'JavaScript':
                header['Content-Type'] = 'application/javascript'
            if ts_body_method == 'Json':
                header['Content-Type'] = 'application/json'
            if ts_body_method == 'Html':
                header['Content-Type'] = 'text/html'
            if ts_body_method == 'Xml':
                header['Content-Type'] = 'text/xml'
            response = requests.request(ts_method.upper(), url, headers=header, data=ts_api_body.encode('utf-8'))
        # 设置返回编码
        response.encoding = 'utf-8'
        # 把返回值传递给前端
        return HttpResponse(response.text)
    except Exception as e:
        return HttpResponse(str(e))


# 复制接口
def copy_api(request):
    api_id = request.GET['api_id']
    old_api = DB_apis.objects.filter(id=api_id)[0]
    DB_apis.objects.create(
        project_id=old_api.project_id,
        name=old_api.name + '_copy',
        api_method=old_api.api_method,
        api_url=old_api.api_url,
        api_header=old_api.api_header,
        api_login=old_api.api_login,
        api_host=old_api.api_host,
        des=old_api.des,
        body_method=old_api.body_method,
        api_body=old_api.api_body,
        result=old_api.result,
        sign=old_api.sign,
        file_key=old_api.file_key,
        file_name=old_api.file_name,
        public_header=old_api.public_header,
        last_api_body=old_api.last_api_body,
        last_body_method=old_api.last_body_method,
    )
    return HttpResponse('')


# 异常值发送请求
def error_request(request):
    api_id = request.GET['api_id']
    new_body = request.GET['new_body']
    span_text = request.GET['span_text']
    api = DB_apis.objects.filter(id=api_id)[0]
    method = api.api_method
    url = api.api_url
    host = api.api_host
    header = api.api_header
    body_method = api.body_method
    header = json.loads(header)
    try:
        header = json.loads(header)
    except:
        return HttpResponse('请求头不符合json格式! ')
    if host[-1] == '/' and url[0] == '/':
        url = host[:-1] + url
    elif host[-1] != '/' and url[0] != '/':
        url = host + '/' + url
    else:
        url = host + url
    try:
        if body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(new_body):
                payload[i[0]] = i[1]
            response = requests.request(method.upper(), url, headers=header, data=payload, files=files)
        elif body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(new_body):
                payload[i[0]] = i[1]
            response = requests.request(method.upper(), url, headers=header, data=payload)
        elif body_method == 'Json':
            header['Content-Type'] = 'text/plain'
            response = requests.request(method.upper(), url, headers=header, data=new_body.encode('utf-8'))
        else:
            return HttpResponse('非法的请求体类型')
        # 把返回值传递给前端页面
        response.encoding = 'utf-8'
        res_json = {"response": response.text, "span_text": span_text}
        return HttpResponse(json.dumps(res_json), content_type='application/json')
    except:
        res_json = {"response": '对不起,接口未通', "span_text": span_text}
        return HttpResponse(json.dumps(res_json), content_type='application/json')


# 首页发送请求
def Api_send_home(request):
    # 提取所有数据
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    ts_body_method = request.GET['ts_body_method']
    ts_api_body = request.GET['ts_api_body']
    # 发送请求获取返回值
    try:
        header = json.loads(ts_header)  # 处理header
    except:
        return HttpResponse('请求头不符合json格式！')
    # 写入到数据库请求记录表中
    DB_apis_log.objects.create(
        user_id=request.user.id,
        api_method=ts_method,
        api_url=ts_url,
        api_header=ts_header,
        api_host=ts_host,
        body_method=ts_body_method,
        api_body=ts_api_body,
    )
    # 拼接完整url
    if ts_host[-1] == '/' and ts_url[0] == '/':  # 都有/
        url = ts_host[:-1] + ts_url
    elif ts_host[-1] != '/' and ts_url[0] != '/':  # 都没有/
        url = ts_host + '/' + ts_url
    else:  # 肯定有一个有/
        url = ts_host + ts_url
    try:
        if ts_body_method == 'none':
            response = requests.request(ts_method.upper(), url, headers=header, data={})

        elif ts_body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(ts_api_body):
                payload[i[0]] = i[1]
            response = requests.request(ts_method.upper(), url, headers=header, data=payload, files=files)

        elif ts_body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(ts_api_body):
                payload[i[0]] = i[1]
            response = requests.request(ts_method.upper(), url, headers=header, data=payload)

        else:  # 这时肯定是raw的五个子选项：
            if ts_body_method == 'Text':
                header['Content-Type'] = 'text/plain'

            if ts_body_method == 'JavaScript':
                header['Content-Type'] = 'text/plain'

            if ts_body_method == 'Json':
                header['Content-Type'] = 'text/plain'

            if ts_body_method == 'Html':
                header['Content-Type'] = 'text/plain'

            if ts_body_method == 'Xml':
                header['Content-Type'] = 'text/plain'
            response = requests.request(ts_method.upper(), url, headers=header, data=ts_api_body.encode('utf-8'))

        # 把返回值传递给前端页面
        response.encoding = "utf-8"
        return HttpResponse(response.text)
    except Exception as e:
        return HttpResponse(str(e))


# 首页获取请求记录
def get_home_log(request):
    user_id = request.user.id
    all_logs = DB_apis_log.objects.filter(user_id=user_id)
    ret = {"all_logs": list(all_logs.values("id", "api_method", "api_host", "api_url"))[::-1]}
    return HttpResponse(json.dumps(ret), content_type='application/json')


# 获取完整的单一的请求记录数据
def get_api_log_home(request):
    log_id = request.GET['log_id']
    log = DB_apis_log.objects.filter(id=log_id)
    ret = {"log": list(log.values())[0]}
    # print(ret)
    return HttpResponse(json.dumps(ret), content_type='application/json')
