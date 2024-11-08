import socket       #To handle sockets
import threading    #To handle multiple clients

"""
Main Functions of server.py:
* handle_clients    -> assign nickname, broadcast message, handle client messages
* broadcast_message -> send message to all connected clients
* start_server      -> start the server and accept new clients
"""

#___________Create a new dictionary called clients__________#
clients: dict[socket.socket, str] = {}
#clients in this case is a dictionary that binds each clients socket to a nickname(str). For example -> 12345: "Onur"

#___________Handle all connected clients______________#
def handle_client(client_socket, client_address): #Expects client socket and adress as arguments
    nickname = client_socket.recv(1024).decode("utf-8")
    #Decode the nickname recieved from from client.py
    clients[client_socket] = nickname
    #Assign the nickname to the client_socket in the clients list
    print(f"[🎉[SERVER] - User '{nickname}' has joined from {client_address[0]} on port {client_address[1]}]")
    #Present the IP and port in tuple format in which 0 is the ip and 1 is the port number. Doing this to present the adress in a more readable way
    broadcast_message(f"{nickname} has joined the chat!", client_socket)
    #Neat printout for better readability

    #As long as the client is connected
    while True:
        #Try the following:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            #Take(receive) message from client and decode the message from bytes to string

            if not message:
                break
            #If there is no message, break the cycle/loop

            print(f"[📩[CHAT] - Message from {nickname}]: {message}")
            #Print out the decoded message
            broadcast_message(message, client_socket)
            #Broadcast it to all other clients

        #If the try does not work, print out the following
        except:
            print(f"[⚠️[CHAT] - Oops! Lost connection with: {nickname} - ({client_address})]")
            break

    #Close the client socket's connection
    del clients[client_socket]  # Remove unnecessary clients from the list to make space for new ones. del because clients is a dict
    client_socket.close()  # Closing client socket
    print(f"[👋[CHAT] - {nickname} has left the chat]") #Print out in the server chat
    broadcast_message(f"{nickname} has left the chat.", client_socket) #Broadcast it to all conencted clients

#______Sending message to all connected clients_______#
def broadcast_message(message, sender_socket):
    print("[📢[BROADCAST] - Sending message to all Users]")
    #Announce that a brodcast is being sent
    for client in clients:
        if client != sender_socket:  #Loop through and avoid echoing the message back to the original sender
            try:
                client.send(message.encode("utf-8"))
                #Send it to all other connected clients
            except:
                client.close()
                del clients[client] #Del; because clients is a dictionary and not a list!
                print("[🚫[BROADCAST] - Could not reach a user, removing them]")
                #If the try doesn't work, close the client socket and remove the client from the list

#___________Start the server and accept new clients__________#
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Create a new socket object called server_socket. Use STREAM for TCP connection
    server_socket.bind(("127.0.0.1", 1234))
    #Bind the socket object to the localhost and port 1234
    server_socket.listen()
    #"Pick up the phone" / Listen for incoming connections

    print("[🚀[SERVER] - The server is now live and listening on port 12345! 🌍]")
    # Neat printout to show that the server is running

    while True:
        client_socket, client_address = server_socket.accept()
        #As long as the servers running(True), accept new connections
        print(f"[🌍[SERVER] - New connection established with {client_address} 🌍]")
        #More neat messagesto make it easier to understand

        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()
        #Create a new thread for each client to handle multiple connections simultanousesly

if __name__ == "__main__":
    start_server()
    #Start the server