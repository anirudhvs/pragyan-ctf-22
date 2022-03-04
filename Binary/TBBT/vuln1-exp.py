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
