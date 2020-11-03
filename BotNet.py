import os
import sys
import paramiko
from paramiko import BadHostKeyException, AuthenticationException, SSHException
import socket
from collections import defaultdict


class BotNet(object):
    def __init__(self):
        self.botnet = defaultdict(list) #dictionary style dict[Bot name] = [botobject]

    @staticmethod
    def disconnect(bot):
        # disconnects any type of bot
        try:
            bot.disconnectSSHbot()
        except:
            print("can't disconnect ssh bot")
            raise

        '''disconnect all other bots here, 
           for now we only have an ssh bot so call that function only
        '''
    def removeallbotsof(self, botuniquename):
        for bottypes in self.botnet[botuniquename]:
            self.disconnect(bottypes)
            #self.botnet[botuniquename].clear() #delete bot entry in dictionary
            del self.botnet[botuniquename]

        print("Bot " + botuniquename + "deleted...")

    def removebotbytype(self, botuniquename, type):
        for bottypes in self.botnet[botuniquename]:
            #if bot of type "type" exists and is disconnected remove it
            if bottypes.type == type and not bottypes.connected:
                self.botnet[botuniquename].remove(botuniquename + type)
            else:
                print("Can't remove this bot since it is still connected, try using bot functions to disconnect it, then try again")

    def addbot(self, botuniquename, bot):
        self.botnet[botuniquename].add(bot)
        print("adding bot of type " + bot.type + " to " + botuniquename)


    def disconnectAllBots(self):
        for botuniquename, botlist in self.botnet.items():
            for bot in botlist:
                self.disconnect(bot)

    def deleteAllBots(self):
        self.disconnectAllBots()
        for botname in self.botnet.keys():
            del self.botnet[botname]
        print("All bots disconnected and deleted")

    def getConnectedBots(self):
        connected = {}
        for botuniquename, botlist in self.botnet.items():
            for bot in botlist:
                if bot.connected:
                    connected[bot.botname] = bot
        print("list of connected bots: " + str(connected.keys()))

    def getDisconnectedBots(self):
        connected = {}
        for botuniquename, botlist in self.botnet.items():
            for bot in botlist:
                if not bot.connected:
                    connected[bot.botname] = bot
        print("list of disconnected bots: " + str(connected.keys()))


class Bot(object):
    def __init__(self, uniquename, host_ip, username, password, port):
        self.uniquename = uniquename
        self.host_ip = host_ip
        self.username = username
        self.password = password
        self.port = port
        self.connected = False
        self.type = "no type"

        if port == 22:
            print("initializing ssh bot for " + username)
            self.botname = uniquename + "ssh"
            self.type = "ssh"
            self.sshbot_client = paramiko.SSHClient()


    def SSHconnect(self):
        self.sshbot_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.sshbot_client.connect(self.host_ip, self.port, self.username, self.password)
            self.connected = True
        except (BadHostKeyException, AuthenticationException, SSHException, socket.error) as e:
            print("Connection Failuire")
            print("error type: " + str(e))

    def disconnectSSHbot(self):
        self.sshbot_client.close()
        self.connected = False
        print("Bot Connection Closed by user")



class BotOperation(object):
    def __init__(self, botlist, host_ip, username, password, port):
        #build botnet
        self.botnet = BotNet()
        for botnames in botlist:
            new_bot = Bot(host_ip, username, password, port)

    def startBot(self):
        while True:
            userinput = input("Would you like to start ")





def main():
    botnet = BotNet()

    mininetBot = Bot("192.168.1.101", "mininet", "mininet", port=22)

    botnet.addBot(mininetBot.username, mininetBot)

    stdin, stdout, stderr = mininetBot.bot_client.exec_command("ls")

    print(stdout.readlines())


if __name__ == '__main__':
    main()


