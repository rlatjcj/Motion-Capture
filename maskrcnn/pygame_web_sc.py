
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
button_width = display_width//3
button_height = display_height//5

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

MENU_LIST = np.array((True, False, False, False, False, False))

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


def button(B_norm, B_high, x, y, w, h, ic, ac, current=None, next=None) :
    global MENU_LIST
    mouse = pygame.mouse.get_pos()

    if x+w > mouse[0] > x and y+h > mouse[1] > y :
        screen.blit(B_norm, (x, y))
        #pygame.draw.rect(screen, ac, (x,y,w,h)) # 장소, action_color, top left w, h
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP and event.button == 1:
                MENU_LIST[current] = False
                MENU_LIST[next] = True
                if current == None:
                    return True
    else :
        screen.blit(B_high, (x, y))
        #pygame.draw.rect(screen, ic, (x,y,w,h)) # 장소, inaction_color, top left w, h


def video_setting(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (display_width, display_height))
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)

    return frame


def INTRO(CURRENT, PREV, B1_norm, B1_high, B2_norm, B2_high):
    PREV = CURRENT
    CURRENT = 0
    #screen.blit(B1, (button_pos_x//2,button_pos_y//5*2))
    button(B1_norm, B1_high, button_pos_x//2, button_pos_y//5*2, button_width, button_height, green, bright_green, CURRENT, 3)
    button(B2_norm, B2_high, button_pos_x//2, button_pos_y//5*4, button_width, button_height, red, bright_red, CURRENT, 2)

    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_p :
                screen.fill(white)
                PAUSE()

    # Game name display
    MakeText("MOTION GAME", 115, False)

    pygame.display.flip()


def PAUSE() :
    #pygame.mixer.music.pause() # music pause
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False

        MakeText("PAUSED", 115)
        pygame.display.update()


def QUIT() :
    pygame.quit()
    quit()


def CHOOSE_GAME(CURRENT, PREV, B1_norm, B1_high, B2_norm, B2_high):
    PREV = CURRENT
    CURRENT = 3
    button(B1_norm, B1_high, button_pos_x//2, button_pos_y//5*2, button_width, button_height, green, bright_green, CURRENT, 4)
    button(B2_norm, B2_high, button_pos_x//2, button_pos_y//5*4, button_width, button_height, red, bright_red, CURRENT, 5)

    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_p :
                screen.fill(white)
                PAUSE()

    # Game name display
    MakeText("CHOOSE GAME", 115, False)

    pygame.display.flip()

def GAME1(CURRENT, PREV, B1_norm, B1_high, B2_norm, B2_high):
    global screen, display_width, display_height
    PREV = CURRENT
    CURRENT = 4

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

        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE:
                    start = time.time()
                    READY = True
                if event.key == pygame.K_p :
                    PAUSE()

        if not READY:
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
                        while True:
                            for event in pygame.event.get():
                                pass
                            button("GO TO MENU", button_pos_x//2, button_pos_y//5*2, button_width, button_height, green, bright_green, CURRENT, 1)
                            button("QUIT", button_pos_x//2, button_pos_y//5*4, button_width, button_height, red, bright_red, CURRENT, 2)
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
                ret, img = camera.read()
                frame = video_setting(img)
                screen.blit(frame, (0,0))
                while True:
                    for event in pygame.event.get():
                        pass
                    if button("TRY AGAIN", button_pos_x//2, button_pos_y//5*2, button_width, button_height, green, bright_green):
                        break
                    button("QUIT", button_pos_x//2, button_pos_y//5*4, button_width, button_height, red, bright_red, CURRENT, 2)

                    pygame.display.flip()

        pygame.display.flip()
        clock.tick(30)


def GAME2(CURRENT, PREV):
    QUIT()

MENU = {0: INTRO, 1: PAUSE, 2: QUIT, 3: CHOOSE_GAME, 4: GAME1, 5: GAME2}

def main():
    try:
        CURRENT = 0
        PREV = 0
        # buttom
        START_norm = pygame.image.load("./image/b_01_start.png")
        START_high = pygame.image.load("./image/b_01_start.png")    # need to edit
        #QUIT_norm =
        #QUIT_high =
        GAME1_norm = pygame.image.load("./image/b_02_1.png")
        GAME1_high = pygame.image.load("./image/b_02_1.png")    # need to edit
        GAME2_norm = pygame.image.load("./image/b_02_2.png")
        GAME2_high = pygame.image.load("./image/b_02_2.png")    # need to edit
        CONTINUE_norm = pygame.image.load("./image/b_04_continue.png")
        CONTINUE_high = pygame.image.load("./image/b_04_continue.png")  # need to edit
        HEY = pygame.image.load("./image/b_05_1_hey.png")
        READY_img = pygame.image.load("./image/b_05_2_ready.png")
        LOADING = pygame.image.load("./image/b_05_3_loading.png")
        while True:
            screen.fill(white)
            num_where = np.argmax(MENU_LIST)
            MENU[num_where](CURRENT, PREV, START_norm, START_high)

    except KeyboardInterrupt or SystemExit :
        QUIT()

if __name__ == "__main__":
    main()
