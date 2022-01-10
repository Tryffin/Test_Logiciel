
import requests, json

import time

url = 'http://127.0.0.1/message'
 
while True:
    str = input()
    data = str 
    r = requests.post(url, data=json.dumps(data))
    time.sleep(1)


def connect():
    """ TODO """
    return False


def is_connected():
    """ TODO """
    return False


def disconnect():
    """ TODO """
    return False
