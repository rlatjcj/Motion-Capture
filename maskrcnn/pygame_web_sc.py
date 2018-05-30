import pygame
from pygame.locals import *
import cv2
import numpy as np
import time
import math
import sys

from image_load import *

white = (255,255,255)
cyan = (0,200,200)

# =============================================================================
# camera load
# =============================================================================
VIDEO = 0
camera = cv2.VideoCapture(VIDEO)


# =============================================================================
# pygame, display, music initialize
# =============================================================================

#initial
pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")

# Display for fullscreen
display_width = pygame.display.Info().current_w
display_height = pygame.display.Info().current_h

# for fullscreen
screen = pygame.display.set_mode([display_width, display_height], pygame.FULLSCREEN | pygame.NOFRAME | pygame.HWSURFACE, 32)
#screen = pygame.display.set_mode([display_width, display_height])


# =============================================================================
# function
# =============================================================================

def MakeText(msg, size, font='freesansbold.ttf'):
    Text = pygame.font.Font(font, size) # font & size
    TextSurf, TextRect = text_objects(msg, Text)
    TextRect.center = (display_width//2,TextRect.height*2//3)
    screen.blit(TextSurf, TextRect)


def text_objects(text, font) :
    textSurface = font.render(text, True, cyan)
    return textSurface, textSurface.get_rect()


def button_pose_quit(B_norm, B_high, x, y, w, h, action = None) :
    LEFT = 1
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y :
        screen.blit(B_high, (x, y))
        for event in pygame.event.get():
            if click[0] == LEFT :
                if event.type == pygame.MOUSEBUTTONUP :
                    action()
                    pygame.display.update()

    else :
        screen.blit(B_norm, (x, y))


def button(B_norm, B_high, x, y, w, h, current=None, next=None) :
    global MENU_LIST
    LEFT = 1
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y :
        screen.blit(B_high, (x, y))
        for event in pygame.event.get():
            if click[0] == LEFT :
                if event.type == pygame.MOUSEBUTTONUP :
                    MENU_LIST[current] = False
                    MENU_LIST[next] = True
    else :
        screen.blit(B_norm, (x, y))


def video_setting(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (display_width, display_height))
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)

    return frame


