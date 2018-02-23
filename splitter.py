#!/usr/bin/env python

import argparse
import math
import os
from PIL import Image


def ensuredir(outdir):
    if not os.path.isdir(outdir):
        os.mkdir(outdir)


def split(imgpath, twidth, theight, margin, spacing, outdir):
    ensuredir(outdir)

    img = Image.open(imgpath)
    w, h = img.size
    cols = (w + spacing - 2 * margin) / (twidth + spacing)
    rows = (h + spacing - 2 * margin) / (theight + spacing)
    ntiles = cols * rows

    for i in range(int(ntiles)):
        path = os.path.join(outdir, f'{i+1}.png')
        ox = (i % cols) * (twidth + spacing) + margin
        oy = math.floor(i / cols) * (theight + spacing) + margin
        img.crop((ox, oy, ox + twidth, oy + theight)).save(path)


if __name__ == '__main__':
    p = argparse.ArgumentParser(conflict_handler='resolve')
    p.add_argument('imgpath', metavar='image', help='the sprite sheet to split')
    p.add_argument('-w', '--width', type=int, dest='twidth', required=True, help='tile width')
    p.add_argument('-h', '--height', type=int, dest='theight', required=True, help='tile height')
    p.add_argument('-m', '--margin', type=int, default=0, help='sprite sheet margin')
    p.add_argument('-s', '--spacing', type=int, default=0, help='space between tiles')
    p.add_argument('-o', '--outdir', default='.', help='destination directory')
    split(**vars(p.parse_args()))
