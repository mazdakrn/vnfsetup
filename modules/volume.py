
from utils import app
from utils import text
from utils import proc
import time

""" create a disk """
def create (desc, output, args):

        vms = desc["VNF"]["vm"]
        prefix = desc["VNF"]["name"]

        for vm in vms:
                name = vm + "-" + prefix

                hosts = []
                if  desc["vm "+vm]["host"]!="":
                        hosts = text.getList(desc["vm "+vm]["host"])

                disk = []
                if desc["vm "+vm]["disk"] != "":
                        disk = text.getList(desc["vm "+vm]["disk"])

                j = 0
                for h in hosts:
                        j = j + 1
                        i = 0
                        params = []

                        for d in disk:
                                size = text.getItem(d, 0)
                                disk_name = text.getItem(d, 1)

                                i = i + 1
                                vname = name +"-no"+str(j)+"-node"+h
                                dname = vname+"-disk"+str(i)+"-"+size+"GB-"+disk_name

                                if search (dname) != -1:
                                        app.exists ("Volume "+dname)
                                        continue

                                params = [str(size), "--display-name="+ dname]

				if (proc.execProcess ("cinder", "create", params, output, args)):
                                        app.failed ("Creating volume " + dname)
                                else:
                                        app.passed ("Creating volume " + dname)


                                status = "creating"

                                while status!="available":
                                        time.sleep(1)
                                        buf = proc.readProcess ("cinder", "show", dname)

                                        for line in buf.readlines():
                                                if line.find("status")!=-1:
                                                        if text.getField(line, 1) == "status":
                                                                status = text.getField(line,2 )
                                                                break

                                        if status == "error":
                                                return -1

        return 1


""" search for a disk """
def search (name):

        buf = proc.readProcess ("cinder", "list")
	return (text.searchString(buf, name, 3))


""" delete a disk """
def delete (desc, output, args):

        vms = desc["VNF"]["vm"]
        prefix = desc["VNF"]["name"]

        for vm in vms:
                name = vm + "-" + prefix

		hosts = []
                if  desc["vm "+vm]["host"]!="":
                        hosts = text.getList(desc["vm "+vm]["host"])

		disk = []
                if desc["vm "+vm]["disk"] != "":
                        disk = text.getList(desc["vm "+vm]["disk"])

                j = 0
                for h in hosts:
                        j = j + 1
                        i = 0

                        for d in disk:
                                size = text.getItem(d, 0)
                                disk_name = text.getItem (d, 1)

                                i = i + 1
                                vname = name +"-no" + str(j) + "-node"+h
                                dname = vname+"-disk" + str(i) + "-"+size+"GB-"+disk_name

                                if search (dname) == -1:
                                        app.notfound ("Volume "+dname)
                                        continue

				if (proc.execProcess ("cinder", "delete", [dname], output, args)):
                                        app.failed ("Deleting volume " + dname)
                                else:
                                        app.passed ("Deleting volume " + dname)

        return 1

def deleteAll (desc, output, args):

        buf = proc.readProcess ("cinder", "list")

        try:
                for line in buf.readlines():
                        id = text.getField(line, 1)
                        name = text.getField(line, 3)

                        if search (name) == -1:
                                continue

			if (proc.execProcess ("cinder", "delete", [id], output, args)):
                                app.failed ("Deleting volume "+name)
                        else:
                                app.passed ("Deleting volume " + name)
        except:
                pass
