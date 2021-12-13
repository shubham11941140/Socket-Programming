# Import the necessary libraries

from random import choice
from random import randint

from string import ascii_lowercase
from string import digits

# Import the necessary functions from the socket library
from socket import AF_INET
from socket import socket
from socket import SOCK_DGRAM

# Set the server IP address and port tuple to a localhost and arbitrary value respectively
# Readjust this value if you want to communicate with another client on the same network
server_IP_address_port = ("127.0.0.1", 20001)

# Set the value of the size of buffer to the default value before it is changed by the user
buffer_size = 1024

# Create a UDP datagram socket with any IP address
UDP_server_socket = socket(family = AF_INET, type = SOCK_DGRAM)

# Bind to IP address and port
UDP_server_socket.bind(server_IP_address_port)

# Appropriate message is displayed
print("UDP server has binded and is waiting for client connection")

# Listen for incoming datagrams until the process is not exited
while True:

    # Split the incoming message from the client into the message and address
    msg, addr = UDP_server_socket.recvfrom(buffer_size)

    # Decode the byte stream to obtain the client message
    client_msg = msg.decode()

    # Appropriate message is displayed
    print("Message from the Client is", client_msg)

    # If the client message is to exit, then we will stop processing datagrams and terminate the process
    if client_msg == 'exit':

        # The appropriate message to end the connection, sent as a byte stream
        UDP_server_socket.sendto("Terminated the connection successfully.".encode(), addr)

        # Appropriate message is displayed
        print("Exiting...")

        # Exit the process of accepting datagrams
        break

    # The case where the server needs to change the size of the buffer obtained from the client end
    # C indicates it is a client message for calibrating
    if client_msg[0] == 'C':

        # Appropriate message is displayed
        print("The IP Address and port of the Client is", addr)

        # Obtain the updated size of the buffer from the message
        buffer_size = int(client_msg.split(':')[1])

        # Appropriate message is displayed
        print("Updated buffer size to", buffer_size, "bytes")

        # Send the appropriate reply message as a byte stream from the server to the client
        UDP_server_socket.sendto(("Buffer Size Calibrated at Server.").encode(), addr)

        # After calibration is performed at the server, move to the next datagram
        continue

    # Generate a random number from one to 100
    random_num = randint(1, 100)

    # Check any particular random number is a fixed constant
    if random_num == 50:

        # Next iteration of the loop
        # Skip sending the reply packet to the client from the server
        continue

    # Since we are generating a random number from 1 to 100 and the probability of that number == 50 is low
    # We get proability of a number in 100 numbers equal to 50 become 1/100
    # On average 1 in 100 packets will be dropped, as that particular packet will not be sent from server to client

    # Sending a reply to client
    # The reply is a random string of a random length, num is also randomly generated
    # It is useful as each reply to the client is a distinct string
    reply = ''.join([choice(ascii_lowercase + digits) for _ in range(random_num)]).encode()

    # Send the reply message as a byte stream from the server to the client
    UDP_server_socket.sendto(reply, addr)
