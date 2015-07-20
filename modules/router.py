from utils import app
from utils import text
from utils import proc

""" create a virtual router """
def create (desc, output, args):

        router = desc["VNF"]["router"]
        prefix = desc["VNF"]["name"]

        for r in router:
                name = r + "-" + prefix

                if search (name) != -1:
                        app.exists ("Router " + name)
                        continue

		if (proc.execProcess ("neutron", "router-create", [name], output, args)):
                        app.failed ("Creating router " + name)
                else:
                        app.passed ("Creating router " + name)

                if desc["router "+r]["interface"] != "":
                        interface = text.getList(desc["router "+r]["interface"])
                        for i in interface:
                                params = [name, i + "-" + prefix]

				if (proc.execProcess ("neutron", "router-interface-add", params, output, args)):
                                        app.failed ("Adding interface " + i + "-" + prefix + " to router " + name)
                                else:
                                        app.passed ("Adding interface " + i + "-" + prefix + " to router " + name)

                id = search (name)


def search (name):

        buf = proc.readProcess ("neutron", "router-list")
	return (text.searchString(buf, name))


""" delete a virtual router """
def delete (desc, output, args):

        router = desc["VNF"]["router"]
        prefix = desc["VNF"]["name"]

        for r in router:
                name = r + "-" + prefix
                interface = desc["router "+r]["interface"]

                router_id = search (name)
                if router_id == -1:
                        app.notfound ("Router " + name)
                        continue

                if (interface !=""):
                        for i in text.getList(interface):
                                params = [name, i + "-" + prefix]

				if (proc.execProcess ("neutron", "router-interface-delete", params, output, args)):
                                        app.failed ("Removing interface " + i + "-" + prefix + " from router " + name)
                                else:
                                        app.passed ("Removing interface " + i + "-" + prefix + " from router " + name)

		if (proc.execProcess ("neutron", "router-delete", [name], output, args)):
                        app.failed ("Deleting router " + name)
                else:
                        app.passed ("Deleting router " + name)


def deleteAll (desc, output, args):

        buf = proc.readProcess ("neutron", "router-list")

        try:
                for line in buf.readlines():
                        id = text.getField(line, 1)
                        name = text.getField(line, 2)

                        if name in search (name) == -1:
                                continue

                        netbuf = proc.readProcess ("neutron", "subnet-list")

                        try:
                                for net in netbuf.readlines():
                                        net_id = text.getField (net, 1)
                                        net_name = text.getField (net, 2)

					params = [id, net_name]

					if (proc.execProcess ("neutron", "router-interface-delete", params, output, args)):
						app.failed ("Remove interface " + net_name + " from router " + name)
					else:
                                                app.passed ("Removed interface " + net_name + " from router " + name)

                        except:
                                pass

			if (proc.execProcess ("neutron", "router-delete", [id], output, args)):
                                app.failed ("Deleting router " + name)
                        else:
                                app.passed ("Deleting router " + name)
        except:
                pass

