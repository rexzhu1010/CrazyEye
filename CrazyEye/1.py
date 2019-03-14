# reimport time
import time
from websocket import create_connection

url = 'ws://47.89.34.238:9106/balance/86608118'
while True:  # 一直链接，直到连接上就退出循环
    time.sleep(2)
    try:
        ws = create_connection(url)
        print(ws)
        break
    except Exception as e:
        print('连接异常：', e)
        continue
while True:  # 连接上，退出第一个循环之后，此循环用于一直获取数据
    ws.send('{"event":"subscribe", "channel":"btc_usdt.ticker"}')
    response = ws.recv()
    print(response)
