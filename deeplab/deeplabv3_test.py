import collections
import os
#import io
#import sys
import tarfile
#import tempfile
import urllib
import time

#from IPython import display
#from ipywidgets import interact
#from ipywidgets import interactive
#from matplotlib import gridspec
from matplotlib import pyplot as plt
import pygame
from pygame.locals import *
import numpy as np
from PIL import Image
import cv2
# import skvideo.io

import tensorflow as tf

if tf.__version__ < '1.5.0':
    raise ImportError('Please upgrade your tensorflow installation to v1.5.0 or newer!')

# Needed to show segmentation colormap labels
#os.chdir('deeplab/')
from utils import get_dataset_colormap

## Select and download models

_MODEL_URLS = {
    'xception_coco_voctrainaug': 'http://download.tensorflow.org/models/deeplabv3_pascal_train_aug_2018_01_04.tar.gz',
    'xception_coco_voctrainval': 'http://download.tensorflow.org/models/deeplabv3_pascal_trainval_2018_01_04.tar.gz',
}

# Check configuration and download the model
_TARBALL_NAME = 'deeplab_model.tar.gz'
model_dir = '../../'

download_path = os.path.join(model_dir, _TARBALL_NAME)

# If model is in download_path, skip downloading model.
if not os.path.isfile(download_path):
    model_url = _MODEL_URLS['xception_coco_voctrainval']
    tf.gfile.MakeDirs(model_dir)

    print('downloading model to %s, this might take a while...' % download_path)
    urllib.request.urlretrieve(model_url, download_path)
    print('download completed!')

## Load model in TensorFlow
_FROZEN_GRAPH_NAME = 'frozen_inference_graph'

class DeepLabModel(object):
    """Class to load deeplab model and run inference."""

    INPUT_TENSOR_NAME = 'ImageTensor:0'
    OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
    INPUT_SIZE = 513

    def __init__(self, tarball_path):
        """Creates and loads pretrained deeplab model."""
        self.graph = tf.Graph()

        graph_def = None
        # Extract frozen graph from tar archive.
        tar_file = tarfile.open(tarball_path)
        for tar_info in tar_file.getmembers():
            if _FROZEN_GRAPH_NAME in os.path.basename(tar_info.name):
                file_handle = tar_file.extractfile(tar_info)
                graph_def = tf.GraphDef.FromString(file_handle.read())
                break

        tar_file.close()

        if graph_def is None:
            raise RuntimeError('Cannot find inference graph in tar archive.')

        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')

        self.sess = tf.Session(graph=self.graph)

    def run(self, image):
        """Runs inference on a single image.

        Args:
            image: A PIL.Image object, raw input image.

        Returns:
            resized_image: RGB image resized from original input image.
            seg_map: Segmentation map of `resized_image`.
        """
        width, height = image.size
        resize_ratio = 1.0 * self.INPUT_SIZE / max(width, height)
        target_size = (int(resize_ratio * width), int(resize_ratio * height))
        resized_image = image.convert('RGB').resize(target_size, Image.ANTIALIAS)
        batch_seg_map = self.sess.run(
            self.OUTPUT_TENSOR_NAME,
            feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(resized_image)]})
        seg_map = batch_seg_map[0]
        return resized_image, seg_map

model = DeepLabModel(download_path)

# with pygame
pygame.init()
cap = cv2.VideoCapture("/workspace/miniproj/data.mp4")
#ret, frame = cap.read()
#ourScreen = pygame.display.set_mode((frame.shape[0], frame.shape[1]))


while True:
    start = time.time()
    ret, frame = cap.read()
    # From cv2 to PIL
    cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow('frame', frame)
    pil_im = Image.fromarray(cv2_im)

    # Run model
    resized_im, seg_map = model.run(pil_im)

    # Adjust color of mask
    seg_image = get_dataset_colormap.label_to_color_image(
        seg_map, get_dataset_colormap.get_pascal_name()).astype(np.uint8)

    cv2.imshow('seg_image', seg_image)

    # Convert PIL image back to cv2 and resize
    #frame = np.array(pil_im)
    #r = seg_image.shape[1] / frame.shape[1]
    #dim = (int(frame.shape[0] * r), seg_image.shape[1])[::-1]
    #resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    #resized = cv2.cvtColor(resized, cv2.COLOR_RGB2BGR)

    # Stack horizontally color frame and mask
    #color_and_mask = np.hstack((resized, seg_image))

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

    print('{:.4f} fps'.format(1/(time.time() - start)))

#output = np.expand_dims(both, axis=0)
#final = np.append(final, output, 0)
#skvideo.io.vwrite("outputvideo111.mp4", final)
