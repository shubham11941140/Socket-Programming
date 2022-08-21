# Import the necessary libraries

from os import _exit

# Import the necessary functions from the socket library
from socket import AF_UNSPEC, SOCK_STREAM, getaddrinfo, socket

# Collect the user input and inform the default inputs
host = input(
    "Enter host (Default host = ip6-localhost) (Enter localhost for IPv4 hostname): "
)  # localhost or ip6-localhost
port = input("Enter port (Default port = 8000): ")  # 8000
data = input("Enter the data to be sent (No default) (Please enter a value): ")

# As we need an input for the data, we cannot proceed till an input is not entered
while data == "":
    data = input("Please enter the data to be sent to server: ")

# Proceed after input has been received

# If host input is not entered, set to default value
if host == "":
    host = "ip6-localhost"

# If port input is not entered, set to default value
if port == "":
    port = 8000

# Uninitialised socket at client
ServerSocket = None

# Iterate through the list of tuples containing information about socket(s) that can be created with the service.

# This is performed by getaddrinfo socket function https://en.wikipedia.org/wiki/Getaddrinfo

# AF_UNSPEC indicates that the caller will accept any protocol family and will not distinguish between IPv4 and IPv6
# SOCK_STREAM means that it is a TCP socket
for addrFamily, socketKind, protocol, cn, socketAddress in getaddrinfo(
        host, port, AF_UNSPEC, SOCK_STREAM):

    # We will try to connect the client socket to the socket at the server
    try:

        # Socket is created at the client
        ServerSocket = socket(addrFamily, socketKind, protocol)

        try:

            # Try to Connect the socket to the socket address at the server
            ServerSocket.connect(socketAddress)

            # Able to connect to the server socket
            print(
                f"This client socket: {addrFamily, socketKind, protocol, cn, socketAddress}"
            )

            # The socket has been established and is in use
            break

        # Client socket is unable to connect to the server socket
        except:

            # Unable to connect, close the connection
            ServerSocket.close()

            # As the socket is closed, there is no initialised socket
            ServerSocket = None

    # As we are unable to establish the socket at the client, the socket remains uninitialised
    except:

        # Socket remains uninitialised
        ServerSocket = None

# The case where we are unable to create a socket at the client, we need to exit
if ServerSocket is None:
    print("Cannot create connection with provided socket.")
    print("Exiting...")
    _exit(1)

# As the socket has been initialised and we have connected it to the server
print(f"Sending to Server: {data}")

# We can start sending data from the client to the server
ServerSocket.send(data.encode())

# As the server is sending messages back to the client, it is received
data = ServerSocket.recv(1024)

# Reply from the server side is complete
print(f"Reply from Server: {data.decode()}")

# Close the socket connection at the client end
ServerSocket.close()
