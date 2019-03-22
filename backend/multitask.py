# rex.zhu
import json
from web import models
import subprocess
from django import  conf

class MultiTaskManager(object):
    def __init__(self,request):
        self.request = request
        self.run_task()


    def run_task(self):
            """调用任务"""

            self.task_parser()


    def task_parser(self):
        """解析任务"""
        print("解析任务")
        self.task_data=json.loads(self.request.POST.get("task_data"))
        print("解析任务",self.task_data)
        task_type = self.task_data.get("task_type")
        if hasattr(self,task_type):
            task_fun=getattr(self,task_type)
            task_fun()
        pass

    def run_task(self):
        """调用任务"""
        self.task_parser()
        pass


    def cmd(self):
        """批量命令
        1.生成任务，保存到数据库中，拿到任务ID
        2.触发任务，不阻塞
        3.返回任务ID 给前端
        """
        print("cmd 方法")
        print("running cmd  commands")

        #大任务
        task_obj = models.Task.objects.create(
            task_type = 'cmd',
            content = self.task_data.get("cmd"),
            user= self.request.user
        )

        selected_host_ids= set(self.task_data["selected_hosts"])

        task_log_objs=[]
        for id in selected_host_ids:
            task_log_objs.append(
            models.TaskLogDetail(task=task_obj,host_to_remote_user_id=id,result="init...")
            )

        #把上面的对象列表放进来，批量写入娄据库
        models.TaskLogDetail.objects.bulk_create(task_log_objs)

        task_script = "python %s/backend/task_runner.py %s"%(conf.settings.BASE_DIR,task_obj.id)

        print("执行subprocess")
        subprocess.Popen(task_script,shell=True)

        self.task_id = task_obj.id




