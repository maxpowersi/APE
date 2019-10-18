
<img  src="https://github.com/maxpowersi/ape/raw/master/logo.png"  width="150"  height="150">.
# APE v0.12b
APE (in spanish "Asistente de Pentest Externo"), is an assistant tool for external pentest. This tool has two modules, recon and scan. Recon module can be used to lunch many tools for recon, and get info (for example subdomains) throug a domain. Scan module, run nmap scan and parse the result in order to run special tools (customizable) for each service. This tool is distributed under the GNU GPLv3 license.
## Requirements
- python
- cat (unix tool)
- head (unix tool)
- dig (unix tool)
- unique (unix tool)
- nmap
- interlace
- nmap-parse-output
- All tools run in recon and scan module.
>Check the default tools in each module, and check that you have all tools and they are accessible by the command line in the path var.
## Installation
```
sudo ./setup.sh
```
## Recon module
This module will run all recon tools in the file "recon.commands.txt". By default this module run the following tools:
- The Harves
- Sublist3r
- OWASP amass
- Subfinder
- knockpy
- lazys3
- teh_s3_bucketeers
- Gitrob

After run the default tools, APE will create a folder with the domain in scope and a folder inside called "recon". In this folder a file called "subdomains.txt" will be created containing all enumerated subdomains (this file concatenate all files ending in ".subdomain.txt". A file called "ips.txt" will be created with the IP for each subdomain in the "subdomains.txt" file. Finally a file called "ips-unique.txt" will be created, ready to use in APE Scan module or in nmap or masscan.

### Adding new tools
You can add you own tools, editing the file "recon.commands.txt". If the tool added generates subdomains, please the output name must end in ".subdomain.txt" to be included in the output  file "subdomains.txt"
### Examples
```
usage: ape-recon.py [-h] [-v] -t TARGET -o OUTPUTDIR -th THREADS

  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
  -t TARGET      the target to perform recon
  -o OUTPUTDIR   path to place all outputs
  -th THREADS    number of threads
```
```
ape-recon.py -t "domain.com" -o "/home/user/folder-output" -th 5
```
## Scan module
This module will run all recon tools in the file "scan.commands.txt". By default this module run nmap. After run the scan tools, this module will run each "{service}.commands.txt" file, to scan each target in scope using the output nmap. By default, for each service the following tools will be run:

>Note: Please observe  that (by default) each dictionary used by ncrack is called:
"usernames.{service}.txt and passwords.{service}.txt". For example:
"usernames.ftp.txt" is for ftp service.
### HTTP
- curl
- httprobe
- phantomJS
- aquatone
- wappalyzer
- webtech
- nikto
- retire
- waybackurls
- linkfinder
- photon
- gobuster
- opendoor
- virtual-host-discovery
- GoogD0rker
- Goohak
### HTTPS
- testssl
- sslscan
### SSH
- ncrack
- ssh-user-enumeration
- nmap scripts
	- banner
	- ssh-audit
	- ssh-auth-methods
	- sshv1
### FTP
- ncrack
- nmap scripts
	- ftp-anon
	- ftp-bounce
	- ftp-syst
	- banner
### Telnet
- ncrack
- nmap scripts
	- banner
	-  telnet-ntlm-info
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
	-  smb-enum-shares
	- smb-vuln-ms17-010
### Adding new tools
You can add you own tools, editing the files "{service}.commands.txt". 
>Note: Please consider that this module can run more tools than nmap if the "scan.commands.txt" file is modified, but only can "parse" nmap outputs.
### Examples
```
usage: ape-scan.py [-h] [-v] -t TARGET -o OUTPUTDIR -th THREADS

  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
  -t TARGET      text file with all IPs in scope
  -o OUTPUTDIR   path to place all outputs
  -th THREADS    number of threads
```
```
ape-scan.py -t domain.com/recon/ips-unique.txt -o OUTPUTDIR -th THREADS
```
