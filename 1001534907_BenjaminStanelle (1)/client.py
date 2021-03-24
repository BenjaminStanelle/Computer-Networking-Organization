"""
Benjamin Stanelle
CSE 4344
1001534907
03/19/2021
"""
import socket
import time
import sys
import os
from os import path

def main():
    HOST= socket.gethostbyname(socket.gethostname())  #might have to be hard coded.
    PORT= 8080
    #ip address will change based on local network
    FORMAT = 'utf-8' #encoding
    FILE_NAME= "test2.html"
    
    
    if len(sys.argv) >= 4: #testing if file name, host ip and port are specified, if not uses defaults
        HOST= check_server_name(sys.argv[1])
        PORT= check_port_number(sys.argv[2])
        FILE_NAME= check_file(sys.argv[3])
            
    elif len(sys.argv) == 3:
        HOST= check_server_name(sys.argv[1])
        PORT= check_port_number(sys.argv[2])
        print("User hasn't provided a filename. Default filename is used.\n")
    elif len(sys.argv) == 2:
        HOST= check_server_name(sys.argv[1])
        print("User hasn't provided a port number. 8080 is used.\n")
        print("User hasn't provided a filename. Default filename is used.\n")
    else:
        print("User hasn't provided any arguments. Default values are used.\n")
    
        
    ADDR= (HOST, PORT)  
    
    client_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)#creates cleitn socket
    print("Client has been established")
    #server_add=()
    try:
        client_socket.connect(ADDR) #tries connecting to server using ip and port specified or default
    except:
        print("Error, incorrect host address and port inputted.")
        client_socket.close() 
        sys.exit(0)
    
    
    send_time = time.time()            #start timer
    client_socket.send(FILE_NAME.encode(FORMAT)) #sends file name to server
    try:
        httpmessage= client_socket.recv(1024)  #receives corresponding message erorr or success
        connection_info=client_socket.recv(1024)  
        data=client_socket.recv(4096)
    except:
        print("Did not receive data from the server correctly.")
        client_socket.close()
        sys.exit(0)
    recv_time = time.time()
    
    file=open("copy_" + FILE_NAME, "w")  #makes new file and stores data in it
    file.write(data.decode(FORMAT))
    file.close()
    
    RTT = recv_time - send_time          #printing
    print("Code: ", httpmessage.decode(FORMAT))
    print("Connection Information: ", connection_info.decode(FORMAT))
    print("Data received by the client is:\n", data.decode(FORMAT))
    print("\nRTT: ", RTT)
    
    client_socket.close()

def check_server_name(name):
    if name == 'localhost' or name == '127.0.0.1' or name==socket.gethostbyname(socket.gethostname()):
        return socket.gethostbyname(socket.gethostname())
    else:
        print("Server name provided is not localhost or 127.0.0.1. Using local server by default.\n")
        return socket.gethostbyname(socket.gethostname())
    
def check_port_number(port):
        try:
            PORT = int(sys.argv[2])
        except:
            print("Given port number not acceptable. Using port 8080\n")
        return PORT
    
def check_file(file):
    if os.path.isdir(file):
        print("Given file name is a directory, using default file test.html.")
        file_name= "test.html"
        return file_name
    elif os.path.exists(file) and os.path.isfile(file):
        return file
        
    else:
        file_name= "test.html"
        print("Given file name does not exist, using default file test.html")
        return file_name

try:
    main()
except KeyboardInterrupt:
    print("Keyboard Interrupt on client side, exitting...")
    sys.exit(0)
    