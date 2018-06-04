# -*- coding: utf-8 -*-
"""
Created on Sat Jun  2 17:42:33 2018

@author: yeop
"""

import random
import colorsys
import cv2
import numpy as np

class JointConfig() :
    # Skeleton information
    skeleton = [0,17,5,7,5,11,5,17,6,8,6,12,6,17,7,9,8,10,11,12,11,13,13,15,12,14,14,16]

    # Part information
    PART_STR = ["nose","left_eye","right_eye","left_ear","right_ear","left_shoulder",
                "right_shoulder","left_elbow","right_elbow","left_wrist","right_wrist",
                "left_hip","right_hip","left_knee","right_knee","left_ankle","right_ankle","neck"]


    # what you interest parts?

    # LEft Parts
    # Left Shoulder
    left_shoulder_parts = [PART_STR.index("neck"), PART_STR.index("left_shoulder"), PART_STR.index("left_hip")]
    left_shoulder_parts2 = [PART_STR.index("left_hip"), PART_STR.index("left_shoulder"), PART_STR.index("left_elbow")]
    left_elbow_parts = [PART_STR.index("left_shoulder"), PART_STR.index("left_elbow"), PART_STR.index("left_wrist")]
    # Left Hip
    left_hip_parts = [PART_STR.index("left_shoulder"), PART_STR.index("left_hip"), PART_STR.index("right_hip")]
    left_hip_parts2 = [PART_STR.index("right_hip"), PART_STR.index("left_hip"), PART_STR.index("left_knee")]
    # Left Knee
    left_knee_parts = [PART_STR.index("left_hip"), PART_STR.index("left_knee"), PART_STR.index("left_ankle")]

    # Right Parts
    # Right Shoulder
    right_shoulder_parts = [PART_STR.index("neck"), PART_STR.index("right_shoulder"), PART_STR.index("right_hip")]
    right_shoulder_parts2 = [PART_STR.index("right_hip"), PART_STR.index("right_shoulder"), PART_STR.index("right_elbow")]
    right_elbow_parts = [PART_STR.index("right_shoulder"), PART_STR.index("right_elbow"), PART_STR.index("right_wrist")]
    # Right Hip
    right_hip_parts = [PART_STR.index("right_shoulder"), PART_STR.index("right_hip"), PART_STR.index("left_hip")]
    right_hip_parts2 = [PART_STR.index("left_hip"), PART_STR.index("right_hip"), PART_STR.index("right_knee")]
    # Right Knee
    right_knee_parts = [PART_STR.index("right_hip"), PART_STR.index("right_knee"), PART_STR.index("right_ankle")]

    # Neck Parts
    neck_parts = [PART_STR.index("nose"), PART_STR.index("neck"), PART_STR.index("right_shoulder")]

    # Parts List
    parts_list = [left_shoulder_parts,
                  left_shoulder_parts2,
                  left_elbow_parts,
                  left_hip_parts,
                  left_hip_parts2,
                  left_knee_parts,
                  right_shoulder_parts,
                  right_shoulder_parts2,
                  right_elbow_parts,
                  right_hip_parts,
                  right_hip_parts2,
                  right_knee_parts,
                  right_knee_parts,
                  neck_parts]



def random_colors(N, bright=True):
    """
    Generate random colors.
    To get visually distinct colors, generate them in HSV space then
    convert to RGB.
    """
    brightness = 1.0 if bright else 0.7
    hsv = [(i / N, 1, brightness) for i in range(N)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    random.shuffle(colors)
    return colors


def display_person_keypoints(image, masks, keypoints, skeleton = None):
    """
    image : frame
    masks : person's masks
    keypoints : 0 ~ 17 keypoints
    skeleton : [0,17,5,7,5,11,5,17,6,8,6,12,6,17,7,9,8,10,11,12,11,13,13,15,12,14,14,16]
    """
    # Number of persons
    N = keypoints.shape[0]
    print(N)
    # If There are no person
    if not N:
        print("\n*** No persons to display *** \n")
    #line_coler = (255,255,255)
    #colors = [line_coler for x in range(N)]
    colors = ((255,255,255),(255,255,255))
    color = None
    for i in range(N):
        color = colors[i]
        mask = masks[:,:,i]
        mask[np.where(mask == 0)] = 0
        mask[np.where(mask != 0)] = 0

        # draw circle
        for Joint in keypoints[i]:
            if (Joint[2] != 0):
                cv2.circle(mask,(Joint[0], Joint[1]), 2, color, 1)

        #draw skeleton connection
        if (len(skeleton)):
            skeleton = np.reshape(skeleton, (-1, 2))

            limb_index = -1
            for limb in skeleton:
                limb_index += 1
                start_index, end_index = limb  # connection joint index from 0 to 17
                Joint_start = keypoints[i][start_index]
                Joint_end = keypoints[i][end_index]
                # Joint:(x,y,v)
                if ((Joint_start[2] != 0) & (Joint_end[2] != 0)):
                    # print(color)VIDEO
                    cv2.line(mask, tuple(Joint_start[:2]), tuple(Joint_end[:2]), color, 3)
    return(masks)



def add_neck_parts(image, keypoints, skeleton = None):
    new_keypoints = []
    # Number of persons
    N = keypoints.shape[0]
    if not N:
        print("\n*** No persons to display *** \n")
    else :
        for i in range(N):
            neck = np.array([(keypoints[i, 5, :] + keypoints[i, 6, :]) / 2]).astype(int)
            # add neck value to keypoints[17]
            one_person_key = np.concatenate((keypoints[i], neck))
            one_person_key.tolist()
            new_keypoints.append(one_person_key)

    result = np.array(new_keypoints)

    return(result)




######## TEST ########
def featureMatching(img, rois) :
    N = len(rois)
    image_list = [None for i in range(N)]

    for i in range(N) :
        image_list[i] = im_crop(img[:,:,i], rois[i])
        cv2.imwrite('img_trim'+str(i)+".png", image_list[i])

    res = None
    orb = cv2.ORB_create()
    #sift = cv2.xfeatures2d.SIFT_create()

    # ORB
    kp1, des1 = orb.detectAndCompute(image_list[0], None)
    kp2, des2 = orb.detectAndCompute(image_list[1], None)

    # SIFT
    #kp1, des1 = sift.detectAndCompute(image_list[0], None)
    #kp2, des2 = sift.detectAndCompute(image_list[1], None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    #bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = bf.match(des1, des2)

    matches = sorted(matches, key=lambda x : x.distance)
    res = cv2.drawMatches(image_list[0], kp1, image_list[1], kp2, matches[:10], res, flags=2)
    cv2.imwrite("Featrue Matching.png", res)

    return matches, res


def im_crop (img, rois):
    w = rois[3]
    h = rois[2]
    x = rois[1]
    y = rois[0]
    #자르고 싶은 지점의 x좌표와 y좌표 지정
    croped_img = img[y:h, x:w]
    croped_img[croped_img == 1] = 255
    return croped_img #필요에 따라 결과물을 리턴
