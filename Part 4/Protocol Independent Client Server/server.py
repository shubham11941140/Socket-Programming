# Import the necessary libraries

from os import _exit

# Import the necessary functions from the socket library
from socket import AF_UNSPEC, SOCK_STREAM, getaddrinfo, socket

# Collect the user input and inform the default inputs
host = input(
    "Enter host (Default host = ip6-localhost) (Enter localhost for IPv4 hostname): "
)  # localhost or ip6-localhost
port = input("Enter port (Default port = 8000): ")  # 8000

# If host input is not entered, set to default value
if host == "":
    host = "ip6-localhost"

# If port input is not entered, set to default value
if port == "":
    port = 8000

# Uninitialised socket at server
ServerSocket = None

# Iterate through the list of tuples containing information about socket(s) that can be created with the service.

# This is performed by getaddrinfo socket function https://en.wikipedia.org/wiki/Getaddrinfo

# AF_UNSPEC indicates that the caller will accept any protocol family and will not distinguish between IPv4 and IPv6
# SOCK_STREAM means that it is a TCP socket
for addrFamily, socketKind, protocol, cn, socketAddress in getaddrinfo(
        host, port, AF_UNSPEC, SOCK_STREAM):

    # We will try to establish a socket at the server
    try:

        # Socket is created at the server
        ServerSocket = socket(addrFamily, socketKind, protocol)

        try:

            # Try to bind the created socket at the specific socket address
            ServerSocket.bind(socketAddress)

            # As it is a socket at the server, it is open to listening from the client side
            ServerSocket.listen(1)

            # As socket is created and listening, it is in use
            print(
                f"Current socket in use: {addrFamily, socketKind, protocol, cn, socketAddress}"
            )

            # The socket has been established and is in use
            break

        except:

            # Socket is unable to bind to the specific socket address, hence close the connection
            ServerSocket.close()

            # As the socket is closed, there is no initialised socket
            ServerSocket = None

    # As we are unable to establish the socket at the server, the socket remains uninitialised
    except:

        # Socket remains uninitialised
        ServerSocket = None

# The case where we are unable to create a socket at the server, we need to exit
if ServerSocket is None:
    print("Cannot create connection with provided socket.")
    print("Exiting...")
    _exit(1)

# As socket is created at the server, accept the connection with the client
Client, address = ServerSocket.accept()

# Client connection is accepted and connection is established
print(f"\n[*] Connected to: {address[0]}:{address[1]}")

# Keep connection open till data is being received
while True:

    # Recive buffer of 1024 bytes from the Client side
    data = Client.recv(1024)

    # Close the connection when data receival has stopped
    if not data:

        # Connection is terminated at server end
        print(f"\n[*] Disconnected from: {address[0]}:{address[1]}")

        # Close the server socket
        Client.close()

        # Once the connection are closed from both sides
        # There is no data flow, so exit the loop
        break

    # Since there is data flow from the client
    # Send the same data back from the server to client
    Client.send(data)
