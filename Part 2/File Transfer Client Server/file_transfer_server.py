# Import the necessary libraries

# Import the necessary functions from the socket library
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, error, socket
from sys import exit
from time import sleep


# Recursive function to try to bind to the socket
def bind_socket():

    # Try to complete the binding of the socket
    try:

        # Appropriate message is displayed
        print("Binding the Port:", port)

        # Bind to the specified host and port
        s.bind((host, port))

        # Since it is the server socket, it will listen
        s.listen(5)

    # Socket is unable to bind to the specific socket address
    except error as msg:

        # We seek to try binding again
        # Appropriate message is displayed
        print("Socket Binding error", msg)

        # Seek to retry
        # Appropriate message is displayed
        print("Retrying...")

        # Wait for an interval of 5 seconds for the function to end
        sleep(5)

        # Retry binding by calling the same function recursively
        bind_socket()


# Host is initialised
host = ""

# Standard port is initialised
port = 8888

# Uninitialised socket at server
s = None

# Create the server socket
try:

    # Try to create the server socket with any IP address and TCP Stream
    s = socket(AF_INET, SOCK_STREAM)

# Unable to create server socket
except error as msg:

    # Appropriate message is displayed
    print("Socket creation error:", msg)

    # Since we are not able to normally bind to the socket
    # We will forcibly bind to the socket

    # SOL_SOCKET manipulates the current socket in use
    # SO_REUSEADDR forcefully attaches to the address of the same socket
    # 1 is a BOOL value for True which sets the forceful attachment to True
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Bind the socket to the specified host and port using the above user-defined function
bind_socket()

# Binding is complete which indicates the server is listening
# Appropriate message is displayed
print("Server Listening...")

# Accept the socket connection from the client connection
conn, address = s.accept()

# Appropriate message is displayed
print("Connection has been established! |", "IP", address[0], "| Port",
      address[1])

# Connection has been established which allows to proceed with the file transfer to client

# Open the file which needs to be sent in read mode
f = open("test_file.txt", "rb")

# Read the file line by line
l = f.read(1024)

# Read as long as there is data left in the file
while l:

    # Send the file data line by line to client
    conn.send(l)

    # Read the next line in the file
    l = f.read(1024)

# As we have fully read the file, we can close it
f.close()

# Wait for an interval of 5 seconds for the file to fully close
sleep(5)

# As all the file contents are sent, closing message is sent
# This is important as it will tell the client to close the connection
conn.send(str.encode("Thank you for connecting"))

# Appropriate message is displayed
print("Done sending")

# Close the connection
conn.close()

# Close the socket at server
s.close()

# Exit the server program
exit()
