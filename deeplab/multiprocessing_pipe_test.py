
import cv2
from multiprocessing import Process, Pipe
import os
import time
import numpy as np

def show(conn):
    print("pr1: {0}, parent: {1}".format(os.getpid(), os.getppid()))
    cap = cv2.VideoCapture("../../data.mp4")

    while True:
        ret, img = cap.read()
        cv2.imshow("Parent Image", img)

        if cv2.waitKey(10) == 32:
            conn.send(img)

        if cv2.waitKey(10) == 27:
            cap.release()
            cv2.destroyAllWindows()

def child(conn):
    child_img = conn.recv()
    print("pr2: {0}, parent: {1}".format(os.getpid(), os.getppid()))
    print(child_img)
    print(child_img.shape)
    print(type(child_img))

    cv2.namedWindow("Child Image")
    cv2.imshow("Child Image", child_img)
    time.sleep(5)
    cv2.destroyWindow("Child Image")


if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    pr1 = Process(target=show, args=(parent_conn,))
    pr2 = Process(target=child, args=(child_conn,))
    pr1.start()
    pr2.start()
