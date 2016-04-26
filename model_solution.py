#! /bin/env python3
# model solution to the CTF challenge
# for the administrator only

from Crypto.Cipher import AES
import base64
import socket
from easyCrypto import decipher
import constants

from time import time

if __name__=='__main__':
    connection = ("127.0.0.1", constants.port)
    
    print("Start: " + str(time()))
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        #connect
        client.connect(connection)
        
        while True:
            response = client.recv(1000)
            if not response:
                continue
            else:
                if response[-1] == ord('\n'):
                    # remove new line from the end
                    response = response[:-1]
                break
        
        print("Received: " + str(response, "ascii"))
        
        #decrypt
        start_key = constants.MIN_KEY
        end_key = constants.MAX_KEY
        
        start_of_msg = str(constants.KNOWN_MSG_START, "ascii")
        end_of_msg = str(constants.KNOWN_MSG_END, "ascii")
        
        key = 0
        
        for i in range(start_key, end_key):
            test = decipher(response, i)
            
            if test.startswith(start_of_msg) and \
            test.endswith(end_of_msg):
                #key found
                
                key = i
                
                break
        
        if key == 0:
            client.close()
            raise Exception("Key not found")
        
        # extract out the important message
        secret = test[len(start_of_msg): -1 * len(end_of_msg)]
        
        secret = bytes(secret, "ascii")
        
        plaintext = constants.KNOWN_MESSAGE + \
        bytes([0] * (16 - len(constants.KNOWN_MESSAGE)))
        
        # prepare the AES
        AES_IV = str(key) + str(0).zfill(16 - len(str(key)) )
        
        suite = AES.new(secret, AES.MODE_CBC, AES_IV)
        
        # encrypt using AES
        cipher = suite.encrypt(plaintext)
        
        # base64 encode and send
        cipher = base64.b64encode(cipher)
        
        client.send(cipher + b"\n")
        
        # wait for an answer
        while True:
            response = client.recv(100)
            if not response:
                continue
            else:
                if str(response, "ascii") == "Success!!!\n":
                    # passed the challenge
                    print("Yay! we won.")
                
                else:
                    client.close()
                    print("Gay, we lost.")
                    exit(1)
                break
        
    except Exception as e:
        print("An error occurred")
        print(e)
        raise Exception(e)
        
        exit(-1)

    client.close()
    print("Finish: " + str(time()))
    


