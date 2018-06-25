import numpy as np
import model as modellib

import cv2
import utils
import numpy as np
from config import Config

from stage import DETERMINE_STAGE2

import calculate
from joint import *

MODEL_DIR = "./log/"

class InferenceConfig(Config):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

    # Give the configuration a recognizable name
    NAME = "coco"

    NUM_CLASSES = 1 + 1  # Person and background

    NUM_KEYPOINTS = 17
    MASK_SHAPE = [28, 28]
    KEYPOINT_MASK_SHAPE = [56,56]
    # DETECTION_MAX_INSTANCES = 50
    TRAIN_ROIS_PER_IMAGE = 100
    MAX_GT_INSTANCES = 128
    RPN_TRAIN_ANCHORS_PER_IMAGE = 150
    USE_MINI_MASK = True
    MASK_POOL_SIZE = 14
    KEYPOINT_MASK_POOL_SIZE = 7
    LEARNING_RATE = 0.002
    STEPS_PER_EPOCH = 1000
    WEIGHT_LOSS = True
    KEYPOINT_THRESHOLD = 0.005

    PART_STR = ["nose","left_eye","right_eye","left_ear","right_ear","left_shoulder",
                "right_shoulder","left_elbow","right_elbow","left_wrist","right_wrist",
                "left_hip","right_hip","left_knee","right_knee","left_ankle","right_ankle"]
    LIMBS = [0,-1,-1,5,-1,6,5,7,6,8,7,9,8,10,11,13,12,14,13,15,14,16]


inference_config = InferenceConfig()
parts_config = JointConfig()

# Recreate the model in inference mode
model = modellib.MaskRCNN(mode="inference",
                          config=inference_config,
                          model_dir=MODEL_DIR)


# Get path to saved weights
MODEL = "../../mask_rcnn_coco_0101.h5"
print("Loading weights from ", MODEL)
model.load_weights(MODEL, by_name=True)


def dist(x,y):
    return np.sqrt(np.sum((x-y)**2))

import cv2
import os
os.getcwd()
img_list = os.listdir("humanpose")

parts_angles = []
leg_list1 = os.listdir("leg1")
leg_list2 = os.listdir("leg2")
manse_list1 = os.listdir("manse1")
manse_list2 = os.listdir("manse2")

for i, list in enumerate(manse_list2):
    print(i)
    img = cv2.imread("humanpose/{}".format(list))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = model.detect_keypoint([img], verbose=0)
    r = results[0]

    try:
        if len(r["rois"]) >= 2:
            area_rois = (r["rois"][:,2]-r["rois"][:,0])*(r["rois"][:,3]-r["rois"][:,1])
            area_argmin = np.argmin(area_rois)
            keypoint = add_neck_parts(img, np.delete(r['keypoints'], area_argmin, 0), skeleton = parts_config.skeleton)
        elif len(r["rois"]) == 1:
            keypoint = add_neck_parts(img, r['keypoints'], skeleton = parts_config.skeleton)

        parts_angles.append(calculate.all_parts_list(parts_config.parts_list, keypoint[0], img.shape))
    except:
        continue


len(parts_angles)
len(manse_list)
len(leg_list)

leg_label = parts_angles
len(leg_label)
manse_label = parts_angles
len(manse_label)

leg_av = np.average(leg_label, axis=0)
manse_av = np.average(manse_label, axis=0)

for i in manse_av:
    print(i)
