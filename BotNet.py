import os
import sys
import paramiko
from paramiko import BadHostKeyException, AuthenticationException, SSHException
import socket
from collections import defaultdict


class BotNet(object):
    def __init__(self):
        self.botnet = defaultdict(list)  # dictionary style dict[Bot name] = [botobject]

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
            # self.botnet[botuniquename].clear() #delete bot entry in dictionary
            del self.botnet[botuniquename]

        print("Bot " + botuniquename + "deleted...")

    def removebotbytype(self, botuniquename, type):
        for bottypes in self.botnet[botuniquename]:
            # if bot of type "type" exists and is disconnected remove it
            if bottypes.type == type and not bottypes.connected:
                self.botnet[botuniquename].remove(botuniquename + type)
            else:
                print(
                    "Can't remove this bot since it is still connected, try using bot functions to disconnect it, then try again")

    def addbot(self, bot):
        for bots in self.botnet[bot.uniquename]:
            if bot.botname == bots.botname:
                print("can't create bot, already here")
                return False
        self.botnet[bot.uniquename].append(bot)
        return True

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

    # implement get all disconnected and connected bots of uniquebot


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

        # don't connect here just initialize all needed variables
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


class BotOperation(object):
    def __init__(self):
        # build botnet
        self.BOTNET = BotNet()
        self.startBot()

    def startBot(self):
        while True:
            userinput = input("BotNet$ ")
            if userinput == "?":
                self.displayCommands()
            elif userinput == "disconnect":
                print("Peace on the nets bruh!")
                break
            elif userinput.__contains__("create"):
                args = getargs(userinput)
                new_bot = Bot(args[0], args[1], args[2], args[3], args[4])
                if self.BOTNET.addbot(new_bot):
                    print(
                        "following bot created: \n\n"
                        "Unique name: " + new_bot.uniquename + "\n"
                                                               "Bot name: " + new_bot.botname + "\n"
                                                                                                "On host ip: " + new_bot.host_ip + "\n"
                                                                                                                                   "Username: " + new_bot.username + "\n"
                                                                                                                                                                     "Password: " + new_bot.password + "\n"
                                                                                                                                                                                                       "Port: " + str(
                            new_bot.port) + "\n"
                                            "Bot type: " + new_bot.type + "\n"
                    )
            elif userinput.__contains__("get all"):
                print(self.BOTNET.botnet)

            elif userinput.__contains__("select"):
                args = getargs(userinput)
                # if specific bot contained in list of uniquebot
                for bot in self.BOTNET.botnet[args[0]]:
                    if bot.type == args[1]:
                        userinput = input(args[1] + args[0] + " ready to go, enter command: \n" + bot.botname + "$ ")
                        self.operateBot(userinput, bot)

                    else:
                        print("this bot doesn't exist, create it with the create command, '?' for more info")

    def operateBot(self, userinput, bot):

        if userinput.__contains__("connect"):
            bot.connect()
        if userinput.__contains__("who?"):
            print(bot)
            userinput = input(bot.botname + "$ ")
            self.operateBot(userinput, bot)
        if userinput.__contains__("exit"):
            self.startBot()

        while bot.connected:
            userinput = input("shell$ ")
            if userinput == "disconnect":
                bot.disconnect()
                userinput = input(bot.botname + "$ ")
                self.operateBot(userinput, bot)
            stdin, stdout, stderr = bot.sshbot_client.exec_command(userinput)
            print(stdout.readlines())

        # fix max recursion depth error

    @staticmethod
    def displayCommands():
        print(
            "---------------------BOTNET COMMANDS---------------------\n"
            "create [uniquename, host_ip, username, password, port]\n"
            "select [uniquename, type]\n"
            "remove type [type, uniquebotname]\n"
            "destroy [uniquebotname]\n"
            "disconnect all\n"
            "delete all\n"
            "get all\n"
            "get connected\n"
            "get disconnected\n"
            "disconnect\n"
            "--------------------- BOT COMMANDS------------------\n"
            "connect\n"
            "disconnect\n"
            "who \n"
        )


def getargs(input):
    i_const_end = input.index("[")
    constinput = input[:i_const_end]

    userinput = input[i_const_end:]  # +1 includes the last space after constant part of command
    i_start_args = userinput.index("[") + 1
    i_close_args = userinput.index("]")
    userinput = userinput[i_start_args:i_close_args]

    return userinput.split(", ")


def main():
    """botnet = BotNet()
    mininetBot = Bot("mininetbot", "192.168.1.101", "mininet", "mininet", 22)
    mininetBot.SSHconnect()
    botnet.addbot(mininetBot)

    stdin, stdout, stderr = mininetBot.sshbot_client.exec_command("ls")
    print(stdout.readlines())

    print(botnet.botnet)"""

    # create [mininetbot, 192.168.1.118, mininet, mininet, 22]
    # create [mininetbot, 192.168.1.118, mininet, mininet, 4444]

    # botnet = BotNet()
    # mininetBot = Bot("mininetbot", "192.168.1.101", "mininet", "mininet", 4444)
    # botnet.addbot(mininetBot)
    # mininetBot.connect()

    # print(stdout.readlines())

    # print(botnet.botnet)

    BotOp = BotOperation()


if __name__ == '__main__':
    main()
