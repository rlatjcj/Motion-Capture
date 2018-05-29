# 76, 146 line for playing music

# =============================================================================
# Import library
# =============================================================================
import pygame
from pygame.locals import *
import cv2
import numpy as np
#from PIL import Image
import time
#import random
#import os 


# =============================================================================
# directory change to folder with this pages
# =============================================================================
#current_path = os.getcwd()


# =============================================================================
# Variables
# =============================================================================
# color
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0,200)
bright_green = (0,255,0,125)
block_color = (53,115,255)

# display size to use


# global variables
MAIN = True
pause = False
#crash = False


# =============================================================================
# camera load
# =============================================================================
camera = cv2.VideoCapture("../avi/angel.mp4")


# =============================================================================
# pygame, display, music initialize
# =============================================================================
#initial
pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")

# Display for fullscreen
#display_width = pygame.display.Info().current_w
#display_height = pygame.display.Info().current_h
display_width = 1280
display_height = 720

# button size to use
button_width = 200
button_height = 130

#screen = pygame.display.set_mode([display_width, display_height], pygame.FULLSCREEN | pygame.NOFRAME | pygame.HWSURFACE, 32)
screen = pygame.display.set_mode([display_width, display_height])
clock = pygame.time.Clock()

# button position
button_pos_x = display_width-button_width
button_pos_y = display_height-button_height

# Music
#music_path = "./music/" # music folder
#pygame.mixer.music.load(music_path+"Kim Ximya X D. Sanders - Process.mp3")
#crash_sound = pygame.mixer.Sound()


# =============================================================================
# function
# =============================================================================

