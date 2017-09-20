# -*- coding: utf-8 -*-
from __future__ import print_function

from pprint import pprint
from fractions import *
import numpy as np

class pg_point(np.ndarray):
    def __new__(cls, inputarr):
        obj = np.asarray(inputarr).view(cls)
        return obj

    def __eq__(self, other):
        if type(other) is type(self):
            return (np.cross(self, other) == 0).all()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def incident(self, l):
        return not self.dot(l)

    def __add__(self, other):
        return pg_point(np.ndarray.__add__(self, other))

    def __sub__(self, other):
        return pg_point(np.ndarray.__sub__(self, other))

    def __mul__(self, other):
        ''' meet '''
        l = np.cross(self, other)
        return pg_line(l)

    def aux(self):
        return pg_line(self)

class pg_line(np.ndarray):
    def __new__(cls, inputarr):
        obj = np.asarray(inputarr).view(cls)
        return obj

    def __eq__(self, other):
        if type(other) is type(self):
            return (np.cross(self, other) == 0).all()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def incident(self, p):
        return not self.dot(p)

    def __add__(self, other):
        return pg_line(np.ndarray.__add__(self, other))

    def __sub__(self, other):
        return pg_line(np.ndarray.__sub__(self, other))

    def __mul__(self, other):
        ''' join '''
        return pg_point(np.cross(self, other))

    def aux(self):
        return pg_point(self)

def join(p, q):
    return p * q

def meet(l, m):
    return l * m

def coincident(p, q, r):
    return r.incident(p * q)

# note: `lambda` is a preserved keyword in python
def pk_point(lambda1, p, mu1, q):
    return pg_point(lambda1 * p + mu1 * q)

# note: `lambda` is a preserved keyword in python
def pk_line(lambda1, l, mu1, m):
    return pg_line(lambda1 * l + mu1 * m)

def coI_core(l, Lst):
    for p in Lst:
        if not l.incident(p):
            return False
    return True

def coI(Lst):
    if len(Lst) < 3:
        return True
    [p, q] = Lst[0:2]
    assert p != q
    return coI_core(p*q, Lst[2:])

def persp(L, M):
    if len(L) != len(M):
        return False
    if len(L) < 3:
        return True
    [pL, qL] = L[0:2]
    [pM, qM] = M[0:2]
    assert pL != qL 
    assert pM != qM
    assert pL != pM
    assert qL != qM
    O = (pL * pM) * (qL * qM)
    for rL, rM in zip(L[2:], M[2:]):
        if not O.incident(rL * rM):
            return False
    return True

def harm_conj(A, B, C):
    # assert coincident(A,B,C)
    l = A * B
    P = l.aux()
    a = P * A
    b = P * B
    c = P * C
    R = P + C
    Q = (A * R) * b
    S = (B * R) * a
    return (Q * S) * l 

def dot(p, l):
    return np.dot(p, l)

def x_ratio(A, B, l, m):
    dAl = dot(A, l)
    dAm = dot(A, m)
    dBl = dot(B, l)
    dBm = dot(B, m)
    if isinstance(dAl, int):
        return Fraction(dAl, dAm) / Fraction(dBl, dBm)
    else:
        return dAl*dBm/(dAm*dBl)

def R(A, B, C, D):
    O = (C*D).aux()
    return x_ratio(A, B, O*C, O*D)


def isharmonic(A, B, C, D):
    O = (C*D).aux()
    OC = O * C
    OD = O * D
    ac = dot(A, OC)
    ad = dot(A, OD)
    bc = dot(B, OC)
    bd = dot(B, OD)
    return ac*bd + ad*bc == 0

def check_pappus(A, B, C, D, E, F):
    G = (A*E) * (B*D)
    H = (A*F) * (C*D)
    I = (B*F) * (C*E)
    assert coincident(G, H, I)

def check_desargue(A, B, C, D, E, F):
    a = B * C
    b = A * C
    c = B * A
    d = E * F
    e = D * F
    f = E * D

    b1 = persp([A, B, C], [D, E, F])
    b2 = persp([a, b, c], [d, e, f])
    if b1: assert b2
    else: assert not b2

if __name__ == "__main__":
    p = pg_point([1-2j, 3-1j, 2+1j])
    q = pg_point([-2+1j, 1-3j, -1-1j])
    r = pg_point([2-1j, -2+1j, 1+1j])
    s = pg_point([2j, 2-2j, 3])
    t = pg_point([2, -2j, 2])

    assert p.incident(p*q)

    print(coI([p, q, pk_point(1, p, 1, q), pk_point(1, p, -1, q)])) # get True
    print(persp([p, q, p + q], [r, p + r, p])) # get False
    O = meet(join(p, s), join(q, t))
    r = join(p, q)
    u = O - r
    check_desargue(p, q, r, s, t, u)

    import sympy
    sympy.init_printing()
    px = sympy.Symbol("px", integer=True)
    py = sympy.Symbol("py", integer=True)
    pz = sympy.Symbol("pz", integer=True)
    qx = sympy.Symbol("qx", integer=True)
    qy = sympy.Symbol("qy", integer=True)
    qz = sympy.Symbol("qz", integer=True)
    lambda1 = sympy.Symbol("lambda1", integer=True)
    mu1 = sympy.Symbol("mu1", integer=True)
    p = pg_point([px, py, pz])
    q = pg_point([qx, qy, qz])
    r = pk_point(lambda1, p, mu1, q)
    # l = join(join(p, q).aux(), r)
    # ans1 = np.dot(l.coord, q.coord)
    # ans2 = np.dot(l.coord, p.coord)
    # ans = sympy.simplify(mu1*ans1 + lambda1* ans2)
    # print(ans)
    # c = harm_conj(p, q, r)
    # ans = sympy.simplify(c.coord[0])
    # print(ans)

    sx = sympy.Symbol("sx", integer=True)
    sy = sympy.Symbol("sy", integer=True)
    sz = sympy.Symbol("sz", integer=True)
    tx = sympy.Symbol("tx", integer=True)
    ty = sympy.Symbol("ty", integer=True)
    tz = sympy.Symbol("tz", integer=True)
    lambda2 = sympy.Symbol("lambda2", integer=True)
    mu2 = sympy.Symbol("mu2", integer=True)

    s = pg_point([sx, sy, sz])
    t = pg_point([tx, ty, tz])
    u = pk_point(lambda2, s, mu2, t)
    G = meet(join(p, t), join(q, s))
    H = meet(join(p, u), join(r, s))
    I = meet(join(q, u), join(r, t))
    ans = np.dot(G, join(H, I))
    ans = sympy.simplify(ans)
    print(ans) # get 0

    # p, q, s   t
    lambda3 = sympy.Symbol("lambda3", integer=True)
    mu3 = sympy.Symbol("mu3", integer=True)
    p2 = pk_point(lambda1, p, mu1, t)
    q2 = pk_point(lambda2, q, mu2, t)
    s2 = pk_point(lambda3, s, mu3, t)
    G = meet(join(p, q), join(p2, q2))
    H = meet(join(q, s), join(q2, s2))
    I = meet(join(s, p), join(s2, p2))
    ans = np.dot(G, join(H, I))
    ans = sympy.simplify(ans)
    print(ans) # get 0
