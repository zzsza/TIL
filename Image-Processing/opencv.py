# -*- coding: utf-8 -*-
import cv2
import os
import numpy as np
import sys
print("python version : {version}".format(version=sys.version))
'''
요구 사항
1. Image Load & Search in directory
    - 현재 폴더 출력 : done
    - 현재 폴더의 이미지 출력 (확장자는 확장성 있게) : done
    - 현재 폴더의 이미지 개수 출력 : done
    - 현재 폴더의 이미지에서 숫자를 입력하면, 해당 파일이 open되도록 : done
2. Image Value read & View
    - RGB로 띄우기 : done
    - gray로 띄우기 : done
    - 버튼에 rgb <-> gray change? 
3. Auto window size, editing window size
    - autosize flag : done
    - edit window size : done
    - 크기를 늘리면 자동으로 이미지도 늘어나게
4. zooming + moving
    - zooming
    - moving    
    
5. bbox size, position check

추가 사항
6. crop : done

7. class화

'''
#1
def show_image(img, show_flag='color', size_flag='auto'):
    flag = show_type(show_flag)
    image = cv2.imread(img, flag)
    size_flag = window_size(size_flag)
    cv2.namedWindow('image', size_flag)
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def crop_image(img):
    global image
    image = cv2.imread(img)
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_crop)

    while True:
        cv2.imshow('image', image)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"):
            image = clone.copy()

        elif key == ord("c"):
            break

    if len(refPt) == 2:
        crop = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        cv2.imshow("crop", crop)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def click_crop(event, x, y, flags, param):
    global refPt, cropping

    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False

        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", image)


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
    cv2.imshow('zoom', zoom)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

refPt = []
cropping = False

image_extension = ('jpg','jpeg','png') # 이미지 확장자
current_folder = os.getcwd() # 현재 폴더
print(current_folder)
image_file = [i for i in os.listdir(current_folder) if i.endswith(image_extension)==True]
print("current folder path : {current_folder}\nimage 개수 : {len_image}\nimage file : {image_file}".format(
    current_folder=current_folder, len_image=len(image_file), image_file=image_file
))

a = raw_input("몇번째 이미지를 보여드릴까요?\n")
try:
    selected_image = image_file[int(a)-1]
    print(selected_image)
except IndexError:
    print("1부터 {n}까지의 숫자를 입력해주세요".format(n=len(image_file)))
finally:
    if int(a)<=0:
        print("양수를 입력해주세요")

# show_image(selected_image)
# zoom(selected_image)
crop_image(selected_image)