from secret import *
from random import randint
from math import gcd
from Crypto.Util.number import *


class EllipticCurve:
    def __init__(self, a, b, p) -> None:
        self.a = a
        self.b = b
        self.p = p

    def isPoint(self, X, Y) -> bool:
        if X == 0 and Y == 0:
            return True
        if (Y**2 - X**3 - self.a*X - self.b) % self.p == 0:
            return True
        else:
            return False


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __eq__(self, A) -> bool:
        return self.x == A.x and self.y == A.y


X = EllipticCurve(a, b, p)
Zero = Point(0, 0)
G = Point(G[0], G[1])

assert(X.isPoint(G.x, G.y))
assert b % p != 0


def add(P: Point, Q: Point, X=X):
    if Q == Zero:
        return P
    if P == Zero:
        return Q
    x1, y1 = P.x, P.y
    x2, y2 = Q.x, Q.y
    if P == Q:
        if gcd(2*y1, X.p) != 1:
            return Zero
        m = ((3*(x1**2)+X.a) * pow(2*y1, -1, X.p)) % X.p
    else:
        if gcd(x1-x2, X.p) != 1:
            return Zero
        m = ((y2-y1) * pow(x2-x1, -1, X.p)) % X.p
    x3 = (m**2 - x1 - x2) % X.p
    y3 = (m*(x1-x3)-y1) % X.p
    R = Point(x3, y3)
    return R


def order(P: Point):
    n = 2
    R = add(P, P)
    while R != Zero:
        n += 1
        R = add(R, P)
    return n


def multiply(P: Point, n: int):
    Q = P
    R = Zero
    n = n % order(P)
    while n != 0:
        if n % 2 == 1:
            R = add(R, Q)
        Q = add(Q, Q)
        n = n//2
    return R


def log(P: Point, Q: Point):
    n = 0
    R = Zero
    while R != Q and n < order(P):
        n += 1
        R = add(R, P)
    return n


def e(P: Point, Q: Point, G: Point):
    return (log(G, P) * log(G, Q)) % order(G)


def encrypt(M: str, G: Point, G1: Point, r: int, s: int):
    pt = bytes_to_long(M.encode())
    return (pt*s*pow(e(multiply(G, r), multiply(G, s), G1), s, order(G1))) % order(G1)


if __name__ == "__main__":
    print(f"Order of point G is: {order(G)}")
    G1 = multiply(G, randint(1, order(G)-1))
    r = randint(1, order(G)-1)
    while True:
        try:
            s = int(input("Enter:"))
        except:
            s = 0
        C = encrypt(flag, G, G1, r, s)
        print(f"You received {C}")
