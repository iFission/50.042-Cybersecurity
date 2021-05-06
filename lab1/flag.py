#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Simple file read in/out
# 1003474
# Alex W

import os
from tqdm import tqdm
import multiprocessing


def deDecrypt(key):
    os.system(
        f'python3 shift_cipher_binary.py -i flag -o flag{key}.png -m d -k {key}'
    )


def checkPng(key):
    if "PNG image data" in os.popen(f'file flag{key}.png').read():
        print("found!")
        print(f'key is {key}')


if __name__ == "__main__":
    processes = []

    for key in tqdm(range(0, 256)):
        decrypt = multiprocessing.Process(target=deDecrypt, args=[key])
        processes.append(decrypt)
        decrypt.start()

    for proc in processes:
        proc.join()

    processes = []
    for key in tqdm(range(0, 256)):
        check = multiprocessing.Process(target=checkPng, args=[key])
        processes.append(check)
        check.start()

    for proc in processes:
        proc.join()