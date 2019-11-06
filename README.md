
<img  src="https://github.com/maxpowersi/ape/raw/master/logo.png"  width="150"  height="150">.
# APE v0.15b
APE (in spanish "Asistente de Pentest Externo"), is an assistant tool for external pentest. This tool has two modules, recon and scan. Recon module can be used to lunch many tools for recon, and get info (for example subdomains) throug a domain. Scan module, run nmap scan and parse the result in order to run special tools (customizable) for each service. This tool is distributed under the GNU GPLv3 license.
## Requirements
- python
- go
- nodejs
- npm
- cat (unix tool)
- head (unix tool)
- sort (unix tool)
- dig (unix tool)
- interlace
- nmap
- nmap-parse-output
- All tools run in recon and scan module.
## Installation
The setup.sh script will try to install all tools and dependencies. <br/>
```
git clone https://github.com/maxpowersi/APE.git
cd APE
sudo ./setup.sh
```
>Check the default tools in each module, and check that you have all tools and they are accessible by the command line in the path var. Some of the tools can not be installed in this script, you will have to install mannualy and add it to the path.

## Recon module
This module will run all recon tools in the file "recon.commands.txt". By default this module run the following tools:
- The Harvester
- Sublist3r
- OWASP amass
- Subfinder
- knockpy
- Gitrob
- bucketeer
- subjack

After run the default tools, APE will create a folder with the domain in scope and a folder inside called "recon". In this folder a file called "subdomains.txt" will be created containing all enumerated subdomains (this file concatenate all files ending in ".subdomain.txt". A file called "ips.txt" will be created with the IP for each subdomain in the "subdomains.txt" file. Finally a file called "ips-unique.txt" will be created, ready to use in APE Scan module or in nmap or masscan.

### Adding new tools
You can add you own tools, editing the file "recon.commands.txt". If the tool added generates subdomains, please the output name must end in ".subdomain.txt" to be included in the output  file "subdomains.txt"
## Scan module
This module will run all recon tools in the file "scan.commands.txt". By default this module run nmap. After run the scan tools, this module will run each "{service}.commands.txt" file, to scan each target in scope using the output nmap. By default, for each service the following tools will be run:

>Note: Please observe  that (by default) each dictionary used by ncrack is called:
"usernames.{service}.txt and passwords.{service}.txt". For example:
"usernames.ftp.txt" is for ftp service.
### HTTPS
- testssl
- sslscan
### HTTP & HTTPS
- nikto
- getJS
- retire
- curl
- wappalyzer
- httprobe
- webscreenshot
- aquatone
- webtech
- waybackurls
- linkfinder
- photon
- gobuster
- opendoor
- virtual-host-discovery
- GoogD0rker
- Goohak
### SSH
- ncrack
- ssh-user-enumeration
- nmap scripts
	- banner
	- ssh-audit
	- ssh-auth-methods
	- sshv1
### Telnet
- ncrack
- nmap scripts
	- banner
	-  telnet-ntlm-info
### FTP
- ncrack
- nmap scripts
	- ftp-anon
	- ftp-bounce
	- ftp-syst
	- banner
### DNS
- dnswalk
- nmap scripts
	- banner
	- dns-cache-snoop
	- dns-recursion
### SMTP
- smtp-user-enum
- nmap scripts
	- banner
	- smtp-open-relay
	- smtp-commands
### RDP
- ncrack
- nmap scripts
	- rdp-ntlm-info
	- rdp-vuln-ms12-020
### SMB
- nmap scripts
	- rdp-ntlm-info
	- smb-protocols
	- smb-enum-shares
	- smb-vuln-ms17-010
### Adding new tools
You can add you own tools, editing the files "{service}.commands.txt". 
>Note: Please consider that this module can run more tools than nmap if the "scan.commands.txt" file is modified, but only can "parse" nmap outputs.
## All module
This module will run recon module, and when it finish, it will start scan module, using the output from recon module.
### Examples
## Help
```
+-+-+-+-+-+-+-+-+-
|A|P|E| |v|0|.|15b|
+-+-+-+-+-+-+-+-+-

usage: ape.py [-h] [-v] -m MODULE -t TARGET -o OUTPUTDIR -q QUEUED
              [-ip CREATEIPFILE]

optional arguments:
  -h, --help        show this help message and exit
  -v, --version     show program's version number and exit
  -m MODULE         module name, it must be recon, scan or all
  -t TARGET         target, for recon it must be a domain, for scan it must be
                    a text file with subdomains or IPs
  -o OUTPUTDIR      path to place all outputs
  -q QUEUED         number of queued or threads, each queued will process one
                    resource (IP or subdomain)
  -ip CREATEIPFILE  resolve subdomains and generate IPs file
```
## Recon
```
ape.py -m recon -t "domain.com" -o "/home/user/" -q 30 -ip true
```
## Scan
```
ape.py -m scan -t "/home/user/domain.com/recon/ips-unique.txt" -o "/home/user/domain.com/ -q 30
```
## All
```
ape.py -m all -t "domain.com" -o "/home/user/" -q 30 -ip true
```
