#ctf encryption challenge

from socket import *
from threading import Thread


#listen params
port = 31337
host = "0.0.0.0"

max_threads = 20

def randomString(size):
    return "".join(choice(string.ascii_letters + string.digits) for _ in range(size))


def client(clientsock, addr):
    return 0


if __name__=='__main__':
    listen_addr = (host, port)
    listensock = socket(AF_INET, SOCK_STREAM)
    listensock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    
    listensock.bind(listen_addr)
    listensock.listen(max_threads)
    
    while True:
       clientsock, addr = listensock.accept()
    
