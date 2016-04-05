#ctf encryption challenge

from socket import *
from threading import Thread

import clientHandler


#listen params
port = 31337
host = "0.0.0.0"

max_threads = 20

if __name__=='__main__':
    
    try:
        listen_addr = (host, port)
        listensock = socket(AF_INET, SOCK_STREAM)
        listensock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 0)
        
        listensock.bind(listen_addr)
        listensock.listen(max_threads)
        
        client_threads = []
        
        print("listener started\n")
        
    except Exception as e:
        print(e)
        exit(-1)
        
    while True:
        try:      
            clientsock, addr = listensock.accept()
            t = Thread(target = clientHandler.Handler, args = (clientsock, addr))
            t.start()
            client_threads.append(t)
        except KeyboardInterrupt:
            print("\nTerminiating CTF Server\n")
            
            for threads in client_threads:
                threads.join()
            break
            
    listensock.close()
    exit(0)
