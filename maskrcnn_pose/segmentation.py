import numpy as np
import os
os.chdir("maskrcnn_pose/")
import model as modellib

import cv2
import utils
import numpy as np
from config import Config

from stage import DETERMINE_STAGE
import calculate
import joint
from joint import JointConfig

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
MODEL = "../../mask_rcnn_coco_humanpose.h5" # This will be in workspace
print("Loading weights from ", MODEL)
model.load_weights(MODEL, by_name=True)


def dist(x,y):
    return np.sqrt(np.sum((x-y)**2))


# function
def SegImg(img, READY, STAGE, LIMIT=None, GAME=True, SUCCESS=False, FAIL=False):
    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    import matplotlib.pyplot as plt
    plt.imshow(img)
    # Run detection
    result = model.detect_keypoint([img], verbose=0)

    # GAME1 & GAME2  r값 공유
    r = result[0]

    if READY and GAME == True:
        person_index = np.where(r["class_ids"] == 1)

        # if there are no people in image
        if len(person_index[0]) == 0:
            return SUCCESS, FAIL, None

        # STAGE
        bounding, center = STAGE.determine_stage(r["masks"][:,:,0])

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

        return SUCCESS, FAIL, result

    if READY and GAME == False:
        person_index = np.where(r["class_ids"] == 1)

        # if there are no people in image
        if len(person_index[0]) < LIMIT :
            return SUCCESS, FAIL

        center = img.shape[0]//2, img.shape[1]//2
        rois = r["rois"]

        # calculate roi's center position
        distances = []
        for idx in range(len(rois)) :
            x = (rois[idx][1] + rois[idx][3])//2
            y = (rois[idx][0] + rois[idx][2])//2
            pos = np.array([x,y])
            distance = dist(pos, center)
            distances.append(distance)
        if len(person_index[0]) < LIMIT:
            final_instance_index = np.array(distances).argsort()[:len(person_index[0])]
        else:
            final_instance_index = np.array(distances).argsort()[:LIMIT]

        rois = r["rois"][final_instance_index]
        person_masks = r["masks"][:,:,final_instance_index]
        plt.imshow(person_masks[:,:,0])
        plt.imshow(person_masks[:,:,1])
        # keypoint part
        # keypoint has 0 ~ 16 parts = 17 parts
        keypoints = r['keypoints']
        person_keypoints = keypoints[final_instance_index,:,:]

        # add neck keypoint to 17 index = 18 part
        person_keypoints = joint.add_neck_parts(img, person_keypoints, skeleton = parts_config.skeleton)

        # draw skeleton image each person

        person_keypoints_img, person_keypoints_masks = joint.display_person_keypoints(img, person_masks, person_keypoints, skeleton = parts_config.skeleton)

        plt.imshow(person_keypoints_img)
        plt.imshow(person_keypoints_masks[:,:,1])
        # person_keypoints_img.shape = (708, 1114, 2)

        parts_angles = []
        # save person segfile
        for i in range(len(person_index[0])):
            cv2.imwrite("person_keypoints_img{}.png".format(i), person_keypoints_img[:,:,i])
            parts_angles.append(calculate.all_parts_list(parts_config.parts_list, person_keypoints[i]))
            print(parts_angles[i])
        # algorithm
        #matches, resi = joint.featureMatching(person_keypoints_img, rois)

        number_of_parts = len(parts_config.parts_list)
        distances = []
        for idx in range(number_of_parts) :
            #for i in range(LIMIT):
            result = dist(parts_angles[0][idx], parts_angles[1][idx])
            distances.append(result)

        # for calculating whether compare keypoints
        SUCCESS, FAIL = calculate.compare_keypoints(distances)
        print(SUCCESS, FAIL)

        return SUCCESS, FAIL, np.sum(person_keypoints_img, axis=2)
