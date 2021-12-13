# Import the necessary libraries

from datetime import datetime as dt

from decimal import Decimal

from random import choice
from random import randint

from string import ascii_lowercase
from string import digits

from time import sleep

# Import the necessary functions from the socket library
from socket import AF_INET
from socket import socket
from socket import SOCK_DGRAM
from socket import timeout

# Set the server IP address and port tuple to a localhost and arbitrary value respectively
# Readjust this value if you want to communicate with another client on the same network
server_IP_address_port = ("127.0.0.1", 20001)

# Get the necessary inputs from the user

# User-defined - Number of echo messages
msg_total = int(input("Enter the number of echo messages to be sent: "))

# User-defined - Given interval
interval = Decimal(input("Enter the interval: "))

# User-defined - Given Packet Size
# As the size of the buffer is same as the packet size
buffer_size = int(input("Enter the packet size in bytes: "))

# Create a UDP socket at client side
UDP_client_socket = socket(family = AF_INET, type = SOCK_DGRAM)

# Set a standard timeout after which we move to the next packet in the case of a packet drop
UDP_client_socket.settimeout(1)

# To store the Average Round Trip Time value
avg_round_trip_time = 0

# Count of packets that have completed a round trip and not been dropped
packets_success = 0

# Calibration of Buffer Size
calibration_msg = ("C :" + str(buffer_size)).encode()

# Print appropriate message to the user
print("Calibrating the size of the buffer...")

# Appropriate message is sent to the server
UDP_client_socket.sendto(calibration_msg, server_IP_address_port)

# Receive acknowledgement message from the server to verify that the calibration is complete
ack_msg = UDP_client_socket.recvfrom(buffer_size)

# Send echo message to server using the created UDP socket
# Iterate through each message as they need to be sent one by one
# msg_count is the iterator that stores the number of echo messages sent
for msg_count in range(1, msg_total + 1):

    # Print appropriate message to the user
    print("Sending message for packet number", msg_count, "of size", buffer_size, "bytes")

    # Estimate the current timestamp to put a timestamp of sending on the packet
    # It marks the sending time of the echo message
    send_time_stamp = Decimal(dt.now().timestamp())

    # Send a random message of a random fixed length
    # It is useful as each message to the server is a distinct string
    client_msg = ''.join([choice(ascii_lowercase + digits) for _ in range(randint(10, 20))]).encode()

    # Send the message as an appropriate byte stream to the server
    UDP_client_socket.sendto(client_msg, server_IP_address_port)

    # Receive the reply packet from the server
    try:

        # Try to receive message from the server
        server_msg = UDP_client_socket.recvfrom(buffer_size)

    # Unable to receive the packet from the server
    # Case of the packet being dropped leading to a socket timeout
    except timeout:

        # Print appropriate message to the user
        print("Packet lost...\nSending next packet")

        # Move to the next datagram
        continue

    # Estimate the current timestamp to put a timestamp of receiving the packet
    # It marks the receiving time of the echo message
    receive_time_stamp = Decimal(dt.now().timestamp())

    # The difference of the receiving time stamp and sending time stamp gives Round Trip Time
    round_trip_time = receive_time_stamp - send_time_stamp

    # Print appropriate message to the user
    print("Message from Server is", server_msg[0].decode("utf-8"))

    # Print appropriate message to the user
    print("Round Trip Time for packet", msg_count, "is", round_trip_time, "seconds")

    # Every packets Round Trip Time contributes to the Average Round Trip Time
    avg_round_trip_time += round_trip_time

    # Since packet has a Round Trip Time and has not been dropped
    # It has successfully returned
    packets_success += 1

    # As we need to send echo messages at a given interval within each other
    # We hold the echo message till the interval is complete
    # If Round Trip Time exceeds interval, send the packet immediately
    sleep(float(max(interval - round_trip_time, 0)))

# Count the number of packets lost/dropped
# The difference of the total packets and successfully transferred packets
packets_lost = (msg_total - packets_success)

# Calculate the loss percentage for the dropped packets (in percentage)
packet_loss_percentage = Decimal(packets_lost / msg_total) * 100

# As we need to find the Average Round Trip Time,
# We divide by the total number of packets successfully transferred
avg_round_trip_time /= packets_success

# Print appropriate message to the user
print("Average Round Trip Time is", avg_round_trip_time, "seconds")

# Print appropriate message to the user
print("The number of packets dropped is", msg_total - packets_success)

# Print appropriate message to the user
print("The packet loss percentage is", packet_loss_percentage, "%")

# Print appropriate message to the user
print("Finished sending, Terminating the connection...")

# Send the message to exit to the server, to terminate the process
UDP_client_socket.sendto('exit'.encode(), server_IP_address_port)

# Receive the termination message from the server
# Indicates that the server has closed the connection
exit_msg = UDP_client_socket.recvfrom(buffer_size)

# Print appropriate message to the user
print(exit_msg[0].decode("utf-8"))
