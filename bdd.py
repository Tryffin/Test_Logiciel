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
    pass


def delete_db(db_path):
    """ TODO """
    pass


# for operations of server
def add_user(db_path, name, password, ip, port):
    """ TODO """
    pass

def delete_user(db_path, name):
    """ TODO """
    pass

def get_user_ip(db_path, name):
    """ TODO """
    pass

def get_user_port(db_path, name):
    """ TODO """
    pass

def get_public_key(db_path, name):
    """ TODO """
    pass

def store_dest_public_key(db_path, name, public_key_dest):
    """ TODO """
    pass

