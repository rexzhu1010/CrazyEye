# rex.zhu


import paramiko
import sys,os
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
                    timeout=3,
                    )

        stdin,stdout,stderr = ssh.exec_command(task_obj.content)
        print("在执行sub_cmd3")
        stdout_res = stdout.read()
        stderr_res = stderr.read()

        result = stdout_res + stderr_res
        sub_task_obj.result = result.decode()

        print("----------------result--------------- \r\n", sub_task_obj.result)
        if stderr_res:
            sub_task_obj.status = 2
        else:
            sub_task_obj.status = 1

    except Exception as e:
        print(e)
        sub_task_obj.status = 2
        sub_task_obj.result = e


    # task_log_obj =  models.TaskLogDetail.objects.get(task=task_obj,host_to_remote_user_id=host_to_user_obj.id)


    sub_task_obj.save()
    ssh.close()


def file_transfer(sub_task_obj,task_data):

    print("在执行file_transfer222222222222222222222222222222222")
    host_to_user_obj = sub_task_obj.host_to_remote_user
    print("我在这里111111111111111111111")
    try:


        t = paramiko.Transport((host_to_user_obj.host.ip_addr,host_to_user_obj.host.port))
        t.connect(username=host_to_user_obj.remote_user.username, password=host_to_user_obj.remote_user.password)
        sftp = paramiko.SFTPClient.from_transport(t)


        if task_data['file_transfer_type'] == 'send':
            sftp.put(task_data["local_file_path"], task_data['remote_file_path'])
            result = "file [%s] send to [%s] succeed!" % (task_data["local_file_path"],task_data['remote_file_path'])

        if task_data['file_transfer_type'] == 'get':
            from django import conf
            local_file_path =  "%s/%s"%(conf.settings.DOWNLOAD_DIR,sub_task_obj.task.id)
            if not os.path.exists(local_file_path):
                os.makedirs(local_file_path)
            filename =  task_data['remote_file_path'].split("/")[-1]
            sftp.get(task_data['remote_file_path'],"%s/%s%s"%(local_file_path,host_to_user_obj.host.ip_addr,filename) )
            result = "download remote file [%s] succeed!"%(task_data['remote_file_path'])

        t.close()
        sub_task_obj.status =1
        sub_task_obj.result= result
    except Exception as e:
        sub_task_obj.status = 2
        sub_task_obj.result = e

    sub_task_obj.save()




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

    pool = ThreadPoolExecutor(max_workers=10)
    if task_obj.task_type == "cmd":
        for sub_task_obj in task_obj.tasklogdetail_set.all():
            pool.submit(ssh_cmd,(sub_task_obj))

    if task_obj.task_type == "file_transfer":
        import json
        task_data =  json.loads(task_obj.content)
        for sub_task_obj in task_obj.tasklogdetail_set.all():
            pool.submit(file_transfer,sub_task_obj,task_data)

    #ssh_cmd(task_obj.tasklogdetail_set.first())






