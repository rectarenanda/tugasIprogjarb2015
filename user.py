import sys
import socket
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10001)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
while True:
# Send data
	message = raw_input("Anda : ")
	print >>sys.stderr, 'sending'
	sock.send(message)
# Look for the response
	#amount_received = 0
	#amount_expected = len(message)
	while True:
		data = sock.recv(1024)
		#amount_received += len(data)
		print >>sys.stderr, 'Teman Anda : "%s"' % data
		if data:
			reply = raw_input("Anda : ")
			sock.send(reply)
		else:
			break
#finally:
#	print >>sys.stderr, 'closing socket'
	sock.close()
