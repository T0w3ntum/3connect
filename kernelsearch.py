from subprocess import call

def main(s):
	s.send('uname -v\n')
	data = s.recv(1024)
	print "[+] Checking searchsploit for %s" % data
	call(['searchsploit', data])

