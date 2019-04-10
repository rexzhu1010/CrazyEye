import sys,os
import paramiko

t =  paramiko.Transport(("47.91.147.240",50022))
t.connect(username="root",password="ASastop2015")
sftp =  paramiko.SFTPClient.from_transport(t)
#sftp.put("D:/test.txt","/tmp/test.txt")
sftp.get("/tmp/test.txt","D:/test.txt")
t.close()

