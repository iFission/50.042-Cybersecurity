#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Simple file read in/out
# 1003474
# Alex W

import os
from tqdm import tqdm
import multiprocessing

import string


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


def deDecrypt(key):
    with open(f"flag{key}.txt", "w") as f:
        output = do_caeser(
            "HE UAL WSCAD EPAE EPCDC UAL ASDCAMF AZ GZMCDLEAZMHZO YCEUCCZ EPCT AZM EPAE EPCF PAM TCE YF AJJIHZETCZE. EPCF UCDC UASRHZO LSIUSF ASIZO HZ MCCJ WIZXCDLAEHIZ, AZM H LAU PCD TARHZO KGHWR SHEESC TIXCTCZEL IN PCD PAZML AL HN LPC UCDC XCDF CADZCLE HZ UPAE LPC UAL LAFHZO, UPHSC PC SHLECZCM HZECZESF, AZM IZWC ID EUHWC LPIIR PHL PCAM HZ LEDIZO MHLLCZE. H LEIIM ATIZO EPC DIWRL UAEWPHZO EPCT, XCDF TGWP JGBBSCM AL EI UPAE H LPIGSM MI ZCVE. EI NISSIU EPCT AZM YDCAR HZEI EPCHD HZEHTAEC WIZXCDLAEHIZ LCCTCM EI YC AZ IGEDAOC, AZM FCE TF WSCAD MGEF UAL ZCXCD NID AZ HZLEAZE EI SCE PHT IGE IN TF LHOPE. EI AWE EPC LJF GJIZ A NDHCZM UAL A PAECNGS EALR. LEHSS, H WIGSM LCC ZI YCEECD WIGDLC EPAZ EI IYLCDXC PHT NDIT EPC PHSS, AZM EI WSCAD TF WIZLWHCZWC YF WIZNCLLHZO EI PHT ANECDUADML UPAE H PAM MIZC. HE HL EDGC EPAE HN AZF LGMMCZ MAZOCD PAM EPDCAECZCM PHT H UAL EII NAD AUAF EI YC IN GLC, AZM FCE H AT LGDC EPAE FIG UHSS AODCC UHEP TC EPAE EPC JILHEHIZ UAL XCDF MHNNHWGSE, AZM EPAE EPCDC UAL ZIEPHZO TIDC UPHWP H WIGSM MI.",
            key, "DECRYPT")
        f.write(output)


def checkText(key):
    if "THE" in os.popen(f'cat flag{key}.txt').read():
        print("found!")
        print(f'key is {key}')


if __name__ == "__main__":
    processes = []

    for key in tqdm(range(0, 26)):
        decrypt = multiprocessing.Process(target=deDecrypt, args=[key])
        processes.append(decrypt)
        decrypt.start()

    for proc in processes:
        proc.join()

    processes = []
    for key in tqdm(range(0, 26)):
        check = multiprocessing.Process(target=checkText, args=[key])
        processes.append(check)
        check.start()

    for proc in processes:
        proc.join()