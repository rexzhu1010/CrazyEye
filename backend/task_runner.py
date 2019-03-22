# rex.zhu


import sys,os


import paramiko
from concurrent.futures import ThreadPoolExecutor

def ssh_cmd(sub_task_obj):
    print("在执行sub_cmd")
    host_to_user_obj = sub_task_obj.host_to_remote_user
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    try:
        ssh.connect(hostname=host_to_user_obj.host.ip_addr,
                    port=host_to_user_obj.host.port,
                    username=host_to_user_obj.remote_user.username,
                    password=host_to_user_obj.remote_user.password,
                    )
    except Exception as e:
        print(e)

    stdin,stdout,stderr = ssh.exec_command(task_obj.content)
    print("在执行sub_cmd3")
    stdout_res = stdout.read()
    stderr_res = stdout.read()

    #task_log_obj =  models.TaskLogDetail.objects.get(task=task_obj,host_to_remote_user_id=host_to_user_obj.id)
    result = stdout_res + stderr_res
    sub_task_obj.result =  result.decode()

    print("----------------result--------------- \r\n",sub_task_obj.result)
    if  stderr_res:
        sub_task_obj.status =2
    else:
        sub_task_obj.status=1

    sub_task_obj.save()
    ssh.close()



if __name__ == "__main__":
    base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(base_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CrazyEye.settings")
    import django
    django.setup()
    from web import  models
    import time
    #有以上三行，才能调用django数据库

    if len(sys.argv) == 1:
        exit("task id not provided!")
    task_id =  sys.argv[1]
    task_obj = models.Task.objects.get(id=task_id)

    #time.sleep(15)
    # task_obj.content="task test"
    # task_obj.save()
    # print("我在执行 task_runner")
    #
    pool =  ThreadPoolExecutor(max_workers=10)
    for sub_task_obj in task_obj.tasklogdetail_set.all():
        pool.submit(ssh_cmd,(sub_task_obj))

    #ssh_cmd(task_obj.tasklogdetail_set.first())






