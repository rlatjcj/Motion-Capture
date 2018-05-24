#import time
import cv2
import numpy as np
from PIL import Image
#import os
#os.chdir("deeplab/")
from model import DeepLabModel
import stage
import calculate

# Needed to show segmentation colormap labels
import get_dataset_colormap

MODEL_PATH = "../../deeplab_model.tar.gz"

'''
if you don't download yet, go below url and download and change file name to deeplab_model.tar.gz
model_url = 'http://download.tensorflow.org/models/deeplabv3_pascal_trainval_2018_01_04.tar.gz'
'''

model = DeepLabModel(MODEL_PATH)

def SegImg(img, READY, success=False, fail=False):
    start = time.time()

    # From cv2 to PIL
    pil_im = Image.fromarray(img)

    # Run model
    seg_map = model.run(pil_im)

    # Adjust color of mask
    seg_image = get_dataset_colormap.label_to_color_image(seg_map).astype(np.uint8)
    seg_image = cv2.cvtColor(seg_image, cv2.COLOR_RGB2GRAY)
    seg_image[np.where(seg_image != 147)] = 0

    if READY:
        # for opening seg_image
        seg_image = cv2.erode(seg_image, np.ones((5,5)), iterations=3)
        seg_image = cv2.dilate(seg_image, np.ones((5,5)), iterations=3)

        # STAGE 1
        bounding, area = stage.rect_big(seg_image.shape[1], seg_image.shape[0], seg_image)
        result = seg_image - bounding

        # # of segmentation for person
        seg_num = np.array(np.where(seg_image == 147)).shape[1]

        # # of not in bounding box
        res_num = np.array(np.where(result == 147)).shape[1]

        #cv2.imshow("img1", img)
        #cv2.imshow("seg_image", seg_image)
        #cv2.imshow("bounding", bounding)
        #cv2.imshow("result", result)
        #print(seg_num, res_num)

        # for calculating whether pixels are changed
        success, fail = calculate.change(res_num)

        # for calculating percentile
        #success, fail = calculate.percentile(res_num, seg_num)

        # to check fps
        #print('{:.4f} fps'.format(1/(time.time() - start)))

        return success, fail
