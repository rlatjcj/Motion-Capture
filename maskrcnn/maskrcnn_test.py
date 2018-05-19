import os
import time
import cv2
import numpy as np
import time

#os.getcwd()
#os.chdir("../maskrcnn")

# Import Mask RCNN
from config import Config
#from dataset import CocoDataset
import model as modellib
import utils

DATASET = "."
YEAR = "2014"
MODEL = "../mask_rcnn_coco.h5"
LOGS = "./log/"  # to save training logs
LIMIT = 10


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

if __name__ == '__main__':
    # Configurations
    config = InferenceConfig()

    # Create model
    model = modellib.MaskRCNN(mode="inference", config=config, model_dir=LOGS)

    # Load weights
    print("Loading weights ", MODEL)
    model.load_weights(MODEL, by_name=True)

    cap = cv2.VideoCapture(0)

    while True:
        start = time.time()
        ret, img = cap.read()
        cv2.imshow('img', img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # If press spacebar
        if cv2.waitKey(10) == 32:
            # Run detection
            r = model.detect([img], verbose=0)[0]
            idx = np.where(r["class_ids"] == 1)[0][0]
            result = np.array(r["masks"], dtype=np.uint8)[:,:,idx]
            result[np.where(result == 1)] = 100
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)

            cv2.imshow('result', result)

        # to check fps
        print('{:.4f} fps'.format(1/(time.time() - start)))

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
