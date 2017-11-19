# -*- coding: utf-8 -*-
import cv2
import os
import numpy as np

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

class ImageViewer:
    refPt = []
    cropping = False

    def __init__(self, args):
        self.args = args

    def show_image(self, img):
        flag = show_type(self.args.show_flag)
        image = cv2.imread(img, flag)
        size_flag = window_size(self.args.size_flag)
        cv2.namedWindow('image', int(size_flag))
        cv2.imshow('image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def crop_image(self, img):
        global image

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



