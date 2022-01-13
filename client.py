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

if __name__ == '__main__':
    pass