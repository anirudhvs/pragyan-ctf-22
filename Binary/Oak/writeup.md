# Oak

## Analysis

### Opening in Ghidra

![Main function](./images/ghidra_main.png?raw=true "Main function")

`main` function expects one command-line argument (flag) which is passed to the `check` function and the returned value is checked if it's true` of `false` if it's `true` then we have got the correct flag.

![Check function](./images/ghidra_check.png?raw=true "Check function")

`check` function takes one parameter, which is passed to `conv` function that returns the array of `long`, then there is a loop that goes through each element of that array and checks if `xor` of that element and `Oak.t(index * index)` (index of that element) is equal to the corresponding element in `Oak.data` if all of them are equal then we get the `true` else we get `false`.

![Check function](./images/ghidra_conv.png?raw=true "Check function")

`conv` function takes one `string` (our input) and creates an array of `long` with the same length as that `string`, then for each `character` in this `string`, it shifts that `character` 8 bit left and add the `character` next to it and store it to the `long` array that was created earlier, and for the last element it adds the first `character` in that `string`.

![Check function](./images/ghidra_t.png?raw=true "T function")

`t` function takes one `integer` parameter (say `len`) it creates the array of `len` length and initializes all of its value to -1 and finally returns the `t_helper` function called with `len` and created array as parameter.

![T_helper function](./images/ghidra_t_helper.png?raw=true "T_helper function")

It's a recursive function with two params, it calls the smaller version of the input until the base case is reached, the second parameter is used for memoization of already appeared cases, `python` version of `t` and `t_helper` can be written as...

```python
mem = {}
def t(n):
    if n in mem.keys():
        return mem[n]
    
    if n == 0:
        mem[0] = 0
        return mem[0]
    if n == 1:
        mem[1] = 1
        return mem[1]
    if n == 2:
        mem[2] = 3
        return mem[2]
    
    mem[n] = 3 * t(n - 1) - 3 * t(n - 2) + t(n - 3)
    return mem[n]
```

## Reversing

We can get each element in the `long` array returned by `conv` function by simply doing `xor` between `data[i]` and `t(i * i)` for `i` ranging from 0 to `data.length`, then we can get the first 8 bits of `long` array which will be our flag, we already have the `t` function we only need the `data` array.

With `javap -verbose Oak` we can get additional information about that class, upon analysis we can see under the `Constant pool` section there is a bunch of numbers with `long` datatype are present this might be our `data` array.

```text
   ...
   #57 = Long               28767l
   #59 = Long               24418l
   #61 = Long               25470l
   #63 = Long               29771l
   #65 = Long               26355l
   #67 = Long               31349l
   #69 = Long               13032l
   #71 = Long               30456l
   #73 = Long               14663l
   #75 = Long               27592l
   #77 = Long               8916l
   #79 = Long               29409l
   #81 = Long               7348l
   #83 = Long               17474l
   #85 = Long               5124l
   #87 = Long               3345l
   #89 = Long               49357l
   #91 = Long               61058l
   #93 = Long               65159l
   #95 = Long               53773l
   #97 = Long               67886l
   #99 = Long               72426l
  #101 = Long               103728l
  #103 = Long               158125l
  #105 = Long               179542l
  #107 = Long               166504l
  #109 = Long               212101l
  #111 = Long               282674l
  #113 = Long               320873l
  #115 = Long               329272l
  #117 = Long               400021l
  #119 = Long               479881l
  #121 = Long               535081l
  #123 = Long               599886l
  #125 = Long               662294l
  #127 = Long               731441l
  #129 = Long               831284l
  #131 = Long               947032l
  #133 = Long               1021482l
  ...
```

## [Complete exploit](./exploit.py "Exploit")
