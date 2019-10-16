import validators
import argparse
import sys
import os

#Writte the hello banner
def banner():
    print """
    +-+-+-+-+-+-+-+-+-
    |A|P|E| |v|0|.|1b|
    +-+-+-+-+-+-+-+-+-
    """

#Writte to the console using colors
def consoleWritte(msg):
    print "\x1b[6;30;42m" + msg +  "\x1b[0m"

#Pars all args
def parseArgs():
    parser = argparse.ArgumentParser(description="", version="0.12b")

    parser.add_argument('-t',action="store", dest="target", help="the target to perform recon", required=True)
    parser.add_argument('-o', action="store", dest="outputDir", help="path to place all outputs", required=True)
    parser.add_argument('-th', action="store", dest="threads", help="number of threads", required=True)
    parameters = parser.parse_args()

    if not validators.domain(parameters.target):
        print "The argument -t (target) is invalid"
        sys.exit()

    if not os.path.exists(parameters.outputDir):
        print "The argument -o (output dir) is invalid"
        sys.exit()

    if not validators.between(int(parameters.threads), min=1, max=50):
        print "The argument -th (threads) is invalid, min 1, max 50"
        sys.exit()
    
    return parameters

#Create project folder if this does not exist
def createProjectFolder(projectDir, reconPath, digPath):    
    consoleWritte("--- Creating project folder ---")

    if not os.path.exists(projectDir):
        os.system("mkdir " + projectDir)

    if not os.path.exists(reconPath):
        os.system("mkdir " + reconPath)

    if not os.path.exists(digPath):
        os.system("mkdir " + digPath)

    consoleWritte("--- The project folders were created ---")
    return projectDir

#Run recon tools
def reconTools(reconPath, apePath, threads, target):
    consoleWritte("--- Starting the recon scan ---")
        
    myCmd = "cd '{RECON_PATH}'; interlace -t '{TARGET}' -o '{RECON_PATH}' -cL '{APE_PATH}/commands/recon.commands.txt' -threads {THREADS}"   
    myCmd = myCmd.replace("{RECON_PATH}", reconPath)
    myCmd = myCmd.replace("{APE_PATH}", apePath)
    myCmd = myCmd.replace("{THREADS}", threads)
    myCmd = myCmd.replace("{TARGET}", target)
    os.system(myCmd)

    consoleWritte("--- The recon scan was run ---")

#Merge subdomains outputs in order to create "subdomains.txt"
def mergeSubdomains(reconPath):
    consoleWritte( "--- Starting mergin all subdomains ---")

    subdomainsFile = "{RECON_PATH}/subdomains.txt".replace("{RECON_PATH}", reconPath)

    myCmd = "cd {RECON_PATH}; cat *.subdomain.txt > {RECON_PATH}/subdomains-tmp.txt".replace("{RECON_PATH}", reconPath)
    os.system(myCmd)
    
    myCmd = ("(sort {RECON_PATH}/subdomains-tmp.txt | uniq -u) > " + subdomainsFile).replace("{RECON_PATH}", reconPath)
    os.system(myCmd)
    
    myCmd = "rm {RECON_PATH}/subdomains-tmp.txt".replace("{RECON_PATH}", reconPath)
    os.system(myCmd)

    consoleWritte("--- the merged file was created ---")
    return subdomainsFile

#Resolve each subdomain in "subdomains.txt"
def resolveDomain(subdomains, digPath, apePath, threads):
    consoleWritte("--- Starting dig for each subdomains ---")

    myCmd = "interlace -tL '{SUBDOMAINS_LIST}' -o '{DIG_PATH}' -cL '{APE_PATH}/commands/resolve.command.txt' -threads {THREADS}"
    myCmd = myCmd.replace("{SUBDOMAINS_LIST}", subdomains)
    myCmd = myCmd.replace("{DIG_PATH}", digPath)
    myCmd = myCmd.replace("{APE_PATH}", apePath)
    myCmd = myCmd.replace("{THREADS}", threads)    
    os.system(myCmd)

    consoleWritte("--- All subdomains were resolved ---")

#Concate IPs to one file, "ips.txt"and "ips-unique.txt"
def concatenateIPs(reconPath, digPath):
    consoleWritte("--- Creating IP file ---")

    myCmd = "cd {DIG_PATH}; cat *.dig.txt > {RECON_PATH}/ips.txt"
    myCmd = myCmd.replace("{RECON_PATH}", reconPath)
    myCmd = myCmd.replace("{DIG_PATH}", digPath)
    os.system(myCmd)

    myCmd = "(awk 'NF > 0' {RECON_PATH}/ips.txt | uniq) > {RECON_PATH}/ips-unique.txt"
    myCmd = myCmd.replace("{RECON_PATH}", reconPath)
    os.system(myCmd)

    myCmd = "rm -r {DIG_PATH}"
    myCmd = myCmd.replace("{DIG_PATH}", digPath)
    os.system(myCmd)

    consoleWritte("--- The IP file was created ---")


banner()
parameters = parseArgs()

threads = parameters.threads
target = parameters.target

#no "/" at ends
apePath = os.path.dirname(os.path.realpath(__file__))
projectPath = os.path.join(parameters.outputDir, target)
reconPath = os.path.join(projectPath, "recon")
digPath = os.path.join(projectPath, "recon/dig")

createProjectFolder(projectPath, reconPath, digPath)
reconTools(reconPath, apePath, threads, target)
subdomains = mergeSubdomains(reconPath)
resolveDomain(subdomains, digPath, apePath, threads)
concatenateIPs(reconPath, digPath)