def INTRO(CURRENT, PREV):
    PREV = CURRENT
    CURRENT = 0
    button(START_norm, START_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*2//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], CURRENT, 1)
    button_pose_quit(QUIT_norm, QUIT_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*5//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], QUIT)

    pygame.display.flip()


def PAUSE() :
    #pygame.mixer.music.pause() # music pause
    global pause
    pause = True

    while pause :
        screen.blit(PAUSE_PRINT, ((display_width-PAUSE_PRINT_SHAPE[0])//2, PAUSE_PRINT_SHAPE[1]//4))
        button_pose_quit(CONTINUE_norm, CONTINUE_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*2//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], UNPAUSE)
        button_pose_quit(QUIT_norm, QUIT_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*5//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], QUIT)

        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_q:
                    screen.fill(white)
                    QUIT()
                if event.key == pygame.K_p:
                    pause = not pause

        pygame.display.update()

def REGAME(FLAG, frame):
    #pygame.mixer.music.pause() # music pause
    start = time.time()
    global pause
    pause = True
    while pause:
        screen.blit(frame, (0,0))
        MakeText("{}".format(math.ceil(10-(time.time()-start))), 200)
        if time.time()-start >= 10:
            screen.fill(white)
            QUIT()

        if FLAG == "FAIL":
            screen.blit(CHALLENGE_PRINT, ((display_width-CHALLENGE_PRINT_SHAPE[0])*3//4, (display_height-CHALLENGE_PRINT_SHAPE[1])*2//7))
            screen.blit(CHALLENGE_IMAGE, ((display_width-CHALLENGE_IMAGE_SHAPE[0])//4, (display_height-CHALLENGE_IMAGE_SHAPE[1])*4//7))
            button_pose_quit(YES_norm, YES_high, (display_width-BUTTON_SHAPE[0])//4, (display_height-BUTTON_SHAPE[1])*6//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], UNPAUSE)
            button_pose_quit(NO_norm, NO_high, (display_width-BUTTON_SHAPE[0])*3//4, (display_height-BUTTON_SHAPE[1])*6//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], QUIT)
        else:
            button_pose_quit(FIRSTTIME_norm, FIRSTTIME_high, (display_width-BUTTON_SHAPE[0])//4, (display_height-BUTTON_SHAPE[1])*6//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], UNPAUSE)
            if not pause:
                return True
            button_pose_quit(RESTART_norm, RESTART_high, (display_width-BUTTON_SHAPE[0])*3//4, (display_height-BUTTON_SHAPE[1])*6//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], UNPAUSE)
            if not pause:
                return False

        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_p:
                    pause = not pause

        pygame.display.update()

def UNPAUSE() :
    global pause
    #pygame.mixer.music.unpause()
    pause = False

def QUIT() :
    '''
    start = time.time()
    while True:
        if time.time()-start >= 5:
            break
        screen.blit(QUIT_IMAGE, (0,0))
        screen.blit(QUIT_MENTION, ((display_width-QUIT_MENTION_SHAPE[0])//2, (display_height-QUIT_MENTION_SHAPE[1])//2))
    '''
    pygame.quit()
    quit()


def CHOOSE_GAME(CURRENT, PREV):
    PREV = CURRENT
    CURRENT = 1
    button(GAME1_norm, GAME1_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*2//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], CURRENT, 2)
    button(GAME2_norm, GAME2_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*5//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], CURRENT, 3)

    pygame.display.flip()

def GAME1(CURRENT, PREV):
    global screen, display_width, display_height
    PREV = CURRENT
    CURRENT = 2

    # LOADING...
    screen.fill(white)
    screen.blit(LOADING, ((display_width-LOADING_SHAPE[0])//2,(display_height-LOADING_SHAPE[1])//2))
    pygame.display.flip()

    TIME_INIT = 5
    TIME_STAGE = 3
    # initialize flags
    FIT = True
    READY = False
    SUCCESS = False
    FAIL = False
    PRINT_SUCCESS = False
    NO_PERSON = False

    # for initializing
    from segmentation import SegImg
    from stage import DETERMINE_STAGE

    ret, img = camera.read()
    STAGE = DETERMINE_STAGE(display_height, display_width)
    SegImg(img, READY, STAGE)

    FIT_time = time.time()

    while True:
        ret, img = camera.read()
        if not ret:
            raise

        frame = video_setting(img)
        screen.blit(frame, (0,0))

        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE:
                    start = time.time()
                    READY = True
                if event.key == pygame.K_p :
                    PAUSE()

        if not READY:
            if NO_PERSON:
                screen.blit(NOPERSON_PRINT, ((display_width-NOPERSON_PRINT_SHAPE[0])//2,(display_height-NOPERSON_PRINT_SHAPE[1])//2))
                if (time.time()-print_time) >= 5:
                    NO_PERSON = False
            elif FIT:
                screen.blit(FIT_PRINT, (display_width-FIT_PRINT_SHAPE[0],10))
                screen.blit(FIT_POSE, ((display_width-FIT_SHAPE[0])//2,display_height-FIT_SHAPE[1]))
                if TIME_INIT < time.time() - FIT_time:
                    FIT = False
            elif not SUCCESS and not FAIL:
                screen.blit(READY_PRINT, ((display_width-READY_PRINT_SHAPE[0])//2,(display_height-READY_PRINT_SHAPE[1])//2))
        else:
            if TIME_STAGE-(time.time()-start) <= 0.01:
                timer = "{}".format(math.ceil(TIME_INIT-(time.time()-start-TIME_STAGE)))
                if float(timer) <= 0.01:
                    SUCCESS, FAIL = SegImg(img, READY, STAGE)
                    if not SUCCESS and not FAIL:
                        NO_PERSON = True
                    READY = False
                    PRINT_SUCCESS = True
                    print_time = time.time()

                screen = STAGE.determine_stage(screen, False)
                MakeText(timer, 200)
            else:
                screen.blit(STAGE_DICT[STAGE.ROUND], ((display_width-STAGE_SHAPE[0])//2,(display_height-STAGE_SHAPE[1])//2))

        if SUCCESS:
            if (time.time()-print_time) >= 5:
                STAGE.ROUND += 1
                if STAGE.ROUND > STAGE.ROUND_LIMIT:
                    READY = False
                    SUCCESS = True
                    FAIL = False
                    PRINT_SUCCESS = False
                    NO_PERSON = False

                    screen.blit(ROUND_CLEAR_PRINT, ((display_width-ROUND_CLEAR_PRINT_SHAPE[0])//2+300,ROUND_CLEAR_PRINT_SHAPE[1]//2))
                    screen.blit(SUCCESS_IMAGE, ((display_width-SUCCESS_IMAGE_SHAPE[0])//2-200,(display_height-SUCCESS_IMAGE_SHAPE[1])//2+100))
                    if (time.time()-print_time) >= 10:
                        screen.blit(frame, (0,0))
                        menu = REGAME("SUCCESS", frame)
                        if menu:
                            MENU_LIST[0] = True
                            MENU_LIST[1] = False
                            MENU_LIST[2] = False
                            MENU_LIST[3] = False
                            break
                        else:
                            break

                else:
                    STAGE.version = {1: np.random.choice(STAGE.ROUND_1),
                                     2: np.random.choice(STAGE.ROUND_2)}.get(STAGE.ROUND)
                    SUCCESS = False
                    PRINT_SUCCESS = False

            else:
                screen.blit(SUCCESS_PRINT, ((display_width-SUCCESS_PRINT_SHAPE[0])//2+300,SUCCESS_PRINT_SHAPE[1]//2))
                screen.blit(SUCCESS_IMAGE, ((display_width-SUCCESS_IMAGE_SHAPE[0])//2-200,(display_height-SUCCESS_IMAGE_SHAPE[1])//2+100))

        elif FAIL:
            screen.blit(frame, (0,0))
            STAGE.version = {1: np.random.choice(STAGE.ROUND_1),
                             2: np.random.choice(STAGE.ROUND_2)}.get(STAGE.ROUND)
            screen.blit(FAIL_PRINT, ((display_width-FAIL_PRINT_SHAPE[0])//2+300,FAIL_PRINT_SHAPE[1]//2))
            screen.blit(SUCCESS_IMAGE, ((display_width-SUCCESS_IMAGE_SHAPE[0])//2-200,(display_height-SUCCESS_IMAGE_SHAPE[1])//2+100))
            if (time.time()-print_time) >= 5:
                FAIL = False
                PRINT_SUCCESS = False
                screen.blit(frame, (0,0))
                REGAME("FAIL", frame)

        pygame.display.flip()


def GAME2(CURRENT, PREV):
    screen.fill(white)
    QUIT()

MENU_LIST = np.array((True, False, False, False))
MENU = {0: INTRO, 1: CHOOSE_GAME, 2: GAME1, 3: GAME2}

def main():
    try:
        CURRENT = 0
        PREV = 0

        while True:
            screen.fill(white)
            num_where = np.argmax(MENU_LIST)
            MENU[num_where](CURRENT, PREV)



            for event in pygame.event.get() :
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_q:
                        screen.fill(white)
                        QUIT()
                    if event.key == pygame.K_p:
                        screen.fill(white)
                        PAUSE()

    except KeyboardInterrupt or SystemExit :
        QUIT()

if __name__ == "__main__":
    main()
