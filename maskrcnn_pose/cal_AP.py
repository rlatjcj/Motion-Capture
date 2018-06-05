import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt

os.getcwd()
os.chdir("../Mask_RCNN_Humanpose")
import coco
import utils
import model as modellib
import visualize
from model import log

%matplotlib inline

# Root directory of the project
ROOT_DIR = os.getcwd()

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "mylogs")

weight_file = "../mask_rcnn_coco_humanpose.h5"

# Directory of images to run detection on
COCO_DIR = "."  # TODO: enter value here

class InferenceConfig(coco.CocoConfig):
    GPU_COUNT = 2
    IMAGES_PER_GPU = 1
    KEYPOINT_MASK_POOL_SIZE = 7

inference_config = InferenceConfig()

# Recreate the model in inference mode
model = modellib.MaskRCNN(mode="inference",
                          config=inference_config,
                          model_dir=MODEL_DIR)

# Get path to saved weights
# Either set a specific path or find last trained weights
# model_path = os.path.join(ROOT_DIR, ".h5 file name here")
# model_path = model.find_last()[1]
model_path = os.path.join(ROOT_DIR, weight_file)
# Load trained weights (fill in path to trained weights here)
assert model_path != "", "Provide path to trained weights"
print("Loading weights from ", model_path)
model.load_weights(model_path, by_name=True)

# Load dataset
assert inference_config.NAME == "coco"


val_dataset_keypoints = coco.CocoDataset(task_type="person_keypoints")
val_dataset_keypoints.load_coco(COCO_DIR, "val", 2017)
val_dataset_keypoints.prepare()

print("Val Keypoints Image Count: {}".format(len(val_dataset_keypoints.image_ids)))
print("Val Keypoints Class Count: {}".format(val_dataset_keypoints.num_classes))
for i, info in enumerate(val_dataset_keypoints.class_info):
    print("{:3}. {:50}".format(i, info['name']))


AP = []
OKS = []
std = np.array([[0.026], [0.025], [0.025], [0.035], [0.035], [0.079],
               [0.079], [0.072], [0.072], [0.062], [0.062],
               [0.107], [0.107], [0.087], [0.087], [0.089], [0.089]])

def center(x, y):
    return [(x[2]+x[0])//2, (x[3]+x[1])//2, (y[2]+y[0])//2, (y[3]+y[1])//2]

def distance(x):
    return np.sqrt((x[0]-x[2])**2+(x[1]-x[3])**2)

def dist(x, y, valid_key):
    return np.sum((x[0,valid_key,0:2]-y[valid_key,0:2])**2, axis=1)

def OKS_algorithm(gt_bbox, gt_keypoint, r):
    gt_r = []
    for gt in gt_bbox:
        d = []
        for rr in r['rois']:
            cent = center(gt, rr)
            d.append(distance(cent))

        gt_r.append(np.argmin(d))

    oks_raw = 0
    for gt, rr in enumerate(gt_r):
        valid_key = np.where(gt_keypoint[gt,:,2] > 0)[0]

        if len(valid_key) == 0:
            oks_raw += 0
        else:
            interest_distance = dist(gt_keypoint, r['keypoints'][rr], valid_key)
            scale = (r['rois'][rr][2]-r['rois'][rr][1])*(r['rois'][rr][3]-r['rois'][rr][0])
            interest_std = std[valid_key].T[0]
            oks_raw += (np.sum(np.exp((-1)*interest_distance / (2*(scale**2)*(interest_std**2)))) / len(valid_key))/len(gt_r)

    return oks_raw



for image_id in range(len(val_dataset_keypoints.image_ids)//2):
    print(2*image_id, 2*image_id+1)
    original_image1, image_meta1, gt_class_id1, gt_bbox1, gt_mask1, gt_keypoint1 =\
        modellib.load_image_gt_keypoints(val_dataset_keypoints, inference_config,
                               2*image_id, augment=False,use_mini_mask=inference_config.USE_MINI_MASK)

    original_image2, image_meta2, gt_class_id2, gt_bbox2, gt_mask2, gt_keypoint2 =\
        modellib.load_image_gt_keypoints(val_dataset_keypoints, inference_config,
                               2*image_id+1, augment=False,use_mini_mask=inference_config.USE_MINI_MASK)

    if(inference_config.USE_MINI_MASK):
        gt_mask1 = utils.expand_mask(gt_bbox1,gt_mask1,original_image1.shape)
        gt_mask2 = utils.expand_mask(gt_bbox2,gt_mask2,original_image2.shape)

    results = model.detect_keypoint([original_image1, original_image2], verbose=0)

    r1 = results[0]
    r2 = results[1]

    try:
        AP.append(utils.compute_ap(gt_bbox1, gt_class_id1, gt_mask1, r1['rois'], r1['class_ids'], r1['scores'], r1['masks'])[0])
    except ValueError:
        print('predict no person')
        AP.append(0)

    try:
        AP.append(utils.compute_ap(gt_bbox2, gt_class_id2, gt_mask2, r2['rois'], r2['class_ids'], r2['scores'], r2['masks'])[0])
    except ValueError:
        print('predict no person')
        AP.append(0)

    try:
        OKS.append(OKS_algorithm(gt_bbox1, gt_keypoint1, r1))
    except ValueError:
        print('predict no person')
        OKS.append(0)

    try:
        OKS.append(OKS_algorithm(gt_bbox2, gt_keypoint2, r2))
    except ValueError:
        print('predict no person')
        OKS.append(0)


mAP = np.average(AP)
mOKS = np.average(m)
################# AP_50 ###################
# original: 0.8096855135868765
# 0.001_decay: 0.811583860751478
# 0.002_decay: 0.8109807646579994
# 0.001: 0.8106929650607266
# 0.002: 0.8149353267504439
