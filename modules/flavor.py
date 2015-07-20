from utils import app
from utils import text
from utils import proc

""" create a flavor """
def create (desc, output, args):

        vms = desc["VNF"]["vm"]
        prefix = desc["VNF"]["name"]

        for vm in vms:

                name = vm + "-" + prefix
                f = desc["vm "+vm]["flavor"]

                if search (name) != -1:
                        app.exists ("Flavor " + name)
                        continue

                memory = text.getItem (f, 0)
                disk = text.getItem (f, 1)
                cpu = text.getItem (f,2)

                params = [name, "auto", memory, disk, cpu]

		if (proc.execProcess("nova", "flavor-create", params, output, args)):
                        app.failed ("Creating flavor " + name)
                else:
                        app.passed ("Creating flavor " + name)


def search (name):

	buf = proc.readProcess ("nova", "flavor-list")
	return (text.searchString(buf, name))


""" delete a flavor """
def delete (desc, output, args):

        vms = desc["VNF"]["vm"]
        prefix = desc["VNF"]["name"]

        for vm in vms:
                name = vm + "-" + prefix

                if search (name) == -1:
                        app.notfound ("Flavor " + name)
                        continue

		if (proc.execProcess ("nova", "flavor-delete", [name], output, args)):
                        app.failed ("Deleting flavor " + name)
                else:
                        app.passed ("Deleting flavor " + name)


def deleteAll (desc, output, args):

        buf = proc.readProcess ("nova", "flavor-list")

        try:
                for line in buf.readlines():
                        id = text.getField(line, 1)
                        name = text.getField(line, 2)

			if (search (name)) == -1:
				continue

			if (proc.execProcess ("nova", "flavor-delete", [id], output, args)):
                                app.failed ("Deleting flavor " + name)
                        else:
                                app.passed ("Deleting flavor " + name)
        except:
                pass

