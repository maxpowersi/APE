from __future__ import print_function
import validators
import argparse
import sys
import os
import datetime

def consoleWritte(msg):
    os.system("printf \"\e[92m--- {0} ---\e[0m\n\n\"".format(msg))

parser = argparse.ArgumentParser(description="")
parser.add_argument('-nhs', action="store_true", dest="noHostScan", help="if its presents, host scan will be executed")
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

queued = parameters.queued
targets = parameters.targets
projectPath = parameters.outputDir
noHostScan = False

if parameters.noHostScan:
    noHostScan = True

apePath = os.path.dirname(os.path.realpath(__file__))
scanPath = os.path.join(projectPath, "scan")
commandsFolderPath = os.path.join(apePath, "commands")

hostCommandsPath = os.path.join(commandsFolderPath, "host.commands")
commandsFiles =  [("ftp", "ftp.commands", "ftp"), 
                  ("ssh", "ssh.commands", "ssh"),
                  ("smtp", "smtp.commands", "smtp"),
                  ("domain", "dns.commands", "dns"),
                  ("ms-wbt-server", "rdp.commands", "rdp"),
                  ("telnet", "telnet.commands", "telnet"),
                  ("http", "http.commands", "http"),
                  ("ssl", "https.commands", "https"),
                  ("https", "https.commands", "https"),
                  ("ssl", "http.commands", "https"),
                  ("https", "http.commands", "https")]
httpJSService =  [("https", "http.js.commands", "https"), ("http", "http.js.commands", "http"), ("ssl", "http.js.commands", "https")]

hostCommandsRunPath = os.path.join(commandsFolderPath, "host.commands.run")
scanCommandsRunPath = os.path.join(commandsFolderPath, "scan.commands.run")
httpJSCommandsRunPath = os.path.join(commandsFolderPath, "http.js.commands.run")

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
                   os.path.join(scanPath, "http-discovery"),
                   os.path.join(scanPath, "host")]

consoleWritte("Creating project folder")
if not os.path.exists(scanPath): os.system("mkdir " + scanPath)
for servicePath in servicesFolder:
    if not os.path.exists(servicePath):
        os.system("mkdir " + servicePath)

consoleWritte("Building host commands list")
hostCommandsRunFile = open(hostCommandsRunPath, "w") 
f = open(hostCommandsPath)
for line in f:
    newLine = line.rstrip()
    if ("_block:" not in newLine and "_blocker_" not in newLine):
        newLine = newLine.replace("_TARGET_", "_target_")
        newLine = newLine.replace("_OUTPUT_", scanPath)
        newLine = newLine.replace("_COMPANY_", "")
        newLine = newLine.replace("_APP_PATH_", apePath)
    hostCommandsRunFile.write(newLine + "\n") 
f.close()
hostCommandsRunFile.close() 

consoleWritte("Building scan commands list")
out = open(scanCommandsRunPath, "w") 
for tup in commandsFiles:
    service =  tup[0]
    commandFileName = tup[1]
    protocol =  tup[2]
    commandFile = os.path.join(commandsFolderPath, commandFileName)
    f = open(commandFile)
    for line in f:
        newLine = line.rstrip()
        if ("_block:" not in newLine and "_blocker_" not in newLine):
            newLine = "nmap-parse-output host/_target_.tcp.top1000.xml service '{0}' | cut -d ':' -f2 | while read p; do {1}; done".format(service, newLine)
            newLine = newLine.replace("_PORT_", "$p")
            newLine = newLine.replace("_TARGET_", "_target_")
            newLine = newLine.replace("_OUTPUT_", scanPath)
            newLine = newLine.replace("_COMPANY_", "")
            newLine = newLine.replace("_APP_PATH_", apePath)
            newLine = newLine.replace("_PROTOCOL_", protocol)
            newLine = newLine.replace("_THREADS_", queued)
        out.write(newLine + "\n") 
    f.close()
out.close() 

consoleWritte("Building http JS commands list")
out = open(httpJSCommandsRunPath, "w") 
for tup in httpJSService:
    service =  tup[0]
    commandFileName = tup[1]
    protocol =  tup[2]
    commandFile = os.path.join(commandsFolderPath, commandFileName)
    f = open(commandFile)
    for line in f:
        newLine = line.rstrip()
        if ("_block:" not in newLine and "_blocker_" not in newLine):
            newLine = "nmap-parse-output host/_target_.tcp.top1000.xml service '{0}' | cut -d ':' -f2 | while read p; do {1}; done".format(service, newLine)
            newLine = newLine.replace("_PORT_", "$p")
            newLine = newLine.replace("_TARGET_", "_target_")
            newLine = newLine.replace("_OUTPUT_", scanPath)
            newLine = newLine.replace("_COMPANY_", "")
            newLine = newLine.replace("_APP_PATH_", apePath)
            newLine = newLine.replace("_PROTOCOL_", protocol)
        out.write(newLine + "\n") 
    f.close()
out.close() 

if noHostScan:
    consoleWritte("Host scan skipped")
else:    
    consoleWritte("Starting host scan")
    os.system("cd '{0}'; interlace -timeout 1200 -tL '{1}' -cL '{2}' -threads {3}".format(scanPath, targets, hostCommandsRunPath, queued))

os.system("cd {0}; sh '{1}/nmapConvertFix.sh'".format(os.path.join(scanPath, "host"), apePath))
with open(os.path.join(scanPath, "nmapToConvert.tmp.txt")) as f:
    for line in f:
        parsedLine = line.split(":")
        toEditFile  = parsedLine[0]
        toEditLine  = int(parsedLine[1])
        toEditFilePath = os.path.join(os.path.join(os.path.join(scanPath, "host"), toEditFile))
        with open(toEditFilePath, 'r') as fileStream:
            data = fileStream.readlines()
            data[toEditLine - 1] = data[toEditLine - 1].replace('name="http"', 'name="https"')
        with open(toEditFilePath, 'w') as fileStream:
            fileStream.writelines(data)
os.remove(os.path.join(scanPath, "nmapToConvert.tmp.txt"))
os.remove(hostCommandsRunPath)

consoleWritte("Starting services scan")
os.system("cd '{0}'; interlace -timeout 1200 -tL '{1}' -cL '{2}' -threads {3}".format(scanPath, targets, scanCommandsRunPath, queued))
os.remove(scanCommandsRunPath)

consoleWritte("Starting http JS scan")
os.system("cd '{0}'; interlace -timeout 1200 -tL '{1}' -cL '{2}' -threads {3}".format(scanPath, targets, httpJSCommandsRunPath, queued))
os.remove(httpJSCommandsRunPath)

consoleWritte("The scan was finished successfully")