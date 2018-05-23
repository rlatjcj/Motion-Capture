import time
import cv2
import numpy as np
from PIL import Image
import os
#os.chdir("deeplab/")
from model import DeepLabModel
import stage

# Needed to show segmentation colormap labels
import get_dataset_colormap

MODEL_PATH = "../../deeplab_model.tar.gz"
THRESHOLD = 0.2

# If model is in download_path, skip downloading model.
if not os.path.isfile(MODEL_PATH):
    model_url = 'http://download.tensorflow.org/models/deeplabv3_pascal_trainval_2018_01_04.tar.gz'
    tf.gfile.MakeDirs(model_url)

    print('downloading model to %s, this might take a while...' % download_path)
    urllib.request.urlretrieve(model_url, download_path)
    print('download completed!')

model = DeepLabModel(MODEL_PATH)

def SegImg(img, flag, success, fail):
    start = time.time()

    # From cv2 to PIL
    pil_im = Image.fromarray(img)

    # Run model
    seg_map = model.run(pil_im)

    # Adjust color of mask
    seg_image = get_dataset_colormap.label_to_color_image(seg_map).astype(np.uint8)
    seg_image = cv2.cvtColor(seg_image, cv2.COLOR_RGB2GRAY)
    seg_image[np.where(seg_image != 147)] = 0
    seg_num = np.array(np.where(seg_image != 147)).shape[1]

    bounding = stage.rect_big(seg_image.shape[1], seg_image.shape[0], seg_image)

    result = seg_image - bounding
    res_num = np.array(np.where(seg_image == 147)).shape[1]

    percentile = res_num / seg_num

    if flag:
        if percentile < THRESHOLD:
            print('percentile is {:.2f}! SUCCESS!'.format(percentile))
            success = True
        else:
            print('percentile is {:.2f}! FAIL!'.format(percentile))
            fail = True

        # for testing
        #cv2.imshow('bounding', bounding)
        #cv2.imshow('seg_image', seg_image)
        #cv2.imshow('result', result)
        return success, fail

    # to check fps
    print('{:.4f} fps'.format(1/(time.time() - start)))
