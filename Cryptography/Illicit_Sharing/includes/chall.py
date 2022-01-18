from Crypto.Util.number import *
from sympy import nextprime
from random import randint

flag = r"p_ctf{redacted}"

def encrypt():
    p0 = getPrime(1024)
    q0 = getPrime(255)
    n0 = p0 * q0

    p1 = nextprime(p0)
    q1 = nextprime(q0)
    n1 = p1 * q1

    r0 = randint(0, 1 << 512)
    r1 = randint(0, 1 << 512)

    assert all([
        p1 ^ p0 < (1 << 512),
        q0.bit_length() == q1.bit_length(),
        n0.bit_length() == n1.bit_length()
    ])

    pt = bytes_to_long(flag.encode())
    ct0 = (pow(pt, p0, n0) + pow(r0, q0 - 1, n0)) % n0
    ct1 = (pow(pt, p1, n1) + pow(r1, q1 - 1, n1)) % n1

    output = f'n0 = {n0}'
    output += f'\nn1 = {n1}'
    output += f'\nct0 = {ct0}'
    output += f'\nct1 = {ct1}\n'

    return output


while input('Press E to encrypt: ') == 'E':
	output = encrypt()
	print(output)
