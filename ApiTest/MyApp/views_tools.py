import json
import os

import requests
import xlwt
from allpairspy import AllPairs
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from MyApp.models import *


# Create your views here.
# 获取公共参数
def glodict(request):
    userimg = str(request.user.id) + '.jpg'
    res = {"username": request.user.username, "userimg": userimg}
    return res


# 进入正交工具页面
def zhengjiao(request):
    return render(request, 'welcome.html', {"whichHTML": "zhengjiao.html", "oid": request.user.id, **glodict(request)})


# 正交工具运行
def zhengjiao_play(request):
    end_values = request.GET['end_values'].split(',')
    new_values = [i.split('/') for i in end_values]
    res = []
    for i in AllPairs(new_values):
        res.append(i)
    d = {"res": res}
    return HttpResponse(json.dumps(d), content_type='application/json')


# 正交工具导出
def zhengjiao_excel(request):
    end_keys = request.GET['end_keys'].split(',')
    end_values = request.GET['end_values'].split(',')
    new_values = [i.split('/') for i in end_values]
    res = []
    for i in AllPairs(new_values):
        res.append(i)
    # 先创建
    wqrf_book = xlwt.Workbook(encoding='utf-8') # 创建excel
    wqrf_sheet = wqrf_book.add_sheet("正交结果") # 创建sheet页
    for i in range(len(res)):
        case_index = '用例: ' + str(i+1) # 用例编号
        hb = list(zip(end_keys, res[i])) # 把key和value合并
        case = ','.join([':'.join(list(i)) for i in hb]) # 格式化
        wqrf_sheet.write(i,0,case_index) # 写入,i为行,0为第一例
        wqrf_sheet.write(i,1,case) # 写入,i为行,1为第二列
    wqrf_book.save('ApiTest/MyApp/static/tmp_zhengjiao.xls') # 保存
    print(os.getcwd())
    return HttpResponse('')
