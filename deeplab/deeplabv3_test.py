<<<<<<< HEAD
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
#from matplotlib import pyplot as plt
=======
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 16 16:57:55 2018

@author: ktai15
"""

###  COPY ALL THE CODE INTO A JYPYTER NOTEBOOK  ### 
###  THE JYPYTER NOTEBOOK NEEDS TO BE IN 'tensorflow\models\research\deeplab'  ### 

## Imports

import collections
import os
import io
import sys
import tarfile
import tempfile
import urllib

from IPython import display
from ipywidgets import interact
from ipywidgets import interactive
from matplotlib import gridspec
from matplotlib import pyplot as plt
>>>>>>> e29af444e9fa72125585a9c4cf117df1d04e40c1
import numpy as np
from PIL import Image
import cv2
# import skvideo.io

import tensorflow as tf

if tf.__version__ < '1.5.0':
    raise ImportError('Please upgrade your tensorflow installation to v1.5.0 or newer!')

# Needed to show segmentation colormap labels
<<<<<<< HEAD
#os.chdir('deeplab/')
from utils import get_dataset_colormap

## Select and download models

=======
sys.path.append('utils')
import get_dataset_colormap


## Select and download models


>>>>>>> e29af444e9fa72125585a9c4cf117df1d04e40c1
_MODEL_URLS = {
    'xception_coco_voctrainaug': 'http://download.tensorflow.org/models/deeplabv3_pascal_train_aug_2018_01_04.tar.gz',
    'xception_coco_voctrainval': 'http://download.tensorflow.org/models/deeplabv3_pascal_trainval_2018_01_04.tar.gz',
}

<<<<<<< HEAD
# Check configuration and download the model

_TARBALL_NAME = 'deeplab_model.tar.gz'
model_dir = '../../'

download_path = os.path.join(model_dir, _TARBALL_NAME)

# If model is download_path, skip downloading model.
if os.path.isdir(download_path):
    model_url = _MODEL_URLS['xception_coco_voctrainaug']
    tf.gfile.MakeDirs(model_dir)

    print('downloading model to %s, this might take a while...' % download_path)
    urllib.request.urlretrieve(model_url, download_path)
    print('download completed!')

## Load model in TensorFlow
_FROZEN_GRAPH_NAME = 'frozen_inference_graph'

class DeepLabModel(object):
    """Class to load deeplab model and run inference."""

=======
Config = collections.namedtuple('Config', 'model_url, model_dir')

def get_config(model_name, model_dir):
    return Config(_MODEL_URLS[model_name], model_dir)

config_widget = interactive(get_config, model_name="xception_coco_voctrainaug", model_dir='')
display.display(config_widget)

# Check configuration and download the model

_TARBALL_NAME = 'deeplab_model.tar.gz'

config = config_widget.result

model_dir = config.model_dir or tempfile.mkdtemp()
tf.gfile.MakeDirs(model_dir)

download_path = os.path.join(model_dir, _TARBALL_NAME)
print('downloading model to %s, this might take a while...' % download_path)
urllib.request.urlretrieve(config.model_url, download_path)
print('download completed!')


## Load model in TensorFlow

_FROZEN_GRAPH_NAME = 'frozen_inference_graph'


class DeepLabModel(object):
    """Class to load deeplab model and run inference."""
    
>>>>>>> e29af444e9fa72125585a9c4cf117df1d04e40c1
    INPUT_TENSOR_NAME = 'ImageTensor:0'
    OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
    INPUT_SIZE = 513

    def __init__(self, tarball_path):
        """Creates and loads pretrained deeplab model."""
        self.graph = tf.Graph()
<<<<<<< HEAD

=======
        
>>>>>>> e29af444e9fa72125585a9c4cf117df1d04e40c1
        graph_def = None
        # Extract frozen graph from tar archive.
        tar_file = tarfile.open(tarball_path)
        for tar_info in tar_file.getmembers():
            if _FROZEN_GRAPH_NAME in os.path.basename(tar_info.name):
                file_handle = tar_file.extractfile(tar_info)
                graph_def = tf.GraphDef.FromString(file_handle.read())
                break

        tar_file.close()
<<<<<<< HEAD

        if graph_def is None:
            raise RuntimeError('Cannot find inference graph in tar archive.')

        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')

        self.sess = tf.Session(graph=self.graph)

    def run(self, image):
        """Runs inference on a single image.

        Args:
            image: A PIL.Image object, raw input image.

