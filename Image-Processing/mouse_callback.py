#-*- coding:utf-8 -*-
import cv2
import numpy as np

drawing = False #Mouse가 클릭된 상태 확인용
mode = True # True이면 사각형, false면 원
ix, iy = -1, -1


# Mouse Callback함수
# def draw_circle(event, x, y, flags, param):
#     global ix, iy, drawing, mode
#
#     if event == cv2.EVENT_LBUTTONDOWN: #마우스를 누른 상태
#         drawing = True
#         ix, iy = x, y
#
#     elif event == cv2.EVENT_MOUSEMOVE: # 마우스 이동
#         if drawing == True:
#             if mode == True:
#                 cv2.rectangle(img, (ix, iy), (x, y), (255, 0, 0), -1)
#             else:
#                 cv2.circle(img, (x,y), 5, (0,255,0), -1)
#
#     elif event == cv2.EVENT_LBUTTONUP:
#         drawing = False # 마우스를 때면 상태 변경
#         if mode == True:
#             cv2.rectangle(img, (ix, iy), (x, y), (255, 0, 0), -1)
#         else:
#             cv2.circle(img, (x,y), 5, (0, 255, 0), -1)
box = []
def zoom_event(event, x, y, flags, param):
    global ix, iy, zoom


    if event == cv2.EVENT_LBUTTONDOWN:
        zoom = True
        print('start mouse, x=', x,'y=', y)
        start_box = [x, y]
        box.append(start_box)

    elif event == cv2.EVENT_LBUTTONUP:
        print('end mouse. x=', x, 'y=', y)
        zoom = False
        end_box = [x, y]
        box.append(end_box)
        print(box)

img = np.zeros((512, 512, 3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image', zoom_event)

while True:
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == 27:
        break

cv2.destroyAllWindows()

# import numpy as np
# import cv2
#
# boxes = []
#
# def on_mouse(event, x, y, flags, params):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         print 'Start Mouse Position: '+str(x)+', '+str(y)
#         sbox = [x, y]
#         boxes.append(sbox)
#
#     elif event == cv2.EVENT_LBUTTONUP:
#         print 'End Mouse Position: '+str(x)+', '+str(y)
#         ebox = [x, y]
#         boxes.append(ebox)
#         print(boxes)
#         crop = img[boxes[-2][1]:boxes[-1][1], boxes[-2][0]:boxes[-1][0]]
#
#         cv2.imshow('crop', crop)
#
#
# count = 0
# while(1):
#     count += 1
#     img = cv2.imread('test.jpeg',0)
#     img = cv2.blur(img, (3,3))
#
#     cv2.namedWindow('real image')
#     cv2.setMouseCallback('real image', on_mouse, 0)
#     cv2.imshow('real image', img)
#     if count < 50:
#         if cv2.waitKey(33) == 27:
#             cv2.destroyAllWindows()
#             break
#     elif count >= 50:
#         if cv2.waitKey(0) == 27:
#             cv2.destroyAllWindows()
#             break
#         count = 0