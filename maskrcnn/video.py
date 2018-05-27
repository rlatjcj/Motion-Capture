
import cv2
import time
import math
import numpy as np
from segmentation import SegImg
from stage import DETERMINE_STAGE


def main():
    # initialize video parameters
    VIDEO = 0
    TIME_INIT = 5
    FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 5
    FONT_COLOR = (255, 0, 0)
    FONT_THICKNESS = 2

    cap = cv2.VideoCapture(VIDEO)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 448)

    # for initializing
    ret, img = cap.read()

    height = img.shape[0]
    width = img.shape[1]

    # initialize flags
    READY = False
    SUCCESS = False
    FAIL = False
    PRINT_SUCCESS = False
    NO_PERSON = False

    STAGE = DETERMINE_STAGE(height, width)

    # set printed string
    READY_PRINT = "READY!"
    NOPERSON_PRINT = "NO PERSON!"
    SUCCESS_PRINT = "SUCCESS!"
    FAIL_PRINT = "FAIL!"
    CLEAR_ALL_ROUND_PRINT = "CLEAR ALL ROUND!"

    # for initializing
    SegImg(img, READY, STAGE)

    # for full screen
    cv2.namedWindow("img", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("img",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

    while True:
        ret, img = cap.read()

        if not ret:
            raise

        if VIDEO == 0:
            img = cv2.flip(img, 1)

        # if you press spacebar
        if cv2.waitKey(10) == 32 and not SUCCESS and not FAIL:
            start = time.time()
            READY = True

        if not READY:
            if NO_PERSON:
                noperson_width, noperson_height = cv2.getTextSize(NOPERSON_PRINT, FONT_FACE, FONT_SCALE, FONT_THICKNESS)[0]
                img_print = cv2.putText(img, NOPERSON_PRINT, ((width-noperson_width)//2, (height+noperson_height)//2), FONT_FACE, FONT_SCALE+2, FONT_COLOR, FONT_THICKNESS)
                if (time.time()-print_time) >= 5:
                    NO_PERSON = False
            elif not SUCCESS and not FAIL:
                text_width, text_height = cv2.getTextSize(READY_PRINT, FONT_FACE, FONT_SCALE, FONT_THICKNESS)[0]
                img_print = cv2.putText(img, READY_PRINT, ((width-text_width)//2, text_height+5), FONT_FACE, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)
        else:
            str_print = "{}".format(math.ceil(TIME_INIT - (time.time() - start)))
            text_width, text_height = cv2.getTextSize(str_print, FONT_FACE, FONT_SCALE, FONT_THICKNESS)[0]
            if float(str_print) == 0.:
                #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                SUCCESS, FAIL = SegImg(img, READY, STAGE)
                if not SUCCESS and not FAIL:
                    NO_PERSON = True
                READY = False
                PRINT_SUCCESS = True
                print_time = time.time()
            img_print = STAGE.determine_stage(img, False)
            img_print = cv2.putText(img_print, str_print, ((width-text_width)//2, text_height+5), FONT_FACE, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)

        if SUCCESS:
            if (time.time()-print_time) >= 5:
                STAGE.ROUND += 1
                # if all stages are clear
                if STAGE.ROUND > STAGE.ROUND_LIMIT:
                    print(time.time()-print_time)
                    READY = False
                    SUCCESS = True
                    FAIL = False
                    PRINT_SUCCESS = False
                    NO_PERSON = False

                    clear_width, clear_height = cv2.getTextSize(CLEAR_ALL_ROUND_PRINT, FONT_FACE, FONT_SCALE, FONT_THICKNESS)[0]
                    img_print = cv2.putText(img, CLEAR_ALL_ROUND_PRINT, ((width-clear_width)//2, (height+clear_height)//2), FONT_FACE, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)
                    if (time.time()-print_time) >= 10:
                        cap.release()
                        cv2.destroyAllWindows()
                        break
                else:
                    STAGE.version = {1: np.random.choice(STAGE.ROUND_1),
                                     2: np.random.choice(STAGE.ROUND_2)}.get(STAGE.ROUND)
                    SUCCESS = False
                    PRINT_SUCCESS = False

            else:
                # print "SUCCESS" for 5sec
                success_width, success_height = cv2.getTextSize(SUCCESS_PRINT, FONT_FACE, FONT_SCALE, FONT_THICKNESS)[0]
                img_print = cv2.putText(img, SUCCESS_PRINT, ((width-success_width)//2, (height+success_height)//2), FONT_FACE, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)
                # if time of printing "SUCCESS" is over 5sec
                # delete "SUCCESS" and print "READY"

        elif FAIL:
            STAGE.version = {1: np.random.choice(STAGE.ROUND_1),
                             2: np.random.choice(STAGE.ROUND_2)}.get(STAGE.ROUND)
            fail_width, fail_height = cv2.getTextSize(FAIL_PRINT, FONT_FACE, FONT_SCALE, FONT_THICKNESS)[0]
            img_print = cv2.putText(img, FAIL_PRINT, ((width-fail_width)//2, (height+fail_height)//2), FONT_FACE, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)
            if (time.time()-print_time) >= 5:
                FAIL = False
                PRINT_SUCCESS = False

        cv2.imshow("img", img_print)

        # if you want to quit
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    main()
