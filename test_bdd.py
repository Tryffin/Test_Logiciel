'''Group4
    test_bdd.py
'''
#from sqlite3.dbapi2 import Cursor
import unittest
#import sys
import sqlite3
#import os
#import random
#import string
import bdd


class TestBDD(unittest.TestCase):
    """class of test"""


    def setUp(self):
        """test of setup"""
        self.db_path = 'logiciel.db'
        self.connect = sqlite3.connect(self.db_path)
        self.cursor = self.connect.cursor()


    def test_01_create_db(self):
        """test of create_db"""
        bdd.delete_db(self.db_path)
        bdd.create_db(self.db_path)
        sql = "SELECT name FROM sqlite_master WHERE type='table';"
        data = self.cursor.execute(sql).fetchall()
        self.assertIn(('User',), data)

    # def test_delete_bd(self):
    #     bdd.delete_db(self.db_path)
    #     sql = "SELECT name FROM sqlite_master WHERE type='table';"
    #     data = self.cursor.execute(sql).fetchall()
    #     self.assertNotIn(('User',), data)


    def test_02_add_user(self):
        """test of add_user"""

        self.assertEqual(bdd.add_user(self.db_path,'Alice', 'Password123!@#', \
         '127.0.0.1', '90'), True)
        sql = "SELECT name FROM User WHERE name = 'Alice';"
        user_name1 = self.cursor.execute(sql).fetchall()[0][0]
        self.assertEqual(user_name1,'Alice')

        self.assertEqual(bdd.add_user(self.db_path,'Bob', 'Password123!@#', \
         '127.0.0.1', '90'), True)
        sql = "SELECT name FROM User WHERE name = 'Bob';"
        user_name2 = self.cursor.execute(sql).fetchall()[0][0]
        self.assertEqual(user_name2,'Bob')

        self.assertEqual(bdd.add_user(self.db_path,'Cecile', 'Password123!@#',\
         '127.0.0.1', '90'), True)
        sql = "SELECT name FROM User WHERE name = 'Cecile';"
        user_name3 = self.cursor.execute(sql).fetchall()[0][0]
        self.assertEqual(user_name3,'Cecile')

        self.assertEqual(bdd.add_user(self.db_path,'Cecile', 'Password', '127.0.0.1', '90'), False)
        self.assertEqual(bdd.add_user(self.db_path,'Alex', 'pass', '127.0.0.1', '90'), False)
        self.assertEqual(bdd.add_user(self.db_path,'Cecile2', 'password', '127.0.0.1', '90'), False)

    # def test_delete_user(self):
    #     bdd.delete_user(self.db_path, 'Cecile')
    #     sql = "SELECT name FROM User WHERE name = 'Cecile';"
    #     data = self.cursor.execute(sql).fetchall()
    #     self.assertIsNone(data)

    def test_03_get_user_ip(self):
        """test of get_user_ip"""
        username = 'Alice'
        cur = self.cursor.execute ('SELECT ip FROM User WHERE name = "{}";'.format(username))
        self.assertEqual(bdd.get_user_ip(self.db_path, username), cur.fetchall())


    def test_04_get_user_port(self):
        """test of get_user_port"""
        username = 'Alice'
        cur = self.cursor.execute ('SELECT port FROM User WHERE name = "{}";'.format(username))
        self.assertEqual(bdd.get_user_port(self.db_path, username), cur.fetchall())


    def test_05_get_public_key(self):
        """test of get_public_key"""
        username = 'Alice'
        cur = self.cursor.execute ('SELECT public_key FROM User \
            WHERE name = "{}";'.format(username))
        self.assertEqual(bdd.get_public_key(self.db_path, username), cur.fetchall())


    def test_06_store_dest_public_key(self):
        """test of store_dest_public_key"""
        pub_key = bdd.get_public_key(self.db_path, 'Bob')[0][0]
        bdd.store_dest_public_key(self.db_path, 'Alice', bdd.get_public_key(self.db_path, 'Bob'))
        pub_key2 = self.cursor.execute ('SELECT public_key_dest FROM User \
            WHERE name = "Alice";').fetchall()
        # print(pub_key)
        # print(pub_key2[0][0])
        self.assertEqual(pub_key, pub_key2[0][0])

    def test_07_log_in(self):
        """test of log_in"""
        self.assertEqual(bdd.log_in(self.db_path, 'Celine','pw'), False)
        self.assertEqual(bdd.log_in(self.db_path, 'Cecile','pw'), False)
        self.assertEqual(bdd.log_in(self.db_path, 'Cecile','Password123!@#'), True)
        
if __name__ == '__main__':
    unittest.main()
