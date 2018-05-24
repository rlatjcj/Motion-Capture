
import cv2
import time
import math
#import os
#os.chdir("deeplab/")
from segmentation import SegImg
import stage

VIDEO = 0
TIME_INIT = 5
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 3
FONT_COLOR = (255, 0, 0)
FONT_THICKNESS = 2

SUCCESS_PRINT = "SUCCESS!"
FAIL_PRINT = "FAIL!"


def main():
    cap = cv2.VideoCapture(VIDEO)

    # setting resolution captured image
    # 1280 x 720 : 10 fps
    # 960 x 544 : 15 fps
    # 800 x 448 : 20 fps
    # 640 x 480 : 30 fps
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 448)

    # read
    ret, img = cap.read()
    #fps = cap.get(cv2.CAP_PROP_FPS)

    # initialize flags
    READY = False
    success = False
    fail = False
    #STAGE = 0
    PRINT_SUCCESS = False

    # for initializing
    SegImg(img, READY)

    height = img.shape[0]
    width = img.shape[1]

    cut_size = (height-(width*9//16))//2
    text_width = 0
    # for full screen
    cv2.namedWindow("img", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("img",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

    while True:
        #print(cap.get(cv2.CAP_PROP_FPS))
        ret, img = cap.read()

        # if we need to crop image
        #img = img[cut_size:height-cut_size,:]
        cut_height = img.shape[0]
        if VIDEO == 0:
            img = cv2.flip(img, 1)

        # if you press spacebar, game start!
        if cv2.waitKey(10) == 32 and not success and not fail:
            start = time.time()
            READY = True

        if not READY:
            if not success and not fail:
                str_print = "READY"
                # for getting "READY" text size
                text_width, text_height = cv2.getTextSize(str_print, FONT_FACE, FONT_SCALE, FONT_THICKNESS)[0]
                img_print = cv2.putText(img, str_print, ((width-text_width)//2, text_height+5), FONT_FACE, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)

        # if you are READY!
        else:
            str_print = "{}".format(math.ceil(TIME_INIT - (time.time() - start)))
            text_width, text_height = cv2.getTextSize(str_print, FONT_FACE, FONT_SCALE, FONT_THICKNESS)[0]
            if float(str_print) == 0.:
                #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                success, fail = SegImg(img, READY, success, fail)
                READY = False
                #STAGE += 1
                PRINT_SUCCESS = True
                print_time = time.time()
            img_print = stage.rect_big(width, cut_height, img, False)
            img_print = cv2.putText(img_print, str_print, ((width-text_width)//2, text_height+5), FONT_FACE, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)


        if success == True:
            # print "SUCCESS" for 5sec
            success_width, success_height = cv2.getTextSize(SUCCESS_PRINT, FONT_FACE, FONT_SCALE+2, FONT_THICKNESS)[0]
            img_print = cv2.putText(img, SUCCESS_PRINT, ((width-success_width)//2, (cut_height+success_height)//2), FONT_FACE, FONT_SCALE+2, FONT_COLOR, FONT_THICKNESS)
            # if time of printing "SUCCESS" is over 5sec
            # delete "SUCCESS" and print "READY"
            if (time.time()-print_time) >= 5:
                success = False
                PRINT_SUCCESS = False

        elif fail == True:
            fail_width, fail_height = cv2.getTextSize(FAIL_PRINT, FONT_FACE, FONT_SCALE+2, FONT_THICKNESS)[0]
            img_print = cv2.putText(img, FAIL_PRINT, ((width-fail_width)//2, (cut_height+fail_height)//2), FONT_FACE, FONT_SCALE+2, FONT_COLOR, FONT_THICKNESS)
            if (time.time()-print_time) >= 5:
                fail = False
                PRINT_SUCCESS = False

        cv2.imshow("img", img_print)

        # if you want to quit
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    main()
