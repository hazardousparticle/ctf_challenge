from socket import *
import random
import string

#length of plain text message
MESSAGE_LENGTH=40


#add to start and end of message then encrypt.
#so user knows when they have found the correct password
KNOWN_MSG_START=b"#$PASS="
KNOWN_MSG_END=b"=WORD$#"



def Handler(clientsock, addr):
    print(addr)
    print("connected")
    
    message = KNOWN_MSG_START + randomString(MESSAGE_LENGTH) + KNOWN_MSG_END
   
    
    #crypted_message = easyCrypto()
    
    
    clientsock.send(message + b'\n')


    message = b'Too slow\n'
    
    clientsock.send(message)

    clientsock.shutdown(SHUT_RDWR)
    clientsock.close()


def randomString(size):
    random.seed()
    msg = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
    
    return bytes(msg, "ascii")


