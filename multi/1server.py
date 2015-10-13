# chat_server.py
 
import sys
import socket
import select

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9000
dict = {}


def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
    dict[server_socket] = "server"
    print "Chat server started on port " + str(PORT)
 
    while 1:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
		welcome = "Selamat datang di chatroom, silahkan ketikkan username anda. \n Username: "
		error = "User sudah digunakan, silahkan cari username lain. \n Username: "		
		sockfd.sendto(welcome, addr)
		while 1:		
			user = sockfd.recv(20)
			if user in dict.values():
				sockfd.sendto(error, addr)
			else:
				dict [sockfd] = user
				sockfd.sendto('Ketik \'help\' untuk melihat perintah apa saja yang tersedia\nSilahkan memulai mengetik pesan anda\n', addr)
				broadcast(server_socket, sockfd, "%s entered our chatting room\n" % (user))
				break
		print "Client (%s, %s) connected" % addr
             
            # a message from a client, not a new connection
            else:
                # process data recieved from client, 
                try:
                    # receiving data from the socket.
		    err = "Maaf, perintah yang anda masukkan salah.\nSilahkan mengetik \'help\' untuk melihat perintah yang ada\n"
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        # there is something in the socket
                        #broadcast(server_socket, sock, "\r" + dict[sock] + " " + data)  
			part = data.split(' ', 1 )
			command = part[0]
			if command == "all":
			     msg = part[1]
			     broadcast(server_socket, sock, "\r" + dict[sock] + ": " + msg + "\n")
			elif command == "to":
			     part2 = part[1].split(' ', 1)
			     uid = part2[0]
			     msg = part2[1]
			     if uid in dict.values():
			     	to(server_socket, sock, uid, "\r" + dict[sock] + ": " + msg + "\n")				
			     else :
				sock.send('Username tidak tersedia\nKetik \'to username_tujuan pesan\' untuk mengirimkan pesan pribadi\nKetik \'list\' untuk mengetahui user yang tersedia\n')
			elif command == "list":
			     daftar(sock)
			elif command == "logout":
			     logout(sock)
			elif command == "help":
			     sock.send('Perintah yang tersedia:\n1.Send to all\n \'all pesan\'\n2.Send to user tertentu\n \'to username_tujuan pesan\'\n3.Daftar member\n \'list\'\n4.Bantuan (untuk menampilkan pesan ini)\n \'help\'\n5.Logout\n \'logout\'\n')
			else :
			     sock.send(err)
                    else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                        # at this stage, no data means probably the connection has been broken
			broadcast(server_socket, sock, "\n" + dict[sock] + " is offline\n")
			del dict[sock]

                # exception 
                except:
                    broadcast(server_socket, sock, "\n" + dict[sock] + " is offline\n")
		    del dict[sock]
                    continue

    server_socket.close()
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

#sendto
def to (server_socket, sock, uid, message):
     for user in dict.values():
	#send to certain user
	if user != "server" and user != dict[sock]:
	     for sck in dict.keys():
		if dict[sck] == uid:
			break
     try :
	sck.send(message)     		
     except :
        # broken socket connection
        socket.close()
        # broken socket, remove it
        if socket in SOCKET_LIST:
             SOCKET_LIST.remove(socket)

def daftar (sock):
     for user in dict.values():
	if user != "server":
	     sock.send(user + "\n")
     sock.send("--------------\n")

def help (sock):
     sock.send()

def logout (sock):
     if sock in SOCKET_LIST:
	sock.close()         
	SOCKET_LIST.remove(sock)
        broadcast(server_socket, sock, "\n" + dict[sock] + " is offline\n")
	del dict[sock]

if __name__ == "__main__":

    sys.exit(chat_server())
