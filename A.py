from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

iv = b"vectinitializare"
k=b"thisisamasterkey"
mode="OFB"
#mode="CBC"
path0 = "/tmp/ktoa.fifo"
path1 = "/tmp/intclt.fifo"
#os.remove(path1)
os.mkfifo(path1)
path2 = "/tmp/atob.fifo"
#os.remove(path2)
os.mkfifo(path2)
path3 = "/tmp/atobkey.fifo"
#os.remove(path3)
os.mkfifo(path3)
path4 = "/tmp/btoa.fifo"

fifo2 = open(path2, "w")   #trimit modul de operare
fifo2.write(mode)
fifo2.close()

fifo0 = open(path0, "rb")   #primesc cheia de la KM
for line in fifo0:
    key=line
fifo0.close()

fifo3 = open(path3, "wb")   #trimit key primit de la server
fifo3.write(key)
fifo3.close()

cipher = Cipher(algorithms.AES(k), modes.CBC(iv))  #decriptez key
decryptor = cipher.decryptor()
a = decryptor.update(key) + decryptor.finalize()
key=a
print(key)

fifo4 = open(path4, "r")   #primesc confirmarea de la B
for line in fifo4:
    print(line)
fifo4.close()
message="this is a long string of characters so i can demonstarate that my program works"
fifo = open(path1, "wb")
if mode=="CBC":      #CBC
    while message:
        block=message[:16]
        message=message[16:]
        ba=bytes(block.ljust(16),'ascii')
        v=bytes([_a ^ _b for _a, _b in zip(ba, iv)])
        print(block)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv)) # folosesc doar pentru AES, apelez functia cu cate 16 bytes ,CBC din functie nu este utilizat
        encryptor = cipher.encryptor()
        iv = encryptor.update(v) + encryptor.finalize()
        fifo.write(iv)
else:       #OFB
    while message:
        block=message[:16]
        message=message[16:]
        print(block)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv)) # folosesc doar pentru AES, apelez functia cu cate 16 bytes ,CBC din functie nu este utilizat
        encryptor = cipher.encryptor()
        iv = encryptor.update(iv) + encryptor.finalize()
        ba=bytes(block.ljust(16),'ascii')
        v=bytes([_a ^ _b for _a, _b in zip(ba, iv)])
        print(v)
        fifo.write(v)
        v=bytes([_a ^ _b for _a, _b in zip(v, iv)])
        print(v)

fifo.close()
