from queue import Queue
from signal import SIGINT, SIGTERM, signal
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, error, socket
from sys import exit
from threading import Thread
from time import sleep

host = "localhost"
port = 8888
sock = None

queue = Queue()
temp = [1, 2]

commands = [
    "connections: Gives all the connections with server",
    "send <id> <message>: To send <message> to client <id>",
    "close: To close the connection with server",
]


def create_socket():
    global sock
    try:
        sock = socket(AF_INET, SOCK_STREAM)
    except error as msg:
        print("Socket creation error: " + str(msg))
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


def connect():
    try:
        sock.connect((host, port))
    except error as msg:
        print("Socket Connection error: " + str(msg))


def quit_gracefully(signal=None, frame=None):
    if sock:
        try:
            sock.shutdown(2)
            sock.close()
        except Exception as msg:
            print("Could not close connection:" + str(msg))
    exit()


def receive_work():
    receive_from_server()
    queue.task_done()


def send_work():
    send_to_server()
    queue.task_done()


def create_jobs():
    for x in temp:
        queue.put(x)
    queue.join()


def send_to_server():
    print("Enter any of the commands given below")
    for x in commands:
        print(x)
    print(">>>>>", end="")
    while True:
        command_str = input()
        if len(command_str) == 0:
            continue
        if command_str == "close":
            break
        command = str.encode(command_str)
        try:
            sock.send(command)
        except Exception as e:
            print(f"Unable to send message to server: {e} ")
            break
        sleep(1)


def receive_from_server():
    while True:
        try:
            data = sock.recv(2048)
        except Exception as ex:
            print("Communication error: %s\n" % str(ex))
            break
        data_str = data.decode("utf-8")
        if data == b"":
            break
        if data_str == " ":
            try:
                sock.send(str.encode(" "))
            except Exception as ex:
                print(f"Unable to send msg to server: {ex}")
                break
        elif data_str:
            print(data_str + "\n>>>>>", end="")


def main():
    create_socket()
    connect()
    signal(SIGINT, quit_gracefully)
    signal(SIGTERM, quit_gracefully)
    t1 = Thread(target=receive_work, args=())
    t2 = Thread(target=send_work, args=())
    t1.daemon = True
    t2.daemon = True
    t1.start()
    t2.start()
    create_jobs()
    sock.close()


main()
