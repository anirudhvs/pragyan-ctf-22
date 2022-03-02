# Pragyan CTF 2022: Classic

Working with the binary provided, it is python compiled binary which can be found by running `strings enc | grep py`.
Python script can be generated from this binary using 2 python packages pyinstxtractor, decompyle3 by running the following commands -

```
python3 pyinstxtractor.py enc
decompyle3 enc_extracted/enc.pyc
```

```
a = "ABCDEFGHIJ"
a1 = "abcd"
enc_a = "ABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJAB"
x = [1, 2, 3]
lst = []


def alg(a, k, lst, enc):
    l = len(k)
    r = [a[i::l] for i in range(l)]
    k1 = ''
    for i in k:
        k1 += str(ord(i))
    else:
        for i in range(l):
            i1 = 0
            e = ''
            for c in r[i]:
                i1 = ord(c) ^ ord(k[i]) ^ (i1 >> 2)
                e += chr(i1)
            else:
                r[i] = e

        else:
            k2 = (k1 * 6)[-3::-1]
            for i in range(len(k2)):
                v2 = k2[i]
                if 48 <= ord(v2) <= 51:
                    lst.append(((ord(enc[i]) ^ 0xe) - 0x2f) ^ 0x09)
                else:
                    if 52 <= ord(v2) <= 54:
                        lst.append((ord(enc[i]) ^ 0xF) + 0x1c)
                    else:
                        if 55 <= ord(v2) <= 57:
                            lst.append((ord(enc[i]) ^ 0xd) - 0x3e)
            else:
                lr = list(zip(*r))
                eflg = "".join(hex((1 << 8)+ord(i))[3:]
                             for i in "".join("".join(j) for j in lr))
                if lst == x and len(lst)!=0:
                    return 'Good Job'
                return 'Try again'


print(alg(a, a1, lst, enc_a))
```

We need to develop a decrypting algorithm for this. ```chars``` in the exploit, is the list formed by reversing the list ```r``` in the chall. 

It can be inferred from the last if statement that given set of numbers are the encryption of the encrypted flag. From the given array of numbers and encrypted key we can get the encrypted flag by reversing the XOR statements.
```
# Prints the encrypted flag from given encrypted list
def decrypt(a1, msg):
    for i in range(len(a1)):
        if 48 <= ord(a1[i]) <= 51:
            msg[i] = chr(((msg[i] ^ 0x09) + 0x2f) ^ 0xe)
        if 52 <= ord(a1[i]) <= 54:
            msg[i] = chr(((msg[i]) - 0x1c) ^ 0xF)
        if 55 <= ord(a1[i]) <= 57:
            msg[i] = chr(((msg[i]) + 0x3e) ^ 0xd)
    s = ""
    for i in msg:
        s += str(i)
    print(s)

x = [25, 46, -3, 73, 4, 86, 5, 52, -2, 86, 6, 48, 3, 88, 91, 2, 25, 53, -2, 55, -2, -1, 0, 53, 87, 0, 6, -2, 85, 52, 0, 2, 88, 89, 5, 73, 3, -3, 2, 1, -6, 25, 4, 83, 0, 48, 0, 89, 4, 48, 25, 88, 89, 4, 6,
     55, -1, 7, 1, 1, 25, 1, 85, 53, 6, 1, 87, 7, 0, 3, 86, 136, 6, 3, 2, 42, 4, 42, -1, 50, 7, 86, 2, 25, -4, 138, 3, 48, 25, 136, 90, 6, 25, 4, 1, 3, 0, -9, 25, 6, 89, 55, 2, -6, 87, 4, 0, 50, 84, 137, 4, 5]

decrypt('0791151174073560118079115117407356011807911511740735601180791151174073560118079115117407356011807911511740735601', x)
```

First 6 characters of the key a1 can be found using the flag format p_ctf. The other characters are found by reversing the encrypted key and find the difference between the two encrypted keys by encrypting the 6 characters separately. This can be found by reversing the initial for-else statement. 
```
def get_key(msg):
# Finding first 6 characters of key
    init = 'p_ctf{'
    keylen = [i for i in range(1, 56)]

    for l in keylen:
        key = ''
        chars = [chr(int(msg[x:x+2], 16))
                 for x in range(0, len(msg), 2)]
        def dif(A, n): return [tuple(A[i:i+n])
                                       for i in range(0, len(A), n)]
        chars = dif(chars, l)
        chars = list(zip(*chars))
        for i in range(min(len(init), len(chars))):
            key += chr(ord(chars[i][0]) ^ ord(init[i]))
        print(key)  # First 6 chars will be j5F/sw

#Finding the remaining characters
    key6 = 'j5F/sw'
    rev_key = '0791151174073560118079115117407356011807911511740735601180791151174073560118079115117407356011807911511740735601'
    l = (len(rev_key)//6)+1
    enck = rev_key[::-1]
    enck = enck[:l]
    print(enck)
    enc_key6 = ''
    for i in key6:
        enc_key6 += str(ord(i))
    print(enc_key6)
    print(enck[-4:])  # Prints last 4 ordinal values
    # Therefore second last is ord(70) --> F and last is ord(81) --> Q

print(get_key('1a6a255b150c73041e1c106e46016b34325a764251286f322c13220c0322196e0243375c074e2e0d35417a7c1c10122738102c45423d7b25'))
```

