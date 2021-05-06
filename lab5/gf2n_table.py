# 1003474
# Alex W

from gf2n import GF2N, Polynomial2

ip = Polynomial2([1, 0, 0, 1, 1])
n = 4

print(f'ip is {ip}')
print("")

for i in range(2**n):
    for j in range(2**n):
        g1 = GF2N(i, n, ip)
        g2 = GF2N(j, n, ip)

        print(f'g1: {g1}')
        print(f'g2: {g2}')
        print(f'add: {g1.add(g2)}')
        print(f'mul: {g1.mul(g2)}')

        print("")
