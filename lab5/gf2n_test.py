# 1003474
# Alex W

from gf2n import *


def test_add_zero():
    p1 = Polynomial2([0])
    p2 = Polynomial2([0])
    p3 = p1.add(p2)
    expected = Polynomial2([0])
    print('p3= p1+p2 = ', p3)

    assert p3 == expected


def test_add():
    print('\nTest 1')
    print('======')
    print('p1=x^5+x^2+x')
    print('p2=x^3+x^2+1')
    p1 = Polynomial2([0, 1, 1, 0, 0, 1])
    p2 = Polynomial2([1, 0, 1, 1])
    p3 = p1.add(p2)
    expected = Polynomial2([1, 1, 0, 1, 0, 1])
    print('p3= p1+p2 = ', p3)

    assert p3 == expected


def test_subtract():
    print('\nTest 1')
    print('======')
    print('p1=x^5+x^2+x')
    print('p2=x^3+x^2+1')
    p1 = Polynomial2([0, 1, 1, 0, 0, 1])
    p2 = Polynomial2([1, 0, 1, 1])
    p3 = p1.sub(p2)
    expected = Polynomial2([1, 1, 0, 1, 0, 1])
    print('p3= p1+p2 = ', p3)

    assert p3 == expected


def test_modp():
    p3 = Polynomial2([0, 0, 1, 1, 1, 1, 0, 0, 1])
    modp = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])

    p4 = p3.modp(modp)
    print(p4)
    expected = Polynomial2([1, 1, 1, 0, 0, 1])
    print(expected)

    assert p4 == expected


def test_modp_2():
    p3 = Polynomial2([0, 1, 1, 1, 0, 0, 1])
    modp = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])

    p4 = p3.modp(modp)
    print(p4)
    expected = Polynomial2([0, 1, 1, 1, 0, 0, 1])
    print(expected)

    assert p4 == expected


def test_shift_right():
    p3 = Polynomial2([0, 0, 1, 1, 1, 1, 0, 0, 1])
    p4 = p3.shift_right()
    expected = Polynomial2([0, 0, 0, 1, 1, 1, 1, 0, 0, 1])
    print(expected)

    assert p4 == expected


def test_mul():
    p1 = Polynomial2([0, 1, 1, 0, 0, 1])
    p2 = Polynomial2([0, 1, 1, 1, 1, 0, 0, 1])
    modp = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])

    p3 = p1.mul(p2, modp)
    expected = Polynomial2([1, 1, 1, 1, 0, 1])

    print(p3)
    print(expected)

    assert p3 == expected


def test_div():

    print('\nTest 2')
    print('======')
    print('p4=x^7+x^4+x^3+x^2+x')
    print('modp=x^8+x^7+x^5+x^4+1')
    p1 = Polynomial2([0, 1, 1, 0, 0, 1])
    p4 = Polynomial2([0, 1, 1, 1, 1, 0, 0, 1])
    # modp=Polynomial2([1,1,0,1,1,0,0,0,1])
    modp = Polynomial2([1, 0, 0, 0, 1, 1, 0, 1, 1])
    p5 = p1.mul(p4, modp)
    expected = Polynomial2([0, 0, 0, 1, 1, 0, 1, 1])
    print('p5=p1*p4 mod (modp)=', p5)

    assert p5 == expected


def test_getInt():
    p1 = Polynomial2([0, 1, 1, 0, 0, 1])
    p1_int = p1.getInt()

    expected = 38

    assert p1_int == expected


def test_3():

    print('\nTest 3')
    print('======')
    print('p6=x^12+x^7+x^2')
    print('p7=x^8+x^4+x^3+x+1')
    p6 = Polynomial2([0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
    p7 = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])
    p8q, p8r = p6.div(p7)

    expected_q = Polynomial2([1, 0, 0, 0, 1])
    expected_r = Polynomial2([1, 1, 1, 1, 0, 1])
    print('q for p6/p7=', p8q)
    print('r for p6/p7=', p8r)

    assert p8q == expected_q
    assert p8r == expected_r


def test_gf2n_getPolynomial2():
    g4 = GF2N(0b110111, 4)

    assert g4.getPolynomial2() == Polynomial2([1, 1, 1, 0, 1, 1])


def test_4():

    print('\nTest 4')
    print('======')
    g1 = GF2N(100)
    g2 = GF2N(5)
    print('g1 = ', g1.getPolynomial2())
    print('g2 = ', g2.getPolynomial2())
    g3 = g1.add(g2)
    print('g1+g2 = ', g3)


def test_g2fn_add():

    print('\nTest 4')
    print('======')
    ip = Polynomial2([1, 0, 0, 1, 1])
    print('irreducible polynomial', ip)
    g4 = GF2N(0b1101, 4, ip)
    g5 = GF2N(0b110, 4, ip)
    print('g4 = ', g4.getPolynomial2())
    print('g5 = ', g5.getPolynomial2())
    g6 = g4.mul(g5)
    print('g4 x g5 = ', g6.p)


def test_1001():

    print('\nTest 5')
    print('======')
    ip = Polynomial2([1, 1, 1])
    print('irreducible polynomial', ip)
    g4 = GF2N(0b10, 2, ip)
    g5 = GF2N(0b11, 2, ip)
    print('g4 = ', g4.getPolynomial2())
    print('g5 = ', g5.getPolynomial2())
    g6 = g4.mul(g5)
    print('g4 x g5 = ', g6.p)


def test_5():

    print('\nTest 5')
    print('======')
    ip = Polynomial2([1, 1, 0, 0, 1])
    print('irreducible polynomial', ip)
    g4 = GF2N(0b1101, 4, ip)
    g5 = GF2N(0b110, 4, ip)
    print('g4 = ', g4.getPolynomial2())
    print('g5 = ', g5.getPolynomial2())
    g6 = g4.mul(g5)
    print('g4 x g5 = ', g6.p)
    assert g6.p == Polynomial2([0, 0, 0, 1])


def test_6():

    print('\nTest 6')
    print('======')
    g7 = GF2N(0b1000010000100, 13, None)
    g8 = GF2N(0b100011011, 13, None)
    print('g7 = ', g7.getPolynomial2())
    print('g8 = ', g8.getPolynomial2())
    q, r = g7.div(g8)
    print('g7/g8 =')
    print('q = ', q.getPolynomial2())
    print('r = ', r.getPolynomial2())

    assert q.p == Polynomial2([1, 0, 0, 0, 1])
    assert r.p == Polynomial2([1, 1, 1, 1, 0, 1])
