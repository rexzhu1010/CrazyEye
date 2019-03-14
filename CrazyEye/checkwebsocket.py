import time, socket
from websocket_server import WebsocketServer
import multiprocessing, threading
from ws4py.client.threadedclient import WebSocketClient


# // 当新的客户端连接时会提示

# 定义websocket client 类
class connect_local(WebSocketClient):
    # 新连接成功时执行
    def opened(self):
        # while True:
        self.send("www.baidu.com")

    # 连接关闭时执行
    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    # 收到数据时执行
    def received_message(self, m):
        print("ws2", m)


# Called for every client connecting (after handshake)
# 定义 连接自己的websocket-server
# 尝试连接，不成功等3秒，再新建连接，用递归方法，失败后调用自己
# 成功连接后，return 连接
def run_local_websocket():
    try:
        ws2 = connect_local('ws://127.0.0.1:9109', protocols=['chat'])
        ws2.connect()
        while True:
            data = ws2.recv(1024)
            if data.strip() != "":
                print(data.decode().strip("\r\n"))

    except Exception as e:
        print(e)
        ws2 = connect_local('ws://127.0.0.1:9109', protocols=['chat'])
        ws2.connect()
        print("run_local_websocket", e, "2222222222222222")
        time.sleep(3)



run_local_websocket()