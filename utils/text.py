
def searchString (buf, word, match = 2):

	for line in buf.readlines():
        	if line.find(word)!=-1:
                	if (word == line.split("|")[match].strip()):
                         	id = line.split("|")[1]
                                return id.strip()

        return -1

# 512:1:1
def getItem(buf, id):

	return buf.strip().split(":")[id].strip()



def getField(buf, id):

	return buf.strip().split("|")[id].strip()


def getList(buf):
	return [x.strip() for x in buf.strip().split(",")]
