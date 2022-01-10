from sqlite3.dbapi2 import Cursor
import unittest, sys, sqlite3, os, random, string
import bdd

class testBDD(unittest.TestCase):

    def setUp(self):
        self.db_path = 'logiciel.db'
        self.connect = sqlite3.connect(self.db_path)
        self.cursor = self.connect.cursor()

    def test_01_create_bd(self):
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

        bdd.add_user(self.db_path,'Alice', 'password', '127.0.0.1', '90')
        sql = "SELECT name FROM User WHERE name = 'Alice';"
        user_name1 = self.cursor.execute(sql).fetchall()[0][0]
        self.assertEqual(user_name1,'Alice')

        bdd.add_user(self.db_path,'Bob', 'password', '127.0.0.1', '90')
        sql = "SELECT name FROM User WHERE name = 'Bob';"
        user_name2 = self.cursor.execute(sql).fetchall()[0][0]
        self.assertEqual(user_name2,'Bob')

        bdd.add_user(self.db_path,'Cecile', 'password', '127.0.0.1', '90')
        sql = "SELECT name FROM User WHERE name = 'Cecile';"
        user_name3 = self.cursor.execute(sql).fetchall()[0][0]
        self.assertEqual(user_name3,'Cecile')
        

    # def test_delete_user(self):
    #     bdd.delete_user(self.db_path, 'Cecile')
    #     sql = "SELECT name FROM User WHERE name = 'Cecile';"
    #     data = self.cursor.execute(sql).fetchall()
    #     self.assertIsNone(data)

    def test_03_get_user_ip(self):
        username = 'Alice'
        cur = self.cursor.execute ('SELECT ip FROM User WHERE name = "{}";'.format(username))
        self.assertEqual(bdd.get_user_ip(self.db_path, username), cur.fetchall())
        

    def test_04_get_user_port(self):
        username = 'Alice'
        cur = self.cursor.execute ('SELECT port FROM User WHERE name = "{}";'.format(username))
        self.assertEqual(bdd.get_user_port(self.db_path, username), cur.fetchall())
        
    def test_05_get_public_key(self):
        username = 'Alice'
        cur = self.cursor.execute ('SELECT public_key FROM User WHERE name = "{}";'.format(username))
        self.assertEqual(bdd.get_public_key(self.db_path, username), cur.fetchall())

    def test_06_store_dest_public_key(self):
        pub_key = bdd.get_public_key(self.db_path, 'Bob')[0][0]
        bdd.store_dest_public_key(self.db_path, 'Alice', bdd.get_public_key(self.db_path, 'Bob'))
        pub_key2 = self.cursor.execute ('SELECT public_key_dest FROM User WHERE name = "Alice";').fetchall()
        print(pub_key)
        print(pub_key2[0][0])
        self.assertEqual(pub_key, pub_key2[0][0])


if __name__ == '__main__':
    unittest.main()