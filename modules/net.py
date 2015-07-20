from utils import app
from utils import text
from utils import proc

""" create network """
def create (desc, output, args):

        network = desc["VNF"]["network"]
        prefix = desc["VNF"]["name"]

        for n in network:
                name = n + "-" + prefix
                type = desc["network "+n]["type"]
                params = [name]

                if search (name) != -1:
                        app.exists ("Network " + name)
                        continue

                if type == 'external':
                        params = params + ["--router:external=True"]

		if (proc.execProcess ("neutron", "net-create", params, output, args)):
                        app.failed ("Creating network " + name)
                else:
                        app.passed ("Creating network " + name)


""" delete a network """
def delete (desc, output, args):

        network = desc["VNF"]["network"]
        prefix = desc["VNF"]["name"]

        for n in network:
                name = n + "-" + prefix

                if search (name) == -1:
                        app.notfound ("Network " + name)
                        continue

		if (proc.execProcess ("neutron", "net-delete", [name], output, args)):
                        app.failed ("Deleting network " + name)
                else:
                        app.passed ("Deleting network " + name)


""" search for a network ID"""
def search (name):

        buf = proc.readProcess ("neutron", "net-list")
	return (text.searchString(buf, name))


def deleteAll (desc, output, args):

        buf = proc.readProcess ("neutron", "net-list")

        try:
                for line in buf.readlines():
                        id = text.getField(line, 1)
                        name = text.getField(line, 2)

			if search (name) == -1:
				continue

			if (proc.execProcess ("neutron", "net-delete", [id], output, args)):
                                app.failed ("Deleting network " + name)
                        else:
                                app.passed ("Deleting network " + name)
        except:
                pass

