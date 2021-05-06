#50.042 FCS Lab 6 template
# Year 2019

import random


def square_multiply(a, x, n):
    res = 1
    for i in bin(x).lstrip('0b'):
        res = res * res % n
        if (i == '1'):
            res = res * a % n
    # return 1
    return res


def miller_rabin(n, a):
    # n: number
    # a: iterations to check

    if n == 2:
        return True

    if n == 2:
        return True

    # if n is even, not prime
    if n % 2 == 0:
        return False

    # write n as 2**r*d + 1
    # find r, d
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(a):
        a = random.randint(2, n - 2)
        x = square_multiply(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = square_multiply(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def generate_prime(n):
    x = random.getrandbits(n)
    while not miller_rabin(x, 2):
        x = random.getrandbits(n)

    return x


if __name__ == "__main__":
    print('Is 561 a prime?')
    print(miller_rabin(561, 2))
    print('Is 27 a prime?')
    print(miller_rabin(27, 2))
    print('Is 61 a prime?')
    print(miller_rabin(61, 2))

    print('Random number (100 bits):')
    print(generate_prime(100))

    print('Random number (60 bits):')
    print(generate_prime(60))