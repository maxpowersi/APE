from __future__ import print_function
import validators
import argparse
import sys
import os

print("""
+-+-+-+-+-+-+-+-+-
|A|P|E| |v|1|.|0|
+-+-+-+-+-+-+-+-+-
""")

parser = argparse.ArgumentParser(description="")
parser.add_argument('-m',action="store", dest="module", help="module name, it must be recon, scan or all", required=True)
parser.add_argument('-e',action="store_true", dest="extensions", help="extensions, coma separeted", default="")
parser.add_argument('-nhs', action="store_true", dest="noHostScan", help="if its presents, host scan will be executed")
parser.add_argument('-t',action="store", dest="target", help="target, for recon it must be a domain, for scan it must be a text file with subdomains or IPs", required=True)
parser.add_argument('-o', action="store", dest="outputDir", help="path to place all outputs", required=True)
parser.add_argument('-q', action="store", dest="queued", help="number of queued or threads, each queued will process one resource (IP, subdomain or URL)", required=True)
parameters = parser.parse_args()

if not parameters.module.lower() in ["scan", "recon", "httpdiscovery"]:
    print("The argument -m (module) is invalid, it must be recon, scan or httpdiscovery")
    sys.exit()

extensions = parameters.extensions
noHostScan = False
module = parameters.module.lower()
isScan = module == "scan"
isRecon = module == "recon"

if parameters.noHostScan:
    noHostScan = True

if isRecon:
    if not validators.domain(parameters.target):
        print("The argument -t (target) is invalid, it must be a domain")
        sys.exit()
else:
    if not os.path.isfile(parameters.target):
        print("The argument -t (target) is invalid, it must be a text file with IPs or subdomains.")
        sys.exit()
        
if not os.path.exists(parameters.outputDir):
    print("The argument -o (output dir) is invalid, it must be a valid folder")
    sys.exit()

if not validators.between(int(parameters.queued), min=1, max=50):
    print("The argument -q (queued) is invalid, min 1, max 500")
    sys.exit()

apePath = os.path.dirname(os.path.realpath(__file__))
target = parameters.target
queued = parameters.queued
projectPath = parameters.outputDir

if isScan:
    if noHostScan:
        os.system("python3 '{3}/scan-ape.py' -t '{0}' -o '{1}' -q {2} -nhs".format(target, projectPath, queued, apePath))
    else:
        os.system("python3 '{3}/scan-ape.py' -t '{0}' -o '{1}' -q {2}".format(target, projectPath, queued, apePath))
else:
    if isRecon:
        os.system("python3 '{3}/recon-ape.py' -t '{0}' -o '{1}' -q {2}".format(target, projectPath, queued, apePath))
    else:
        if extensions is not "":
             os.system("python3 '{3}/http-discovery.py' -t '{0}' -o '{1}' -q {2} -e {4}".format(target, projectPath, queued, apePath, extensions))
        else:
             os.system("python3 '{3}/http-discovery.py' -t '{0}' -o '{1}' -q {2}".format(target, projectPath, queued, apePath))