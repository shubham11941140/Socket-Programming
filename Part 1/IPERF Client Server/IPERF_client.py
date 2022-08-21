# Import the necessary libraries

from datetime import datetime as dt
from decimal import Decimal
from random import choice, randint

# Import the necessary functions from the socket library
from socket import AF_INET, SOCK_DGRAM, socket, timeout
from string import ascii_lowercase, digits
from time import sleep

from matplotlib.pyplot import grid, plot, show, subplot, title, xlabel, ylabel

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
UDP_client_socket = socket(family=AF_INET, type=SOCK_DGRAM)

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


# A function that reduces the interval to 90 % of it's initial value
def new_interval(interval_value):

    # Calculate 10 % of the interval value
    to_be_lost = Decimal(interval_value / 10)

    # Remove it from the current value
    new_interval_value = Decimal(interval_value - to_be_lost)

    # As 10 % is removed from the initial interval, 90 % is left
    return new_interval_value


# To store the Average Throughput values after each second
AVG_THROUGHPUT = []

# To store the Average Delay values after each second
AVG_DELAY = []

# To store the Time Scale each second
TIME = []

# To store the number of seconds passed
count_seconds = 0

# It will essentially store the amount of delay time before transmission of a packet in the next second
# Since there is no delay initially, set to ZERO
delta = 0

# Send the message to the server using created UDP socket iteratively
# This loop will iterate over time in seconds and will increment time till all packets are not tranferred
while msg_total > 0:

    # Since we have no more packets to be transferred, we can stop the packet transfer
    if msg_total == 0:

        # Stop the packet transfer
        break

    # Increment time as we have moved to the next second to transmit the packets
    count_seconds += 1

    # Print appropriate message to the user
    print("Second", count_seconds, ":")

    # To store the Average Delay Time value
    avg_delay = 0

    # Count of packets that have completed a round trip and not been dropped
    packets_success = 0

    # This stores the time from where one second starts to send the loop
    second_start = Decimal(dt.now().timestamp())

    # Send each packet of that particular second one after the other iteratively
    # Transmit packets as long as the second is not over
    # Difference of current timestamp and starting timestamp must not exceed ONE
    while Decimal(dt.now().timestamp()) - second_start <= 1:

        # The condition where the delay to send the current packet exceeds ONE
        if delta > 1:

            # As the delay was more than one second we need to sleep for the whole second
            tosleep = 1

            # Reduce the delay by one second
            delta -= 1

            # As we wait for the whole second on account of delay, no packet is sent in this second
            # Print appropriate message to the user
            print("No packet will be sent in this second")

        else:

            # Set the sleep value to the delay
            tosleep = Decimal(delta)

        # Wait/Sleep for the delay to complete
        sleep(float(tosleep))

        # Since we have no more packets to be transferred, we can stop the packet transfer
        if msg_total == 0:

            # Stop the packet transfer
            break

        # Since we have skipped the whole second, we cannot transfer any packets
        if tosleep == 1:

            # Stop the packet transfer
            break

        # Send message to server
        # Send a random message of a random fixed length
        # It is useful as each message to the server is a distinct string
        client_msg = "".join([
            choice(ascii_lowercase + digits) for _ in range(randint(10, 20))
        ]).encode()

        # Send the message as an appropriate byte stream to the server
        UDP_client_socket.sendto(client_msg, server_IP_address_port)

        # Estimate the current timestamp to put a timestamp of sending on the packet
        # It marks the sending time of the echo message
        send_time_stamp = Decimal(dt.now().timestamp())

        # As we have sent a packet, we decrement the packets left to be sent
        msg_total -= 1

        # Receive the reply packet from the server
        try:

            # Try to receive message from the server
            server_msg = UDP_client_socket.recvfrom(buffer_size)

            # Print appropriate message to the user
            print("Received message:", server_msg[0].decode())

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
        round_trip_time = Decimal(receive_time_stamp - send_time_stamp)

        # Since packet has a Round Trip Time and has not been dropped
        # It has successfully returned
        packets_success += 1

        # Every packets Round Trip Time contributes to the Average Delay in the network
        avg_delay += Decimal(round_trip_time)

        # As we need to send echo messages at a given interval within each other
        # We hold the echo message till the interval is complete
        # If Round Trip Time exceeds interval, send the packet immediately
        # This will essentially store the delay of the next packet from the previous
        sleeptime = Decimal(max(interval - round_trip_time, 0))

        # As packet's Round Trip Time is estimated, we need to change the interpacket interval
        # Setting the current interval to the new interpacket interval, for the next packet
        # Above user-defined function specifies the change in this interval size
        interval = new_interval(interval)

        # The time which is over in this particular second
        passtime = Decimal(Decimal(dt.now().timestamp()) - second_start)

        # Wait for the interpacket interval to complete before sending the next packet
        # Sleep for the time which is left to send the next packet

        # The time for this second has aldready exceeded the deadline
        if passtime > 1:

            # Store the remaining delay to be carried over to the next second
            delta = Decimal(tosleep)

            # Move to the next second immediately
            break

        # The case if the delay is so high that it is moving over to the next second and we have time leftover in this second
        if passtime + sleeptime > 1 and passtime <= 1:

            # Set the sleep value to the rest of the second
            tosleep = Decimal(1 - passtime)

            # Store the remaining delay to be carried over to the next second
            delta = Decimal(sleeptime - (1 - passtime))

        # We have time in the current second to complete the delay
        else:

            # Set the sleep value to the delay
            tosleep = Decimal(sleeptime)

        # Wait/Sleep for the delay to complete
        sleep(float(tosleep))

    # The situation where the socket slept for the whole second and no packet could be transferred
    # Since there is no successfull packet whose RTT is calculated successfully, there is no delay
    if packets_success == 0:

        # As there is no RTT of any packet, no delay is estimated due to which average delay stays ZERO
        # It is not estimated, so we can safely return ZERO to the user
        avg_delay = 0

    else:

        # As we need to find the Average Delay,
        # We divide by the total number of packets successfully transferred
        avg_delay /= packets_success

    # The Average Throughput is given by the total data transferred by the total time passed (in bytes per second)
    # The total data transferred is the successful packets transferred multiplied by the data carried by each packet
    # Since we need to calculate Average Throughput every one second, we don't need to explicitly divide by 1
    # As the size of the buffer is taken in bytes, no change in unit is required
    # Since the same packet is transferred from client and vice-versa, the data transferred is twice (hence the factor of TWO)
    avg_throughput = packets_success * buffer_size * 2

    # Print appropriate message to the user
    print("The Average Throughput is", avg_throughput, "bytes/seconds")

    # Print appropriate message to the user
    print("The Average Delay is", avg_delay, "seconds")

    # Append for plotting average throughput
    AVG_THROUGHPUT.append(avg_throughput)

    # Append for plotting average delay
    AVG_DELAY.append(avg_delay)

    # Append for plotting time scale
    TIME.append(count_seconds)

