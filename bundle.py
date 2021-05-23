#!/usr/bin/env python

import os
import shutil
import subprocess

bundle_dir = 'bundle'
img_formats = {
    'jpeg',
    'jpg',
    'png',
    'svg',
    'webp',
}
max_size = 2**21
blacklist = {
    # Is animation, shouldbe gif...
    'Li_Hongzhi_dubstep.webp',

    # Backup only.
    'That_Rabbit_cute_transparent_background.png',

    # Stack Exchange are Nazis.
    'Qing_Dinasty_gay_foreplay.jpg',
    'Rugae_vaginales_with_black_hole.jpg',
}

def convert(running_list, output_index):
    # print(
    subprocess.run(
        [
            'convert',
            '-append',
        ] +
        running_list +
        [
            '-resize',
            '600x',
            os.path.join(bundle_dir, "{:02d}".format(output_index)) + '.jpg'
        ]
    )

shutil.rmtree(bundle_dir)
os.mkdir(bundle_dir)
output_index = 0
running_size = 0
running_list = []
for f in sorted(os.listdir()):
    if os.path.splitext(f)[1][1:] in img_formats and not f in blacklist:
        cur_size = os.path.getsize(f)
        if running_size + cur_size < max_size:
            running_size += cur_size
            running_list.append(f)
        else:
            print(output_index)
            print(cur_size)
            print()
            convert(running_list, output_index)
            running_size = cur_size
            running_list = []
            output_index += 1
convert(running_list, output_index)
