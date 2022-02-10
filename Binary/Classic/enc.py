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
