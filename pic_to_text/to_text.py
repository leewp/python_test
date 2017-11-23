#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
from PIL import Image

parser = argparse.ArgumentParser(description='Convert picture to text')
parser.add_argument('ori_file', metavar='str', help='The origin picture path')
parser.add_argument('-o', '--out', default='out.txt', metavar='str', type=str,
                    help='The output text file path')
parser.add_argument('-w', '--weight', default='80', metavar='int', type=int,
                    help='The output text weight')
parser.add_argument('-hei', '--height', default='80', metavar='int', type=int,
                    help='The output text height')
args = parser.parse_args()

FILE = args.ori_file
OUTPUT = args.out
WEIGHT = args.weight
HEIGHT = args.height
SYMBOLS = '~!@#$%^&*()_+~!@#$%^&*()_+'
print FILE
# Gray = (R * 299 + G * 587 + B * 114 + 500) / 1000


def get_symbol(r, g, b, w):
    if w == 0:
        return ' '
    gray = (r * 299 + g * 587 + b * 114 + 500)/1000
    return SYMBOLS[gray % len(SYMBOLS)]


with open(OUTPUT, 'w') as out_file:
    print 'Wait, dealing...'
    with Image.open(FILE) as im:
        im = im.resize((WEIGHT, HEIGHT), Image.NEAREST)
        for j in range(0, HEIGHT):
            for i in range(0, WEIGHT):
                cur_sym = get_symbol(*im.getpixel((i, j)))
                out_file.write(cur_sym)
                out_file.write(cur_sym)
            out_file.write('\n')
            print 'finish %d%%' % (j * 100 / (HEIGHT-1))
    print 'Finished, output file is', OUTPUT





