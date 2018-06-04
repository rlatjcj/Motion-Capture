import cv2
import numpy as np

from config import Config
import model as modellib
import utils
from stage import DETERMINE_STAGE
import calculate

MODEL = "../../mask_rcnn_coco.h5"
LOGS = "./log/"  # to save training logs

class InferenceConfig(Config):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    DETECTION_MIN_CONFIDENCE = 0

    # Give the configuration a recognizable name
    NAME = "coco"

    # Number of classes (including background)
    NUM_CLASSES = 1 + 80  # COCO has 80 classes


# Configurations
config = InferenceConfig()

# Create model
model = modellib.MaskRCNN(mode="inference", config=config, model_dir=LOGS)

# Load weights
print("Loading weights ", MODEL)
model.load_weights(MODEL, by_name=True)

def dist(x,y):
    return np.sqrt(np.sum((x-y)**2))

def SegImg(img, READY, STAGE, LIMIT=None, SUCCESS=False, FAIL=False):
    # Run detection
    r = model.detect([img], verbose=0)[0]

    if READY:
        person_index = np.where(r["class_ids"] == 1)[0]

        # if there are no people in image
        if len(person_index) == 0:
            return SUCCESS, FAIL


        # STAGE
        bounding, center = STAGE.determine_stage(r["masks"][:,:,0])

        rois = np.array(r["rois"][person_index])

        # calculate roi's center position
        distances = []
        for idx in range(len(rois)) :
            x = (rois[idx][1] + rois[idx][3])//2
            y = (rois[idx][0] + rois[idx][2])//2
            pos = np.array([x,y])
            result = dist(pos, center)
            distances.append(result)

        final_instance_index = np.array(distances).argsort()[:LIMIT]

        masks = np.array(r["masks"], dtype=np.uint8)[:,:,person_index]
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
