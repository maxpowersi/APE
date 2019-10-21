from __future__ import print_function
import validators
import argparse
import sys
import os

def consoleWritte(msg):
    print("\x1b[6;30;42m" + msg +  "\x1b[0m")

def parseArgs():
    parser = argparse.ArgumentParser(description="", version="0.12b")

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

#no "/" at ends
apePath = os.path.dirname(os.path.realpath(__file__))
scanPath = os.path.join(projectPath, "scan")
servicesFolder =  [os.path.join(scanPath, "http"), 
                    os.path.join(scanPath, "https"), 
                    os.path.join(scanPath, "ftp"),
                    os.path.join(scanPath, "ssh"), 
                    os.path.join(scanPath, "smtp"), 
                    os.path.join(scanPath, "dns"), 
                    os.path.join(scanPath, "rdp"),
                    os.path.join(scanPath, "nmap")]

consoleWritte("--- Creating project folder ---")
if not os.path.exists(scanPath): os.system("mkdir " + scanPath)
for servicePath in servicesFolder:
    if not os.path.exists(servicePath): os.system("mkdir " + servicePath)
consoleWritte("--- The project folders were created ---")

consoleWritte("--- Starting scan tool for each target ---")
os.system("interlace -tL '{1}' -o '{0}' -cL '{2}/commands/scan.commands.txt' -threads {3}".format(scanPath, targets, apePath, queued))
consoleWritte("--- The scan was run ---")