#worker thread for client connections

import socket
from easyCrypto import cipher
from Crypto.Cipher import AES
import base64
import binascii
from time import sleep
from threading import Thread, Event
import errno
from helperStuff import *
from constants import *


class Client(object):
    def __init__(self): #, self.clientsock, addr):
#        self.clientsock = clientsock
#        self.addr = addr
        self.timeOut_signal = Event()
        

    def timeOut(self, secs = time_limit):
        self.timeOut_signal.clear()
        sleep(secs)
        self.timeOut_signal.set()
        #TODO: fix this so that it aborts the sleep when the client handler closes

    def Handler(self, clientsock, addr):
        print(str(addr) + " Connected")

        #generate the randm message and encrypt it
        message = randomString(MESSAGE_LENGTH)
        
        print(str(addr) +" secret: " + str(message, "ascii"))

        not_crypted = KNOWN_MSG_START + message + KNOWN_MSG_END
        
        cipher_key = randomKey()

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
        
        t = Thread(target = self.timeOut)
        t.start()
        
        buffer_size = 500
        
        try:
            
            clientsock.setblocking(False)
            
            AES_IV = str(cipher_key) + str(0).zfill(16 - len(str(cipher_key)) )
            print(str(addr) + " AES IV expected: " + AES_IV)
            
            while True:
                if self.timeOut_signal.is_set():
                    raise TimeExpired()
                
                try:
                    response = clientsock.recv(buffer_size)
                    if not response:
                        continue
                    else:
                        if response[-1] == ord('\n'):
                            # remove new line from the end
                            response = response[:-2]
                        
                        print(str(addr) + " sends " + str(response, "ascii") +\
                        "\t(" + str(len(response)) + " bytes)")
                        
                        break
                except socket.error as e:
                    err = e.args[0]
                    if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                        #nothing received.
                        continue
                    else:
                        raise Exception(e)

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
                print(str(addr) + " Successful")
            else:
                raise ValueError("Plaintext doesnt match")
        except (binascii.Error, ValueError):
            clientsock.send(b"Failure!!!\n")
            print(str(addr) + " Fail")
            pass
        except TimeExpired:
            clientsock.send(b'Too Slow!!!\n')
            print(str(addr) + " took too long")
            pass
        except (Exception, OSError) as e:
            print(str(e))
            print("Error\n")
            return
        
        #t.join()
        
        try:
            clientsock.shutdown(socket.SHUT_RDWR)
        except OSError as e:
            err = e.args[0]
            if err == errno.ENOTCONN:
                #client left early
                print(str(addr) + " Got scared off and quit\n")
                pass
            else:
                raise Exception(e)

        clientsock.close()
            
        print(str(addr) + " Socket closed")

