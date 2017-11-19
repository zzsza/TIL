# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import argparse
import sys

import image_viewer

print("python version : {version}".format(version=sys.version))


parser = argparse.ArgumentParser()
parser.add_argument("--folder_path", help="folder path", default="./")
parser.add_argument("--show_flag", help="'color' or 'gray'", default='color', type=str)
parser.add_argument("--size_flag", help="window_size : auto, normal, full", default='auto', type=str)
parser.add_argument("--crop_mode", help="crop_mode : 'True' or 'False' ", default=False, type=bool)

args = parser.parse_args()

image_extension = ('jpg', 'jpeg', 'png')  
current_folder = args.folder_path
image_file = [i for i in os.listdir(current_folder) if i.endswith(image_extension) == True]
print("current folder path : {current_folder}\nimage 개수 : {len_image}\nimage file : {image_file}".format(
    current_folder=current_folder, len_image=len(image_file), image_file=image_file
))

a = raw_input("몇번째 이미지를 보여드릴까요?\n")
try:
    selected_image = image_file[int(a) - 1]
    print(selected_image)
except IndexError:
    print("1부터 {n}까지의 숫자를 입력해주세요".format(n=len(image_file)))
finally:
    if int(a) <= 0:
        print("양수를 입력해주세요")


def main(selected_image):
    if args.crop_mode == True:
        op = image_viewer.ImageViewer(args)
        op.crop_image(selected_image)

    else:
        op = image_viewer.ImageViewer(args)
        op.show_image(selected_image)

if __name__ == '__main__':
    main(selected_image)