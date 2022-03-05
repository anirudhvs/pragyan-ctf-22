# Blind Scout

## First Part

Here the flag is encoded with five different RSA key pairs, but two of them have a common divisor. Consider n1 and n2 as follows: n1 = p _ q1 n2 = p _ q2

Here p, q1, q2 are prime numbers. All we need to do is to check which of the two n values don't have GCD equal to 1. Calculate p, q (n1/p). Calculate the private key and decrypt the cipher corresponding to the n value.

```python
from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from base64 import b64decode
import sys

pub1 = RSA.importKey(open("pub1.pem", "rb").read(), passphrase=None)
e1 = pub1.e
n1 = pub1.n

pub2 = RSA.importKey(open("pub2.pem", "rb").read(), passphrase=None)
e2 = pub2.e
n2 = pub2.n

pub3 = RSA.importKey(open("pub3.pem", "rb").read(), passphrase=None)
e3 = pub3.e
n3 = pub3.n

pub4 = RSA.importKey(open("pub4.pem", "rb").read(), passphrase=None)
e4 = pub4.e
n4 = pub4.n

pub5 = RSA.importKey(open("pub5.pem", "rb").read(), passphrase=None)
e5 = pub5.e
n5 = pub5.n

myList = [(n1,e1),(n2,e2),(n3,e3),(n4,e4),(n5,e5)]
cipher = 'Z9jO5jqN9+fKNYJ14xA3QV96x4AlIIjOwoGSSq2D0G6ddMnKipNJkS2n0IS3blQAMym5dnzKC5MIetKikgozmzruuKDn2Xbkdv529Na2MXizJEMTxP/ioYzUFl2rJfg7xvyrNxEyPRWoJievmjpnum2pkrWAknAb+6Hj0Qv5yIo='
cipher = bytes_to_long(b64decode(cipher))

for i in range(len(myList)):
    for j in range(len(myList)):
        if (i!=j and GCD(myList[i][0],myList[j][0])!=1):
            p = GCD(myList[i][0],myList[j][0])
            q = myList[j][0]//p
            phi = (p-1)*(q-1)
            e = myList[j][1]
            n = myList[j][0]
            d = inverse(e4,phi)
            pt = pow(cipher, d, n4)
            pt = long_to_bytes(pt).decode('utf-8')
            print(pt)
            sys.exit()
```

## Second Part

Once we have the private key, we can decrypt the cipher. From the name of the question, we can guess that the binary numbers are braille (for blind people).

Decode the cipher from www.dcode.fr/braille-alphabet#f0
