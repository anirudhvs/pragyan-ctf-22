The first part is to do a padding oracle attack and decrypt the token.
Now we know the plaintext and ciphertext of the token so we can use it to manipulate the IV we provide.
Manipulate the IV to get gg's secret.
Again manipulate the IV to pass the username 'gg' and his password.

```py
from Crypto.Util.strxor import strxor
from Crypto.Util.Padding import pad, unpad
from pwn import remote

r = remote('example.xyz', '2222')

ct = r.recvlines(2)[-1].decode().strip()
iv = bytes.fromhex(ct[:32])
ct = ct[32:]
pt = [ord('.')] * 16

# padding oracle attack on one block of ciphertext
for i in range(15, -1, -1):
    niv = list(iv)

    for j in range(15, i, -1):
        niv[j] = pt[j] ^ iv[j] ^ (16 - i)

    for j in range(256):
        if j == iv[i] and i == 15:
            continue

        niv[i] = j
        nct = bytes(niv).hex() + ct
        r.sendline(nct.encode())

        res = r.recvline().decode().strip()
        if res != 'idek':
            pt[i] = j ^ (16 - i) ^ iv[i]
            print(bytes(pt))
            break

# getting the password
token = bytes(pt)
print(f'token: {unpad(token, 16).decode()}')

niv = strxor(iv, token)
target = pad(unpad(token, 16) + b'gg', 16)
niv = strxor(niv, target)
nct = niv.hex() + ct
r.sendline(nct.encode())

password = r.recvline().decode().strip()
print(f'password: {password}')

# passing the username
niv = strxor(iv, token)
niv = strxor(niv, pad(b'gg', 16))
nct = niv.hex() + ct
r.sendline(nct.encode())
r.recvline()

# supplying the password
niv = strxor(iv, token)
niv = strxor(niv, pad(password.encode(), 16))
nct = niv.hex() + ct
r.sendline(nct.encode())

flag = r.recvline().decode().strip()
print(f'flag: {flag}')

r.close()

#p_ctf{4_l1ttl3_p4d4tt4ck_h3r3_&4_l1ttl3_x0r_THERE}
```
