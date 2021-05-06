### 1003474

### Alex W

# Hand-in 1

## Demo encryption and decryption of RSA.

```python
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
```

output

```
rsakey_pub: Public RSA key at 0x10831F730
rsakey_pub.n: 137192589322920327798304066868257366048326623046604842601193496000910399102562405373359280553440670985475795574105894521657759283605443557241656006865467645448801936165354794569302265024976811574523608278505147998805396231259620157290521848208504333356832707853164915965378308417687191119796948698492728174051
rsakey_pub.e: 65537
rsakey_priv: Private RSA key at 0x1083DE100
rsakey_priv.n: 137192589322920327798304066868257366048326623046604842601193496000910399102562405373359280553440670985475795574105894521657759283605443557241656006865467645448801936165354794569302265024976811574523608278505147998805396231259620157290521848208504333356832707853164915965378308417687191119796948698492728174051
rsakey_priv.d: 12585285365662099435790531303110659393663726715537609498731637059332488814022692236517326009540951126305453148473757386883843459618779112045666355086061176783196094726614187589104240130162483582419440962475956215150067643140278221994821416389718381974591186996996702171475874701122021649864444006784578982945

message: hi there!~

message_encoded_int_encrypted: 124685623998621700508856700831650569405418535525995379229522738581756256897927080339460405699332768861906498481234164037136268073174171099243045789070411090261760250447822476075058862254702355586717300026974583164984707526649194866285061304900513113876812497864969802765754567726631555956036938491038987454672

message_encoded_decrypted: hi there!~
```

## Demo signing a message and verifying it.

```python
from Crypto.Hash import SHA256
h = SHA256.new()
h.update(b'Hello')
print(f"hash: {h.hexdigest()}")

sha256_signed = encrypt_string(h.hexdigest(), rsakey_priv.d, rsakey_priv.n)
sha256_verify = decrypt_string(sha256_signed, rsakey_pub.e, rsakey_pub.n)

print(f"verified hash: {sha256_verify}")
```

output

```
hash: 185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969
verified hash: 185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969
```

## Demo protocol attack to both encryption and digital signature.

### Attack on encryption

```python
print("encrypting:\n100\n")
y = encrypt(100, rsakey_pub.e, rsakey_pub.n)
y_s = encrypt(2, rsakey_pub.e, rsakey_pub.n)
m = y * y_s

m_decrypted = decrypt(m, rsakey_priv.d, rsakey_priv.n)
print(f"result:\n{y}\n")
print(f"modified to:\n{m}\n")
print(f"decrypted:\n{m_decrypted}\n")
```

output

```
encrypting:
100

result:
122958632740668866768666000464174722842511114811350455529516542396465965526253172448121048019762699874069569688906522114895853576958876108469062241665797249738074069489131133990226837557144423192495381999896877667248042608974978625187857286476284582122349548284682940363603261607393108918231380108825679302933

modified to:
14796556706011057421230602305486552248855745183143199315642325219206704758357951572333947812165594322525936201986586072256802300860610907816439523040098974520309157826018934980002674084491828123262159118849481716253756926787347167940620386104561283126035581194903376476228474799711343863604082255278522966753174088976398017000538593656460383458941014617614440903331271116320427652570995408643220625312445577753737142875044534634918823810106286129842096523799918473110015795370479699377112672572977460768165840036129318469705949144877519471734209850223440698043036440379920687994864307777969041101940061429449541589622

decrypted:
200
```

## Attack on digital signature

```python
import random

signature = SHA256.new()
signature.update(get_byte_from_int(2))
s = signature.hexdigest()

print(f"signature: {s}")

x = encrypt_string(s, rsakey_pub.e, rsakey_pub.n)
x_prime = encrypt_string(s, rsakey_pub.e, rsakey_pub.n)

print(f"x == x_prime: {x == x_prime}")
```

output

