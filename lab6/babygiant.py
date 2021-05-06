#50.042 FCS Lab 6 template
#Year 2019

import math
import primes


def baby_step(alpha, beta, p, fname):
    m = int(math.floor(math.sqrt(p)))

    with open(fname, "w") as fout:
        for a_b in range(0, m):
            fout.write(str((beta * alpha**a_b) % p) + "\n")


def giant_step(alpha, p, fname):
    m = int(math.floor(math.sqrt(p)))

    with open(fname, "w") as fout:
        for a_g in range(0, m):
            fout.write(str(primes.square_multiply(alpha, a_g * m, p)) + "\n")


def baby_giant(alpha, beta, p):
    # alpha = alpha or g
    # beta = A or B (A or B's P+)
    # p = p

    m = int(math.floor(math.sqrt(p)))

    baby_step(alpha, beta, p, "baby_step.txt")
    giant_step(alpha, p, "giant_step.txt")

    baby_step_list = []
    giant_step_list = []

    with open("baby_step.txt", "r") as fin:
        baby_step_list = [line.rstrip("\n") for line in fin.readlines()]

    with open("giant_step.txt", "r") as fin:
        giant_step_list = [line.rstrip("\n") for line in fin.readlines()]

    # compare both lists to find collision
    collision = list(set(baby_step_list).intersection(set(giant_step_list)))

    if len(collision) > 0:
        a_b = baby_step_list.index(collision[0])
        a_g = giant_step_list.index(collision[0])

        return a_g * m - a_b

    else:
        return -1


if __name__ == "__main__":
    """
    test 1
    My private key is:  264
    Test other private key is:  7265
    
    """
    p = 17851
    alpha = 17511
    A = 2945
    B = 11844
    sharedkey = 1671
    a = baby_giant(alpha, A, p)
    b = baby_giant(alpha, B, p)
    guesskey1 = primes.square_multiply(A, b, p)
    guesskey2 = primes.square_multiply(B, a, p)
    print('Guess key 1:', guesskey1)
    print('Guess key 2:', guesskey2)
    print('Actual shared key :', sharedkey)
