#!/usr/bin/env python3
# ECB wrapper skeleton file for 50.042 FCS
# 1003474
# Alex W

from present import *
import argparse
import math
from tqdm import tqdm

nokeybits = 80
blocksize = 64


def get_block_binary_from_bytes(bytes_in):
    block_binary = ''
    for byte in bytes_in:
        block_binary += f"{bin(byte).lstrip('0b'):0>8}"

    return block_binary


def get_bytes_from_block_binary_int(binary_in):

    return binary_in.to_bytes(8, byteorder='big')


def ecb(infile, outfile, keyfile, mode):
    key = -1
    with open(keyfile, 'r') as f:
        key = get_hex_int(f.read())
        print(key)

    fin = open(infile, mode='rb')
    fout = open(outfile, mode='wb')

    infile_hex = fin.read()

    encrypted_blocks = b''

    if mode == 'e':

        for i in tqdm(range(math.ceil(len(infile_hex) / 8))):

            block_bytes = infile_hex[i * 8:i * 8 + 8]

            if len(block_bytes) < 8:
                block_bytes = block_bytes.ljust(8, b'0')

            block_binary_string = get_block_binary_from_bytes(block_bytes)
            block_binary_int = get_bin_int(block_binary_string)
            encrypted_block_int = present(block_binary_int, key)
            encrypted_block_bytes = get_bytes_from_block_binary_int(
                encrypted_block_int)

            encrypted_blocks += encrypted_block_bytes

    elif mode == 'd':

        for i in tqdm(range(math.ceil(len(infile_hex) / 8))):

            block_bytes = infile_hex[i * 8:i * 8 + 8]
            block_binary_string = get_block_binary_from_bytes(block_bytes)
            block_binary_int = get_bin_int(block_binary_string)
            encrypted_block_int = present_inv(block_binary_int, key)
            encrypted_block_bytes = get_bytes_from_block_binary_int(
                encrypted_block_int)

            if i == len(infile_hex) // 8 - 1:
                encrypted_block_bytes = encrypted_block_bytes.rstrip(b'0')

            encrypted_blocks += encrypted_block_bytes

    fout.write(encrypted_blocks)

    fin.close()
    fout.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Block cipher using ECB mode.')
    parser.add_argument('-i', dest='infile', help='input file')
    parser.add_argument('-o', dest='outfile', help='output file')
    parser.add_argument('-k', dest='keyfile', help='key file')
    parser.add_argument('-m',
                        dest='mode',
                        help='mode, e for encryption, d for decryption')

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    keyfile = args.keyfile
    mode = args.mode

    ecb(infile, outfile, keyfile, mode)
