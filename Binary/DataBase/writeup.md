# DataBase

## Analysis

With `checksec`, we can see that file hast RELRO disabled so there might be something to do with `global offset table`.

With `objdump -t database` we can get all the address in executable, and with address of main provided, we can calcuatate rest of the address needed for exploit.

There are a total of 4 options Show, Insert, Update, Remove, and Exit.

Here Show option calls the print_items function which will print all the available elements according to their `size` even if the string end by `\x00` it will print exactly the `size` number of character we can abuse this by changing `size` to a larger value in ( in update function ) and print the addresses that are not allocated to us.

There is also a `secret` function which calls `system('/bin/cat flag')`, So we have to call secret function somehow.

Update function can be used to change the `size` of any string and then override its value with the string of maximum `size` length, Here, the function doesn't allocate extra `size` it will override addresses on the heap (overflow) we can abuse this to override top header of the heap to arbitrary value ie., causing house of force vulnerability.

## Exploit

### Getting the address of heap

We can use heap metadata to get addresses on the heap. By allocating three `string` using `Insert` options the deleting last and then second last `string`, we will have the heap metadata stored where the second `string` was, which will be the address of third-string, and then increasing the `size` of the first string ( using Update function ) we can get the heap metadata available at second string by simply printing the first `string`, then we can allocate two more string, and third `string` this time will start at the address that we printed.

### Writing to arbitrary address using House of force

Once we get the address on the heap, we can get the address of the `secret` function and `GOT` entry of fflush/exit/read/atoi using `gdb`, and trick malloc to return the address of one of these and override them with the address of `secret` function so next time we call any of them we actually call secret function and get the `flag`.

We can calculate the offset size needed with the address we want to allocate and the heap address. Once we have that offset we can just pass that offset as `size` in the next insert call and then if we allocate another string using insert, the address we will get is the address we wanted malloc to return and we just simply override that address.

## [Complete exploit](./exploit.py "Exploit")
