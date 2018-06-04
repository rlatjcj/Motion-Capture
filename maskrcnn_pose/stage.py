
import cv2
import numpy as np
import pygame

BOUNDING_COLOR_PRINT = (0,255,255)
BOUNDING_COLOR = 100


class DETERMINE_STAGE():

    def __init__(self, height, width):
        self.ROUND = 1
        self.height = height
        self.width = width
        self.version = 0

        self.ROUND_LIMIT = 3
        # the number of STAGEs for each round
        self.ROUND_1 = 1
        self.ROUND_2 = 2
        self.ROUND_3 = 1


    def determine_stage(self, img=None, flag=True):
        self.STAGE_LIST = {"1-0": self.rect_big,
                           "2-0": self.rect_thin,
                           "2-1": self.rect_fat,
                           "3-0": self.rect_air}.get("{}-{}".format(self.ROUND, self.version))

        return self.STAGE_LIST(img, flag)


    # 1-0 ROUND
    def rect_big(self, img=None, flag=True):
        if flag:
            seg_height = img.shape[0]
            seg_width = img.shape[1]
            rect_width = seg_width * 3 // 5
            rect_height = seg_height * 4 // 5
            bounding = cv2.rectangle(np.zeros((seg_height, seg_width), dtype=np.uint8),
                        ((seg_width-rect_width)//2, seg_height-rect_height),
                        ((seg_width+rect_width)//2, seg_height), BOUNDING_COLOR, -1)

            center = np.array([self.width//2, (2*self.height-rect_height)//2])

            return bounding, rect_width*rect_height, center

        else:
            rect_width = self.width * 3 // 5
            rect_height = self.height * 4 // 5
            pygame.draw.rect(img, BOUNDING_COLOR_PRINT,
                             ((self.width-rect_width)//2,
                             self.height-rect_height,
                             rect_width,
                             rect_height), 5)

            return img


    # 2-0 STAGE
    def rect_thin(self, img=None, flag=True):
        if flag:
            seg_height = img.shape[0]
            seg_width = img.shape[1]
            rect_width = seg_width * 2 // 5
            rect_height = seg_height * 4 // 5
            bounding = cv2.rectangle(np.zeros((seg_height, seg_width), dtype=np.uint8),
                        ((seg_width-rect_width)//2, seg_height-rect_height),
                        ((seg_width+rect_width)//2, seg_height), BOUNDING_COLOR, -1)

            center = np.array([self.width//2, (2*self.height-rect_height)//2])

            return bounding, rect_width*rect_height, center

        else:
            rect_width = self.width * 2 // 5
            rect_height = self.height * 4 // 5
            pygame.draw.rect(img, BOUNDING_COLOR_PRINT,
                             ((self.width-rect_width)//2,
                             self.height-rect_height,
                             rect_width,
                             rect_height), 5)

            return img

    # 2-1 STAGE
    def rect_fat(self, img=None, flag=True):
        if flag:
            seg_height = img.shape[0]
            seg_width = img.shape[1]
            rect_width = seg_width * 3 // 5
            rect_height = seg_height * 2 // 5
            bounding = cv2.rectangle(np.zeros((seg_height, seg_width), dtype=np.uint8),
                        ((seg_width-rect_width)//2, seg_height-rect_height),
                        ((seg_width+rect_width)//2, seg_height), BOUNDING_COLOR, -1)

            center = np.array([self.width//2, (2*self.height-rect_height)//2])

            return bounding, rect_width*rect_height, center

        else:
            rect_width = self.width * 3 // 5
            rect_height = self.height * 2 // 5
            pygame.draw.rect(img, BOUNDING_COLOR_PRINT,
                             ((self.width-rect_width)//2,
                             self.height-rect_height,
                             rect_width,
                             rect_height), 5)

            return img

    # 3-0 STAGE
    def rect_air(self, img=None, flag=True):
        if flag:
            seg_height = img.shape[0]
            seg_width = img.shape[1]
            rect_width = seg_width * 3 // 5
            rect_height = seg_height * 3 // 5
            bounding = cv2.rectangle(np.zeros((seg_height, seg_width), dtype=np.uint8),
                        ((seg_width-rect_width)//2, seg_height-rect_height*4//3),
                        ((seg_width+rect_width)//2, seg_height-rect_height//3), BOUNDING_COLOR, -1)

            center = np.array([self.width//2, (2*self.height-rect_height)//2])

            return bounding, rect_width*rect_height, center

        else:
            rect_width = self.width * 3 // 5
            rect_height = self.height * 3 // 5
            pygame.draw.rect(img, BOUNDING_COLOR_PRINT,
                             ((self.width-rect_width)//2,
                             self.height-rect_height*4//3,
                             rect_width,
                             rect_height), 5)

            return img
