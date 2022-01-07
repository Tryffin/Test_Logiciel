
import requests, json

import time

url = 'http://20.91.130.117:80/http/message/' #URL链接
 
while True:
    str = input() #输入发送信息
    data = str 
    r = requests.post(url, data=json.dumps(data)) #  data转json,REST POST 发送数据
    time.sleep(1) # 睡眠1秒
