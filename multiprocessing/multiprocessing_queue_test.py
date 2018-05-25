import multiprocessing
import cv2
import time

def cam_loop(the_q):
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('papa')

    while True:
        _ , img = cap.read()

        if cv2.waitKey(10) == 32:
            the_q.put(img)

        cv2.imshow('papa', img)
        if cv2.waitKey(10) == 27:
            break

def show_loop(the_q):
    i = 0
    while True:
        from_queue = the_q.get()
        if from_queue is not None:
            cv2.imwrite('pepe{}.png'.format(i), from_queue)
            i += 1

if __name__ == '__main__':

    logger = multiprocessing.log_to_stderr()
    logger.setLevel(multiprocessing.SUBDEBUG)

    the_q = multiprocessing.Queue()

    cam_process = multiprocessing.Process(target=cam_loop,args=(the_q, ))
    cam_process.start()

    show_process = multiprocessing.Process(target=show_loop,args=(the_q, ))
    show_process.start()

    cam_process.join()
    show_loop.join()
