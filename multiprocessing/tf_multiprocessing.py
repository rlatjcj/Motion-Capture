
import numpy as np
import time
import tensorflow as tf
import threading
import cv2

#x = np.array(range(6), dtype=float)
x = cv2.imread("../simpleperson.jpg")
import matplotlib.pyplot as plt
x.shape
plt.imshow(x)
QUEUE_LENGTH = x.shape[0]*x.shape[1]*x.shape[2]
x_tf = tf.placeholder(dtype=tf.uint8)
queue = tf.FIFOQueue(QUEUE_LENGTH, dtypes=tf.uint8)
enqueue_op = queue.enqueue(x_tf)
dequeue_op = queue.dequeue()

def enqueue(coord, sess, x):
    cur_ind = 0
    while not coord.should_stop():
        if cur_ind > len(x) - 1:
            cur_ind = 0

        # instead of feature extraction
        feed = {x_tf: x[cur_ind]}
        time.sleep(2)

        sess.run(enqueue_op, feed_dict=feed)
        print('Enqueue %d !' % x[cur_ind])
        cur_ind += 1

coord = tf.train.Coordinator()

with tf.Session() as sess:
    thread = threading.Thread(target=enqueue, args=(coord, sess, x))
    thread.start()


    time.sleep(4)
    x_out = sess.run(dequeue_op)
    print(x_out.shape)
    print('x_out: ', x_out)

    coord.request_stop()
    coord.join([thread])




'''

from multiprocessing import Process, Queue
from PIL import Image
import cv2
import os
import numpy as np
import tensorflow as tf
from segmentation import SegImg

def image_display(taskqueue):
    cv2.namedWindow('image_display')
   while True:
      image = taskqueue.get()              # Added
      if image is None:  break             # Added
      cv2.imshow ('image_display', image)  # Added
      cv2.waitKey(10)                      # Added
      continue                             # Added

      if taskqueue.get()==None:
         continue
      else:
         image = taskqueue.get()
         im = Image.fromstring(image['mode'], image['size'], image['pixels'])
         num_im = np.asarray(im)
         cv2.imshow ('image_display', num_im)


if __name__ == '__main__':
   taskqueue = Queue()
   cap = cv2.VideoCapture(0)
   p = Process(target=image_display, args=(taskqueue,))
   p.start()

   while True:
      flag, image = cap.read()

      taskqueue.put(image)  # Added
      import time           # Added
      time.sleep(1/30)         # Added
      continue              # Added

      if flag == 0:
         break
      im = Image.fromarray(image)
      im_dict = {
      'pixels': im.tostring(),
      'size': im.size,
      'mode': im.mode,
      }
      taskqueue.put(im_dict)

taskqueue.put(None)
p.join()
cv2.DestroyAllWindows()
'''
