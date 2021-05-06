from primes import *


class TestSquareMultiply:
    def test_1(self):
        # "4 = 5^2 % 7"
        assert square_multiply(5, 2, 7) == 4

    def test_2(self):
        # "1 = 3^8 
        assert square_multiply(3, 8, 5

    def test_3(self):
        # "0 = 4^4 % 4"
        assert square_multiply(4, 4, 4) == 0


class TestPrime:
    def test_1(self):
        assert miller_rabin(561, 2) == False

    def test_2(self):
        assert miller_rabin(27, 2) == False

    def test_3(self):
        assert miller_rabin(61, 2) == True

    def test_4(self):
        assert miller_rabin(61, 2) == False
