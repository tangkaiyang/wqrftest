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
from MyApp.views_tools import *
from MyApp.views_test import *

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
    url(r'^add_case/(?P<eid>.*)/$', add_case),  # 增加用例
    url(r'^del_case/(?P<eid>.*)/(?P<oid>.*)/$', del_case),  # 删除用例
    url(r'^copy_case/(?P<eid>.*)/(?P<oid>.*)/$', copy_case),  # 复制用例用例

    url(r'^get_small/$', get_small),  # 获取小用例步骤的列表数据
    url(r'^add_new_step/$', add_new_step),  # 新增小步骤接口
    url(r'^delete_step/(?P<eid>.*)/$', delete_step),  # 删除小步骤接口
    url(r'^user_upload/$', user_upload),  # 上传头像
    url(r'^get_step/$', get_step),  # 获取小步骤
    url(r'^save_step/$', save_step),  # 保存小步骤
    url(r'^step_get_api/$', step_get_api),  # 步骤详情页获取接口数据
    url(r'^Run_Case/$', Run_case),  # 运行大用例
    url(r'^look_report/(?P<eid>.*)/$', look_report),  # 查看报告
    url(r'^save_project_header/$', save_project_header),  # 保存项目公共请求头
    url(r'^save_case_name/$', save_case_name),  # 保存用例名称
    url(r'^save_project_host/$', save_project_host),  # 保存项目公共域名
    url(r'^project_get_login/$', project_get_login),  # 获取项目登录态接口
    url(r'^project_login_save/$', project_login_save),  # 保存项目登录态接口
    url(r'^project_login_send/$', project_login_send),  # 调试请求登录态接口
    url(r'^Home_save_api/$', Home_save_api),  # 首页保存请求数据
    url(r'^search/$', search),  # 首页搜索功能

    url(r'^global_data/(?P<id>.*)/$', global_data),  # 进入全局变量
    url(r'^global_data_add/$', global_data_add),  # 新增全局变量
    url(r'^global_data_delete/$', global_data_delete),  # 删除全局变量
    url(r'^global_data_save/$', global_data_save),  # 保存全局变量
    url(r'^global_data_change_check/$', global_data_change_check),  # 更改项目的生效变量组

    # ------------------小工具-----------------
    url(r'^tools_zhengjiao/$', zhengjiao),  # 进入小工具页面
    url(r'^zhengjiao_play/$', zhengjiao_play),  # 正交工具运行
    url(r'^zhengjiao_excel/$', zhengjiao_excel),  # 正交工具导出

    # ------------ 测试用接口
    url(r'^test_login_A/$', test_login_A),  # 保存一个全局变量组
    url(r'^test_login_B/$', test_login_B),  # 保存一个全局变量组
    url(r'^test_api_A/$', test_api_A),  # 保存一个全局变量组
    url(r'^test_api_B/$', test_api_B),  # 保存一个全局变量组
]
