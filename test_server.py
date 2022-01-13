import unittest
import requests
import shlex
import subprocess
import time
import json
import sqlite3
import bdd

class TestServer(unittest.TestCase):

	SrvSubprocess = None

	TestPort = "90"
	SrvAddr = "127.0.0.1"
	SrvUrl = "http://" + SrvAddr + ":" + TestPort

	def setUp(self):
		bdd.delete_db('logiciel.db')
		bdd.create_db('logiciel.db')
		cmd = "python server.py"	
		args = shlex.split(cmd)
		self.SrvSubprocess  = subprocess.Popen(args) # launch command as a subprocess
		time.sleep(3)

	def tearDown(self):
		print("Killing subprocess server")
		self.SrvSubprocess.kill()
		self.SrvSubprocess.wait()

	def test_01_launchSrv(self):
		response = requests.get(self.SrvUrl+'/isconnected')
		self.assertEqual(response.status_code, 200)
		
	def test_02_adduser(self):
		# verify response of server
		data = "Alice Pass123!@#"
		response = requests.post(url=self.SrvUrl+'/add_user', data=json.dumps(data))
		self.assertEqual(response.status_code, 200)

		# verify database
		connect = sqlite3.connect('logiciel.db')
		cursor = connect.cursor()
		sql = "SELECT name FROM User WHERE name = 'Alice';"
		user_name = cursor.execute(sql).fetchall()[0][0]
		self.assertEqual(user_name,'Alice')
  
	def test_03_handle_message(self):
		data = "hello"
		response = requests.post(url=self.SrvUrl+'/message', data=json.dumps(data))
		self.assertEqual(response.status_code, 200)	

  
	def test_04_get_ip(self):
		# verify response of server
		bdd.add_user('logiciel.db', 'Bob', 'Pass123!@#', '127.0.0.10', '90')
		name = "Bob"
		response = requests.get(url=self.SrvUrl+'/ip?name='+name)
		self.assertEqual(response.status_code, 200)
		
		# verify database
		connect = sqlite3.connect('logiciel.db')
		cur = connect.cursor()
		sql = "SELECT ip FROM User WHERE name = 'Bob';"
		ip = cur.execute(sql).fetchall()[0][0]
		self.assertEqual(ip, '127.0.0.10')
  
if __name__ == '__main__':
	unittest.main()
