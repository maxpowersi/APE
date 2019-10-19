from __future__ import print_function
import validators
import argparse
import sys
import os

#Writte the hello banner
def banner():
    print("""
    +-+-+-+-+-+-+-+-+-
    |A|P|E| |v|0|.|12b|
    +-+-+-+-+-+-+-+-+-
    """)

#Writte to the console using colors
def consoleWritte(msg):
    print ("\x1b[6;30;42m" + msg +  "\x1b[0m")

#Pars all args
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

#Create project folder if this does not exist
def createProjectFolder(projectDir, reconPath):    
    consoleWritte("--- Creating project folder ---")

    if not os.path.exists(projectDir): os.system("mkdir " + projectDir)
    if not os.path.exists(reconPath): os.system("mkdir " + reconPath)

    consoleWritte("--- The project folders were created ---")

#Run recon tools
def reconTools(reconPath, apePath, target):
    consoleWritte("--- Starting the recon scan ---")

    os.system("cd '{0}'; interlace -t '{1}' -o '{0}' -cL '{2}/commands/recon.commands.txt' -threads 10".format(reconPath, target, apePath))

    consoleWritte("--- The recon scan was run ---")

#Merge subdomains outputs in order to create "subdomains.txt"
def mergeSubdomains(reconPath):
    consoleWritte( "--- Starting mergin all subdomains ---")

    subdomainsFile = "{0}/subdomains.txt".format(reconPath)

    #convert csv knockfile to  .subdomain.txt
    for file in os.listdir(reconPath):
        if file.endswith(".csv"):
            knockpyOutput = os.path.join(reconPath, file).replace(".csv", "")
            os.system("cd {0}; cat {1}.csv | cut -d ',' -f4 > {1}.subdomain.txt".format(reconPath, knockpyOutput))
            break

    os.system("cd {0}; cat *.subdomain.txt > {0}/subdomains-tmp.txt".format(reconPath))
    os.system(("(sort -u {0}/subdomains-tmp.txt) > " + subdomainsFile).format( reconPath))
    os.system("rm {0}/subdomains-tmp.txt".format(reconPath))

    consoleWritte("--- the merged file was created ---")

    return subdomainsFile

#Resolve each subdomain in "subdomains.txt"
def resolveDomain(subdomains, digPath, apePath):
    consoleWritte("--- Starting dig for each subdomains ---")

    os.system("interlace -tL '{0}' -o '{1}' -cL '{2}/commands/resolve.command.txt' -threads 30 > /dev/null".format(subdomains, digPath, apePath) )

    consoleWritte("--- All subdomains were resolved ---")

#Concate IPs to one file, "ips.txt"and "ips-unique.txt"
def concatenateIPs(reconPath, digPath):
    consoleWritte("--- Creating IP file ---")

    os.system("cd {0}; cat *.dig.txt > {1}/ips.txt".format(digPath, reconPath))
    os.system("(sort -u {0}/ips.txt) > {0}/ips-unique.txt".format(reconPath))
    os.system("rm -r {0}".format(digPath))

    consoleWritte("--- The IP file was created ---")

banner()

parameters = parseArgs()
target = parameters.target
createIpFiles = parameters.createIpFile

#no "/" at ends
apePath = os.path.dirname(os.path.realpath(__file__))
projectPath = os.path.join(parameters.outputDir, target)
reconPath = os.path.join(projectPath, "recon")
digPath = os.path.join(projectPath, "recon/dig")

createProjectFolder(projectPath, reconPath)
reconTools(reconPath, apePath, target)
subdomains = mergeSubdomains(reconPath)

if(createIpFiles.lower() == "true"):
    if not os.path.exists(digPath): os.system("mkdir " + digPath)
    resolveDomain(subdomains, digPath, apePath)
    concatenateIPs(reconPath, digPath)