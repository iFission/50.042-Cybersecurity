### 1003474

### Alex W

# DHKE 4

## demo key exchange

run dhke.py, simulates generation of p, alpha, my private key, other private key, and shared key.

```bash
python3 dhke.py

Generate P and alpha:
P: 1066866953767767966985889
alpha: 964003671212914702038245
Length of p is 80 bits.

My private key is:  803621601571394732125375
Test other private key is:  663462369594397759780506

My public key is:  740305017435228433642667
Test other public key is:  296261542090770279913829
My shared key is:  146119882331721679175004
Test other shared key is:  146119882331721679175004
Length of key is 77 bits.
```

## PRESENT ECB

given shared key = `146119882331721679175004`

convert to hex, then store in key_shared file
`0x1ef12cb8b462737afd5c`

message stored in message.txt

```bash
cat message.txt
Input #1: n > 3, an odd integer to be tested for primality
Input #2: k, the number of rounds of testing to perform
Output: “composite” if n is found to be composite, “probably prime” otherwise

write n as 2r·d + 1 with d odd (by factoring out powers of 2 from n − 1)
WitnessLoop: repeat k times:
    pick a random integer a in the range [2, n − 2]
    x ← ad mod n
    if x = 1 or x = n − 1 then
        continue WitnessLoop
    repeat r − 1 times:
        x ← x2 mod n
        if x = n − 1 then
            continue WitnessLoop
    return “composite”
return “probably prime”
```

encrypt the message with the key file

```bash
python3 ecb.py -i message.txt -o message_encrypt.txt -k key_shared -m e
```

decrypt the message

```bash
python3 ecb.py -i message_encrypt.txt -o message_decrypt.txt -k key_shared -m d
```

check that message_decrypt.txt == message.txt

```bash
md5 message.txt message_decrypt.txt
MD5 (message.txt) = 46caaed7aab5fef600d9a006342b5dab
MD5 (message_decrypt.txt) = 46caaed7aab5fef600d9a006342b5dab
```

the md5 hashes are equal, hence the files are the same, shows that the shared key is successful in securing the communication.

## advantages, disadvantages

### advantage:

good against passive eavesdropper: costly to solve discrete log algorithm

### disadvantage:

not strong against MITM attack. if the attacker is able to intercept and alter the communication, he is able to decrypt message m, replace with whatever m' he chooses, without the recipients finding out.

if prime generator not chosen properly, then generator only generates to a small subgroup. easily guessable

# DHKE 6

### 16 bit

```
python3 dhke.py
Generate P and alpha:
P: 43891
alpha: 39713
Length of p is 16 bits.

My private key is:  13909
Test other private key is:  39769

My public key is:  18327
Test other public key is:  23176
My shared key is:  5995
Test other shared key is:  5995
Length of key is 13 bits.
```

```
time python3 babygiant.py
Guess key 1: 5995
Guess key 2: 5995
Actual shared key : 5995
/usr/local/bin/python3   0.03s user 0.01s system 92% cpu 0.046 total
```

### 20 bit

```
python3 dhke.py
Generate P and alpha:
P: 1035791
alpha: 462608
Length of p is 20 bits.

My private key is:  477082
Test other private key is:  167759

My public key is:  367074
Test other public key is:  236328
My shared key is:  912394
Test other shared key is:  912394
Length of key is 20 bits.
```

```
time python3 babygiant.py
Guess key 1: 912394
Guess key 2: 912394
Actual shared key : 912394
python3 babygiant.py  0.14s user 0.03s system 81% cpu 0.205 total
```

### 24 bit

```
python3 dhke.py
Generate P and alpha:
P: 16737893
alpha: 15631086
Length of p is 24 bits.

My private key is:  14096479
Test other private key is:  1395924

My public key is:  13900057
Test other public key is:  7004407
My shared key is:  14431287
Test other shared key is:  14431287
Length of key is 24 bits.
```

```
time python3 babygiant.py
Guess key 1: 14431287
Guess key 2: 14431287
Actual shared key : 14431287
python3 babygiant.py  3.06s user 0.04s system 99% cpu 3.118 total
```

### 26 bit

```
python3 dhke.py
Generate P and alpha:
P: 50721161
alpha: 16811197
Length of p is 26 bits.

My private key is:  35739742
Test other private key is:  47323310

My public key is:  38928455
Test other public key is:  49837238
My shared key is:  49911966
Test other shared key is:  49911966
Length of key is 26 bits.
```

```
time python3 babygiant.py
Guess key 1: 49911966
Guess key 2: 49911966
Actual shared key : 49911966
/usr/local/bin/python3   12.10s user 0.08s system 99% cpu 12.234 total
```

### 28 bit

```
python3 dhke.py
Generate P and alpha:
P: 213817207
alpha: 135520120
Length of p is 28 bits.

My private key is:  20652563
Test other private key is:  159298960

My public key is:  87759247
Test other public key is:  3524869
My shared key is:  170176823
Test other shared key is:  170176823
Length of key is 28 bits.
```

```
time python3 babygiant.py
Guess key 1: 170176823
Guess key 2: 170176823
Actual shared key : 170176823
python3 babygiant.py  93.55s user 0.54s system 99% cpu 1:34.46 total
```

from lecture, the time and space complexity of babygiant is `O(2^(n/2))`
from research online, key length is recommended to be at least 2048 bits to be practically resistant to babygiant.
