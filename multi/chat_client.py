# chat_client.py

import sys
import socket
import select
 
def chat_client():

    host = 'localhost'
    port = 9000
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
    while 1:
    	data = s.recv(4096)
    	sys.stdout.write(data)
	pesan = data.split(' ', 1 )
	if pesan[0]=='User' or pesan[0]=='Selamat' :
		s.send(raw_input(""))
	else:
		break
    sys.stdout.write(''); sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
         
        for sock in ready_to_read:             
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    sys.stdout.write(''); sys.stdout.flush()     
            
            else :
                # user entered a message
                #msg = sys.stdin.readline()
                s.send(raw_input(""))
                sys.stdout.write(''); sys.stdout.flush() 

if __name__ == "__main__":

    sys.exit(chat_client())
