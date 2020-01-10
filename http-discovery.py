from __future__ import print_function
import validators
import argparse
import sys
import subprocess
import os
import datetime

parser = argparse.ArgumentParser(description="")
parser.add_argument('-t',action="store", dest="targets", help="list of URL in scope, in a text file", required=True)
parser.add_argument('-e',action="store", dest="extensions", help="extensions, coma separeted", default="")
parser.add_argument('-o', action="store", dest="outputDir", help="path to place all outputs", required=True)
parser.add_argument('-q', action="store", dest="queued", help="number of queued or threads, each queued will process one resource (IP, subdomain or URL)", required=True)
parameters = parser.parse_args()

targetsPath = parameters.targets
extensions = parameters.extensions
scanPath = parameters.outputDir
threads = parameters.queued
apePath  =  os.path.dirname(os.path.realpath(__file__))
commandsFolderPath = os.path.join(apePath, "commands")
commandsFilePath = os.path.join(commandsFolderPath, "http.discovery.commands")

targetFile = open(targetsPath)
commandsFile = open(commandsFilePath)
for target in targetFile:
    target = target.rstrip()
    for command in commandsFile:
        command = command.rstrip()
        command = command.replace("_TARGET_", target)
        command = command.replace("_DOMAIN_", target.replace("/","").replace(":","").replace("https", "").replace("http", ""))
        command = command.replace("_OUTPUT_", scanPath)
        command = command.replace("_APP_PATH_", apePath)
        command = command.replace("_THREADS_", threads)
        command = command.replace("_EXTENSIONS_NOT_DOT", extensions.replace(".", ""))
        command = command.replace("_EXTENSIONS_", extensions)
        if "echo" not in command:
            print('\033[93m' + command + '\033[0m')
        os.system(command)
targetFile.close()
commandsFile.close()