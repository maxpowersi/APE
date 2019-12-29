from __future__ import print_function
import validators
import argparse
import sys
import os
import datetime

def consoleWritte(msg):
    os.system("printf \"\e[92m--- {0} ---\e[0m\n\n\"".format(msg))

def parseArgs():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-t',action="store", dest="targets", help="list of IPs in scope, in a text file", required=True)
    parser.add_argument('-o', action="store", dest="outputDir", help="path to place all outputs", required=True)
    parser.add_argument('-q', action="store", dest="queued", help="number of queued, each queued will process one resource (IP or subdomain)", required=True)
    parameters = parser.parse_args()

    if not os.path.isfile(parameters.targets):
        print("The argument -t (targets) is invalid, it must be a text file with IPs or subdomains.")
        sys.exit()

    if not os.path.exists(parameters.outputDir):
        print("The argument -o (output dir) is invalid, it must be a valid folder")
        sys.exit()

    if not validators.between(int(parameters.queued), min=1, max=50):
        print("The argument -q (queued) is invalid, min 1, max 500")
        sys.exit()
    
    return parameters

parameters = parseArgs()
queued = parameters.queued
targets = parameters.targets
projectPath = parameters.outputDir

apePath = os.path.dirname(os.path.realpath(__file__))
scanPath = os.path.join(projectPath, "scan")
servicesFolder =  [os.path.join(scanPath, "http"), 
                   os.path.join(scanPath, "ftp"),
                   os.path.join(scanPath, "ssh"), 
                   os.path.join(scanPath, "telnet"), 
                   os.path.join(scanPath, "smtp"), 
                   os.path.join(scanPath, "dns"), 
                   os.path.join(scanPath, "rdp"),
                   os.path.join(scanPath, "https"),
                   os.path.join(scanPath, "http/JS"),
                   os.path.join(scanPath, "https/JS"),
                   os.path.join(scanPath, "host")]

commandsFiles =  [("ftp", "ftp.commands.txt"), 
                  ("ssh", "ssh.commands.txt"),
                  ("smtp", "smtp.commands.txt"),
                  ("dns", "dns.commands.txt"),
                  ("rdp", "rdp.commands.txt"),
                  ("telnet", "telnet.commands.txt"),
                  ("ssl", "ssl.commands.txt"),
                  ("https", "ssl.commands.txt"),
                  ("ssl", "https.commands.txt"),
                  ("https", "https.commands.txt"),
                  ("http", "http.commands.txt")]

consoleWritte("Creating project folder")
if not os.path.exists(scanPath): os.system("mkdir " + scanPath)
for servicePath in servicesFolder:
    if not os.path.exists(servicePath): os.system("mkdir " + servicePath)

consoleWritte("Building commands list")
scanCommandsFile = open(os.path.join(os.path.join(apePath, "commands"), "scan.commands.txt"), "w") 
scanCommandsFileAfter = open(os.path.join(os.path.join(apePath, "commands"), "scanAfter.commands.txt"), "w") 
for tup in commandsFiles:
    service =  tup[0]
    commandFileName = tup[1]
    commandFile = os.path.join(os.path.join(apePath, "commands"), commandFileName)
    f = open(commandFile)
    for line in f:
        writter = scanCommandsFile
        if "###" in line:
            writter = scanCommandsFileAfter
            line = line.replace("###", "")
        newLine = "nmap-parse-output host/_target_.xml service '{0}' | cut -d ':' -f2 | while read p; do {1}; done".format(service, line.rstrip())
        newLine = newLine.replace("_port_", "$p")            
        writter.write(newLine  + "\n") 
    f.close()
scanCommandsFile.close() 
scanCommandsFileAfter.close()
print(os.path.join(os.path.join(apePath, "commands"), "scan.commands.txt"))
consoleWritte("Starting host scan")
os.system("cd '{0}'; interlace --silent -timeout 1200 -tL '{1}' -o '{0}' -cL '{2}/commands/host.commands.txt' -threads {3}"
    .format(scanPath, targets, apePath, queued))

consoleWritte("Starting services scan")
os.system("cd '{0}'; interlace --silent -timeout 1200 -tL '{1}' -o '{0}' -cL '{2}/commands/scan.commands.txt' -threads {3}"
    .format(scanPath, targets, apePath, queued))
os.system("interlace --silent -timeout 1200 -tL '{1}' -o '{0}' -cL '{2}/commands/scanAfter.commands.txt' -threads {3}"
    .format(scanPath, targets, apePath, queued))

os.remove(os.path.join(os.path.join(apePath, "commands"), "scan.commands.txt"))
os.remove(os.path.join(os.path.join(apePath, "commands"), "scanAfter.commands.txt"))

consoleWritte("The scan was finished successfully")