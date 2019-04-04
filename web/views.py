from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import json

from backend.multitask import MultiTaskManager
from web import  models


# Create your views here.


def dashboard(request):

    return render(request,'index.html')


def web_ssh(request):

    return render(request,'web_ssh.html')


def login_acc(request):

    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user = authenticate(username=username,password=password)
        if user :
            login(request,user)
            next_url = request.GET.get("next", "/")  # 获取上一页路径，如没有就是/
            return redirect(next_url)
        else:
            error = "Wrong username or password!"


    return render(request,"login.html",{"error_msg":error})

def logout_acc(request):
    logout(request)
    return redirect("login/")


def host_mgr(request):
    return render(request,"host_mgr.html")


def batch_task_mgr(request):

    print(request.POST)
    task_data = json.loads(request.POST.get('task_data'))
    print(task_data)
    task_obj = MultiTaskManager(request)

    response = {
        'task_id':task_obj.task_obj.id,
        "selected_hosts":list(task_obj.task_obj.tasklogdetail_set.all().values("id","host_to_remote_user__host__name","host_to_remote_user__host__ip_addr","host_to_remote_user__remote_user__username"))

    }

    return  HttpResponse(json.dumps(response))


def get_task_result(request):
    task_id = request.GET.get("task_id")

    sub_tasklog_objs = models.TaskLogDetail.objects.filter(task_id=task_id)

    log_data =  list(sub_tasklog_objs.values("id",'status','result'))

    return HttpResponse(json.dumps(log_data))



def file_transfer(request):

    return render(request,"file_transfer.html")





