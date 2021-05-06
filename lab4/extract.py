#!/usr/bin/env python3
# ECB plaintext extraction skeleton file for 50.042 FCS
# 1003474
# Alex W

import argparse
from collections import Counter


def getInfo(headerfile):
    header = []
    header_length = -1
    with open(headerfile, 'rb') as f:
        header = f.read()
        header_length = len(header)

    return header, header_length


def extract(infile, outfile, headerfile):
    header, header_length = getInfo(headerfile)
    encrypted = []

    with open(infile, 'rb') as fin:
        fin.read(header_length + 1)
        while True:
            byte_in = fin.read(8)
            if byte_in == b"":
                break
            else:
                encrypted.append(byte_in)

    # find the block with highest frequency
    block_frequency = dict(Counter(encrypted))

    frequency = -1
    for block, count in block_frequency.items():
        if count > frequency:
            highest_freuqency_block = block
            frequency = count

    # decrypt based on freuqency
    # assign highest freuqency as 11111111
    # others all 00000000
    decrypted = [
        b'0' * 8 if block == highest_freuqency_block else b'1' * 8
        for block in encrypted
    ]

    # combine decrypted bytes
    decrypted = "".join([block.decode() for block in decrypted]).encode()

    with open(outfile, 'wb') as fout:

        # write header, then add \n for a total of 16 bytes
        fout.write(header)
        fout.write(b'\n')
        fout.write(decrypted)
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract PBM pattern.')
    parser.add_argument('-i',
                        dest='infile',
                        help='input file, PBM encrypted format')
    parser.add_argument('-o', dest='outfile', help='output PBM file')
    parser.add_argument('-hh', dest='headerfile', help='known header file')

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    headerfile = args.headerfile

    print('Reading from: %s' % infile)
    print('Reading header file from: %s' % headerfile)
    print('Writing to: %s' % outfile)

    success = extract(infile, outfile, headerfile)
