# IPERF echo client and server

If you want to estimate the throughput and delay without the situation of packet loss,
then comment out lines 75 to 82 in the "IPERF_server.py" file
This will remove the case of artificial packet drop from the server end and give an output
not affected by packet drop

Run the server using:

    python3 IPERF_server.py

Run the client using:

    python3 IPERF_client.py

You will be prompted to provide number of echo messages, interval and packet size to be sent.

    For the number of echo message ENTER: Any positive integer greater than ZERO
    For Example: 100, 500, 1000

    For the interval: Enter a positive real number greater than ZERO
    For Example: 0.7, 1, 2
    (We keep the interval a little big in this case, as we are reducing interval size)
    (Since the interval size reduces within the function, keeping a moderate value will
    help understanding the packet transmission better, helping plot a more accurate
    throughput and delay graph)

    For the packet size: Enter a positive real number greater than TEN
    For Example: 64, 128, 256
    (Very small packets can cause hindrance in transmission of standard client server message)

PRESS ENTER to move onto the next line
