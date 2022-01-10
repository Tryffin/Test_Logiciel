from flask import Flask, request, jsonify
from flask import Flask
import json

app = Flask(__name__)

@app.route('/message', methods=['post'])
def post_http():
    if not request.data:
        return ('fail')
    params = request.data.decode('utf-8')
    prams = json.loads(params)
    print(prams)
    return prams

def connexion():
    """ TODO """
    return False

def message():
    """ TODO """
    return False

# def add_room():
#     """ TODO """
#     return False

def add_user():
    """ TODO """
    return False

def handle_message():
    """ TODO """
    return False

def join():
    """ user join a room """
    return False

def quit():
    """ user quit a room """
    return False


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80)