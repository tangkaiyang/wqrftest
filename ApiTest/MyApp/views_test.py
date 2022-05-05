import json

import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from MyApp.models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from MyApp.global_def import *


def test_login_A(request):
    res = {"userid": "uA"}
    return HttpResponse(json.dumps(res), content_type='application/json')


def test_login_B(request):
    res = {"userid": "uB"}
    return HttpResponse(json.dumps(res), content_type='application/json')


def test_api_A(request):
    res = {"errcode": "0"}
    return HttpResponse(json.dumps(res), content_type='application/json')


def test_api_B(request):
    res = {"errcode": "0"}
    return HttpResponse(json.dumps(res), content_type='application/json')
