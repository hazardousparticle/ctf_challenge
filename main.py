#ctf encryption challenge

from socket import *
from threading import Thread

import clientHandler


#listen params
port = 33333
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
        
        print("listener started on port: " + str(port) +"\n")
        
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
            print("\nTerminating CTF Server\n")
            
            for index, thread in enumerate(client_threads):
                thread.join()
                print("Thread closed: " + str(index))
            break
            
    listensock.close()
    exit(0)
