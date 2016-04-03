from socket import *
import random
import string
from easyCrypto import cipher

#length of plain text message
MESSAGE_LENGTH=40


#add to start and end of message then encrypt.
#so user knows when they have found the correct password
KNOWN_MSG_START=b"#$!PASS="
KNOWN_MSG_END=b"=WORD!$#"

#key range
MIN_KEY=500
MAX_KEY=1000

def Handler(clientsock, addr):
    print(addr)
    print("connected")
    
    #generate the randm message and encrypt it
    message = KNOWN_MSG_START + randomString(MESSAGE_LENGTH) + KNOWN_MSG_END
    
    random.seed()
   
    cipher_key = random.randint(MIN_KEY, MAX_KEY)
    crypted_message = cipher(message, cipher_key)
    
    clientsock.send(crypted_message + b'\n')
    
    #wait for an answer
    
    
    
    
    #check the answer 
    

    if True: #timedOut()
        clientsock.send(b'Too Slow\n')

        clientsock.shutdown(SHUT_RDWR)
        clientsock.close()


def randomString(size):
    random.seed()
    msg = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
    
    return bytes(msg, "ascii")

