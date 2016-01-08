import os
import subprocess, shlex, time

def getdata_condkeys(data, key, condkeys, condvalues, islist=False):
	'''
	Gets  data[key] values as list with condkeys satisfying condvalues
	'''
	keydata = []
	for k,d in data.iteritems():
		condvalid = True
		for k in range(len(condkeys)):
			condkey = condkeys[k]
			condvalue = condvalues[k]
			if d[condkey] != condvalue:
				condvalid = False
				break
		if condvalid:
			if islist:
				keydata.extend(d[key])
			else:
				keydata.append(d[key])
	return keydata

def getsortedkeys(undict, reverse=False):
	skeys = []
	unsorteddict = dict(undict)
	while len(unsorteddict.keys()) > 0:
		if reverse:
			maxvalue = max(unsorteddict.values())
		else:
			maxvalue = min(unsorteddict.values())
		mkeys = [x for x in unsorteddict.keys() if unsorteddict[x] == maxvalue]
		for mk in mkeys:
			skeys.append(mk)
			del unsorteddict[mk]
	return skeys

def createDir(direc):
	command = "mkdir -p "+direc
	#print "create dir for ", direc

	if not (os.path.exists(direc) and os.path.isdir(direc)):
		os.system(command) 

def command(args, timeout = 300):
	print "Command: ", args
	args = shlex.split(args)
	p = subprocess.Popen(args, stdout=subprocess.PIPE)#, stdin=None, stdout=PIPE, stderr=None)

	timeout = timeout/10
	op = ""

	if timeout ==0:
		timeout = 1

	time.sleep(5)
	for i in range(timeout):
		if p.poll() is  0:
			op, err = p.communicate(None)
			return op
		else:
			time.sleep(10)
	if p.poll() is not 0:
		p.kill()
		print "Timeout, killed process"
	else:
		op, err = p.communicate(None)
	return op


def createstructure(datastructure,keys, lasttype='{}'):
	tempdata = datastructure
	for k in keys:
		if not tempdata.has_key(k):
			if keys.index(k) +1 < len(keys):
				tempdata[k] = {}
			elif lasttype == '()':
				tempdata[k] = set()
			elif lasttype == '[]':
				tempdata[k] = []
			elif lasttype == '0':
				tempdata[k] = 0
			else:
				tempdata[k] = {}
		tempdata = tempdata[k]

def getrevdns(ip):
		try:
			output = subprocess.check_output(shlex.split('dig -x '+ip))
			return output.split('ANSWER SECTION:')[1].strip().split('\n')[0].split('PTR')[1].strip()[:-1]
		except:
			#print 'error in ', output , 'for ', ip
			return  str(ip)
