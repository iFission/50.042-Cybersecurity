#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Simple file read in/out
# 1003474
# Alex W

# Import libraries
import sys
import argparse
import string


def encrypt(byte, key):
    return ((ord(byte) + key) % 256)


def decrypt(byte, key):
    return encrypt(byte, -key)


def doStuff(filein, fileout, key, mode):

    CHAR_SIZE = len(string.printable)
    # error checking
    if mode != "d" and mode != "e":
        raise SyntaxError('mode must be "e" or "d"')

    if key < 0 or key > 255:
        raise ValueError('The key must be between 0 and 255')

    # print(f"mode: {mode}")
    # print(f"key: {key}")

    # open file handles to both files
    fin = open(filein, mode='rb')  # binary read mode
    fout = open(fileout, mode='wb')  # binary write mode
    # c = fin.read()  # read in file into c as a str
    # print(c)

    output = bytearray()

    byte = fin.read(1)
    while byte:
        if mode == "e":
            output.append(encrypt(byte, key))
        if mode == "d":
            output.append(decrypt(byte, key))
        byte = fin.read(1)

    # do shift
    # output = ""

    # print for 10 chars for sanity check
    # print(output[:10])

    # and write to fileout
    fout.write(output)

    # close all file streams
    fin.close()
    fout.close()


# our main function
if __name__ == "__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='filein', help='input file')
    parser.add_argument('-o', dest='fileout', help='output file')
    parser.add_argument('-k', dest='key', help='key')
    parser.add_argument('-m', dest='mode', help='d or e')

    # parse our arguments
    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout
    key = int(args.key)
    mode = args.mode

    doStuff(filein, fileout, key, mode)

    # all done
