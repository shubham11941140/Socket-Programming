import sys
from os import _exit
from os.path import dirname, realpath
from socket import error, socket
from threading import Thread

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
)

client_password = "21c2904902c86e0cd990adce85c9f871"
client_password = bytes.fromhex(client_password)


def encrypt(plaintext_bytes):
    CURR_DIR = dirname(realpath(__file__))
    alicePubKey = load_pem_public_key(
        open(CURR_DIR + "/server-rsapub.pem", "rb").read(), default_backend())
    ciphertext_bytes = alicePubKey.encrypt(
        plaintext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    # return ciphertext_bytes.hex()
    return ciphertext_bytes


def decrypt(ciphertext_bytes):
    CURR_DIR = dirname(realpath(__file__))
    alicePrivKey = load_pem_private_key(
        open(CURR_DIR + "/client-rsapvt.pem", "rb").read(),
        client_password,
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


ClientSocket = socket()
host = "127.0.0.1"
port = 1235

print("Waiting for connection")
try:
    ClientSocket.connect((host, port))
except error as e:
    print(str(e))


def PrintMessage():
    # for message in iter(lambda: ClientSocket.recv(1024).decode(), ''):
    while True:
        message = ClientSocket.recv(1024)
        if len(message) > 0:
            message = decrypt(message).decode()
        else:
            print("\nDisconnected from Server. Exiting...")
            ClientSocket.close()
            _exit(0)
        if "|" in message:
            source, message = message.split("|")
            print(f"\nRecieved a message from {source}: \n{message}")
            print("\nEnter target address and message: ", end="")
        else:
            print(f"\n{message}\n")
            print("\nEnter target address and message: ", end="")


background_thread = Thread(target=PrintMessage)
background_thread.daemon = True
background_thread.start()

print(
    f"Connected!\nThis client address: {ClientSocket.getsockname()[0]}:{ClientSocket.getsockname()[1]}\n"
)
while True:
    Input = input("\nEnter target address and message: ")
    ClientSocket.send(encrypt(Input.encode()))
    if Input == "quit":
        print("Quitting...")
        ClientSocket.close()
        sys.exit()
