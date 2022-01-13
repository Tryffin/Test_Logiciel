import unittest
import shlex
import subprocess
import time
import os
import warnings 
import bdd

class TestClient(unittest.TestCase):
    SrvSubprocess = None
    CliSubprocess = None
    TestPort = "90"
    SrvAddr = "127.0.0.1"
    SrvUrl = "http://" + SrvAddr + ":" + TestPort

    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
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
      
    def test_01_AddUser(self):
        cmd = os.popen("python client.py adduser name Alice password Pass123!@#").read()
        self.assertEqual(cmd, 'Alice is added\n')
        
    def test_02_SendMessage(self):
        cmd = os.popen("python client.py send message hello").read()
        self.assertEqual(cmd, 'Your message: hello is sent\n')
        
    def test_03_getIP(self):
        os.system("python client.py adduser name Bob password Pass123!@#")
        cmd = os.popen("python client.py getip name Bob").read()
        self.assertEqual(cmd, "Bob's IP is: 127.0.0.1\n")

if __name__ == '__main__':
    unittest.main()