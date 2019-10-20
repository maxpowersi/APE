from __future__ import print_function
import validators
import argparse
import sys
import os
import datetime

def consoleWritte(msg):
    print ("\x1b[6;30;42m" + msg +  "\x1b[0m")

def parseArgs():
    parser = argparse.ArgumentParser(description="", version="0.12b")
    parser.add_argument('-t',action="store", dest="target", help="the target to perform recon", required=True)
    parser.add_argument('-o', action="store", dest="outputDir", help="path to place all outputs", required=True)
    parser.add_argument('-ip', action="store", dest="createIpFile", help="resolve subdomains and generate IPs file", required=True)
    parameters = parser.parse_args()

    if not validators.domain(parameters.target):
        print("The argument -t (target) is invalid, it must be a domain")
        sys.exit()

    if not os.path.exists(parameters.outputDir):
        print ("The argument -o (output dir) is invalid, it must be a valid path")
        sys.exit()

    if not parameters.createIpFile.lower() in ["true", "false"]:
        print ("The argument -ip (createIpFile) is invalid, it must be true or false")
        sys.exit()
    
    return parameters

print("""
+-+-+-+-+-+-+-+-+-
|A|P|E| |v|0|.|12b|
+-+-+-+-+-+-+-+-+-
""")

parameters = parseArgs()
target = parameters.target
createIpFiles = parameters.createIpFile

#no "/" at ends
apePath = os.path.dirname(os.path.realpath(__file__))
projectPath = os.path.join(parameters.outputDir, target)
reconPath = os.path.join(projectPath, "recon")
digPath = os.path.join(projectPath, "recon/dig")
subdomainsFile = "{0}/subdomains.txt".format(reconPath)
now = datetime.datetime.now()

consoleWritte("--- Creating project folder ---")
if not os.path.exists(projectPath): os.system("mkdir " + projectPath)
if not os.path.exists(reconPath): os.system("mkdir " + reconPath)
consoleWritte("--- The project folders were created ---")

consoleWritte("--- Starting the recon scan at {0}:{1}:{2} ---".format(now.hour, now.minute, now.second))
os.system("cd '{0}'; interlace -t '{1}' -o '{0}' -cL '{2}/commands/recon.commands.txt' -rp '{2}' -threads 10 -p {3}"
    .format(reconPath, target, apePath, target.split(".")[0]))
consoleWritte("--- The recon scan was run ---")

if(createIpFiles.lower() == "true"):
    if not os.path.exists(digPath): os.system("mkdir " + digPath)
    consoleWritte("--- Starting dig for each subdomains ---")
    digCommand = "(ip=$(dig +short _target_ | head -n 1); if [ $ip ] ; then echo $ip; else echo '\n'; fi > _output_/_target_.dig.txt) > /dev/null 2>&1"
    os.system("interlace -tL '{0}' -o '{1}' -c '{2}' -threads 30 > /dev/null".format(subdomainsFile, digPath, digCommand))
    os.system("cd {0}; cat *.dig.txt > {1}/ips.txt".format(digPath, reconPath))
    os.system("(sort -u {0}/ips.txt) > {0}/ips-unique.txt".format(reconPath))
    os.system("rm -r {0}".format(digPath))
    consoleWritte("--- All subdomains were resolved ---")

now = datetime.datetime.now()
consoleWritte("--- The recon scan finished at {0}:{1}:{2} ---".format(now.hour, now.minute, now.second))