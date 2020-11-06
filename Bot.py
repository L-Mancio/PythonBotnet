import os
import socket
import paramiko
from paramiko import BadHostKeyException, AuthenticationException, SSHException

class Bot(object):
    def __init__(self, uniquename, host_ip, username, password, port):
        self.uniquename = uniquename
        self.host_ip = host_ip
        self.username = username
        self.password = password
        self.port = int(port)
        self.connected = False
        self.type = "no type"
        self.botname = ""

        #don't connect here just initialize all needed variables
        if self.port == 22:
            print("initializing ssh bot for " + username)
            self.botname = uniquename + "ssh"
            self.type = "ssh"
            self.sshbot_client = paramiko.SSHClient()
        elif self.port >= 4444:
            print("initializing netcat bot for " + username)
            self.botname = uniquename + "netcat"
            self.type = "nc"

    def __str__(self):
        if not self.botname:
            return self.uniquename + " exists but of no specific type, are you sure this is your intended behavior?"
        else:
            return self.botname

    def __repr__(self):
        if not self.botname:
            return self.uniquename + "*"
        else:
            return self.botname

    def connect(self):
        if self.type == "ssh":
            self.SSHconnect()
        elif self.type == "nc":
            self.NCConnect()

    def disconnect(self):
        if self.type == "ssh":
            self.disconnectSSHbot()
        elif self.type == "nc":
            self.disconnectNCbot()

    def SSHconnect(self):
        if self.connected:
            print("Already Connected")
            return
        self.sshbot_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.sshbot_client.connect(self.host_ip, self.port, self.username, self.password)
            self.connected = True
            print(self.botname + " CONNECTED!")
        except (BadHostKeyException, AuthenticationException, SSHException, socket.error) as e:
            print("Connection Failuire")
            print("error type: " + str(e))

    def NCConnect(self):
        if self.connected:
            print("Already Connected")
            return
        try:
            # /k would remain on shell and not terminate
            print("starting NetCat Bot, it's a little buggy but hang on tight")
            os.chdir("C:/Users/lucam/Desktop/nc111nt_safe/")
            self.connected = True
            os.system("cmd /k nc -lvp" + str(self.port))

        except:
            print("Connection Failuire")
            raise

    def disconnectSSHbot(self):
        if not self.connected:
            print("Already Disconnected")
            return
        self.sshbot_client.close()
        self.connected = False
        print("SSH Bot Connection Closed by user")

    def disconnectNCbot(self):
        if not self.connected:
            print("Already Disconnected")
            return
        # ideally some command to stop
        self.connected = False
        print("NC Bot Connection Closed by user")
