import validators
import argparse
import sys
import os

#Writte the hello banner
def banner():
    print """
    +-+-+-+-+-+-+-+-+-
    |A|P|E| |v|0|.|12b|
    +-+-+-+-+-+-+-+-+-
    """

#Writte to the console using colors
def consoleWritte(msg):
    print "\x1b[6;30;42m" + msg +  "\x1b[0m"

#Pars all args
def parseArgs():
    parser = argparse.ArgumentParser(description="", version="0.12b")

    parser.add_argument('-t',action="store", dest="targets", help="list of IPs in scope, in a text file", required=True)
    parser.add_argument('-o', action="store", dest="outputDir", help="path to place all outputs", required=True)
    parser.add_argument('-q', action="store", dest="queued", help="number of queued, each queued will process one resource (IP or subdomain)", required=True)
    parameters = parser.parse_args()

    if not validators.domain(parameters.targets):
        print "The argument -t (targets) is invalid"
        sys.exit()

    if not os.path.exists(parameters.outputDir):
        print "The argument -o (output dir) is invalid"
        sys.exit()

    if not validators.between(int(parameters.queued), min=1, max=50):
        print "The argument -q (queued) is invalid, min 1, max 50"
        sys.exit()
    
    return parameters

banner()
parameters = parseArgs()
queued = parameters.queued
targets = parameters.targets
projectDir = parameters.outputDir