# Plotting the graph
# Create TWO Horizontal subgraphs to show both the plots

# Create a Subplot for Throughput
subplot(1, 2, 1)

# Plot the Average Throughput in bytes per second on the Y-axis, Time scale in seconds on the X-axis
# Color of the plot is Red
plot(TIME, AVG_THROUGHPUT, "red")

# Label the X-axis in the subplot with the Time scale in seconds
xlabel("Time (in seconds)")

# Label the Y-axis in the subplot with the Average Throughput in bytes per second
ylabel("Average Throughput (bytes/seconds)")

# Label the graph as Y-axis vs X-axis
title("Average Throughput (bytes/seconds) vs Time (in seconds)")

# Make a grid out of the graph to give better approximation
grid(True)

# Create a Subplot for Delay
subplot(1, 2, 2)

# Plot the Average Delay values in seconds on the Y-axis, Time scale in seconds on the X-axis
# Color of the plot is Blue
plot(TIME, AVG_DELAY, "blue")

# Label the X-axis in the subplot with the Time scale in seconds
xlabel("Time (in seconds)")

# Label the Y-axis in the subplot with the Average Delay in seconds
ylabel("Average Delay (in seconds)")

# Label the graph as Y-axis vs X-axis
title("Average Delay (in seconds) vs Time (in seconds)")

# Make a grid out of the graph to give better approximation
grid(True)

# Display the graph to the user
show()

# Print appropriate message to the user
print("Graph Plotting is Complete")

# Print appropriate message to the user
print("Finished sending, Terminating the connection...")

# Send the message to exit to the server, to terminate the process
UDP_client_socket.sendto("exit".encode(), server_IP_address_port)

# Receive the termination message from the server
# Indicates that the server has closed the connection
exit_msg = UDP_client_socket.recvfrom(buffer_size)

# Print appropriate message to the user
print(exit_msg[0].decode("utf-8"))
