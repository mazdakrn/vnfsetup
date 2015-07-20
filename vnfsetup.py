#!/user/bin/python

import sys
import os

from modules import net
from modules import router
from modules import subnet
from modules import image
from modules import flavor
from modules import volume
from modules import vm

from utils import config
from utils import app
from utils import text
from utils import proc


def cleanModules (desc, output, args):
	
	modules = args["clean"]
	app.info ("Cleaning up ... ")
	
	if "vm" in modules or "all" in modules:
		app.info ("Cleaning VMs")
		vm.deleteAll (desc, output, args)

	if "vol" in modules or "all" in modules:
	        app.info ("Cleaning volumes")
        	volume.deleteAll (desc, output, args)

	if "net" in modules or "all" in modules:
	        app.info ("Cleaning routers")
        	router.deleteAll (desc, output, args)

	        app.info ("Cleaning subnets")
        	subnet.deleteAll (desc, output, args)

		app.info ("Cleaning all networks")
        	net.deleteAll (desc, output, args)

	if "flv" in modules or "all" in modules:
        	app.info ("Cleaning all flavors")
        	flavor.deleteAll (desc, output, args)

	if "img" in modules or "all" in modules:
        	app.info  ("Cleaning all images")
        	image.deleteAll (desc, output, args)


""" setup network, image, flavor """
def setupModules (desc, output, args):

	modules = args["setup"]
    	name = desc["VNF"]["name"]
    	app.info ("Setting up " + name)
	
	if "net" in modules or "all" in modules:
		if desc["VNF"]["network"] != []:
        		app.info ("Setting up network:")
	        	net.create (desc, output, args)

			app.info ("Setting up subnets:")
	        	subnet.create (desc, output, args)
    		else:
        		app.notfound ("network configuration")
    
	    	if desc["VNF"]["router"] != []:
        		app.info ("Setting up routers:")
	        	router.create (desc, output, args)
	    	else:
        		app.notfound ("router configuration")


	if "flv" in modules or "all" in modules:	
		if desc["VNF"]["vm"] != []:
        		app.info ("Setting up flavors:")
	        	flavor.create (desc, output, args)
		else:
        		app.notfound ("VM configuration")


	if "img" in modules or "all" in modules:
		if desc["VNF"]["vm"] != []:
			app.info ("Setting up images:")
		        image.create (desc, output, args)
		else:
        		app.notfound ("VM configuration")


	if "vol" in modules or "all" in modules:
		if desc["VNF"]["vm"] != []:
			app.info ("Setting up volumes:")
			volume.create (desc, output, args)
		else:
			app.info ("volume configuration")


	if "vm" in modules or "all" in modules:
		if desc["VNF"]["vm"] != []:
        		app.info ("Setting up VMs:")
        		vm.create (desc, output, args)
    		else:
        		app.info ("VM configuration")



""" clean up network, image, flavor """
def removeModules (desc, output, args):

	modules = args["remove"]
    	name = desc["VNF"]["name"]
    	app.info ("Removing " + name)

	if "vm" in modules or "all" in modules:
		if desc["VNF"]["vm"] != []:
        		app.info ("Removing VMs")
        		vm.delete (desc, output, args)
    		else:
        		app.notfound ("VM configuration")


        if "vol" in modules or "all" in modules:
                if desc["VNF"]["vm"] != []:
                        app.info ("Removing volumes:")
                        volume.delete (desc, output, args)
                else:
                        app.notfound ("volume configuration")


	if "net" in modules or "all" in modules:
    		if desc["VNF"]["router"] != []:  
        		app.info ("Removing routers:")
        		router.delete (desc, output, args)
    		else:
        		app.notfound ("router configuration")

    		if desc["VNF"]["network"] != []:
			app.info ("Removing subnets:")
			subnet.delete (desc, output, args)

			app.info ("Removing networks:")
        		net.delete (desc, output, args)
    		else:
        		app.notfound ("network configuration")
	

	if "flv" in modules or "all" in modules:
    		if desc["VNF"]["vm"] != []:
        		app.info ("Removing flavors:")
        		flavor.delete (desc, output, args)
    		else:
        		app.notfound ("VM configuration")


	if "img" in modules or "all" in modules:
    		if desc["VNF"]["vm"] != []:
			app.info ("Removing images:")
        		image.delete (desc ,output, args)
    		else:
        		app.notfound ("VM configuration")


def main(argv=None):
	
	if len(argv) == 0:
        	app.help()
                return 1

	ret, args = config.parseArguments(argv)

	if (ret != 0 or args['help'] == True):
		app.help()
		return 1 

        if args['input'] == "":
	        app.die ("Need a config file")

        if not os.path.isfile(args['input']):
        	app.die ("Config file does not exist")

	desc = config.config_read(args['input'])
	#app.chk_ip(desc)

        if args['log'] == "":
        	output = open (os.devnull, "w")
        else:
        	output = open (args['log'],"w")

        if (args['remove'] != ""):
        	ret = removeModules (desc, output, args)

	if (args['clean'] != ""):
		ret =  cleanModules (desc, output, args)

	if (args['setup'] != ""):
		ret =  setupModules (desc, output, args)
		
	output.close()
	return ret


""" start of script """
if __name__=='__main__': sys.exit(main(sys.argv[1:]))

