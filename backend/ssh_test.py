# rex.zhu

import  paramiko

ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

ssh.connect('192.168.1.98',22,"root","123")
stdin,stdout,stderr = ssh.exec_command('ifconfig')
print(stdout.read().decode())

ssh.close()