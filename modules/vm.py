import os
import time

import net
import image
import volume
import flavor

from utils import app
from utils import text
from utils import proc

""" create a vm """
def create (desc, output, args):

        vms = desc["VNF"]["vm"]
        prefix = desc["VNF"]["name"]

        for vm in vms:
                name = vm + "-" + prefix

                hosts = []
                if  desc["vm "+vm]["host"]!="":
                        hosts = text.getList (desc["vm "+vm]["host"])

                disk = []
                if desc["vm "+vm]["disk"] != "":
                        disk = text.getList(desc["vm "+vm]["disk"])

                network = []
                if desc["vm "+vm]["network"] != "":
                        network = text.getList(desc["vm "+vm]["network"])

                j = 0
                for h in hosts:
                        j = j + 1
                        i = 0
                        params = []
                        dev = "a"
                        vname = name +"-no"+str(j)+"-node"+h

                        if search (vname) != -1:
                                app.exists ("VM " + vname)
                                continue

                        for d in disk:
                                size = text.getItem (d,0)
                                disk_name = text.getItem(d,1)
                                dot = text.getItem (d,2)

                                i = i + 1
                                n = vname+"-disk"+str(i)+"-"+size+"GB-"+disk_name

                                """ user create disk"""
                                id = volume.search (n)
                                if id == -1:
                                        app.warn ("Cannot find volume" + n)
					continue

                                params = params + ["--block-device-mapping","vd"+dev+"="+id+":::"+dot]
                                dev = chr(ord(dev)+1)

                        for n in network:
                                netn = n + "-" + prefix
                                id = net.search (netn)
                                if id == -1:
                                        app.warn ("Connot find network " + netn)
					continue

                                params = params + ["--nic","net-id=" + id]


                        params = [vname] + params + ["--flavor",name,"--image",name]

                        if (h != 'x'):
                                params = params + ["--availability_zone","nova:" + h]


                        """more check needed"""
                        data = desc["vm "+vm]["userdata"] + "/" + "user-data"
                        if os.path.isfile (data):
                                params = params + ["--config-drive","true","--user-data",data]

			if (proc.execProcess ("nova", "boot", params, output, args)):
                                app.failed ("Creating VM " + vname)
                        else:
                                app.passed ("Creating VM " + vname)


                        status = "creating"

                        while status!="ACTIVE":
                                time.sleep(1)
                                buf = proc.readProcess ("nova", "show", vname)

                                for line in buf.readlines():
                                        if line.find("status")!=-1:
                                                if text.getField(line, 1) == "status":
                                                        status = text.getField(line,2)
                                                        break

                                if status == "ERROR":
                                        app.warn ("Error creating VM " + vname)
                                        continue


"""search for an ID of a vm """
def search (name):

        buf = proc.readProcess ("nova", "list")
	return (text.searchString(buf, name))


""" delete a vm """
def delete (desc, output, args):
	
        vms = desc["VNF"]["vm"]
        prefix = desc["VNF"]["name"]

        for vm in vms:
                name = vm + "-" + prefix
                hosts = text.getList(desc["vm "+vm]["host"])

                j = 0
                for h in hosts:
                        j = j + 1
                        vname = name+"-no"+str(j)+"-node"+h

                        if search (vname) == -1:
                                app.notfound ("VM " + vname)
                                continue


			if (proc.execProcess ("nova", "delete", [vname], output, args)):
                                app.failed ("Deleting VM " + vname)
                        else:
                                status=0
                                while status!=-1:
                                        status = search (vname)
                                        time.sleep(1)

                                app.passed ("Deleting VM " + vname)


def deleteAll (desc, output, args):

        buf = proc.readProcess ("nova", "list")

        try:
                for line in buf.readlines():
                        id = text.getField(line, 1)
                        name = text.getField(line, 2)

			if search (name) == -1:
				continue

			if (proc.execProcess ("nova", "delete", [id], output, args)):
                                app.failed ("Deleting vm " + name)
                        else:
                                app.passed ("Deleting vm " + name)
        except:
                pass

