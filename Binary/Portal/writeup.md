# Pragyan CTF 2022: Portal
## Write-Up

1) There is no input validation for the prompt "Enter coupon code:". So variables from the stack can be leaked through a format string attack.

2) Find out from which DWORD the flag starts in the leak base using gdb.

3) ```python3 -c 'for i in range(5,15): print(f"%{i}$p", end="")'```
      - The output of the above piece of code is used to fill in the prompt for the attck.

4) Convert the Hex output to ASCII and swapping endianness will reveal the flag.
      - You can use this online tool https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')Swap_endianness('Raw',8,true) for this.