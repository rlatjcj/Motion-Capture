import os
import time
import cv2
import numpy as np
import time

#os.getcwd()
#os.chdir("./maskrcnn")

# Import Mask RCNN
from config import Config
import model as modellib
import utils

MODEL = "../../mask_rcnn_coco.h5"
LOGS = "./log/"  # to save training logs
LIMIT = 2


############################################################
#  Configurations
############################################################

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

def SegImg(img):
    start = time.time()
    # Run detection
    r = model.detect([img], verbose=0)[0]
    n = 0
    for idx in np.where(r["class_ids"] == 1)[0]:
        if n > LIMIT:
            break
        n += 1
        
        if idx == 0:
            result = np.array(r["masks"], dtype=np.uint8)[:,:,idx]
            result[np.where(result == 1)] = 100
        else:
            raw = np.array(r["masks"], dtype=np.uint8)[:,:,idx]
            raw[np.where(raw == 1)] = 200
            result += raw

    result[np.where(result != 0)] = 200
    result = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
    cv2.imshow('result', result)

    # to check fps
    print('{:.4f} fps'.format(1/(time.time() - start)))
