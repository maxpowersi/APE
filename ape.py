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
parser.add_argument('-t',action="store", dest="target", help="target, for recon it must be a domain, for scan it must be a text file with subdomains or IPs", required=True)
parser.add_argument('-o', action="store", dest="outputDir", help="path to place all outputs", required=True)
parser.add_argument('-q', action="store", dest="queued", help="number of queued or threads, each queued will process one resource (IP or subdomain)", required=True)
parameters = parser.parse_args()

if not parameters.module.lower() in ["scan", "recon"]:
    print("The argument -m (module) is invalid, it must be recon or scan")
    sys.exit()

module = parameters.module
isScan = module == "scan"

if parameters.module.lower() == "scan":
    if not os.path.isfile(parameters.target):
        print("The argument -t (target) is invalid, it must be a text file with IPs or subdomains.")
        sys.exit()
else:
    if not validators.domain(parameters.target):
        print("The argument -t (target) is invalid, it must be a domain")
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
    os.system("python3 '{3}/scan-ape.py' -t '{0}' -o '{1}' -q {2} ".format(target, projectPath, queued, apePath))
else:
    os.system("python3 '{3}/recon-ape.py' -t '{0}' -o '{1}' -q {2}".format(target, projectPath, queued, apePath))