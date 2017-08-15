import socket, sys, select, json
from optparse import OptionParser

def prompt() :
    sys.stdout.write('')
    sys.stdout.flush()

def print_opt(file):
	with open(file) as data_file:
		data = json.load(data_file)
	keylist = data.keys()
	keylist.sort()
	for i in keylist:
		print i + ":\t" + data[i][0]
	ans = True
	while ans:
		ans = raw_input("[!]>")
		msg = data[ans][1]
		ans = False
	return msg

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
			msg = print_opt('windows.json')
			p = False
		elif p == "2":
			msg = print_opt('linux.json')
			p = False
	return msg

def main_loop(s):
	while 1:
		socket_list = [sys.stdin, s]
		read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
		for sock in read_sockets:
			if sock == s:
				data = sock.recv(4096)
				if not data:
					print '\n[-] Disconnected from target.'
					sys.exit()
				else:
					sys.stdout.write(data)
					with open("3connect.log", "a") as f:
						f.write(data)
					prompt()
			else:
				msg = sys.stdin.readline()
				if msg[0] == '#':
					msg = get_cmd()
					s.send(msg)
					prompt()
				else:
					s.send(msg)
					prompt()

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
    main_loop(s)

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
	main_loop(conn)

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
