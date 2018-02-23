#!/usr/bin/env python

import argparse
import math
import os
from PIL import Image


def ensuredir(outdir):
    if not os.path.isdir(outdir):
        os.mkdir(outdir)


def extrude(imgpath, twidth, theight, margin, spacing, outdir, quantize):
    ensuredir(outdir)

    img = Image.open(imgpath)
    w, h = img.size
    cols = int((w + spacing - 2 * margin) / (twidth + spacing))
    rows = int((h + spacing - 2 * margin) / (theight + spacing))
    ntiles = cols * rows

    extruded = Image.new('RGBA', (w + 2 * cols, h + 2 * rows), (255, 0, 0, 0))
    for i in range(int(ntiles)):
        col = i % cols
        row = math.floor(i / cols)

        ox = col * (twidth + spacing) + margin
        oy = row * (theight + spacing) + margin
        quad = img.crop((ox, oy, ox + twidth, oy + theight))

        eox = ox + 2 * col + 1
        eoy = oy + 2 * row + 1
        extruded.paste(quad, (eox, eoy))

        # duplicate quad borders
        top = extruded.crop((eox, eoy, eox + twidth, eoy + 1))
        extruded.paste(top, (eox, eoy - 1))

        right = extruded.crop((eox + twidth - 1, eoy - 1, eox + twidth, eoy + theight))
        extruded.paste(right, (eox + twidth, eoy - 1))

        bottom = extruded.crop((eox, eoy + theight - 1, eox + twidth + 1, eoy + theight))
        extruded.paste(bottom, (eox, eoy + theight))

        left = extruded.crop((eox, eoy - 1, eox + 1, eoy + theight + 1))
        extruded.paste(left, (eox - 1, eoy - 1))

    if quantize:
        extruded = extruded.convert('P', palette=Image.ADAPTIVE, colors=256)

    path = os.path.join(outdir, f'{os.path.splitext(imgpath)[0]}_extruded.png')
    print(f'Saving modified file to {path}')
    extruded.save(path)


if __name__ == '__main__':
    p = argparse.ArgumentParser(conflict_handler='resolve')
    p.add_argument('imgpath', metavar='image', help='the sprite sheet to split')
    p.add_argument('-w', '--width', type=int, dest='twidth', required=True, help='tile width')
    p.add_argument('-h', '--height', type=int, dest='theight', required=True, help='tile height')
    p.add_argument('-m', '--margin', type=int, default=0, help='sprite sheet margin')
    p.add_argument('-s', '--spacing', type=int, default=0, help='space between tiles')
    p.add_argument('-q', '--quantize', action='store_true', help='quantize the output image')
    p.add_argument('-o', '--outdir', default='.', help='destination directory')
    extrude(**vars(p.parse_args()))
