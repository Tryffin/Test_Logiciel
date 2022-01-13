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
    pass


@app.route('/ip', methods=['GET'])
def get_ip():
    """ TODO """
    pass

@app.route('/isconnected', methods=['GET'])
def connexion():
    """ TODO """
    pass

def message():
    """ TODO """
    pass

if __name__ == '__main__':
    pass