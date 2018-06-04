import pygame
from pygame.locals import *
import cv2
import numpy as np

from visualize import *
from menu import *
from settings import *


clock = pygame.time.Clock()

MENU = {0: INTRO, 1: CHOOSE_GAME, 2: GAME1, 3: GAME2, 4: SETTING}

def main():
    try:
        intro = cv2.VideoCapture("./sound/kt_motion_intro.mp4")
        while True:
            ret, img = intro.read()
            if not ret:
                break
            frame_intro = video_setting(img, True)
            screen.blit(frame_intro, (0,0))
            pygame.display.flip()
            clock.tick(30)

        CURRENT = 0
        PREV = 0
        INTRO_MUSIC = True

        global go_menu
        go_menu = False

        while True:
            if INTRO_MUSIC:
                pygame.mixer.music.load("./sound/bgm4.mp3")
                pygame.mixer.music.play(-1, 0.0)
                INTRO_MUSIC = False

            screen.fill(white)
            num_where = np.argmax(MENU_LIST)
            MENU[num_where](CURRENT, PREV)
            if (num_where == 2 or num_where == 3) and go_menu:
                INTRO_MUSIC =True

            for event in pygame.event.get() :
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_p:
                        PAUSE()

    except KeyboardInterrupt or SystemExit :
        QUIT()

if __name__ == "__main__":
    main()
