from secrets import token_bytes

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
iv = b"vectinitializare"
k=b"thisisamasterkey"
#v=b"a secret message"
path0 = "/tmp/ktoa.fifo"
os.remove(path0)
os.mkfifo(path0)
v=token_bytes(16)  #Generez o cheie random
print(v)
cipher = Cipher(algorithms.AES(k), modes.CBC(iv)) # folosesc doar pentru AES, apelez functia cu cate 16 bytes ,CBC din functie nu este utilizat
encryptor = cipher.encryptor()
key = encryptor.update(v) + encryptor.finalize()    #criptez cheia cu MasterKey k
print(key)
fifo0 = open(path0, "wb")   #trimit key catre A
fifo0.write(key)
fifo0.close()