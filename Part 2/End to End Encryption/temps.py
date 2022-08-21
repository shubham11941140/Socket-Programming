from _thread import start_new_thread
from os.path import dirname, realpath
from socket import error, socket

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
)

server_password = "81079406b13ba43243d9ca233f5de29d"
server_password = bytes.fromhex(server_password)


def encrypt(plaintext_bytes):
    CURR_DIR = dirname(realpath(__file__))
    alicePubKey = load_pem_public_key(
        open(CURR_DIR + "/client-rsapub.pem", "rb").read(), default_backend())
    ciphertext_bytes = alicePubKey.encrypt(
        plaintext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return ciphertext_bytes


def decrypt(ciphertext_bytes):
    CURR_DIR = dirname(realpath(__file__))
    alicePrivKey = load_pem_private_key(
        open(CURR_DIR + "/server-rsapvt.pem", "rb").read(),
        server_password,
        default_backend(),
    )
    d = alicePrivKey.decrypt(
        ciphertext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return d


ServerSocket = socket()
host = "127.0.0.1"  # localhost
port = 1235
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except error as e:
    print(str(e))

print("Waiting for a Connection..")
ServerSocket.listen(5)
mapping = {}


def forward(message, source, target):
    message = f"{source}|{message}"
    mapping[target].sendall(encrypt(message.encode()))


def increaseThreadCount():
    global ThreadCount
    ThreadCount += 1


def decreaseThreadCount():
    global ThreadCount
    ThreadCount -= 1


def getThreadCount():
    return ThreadCount


def threaded_client(connection):
    while True:
        data = connection.recv(2048)
        if not data:
            print(f"\n[*] Disconnected from {connection.getpeername()}")
            connection.close()
            decreaseThreadCount()
            print(f"Total clients connected: {getThreadCount()}")
            break
        data = decrypt(data).decode()
        reply = ""
        try:
            target, message = data.split("/")
            ip, port = target.split(":")

            port = int(port)
            target = (ip, port)
            if target not in mapping:
                reply = "[*] Server Error: Cannot find specified target client"
            else:
                source = connection.getpeername()
                forward(message, source, target)
        except:
            reply = "[*] Parse Error: Invalid Input Format"

        if reply != "":
            connection.sendall(encrypt(str.encode(reply)))


while True:
    Client, address = ServerSocket.accept()
    print("\n[*] Connected to: " + address[0] + ":" + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    increaseThreadCount()
    mapping[address] = Client
    print(f"Total clients connected: {ThreadCount}")
ServerSocket.close()
