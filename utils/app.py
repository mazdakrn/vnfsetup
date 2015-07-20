import sys
import socket

def die(message):
        print "[-] " + message
        sys.exit(1)

def warn(message):
        print "[-] " + message

def info(message):
        print "[*] " + message

def ok(message):
        print "[+] " + message



def failed(message):
        warn (message + " ... failed")

def passed(message):
        ok (message + " ... done")

def exists (message):
        info (message + " exists ... skipping")

def notfound (message):
        warn (message + " not found ... skipping")


def printCMD(command, subcommand, params):

	print "[D] exec -> " + command + " " +  subcommand,
        for item in params:
        	print " " + item,

	print
	sys.stdout.flush()


def chk_ip(desc):
	
	networks = desc["VNF"]["network"]
	IPS = ["subnet","start","end","gateway"]

	for n in networks:
	
		name = "network "+n

		for item in IPS:
			val = desc[name][item]
			if val != "":
				ip = val.split("/")[0]
				
				try:
					socket.inet_aton(ip)
				except socket.error:
					die ("Config file error : invalid value for " + item + " in section " + name)


def help():
	print "vnfsetup.py <options> <actions> <modules>"
        print "\nOptions:"
        print "\t-i <config file> or --input=<config file> \tspecify configuration file"
        print "\t-l <log file> or --log=<log file> \t\tspecify log files"
        print "\t-d or --debug \t\t\t\t\tShow executed commands"
        print "\t-v or --verbose \t\t\t\tVerbose mode"
        print "\t-h or --help \t\t\t\t\tHelp"
	
        print "\nActions:"
        print "\t-s <modules> or --setup <modules>\tsetup vnf"
        print "\t-r <modules> or --setup <modules>\tremove vnf"
        print "\t-c <modules> or --clean <modules>\tclean system"
	print "\nModules:"
	print "\tnet\tnetwork"
	print "\tflv\tflavor"
	print "\timg\timage"
	print "\tvol\tvolume"
	print "\tvm\tvirtual machine"
	print "\tall\tall modules (net,flv,img,vol,vm)"
	print
