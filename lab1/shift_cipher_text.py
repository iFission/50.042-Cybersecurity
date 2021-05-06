#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Simple file read in/out
# 1003474
# Alex W

# Import libraries
import sys
import argparse
import string


def encrypt(char, key):
    return (string.printable[(string.printable.index(char) + key) % 100])


def decrypt(char, key):
    return encrypt(char, -key)


def doStuff(filein, fileout, key, mode):

    CHAR_SIZE = len(string.printable)
    # error checking
    if mode != "d" and mode != "e":
        raise SyntaxError('mode must be "e" or "d"')

    if key < 1 or key > (CHAR_SIZE - 1):
        raise ValueError(
            'The key must be between 1 and len(string.printable) (100) - 1')

    print(f"mode: {mode}")
    print(f"key: {key}")

    # open file handles to both files
    fin = open(filein, mode='r', encoding='utf-8', newline='\n')  # read mode
    fin_b = open(filein, mode='rb')  # binary read mode
    fout = open(fileout, mode='w', encoding='utf-8',
                newline='\n')  # write mode
    fout_b = open(fileout, mode='wb')  # binary write mode
    c = fin.read()  # read in file into c as a str

    # do shift
    output = ""
    if mode == "e":
        output = "".join([encrypt(char, key) for char in c])
    if mode == "d":
        output = "".join([decrypt(char, key) for char in c])

    # print for 10 chars for sanity check
    print(output[:10])

    # and write to fileout
    fout.write(output)

    # close all file streams
    fin.close()
    fin_b.close()
    fout.close()
    fout_b.close()


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
