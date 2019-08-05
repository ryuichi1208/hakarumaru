#!/usr/bin/env python3

import os
import sys
import random

def main():
    with open("data", "wb") as fout:
        bary = bytearray([0xFF, 0x12, 0x89])
        bary.append(0)
        bary.extend([1, 127])
        fout.write(bary)

if __name__ == "__main__":
    main()
