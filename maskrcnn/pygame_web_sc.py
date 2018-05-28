
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
#display_width = 1280
#display_height = 720

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

MENU_LIST = np.array((True, False, False, False, False, False))

def MakeText(msg, size, text=True, x=None, y=None, w=None, h=None, font='freesansbold.ttf'):
    Text = pygame.font.Font(font, size) # font & size
    TextSurf, TextRect = text_objects(msg, Text)
    if h == None:
        if text:
            TextRect.center = ((display_width//2),display_height//2)
        else:
            TextRect.center = ((display_width//2),TextRect.height*2//3)
    # button
    else:
        TextRect.center = ((x+(w//2)),(y+(h//2)))
    screen.blit(TextSurf, TextRect)


def text_objects(text, font) :
    # pass trough text, font
    textSurface = font.render(text, True, black)
    # get_rect() : rectecgular area of the surface
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, ic, ac, current, next) :
    LEFT = 1
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y :
        pygame.draw.rect(screen, ac, (x,y,w,h)) # 장소, action_color, top left w, h
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP and event.button == LEFT:
                if next == 2:
                    QUIT()
                MENU_LIST[current] = False
                MENU_LIST[next] = True
                pygame.display.flip()
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
    PREV = CURRENT
    CURRENT = 0
    button("START", int(button_pos_x/2), int(button_pos_y/5*2), button_width, button_height, green, bright_green, CURRENT, 3)
    button("QUIT", int(button_pos_x/2), int(button_pos_y/5*4), button_width, button_height, red, bright_red, CURRENT, 2)

    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_p :
                PAUSED(CURRENT, PREV)

    # Game name display
    MakeText("MOTION GAME", 115, False)

    pygame.display.flip()


def PAUSED(CURRENT, PREV) :
    print(MENU_LIST)
    PREV = CURRENT
    CURRENT = 1

    #pygame.mixer.music.pause() # music pause
    pause = True

    while pause:
        MakeText("PAUSED", 115, False)
        button("CONTINUE", int(button_pos_x/2), int(button_pos_y/5*2), button_width, button_height, green, bright_green, CURRENT, PREV)
        button("QUIT", int(button_pos_x/2), int(button_pos_y/5*4), button_width, button_height, red, bright_red, CURRENT, 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP and event.button == 1:
                pause = False


def QUIT() :
    pygame.quit()
    quit()


def CHOOSE_GAME(CURRENT, PREV):
    PREV = CURRENT
    CURRENT = 3
    button("GAME1", int(button_pos_x/2), int(button_pos_y/5*2), button_width, button_height, green, bright_green, CURRENT, 4)
    button("GAME2", int(button_pos_x/2), int(button_pos_y/5*4), button_width, button_height, red, bright_red, CURRENT, 5)

    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_q:
                QUIT()
            if event.key == pygame.K_p :
                PAUSED(CURRENT, PREV)

    # Game name display
    MakeText("CHOOSE GAME", 115, False)

    pygame.display.flip()

def GAME1(CURRENT, PREV):
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

    TIME_INIT = 5
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
                if event.key == pygame.K_p :
                    PAUSED(CURRENT, PREV)

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
        clock.tick(20)


def GAME2(CURRENT, PREV):
    QUIT()

MENU = {0: INTRO, 1: PAUSED, 2: QUIT, 3: CHOOSE_GAME, 4: GAME1, 5: GAME2}

# =============================================================================
# This is main function
# =============================================================================
def main():
    try:
        CURRENT = 0
        PREV = 0
        while True :

            ret, frame = camera.read()

            frame = video_setting(frame)
            screen.blit(frame, (0,0))
            num_where = np.argmax(MENU_LIST)
            MENU[num_where](CURRENT, PREV)

            for event in pygame.event.get() :
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_q:
                        QUIT()


    except KeyboardInterrupt or SystemExit :
        QUIT()

if __name__ == "__main__":
    main()
