import socketserver,json
import subprocess

connLst = []

class Connector(object):
    def __init__(self,account,password,addrPort,conObj):
        self.account = account
        self.password = password
        self.addrPort = addrPort
        self.conObj = conObj

class MyServer(socketserver.BaseRequestHandler):

    def handle(self):
        print("got connection from",self.client_address)
        register = False
        while True:
            conn = self.request
            data = conn.recv(1024)
            if not data:
                continue
            dataobj = json.loads(data.decode('utf-8'))

            if type(dataobj) == list and not register:
                account = dataobj[0]
                password = dataobj[1]
                conObj = Connector(account,password,self.client_address,self.request)
                connLst.append(conObj)
                register = True
                continue
            print(connLst)

            if len(connLst) > 1 and type(dataobj) == dict:
                sendok = False
                for obj in connLst:
                    if dataobj['to'] == obj.account:
                        obj.conObj.sendall(data)
                        sendok = True
                if sendok == False:
                    print('no target valid!')
            else:
                conn.sendall('nobody recevied!'.encode('utf-8'))
                continue

if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1',8021),MyServer)
    print('waiting for connection...')
    server.serve_forever()