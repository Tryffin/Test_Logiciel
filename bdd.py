""" bdd.py
"""
import sqlite3
import logging
import re
from Crypto.PublicKey import RSA

IP = '127.0.0.1'
PORT = 90

# for db itself
def create_db(db_path):
    """ TODO """
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()

    cursor.execute('CREATE TABLE User ( \
                [id] INTEGER PRIMARY KEY AUTOINCREMENT, \
                [name] TEXT UNIQUE NOT NULL, \
                [password] TEXT NOT NULL, \
                [port] TEXT NOT NULL,\
                [ip] TEXT NOT NULL,\
                [public_key] TEXT NOT NULL, \
                [public_key_dest] TEXT, \
                [private_key] TEXT NOT NULL, \
                [chat_dest] TEXT) \
                ')


def delete_db(db_path):
    """ TODO """
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    cursor.execute('DROP TABLE IF EXISTS User')


# for operations of server
def add_user(db_path, name, password, ip = IP, port = PORT):
    """ TODO """
    re = True
    if user_existed(db_path, name):
        logging.warning("user already existed")
        re = False
    elif not verify_name(name):
        logging.warning("user name wrong format")
        re = False
    elif not verify_password(password):
        logging.warning("user password wrong format")
        re = False
    else:
        connect = sqlite3.connect(db_path)
        cursor = connect.cursor()
        keypair = RSA.generate(1024)
        pubkey = keypair.publickey()
        private_key_start_comment = '-----BEGIN RSA PRIVATE KEY-----'
        private_key_end_comment = '-----END RSA PRIVATE KEY-----'
        public_key_start_comment = '-----BEGIN PUBLIC KEY-----'
        public_key_end_comment = '-----END PUBLIC KEY-----'
        public_key_pem = pubkey.exportKey(format='PEM', passphrase=None, pkcs=1)
        public_key_final = str(public_key_pem.decode('ascii')).replace('\n','') \
            .replace(public_key_start_comment,'').replace(public_key_end_comment,'').replace(' ','')
        private_key_pem = keypair.exportKey(format='PEM', passphrase=None, pkcs=1)
        private_key_final = str(private_key_pem.decode('ascii')).replace('\n','') \
            .replace(private_key_start_comment,'').replace(private_key_end_comment,'') \
            .replace(' ','')
        sql = 'INSERT INTO User (name, password, ip, port, public_key, private_key) \
            VALUES (?,?,?,?,?,?)'
        # cursor.execute(sql,(name, password, ip, port, str(rsa.publickey()), str(rsa)))
        cursor.execute(sql,(name, hash(password), ip, port, public_key_final, private_key_final))
        connect.commit()

    return re

def delete_user(db_path, name):
    """ TODO """
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    sql = 'DELETE FROM User WHERE name=?'
    cursor.execute(sql,(name,))
    connect.commit()

def get_user_ip(db_path, name):
    """ TODO """
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    sql = 'SELECT ip FROM User WHERE name=?'
    ip = cursor.execute(sql,(name,)).fetchall()
    connect.commit()
    if len(ip):
        return ip
    else:
        logging.warning("get_user_ip: user doesn't exist")
        return False

def get_user_port(db_path, name):
    """ TODO """
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    sql = 'SELECT port FROM User WHERE name=?'
    port = cursor.execute(sql,(name,)).fetchall()
    connect.commit()
    return port

def get_public_key(db_path, name):
    """ TODO """
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    sql = 'SELECT public_key FROM User WHERE name=?'
    public_key = cursor.execute(sql,(name,)).fetchall()
    connect.commit()

    return public_key

def store_dest_public_key(db_path, name, public_key_dest):
    """ TODO """
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    sql = 'UPDATE user SET public_key_dest=? WHERE name=?'
    cursor.execute(sql, (public_key_dest[0][0], name))
    connect.commit()
    return True

def user_existed(db_path, name):
    """ TODO """
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    sql = 'SELECT * FROM User WHERE name=?'
    data = cursor.execute(sql, (name, )).fetchall()
    connect.commit()
    if len(data):
        return True
    return False

def has_special_char(str):
    """ TODO """
    char_special = "~!@#$%^&*()_+-*/<>,.[]/"

    for i in char_special:
        if i in str:
            return True

    return False

def verify_name(name):
    """TODO"""
    if re.search(r'\d', name) :
        logging.warning("username should not contain number")
        return False

    if has_special_char(name) :
        logging.warning("username should not contain special letter")
        return False

    return True

def verify_password(user_pw):
    """ TODO"""
    if len(user_pw) < 8 :
        logging.warning("password lenth should > 8")
        return False

    if not any(x.isupper() for x in user_pw) :
        logging.warning("password should contain at least one upper letter")
        return False

    if not has_special_char(user_pw) :
        logging.warning("password should contain at least one special letter")
        return False

    if not re.search(r'\d', user_pw) :
        logging.warning("password should contain at least one number")
        return False

    return True

def log_in(db_path, name, pw):
    """ TODO """
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()

    #verifier le nom existe 
    cursor.execute("SELECT name FROM User WHERE name = ?", (name,))
    data=cursor.fetchall()
    if len(data)==0:
        print('There is no user named %s'%name)    
        return False

    #verifier les mots de passe corresponds a le nom 
    cursor.execute("SELECT password FROM User WHERE name = ?", (name,))
    data=cursor.fetchone()
    _pw = hash(pw)
    if str(data[0]) != str(_pw):
        print('password invalid')    
        return False
    else :
        print("log in successfully")
        return True