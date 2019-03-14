# import socket
# import json
# from webso
#
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #声明socket类型，同时生成socket 连接对象
#
# #client.connect(("192.168.1.103",9105))  #设定连接地址，端口
# client.connect(("47.89.34.238",9105))
# while True:
#     #msg = input (">>:").strip()
#     # client.send(msg.encode("utf-8"))   #发送信息，只能发送byter  类型
#     data = client.recv(1024)   #设定接收数据大小
#    # print("recv:",json.loads(data.decode()))
#     if data.strip() :
#         print("recv:",data.decode("utf-8"))
#
#
# client.close()


import time
import threading,multiprocessing
from ws4py.client.threadedclient import WebSocketClient


class DummyClient1(WebSocketClient):

    def opened(self):
        # while True:
        self.send("www.baidu.com")

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, m):
        print("1", m)
        ws1.connect()


class DummyClient(WebSocketClient,ws1=None):
    def __init__(self):
        self.ws1 = ws1

    def opened(self):
        # while True:
        self.send("www.baidu.com")

    def closed(self, code, reason=None):
        print( "Closed down", code, reason)

    def received_message(self, m):
        print ("1",m)
        self.ws1.connect()
        # ws1.run_forever()
        self.ws1.send(m)

ws1 =  DummyClient1('ws://127.0.0.1:9105', protocols=['chat'])

def run_socket_client():
    while True:
          try:
            ws = DummyClient('ws://47.89.34.238:9105',protocols=['chat'])
            #ws = DummyClient('ws://127.0.0.1:9105', protocols=['chat'])
            print("已联接上")
            ws.connect()
            ws.run_forever()

          except Exception as e:
            print("联接异常，得新联接")
            # ws.close()
          print("sleep 3 ")
          time.sleep(3)



#-----------------------------------------------------------------------------------------------

import time
from websocket_server import WebsocketServer
import multiprocessing,threading

# // 当新的客户端连接时会提示


# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    server.send_message_to_all("Hey all, a new client has joined us")
    i = 0
    while i < 5:
            server.send_message(client,"%s"%i)
            time.sleep(i)
            i += 1


# // 当旧的客户端离开

# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])

# // 接收客户端的信息。

# Called when a client sends a message
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200] + '..'
    print("Client(%d) said: %s" % (client['id'], message))
    server.send_message_to_all(message)
    server.send_message_to_all("1")
    print("1111111111")


def  run_server():
    try :
        PORT = 9107
        server = WebsocketServer(PORT, "0.0.0.0")
        server.set_fn_new_client(new_client)
        server.set_fn_client_left(client_left)
        server.set_fn_message_received(message_received)
        server.run_forever()
    except Exception as e:
        print("出错")


p1 = multiprocessing.Process(target=run_server())
p1.start()


print("我是最后的")


