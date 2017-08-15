# 3connect

## About
3connect is a basic netcat clone allowing you to set up bind or reverse shells to your target. The added benefit is you can define basic commands to send and read from the target. I've also included plugin support if you would like to extend the functionality.

## Usage

- Set up listener

```
./3connect.py -l -H <local IP> -p <port to listen on>
```

- Connect to listener

```
./3connect.py -c -H <target IP> -p <target port>
```

Once connected, you can issues any command as usual. However, if you type `#`, 3connect will display a menu of options.

```lang=bash
root@kali:~/3connect# ./3connect.py -H 127.0.0.1 -c -p 444
[+] Connected to remote host.
id
uid=0(root) gid=0(root) groups=0(root)
#

		[+] What Platform?
		1. Windows
		2. Linux
		
[!]>2
1:	Spawn python shell
2:	Linux Basic
		uname -a | /etc/issue | ls -al /etc/cron.*
3:	Writable directories
4:	Environment Variables
5:	Network Info
6:	Installed Applications
7:	Find SETUID files
8:	Plugin - Check searchsploit for Kernel
```

Each options is loaded from the `linux.json` file for linux and the `windows.json` (Currently doesn't exist) for windows hosts. You are free to add your own options and commands to these files to expand the use.

## Plugin Support

You'll notice a test plugin in the `linux.json` file. 3connect will load a plugin if `plugin:` is found in the command for a particular option. It will then call that plugins main function and pass the socket to it. This is to allow you to extend the functionality, I have provided a basic (altthough useless) example in kernelsearch.py.
