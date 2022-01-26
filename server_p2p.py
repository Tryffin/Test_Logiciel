import socketserver,json
import subprocess

connLst = []

class Connector(object):
    def __init__(self,account,password,addrPort,conObj):
        self.account = account
        self.password = password
        self.addrPort = addrPort
        self.conObj = conObj
