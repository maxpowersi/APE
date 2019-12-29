from __future__ import print_function
import validators
import argparse
import sys
import os
import datetime
import re 

def consoleWritte(msg):
    os.system("printf \"\e[92m--- {0} ---\e[0m\n\n\"".format(msg))

def parseArgs():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-t',action="store", dest="target", help="the target to perform recon", required=True)
    parser.add_argument('-o', action="store", dest="outputDir", help="path to place all outputs", required=True)
    parser.add_argument('-q', action="store", dest="threads", help="number of threads to use", required=True)
    parameters = parser.parse_args()

    if not validators.domain(parameters.target):
        print("The argument -t (target) is invalid, it must be a domain")
        sys.exit()

    if not os.path.exists(parameters.outputDir):
        print ("The argument -o (output dir) is invalid, it must be a valid path")
        sys.exit()

    if not validators.between(int(parameters.threads), min=1, max=50):
        print("The argument -q (queued) is invalid, min 1, max 500")
        sys.exit()
    
    return parameters

parameters = parseArgs()
target = parameters.target
threads = parameters.threads

apePath = os.path.dirname(os.path.realpath(__file__))
projectPath = os.path.join(parameters.outputDir, target)
reconPath = os.path.join(projectPath, "recon")
dnsresolverPath = os.path.join(projectPath, "recon/dnsresolver")
subdomainsFile = "{0}/subdomains.txt".format(reconPath)

regexIP = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''
      
consoleWritte("Creating project folders")
if not os.path.exists(projectPath): os.system("mkdir " + projectPath)
if not os.path.exists(reconPath): os.system("mkdir " + reconPath)

consoleWritte("Starting the recon scan")
os.system("cd '{0}'; interlace --silent -t '{1}' -o '{0}' -cL '{2}/commands/recon.commands.txt' -rp '{2}' -p {3} -threads {4}"
    .format(reconPath, target, apePath, target.split(".")[0], threads))

consoleWritte("Concatenating all subdomains found")
os.system("cd {0}; for i in *.csv; do  cat $i | cut -d ',' -f4 > $i.subdomain.txt; break; done ;cd {0}; sort -u *.subdomain.txt > {0}/subdomains.txt"
    .format(reconPath))

consoleWritte("Starting dns resolver for each subdomains")
if not os.path.exists(dnsresolverPath): os.system("mkdir " + dnsresolverPath)
dnsresolverCommandFilePath = os.path.join(dnsresolverPath, "dnsresolver.command.py")
os.system("interlace --silent -tL '{0}' -o '{1}' -cL '{3}/dnsresolver.command.py' -threads {2}".format(subdomainsFile, dnsresolverPath, threads, apePath))

consoleWritte("Concatenating all IPs found")
os.system("cd {0}; cat *.dig.txt > {1}/ips.txt".format(dnsresolverPath, reconPath))
os.system("cat {0}/ips.txt | cut -d ':' -f 2 | sed -e $'s/,/\\\n/g' | sort -u > {1}/ips-unique.tmp.txt".format(reconPath, dnsresolverPath))
ipsUnique = open("{0}/ips-unique.txt".format(reconPath), "w")
ipsUniqueTemp= open("{0}/ips-unique.tmp.txt".format(dnsresolverPath), "r")
for l in ipsUniqueTemp:
    if re.search(regexIP, l): ipsUnique.write(l)
ipsUnique.close()
ipsUniqueTemp.close()
os.system("rm -r {0}".format(dnsresolverPath))

consoleWritte("The scan was finished successfully")