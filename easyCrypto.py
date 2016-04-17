import random
#from helperStuff import randomKey

#return encrypted message bytes
#args byte array, int
def cipher(message, key = 0):
    
    crypted = ""
    
    for c in message:
        
        random.seed()
        
        s = (c + key)
        
        # maximum of a standard char + key =  b0000 0011 1111 1111
        
        left = (s & (0x03 << 8)) >> 8
        
        right = (s & 0x00ff) << 8
        
        c1 = left | (random.randint(0,0x3fff) << 2)
        c2 = right | random.randint(0,0xff)
        
        c1 = c1 ^ key
        c2 = c2 ^ key
        
        crypted = crypted + "." + str(c1) + "." + str(c2)
        
    return bytes(crypted, "ascii")

#return plaintext message string
#args: string, int
def decipher(ciphertext, key):
    plain = ""
    
    ciphertext = str(ciphertext, "ascii")
    
    values = ciphertext.split(".")
    
    values = values[1:]
    
    for i in range(int(len(values)/2)):
    
        left = int(values[i *2]) ^ key
        left = (left & 0x0003) << 8
        
        right = int(values[i*2 + 1]) & 0xff00
        right = right ^ key
        right = right >> 8
        
        c = ((left | right) - key)
        
        if (c < 0 or c > 0x11000):
            #invalid char
            plain = ""
            break
        
        plain += chr(c)
    
    return plain

