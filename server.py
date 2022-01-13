from flask import Flask, request, jsonify, Response
import json
import sqlite3
import bdd

app = Flask(__name__)
db_path = 'logiciel.db'
IP = '127.0.0.1'
PORT = '90'

@app.route('/message', methods=['post'])
def handle_message():
    """ TODO """
    if not request.data:
        return ('fail')
    params = request.data.decode('utf-8')
    prams = json.loads(params)
    print(prams)
    return prams


@app.route('/add_user', methods=['post'])
def addUser():
    """ TODO """
    if not request.data:
        return ('fail')
    params = request.data.decode('utf-8')
    prams = json.loads(params)
    x = prams.split()
    name = x[0]
    password = x[1]
    print(name)
    print(password)
    if bdd.verify_name(name) == True and bdd.verify_password(password) == True:
        bdd.add_user(db_path, name, password, IP, PORT)
        print("User added") 
        return params
    else:
        print("Wrong format of username or password")     
        return params


@app.route('/ip', methods=['GET'])
def get_ip():
    """ TODO """
    name = request.args.get("name")
    return bdd.get_user_ip(db_path, name)[0][0]

@app.route('/isconnected', methods=['GET'])
def connexion():
    """ TODO """
    print("Client is connected")
    return Response(status=200)

def message():
    """ TODO """
    pass

if __name__ == '__main__':
    bdd.delete_db(db_path)
    bdd.create_db(db_path)
    app.run(host=IP, port=PORT)