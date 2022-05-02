import json

import requests
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
