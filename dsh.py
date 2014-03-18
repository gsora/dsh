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
            logging.debug('history: %s', history_values)
            if text:
                self.matches = sorted(h 
                                      for h in history_values 
                                      if h and h.startswith(text))
            else:
                self.matches = []
            logging.debug('matches: %s', self.matches)
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        logging.debug('complete(%s, %s) => %s', 
                      repr(text), state, repr(response))
        return response

def menu(PS1, histFile):
    histFilePath = ""
    histFile = histFile.replace("~", os.path.expanduser("~"))
    
    try:
        if not os.path.exists(histFile):
            os.system("touch {}".format(histFile))
            readline.read_history_file(histFile)
            histFilePath = histFile
        else:
            readline.read_history_file(histFile)
            histFilePath = histFile
    except FileNotFoundError:
        os.system("touch ~/.dsh_history")
        readline.read_history_file(os.path.expanduser("~/.dsh_history"))
        histFilePath = os.path.expanduser("~/.dsh_history")
        
    stdinShell = input(PS1)
    stdinShell = stdinShell.replace("~", os.path.expanduser("~"))
    if stdinShell == "exit":
        readline.write_history_file(histFilePath)
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
    readline.write_history_file(histFilePath)
    
def main():
    signal.signal(signal.SIGINT, signal_handler)
    readline.parse_and_bind('tab: complete')
    readline.parse_and_bind('set editing-mode vi')
    readline.set_completer(HistoryCompleter().complete)
    while(True):
        PS1 = confparse.getPS1()
        histFile = confparse.getHistFile()
        menu(PS1, histFile)

if __name__ == "__main__":
    main()