```
signature: dbc1b4c900ffe48d575b5da5c638040125f65db0fe3e24494b76ea986457d986
x == x_prime: True
```

## Explain the limitation of protocol attack.

RSA encryption protocol attack works only when signature is not used together with the original message. If signature is attached, it can be quickly verified that the cipher text was altered.

It also requires the attacker to know roughly the content of the message. Otherwise, he can't modify it purposefully.

# Hand-in 2

Published public key:

```
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDfks4quJinfGQPRFd/JnrlDPCR
duj29l0gfRL00N6FbWi5FmPzOMsE8z7Ds3YPO05hhPxx7Ecupvt8w54B+3CIoUDC
NcCnx+r+LD5M/7IlddVHHS4jmzPDFRsVZqdeROl0FKdJaX0bDJ8kVNqDq3OgOxHP
/YgWFPd3jltkqaHO4wIDAQAB
-----END PUBLIC KEY-----
```

friend sends me ciphertext, encrypted with my public key:

```python
plaintext = "hi alex!"
print(f"plaintext: {plaintext}\n")
ciphertext = encrypt_RSA('pub.pem', plaintext)
print(f"ciphertext: {ciphertext}\n")
```

i decrypt the ciphertext with my private key:

```
plaintext = decrypt_RSA('priv.pem', ciphertext)
print(f"decrypted: {plaintext}\n")
```

output

```
decrypted:'hi alex!
```

create data and digital signature to my friend:

```python
def sign_data(private_key_file, data):
    key = RSA.importKey(open(private_key_file).read())
    h = SHA256.new()
    h.update(data)
    signer = PKCS1_PSS.new(key)
    signature = signer.sign(h)

    return signature

data = b'hi there!'
signature = sign_data('priv.pem', data)
```

my friend verifies the data and signature:

```python
def verify_sign(public_key_file, sign, data):
    key = RSA.importKey(open(public_key_file).read())
    h = SHA256.new()
    h.update(data)
    verifier = PKCS1_PSS.new(key)
    return verifier.verify(h, sign)

print(f"sign match: {verify_sign('pub.pem', signature, data)}\n")
```

## Demo protocol attack to both encryption and digital signature.

### Attack on encryption

```python
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
```

output

