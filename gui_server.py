
import socket
import struct
import pickle
import threading

# Choose a port that is free
PORT = 12345

# An IPv4 address is obtained for the server.
SERVER = 'localhost'

# Address is stored as a tuple
ADDRESS = (SERVER, PORT)

# the format in which encoding and decoding will occur
FORMAT = "utf-8"

# Lists that will contains all the clients connected to 
# the server and their names.
clients, names = [], []

# Create a new socket for the server
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# bind the address of the server to the socket
server.bind(ADDRESS)

# method for broadcasting
def broadcastMessage(message):
	for client in clients:
		client.send(message)

# function to start the connection
def startChat():

	print("server is working on " + SERVER)
	
	# listening for connections
	server.listen()
	
	while True:
	
		# accept connections and returns
		# a new connection to the client
		# and the address bound to it
		conn, addr = server.accept()
		conn.send("NAME".encode(FORMAT))
		name = conn.recv(1024).decode(FORMAT)
		
		# append the name and client to the respective list
		names.append(name)
		clients.append(conn)
		print(f"Name is :{name}")
		
		# broadcast message
		broadcastMessage(f"{name} has joined the chat!".encode(FORMAT))
		
		conn.send('you are now connected!'.encode(FORMAT))
		
		# Start the handling thread
		thread = threading.Thread(target = handle, args = (conn, addr))
		thread.start()
		
		# no. of clients connected to the server
		print(f"active connections {threading.activeCount()-2}")

# method to handle the incoming messages
def handle(conn, addr):

	print(f"new connection {addr}")
	
	while True:
		try:
			message = conn.recv(1024)  # receive message
			broadcastMessage(message)  # broadcast message
		except:
			index = clients.index(conn) # when client left chatroom
			clients.remove(conn)       # remove conn from clients tuple
			conn.close()
			name = names[index]
			broadcastMessage(f'{name} has left the chat room!'.encode('utf-8'))
			names.remove(name)		# remove client name from names tuple
			print(f'{name} has left the chat room!\n')
			print(f"active connections {threading.activeCount()-1}")
			break
	
# call the method to begin the communication
startChat()
