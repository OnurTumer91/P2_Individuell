import socket       #To handle sockets
import threading    #To handle simultaneous connections/send-recieve data
import sys          #Makes the terminal a bit more flexible

"""
Main functions of client.py:
* recieve messages  -> print them out
* send messages     -> take input from the user and send it to the server
* start_client      -> connect to the server and boot up threads to send/recieve data
"""

#______Takes messages from the server and prints them out________#
def receive_messages(client_socket): #Recieve message; expects a client socket as an argument
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            #decode the recieved message from bytes to string
            
            if message:
                sys.stdout.write("\r" + " " * 80 + "\r")
                #Clears the current input line with 80 spaces. /r moves cursor to the beginning of the line!
                #I use this because when client A is typing and recieves a message from client B the command line looks a bit weird. 
                #By using this I make sure that the command line looks clean at all times.
                print(f"[📥[INBOX] - New message]: {message}")
                #Display inc message

                sys.stdout.write("Type a message to send to the server: ") #writes the prompt directly to the terminal without adding a new line (unlike print())
                sys.stdout.flush() #forces the prompt to appear immediately

            else:
                break
            #If no message is recieved, break the loop

        except socket.error as e:
            print(f"[⚠️[INBOX] - Connection lost with the server: {e}]")
            client_socket.close()
            break
            #If the try doesn't work, close the client socket and break the loop

#_______________Client sending message to the server_____________#
def send_messages(client_socket, nickname): #Send messages; expects a client_socket and a nickname as arguments
    while True:
        message = input("Type a message to send to the server: ")
        #take input from the user, store it in message

        ###################################
        full_message = (f'{nickname}: {message}') #Adds nickname to the message, did not end up using this, but proud of it nonetheless.
        ###################################

        try:
            client_socket.send(message.encode('utf-8'))
            print(f"[📤[OUTBOX] - Message sent]: {message}")
            #send encoded message to the server
        except Exception as e:
            print(f"[🚫[OUTBOX] - Failed to send message: {e}")
            client_socket.close()
            break
            #If the try doesn't work, close the client socket and break the loop

#_Connect to the server and boot up threads to send/recieve data_#
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Create a new socket object that contains the client socket, define the socket as a TCP connection
    try:
        print("[🔄[CLIENT] - Trying to connect to the server...]")
        client_socket.connect(("127.0.0.1", 1234))
        print("[🎉[CLIENT] - Connected to the server successfully!]")
        #Try to establish a connection and print out sucessfull right after the connection is established

    except Exception as e:
        print(f"[❌[CLIENT] - Could not connect to the server: {e}]")
        return
        #If the try/connection doesn't work, print out the message and return

    #Choose a nick
    nickname = input("Choose a username: ")
    client_socket.send(nickname.encode("utf-8"))

    #Start threads to recieve/send messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket, nickname))
        

    receive_thread.start()
    send_thread.start()
    #Start the threads

if __name__ == "__main__":
    start_client()