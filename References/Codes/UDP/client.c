#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define MAXLINE 1024
#define PORT 8000

int main(){
  int serverDescriptor = socket(AF_INET, SOCK_DGRAM, 0);
    int addressLength;
  
  char sendMessage[MAXLINE],recvMessage[MAXLINE];
  printf("\n Enter message :");
  fgets(sendMessage,sizeof(sendMessage),stdin);
  
  struct sockaddr_in serverAddress;
  serverAddress.sin_family = AF_INET;
  serverAddress.sin_addr.s_addr = INADDR_ANY;
  serverAddress.sin_port = htons(PORT); 
 
  addressLength = sizeof(serverAddress);
 
  sendto(serverDescriptor,sendMessage,MAXLINE,0,(struct sockaddr*)&serverAddress,addressLength);
  recvfrom(serverDescriptor,recvMessage,MAXLINE,0,NULL,NULL);
 
  printf("\nServer's Echo : %s\n",recvMessage);

  return 0;
}
