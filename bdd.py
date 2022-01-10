""" bdd.py
"""
import sqlite3
import os
from Crypto import Random  #pip3 install pycryptodome
from Crypto.PublicKey import RSA
import rsa


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
def add_user(db_path, name, password, ip, port):
    """ TODO """
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    keypair = RSA.generate(1024)
    pubkey = keypair.publickey()
    private_key_start_comment = '-----BEGIN RSA PRIVATE KEY-----'
    private_key_end_comment = '-----END RSA PRIVATE KEY-----'
    public_key_start_comment = '-----BEGIN PUBLIC KEY-----'
    public_key_end_comment = '-----END PUBLIC KEY-----'
    public_key_pem = pubkey.exportKey(format='PEM', passphrase=None, pkcs=1)
    public_key_final = str(public_key_pem.decode('ascii')).replace('\n','').replace(public_key_start_comment,'').replace(public_key_end_comment,'').replace(' ','')
    private_key_pem = keypair.exportKey(format='PEM', passphrase=None, pkcs=1)
    private_key_final = str(private_key_pem.decode('ascii')).replace('\n','').replace(private_key_start_comment,'').replace(private_key_end_comment,'').replace(' ','')
    sql = 'INSERT INTO User (name, password, ip, port, public_key, private_key) VALUES (?,?,?,?,?,?)'
    # cursor.execute(sql,(name, password, ip, port, str(rsa.publickey()), str(rsa)))
    cursor.execute(sql,(name, password, ip, port, public_key_final, private_key_final))
    connect.commit()

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
    return ip

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

# db_path = 'logiciel.db'
# delete_db(db_path)
# create_db(db_path)
# add_user(db_path, 'David','passw', '127.0.0.1', '90')
# add_user(db_path, 'Elan','passw', '127.0.0.1', '90')
# print(get_public_key(db_path, 'David')[0][0])
# print(get_public_key(db_path, 'Elan')[0][0])

# store_dest_public_key(db_path,'David', get_public_key(db_path, 'Elan'))
# connect = sqlite3.connect(db_path)
# cursor = connect.cursor()
# cursor.execute ('SELECT public_key_dest FROM User WHERE name = "David";')
# #cursor.execute ('SELECT port FROM User WHERE name = "{}";'.format('David'))
# print(cursor.fetchall()[0][0])
# #print(cursor.fetchall())