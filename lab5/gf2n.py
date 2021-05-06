# 50.042 FCS Lab 5 Modular Arithmetics
# Year 2020
# 1003474
# Alex W

import copy
from itertools import zip_longest


class Polynomial2:
    def __init__(self, coeffs):
        self.coeffs = coeffs

    def add(self, p2):
        result = []

        for x, y in zip_longest(self.coeffs, p2.coeffs, fillvalue=0):
            result.append(x ^ y)

        # remove trailing 0
        while len(result) > 1 and result[-1] == 0:
            result.pop(-1)

        return Polynomial2(result)

    def sub(self, p2):
        return self.add(p2)

    def mul(self, p2, modp=None):
        results = []

        # calculate x0
        results.append(p2)

        for index in range(1, len(self.coeffs)):
            result_prev = results[-1]
            try:
                if result_prev.coeffs.index(1) > -1:
                    result_prev_shifted = result_prev.shift_right()

                    if modp:
                        result = result_prev_shifted.modp(modp)
                        results.append(result)
                    else:
                        result_prev_shifted = result_prev.shift_right()
                        results.append(result_prev_shifted)

            # if prev result no MSB 1
            except ValueError:
                result_prev_shifted = result_prev.shift_right()
                results.append(result_prev_shifted)

        result_sum = Polynomial2([0])

        for index, coeff in enumerate(self.coeffs):
            if coeff == 1:
                result_sum = result_sum.add(results[index])

        return result_sum

    @property
    def deg(self):
        return len(self.coeffs) - 1

    @property
    def lc(self):
        return self.coeffs[-1]

    def div(self, p2):
        q = Polynomial2([0])
        r = copy.deepcopy(self)

        b = p2
        d = b.deg
        c = b.lc

        while r.deg >= d:
            s = Polynomial2([0 for i in range(r.deg - d)] + [1])
            q = s.add(q)
            r = r.sub(s.mul(b))

        return q, r

    def modp(self, modp):

        # check if MSB coincides
        if len(self.coeffs) >= len(modp.coeffs):

            # XOR self and modp without MSB
            # same as adding
            return Polynomial2(self.coeffs[:-1]).add(
                Polynomial2(modp.coeffs[:-1]))

        else:
            return self

    def shift_right(self):
        # bit shift right
        # same as adding 0 to LSB
        return Polynomial2([0] + self.coeffs)

    def __str__(self):
        result = ''

        for index, coeff in enumerate(self.coeffs[::-1]):
            if coeff == 1:
                result += f'x^{len(self.coeffs)-index-1}+'

        return result.rstrip("+")

    def __eq__(self, p2):
        return str(self) == str(p2)

    def getInt(self):
        result = 0
        for index, coeff in enumerate(self.coeffs):
            result += coeff * 2**index

        return result


class GF2N:
    affinemat = [[1, 0, 0, 0, 1, 1, 1, 1], [1, 1, 0, 0, 0, 1, 1, 1],
                 [1, 1, 1, 0, 0, 0, 1, 1], [1, 1, 1, 1, 0, 0, 0, 1],
                 [1, 1, 1, 1, 1, 0, 0, 0], [0, 1, 1, 1, 1, 1, 0, 0],
                 [0, 0, 1, 1, 1, 1, 1, 0], [0, 0, 0, 1, 1, 1, 1, 1]]

    def __init__(self, x, n=8, ip=Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])):
        self.x = x
        self.n = n
        self.ip = ip

    def add(self, g2):
        # polynomial addition
        # then reduce with ip
        result = self.p.add(g2.p)

        # XOR with ip
        result = result.modp(self.ip)

        return GF2N(result.getInt(), self.n, self.ip)

    def sub(self, g2):
        # same as add
        return self.add(g2.p)

    def mul(self, g2):
        # normal polynomial mul with modp ip
        result = self.p.mul(g2.p, self.ip)

        return GF2N(result.getInt(), self.n, self.ip)

    def div(self, g2):
        # normal polynomial division
        q, r = self.p.div(g2.p)
        return GF2N(q.getInt(), self.n, self.ip), GF2N(r.getInt(), self.n,
                                                       self.ip)

    @property
    def p(self):
        return self.getPolynomial2()

    def getPolynomial2(self):
        coeffs = list(str(bin(self.x)).lstrip('0b'))
        polynomial2 = Polynomial2([int(x) for x in coeffs][::-1])
        return polynomial2

    def __str__(self):
        return str(self.p.getInt())

    def getInt(self):
        return self.p.getInt()

    def mulInv(self):
        pass

    def affineMap(self):
        pass


if __name__ == "__main__":
    print('\nTest 1')
    print('======')
    print('p1=x^5+x^2+x')
    print('p2=x^3+x^2+1')
    p1 = Polynomial2([0, 1, 1, 0, 0, 1])
    p2 = Polynomial2([1, 0, 1, 1])
    p3 = p1.add(p2)
    print('p3= p1+p2 = ', p3)

    print('\nTest 2')
    print('======')
    print('p4=x^7+x^4+x^3+x^2+x')
    print('modp=x^8+x^7+x^5+x^4+1')
    p4 = Polynomial2([0, 1, 1, 1, 1, 0, 0, 1])
    # modp=Polynomial2([1,1,0,1,1,0,0,0,1])
    modp = Polynomial2([1, 0, 0, 0, 1, 1, 0, 1, 1])
    p5 = p1.mul(p4, modp)
    print('p5=p1*p4 mod (modp)=', p5)

    print('\nTest 3')
    print('======')
    print('p6=x^12+x^7+x^2')
    print('p7=x^8+x^4+x^3+x+1')
    p6 = Polynomial2([0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
    p7 = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])
    p8q, p8r = p6.div(p7)
    print('q for p6/p7=', p8q)
    print('r for p6/p7=', p8r)

    ####
    print('\nTest 4')
    print('======')
    g1 = GF2N(100)
    g2 = GF2N(5)
    print('g1 = ', g1.getPolynomial2())
    print('g2 = ', g2.getPolynomial2())
    g3 = g1.add(g2)
    print('g1+g2 = ', g3)

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

    # print('\nTest 7')
    # print('======')
    # ip = Polynomial2([1, 1, 0, 0, 1])
    # print('irreducible polynomial', ip)
    # g9 = GF2N(0b101, 4, ip)
    # print('g9 = ', g9.getPolynomial2())
    # print('inverse of g9 =', g9.mulInv().getPolynomial2())

    # print('\nTest 8')
    # print('======')
    # ip = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])
    # print('irreducible polynomial', ip)
    # g10 = GF2N(0xc2, 8, ip)
    # print('g10 = 0xc2')
    # g11 = g10.mulInv()
    # print('inverse of g10 = g11 =', hex(g11.getInt()))
    # g12 = g11.affineMap()
    # print('affine map of g11 =', hex(g12.getInt()))

    p6 = Polynomial2([1, 0, 1, 0, 1])
    p7 = Polynomial2([1, 0])
    p8q, p8r = p7.div(p6)
    print(p8q, p8r)