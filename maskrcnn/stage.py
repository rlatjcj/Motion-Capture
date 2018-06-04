import cv2
import numpy as np
import pygame
from load import *
from settings import *

BOUNDING_COLOR_PRINT = (0,255,255)
BOUNDING_COLOR = 100


class DETERMINE_STAGE():

    def __init__(self, height, width):
        self.ROUND = 1
        self.height = height
        self.width = width

        self.ROUND_LIMIT = 3
        # the number of STAGEs for each round
        self.ROUND_1 = 3
        self.ROUND_2 = 4
        self.ROUND_3 = 3
        self.version = {1: np.random.choice(self.ROUND_1),
                        2: np.random.choice(self.ROUND_2),
                        3: np.random.choice(self.ROUND_3)}.get(self.ROUND)



    def determine_stage(self, img=None, flag=True):
        self.STAGE_LIST = {"1-0": self.rect_big,
                           "1-1": self.tri,
                           "1-2": self.mush,
                           "2-0": self.rect_thin,
                           "2-1": self.rect_fat,
                           "2-2": self.circle,
                           "2-3": self.infi,
                           "3-0": self.rect_air,
                           "3-1": self.heart,
                           "3-2": self.star}.get("{}-{}".format(self.ROUND, self.version))

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

            center = np.array([seg_width//2, seg_height-rect_height//2])

            return bounding, center

        else:
            rect_width = self.width * 3 // 5
            rect_height = self.height * 4 // 5
            pygame.draw.rect(img, BOUNDING_COLOR_PRINT,
                             ((self.width-rect_width)//2,
                             self.height-rect_height,
                             rect_width,
                             rect_height), 5)

            return img

    # 1-1 STAGE
    def tri(self, img=None, flag=True):
        if flag:
            seg_height = img.shape[0]
            seg_width = img.shape[1]
            rect_width = seg_height * 4 // 5
            rect_height = seg_height * 4 // 5
            bounding = cv2.resize(GAME1_tri_cv, (rect_width, rect_height), interpolation=cv2.INTER_CUBIC)
            bounding[np.where(bounding != 0)] = BOUNDING_COLOR
            bounding = cv2.copyMakeBorder(bounding,seg_height-rect_height,0,(seg_width-rect_width)//2,(seg_width-rect_width)//2,cv2.BORDER_CONSTANT,value=0)

            center = np.array([seg_width//2, seg_height-rect_height//2])

            return bounding, center

        else:
            rect_width = self.height * 4 // 5
            rect_height = self.height * 4 // 5
            tri = pygame.transform.scale(GAME1_tri, (rect_width, rect_height))
            img.blit(tri, ((self.width-rect_width)//2, self.height-rect_height))

            return img

    # 1-2 STAGE
    def mush(self, img=None, flag=True):
        if flag:
            seg_height = img.shape[0]
            seg_width = img.shape[1]
            rect_width = seg_width * 4 // 5
            rect_height = seg_height * 4 // 5
            bounding = cv2.resize(GAME1_mush_cv, (rect_width, rect_height), interpolation=cv2.INTER_CUBIC)
            bounding[np.where(bounding != 0)] = BOUNDING_COLOR
            bounding = cv2.copyMakeBorder(bounding,seg_height-rect_height,0,(seg_width-rect_width)//2,(seg_width-rect_width)//2,cv2.BORDER_CONSTANT,value=0)

            center = np.array([seg_width//2, seg_height-rect_height//2])

            return bounding, center

        else:
            rect_width = self.width * 4 // 5
            rect_height = self.height * 4 // 5
            mush = pygame.transform.scale(GAME1_mush, (rect_width, rect_height))
            img.blit(mush, ((self.width-rect_width)//2, self.height-rect_height))

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

            center = np.array([(seg_width-rect_width)//2+rect_width//2, seg_height-rect_height+rect_height//2])

            return bounding, center

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

            center = np.array([(seg_width-rect_width)//2+rect_width//2, seg_height-rect_height+rect_height//2])

            return bounding, center

        else:
            rect_width = self.width * 3 // 5
            rect_height = self.height * 2 // 5
            pygame.draw.rect(img, BOUNDING_COLOR_PRINT,
                             ((self.width-rect_width)//2,
                             self.height-rect_height,
                             rect_width,
                             rect_height), 5)

            return img

    # 2-2 STAGE
    def circle(self, img=None, flag=True):
        if flag:
            seg_height = img.shape[0]
            seg_width = img.shape[1]
            rect_width = seg_width * 4 // 5
            rect_height = seg_height * 4 // 5
            bounding = cv2.resize(GAME1_circle_cv, (rect_width, rect_height), interpolation=cv2.INTER_CUBIC)
            bounding[np.where(bounding != 0)] = BOUNDING_COLOR
            bounding = cv2.copyMakeBorder(bounding,seg_height-rect_height,0,(seg_width-rect_width)//2,(seg_width-rect_width)//2,cv2.BORDER_CONSTANT,value=0)

            center = np.array([(seg_width-rect_width)//2+rect_width//2, seg_height-rect_height*4//3+rect_height//2])

            return bounding, center

        else:
            rect_width = self.width * 4 // 5
            rect_height = self.height * 4 // 5
            circle = pygame.transform.scale(GAME1_circle, (rect_width, rect_height))
            img.blit(circle, ((self.width-rect_width)//2, self.height-rect_height))

            return img

    # 2-3 STAGE
    def infi(self, img=None, flag=True):
        if flag:
            seg_height = img.shape[0]
            seg_width = img.shape[1]
            rect_width = seg_width * 4 // 5
            rect_height = seg_height * 4 // 5
            bounding = cv2.resize(GAME1_infi_cv, (rect_width, rect_height), interpolation=cv2.INTER_CUBIC)
            bounding[np.where(bounding != 0)] = BOUNDING_COLOR
            bounding = cv2.copyMakeBorder(bounding,seg_height-rect_height,0,(seg_width-rect_width)//2,(seg_width-rect_width)//2,cv2.BORDER_CONSTANT,value=0)

            center = np.array([(seg_width-rect_width)//2+rect_width//2, seg_height-rect_height*4//3+rect_height//2])

            return bounding, center

        else:
            rect_width = self.width * 4 // 5
            rect_height = self.height * 4 // 5
            infi = pygame.transform.scale(GAME1_infi, (rect_width, rect_height))
            img.blit(infi, ((self.width-rect_width)//2, self.height-rect_height))

            return img

    # 3-0 STAGE
    def rect_air(self, img=None, flag=True):
        if flag:
            seg_height = img.shape[0]
            seg_width = img.shape[1]
            rect_width = seg_width * 3 // 5
            rect_height = seg_height * 3 // 5
            bounding = cv2.rectangle(np.zeros((seg_height, seg_width), dtype=np.uint8),
                        ((seg_width-rect_width)//2, seg_height-rect_height*6//5),
                        ((seg_width+rect_width)//2, seg_height-rect_height//5), BOUNDING_COLOR, -1)

            center = np.array([(seg_width-rect_width)//2+rect_width//2, seg_height-rect_height*4//3+rect_height//2])

            return bounding, center

        else:
            rect_width = self.width * 3 // 5
            rect_height = self.height * 3 // 5
            pygame.draw.rect(img, BOUNDING_COLOR_PRINT,
                             ((self.width-rect_width)//2,
                             self.height-rect_height*6//5,
                             rect_width,
                             rect_height), 5)
            img.blit(JUMP_PRINT, (display_width-JUMP_PRINT_SHAPE[0], 15))

            return img

    # 3-1 STAGE
    def heart(self, img=None, flag=True):
        if flag:
            seg_height = img.shape[0]
            seg_width = img.shape[1]
            rect_width = seg_width * 4 // 5
            rect_height = seg_height * 4 // 5
            bounding = cv2.resize(GAME1_heart_cv, (rect_width, rect_height), interpolation=cv2.INTER_CUBIC)
            bounding[np.where(bounding != 0)] = BOUNDING_COLOR
            bounding = cv2.copyMakeBorder(bounding,seg_height-rect_height,0,(seg_width-rect_width)//2,(seg_width-rect_width)//2,cv2.BORDER_CONSTANT,value=0)

            center = np.array([(seg_width-rect_width)//2+rect_width//2, seg_height-rect_height*4//3+rect_height//2])

            return bounding, center

        else:
            rect_width = self.width * 3 // 5
            rect_height = self.height * 4 // 5
            heart = pygame.transform.scale(GAME1_heart, (rect_width, rect_height))
            img.blit(heart, ((self.width-rect_width)//2, self.height-rect_height))

            return img

    # 3-2 STAGE
    def star(self, img=None, flag=True):
        if flag:
            seg_height = img.shape[0]
            seg_width = img.shape[1]
            rect_width = seg_width * 4 // 5
            rect_height = seg_height * 4 // 5
            bounding = cv2.resize(GAME1_star_cv, (rect_width, rect_height), interpolation=cv2.INTER_CUBIC)
            bounding[np.where(bounding != 0)] = BOUNDING_COLOR
            bounding = cv2.copyMakeBorder(bounding,seg_height-rect_height,0,(seg_width-rect_width)//2,(seg_width-rect_width)//2,cv2.BORDER_CONSTANT,value=0)

            center = np.array([(seg_width-rect_width)//2+rect_width//2, seg_height-rect_height*4//3+rect_height//2])

            return bounding, center

        else:
            rect_width = self.width * 3 // 5
            rect_height = self.height * 4 // 5
            star = pygame.transform.scale(GAME1_star, (rect_width, rect_height))
            img.blit(star, ((self.width-rect_width)//2, self.height-rect_height))

            return img
