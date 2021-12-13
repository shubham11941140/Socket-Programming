#include<stdio.h>
#include<stdlib.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<unistd.h>
#include <arpa/inet.h>

#define MAXLINE 1024  
#define PORT 8000

int main(){

  int socketDescriptor = socket(AF_INET, SOCK_DGRAM, 0);
  int number;
  int addressLength;
  char message[MAXLINE];

  struct sockaddr_in  serverAddress,clientAddress;
  serverAddress.sin_family = AF_INET;
  serverAddress.sin_addr.s_addr=INADDR_ANY;
  serverAddress.sin_port=htons(PORT);

  bind(socketDescriptor,(struct sockaddr*)&serverAddress,sizeof(serverAddress));

  printf("\nServer Started ...\n");

  while(1){
    printf("\n");
    addressLength = sizeof(clientAddress);

    number = recvfrom(socketDescriptor,message,MAXLINE,0,(struct sockaddr*)&clientAddress,&addressLength);

 printf("\n New Connection from client %s:%d \n ", inet_ntoa(clientAddress.sin_addr), ntohs(clientAddress.sin_port)); 
    printf("\n Client's Message: %s ",message);

    if(number<1)
      perror("send error");

      sendto(socketDescriptor,message,number,0,(struct sockaddr*)&clientAddress,addressLength);
  }
  return 0;
}
