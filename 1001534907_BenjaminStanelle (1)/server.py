"""
Benjamin Stanelle
CSE 4344
1001534907
03/19/2021
"""
# Import socket module
import socket
#from socket import *
# Import thread module
import threading
import time
import sys

# Create a TCP server socket
HEADER = 64 #lets the server know how many bytes the client is sending
    #ip address will change based on local network
FORMAT = 'utf-8' #encoding
DISCONNECT_MESSAGE = 'DISCONNECTED'
    
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #makes a  new socket, ipv4, with a family
    
    # Assign a port number
serverPort = 8080
    
SERVER= socket.gethostbyname(socket.gethostname()) #gets the network ip automatically
    
address= (SERVER, serverPort)
    # Bind the socket to server address and server port
    
serverSocket.bind(address) #binds the address to this socket so anything that hits that goes to that ip address goes to that socket
    
connections= [] #used for connection information
    
    
  

def start():    #handles new connections and distributes then where they need to go
    serverSocket.listen(5) #server running and listening with buffer of 5
    print(f"[LISTENING] Server is listening on {SERVER} port: {serverPort}")
    while True:
        conn, addr = serverSocket.accept() #waits for new connection then stores ip address and port it came from
        try:
            thread= threading.Thread(target= handle_client, args= (conn, addr)) #pass new connection on new thread to handle client
            thread.daemon = True
            thread.start()
            
            
            connections.append(conn)    #append current connection info
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}", end='')
        except KeyboardInterrupt:
            print("Keyboard Interrupt. Connection closed, exiting.")
            conn.close()
            sys.exit(0)
            

def handle_client(conn, addr):  #handles individual connect between client and server 1:1
    print("\n[NEW CONNECTION]\n")
    try:
        message = conn.recv(1024).decode('utf-8') #receives message from client argv[3]
        f = open(message,'r')   #opens file and puts in buffer
        print("File requested: ", message)
        outputdata = f.read()

        #adding connection information
        connections_str= "".join(str(connections[len(connections)-1]))
        connections_str+= "".join("\nladdr is Host address and port (server side)\nraddr is client address and port")
        connections_str+= "".join("\nHost Name: ")
        connections_str+= "".join(socket.gethostname())
        print(connections_str) #print connection info on server side
        
        conn.send("HTTP/1.1 200 OK\r\n\r\n".encode(FORMAT)) #sending data and connection info
        conn.send(connections_str.encode(FORMAT))
        conn.send(str(outputdata).encode(FORMAT))
        
        print("[CONNECTION CLOSED]")
        conn.close() #close current connection and cleanly disconnect
    except IOError:
        # Send HTTP response message for file not found
        conn.send("HTTP/1.1 404 Not found\r\n\r\n".encode(FORMAT))
        conn.send(connections_str.encode(FORMAT))
        conn.send("<html><head></head><body><h1>404 Not found</h1></body></html>\r\n".encode(FORMAT))
        conn.close()

print("[STARTING] server is starting...")
try:
    start()
except KeyboardInterrupt:
    print("Keyboard Interrupt, server closed.")
    sys.exit(0)