Now decrypt the encrypted flag which we got above with the original key found above as well. This is done by reversing the code after the encryption of encrypted flag.
```
def flag(msg, key):
    l = len(key)
    chars = [chr(int(msg[x:x+2], 16)) for x in range(0, len(msg), 2)]

    def dif(A, n): return [tuple(A[i:i+n])
                                   for i in range(0, len(A), n)]
    chars = dif(chars, l)
    chars = list(zip(*chars))
    for i in range(l):
        a = 0
        e = ''
        for j in range(len(chars[i])):
            if a == 0:
                a = ord(chars[i][j]) ^ ord(key[i]) ^ (a >> 2)
            else:
                a = ord(chars[i][j]) ^ ord(key[i]) ^ (
                    ord(chars[i][j-1]) >> 2)
            e += chr(a)
        chars[i] = e

    dflag = ''
    for i in range(len(chars[0])):
        for j in range(len(chars)):
            dflag += chars[j][i]
    return dflag

print(flag('1a6a255b150c73041e1c106e46016b34325a764251286f322c13220c0322196e0243375c074e2e0d35417a7c1c10122738102c45423d7b25', 'j5F/swFQ'))
```

The complete exploit will be :-
```
a = "ABCDEFGHIJ"
a1 = "abcd"
enc_a = "ABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJAB"
x = [1, 2, 3]
lst = []

def get_key(msg):
    init = 'p_ctf{'
    keylen = [i for i in range(1, 56)]

    for l in keylen:
        key = ''
        chars = [chr(int(msg[x:x+2], 16))
                 for x in range(0, len(msg), 2)]
        def dif(A, n): return [tuple(A[i:i+n])
                                       for i in range(0, len(A), n)]
        chars = dif(chars, l)
        chars = list(zip(*chars))
        for i in range(min(len(init), len(chars))):
            key += chr(ord(chars[i][0]) ^ ord(init[i]))
        print(key)  # First 6 chars will be j5F/sw

    key6 = 'j5F/sw'
    rev_key = '0791151174073560118079115117407356011807911511740735601180791151174073560118079115117407356011807911511740735601'
    l = (len(rev_key)//6)+1
    enck = rev_key[::-1]
    enck = enck[:l]
    print(enck)
    enc_key6 = ''
    for i in key6:
        enc_key6 += str(ord(i))
    print(enc_key6)
    print(enck[-4:])  # Prints last 4 ordinal values
    # Therefore second last is ord(70) --> F and last is ord(81) --> Q


# Prints the encrypted flag from given encrypted list
def decrypt(a1, msg):
    for i in range(len(a1)):
        if 48 <= ord(a1[i]) <= 51:
            msg[i] = chr(((msg[i] ^ 0x09) + 0x2f) ^ 0xe)
        if 52 <= ord(a1[i]) <= 54:
            msg[i] = chr(((msg[i]) - 0x1c) ^ 0xF)
        if 55 <= ord(a1[i]) <= 57:
            msg[i] = chr(((msg[i]) + 0x3e) ^ 0xd)
    s = ""
    for i in msg:
        s += str(i)
    print(s)


x = [25, 46, -3, 73, 4, 86, 5, 52, -2, 86, 6, 48, 3, 88, 91, 2, 25, 53, -2, 55, -2, -1, 0, 53, 87, 0, 6, -2, 85, 52, 0, 2, 88, 89, 5, 73, 3, -3, 2, 1, -6, 25, 4, 83, 0, 48, 0, 89, 4, 48, 25, 88, 89, 4, 6,
     55, -1, 7, 1, 1, 25, 1, 85, 53, 6, 1, 87, 7, 0, 3, 86, 136, 6, 3, 2, 42, 4, 42, -1, 50, 7, 86, 2, 25, -4, 138, 3, 48, 25, 136, 90, 6, 25, 4, 1, 3, 0, -9, 25, 6, 89, 55, 2, -6, 87, 4, 0, 50, 84, 137, 4, 5]


def flag(msg, key):
    l = len(key)
    chars = [chr(int(msg[x:x+2], 16)) for x in range(0, len(msg), 2)]

    def dif(A, n): return [tuple(A[i:i+n])
                                   for i in range(0, len(A), n)]
    chars = dif(chars, l)
    chars = list(zip(*chars))
    for i in range(l):
        a = 0
        e = ''
        for j in range(len(chars[i])):
            if a == 0:
                a = ord(chars[i][j]) ^ ord(key[i]) ^ (a >> 2)
            else:
                a = ord(chars[i][j]) ^ ord(key[i]) ^ (
                    ord(chars[i][j-1]) >> 2)
            e += chr(a)
        chars[i] = e

    dflag = ''
    for i in range(len(chars[0])):
        for j in range(len(chars)):
            dflag += chars[j][i]
    return dflag


decrypt('0791151174073560118079115117407356011807911511740735601180791151174073560118079115117407356011807911511740735601', x)
print(get_key('1a6a255b150c73041e1c106e46016b34325a764251286f322c13220c0322196e0243375c074e2e0d35417a7c1c10122738102c45423d7b25'))
print(flag('1a6a255b150c73041e1c106e46016b34325a764251286f322c13220c0322196e0243375c074e2e0d35417a7c1c10122738102c45423d7b25', 'j5F/swFQ'))
```
