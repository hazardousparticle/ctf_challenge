from socket import *
import random
import string
from easyCrypto import cipher
from Crypto.Cipher import AES
import base64
from threading import Thread, Event
from time import sleep

#length of plain text message
MESSAGE_LENGTH=32


#add to start and end of message then encrypt.
#so user knows when they have found the correct password
KNOWN_MSG_START=b"#$!PASS="
KNOWN_MSG_END=b"=WORD!$#"

#key range
MIN_KEY=500
MAX_KEY=1000

#message which must be AES'd
KNOWN_MESSAGE=b"Let Me In!"

timeout = Event()

def timer(delay=30):
    timeout.clear()
    sleep(delay)
    timeout.set()



def Handler(self, clientsock, addr):
    print(addr)
    print("connected")

    #generate the randm message and encrypt it
    message = randomString(MESSAGE_LENGTH)

    crypted = KNOWN_MSG_START + message + KNOWN_MSG_END

    random.seed()

    cipher_key = random.randint(MIN_KEY, MAX_KEY)
    crypted_message = cipher(crypted, cipher_key)
    
    clientsock.send(crypted_message + b'\n')
    
    t = Thread(target = timer)
    t.start()

    #once the easy key is found and the message is decrypted,
    #the contestant must use the secret message as the key
    #to encrypt the string KNOWN_MESSAGE using AES-256 CBC.
    #the KNOWN_MESSAGE must be padded a the end with \x00's until its exactly 16 bytes
    #the AES IV will be a 16 byte string starting with the found key and then padded with '0's
    #once encrypted, the cipher text will be sent back base64-ed


    #wait for an answer
    response = b"message"
    
    #TODO: receive stuff
    
    
    if not timeout.is_set():
        #response must be base64 encoded.
        response = base64.b64decode(response)
        
        #decrypt the answer
        AES_IV = str(cipher_key) + str(0).zfill(16-len(cipher_key))
        suite = AES.new(message, AES.MODE_CBC, AES_IV)
        
        #the contestant wins if i can decrypt their response and obtain KNOWN_MESSAGE
        plaintext = suite.decrypt(response)

        #still have time
        if plaintext == KNOWN_MESSAGE + bytes([0] * (16 - len(KNOWN_MESSAGE))):
            #success
            clientsock.send(b"Success!!!\n")
            print(addr)
            print("successful\n")
        else:
            clientsock.send(b"Failure!!!\n")
    else:
        clientsock.send(b'Too Slow\n')

    t.join()
    clientsock.shutdown(SHUT_RDWR)
    clientsock.close()


def randomString(size):
    random.seed()
    msg = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
    
    return bytes(msg, "ascii")

