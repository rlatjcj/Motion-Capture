import time
import cv2
import numpy as np
from PIL import Image
import os

from model import DeepLabModel

# Needed to show segmentation colormap labels
import get_dataset_colormap

MODEL_PATH = "../../deeplab_model.tar.gz"

# If model is in download_path, skip downloading model.
if not os.path.isfile(MODEL_PATH):
    model_url = 'http://download.tensorflow.org/models/deeplabv3_pascal_trainval_2018_01_04.tar.gz'
    tf.gfile.MakeDirs(model_dir)

    print('downloading model to %s, this might take a while...' % download_path)
    urllib.request.urlretrieve(model_url, download_path)
    print('download completed!')

model = DeepLabModel(MODEL_PATH)

def SegImg(img):
    start = time.time()
    
    # From cv2 to PIL
    pil_im = Image.fromarray(img)

    # Run model
    resized_im, seg_map = model.run(pil_im)

    # Adjust color of mask
    seg_image = get_dataset_colormap.label_to_color_image(seg_map).astype(np.uint8)

    cv2.imshow('seg_image', seg_image)

    # to check fps
    print('{:.4f} fps'.format(1/(time.time() - start)))
