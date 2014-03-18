import subprocess
import signal 
import os
import confparse
import readline

def signal_handler(signal, frame):
    return True

def menu(PS1):
    stdinShell = input(PS1)
    if stdinShell == "exit":
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
                    os.chdir(os.path.expanduser("~"))
                    return True
            spawnedProc = subprocess.Popen(commandList, shell=False); spawnedProc.wait()
        except KeyboardInterrupt:
            spawnedProc.kill()
        except FileNotFoundError:
            print("Error --> {}: no such file or directory".format(commandList[0]))
    
def main():
    signal.signal(signal.SIGINT, signal_handler)
    readline.parse_and_bind('tab: complete')
    readline.parse_and_bind('set editing-mode vi')
    while(True):
        PS1 = confparse.getPS1()
        menu(PS1)

if __name__ == "__main__":
    main()
