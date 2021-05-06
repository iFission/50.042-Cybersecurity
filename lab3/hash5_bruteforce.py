# 1003474
# Alex W
# When the script is run from scratch, it takes about 5 minutes.
# Subsequent runs (with generated hash) takes 164 seconds.

import hashlib
import itertools
from tqdm import tqdm
import pickle

plaintext_list = []
hashed_list = []

char_set = "0123456789abcdefghijklmnopqrstuvwxyz"
char_set = [char for char in char_set]
char_length = 5

try:
    with open("plaintext_list.pickle", "rb") as f:
        plaintext_list = pickle.load(f)
    with open("hashed_list.pickle", "rb") as f:
        hashed_list = pickle.load(f)
except FileNotFoundError as e:
    print("generate")
    iter_set = list(itertools.product(char_set, repeat=char_length))
    print(len(iter_set))

    for permutation in tqdm(iter_set):
        plaintext = "".join(permutation)
        plaintext_list.append(plaintext)

        hashed = hashlib.md5(plaintext.encode()).hexdigest()
        hashed_list.append(hashed)

    with open("plaintext_list.pickle", "wb") as f:
        pickle.dump(plaintext_list, f, protocol=4)
    with open("hashed_list.pickle", "wb") as f:
        pickle.dump(hashed_list, f, protocol=4)

hashes = """a92b66a9802704ca8616c4b092378272
d4efdba5e9725e77c9b9051fa8136f0a
96f6065d8f2dd1376eff88fba65d1d83
78c1b8edd1bc3ffc438432479289a9e1
0d5b558d5f6744deaaf5b016c6c77a57
ddaafa5d551a582bc924d09cc8d33ee5
a74edf83748e3c4fa5f31ec10bad79db
1b31905c59f481958d2eb72158c27ac7
6e313b70d12de950443527a33d802b76
de952f5454fb0ee79bca249f80e9fe8f
a8218c67a5b4e652e30a59372e07df59
836626589007d7dd5304c8d22815fffc
644674d142ba2174a80889f833b32563
1b4baba3ae3be69857b323cf6b7fcd80
81466b6bb4be5a48e2230be1338bcde6
""".split()

for hash_current in tqdm(hashes):
    index = -1
    index = hashed_list.index(hash_current)
    print(f'plaintext: {plaintext_list[index]}')
    print(f'hash: {hash_current}')