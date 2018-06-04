# -*- coding: utf-8 -*-
"""
Created on Sat Jun  2 17:39:09 2018

@author: yeop
"""

import os
os.getcwd()
os.chdir("/workspace/motioncapture_yeo/maskrcnn_pose")
import numpy as np
import coco
import model as modellib
#import visualize
from model import log
import cv2
import time
import pygame
import utils
import numpy as np

#os.chdir("/workspace/motioncapture_yeo/maskrcnn_pose")
from stage import DETERMINE_STAGE
import calculate
import joint
from joint import JointConfig


ROOT_DIR = os.getcwd()
ROOT_DIR
# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "mylogs")
# Local path to trained weights file
#COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mylogs/coco20180530T1104/mask_rcnn_coco_0012.h5")


class InferenceConfig(coco.CocoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    KEYPOINT_MASK_POOL_SIZE = 7


inference_config = InferenceConfig()
parts_config = JointConfig()

# Recreate the model in inference mode
model = modellib.MaskRCNN(mode="inference",
                          config=inference_config,
                          model_dir=MODEL_DIR)


# Get path to saved weights
model_path = "../../mask_rcnn_coco_humanpose.h5" # This will be in workspace
model_path
#model_path = os.path.join(ROOT_DIR, "mylogs/coco20180530T1104/mask_rcnn_coco_0012.h5")
assert model_path != "", "Provide path to trained weights"
print("Loading weights from ", model_path)
model.load_weights(model_path, by_name=True)


# variables
#class_names = ['BG', 'person']
LIMIT = 2


def dist(x,y):
    return np.sqrt(np.sum((x-y)**2))


# function
def SegImg(img, READY, STAGE, SUCCESS=False, FAIL=False, GAME1 = False, GAME2 = False):

    # Run detection
    img = cv2.imread("../../esens.jpeg")
    cv2.imwrite("img.png", img)
    result = model.detect_keypoint([img], verbose=0)

    # GAME1 & GAME2  r값 공유
    r = result[0]

    if READY & GAME1 :
        person_index = np.where(r["class_ids"] == 1)

        # if there are no people in image
        if len(person_index[0]) == 0:
            return SUCCESS, FAIL

        # GAME1 PART
        STAGE = DETERMINE_STAGE(img.shape[0], img.shape[1])
        # STAGE
        bounding, area, center = STAGE.determine_stage(r["masks"][:,:,0])

        rois = r["rois"]

        # calculate roi's center position
        distances = []
        for idx in range(len(rois)) :
            x = (rois[idx][1] + rois[idx][3])//2
            y = (rois[idx][0] + rois[idx][2])//2
            pos = np.array([x,y])
            result = dist(pos, center)
            distances.append(result)
        final_instance_index = np.array(distances).argsort()[:LIMIT]

        masks = r["masks"]
        person_masks = masks[:,:,final_instance_index]

        person_masks = np.sum(person_masks, axis=2, dtype=np.uint8)
        person_masks[np.where(person_masks == 0)] = 0
        person_masks[np.where(person_masks != 0)] = 200

        # for postprocessing about person_masks
        person_masks = cv2.erode(person_masks, np.ones((5,5)), iterations=3)
        person_masks = cv2.dilate(person_masks, np.ones((5,5)), iterations=3)

        result = person_masks - bounding

        # # of segmentation for person
        seg_num = np.array(np.where(person_masks == 200)).shape[1]

        # # of not in bounding box
        res_num = np.array(np.where(result == 200)).shape[1]

        # for calculating whether pixels are changed
        SUCCESS, FAIL = calculate.change(res_num)
        print(SUCCESS, FAIL)
        # for printing segmentation images
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
        cv2.imwrite("person_masks.png", person_masks)
        cv2.imwrite("result.png", result)

        return SUCCESS, FAIL

    if READY & GAME2 :
        person_index = np.where(r["class_ids"] == 1)

        # if there are no people in image
        if len(person_index[0]) < 2 :
            print("more person")
            return SUCCESS, FAIL

        # GAME2 PART

        # tmp center : This center will be changed to boundary center
        tmp_center = img.shape[0]//2, img.shape[1]//2
        center = tmp_center

        rois = r["rois"]

        # calculate roi's center position
        distances = []
        for idx in range(len(rois)) :
            x = (rois[idx][1] + rois[idx][3])//2
            y = (rois[idx][0] + rois[idx][2])//2
            pos = np.array([x,y])
            distance = dist(pos, center)
            distances.append(distance)
        final_instance_index = np.array(distances).argsort()[:LIMIT]

        rois = r["rois"][final_instance_index]
        person_masks = r["masks"][:,:,final_instance_index]

        # keypoint part
        # keypoint has 0 ~ 16 parts = 17 parts
        keypoints = r['keypoints']
        person_keypoints = keypoints[final_instance_index,:,:]

        # add neck keypoint to 17 index = 18 part
        person_keypoints = joint.add_neck_parts(img, person_keypoints, skeleton = parts_config.skeleton)
        person_keypoints
        # draw skeleton image each person

        person_keypoints_img = joint.display_person_keypoints(img, person_masks, person_keypoints, skeleton = parts_config.skeleton)
        # person_keypoints_img.shape = (708, 1114, 2)

        # save person segfile
        cv2.imwrite("person_keypoints_img1.png", person_keypoints_img[:,:,0])
        cv2.imwrite("person_keypoints_img2.png", person_keypoints_img[:,:,1])

        # algorithm
        matches, resi = joint.featureMatching(person_keypoints_img, rois)

        # caculate ineterest parts angles
        first_person_parts_angles = calculate.all_parts_list(parts_config.parts_list, person_keypoints[0]) # first person's parts angle
        second_person_parts_angles = calculate.all_parts_list(parts_config.parts_list, person_keypoints[1]) # second person's parts angle
        print(first_person_parts_angles)
        print(second_person_parts_angles)

        number_of_parts = len(parts_config.parts_list)
        distances = []
        for idx in range(number_of_parts) :
            result = dist(first_person_parts_angles[idx], second_person_parts_angles[idx])
            distances.append(result)

        # for calculating whether compare keypoints
        SUCCESS, FAIL = calculate.compare_keypoints(distances)
        print(SUCCESS, FAIL)