def MakeText(msg, size, x=None, y=None, w=None, h=None, font='freesansbold.ttf'):
    Text = pygame.font.Font(font, size) # font & size
    TextSurf, TextRect = text_objects(msg, Text)
    if h == None:
        TextRect.center = ((display_width/2),TextRect.height//2)
    else:
        TextRect.center = ((x+(w/2)),(y+(h/2)))
    screen.blit(TextSurf, TextRect)



def text_objects(text, font) :
    # pass trough text, font
    textSurface = font.render(text, True, black)
    # get_rect() : rectecgular area of the surface
    return textSurface, textSurface.get_rect()


def button_pose_quit(msg, x, y, w, h, ic, ac, action = None) :
    LEFT = 1
    mouse = pygame.mouse.get_pos()
    # =============================================================================
    # print(mouse)
    # (656, 632) ....
    # mouse[0] = x_value, mouse[1] = y_value
    # =============================================================================
    click = pygame.mouse.get_pressed()

    #(0, 0, 0) (left_button, middle_button, right_button)

    if x+w > mouse[0] > x and y+h > mouse[1] > y :
        pygame.draw.rect(screen, ac, (x,y,w,h)) # 장소, action_color, top left w, h
        for event in pygame.event.get():
            if click[0] == LEFT :
                if event.type == pygame.MOUSEBUTTONUP :
                    action()
                    pygame.display.update()

    else :
        pygame.draw.rect(screen, ic, (x,y,w,h)) # 장소, inaction_color, top left w, h

    MakeText(msg, 20, x=x, y=y, w=w, h=h, font='freesansbold.ttf')



def button(msg, x, y, w, h, ic, ac, current, next) :
    LEFT = 1
    mouse = pygame.mouse.get_pos()
    # =============================================================================
    # print(mouse)
    # (656, 632) ....
    # mouse[0] = x_value, mouse[1] = y_value
    # =============================================================================
    click = pygame.mouse.get_pressed()

    #(0, 0, 0) (left_button, middle_button, right_button)

    if x+w > mouse[0] > x and y+h > mouse[1] > y :
        pygame.draw.rect(screen, ac, (x,y,w,h)) # 장소, action_color, top left w, h
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and click[0] == LEFT:
                MENU_LIST[current] = False
                MENU_LIST[next] = True
                pygame.display.update()

    else :
        pygame.draw.rect(screen, ic, (x,y,w,h)) # 장소, inaction_color, top left w, h

    MakeText(msg, 20, x=x, y=y, w=w, h=h, font='freesansbold.ttf')



def video_setting(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (display_width, display_height))
    frame = np.rot90(np.fliplr(frame))
    frame = pygame.surfarray.make_surface(frame)

    return frame


def INTRO(CURRENT, PREV):

    PREV = CURRENT # 1
    CURRENT = 0
    #button(msg, x, y, w, h, inaction_button_color, action_button_color, function_name)
    button("Go motion!", int(button_pos_x/2), int(button_pos_y/5*2), button_width, button_height, green, bright_green, CURRENT, 1)
    button_pose_quit("Quit", int(button_pos_x/2), int(button_pos_y/5*4), button_width, button_height, red, bright_red, QUIT)

    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_q:
                QUIT()
            if event.key == pygame.K_p:
                PAUSED()

    # Game name display
    MakeText("Motion GAME", 115)

    pygame.display.update()




def PAUSED() :
    #pygame.mixer.music.pause() # music pause
    global pause
    pause = True

    while pause :
        MakeText("PAUSED", 115, False)
        button_pose_quit("Continue!", int(button_pos_x/2), int(button_pos_y/5*2), button_width, button_height, green, bright_green, UNPAUSE)
        button_pose_quit("Quit", int(button_pos_x/2), int(button_pos_y/5*4), button_width, button_height, red, bright_red, QUIT)

        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_q:
                    QUIT()
                if event.key == pygame.K_p:
                    pause = not pause

        pygame.display.update()


def UNPAUSE() :
    global pause
    #pygame.mixer.music.unpause()
    pause = False

def QUIT() :
    pygame.quit()
    quit()


def CHOOSE_GAME(CURRENT, PREV):
    PREV = CURRENT
    CURRENT = 1
    button("GAME1", int(button_pos_x/2), int(button_pos_y/5*2), button_width, button_height, green, bright_green, CURRENT, 2)
    button("GAME2", int(button_pos_x/2), int(button_pos_y/5*4), button_width, button_height, red, bright_red, CURRENT, 3)

    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_q:
                QUIT()
            if event.key == pygame.K_p:
                PAUSED()

    # Game name display
    MakeText("Choose Game", 115)

    pygame.display.update()


def GAME1(CURRENT, PREV):
    global screen, display_width, display_heightm
    PREV = CURRENT
    CURRENT = 2

    # LOADING...
    screen.fill(white)
    MakeText("LOADING...", 115)
    pygame.display.flip()

    from segmentation import SegImg
    from stage import DETERMINE_STAGE

    # for initializing
    ret, img = camera.read()

    TIME_INIT = 5 #####
    # initialize flags
    READY = False
    SUCCESS = False
    FAIL = False
    PRINT_SUCCESS = False
    NO_PERSON = False

    # for initializing
    STAGE = DETERMINE_STAGE(display_height, display_width)
    SegImg(img, READY, STAGE)


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


        if not READY:
            if NO_PERSON:
                MakeText("NO PERSON", 115)
                if (time.time()-print_time) >= 5:
                    NO_PERSON = False
            elif not SUCCESS and not FAIL:
                MakeText("READY", 115)
        else:
            timer = "{}".format(math.ceil(TIME_INIT - (time.time() - start)))
            if float(timer) == 0.:
                SUCCESS, FAIL = SegImg(img, READY, STAGE)
                if not SUCCESS and not FAIL:
                    NO_PERSON = True
                READY = False
                PRINT_SUCCESS = True
                print_time = time.time()

            screen = STAGE.determine_stage(screen, False)
            MakeText(timer, 115, False)

        if SUCCESS:
            if (time.time()-print_time) >= 5:
                STAGE.ROUND += 1
                if STAGE.ROUND > STAGE.ROUND_LIMIT:
                    READY = False
                    SUCCESS = True
                    FAIL = False
                    PRINT_SUCCESS = False
                    NO_PERSON = False

                    MakeText("CLEAR ALL ROUND", 115)
                    if (time.time()-print_time) >= 10:
                        camera.release()
                        QUIT()
                else:
                    STAGE.version = {1: np.random.choice(STAGE.ROUND_1),
                                     2: np.random.choice(STAGE.ROUND_2)}.get(STAGE.ROUND)
                    SUCCESS = False
                    PRINT_SUCCESS = False

            else:
                MakeText("SUCCESS", 115)

        elif FAIL:
            STAGE.version = {1: np.random.choice(STAGE.ROUND_1),
                             2: np.random.choice(STAGE.ROUND_2)}.get(STAGE.ROUND)
            MakeText("FAIL", 115)
            if (time.time()-print_time) >= 5:
                FAIL = False
                PRINT_SUCCESS = False

        pygame.display.flip()


def GAME2(CURRENT, PREV):
    QUIT()


MENU_LIST = np.array((True, False, False, False))

MENU = {0: INTRO, 1: CHOOSE_GAME, 2: GAME1, 3: GAME2}
#QUITMENU = { 1: PAUSED, 2:UNPAUSE, 3: QUIT }

#MENU = {0: INTRO, 1: PAUSED, 2: QUIT, 3: CHOOSE_GAME, 4: GAME1, 5: GAME2}
# =============================================================================
# This is main function
# =============================================================================
def main() :
    try:
        global pause
        CURRENT = 0
        PREV = 0
        while True :

            ret, frame = camera.read()
            import matplotlib.pyplot as plt

            frame = video_setting(frame)
            screen.blit(frame, (0,0))

            num_where = np.argmax(MENU_LIST)
            MENU[num_where](CURRENT, PREV)

            for event in pygame.event.get() :
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_q:
                        QUIT()
                    if event.key == pygame.K_p:
                        PAUSED()

            clock.tick(30) # 20 is frame per sec


    except KeyboardInterrupt or SystemExit :
        QUIT()

if __name__ == "__main__":
    main()
