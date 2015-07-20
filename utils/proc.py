import subprocess
from subprocess import call
import StringIO

import app

def execProcess(command, subcommand, params, output, args):

	if (args['debug'] == True):
			app.printCMD (command, subcommand, params)

	return (call([command, subcommand] + params, stdout = output, stderr = subprocess.STDOUT))



def readProcess(command, subcommand, params = None):

	if (params == None):
                p = subprocess.Popen ([command,subcommand], stdout=subprocess.PIPE)
	else:
                p = subprocess.Popen ([command,subcommand, params], stdout=subprocess.PIPE)
     
	res, err = p.communicate()
        buf =  StringIO.StringIO(res)

        buf.readline()
        buf.readline()
        buf.readline()

	return buf
	
