from os.path import dirname, realpath

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_key_pairs(secret_bytes):
    # Generate an RSA Keys
    private_key = rsa.generate_private_key(public_exponent=65537,
                                           key_size=2048,
                                           backend=default_backend())
    public_key = private_key.public_key()

    # Get current working directory
    CURR_DIR = dirname(realpath(__file__))

    # Save the RSA key in PEM format
    with open(CURR_DIR + "/private_key.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(
                    secret_bytes),
            ))

    # Save the Public key in PEM format
    with open(CURR_DIR + "/public_key.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            ))


# A 16 byte password in hex
password = "21c2904902c86e0cd990adce85c9f871"
generate_key_pairs(bytes.fromhex(password))
