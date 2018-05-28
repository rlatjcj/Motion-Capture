
# 76, 146 line for playing music

# =============================================================================
# Import library
# =============================================================================
import pygame
from pygame.locals import *
import cv2
import numpy as np
import time
import math
import sys

# =============================================================================
# Variables
# =============================================================================
# color
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
block_color = (53,115,255)
white = (255, 255, 255)

# initialize video parameters
VIDEO = 0

# =============================================================================
# camera load
# =============================================================================
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

# button size to use
button_width = 200
button_height = 130

#screen = pygame.display.set_mode([display_width, display_height], pygame.FULLSCREEN | pygame.NOFRAME | pygame.HWSURFACE, 32)
screen = pygame.display.set_mode([display_width, display_height])
clock = pygame.time.Clock()

# button position
button_pos_x = display_width-button_width
button_pos_y = display_height-button_height

pause = False

# Music
#music_path = "./music/" # music folder
#pygame.mixer.music.load(music_path+"Kim Ximya X D. Sanders - Process.mp3")
#crash_sound = pygame.mixer.Sound()


# =============================================================================
# function
# =============================================================================

def MakeText(msg, size, text=True, x=None, y=None, w=None, h=None, font='freesansbold.ttf'):
    Text = pygame.font.Font(font, size) # font & size
    TextSurf, TextRect = text_objects(msg, Text)
    if h == None:
        if text:
            TextRect.center = (display_width//2,display_height//2)
        else:
            TextRect.center = (display_width//2,TextRect.height*2//3)
    # button
    else:
        TextRect.center = ((x+(w//2)),(y+(h//2)))
    screen.blit(TextSurf, TextRect)


def text_objects(text, font) :
    # pass trough text, font
    textSurface = font.render(text, True, black)
    # get_rect() : rectecgular area of the surface
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, ic, ac, action) :
    global MENU_LIST, pause
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y :
        pygame.draw.rect(screen, ac, (x,y,w,h)) # 장소, action_color, top left w, h
        for event in pygame.event.get():
            if click[0] == 1 and action != None:
                action()

            if action == None:
                if msg == "QUIT":
                    sys.exit()
                if msg == "TRY AGAIN":
                    return True
    else :
        pygame.draw.rect(screen, ic, (x,y,w,h)) # 장소, inaction_color, top left w, h

    MakeText(msg, 20, x=x, y=y, w=w, h=h, font='freesansbold.ttf')


def video_setting(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (display_width, display_height))
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)

    return frame


def INTRO():
    while True:
        screen.fill(white)
        button("START", button_pos_x//2, button_pos_y//5*2, button_width, button_height, green, bright_green, CHOOSE_GAME)
        button("QUIT", button_pos_x//2, button_pos_y//5*4, button_width, button_height, red, bright_red, QUIT)

        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_p :
                    screen.fill(white)
                    PAUSE()

        # Game name display
        MakeText("MOTION GAME", 115, False)

        pygame.display.flip()


def PAUSE() :
    global pause

    #pygame.mixer.music.pause() # music pause
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False

        MakeText("PAUSE", 115)
        pygame.display.flip()


def QUIT() :
    pygame.quit()
    quit()


def CHOOSE_GAME():
    while True:
        screen.fill(white)
        button("GAME1", button_pos_x//2, button_pos_y//5*2, button_width, button_height, green, bright_green, GAME1)
        button("GAME2", button_pos_x//2, button_pos_y//5*4, button_width, button_height, red, bright_red, GAME2)

        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_p :
                    screen.fill(white)
                    PAUSE()

        # Game name display
        MakeText("CHOOSE GAME", 115, False)

        pygame.display.update()
        clock.tick(30)

def GAME1():
    global screen, display_width, display_height

    # LOADING...
    screen.fill(white)
    MakeText("LOADING...", 115)
    pygame.display.flip()

    from segmentation import SegImg
    from stage import DETERMINE_STAGE

    # for initializing
    ret, img = camera.read()

    # load images
    FIT_POSE = pygame.image.load("./image/p_00_position_.png")
    FIT_POSE = pygame.transform.scale(FIT_POSE, (display_width//2, display_height*9//10))
    FIT_SHAPE = pygame.surfarray.array2d(FIT_POSE).shape

    TIME_INIT = 5
    # initialize flags
    FIT = True
    READY = False
    SUCCESS = False
    FAIL = False
    PRINT_SUCCESS = False
    NO_PERSON = False

    # for initializing
    STAGE = DETERMINE_STAGE(display_height, display_width)
    SegImg(img, READY, STAGE)

    FIT_time = time.time()
    while True:
        ret, img = camera.read()
        if not ret:
            raise

        frame = video_setting(img)
        screen.blit(frame, (0,0))

        if not READY:
            for event in pygame.event.get() :
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_SPACE:
                        start = time.time()
                        READY = True
                    if event.key == pygame.K_p :
                        PAUSE()

            if NO_PERSON:
                MakeText("NO PERSON", 115)
                if (time.time()-print_time) >= 5:
                    NO_PERSON = False
            elif FIT:
                MakeText("FIT THE TALLEST PERSON", 115, False)
                screen.blit(FIT_POSE, ((display_width-FIT_SHAPE[0])//2,display_height-FIT_SHAPE[1]-20))
                if TIME_INIT < time.time() - FIT_time:
                    FIT = False
            elif not SUCCESS and not FAIL:
                MakeText("READY", 115)
        else:
            timer = "{}".format(math.ceil(TIME_INIT - (time.time() - start)))
            if float(timer) <= 0.01:
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
                        MakeText("PRESS SPACEBAR TO GO TO MENU", 100)
                else:
                    ret, img = camera.read()
                    frame = video_setting(img)
                    screen.blit(frame, (0,0))
                    STAGE.version = {1: np.random.choice(STAGE.ROUND_1),
                                     2: np.random.choice(STAGE.ROUND_2)}.get(STAGE.ROUND)
                    SUCCESS = False
                    PRINT_SUCCESS = False

            else:
                MakeText("SUCCESS", 115)

        elif FAIL:
            STAGE.version = {1: np.random.choice(STAGE.ROUND_1),
                             2: np.random.choice(STAGE.ROUND_2)}.get(STAGE.ROUND)
            ret, img = camera.read()
            frame = video_setting(img)
            screen.blit(frame, (0,0))
            MakeText("FAIL", 115)

            if (time.time()-print_time) >= 5:
                FAIL = False
                PRINT_SUCCESS = False

                pygame.display.flip()

        pygame.display.flip()
        clock.tick(30)


def GAME2():
    QUIT()

def main():
    try:
        CURRENT = 0
        PREV = 0
        screen.fill(white)
        INTRO()

        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_q:
                    QUIT()


    except KeyboardInterrupt or SystemExit :
        QUIT()

if __name__ == "__main__":
    main()
