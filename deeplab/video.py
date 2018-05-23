
import cv2
import time
import math
from segmentation import SegImg

VIDEO = "../../data1.mp4"
TIME_INIT = 5
FONT_FACE = cv2.FONT_HERSHEY_DUPLEX
FONT_SCALE = 5
FONT_COLOR = (255, 0, 0)
FONT_THICKNESS = 2

def main():
    cap = cv2.VideoCapture(VIDEO)
    # for initializing
    ret, img = cap.read()
    SegImg(img)
    #fps = cap.get(cv2.CAP_PROP_FPS)
    flag = False

    height = img.shape[0]
    width = img.shape[1]
    text_width = 0

    while True:
        ret, img = cap.read()
        if VIDEO == 0:
            img = cv2.flip(img, 1)

        # if you press spacebar
        if cv2.waitKey(10) == 32:
            start = time.time()
            flag = True

        if not flag:
            str_print = "READY"
            text_width = cv2.getTextSize(str_print, FONT_FACE, FONT_SCALE, FONT_THICKNESS)[0][0]
        else:
            str_print = "{}".format(math.ceil(TIME_INIT - (time.time() - start)))
            text_width = cv2.getTextSize(str_print, FONT_FACE, FONT_SCALE, FONT_THICKNESS)[0][0]
            if float(str_print) == 0.:
                #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                SegImg(img)
                flag = False

        img_print = cv2.putText(img, str_print, ((width-text_width)//2, 120), FONT_FACE, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)
        cv2.imshow("img", img_print)

        # if you want to quit
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    main()
