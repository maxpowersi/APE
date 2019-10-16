import validators
import argparse
import sys
import os

#Writte the hello banner
def banner():
    print """
    +-+-+-+-+-+-+-+-+-+
    |A|P|E| |v|0|.|1b|
    +-+-+-+-+-+-+-+-+-+
    """

#Writte to the console using colors
def consoleWritte(msg):
    print "\x1b[6;30;42m" + msg +  "\x1b[0m"

#Pars all args
def parseArgs():
    parser = argparse.ArgumentParser(description="", version="0.1b")
    parser.add_argument('-t',action="store", dest="target", help="the target to perform recon", required=True)
    parser.add_argument('-o', action="store", dest="outputDir", help="path to place all outputs", required=True)
    parser.add_argument('-th', action="store", dest="threads", help="number of threads", required=True)
    parameters = parser.parse_args()

    if not validators.domain(parameters.target):
        print "The argument -t (target) is invalid"
        sys.exit()

    folder = os.path.dirname(parameters.outputDir)
    if not os.path.exists(folder):
        print "The argument -o (output dir) is invalid"
        sys.exit()

    if not validators.between(int(parameters.threads), min=1, max=50):
        print "The argument -th (threads) is invalid, min 1, max 50"
        sys.exit()
    
    return parameters

#Create project folder if this does not exist
def createProjectFolder(parameters):
    folder = parameters.outputDir + parameters.target
    if not os.path.exists(folder):
        myCmd = "mkdir {OUTPUT}/{TARGET}"
        myCmd = myCmd.replace("{TARGET}", parameters.target)
        myCmd = myCmd.replace("{OUTPUT}", parameters.outputDir)
        os.system(myCmd)
        os.system(myCmd + "/recon")
        os.system(myCmd + "/scan")
        os.system(myCmd + "/recon/dig")
        consoleWritte("--- The project folder was create ---")
    else:
        consoleWritte("--- The project folder exists ---")

#Run recon tools
def reconTools(parameters):
    consoleWritte("--- Starting the recon scan ---")
    myCmd = "interlace -t {TARGET} -o {OUTPUT} -cL commands/recon.commands.txt -threads {THREADS}"
    myCmd = myCmd.replace("{TARGET}", parameters.target)
    myCmd = myCmd.replace("{OUTPUT}", parameters.outputDir)
    myCmd = myCmd.replace("{THREADS}", parameters.threads)
    os.system(myCmd)
    consoleWritte("--- The recon scan was run ---")

#Merge subdomains outputs in order to create "subdomains.txt"
def mergeSubdomains(parameters):
    consoleWritte( "--- Starting mergin all subdomains ---")
    #subdomains = "{OUTPUT}" + "/" + "{PROJECT_NAME}" + "/recon/" + "{PROJECT_NAME}" + ".sublist3r.txt".replace("{PROJECT_NAME}", parameters.target).replace("{OUTPUT}", parameters.outputDir)
    myCmd = "cd {OUTPUT}/{PROJECT_NAME}/recon/; cat *.subdomain.txt > {OUTPUT}/{PROJECT_NAME}/recon/subdomains-tmp.txt"
    myCmd = myCmd.replace("{PROJECT_NAME}", parameters.target)
    myCmd = myCmd.replace("{OUTPUT}", parameters.outputDir)
    os.system(myCmd)
    myCmd = "(sort  {OUTPUT}/{PROJECT_NAME}/recon/subdomains-tmp.txt | uniq -u) >  {OUTPUT}/{PROJECT_NAME}/recon/subdomains.txt"
    myCmd = myCmd.replace("{PROJECT_NAME}", parameters.target)
    myCmd = myCmd.replace("{OUTPUT}", parameters.outputDir)
    os.system(myCmd)
    myCmd = "rm {OUTPUT}/{PROJECT_NAME}/recon/subdomains-tmp.txt"
    myCmd = myCmd.replace("{PROJECT_NAME}", parameters.target)
    myCmd = myCmd.replace("{OUTPUT}", parameters.outputDir)
    os.system(myCmd)
    consoleWritte("--- the merged file was created ---")

#Resolve each subdomain in "subdomains.txt"
def resolveDomain(parameters, subdomains):
    consoleWritte("--- Starting dig for each subdomains ---")
    myCmd = "interlace -tL {SUBDOMAINS_LIST} -o {OUTPUT} -cL commands/resolve.command.txt -threads {THREADS} -p {PROJECT_NAME}".replace("{SUBDOMAINS_LIST}", subdomains)
    myCmd = myCmd.replace("{THREADS}", parameters.threads)
    myCmd = myCmd.replace("{PROJECT_NAME}", parameters.target)
    myCmd = myCmd.replace("{OUTPUT}", parameters.outputDir)
    os.system(myCmd)
    myCmd = "rm -r {OUTPUT}/{PROJECT_NAME}/recon/dig"
    myCmd = myCmd.replace("{PROJECT_NAME}", parameters.target)
    myCmd = myCmd.replace("{OUTPUT}", parameters.outputDir)
    os.system(myCmd)
    consoleWritte("--- all subdomains were resolved ---")

#Concate IPs to one file, "ips.txt"and "ips-unique.txt"
def concatenateIPs(parameters):
    consoleWritte("--- Creating IP file ---")
    myCmd = "cd {OUTPUT}/{PROJECT_NAME}/recon/dig/; cat *.dig.txt > {OUTPUT}/{PROJECT_NAME}/recon/ips_list.txt"
    myCmd = myCmd.replace("{PROJECT_NAME}", parameters.target)
    myCmd = myCmd.replace("{OUTPUT}", parameters.outputDir)
    os.system(myCmd)
    myCmd = "(sort  {OUTPUT}/{PROJECT_NAME}/recon/ips.txt | uniq -u) >  {OUTPUT}/{PROJECT_NAME}/recon/ips-unique.txt"
    myCmd = myCmd.replace("{PROJECT_NAME}", parameters.target)
    myCmd = myCmd.replace("{OUTPUT}", parameters.outputDir)
    consoleWritte("The IP file was created")

banner()
parameters = parseArgs()
createProjectFolder(parameters)
reconTools(parameters)
subdomains = mergeSubdomains(parameters)
resolveDomain(parameters, subdomains)
concatenateIPs(parameters)