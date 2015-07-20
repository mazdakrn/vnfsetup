from utils import app
from utils import text
from utils import proc

def create (desc, output, args):

        network = desc["VNF"]["network"]
        prefix = desc["VNF"]["name"]

        for n in network:
                name = n + "-" + prefix
                subnet = desc["network "+n]["subnet"]
                start = desc["network "+n]["start"]
                end = desc["network "+n]["end"]
                dhcp = desc["network "+n]["dhcp"]
                gateway = desc["network "+n]["gateway"]
                nameserver = desc["network "+n]["nameserver"]
                route = desc["network "+n]["route"]

                if search (name) != -1:
                        app.exists ("Subnet " + name)
                        continue

                params = [name, subnet,"--name",name]

                if start != "" and end != "":
                        params = params + ["--allocation-pool","start=" + start + ",end="+ end]

                if gateway != "":
                        params = params + ["--gateway="+gateway]

                if dhcp == "false":
                        params = params + ["--disable-dhcp"]

                if nameserver != "":
                        params = params + ["--dns_nameservers","list=true"]
                        for ns in text.getList(nameserver):
                                params = params + [ns]

                if route != "":
                        params = params + ["--host_routes","type=dict","list=true"]
                        for r in text.getList(route):
                                dest = getitem (r, 0)
                                next_hop = text.getItem (r, 1)
                                params = params + ["destination="+dest+",nexthop="+next_hop]

		if (proc.execProcess("neutron", "subnet-create", params, output, args)):
                        app.failed ("Creating subnet "+name)
                else:
                        app.passed ("Creating subnet " + name)


def search (name):

        buf = proc.readProcess ("neutron", "subnet-list")
	return (text.searchString(buf, name))


""" delete a subnet """
def delete (desc, output, args):

        network = desc["VNF"]["network"]
        prefix = desc["VNF"]["name"]

        for n in network:
                name = n + "-" + prefix

                if search (name) == -1:
                        app.notfound ("Subnet " + name)
                        continue

		if (proc.execProcess ("neutron", "subnet-delete", [name], output, args)):
                        app.failed ("Deleting subnet " + name)
                else:
                        app.passed ("Deleting subnet " + name)



def deleteAll (desc, output, args):

        buf = proc.readProcess ("neutron", "subnet-list")

        try:
                for line in buf.readlines():
                        id = text.getField(line, 1)
                        name = text.getField (line, 2)

			if search (name) == -1:
				continue

			if (proc.execProcess ("neutron", "subnet-delete", [id], output, args)):
                                app.failed ("Deleting subnet " + name)
                        else:
                                app.passed ("Deleting subnetwork " + name)
        except:
                pass

