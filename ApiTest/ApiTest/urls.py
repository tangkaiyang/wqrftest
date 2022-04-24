"""ApiTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from MyApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^welcome/$', welcome),
    url(r'^case_list/$', case_list),
    url(r'^home/$', home),
    url(r"^child/(?P<eid>.+)/(?P<oid>.*)/(?P<ooid>.*)/$", child),  # 返回子页面
    url(r'^login/$', login),
    url(r'^login_action/$', login_action),
    url(r'^register_action/$', register_action),
    url(r'^accounts/login/$', login),
    url(r'^logout/$', logout),
    url(r'^pei/$', pei),
    url(r'^help/$', api_help),
    url(r'^project_list/$', project_list),
    url(r'^delete_project/$', delete_project),
    url(r'^add_project/$', add_project),
    url(r'^apis/(?P<id>.*)/$', open_apis),
    url(r'^cases/(?P<id>.*)/$', open_cases),
    url(r'^project_set/(?P<id>.*)/$', open_project_set),  # 进入项目设置
    url(r'^save_project_set/(?P<id>.*)/$', save_project_set),  # 保存项目设置
    url(r'^project_api_add/(?P<Pid>.*)/$', project_api_add),  # 新增接口
    url(r'^project_api_del/(?P<id>.*)/$', project_api_del),  # 删除接口
    url(r'^save_bz/$', save_bz),  # 保存备注
    url(r'^get_bz/$', get_bz),
    url(r'^Api_save/$', Api_save),  # 保存接口
    url(r'^get_api_data/$', get_api_data),  # 展示接口内容
    url(r'^Api_send/$', Api_send),  # 发送请求
    url(r'^copy_api/$', copy_api),  # 复制接口
    url(r'^error_request/$', error_request),  # 调用异常测试接口
    url(r'^Api_send_home/$', Api_send_home),  # 首页发送请求
    url(r'^get_home_log/$', get_home_log),  # 获取最新请求记录
    url(r'^get_api_log_home/$', get_api_log_home),  # 获取完整的单一的请求记录数据
    url(r'^home_log/(?P<log_id>.*)/$', home),  # 再次进入首页,带上请求记录
]
