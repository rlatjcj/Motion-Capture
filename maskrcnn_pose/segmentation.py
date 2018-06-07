import numpy as np
import model as modellib

import cv2
import utils
import numpy as np
from config import Config

from stage import DETERMINE_STAGE
from stage import DETERMINE_STAGE2

import calculate
from joint import *
from settings import *

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

# function
def SegImg(img, READY, STAGE, LIMIT=None, GAME=True, SUCCESS=False, FAIL=False):

    # Run detection
    result = model.detect_keypoint([img], verbose=0)

    # GAME1 & GAME2  r
    r = result[0]

    # CHECK AREA
    area_rois = (r["rois"][:,2]-r["rois"][:,0])*(r["rois"][:,3]-r["rois"][:,1])

    # SELECT PERSON area > 9999
    person_index = np.where(area_rois >= 10000)
    person_index = person_index[0]
    rois = r["rois"][person_index]
    masks = r["masks"][:,:,person_index]
    class_ids = r["class_ids"][person_index]
    keypoints = r["keypoints"][person_index,:,:]

    if READY and GAME == True:
        # if there are no people in image
        if len(person_index) == 0:
            return SUCCESS, FAIL, None
        # STAGE
        bounding, center = STAGE.determine_stage(masks[:,:,0])

        # calculate roi's center position
        distances = []
        for idx in range(len(rois)) :
            x = (rois[idx][1] + rois[idx][3])//2
            y = (rois[idx][0] + rois[idx][2])//2
            pos = np.array([x,y])
            result = dist(pos, center)
            distances.append(result)

        final_instance_index = np.array(distances).argsort()[:LIMIT]

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

        return SUCCESS, FAIL, result

    if READY and GAME == False:
        # If There is no or more person
        if len(person_index) == 0 :
            return SUCCESS, FAIL, None
        elif len(person_index) == 1 :
            return SUCCESS, FAIL, "MORE_PERSON"

        # ground truth cordinates is in STAGE.determine_stage !!!!!!!!!!!
        # ground_truth = STAGE.determine_stage(masks[:,:,0])
        LIMIT = 2

        person_rois = (rois[:,2]-rois[:,0])*(rois[:,3]-rois[:,1])
        final_instance_index = np.array(-person_rois).argsort()[:LIMIT]

        rois = rois[final_instance_index,]
        person_masks = masks[:,:,final_instance_index]

        # keypoint part
        # keypoint has 0 ~ 16 parts = 17 parts
        person_keypoints = keypoints[final_instance_index,:,:]

        # add neck keypoint to 17 index = 18 part
        person_keypoints = add_neck_parts(img, person_keypoints, skeleton = parts_config.skeleton)

        # draw skeleton image each person
        person_keypoints_img , person_keypoints_masks = display_person_keypoints(img, person_masks, person_keypoints, skeleton = parts_config.skeleton)
        output = np.sum(person_keypoints_masks, axis=2)

        parts_angles = []
        #person_keypoints# x, y
        for i in range(LIMIT):
            parts_angles.append(calculate.all_parts_list(parts_config.parts_list, person_keypoints[i], img.shape))

        # compare angles of one player to angles of another player
        # if there is a difference of angles bigger than threshold, FAIL!
        number_of_parts = len(parts_config.parts_list)
        for i in range(len(parts_angles)):
            for j in range(i+1, len(parts_angles)):
                angle_dif = np.abs(np.array(parts_angles[i])-np.array(parts_angles[j]))
                comp_player_s, _ = calculate.check_angles(angle_dif)
                if not comp_player_s:
                    SUCCESS = False
                    FAIL = True
                    return SUCCESS, FAIL, output

        # compare angle of player to label
        # if there is a difference of angles bigger than threshold, SUCCESS!
        for part in parts_angles:
            for label in label_list[STAGE.ROUND]:
                angle_dif_label = np.abs(label-np.array(part))
                comp_label_s, _ = calculate.check_angles(angle_dif_label)
                if comp_player_s:
                    SUCCESS = True
                    FAIL = False
                    return SUCCESS, FAIL, output

        SUCCESS = False
        FAIL = True
        return SUCCESS, FAIL, output
