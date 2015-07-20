from utils import app
from utils import text
from utils import proc

import os

""" create an image """
def create (desc, output, args):

        vms = desc["VNF"]["vm"]
        prefix = desc["VNF"]["name"]

        for vm in vms:
                name = vm + "-" + prefix
		fmt = text.getItem(desc["vm "+vm]["image"],0)
                image = text.getItem(desc["vm "+vm]["image"],1)

                if search (name) != -1:
                        app.exists ("Image " + name)
                        continue

                if not os.path.isfile(image):
                        app.warn ("Image " + image + " does not exist")
			continue

                params = ["--name",name ,"--container-format","bare","--file",image]
		params = params + ['--disk-format', fmt]

		if (proc.execProcess ("glance", "image-create", params, output, args)):
                        app.failed ("Creating image " + name)
                else:
                        app.passed ("Creating image " + name)


def search (name):

        buf = proc.readProcess ("glance", "image-list")
	return (text.searchString(buf, name))


""" delete an image """
def delete (desc, output, args):

        vms = desc["VNF"]["vm"]
        prefix = desc["VNF"]["name"]

        for vm in vms:
                name = vm + "-" + prefix

                if search (name) == -1:
                        app.notfound  ("Image " + name)
                        continue

		if (proc.execProcess("glance", "image-delete", [name], output, args)):
                        app.failed ("Deleting image " + name)
                else:
                        app.passed ("Deleting image " + name)


def deleteAll(desc, output, args):

        buf = proc.readProcess ("glance", "image-list")

        try:
                for line in buf.readlines():
                        id = text.getField (line, 1)
                        name = text.getField (line, 2)

                        if search (name)== -1:
                                continue
	
			if (proc.execProcess ("glance", "image-delete", [id], output, args)):
                                app.failed ("Deleting image " + name)
                        else:
                                app.passed ("Deleting image " + name)
        except:
                pass

