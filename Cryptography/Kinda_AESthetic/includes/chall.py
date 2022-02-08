from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os, sys

KEY = os.urandom(16)
IV = os.urandom(16)

def encrypt(msg):
    msg = pad(msg, 16)
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    encrypted = cipher.encrypt(msg)
    encrypted = encrypted.hex()
    msg = IV.hex() + encrypted
    return msg

def decrypt(msg, iv):
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(msg), 16).decode()
    return decrypted

def parse(inp):
    iv = bytes.fromhex(inp[:32])
    msg = bytes.fromhex(inp[32:])
    msg = decrypt(msg,iv)
    return msg

secrets = {
    'abrac': 'iloveyou',
    'sudo': REDACTED, # ;)
    'gg': REDACTED,
    'yeager': 'ironman'
}

flag = REDACTED
token = REDACTED

def lookup(inp):
    try:
        cipher = AES.new(KEY, AES.MODE_CBC, inp[:16])
        inp = unpad(cipher.decrypt(inp[16:]), 16)
    except:
        return 'idek'
    try:
        name = inp.decode()
        assert name[:len(token)] == token
        name = name[len(token):]
        return secrets[name]
    except:
        return 'idk'

print('Here is an encrypted token for you:')
print(encrypt(token.encode()))

while True:
    try:
        inp = input()
        try:
            user = parse(inp)
            assert user == 'gg'
            print('Welcome gg! Enter your secret passphrase:')
            inp = input()
            password = parse(inp)
            if password == secrets['gg']:
                print(flag)
                sys.exit(0)
            else:
                print(r'p_ctf{potato}')
        except:
            inp = bytes.fromhex(inp)
            print(lookup(inp))
    except:
        print('')
        sys.exit(0)

