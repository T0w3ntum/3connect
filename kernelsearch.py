from subprocess import call

def main(s):
	s.send('uname -r\n')
	data = s.recv(1024)
	print "\n[+] Checking searchsploit for %s\n" % data
	call(['searchsploit', data])

