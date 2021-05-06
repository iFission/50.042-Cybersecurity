def encrypt(letter, key):
    if letter.isupper():
        return (chr((ord(letter) + key - ord('A')) % 26 + ord('A')))
    elif letter.islower():
        return (chr((ord(letter) + key - ord('a')) % 26 + ord('a')))
    else:
        return letter


def decrypt(letter, key):
    return encrypt(letter, -key)


def do_caeser(string, key, mode="ENCRYPT"):
    if mode == "ENCRYPT":
        return "".join([encrypt(letter, key) for letter in string])
    if mode == "DECRYPT":
        return "".join([decrypt(letter, key) for letter in string])


print(encrypt('B', 2))
print(do_caeser('aaa', 2))
print(do_caeser('aaa', 2, "DECRYPT"))
print(do_caeser('hi im alex', 2))
print(do_caeser('jk ko cngz', 2, "DECRYPT"))