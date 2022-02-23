# Secure lock 🔒

## Analysis

### `main`

function start with printing a lock (with 5 pins) with asking which pin to unlock, if we can enter the pin number if the pin number is not equal to 0x4 it prints `Invalid order..` and exits, otherwise it prompts us to input if the input provided is wrong it prints `wrong` and exits but if we provide correct input it asks for next pin to unlock until all the pins are open in proper order, once all are open it print `You have everything to get the flag!` and asks the flag, which it evaluates to prints `Correct!` or `Wrong..`.

By checking in `Ghidra` or `gdb` we can see after the first pin number and its input there is a call to the `check1` function that returns `true` or `false` depending upon the parameters, for a second there is a call to `check2` and so on till `check5` for 5th input, and for all of the parameters are the input we provide we just have to reverse all these functions to get the input and pass them lock to unlock it.

### `check1`

This function takes an `unsigned long` value as a parameter and puts it through a bunch of checks, and if it passes all the checks function return `true` otherwise `false`. It also calls `check_num_1` (checks if the number is prime or not) and `check_num_2` (checks if the number is Armstrong or not) function on the parameter, and their return value is checked if they are both `true`.

### `check2`

This function also takes an `unsinged long` as a parameter, it calls `srand` function with `0x8a1b791f` parameter, then there is a loop that runs exactly 6 times and calls `rand` function, the function makes a new number with output from `rand` and then calls `shuffle` function on parameter and checks if the new number is equal to the output of shuffle function and returns `true` if equals otherwise `false`.

### `check3`

This function has two parameters one char array and the second being its length first it calls `conv` function which just returns `base64` encoding of input, then there is the comparison with `strncmp` between our encoded string and a global char array which can be examined in `gdb` and is `"TWM1THlGN1l2SXhMeGVUWA=="`, it returns `true` if they are equal otherwise `false`.

### `check4`

This one also takes two parameters one char array, and second, being the length of that array, there are a lot of comparisons that define the input string.

### `check5`

This function takes one parameter of `unsigned long`, it creates two arrays of 6 elements, one of the arrays is initialized to certain numbers (say array name is `A`), another one is filled in for loop coming after it, which get the 8 bits of parameter performs operation between those 8 bits and array `A` using `xor` and `get` and `change` functions, once the second array is filled we create a new number using that array if new number constructed equals to `0xa8f24130a1ef` function return `true` else `false`.

### `check_flag`

This function takes a char array (flag) with all the input provided for `check1` to `check5`, there is also array of 32 elements, first it takes two strings from `check3` (`str1`) and `check4`(`str2`), then it goes through all the characters of input flag if `index` of character is odd it does xor between that character and `change(str2[(index - 1) / 2])` else it does xor between that character `change(str1[index / 2])`, here `change` function takes byte swaps its two nibbles, then there are four `for` loops each handle 8 bytes of input flag, first `for` loop does `xor` between index 0 to 7 of input flag to `unsigned long` (say `int1`) provided to `check1` one byte at time (by dividing `int1` by 256 index 0 will have last byte of `int1` and index 7 will have first byte of `int1`), same goes for second and third for loop but number are changed to number provided to `check2` and `check3`, and index are 8 to 15 and 16 to 23, last `for` loop does xor of index 24 to 31 of input flag with `0xff`, after all the for loops there compare if each character is equal to 32 length array (that was given in the function), if all are equal it return `true` otherwise `false`.

## [Complete exploit](./exploit.py "Exploit")
