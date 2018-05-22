
import cv2
from multiprocessing import Process, Queue
import numpy as np
import time
import os

def show(n, result):
    print("pr1: {0}, parent: {1}".format(os.getpid(), os.getppid()))
    cap = cv2.VideoCapture(0)

    while True:
        ret, img = cap.read()
        cv2.imshow("Parent Image", img)

        if cv2.waitKey(10) == 32:
            result.put(img)

        if cv2.waitKey(10) == 27:
            cap.release()
            cv2.destroyAllWindows()

def child(n, result):
    child_img = result.get()
    print("pr2: {0}, parent: {1}".format(os.getpid(), os.getppid()))
    print(child_img)
    print(child_img.shape)
    print(type(child_img))

    cv2.namedWindow("Child Image")
    cv2.imshow("Child Image", child_img)
    time.sleep(5)
    cv2.destroyWindow("Child Image")


if __name__ == "__main__":
    result = Queue()
    pr1 = Process(target=show, args=(0, result))
    pr2 = Process(target=child, args=(1, result))
    pr1.start()
    pr2.start()


'''
img = cv2.imread('../../data3.jpeg', cv2.IMREAD_COLOR) # here I'm using a indexed 16-bit tiff as an example.
num_processes = 2
kernel_size = 5
tile_size = img.shape[0]/num_processes  # Assuming img.shape[0] is divisible by 4 in this case

def mp_filter(x, result):
    print(psutil.virtual_memory())  # monitor memory usage
    result.put(cv2.GaussianBlur(img[int(tile_size*x):int(tile_size*(x+1)), :], (kernel_size, kernel_size), kernel_size/5))
    # note that you actually have to process a slightly larger block and leave out the border.

if __name__ == '__main__':
    s = time.time()
    result = Queue()
    processes = [Process(target=mp_filter, args=(i, result)) for i in range(num_processes)]

    for p in processes:
        p.start()

    for i in range(num_processes):
        print(i)
        if i == 0:
            res = result.get()
        else:
            res = np.concatenate((res, result.get()), axis=0)

    for p in processes:
        p.join()

    print(res.shape)
    cv2.imshow("img1", img)
    cv2.imshow("img", res)
    print(res.shape)
    print("Time: {:.4f}".format(time.time() - s))

    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()
'''
