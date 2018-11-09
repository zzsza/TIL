# -*- coding: utf-8 -*-
import cv2
import os
import numpy as np
import sys
print("python version : {version}".format(version=sys.version))

def show_image(image_files, now_order, len_image, show_flag='color', size_flag='full'):
    global image, refPt

    flag = show_type(show_flag)
    size_flag = window_size(size_flag)
    image = cv2.imread(image_files[int(now_order)], flag)
    y, x = image.shape[:2]

    cv2.namedWindow('viewer', size_flag)
    cv2.setMouseCallback("viewer", crop_callback)
    clone = image.copy()
    now_order = int(now_order)

    color_mode = True

    while True:
        cv2.imshow('viewer', image)
        key = cv2.waitKey(1) & 0xFF

        if key == 27: # ESC
            quit()

        elif key == 2: # <
            if now_order <= 0:
                now_order = now_order + len_image - 1
            else:
                now_order -= 1
            image_file = image_files[now_order]
            print(image_file)
            image = cv2.imread(image_file)
            clone = image.copy()
            cv2.imshow("viewer", image)

        elif key == 3: # >
            if now_order+1 >= len_image:
                now_order = now_order - len_image + 1
            else:
                now_order += 1
            image_path = image_files[now_order]
            print(image_path)
            image = cv2.imread(image_path)
            clone = image.copy()
            cv2.imshow("viewer", image)

        elif key == ord("r"):
            image = clone.copy()
            refPt = []

        elif key == ord("c"):
            if len(refPt) == 2:
                crop = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
                cv2.resize(crop, (x, y), fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                cv2.imshow("viewer", crop)
                cv2.waitKey(0)

            else:
                print('There is a no rectangle..')

        elif key == ord("g"):
            if color_mode == True:
                image_file = image_files[now_order]
                image = cv2.imread(image_file, 0)
                cv2.imshow("viewer", image)
                color_mode = False

            else:
                image_file = image_files[now_order]
                image = cv2.imread(image_file)
                cv2.imshow("viewer", image)
                color_mode = True


def crop_callback(event, x, y, flags, param):
    global refPt, cropping

    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False

        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        print(refPt[0], refPt[1])
        cv2.imshow("viewer", image)



def show_type(style):
    if style == 'color':
        return 1
    elif style == 'gray':
        return 0
    else:
        return -1

def window_size(size_flag):
    if size_flag == 'auto':
        return cv2.WINDOW_AUTOSIZE
    elif size_flag == 'normal':
        return cv2.WINDOW_NORMAL
    elif size_flag == 'full':
        return cv2.WINDOW_FULLSCREEN

def zoom(img):
    '''
    2배로 zoom
    '''
    image = cv2.imread(img)

    zoom = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    cv2.imshow('viewer', zoom)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def bbox(img):
    image = cv2.imread(img)
    r = cv2.selectROI(image)
    crop = image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    cv2.imshow("viewer", crop)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




refPt = []
cropping = False
zoom = False

image_extension = ('jpg', 'jpeg', 'png')
current_folder = os.getcwd()
print(current_folder)
image_files = [i for i in os.listdir(current_folder) if i.endswith(image_extension) is True]

if image_files == []:
    print("현재 폴더 내에 이미지 파일이 없습니다")
else:
    print("현재 폴더 경로 : {current_folder}\nimage 개수 : {len_image}\nimage file : {image_file}".format(
        current_folder=current_folder, len_image=len(image_files), image_file=image_files
    ))

    input = input("몇번째 이미지를 보여드릴까요?\n")
    try:
        now_order = int(input) - 1
        selected_image = image_files[int(input)-1]
        print(selected_image)
    except IndexError:
        print("1부터 {n}까지의 숫자를 입력해주세요".format(n=len(image_files)))
        
    else:
        if int(input) <= 0:
            print("양수를 입력해주세요")
        else:
            print('error')

    show_image(image_files, now_order=now_order, len_image=len(image_files))

