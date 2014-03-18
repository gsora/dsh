def getPS1():
    from time import strftime
    from socket import gethostname
    from os import getcwd, path
    from getpass import getuser
    
    configFilePath = path.expanduser("~/.dshrc")

    currentTime = strftime("%X")
    currentDate = strftime("%x")
    hostname = gethostname()
    curDir = getcwd()
    username = getuser()

    configFile = open(configFilePath, 'r+')
    for line in configFile:
        if line[:1] is "#":
            pass
        elif line[:4] == "PS1=":
            return(line.replace("@time", currentTime).replace("@date", currentDate).replace("@host", hostname).replace("@pwd", curDir).replace("@user", username).rstrip('\n')[4:])

def getHistFile():
    from os import path
    
    configFilePath = path.expanduser("~/.dshrc")

    configFile = open(configFilePath, 'r+')
    for line in configFile:
        if line[:1] is "#":
            pass
        elif line[:5] == "HIST=":
            return(line[5:])