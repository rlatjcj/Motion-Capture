
import cv2
import numpy as np

BOUNDING_COLOR_PRINT = (255,255,0)
BOUNDING_COLOR = 100


class DETERMINE_STAGE():

    def __init__(self, height, width):
        self.ROUND = 1
        self.height = height
        self.width = width
        self.version = 0

        self.ROUND_LIMIT = 1
        # the number of STAGEs for each round
        self.ROUND_1 = 1
        self.ROUND_2 = 2
        #self.ROUND_3 = 0


    def determine_stage(self, img=None, flag=True):
        self.STAGE_LIST = {"1-0": self.rect_big,
                           "2-0": self.rect_thin,
                           "2-1": self.rect_fat}.get("{}-{}".format(self.ROUND, self.version))

        return self.STAGE_LIST(img, flag)


    # 1-0 ROUND
    def rect_big(self, img=None, flag=True):
        rect_width = self.width * 3 // 5
        rect_height = self.height * 4 // 5

        if flag:
            bounding = cv2.rectangle(np.zeros((self.height, self.width), dtype=np.uint8),
                        ((self.width-rect_width)//2, self.height-rect_height),
                        ((self.width+rect_width)//2, self.height), BOUNDING_COLOR, -1)

            center = np.array([self.width//2, (2*self.height-rect_height)//2])

            return bounding, rect_width*rect_height, center

        else:
            img_print = cv2.rectangle(img,
                        ((self.width-rect_width)//2, self.height-rect_height),
                        ((self.width+rect_width)//2, self.height), BOUNDING_COLOR_PRINT, 2)

            return img_print


    # 2-0 STAGE
    def rect_thin(self, img=None, flag=True):
        rect_width = self.width * 2 // 5
        rect_height = self.height * 4 // 5

        if flag:
            bounding = cv2.rectangle(np.zeros((self.height, self.width), dtype=np.uint8),
                        ((self.width-rect_width)//2, self.height-rect_height),
                        ((self.width+rect_width)//2, self.height), BOUNDING_COLOR, -1)

            center = np.array([self.width//2, (2*self.height-rect_height)//2])

            return bounding, rect_width*rect_height, center

        else:
            img_print = cv2.rectangle(img,
                        ((self.width-rect_width)//2, self.height-rect_height),
                        ((self.width+rect_width)//2, self.height), BOUNDING_COLOR_PRINT, 2)

            return img_print

    # 2-1 STAGE
    def rect_fat(self, img=None, flag=True):
        rect_width = self.width * 3 // 5
        rect_height = self.height * 2 // 5

        if flag:
            bounding = cv2.rectangle(np.zeros((self.height, self.width), dtype=np.uint8),
                        ((self.width-rect_width)//2, self.height-rect_height),
                        ((self.width+rect_width)//2, self.height), BOUNDING_COLOR, -1)

            center = np.array([self.width//2, (2*self.height-rect_height)//2])

            return bounding, rect_width*rect_height, center

        else:
            img_print = cv2.rectangle(img,
                        ((self.width-rect_width)//2, self.height-rect_height),
                        ((self.width+rect_width)//2, self.height), BOUNDING_COLOR_PRINT, 2)

            return img_print

    # 3-0 STAGE
