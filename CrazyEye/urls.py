"""CrazyEye URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from web import  views
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r"^$",views.dashboard,name="dashboard"),
    url(r"^web_ssh/*$",views.web_ssh,name="web_ssh"),
    url(r"login/*$",views.login_acc,name="login_acc"),
    url(r"logout/*$",views.logout_acc,name="logout_acc"),
    url(r"^host_mgr/*$",views.host_mgr,name="host_mgr"),
    url(r"^batch_task_mgr/*$",views.batch_task_mgr,name="batch_task_mgr"),


]
