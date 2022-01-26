"""client.py
Usage:
 client.py adduser name <name> password <password>
 client.py send message <message>
 client.py getip name <name>
 client.py chat name <name> password <password>
 
Options:
 -h --help     Show this screen.
 -v --version    Show version.
"""
from asyncio.windows_events import NULL
from operator import truediv
import requests, json
import bdd
import logging
from docopt import docopt
from socket import *
import threading,sys,json,re

PORT = "90"
SRVADR = "127.0.0.1"
db_path = 'logiciel.db'
global userName
global tcpCliSock

HOST = '127.0.0.1' 
PORT1=8021
BUFSIZ = 1024
ADDR = (HOST,PORT1)

def send_message(mesg):
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

def add_user(name, password):
    """ TODO """
    SUBURL = "/add_user"
    URL = "http://" + SRVADR + ":" + PORT + SUBURL
    data = name + ' '+ password
    if(bdd.verify_name(name)== False or bdd.verify_password(password)== False):
        return logging.warning("Wrong format of username or password")
    r = requests.post(URL, data=json.dumps(data))
    if r.status_code == 500:
        print("Can't add this person in the database")
    else:
        print(name + " is added")
        return r

def require_ip(name):
    """ TODO """
    SUBURL = "/ip"
    FUNC = '?name=' + name
    URL = "http://" + SRVADR + ":" + PORT + SUBURL + FUNC
    r =  requests.get(URL)
    if r.status_code == 500:
        print("Can't find this person in the database")
    else:
        return print(name+"'s IP is: "+r.text)

def log_in(name, password):
    SUBURL = "/log_in"
    URL = "http://" + SRVADR + ":" + PORT + SUBURL
    data = name + ' '+ password
    r = requests.post(URL, data=json.dumps(data))
    if r.status_code == 500:
        print("Can't find this person in the database")
        return False
    else:
        print("log in successfully")
        return True

def verify(name, password):
    if not log_in(name, password):
        return False
    else:
        global userName
        userName = name
        return (name, password)
    
class inputdata(threading.Thread):
    def run(self):
        while True:
            sendto = input('to>>:')
            msg = input('msg>>:')
            dataObj = {'to':sendto,'msg':msg,'froms':userName}
            datastr = json.dumps(dataObj)
            tcpCliSock.send(datastr.encode('utf-8'))
            
class getdata(threading.Thread):
    def run(self):
        while True:
            data = tcpCliSock.recv(BUFSIZ)
            dataObj = json.loads(data.decode('utf-8'))
            print('{} -> {}'.format(dataObj['froms'],dataObj['msg']))
            

def chat(name, password):
    """ TODO """

    while True:
        if verify(name, password) != False:
            regInfo =  verify(name, password)
        else:
            sys.exit(0)
            
        if  regInfo:
            global tcpCliSock
            tcpCliSock = socket(AF_INET,SOCK_STREAM)
            tcpCliSock.connect(ADDR)

            datastr = json.dumps(regInfo)
            tcpCliSock.send(datastr.encode('utf-8'))
            break

    myinputd = inputdata()
    mygetdata = getdata()
    myinputd.start()
    mygetdata.start()
    myinputd.join()
    mygetdata.join()


if __name__ == '__main__':
    ARGS = docopt(__doc__, version="Client v1.0")
    #print(ARGS)
    if ARGS.get('adduser') == True:
        add_user(name=ARGS.get('<name>'), password= ARGS.get('<password>'))

    elif ARGS.get('send') == True:
        send_message(mesg=ARGS.get('<message>'))

    elif ARGS.get('getip') == True:
        require_ip(name=ARGS.get('<name>'))

    elif ARGS.get('chat') == True:
        chat(name=ARGS.get('<name>'), password=ARGS.get('<password>'))