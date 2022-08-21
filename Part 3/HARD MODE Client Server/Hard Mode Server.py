from queue import Queue
from signal import SIGINT, SIGTERM, signal
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, error, socket
from sys import exit
from threading import Thread
from time import sleep

host = ""
port = 8888
sock = None

queue = Queue()
temp = [1]

client_connections = []
client_addresses = []
client_threads = []


def create_socket():
    global sock
    try:
        sock = socket(AF_INET, SOCK_STREAM)
    except error as msg:
        print("Socket creation error: " + str(msg))
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


def bind_socket():
    try:
        print("Binding the Port: " + str(port))
        sock.bind((host, port))
        sock.listen(5)
    except error as msg:
        print("Socket Binding error:" + str(msg) + "\n" + "Retrying...")
        sleep(5)
        bind_socket()


def quit_gracefully(signal=None, frame=None):
    for conn in client_connections:
        try:
            conn.shutdown(2)
            conn.close()
            sock.close()
        except Exception as msg:
            print("Could not close connection:" + str(msg))
    exit()


def accept_conn():
    while True:
        try:
            conn, addr = sock.accept()
            client_connections.append(conn)
            client_addresses.append(addr)
            conn.setblocking(1)
            t = Thread(target=send_client,
                       args=(client_connections[-1], client_addresses[-1]))
            t.daemon = True
            client_threads.append(t)
            t.start()
        except Exception as msg:
            print("Cannot accept connections: " + str(msg))
        print("Connection has been established with client: " + str(addr))


def work():
    accept_conn()
    queue.task_done()


def create_jobs():
    for x in temp:
        queue.put(x)
    queue.join()


def send_client(conn, addr):
    while True:
        command = conn.recv(2048)
        command_str = (command.decode("utf-8")).strip()
        if command == b"":
            break
        if command_str == "connections":
            output_str = clients()
        elif command_str[0:4] == "send":
            to_id = int(command_str[5])
            msg = command_str[7:]
            msg = f"FROM {addr}: " + msg
            to_conn = client_connections[to_id]
            to_addr = client_addresses[to_id]
            try:
                to_conn.send(str.encode(msg))
            except Exception as ex:
                print("Cannot send message to {} from {}: {}".format(
                    to_addr, addr, ex))
                continue
            output_str = "MESSAGE sent successfully to {}\n".format(to_addr)
        else:
            output_str = "Please enter correct command!"
        try:
            conn.send(str.encode(output_str))
        except Exception as ex:
            print("Cannot send status message to client: {} from server:= {}".
                  format(addr, ex))


def clients():
    clients = "CLIENTS\nCLIENT ID \tIP ADDRESS\t PORT\n"
    for i, conn in enumerate(client_connections):
        try:
            conn.send(str.encode(" "))
            data = conn.recv(2048)
            if data == b"":
                raise Exception("connection broken")
        except Exception as e:
            if i < len(client_connections):
                del client_connections[i]
            if i < len(client_addresses):
                del client_addresses[i]
            continue
        clients += f"{i}: \t{client_addresses[i][0]}\t{client_addresses[i][1]}\n"
    return clients


def main():
    create_socket()
    bind_socket()
    signal(SIGINT, quit_gracefully)
    signal(SIGTERM, quit_gracefully)
    t = Thread(target=work, args=())
    t.daemon = True
    t.start()
    create_jobs()


main()
