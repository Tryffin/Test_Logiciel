'''
Client get IP
'''

import time
import requests

name = input()
PORT = "90"
SRVADR = "127.0.0.1"
SUBURL = "/ip"
FUN = '?name=' + name

URL = "http://" + SRVADR + ":" + PORT + SUBURL + FUN

r = requests.get(URL)
print(r.text)