#ctf encryption challenge

from socket import *
from threading import Thread

from clientHandler import Client


#listen params
port = 37133 #TODO: make it custoizable using command line args
host = "0.0.0.0"
host6 = "::"

max_threads = 20
use_ip6 = False #TODO: autmatically detect this


if __name__=='__main__':
    
    if use_ip6:
        print("IPv6 is enabled.")
        listen_addr = (host6, port, 0, 0)
    else:
        listen_addr = (host, port)
        
    try:
        if use_ip6:
            listensock = socket(AF_INET6, SOCK_STREAM)
        else:
            listensock = socket(AF_INET, SOCK_STREAM)
        
        listensock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 0)
        
        listensock.bind(listen_addr)
        listensock.listen(max_threads)
        
        client_threads = []
        client_list = []
        
        print("listener started on port: " + str(port) +"\n")
        
    except Exception as e:
        print(e)
        exit(-1)
        
    while True:
        try:      
            clientsock, addr = listensock.accept()
            connectedclient = Client()
            client_list.append(connectedclient)
            t = Thread(target = connectedclient.Handler, args = (clientsock, addr))
            t.start()
            client_threads.append(t)
        except KeyboardInterrupt:
            print("\nTerminating CTF Server\n")
            
            for index, thread in enumerate(client_threads):
                thread.join()
                print("Thread closed: " + str(index))
            break
            
    listensock.close()
    exit(0)