```
encrypting:
100

result:
b'D\xbb\x08\xfeEL\xfd^\x93FY\xf5\xd1\x95\xe3`\x13\xf1?\xf1\xd6\xfa\x95A\xd5\xec\x04[^\xdd\x99\xc5\xe2\x14\x0c\x8ch\x8f\xc4\xa2\n"\x1b\xb5_\xda^=\x83-\xe6\xcb\x13\xc9)!>2.W$\x90ua\x89\x88#\x94KI\xe3\xa8t\x86\xdeL\xea\x0f\xeb\xc4\xe4\xf6\xa6\xe98[\xa5\x8cx\xf4;\x1a\xe1\xa4\xe6i\x8d\x9dh\x1e\xec\xa4d=qI\xfb\xbb`\x14\x92&d\x15*\x0f\xce\xf0z\xc4\x0c\xd2a\xa5T~;\xf6'

modified to:
b'!\xb6u@\xba\x8ePZ\xa8\xe1+\xf3\x9e\xac\x84-\x03T\xf9Z\x13\x84X\xb3q\xd0(\xc8M\xc9}\x85\xe4\xfa\xfa\n\x90\xe9\xe3\t7\x884:\x11G\xcc^J\xf4\xd9\xd3V\xd9\x97/\x84\xd8\x86Q8\xc4\x93\xe8G\x879\x1a\xf5+\xc4\xea\xb2\xd1\xfc\x9d\x86\xa3\x98\xb3l\xbf\x8fh\xce\xb7\x04\x93\xc9\x02\x85\xcd\xa5\xd3o|\xa8.\x14=;\xa3c\xffH.\xd2.\xdd\x19\x91Z\x8e\xf2\xb3\x82\x18\xb8\x08\x88T\x11\xef{\xe1\x9c(\xa7\x17\xf3\\\x1aR\xc0\n\xe2\xe0\x13\xe5\xdf\xe4\xf1\xcb\xfe\xa7\xd9\xc1xc\xc8\xe6\x17|\xbc\xcd\xe8\x9d\xeb\xc4K\x98G\xae8rB1\x81\x7f\xe6B\x8dx;\x87\xd5\x15\xe9\x94@=-J\x9c\xf8A\xbb\xc6u\xa9\xd1X\x0f\xd2c\xa9\xe8\x85\xba-\xd9\x97\x01F/\xa2\x10\x03-\xad\x96\x81_C\x08\\B\xd6x`\xf4\\\xd7\xea\x8dn-V\xaeY\xf5\xb3\xf4\xd4\xec"\xc4\x0b\x8a\xf8\xef1\xd4\xbc2\xff\xde\xe1V\xf2\xe2\x9b\x96\x04\xd6 '

Traceback (most recent call last):
  File "/Users/ALEX/Documents/Term 6/50.042 Cybersecurity/lab7/lab7.py", line 185, in <module>
    m_decrypted = decrypt_RSA('priv.pem', m)
  File "/Users/ALEX/Documents/Term 6/50.042 Cybersecurity/lab7/lab7.py", line 143, in decrypt_RSA
    plaintext = cipher.decrypt(ciphertext)
  File "/usr/local/lib/python3.8/site-packages/Crypto/Cipher/PKCS1_OAEP.py", line 167, in decrypt
    raise ValueError("Ciphertext with incorrect length.")
ValueError: Ciphertext with incorrect length.
```

Can't decrypt due to Ciphertext with incorrect length

## Attack on digital signature

```python
import random

digest = SHA256.new()
digest.update(get_byte_from_int(2))
s = digest.hexdigest()

print(f"signature: {s}")

x = sign_data('priv.pem', s.encode())
x_prime = sign_data('priv.pem', s.encode())

print(f"x == x_prime: {x == x_prime}")
print()
```

output

```
signature: dbc1b4c900ffe48d575b5da5c638040125f65db0fe3e24494b76ea986457d986
x == x_prime: False
```

Digital signature attack fails as the digital signature changes each time it is signed with private key

## Explain the purpose of Optimal Asymetric Encryption Padding (OAEP) to encrypt and de- crypt using RSA. Explain how it works.

Purpose: converts deterministic encryption scheme of RSA into a probabilistic scheme, using a random padding scheme. It prevents malleability of RSA.

How it works: It uses Feistel network with a pair of random oracle G and H to process the plaintext prior to asymmetric encryption.

Encryption

```
messages are padded with k1 zeros to be n − k0 bits in length
r is a randomly generated k0-bit string
G expands the k0 bits of r to n − k0 bits.
X = m00..0 ⊕ G(r)
H reduces the n − k0 bits of X to k0 bits.
Y = r ⊕ H(X)
The output is X || Y where X is shown in the diagram as the leftmost block and Y as the rightmost block
```

Decryption

```
recover the random string as r = Y ⊕ H(X)
recover the message as m00..0 = X ⊕ G(r)
```

## Explain the purpose of Probabilistic Signature Scheme (PSS) to sign and verify using RSA. Explain how it works.

Purpose: Generates different signature value each time. Requires message itself to verify signature, though the message is not recoverable from the signature.

How it works:
Encryption

```
1: Hash the message to be signed with a hash function.

2: The hash is transformed into an encoded message. This transformation operation uses padding which is random, integrating mask generation function.

3: A signature primitive is applied to the encoded message by using the private key to produce the signature
```

Verification

```
1: Hash the message to be signed with a hash function.

2: A verification primitive is then applied to the signature by using the public key of the key pair to recover the message.

3: Verify that the encoded message is a valid transformation of the hash value
```
