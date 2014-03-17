from time import strftime
from socket import gethostname
from os import getcwd, path
from getpass import getuser

def getPS1():
    configFilePath = path.expanduser("~/.dshrc")

    currentTime = strftime("%X")
    currentDate = strftime("%x")
    hostname = gethostname()
    curDir = getcwd()
    username = getuser()

    configFile = open(configFilePath, 'r')
    for line in configFile:
        if line[:1] is "#":
            pass
        elif line[:4] == "PS1=":
            return(line.replace("@time", currentTime).replace("@date", currentDate).replace("@host", hostname).replace("@pwd", curDir).replace("@user", username)[4:])