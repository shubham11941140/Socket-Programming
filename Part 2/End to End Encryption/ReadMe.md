## Implemented an RSA Asymmetric encryption to encrypt the packets being transfered from server to client and client to server. 
### This prevents the person eavesdroping to know what messages are being transfered. This method preserves both privacy and authenticity of the server and client.  

#### File info:
**server.py** - Python3 code for server. To run it, execute `python3 server.py`  
**client.py** - Python3 code for client. To run it, execute `python3 client.py`  
**client-rsapub.pem** - Contains public key of client shared with server.  
**client-rsapvt.pem** - Contains private key of client. AES-256 CBC encrypted and can only be decrypted by `client.py`. Password to decrypt is given in `client.py`.  
**server-rsapub.pem** - Contains public key of server shared with client.  
**server-rsapvt.pem** - Contains private key of server. AES-256 CBC encrypted and can only be decrypted by `server.py`. Password to decrypt is given in `server.py`.  
**key_generator.py** - Generates public and private key pairs. You don't need to execute this file as keys are already provided. However, if you wish to change the keys, you can change the password in this file and generate new public and private key pairs. Make sure to rename the generated files corresponding to server and client and change those passwords in `client.py` and `server.py`  

#### File upload is one of the most important functionalities of a server. 
You provide your CV to a server for getting a job, upload your assignments to submit them on time, upload your profile photo on social media, store files in a cloud for backup, etc. People use file upload in their day to day lives for numerous reasons. I added this functionality to my server and client model. Not just that, these files being transfered are **end-to-end encrypted** by RSA to preserve privacy of user uploading file to the server. Currently supports text files. 

#### File info:
**source.txt** - Contains file that needs to be uploaded.  
**target.txt** - Contains file getting created after copy has been completed.  

#### How to execute code:
Run server.py by executing  
`$ python3 server.py`  
on terminal. It by default runs on port number 8000. So please make sure that 8000 is free before executing. Then run  
`$ python3 client.py`  
This will read every 256 bytes in source.txt, encrypt them using RSA and transfer them to server for security. Server will decrypt the bytes, convert them to text and store it in target.txt. Server acknowledges the recieved bytes by sending a direct messages. These acknowledgements are also **end-to-end encrypted**.
, I used the implementation in 1st question to encrypt/decrypt messages from a client to server and vice versa so that no one except the recipient can know what messages are being delivered to whome :-)

#### Input Format to code:
Input follows strict format-  
`destination_ipaddress:destination_port\Message to be transfered`  
For example, to send a message "Hello World" to 127.0.0.1, port number 8002, you need to write "127.0.0.1:8002/Hello World" without quotes. There are some characters that cannot be sent to client. Since : and / are used as a separators, they cannot be included as a part  of message. Also, | (pipe) also cannot be used as a character to be transfered because it is being used as a separator for source client and message by the server. Rest everything works well.

#### Some Features:
1. End-to-end encryption from client to server and server to client using RSA.  
2. As soon as client gets connected/disconnected, server shows a notification of client connected/disconnected with it's socket information.
3. Server shows current number of connected clients to it. This number gets updated as a new client connects or a connected client disconnects.  
4. As soon as your message gets delivered, it will show up on your terminal by the use of threading.  
5. If the server is terminated, all clients automatically disconnects from the server. Those clients exit gracefully and automatically on losing connection with the server.  
6. If a client wants to disconnect, you can press Ctrl+C to generate a KeyboardInterrupt or simple type "quit" without quotes to exit more gracefully.
