import random

def easyCrypto(message, key):
    
    crypted = ""
    
    for c in message:
        
        random.seed()
        
        s = (c + key)
        
        left = (s & 0xff00)
        right = (s & 0x00ff) << 8        
        
        c1 = left | random.randint(0,0xff)
        c2 = right | random.randint(0,0xff)
        
        crypted = crypted + "." + str(c1) + "." + str(c2)
        
    return bytes(crypted, "ascii")

def decipher(ciphertext, key):
    plain = ""
    
    ciphertext = str(ciphertext, "ascii")
    
    values = ciphertext.split(".")
    
    values = values[1:]
    
    for i in range(int(len(values)/2)):
    
        left = int(values[i *2]) & 0xff00
        right = int(values[i*2 + 1]) & 0xff00
        right = right >> 8
        
        c = ((left | right) - key)
        plain += chr(c)
    
    return plain


message = b'Hello'

cipher = easyCrypto(message, 653)
print(cipher)

for i in range(600, 779):
    print(decipher(cipher, i))


