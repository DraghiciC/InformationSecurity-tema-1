import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
mode=""
iv = b"vectinitializare"
k=b"thisisamasterkey"
path2 = "/tmp/atob.fifo"
path = "/tmp/intclt.fifo"
path3 = "/tmp/atobkey.fifo"
path4 = "/tmp/btoa.fifo"
os.remove(path4)
os.mkfifo(path4)

fifo2 = open(path2, "r")   #primesc modul de operare
for line in fifo2:
    mode=line
fifo2.close()

fifo3 = open(path3, "rb")   #primesc key de la A
for line in fifo3:
    key=line
fifo3.close()

cipher = Cipher(algorithms.AES(k), modes.CBC(iv))  #decriptez key
decryptor = cipher.decryptor()
a = decryptor.update(key) + decryptor.finalize()
key=a
print("key =  ",key)

fifo4 = open(path4, "w")   #trimit confirmarea
fifo4.write("received")
fifo4.close()
message=""
print(mode)
fifo = open(path, "rb")
for lin in fifo:
    line=line+lin
if mode=="CBC":  # CBC
    while line:
        l=line[:16]
        line=line[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        a = decryptor.update(l) + decryptor.finalize()
        v = bytes([_a ^ _b for _a, _b in zip(a, iv)])
        iv=l
        message=message+v.decode('ascii')
else:   # OFB
    l = line[:16]
    line = line[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    iv = encryptor.update(iv) + encryptor.finalize()
    v = bytes([_a ^ _b for _a, _b in zip(l, iv)])
    while line:
        l=line[:16]
        line=line[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        iv = encryptor.update(iv) + encryptor.finalize()
        v = bytes([_a ^ _b for _a, _b in zip(l, iv)])
        message = message + v.decode('ascii')
fifo.close()
print(message)