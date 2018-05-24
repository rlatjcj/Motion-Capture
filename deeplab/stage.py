
import cv2
import numpy as np

BOUNDING_COLOR_PRINT = (255,255,0)
BOUNDING_COLOR = 100

def rect_big(width, height, img, flag=True):
    rect_width = width * 3 // 5
    rect_height = height * 4 // 5

    if flag == True:
        bounding = cv2.rectangle(np.zeros((height, width), dtype=np.uint8),
                    ((width-rect_width)//2, height-rect_height),
                    ((width+rect_width)//2, height), BOUNDING_COLOR, -1)

        return bounding, rect_width*rect_height
        
    else:
        img_print = cv2.rectangle(img, ((width-rect_width)//2, height-rect_height),
                    ((width+rect_width)//2, height), BOUNDING_COLOR_PRINT, 2)

        return img_print
