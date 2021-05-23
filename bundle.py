#!/usr/bin/env python

import os
import shutil
import subprocess
import sys

if len(sys.argv) > 1:
    max_size = int(sys.argv[1])
else:
    max_size = 2**21

bundle_dir = 'bundle'
img_formats = {
    'jpeg',
    'jpg',
    'png',
    'svg',
    'webp',
}
blacklist = {
    # Is animation, shouldbe gif...
    'Li_Hongzhi_dubstep.webp',

    # Backup only.
    'That_Rabbit_cute_transparent_background.png',
    'Mashimaro.png',

    # Stack Exchange are Nazis.
    'Qing_Dinasty_gay_foreplay.jpg',
    'Jin_ping_mei.jpg',
    'Rugae_vaginales_with_black_hole.jpg',
}

def convert(running_list, output_index):
    # https://stackoverflow.com/questions/20737061/merge-images-side-by-sidehorizontally/63575228#63575228
    out = os.path.join(bundle_dir, "{:02d}".format(output_index)) + '.jpg'
    subprocess.run(
        [
            'convert',
            '-append',
        ] +
        running_list +
        [
            '-resize',
            '600x',
            out
        ]
    )
    return os.path.getsize(out)

shutil.rmtree(bundle_dir)
os.mkdir(bundle_dir)
output_index = 0
running_size = 0
running_list = []
for f in sorted(os.listdir()):
    if os.path.splitext(f)[1][1:] in img_formats and not f in blacklist:
        cur_size = os.path.getsize(f)
        if cur_size < max_size:
            if running_size + cur_size > max_size:
                print(output_index)
                leftover_running_size = 0
                leftover_running_list = []
                while convert(running_list, output_index) > max_size:
                    print('retry')
                    rm_p = running_list.pop()
                    leftover_running_list.append(rm_p)
                    leftover_running_size += os.path.getsize(rm_p)
                leftover_running_list.reverse()
                running_size = leftover_running_size
                running_list = leftover_running_list
                output_index += 1
            running_size += cur_size
            running_list.append(f)
if running_list:
    convert(running_list, output_index)
