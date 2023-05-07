import random



def key_scheduling(key):
    sched = [i for i in range(256)]
    
    key_length = len(key)
    j = 0
    for i in range(256):
        j = (j + sched[i] + key[i % key_length]) % 256
        
        sched[i], sched[j] = sched[j], sched[i]
        
    return sched
    

def stream_generation(sched):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + sched[i]) % 256
        
        sched[i], sched[j] = sched[j], sched[i]
        
        yield sched[(sched[i] + sched[j]) % 256]        


def encrypt(text, key):
    text = [ord(char) for char in text]
    key = [ord(char) for char in key]
    
    sched = key_scheduling(key)
    key_stream = stream_generation(sched)
    
    ciphertext = ''
    for char in text:
        enc = str(hex(char ^ next(key_stream))).upper()[2:].zfill(2)
        ciphertext += enc
        
    return ciphertext
    

def decrypt(ciphertext, key):
    ciphertext = [int(ciphertext[i:i+2], 16) for i in range(0, len(ciphertext), 2)]
    key = [ord(char) for char in key]
    
    sched = key_scheduling(key)
    key_stream = stream_generation(sched)
    
    plaintext = ''
    for char in ciphertext:
        dec = str(chr(char ^ next(key_stream)))
        plaintext += dec
    
    return plaintext


if __name__ == '__main__':
    ed = input('Enter E for Encrypt, or D for Decrypt: ').upper()
    if ed == 'E':
        plaintext = input('Enter your plaintext: ')
        key = input('Enter your secret key: ')
        result = encrypt(plaintext, key)
        print('Result: ')
        print(result)
    elif ed == 'D': 
        ciphertext = input('Enter your ciphertext: ')
        key = input('Enter your secret key: ')
        result = decrypt(ciphertext, key)
        print('Result: ')
        print(result)
    else:
        print('Error in input - try again.')
