from socket import *
import random
import string
from easyCrypto import cipher
from Crypto.Cipher import AES
import base64
import binascii
import signal
from time import sleep
from threading import Thread

#enable cheat mode:
cheats = False



#length of plain text message
MESSAGE_LENGTH=32


#add to start and end of message then encrypt.
#so user knows when they have found the correct password
KNOWN_MSG_START=b"#$!PASS="
KNOWN_MSG_END=b"=WORD!$#"

#key range
MIN_KEY=400
#keep the key + char less than 0x03ff
MAX_KEY=(0x03ff - ord('z'))

#message which must be AES'd
KNOWN_MESSAGE=b"Let Me In!"

#time limit
time_limit = 30

class TimeExpired(Exception): pass
#    def __init__(self, value):
#        self.value = value

#def timeOut(secs = time_limit):
#    sleep(secs)
#    raise TimeExpired("Too slow")


def Handler(clientsock, addr):
    print(str(addr) + " Connected")

    #generate the randm message and encrypt it
    message = randomString(MESSAGE_LENGTH)
    
    print(str(addr) +" secret: " + str(message, "ascii"))

    not_crypted = KNOWN_MSG_START + message + KNOWN_MSG_END
    
    random.seed()
    cipher_key = random.randint(MIN_KEY, MAX_KEY)

    if cheats:
        cipher_key = 777
        
    print(str(addr) + " key: " + str(cipher_key))
    
    crypted_message = cipher(not_crypted, cipher_key)
    
    clientsock.send(crypted_message + b'\n')

    #once the easy key is found and the message is decrypted,
    #the contestant must use the secret message as the key
    #to encrypt the string KNOWN_MESSAGE using AES-256 CBC.
    #the KNOWN_MESSAGE must be padded at the end with \x00's until its exactly 16 bytes
    #the AES IV will be a 16 byte string starting with the found key and then padded with '0's
    #once encrypted, the cipher text will be sent back base64-ed


    #wait for an answer
    
#    t = Thread(target = timeOut)
#    t.start()
    
    buffer_size = 500
    
    try:
        
        AES_IV = str(cipher_key) + str(0).zfill(16 - len(str(cipher_key)) )
        print(str(addr) + " AES IV expected: " + AES_IV)
        
        while True:
            response = clientsock.recv(buffer_size)
            
            if not response:
                continue
            else:
                print(str(addr) + " sends " + str(response, "ascii"))
                break


        #response must be base64 encoded.
        response = base64.b64decode(response)
        
        #decrypt the answer
        suite = AES.new(message, AES.MODE_CBC, AES_IV)
        
        #the contestant wins if i can decrypt their response and obtain KNOWN_MESSAGE
        plaintext = suite.decrypt(response)

        #still have time
        if plaintext == KNOWN_MESSAGE + bytes([0] * (16 - len(KNOWN_MESSAGE))):
            #success
            clientsock.send(b"Success!!!\n")
            print(str(addr) + " Successful\n")
        else:
            raise ValueError("Plaintext doesnt match")
    except (binascii.Error, ValueError):
        clientsock.send(b"Failure!!!\n")
        print(str(addr) + " Fail")
        pass
    except TimeExpired:
        clientsock.send(b'Too Slow!!!\n')
        print(str(addr) + " took too long\n")
        pass
    except OSError as e:
        print(str(e))
        print("Error\n")
        return
    
    #t.join()
    
    clientsock.shutdown(SHUT_RDWR)
    clientsock.close()
    
    print(str(addr) + " Socket closed")


def randomString(size):
    random.seed()
    msg = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
    
    if cheats:
        msg = "bEXihGB7Wn9XK6EMApXU8kZjNPatHa6n"
    
    return bytes(msg, "ascii")

