import getopt
import os
import ConfigParser

import text
import app

def config_read(file):

        if not os.path.isfile(file):
                app.die ("Configuration file does not exist")

        parser = ConfigParser.ConfigParser()
        parser.read(file)

        if not parser.has_section("VNF"):
                app.die ("Config file: cannot find section [VNF]")

	config = {}
        config['VNF']={}

        if parser.has_option("VNF","name") and parser.get("VNF", "name") != "":
                config['VNF']['name'] = parser.get("VNF","name").strip()
        else:
                config['VNF']['name'] = ""

        if parser.has_option("VNF","network") and parser.get("VNF","network") != "":
                config['VNF']['network'] = text.getList(parser.get("VNF","network"))
        else:
                config['VNF']['network']=[]

        if parser.has_option("VNF","router") and parser.get("VNF","router") != "":
                config['VNF']['router'] = text.getList(parser.get("VNF","router"))
        else:
                config['VNF']['router'] = []

        if parser.has_option("VNF","vm") and parser.get("VNF","vm") != "":
                config['VNF']['vm'] = text.getList(parser.get("VNF","vm"))
        else:
                config['VNF']['vm'] = []

        options = {}
        options ['VNF'] = ['network','router','vm']
        options ['network'] = ['subnet','start','end','dhcp','gateway','nameserver','route','type']
        options ['vm'] = ['image','host','flavor','disk','network','userdata']
        options ['router'] = ['interface']

        for sec in options['VNF']:
                for n in config['VNF'][sec]:

                        name = sec + " " + n
                        if not parser.has_section(name):
                                app.die ("Config file: cannot find section [" + name + "]")

                        config[name] = {}

                        for opt in options[sec]:
                                if parser.has_option(name,opt):
                                        config[name][opt] = parser.get(name,opt).strip()
                                else:
                                        config[name][opt] = ""

        return config


def parseArguments(argv):

	options = {}
	options['help'] = False
	options['input'] = ""
	options['log'] = ""
	options['clean'] = ""
	options['setup'] = ""
	options['remove'] = ""
	options['verbosity'] = 0
	options['debug'] = False

        try:
		opts, args = getopt.getopt(argv,"hr:l:i:s:c:vd",["help","remove=","log=","input=","setup=","clean=","verbose","debug"])
                
		for opt, arg in opts:
                        if opt in ("-h","--help"):
				options['help'] = True
                        elif opt in ("-l","--log"):
                                options['log'] = arg
                        elif opt in ("-i","--input"):
                                options['input'] = arg
                        elif opt in ("-c","--clean"):
                                options['clean'] = text.getList (arg)
                        elif opt in ("-s","--setup"):
                                options['setup'] = text.getList (arg)
			elif opt in ("-r","--remove"):
				options["remove"] = text.getList (arg)
			elif opt in ("-v","--verbose"):
				options["verbosity"] = options["verbosity"] + 1
			elif opt in ("-d","--debug"):
				options["debug"] = True

		return 0, options

        except getopt.GetoptError:
                return 1, options

