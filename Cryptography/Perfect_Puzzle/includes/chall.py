from Crypto.Util.number import getPrime, bytes_to_long
from random import randint
from flag import flag

def getprime(N):
    a = randint(0, N)
    return getPrime(a)

def invdivsum(a):
    ret = 0
    for i in range(a):
        if a % (i+1) == 0:
            ret += 1/(i+1)
    return ret

p = getprime(1024)
q = getprime(1024)
n = p*q
e = 65537
flag_int = bytes_to_long(flag.encode())
CipherText = pow(flag_int, e, n)
Xemu = getprime(1024)
Alice = p + Xemu ** 2
Bob = q * Xemu
sum = Xemu*(Xemu+1) >> 1
Result = invdivsum(sum)
print(CipherText, Alice, Bob, Result)
