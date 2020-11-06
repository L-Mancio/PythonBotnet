from Botnet.Bot import Bot
from Botnet.oldFiles.BotNet import BotNet


def getargs(commandinput):
    i_const_end = commandinput.index("[")
    constinput = commandinput[:i_const_end]

    userinput = commandinput[i_const_end:]  # +1 includes the last space after constant part of command
    i_start_args = userinput.index("[") + 1
    i_close_args = userinput.index("]")
    userinput = userinput[i_start_args:i_close_args]

    return userinput.split(", ")


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
                        "Port: " + str(new_bot.port) + "\n"
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
