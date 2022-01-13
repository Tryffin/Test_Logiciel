"""client.py
Usage:
 client.py adduser name <name> password <password>
 client.py send message <message>
 client.py getip name <name>
 
Options:
 -h --help     Show this screen.
 -v --version    Show version.
"""
import requests, json
import bdd
import logging
from docopt import docopt

def send_message():
    """ TODO """
    SUBURL = "/message"
    URL = "http://" + SRVADR + ":" + PORT + SUBURL
    data = mesg
    r = requests.post(URL, data=json.dumps(data))
    if r.status_code == 500:
        print("Can't send this message")
    else:
        print("Your message: "+mesg +" is sent")
        return r

def add_user():
    """ TODO """
    pass

def require_ip():
    """ TODO """
    pass

def disconnect():
    """ TODO """
    pass

if __name__ == '__main__':
    pass