=======
        
        if graph_def is None:
            raise RuntimeError('Cannot find inference graph in tar archive.')

        with self.graph.as_default():      
            tf.import_graph_def(graph_def, name='')
        
        self.sess = tf.Session(graph=self.graph)
            
    def run(self, image):
        """Runs inference on a single image.
        
        Args:
            image: A PIL.Image object, raw input image.
            
>>>>>>> e29af444e9fa72125585a9c4cf117df1d04e40c1
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

<<<<<<< HEAD
## Webcam demo
cap = cv2.VideoCapture("/workspace/miniproj/data.mp4")

while True:
    start = time.time()
    ret, frame = cap.read()
=======

## Webcam demo
cap = cv2.VideoCapture("/home/ktai15/workspace/tensorflow/avi/hotel.mp4")


    
###  UNCOMMENT NEXT LINES TO SAVE THE VIDEO  ###
# Next line may need adjusting depending on webcam resolution
#final = np.zeros((1, 384, 1026, 3))

import time
while True:
    start = time.time()
        
    ret, frame = cap.read()
    
>>>>>>> e29af444e9fa72125585a9c4cf117df1d04e40c1
    # From cv2 to PIL
    cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(cv2_im)

    # Run model
    resized_im, seg_map = model.run(pil_im)
<<<<<<< HEAD

    # Adjust color of mask
    seg_image = get_dataset_colormap.label_to_color_image(
        seg_map, get_dataset_colormap.get_pascal_name()).astype(np.uint8)

    # Convert PIL image back to cv2 and resize
    #frame = np.array(pil_im)
    #r = seg_image.shape[1] / frame.shape[1]
    #dim = (int(frame.shape[0] * r), seg_image.shape[1])[::-1]
    #resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    #resized = cv2.cvtColor(resized, cv2.COLOR_RGB2BGR)

    # Stack horizontally color frame and mask
    #color_and_mask = np.hstack((resized, seg_image))

    cv2.imshow('seg_image', seg_image)
    cv2.imshow('cv2_im', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
=======
    
    # Adjust color of mask
    seg_image = get_dataset_colormap.label_to_color_image(
        seg_map, get_dataset_colormap.get_pascal_name()).astype(np.uint8)
    
    # Convert PIL image back to cv2 and resize
    frame = np.array(pil_im)
    r = seg_image.shape[1] / frame.shape[1]
    dim = (int(frame.shape[0] * r), seg_image.shape[1])[::-1]
    resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    #resized = cv2.cvtColor(resized, cv2.COLOR_RGB2BGR)
    
    # Stack horizontally color frame and mask
    #color_and_mask = np.hstack((resized, seg_image))

    cv2.imshow('seg_map', seg_map)
    cv2.imshow('cv2_im', cv2_im)
>>>>>>> e29af444e9fa72125585a9c4cf117df1d04e40c1
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
<<<<<<< HEAD

    print('{:.4f} fps'.format(1/(time.time() - start)))

#output = np.expand_dims(both, axis=0)
#final = np.append(final, output, 0)
#skvideo.io.vwrite("outputvideo111.mp4", final)
=======
    
    print(1/(time.time() - start),' s')
    
output = np.expand_dims(both, axis=0)
final = np.append(final, output, 0)
skvideo.io.vwrite("outputvideo111.mp4", final)
>>>>>>> e29af444e9fa72125585a9c4cf117df1d04e40c1