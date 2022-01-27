"""client.py
Usage:
 client.py adduser name <name> password <password>
 client.py send message <message>
 client.py getip name <name>
 client.py chat dname <dname> name <name> password <password>
 client.py sendkey from <name1> to <name2> 
 
Options:
 -h --help     Show this screen.
 -v --version    Show version.
"""
from asyncio.windows_events import NULL
from calendar import day_name
from operator import truediv
from socket import *
import threading,sys,json,re
import requests, json
from docopt import docopt
import bdd
import logging


PORT = "90"
SRVADR = "127.0.0.1"
db_path = 'logiciel.db'
global userName
global tcpCliSock
global dname
global myinputd
global mygetdata

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
    # if(bdd.verify_name(name)== False or bdd.verify_password(password)== False):
    #     return logging.warning("Wrong format of username or password")
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
        print("Can't find this person in the database or password invalid")
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
        # global dname
        print("Welcome to " + dname + " and " + userName + "'s chat room!")
        while True:
            # sendto = input('to>>:')
            msg = input('msg>>:')
            if msg == "exit":
                myinputd._delete()
                break
            elif msg == "":
                continue
            dataObj = {'to':dname,'msg':msg,'froms':userName}
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

    global mygetdata
    global myinputd
    myinputd = inputdata()
    mygetdata = getdata()
    myinputd.start()
    mygetdata.start()
    myinputd.join()
    mygetdata.join()


def sendkey(name1, name2):
    """ TODO """
    SUBURL = "/get_store_key"
    URL = "http://" + SRVADR + ":" + PORT + SUBURL
    data = str(name1) + ' '+ str(name2)
    r = requests.post(URL, data=json.dumps(data))

    if r.status_code == 500:
        print("Can't store this person's key")
        return False
    else:
        print("key is added")
        return True


if __name__ == '__main__':
    ARGS = docopt(__doc__, version="Client v1.0")

    #print(ARGS)
    if ARGS.get('adduser'):
        add_user(name=ARGS.get('<name>'), password= ARGS.get('<password>'))

    elif ARGS.get('send'):
        send_message(mesg=ARGS.get('<message>'))

    elif ARGS.get('getip'):
        require_ip(name=ARGS.get('<name>'))

    elif ARGS.get('chat'):
        dname=ARGS.get('<dname>')
        chat(name=ARGS.get('<name>'), password=ARGS.get('<password>'))
    
    elif ARGS.get('sendkey'):
        sendkey(name1=ARGS.get('<from>'), name2=ARGS.get('<to>'))