# 1003474
# Alex W

from random import choice, seed
import hashlib

plaintext_list = [
    "opmen",
    "tthel",
    "cance",
    "nized",
    "tpoin",
    "aseas",
    "dsmto",
    "egunb",
    "mlhdi",
    "ofror",
    "hed4e",
    "di5gv",
    "owso9",
    "sso55",
    "lou0g",
]
salted_password_list = []
salted_hashed_list = []

salt_char_set = "abcdefghijklmnopqrstuvwxyz"

seed(-1)

for password in plaintext_list:
    salt = choice(salt_char_set)
    salted_password = password + salt
    salted_password_list.append(salted_password)

    hashed = hashlib.md5(salted_password.encode()).hexdigest()
    salted_hashed_list.append(hashed)

print(salted_password_list, salted_hashed_list)

with open('pass6.txt', 'w') as f:
    f.write("\n".join(salted_password_list))
    f.write("\n")

with open('salted6.txt', 'w') as f:
    f.write("\n".join(salted_hashed_list))
    f.write("\n")