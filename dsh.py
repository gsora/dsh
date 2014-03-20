import subprocess
import signal 
import os
import confparse
import readline

homePath = os.path.expanduser("~")

def signal_handler(signal, frame):
    return True

def get_history_items():
    return [ readline.get_history_item(i)
             for i in xrange(1, readline.get_current_history_length() + 1)
             ]

class HistoryCompleter(object):
    
    def __init__(self):
        self.matches = []
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            history_values = get_history_items()
            if text:
                self.matches = sorted(h 
                                      for h in history_values 
                                      if h and h.startswith(text))
            else:
                self.matches = []
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response

def histFilePath():
    histFile = confparse.getHistFile()
    # if history file is specified
    if histFile is not None:
        histFile = histFile.replace("~", os.path.expanduser("~")).replace("./", os.getcwd() + "/").replace("\n", "")
        print(os.path.exists(histFile))
        if not os.path.exists(histFile):
            os.system("touch {}".format(histFile))
            readline.read_history_file(histFile)
            return histFile
        else:
            readline.read_history_file(histFile)
            return histFile
    else:
        # file not specified
        if not os.path.exists(os.path.expanduser("~./dsh_history")):
            os.system("touch ~/.dsh_history")
            readline.read_history_file(os.path.expanduser("~/.dsh_history"))
            histFile = os.path.expanduser("~/.dsh_history")
            return histFile
        else:
            readline.read_history_file(os.path.expanduser("~/.dsh_history"))
            histFile = os.path.expanduser("~/.dsh_history")
            return histFile
    

def menu(PS1, histFile):
    stdinShell = input(PS1)
    stdinShell = stdinShell.replace("~", os.path.expanduser("~"))
    if stdinShell == "exit":
        readline.write_history_file(histFile)
        exit()
    
    if stdinShell == "clear":
        subprocess.call("clear")
        return True
        
    if stdinShell == "help":
        print("Dumb Shell: the dumbest shell you'll find on the net. Period.")
        return True
    
    commandList = stdinShell.split(' ')
    
    argsString = ""
    
    firstIteration = True
    for i in commandList:
        if len(commandList) == 1:
            argsString = "no arguments given"
            break
        if i == commandList[0]:
            pass
        else:
            if firstIteration == True:
                argsString = i
                firstIteration = False
            else:
                argsString = argsString + ", " + i
                
    if(len(commandList) == 1 and commandList[0] == ""):
        pass
    else:
        try:
            if commandList[0] == "cd":
                try:
                    os.chdir(commandList[1])
                    return True
                except IndexError:
                    os.chdir(homePath)
                    return True
            spawnedProc = subprocess.Popen(commandList, shell=False); spawnedProc.wait()
        except KeyboardInterrupt:
            spawnedProc.kill()
        except FileNotFoundError:
            print("Error --> {}: no such file or directory".format(commandList[0]))
    readline.write_history_file(histFile)
    
def main():
    signal.signal(signal.SIGINT, signal_handler)
    readline.parse_and_bind('tab: complete')
    readline.parse_and_bind('set editing-mode vi')
    readline.set_completer(HistoryCompleter().complete)
    histFile = histFilePath()
    while(True):
        PS1 = confparse.getPS1()
        menu(PS1, histFile)

if __name__ == "__main__":
    main()
