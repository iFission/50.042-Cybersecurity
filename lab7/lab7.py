from Crypto.PublicKey import RSA
from base64 import decodebytes, encodebytes


## Demo encryption and decryption of RSA.
def square_multiply(a, x, n):
    res = 1
    for i in bin(x).lstrip('0b'):
        res = res * res % n
        if (i == '1'):
            res = res * a % n

    return res


key = open('mykey.pem.pub', 'r')
rsakey_pub = RSA.importKey(key.read())
print(f"rsakey_pub: {rsakey_pub}")
print(f"rsakey_pub.n: {rsakey_pub.n}")
print(f"rsakey_pub.e: {rsakey_pub.e}")

key = open('mykey.pem.priv', 'r')
rsakey_priv = RSA.importKey(key.read())
print(f"rsakey_priv: {rsakey_priv}")
print(f"rsakey_priv.n: {rsakey_priv.n}")
print(f"rsakey_priv.d: {rsakey_priv.d}")

print()


def encrypt(x, e, n):
    return square_multiply(x, e, n)


def decrypt(x, d, n):
    return square_multiply(x, d, n)


def get_byte_from_int(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def get_int_from_byte(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')


message = "hi there!~"


def encrypt_string(message, e, n):

    message_encoded = encodebytes(message.encode())
    message_encoded_int = get_int_from_byte(message_encoded)
    message_encoded_int_encrypted = encrypt(message_encoded_int, e, n)

    return message_encoded_int_encrypted


def decrypt_string(encoded_int, d, n):

    message_encoded_int_decrypted = decrypt(encoded_int, d, n)

    return decodebytes(
        get_byte_from_int(message_encoded_int_decrypted)).decode()


message_encoded_int_encrypted = encrypt_string(message, rsakey_pub.e,
                                               rsakey_pub.n)

message_encoded_decrypted = decrypt_string(message_encoded_int_encrypted,
                                           rsakey_priv.d, rsakey_priv.n)
print(f"message: {message}\n")
print(f"message_encoded_int_encrypted: {message_encoded_int_encrypted}\n")
print(f"message_encoded_decrypted: {message_encoded_decrypted}\n")

## Demo signing a message and verifying it.
from Crypto.Hash import SHA256
h = SHA256.new()
h.update(b'Hello')
print(f"hash: {h.hexdigest()}")

sha256_signed = encrypt_string(h.hexdigest(), rsakey_priv.d, rsakey_priv.n)
sha256_verify = decrypt_string(sha256_signed, rsakey_pub.e, rsakey_pub.n)

print(f"verified hash: {sha256_verify}")
print()

## Demo protocol attack to both encryption and digital signature.
print("encrypting:\n100\n")
y = encrypt(100, rsakey_pub.e, rsakey_pub.n)
y_s = encrypt(2, rsakey_pub.e, rsakey_pub.n)
m = y * y_s

m_decrypted = decrypt(m, rsakey_priv.d, rsakey_priv.n)
print(f"result:\n{y}\n")
print(f"modified to:\n{m}\n")
print(f"decrypted:\n{m_decrypted}\n")

##
import random

signature = SHA256.new()
signature.update(get_byte_from_int(2))
s = signature.hexdigest()

print(f"signature: {s}")

x = encrypt_string(s, rsakey_pub.e, rsakey_pub.n)
x_prime = encrypt_string(s, rsakey_pub.e, rsakey_pub.n)

print(f"x == x_prime: {x == x_prime}")
print()

##
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS


def generate_RSA(bits=1024):
    priv = RSA.generate(bits)
    pub = priv.publickey()
    with open('priv.pem', 'wb') as f:
        f.write(priv.exportKey('PEM'))
    with open('pub.pem', 'wb') as f:
        f.write(pub.exportKey('PEM'))


generate_RSA()


def encrypt_RSA(public_key_file, message):
    key = open(public_key_file, 'r')
    rsakey_pub = RSA.importKey(key.read())
    cipher = PKCS1_OAEP.new(rsakey_pub)
    ciphertext = cipher.encrypt(bytes(message, 'utf8'))
    return ciphertext


def decrypt_RSA(private_key_file, ciphertext):
    key = open(private_key_file, 'r')
    rsakey_priv = RSA.importKey(key.read())
    cipher = PKCS1_OAEP.new(rsakey_priv)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.decode()


plaintext = "hi alex!"
print(f"plaintext: {plaintext}\n")
ciphertext = encrypt_RSA('pub.pem', plaintext)
print(f"ciphertext: {ciphertext}\n")
plaintext = decrypt_RSA('priv.pem', ciphertext)
print(f"decrypted: {plaintext}\n")


def sign_data(private_key_file, data):
    key = RSA.importKey(open(private_key_file).read())
    h = SHA256.new()
    h.update(data)
    signer = PKCS1_PSS.new(key)
    signature = signer.sign(h)

    return signature


def verify_sign(public_key_file, sign, data):
    key = RSA.importKey(open(public_key_file).read())
    h = SHA256.new()
    h.update(data)
    verifier = PKCS1_PSS.new(key)
    return verifier.verify(h, sign)


data = b'hi there!'
signature = sign_data('priv.pem', data)
print(f"sign match: {verify_sign('pub.pem', signature, data)}\n")

## protocol attack
print("encrypting:\n100\n")
y = encrypt_RSA('pub.pem', "100")
y_s = encrypt_RSA('pub.pem', "2")
m = get_byte_from_int(get_int_from_byte(y) * get_int_from_byte(y_s))

print(f"result:\n{y}\n")
print(f"modified to:\n{m}\n")
try:
    m_decrypted = decrypt_RSA('priv.pem', m)
    print(f"decrypted:\n{m_decrypted}\n")
except ValueError:
    print(ValueError)
## cant decrypt. incorrect length

##
import random

digest = SHA256.new()
digest.update(get_byte_from_int(2))
s = digest.hexdigest()

print(f"signature: {s}")

x = sign_data('priv.pem', s.encode())
x_prime = sign_data('priv.pem', s.encode())

print(f"x == x_prime: {x == x_prime}")
print()
