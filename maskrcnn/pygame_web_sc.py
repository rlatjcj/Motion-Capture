
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
bright_red = (255,0,0)
bright_green = (0,255,0)
block_color = (53,115,255)

# display size to use


# global variables
pause = False
#crash = False


# =============================================================================
# camera load
# =============================================================================
camera = cv2.VideoCapture(0)


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

MENU_LIST = np.array((True, False, False, False, False, False))

def unpause() :
    global pause
    pygame.mixer.music.unpause()
    pause = False

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


def button(msg, x, y, w, h, ic, ac, current, next) :
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
        if click[0] == 1:
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


def game_loop() :
    #pygame.mixer.music.play(-1) # 5 is 6 times , -1 is loop

    global pause
    #dodged = 0 # This is User Score

    gameExit = False

    while not gameExit :
        # use same cmamera(avi, mp4...)
        ret, frame = camera.read()
        frame = video_setting(frame)
        screen.blit(frame, (0,0))

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                QUIT()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_p :
                    pause = True
                    PAUSED()

        pygame.display.update()
        clock.tick(20)


def INTRO(CURRENT, PREV):
    PREV = CURRENT
    CURRENT = 0
    #button(msg, x, y, w, h, inaction_button_color, action_button_color, function_name)
    button("Go motion!", int(button_pos_x/2), int(button_pos_y/5*2), button_width, button_height, green, bright_green, CURRENT, 3)
    button("Quit", int(button_pos_x/2), int(button_pos_y/5*4), button_width, button_height, red, bright_red, CURRENT, 2)

    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_p :
                pause = True
                PAUSED(CURRENT, PREV)

    # Game name display
    MakeText("Motion GAME", 115)

    pygame.display.update()


def PAUSED(CURRENT, PREV) :
    PREV = CURRENT
    CURRENT = 1
    print(CURRENT, PREV)
    pygame.mixer.music.pause() # music pause
    MakeText("Paused", 115)

    while pause :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                QUIT()

        button("Continue!", int(button_pos_x/2), int(button_pos_y/5*2), button_width, button_height, green, bright_green, PREV, CURRENT)
        button("Quit", int(button_pos_x/2), int(button_pos_y/5*4), button_width, button_height, red, bright_red, CURRENT, 2)

        pygame.display.update()


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
                pause = True
                PAUSED(CURRENT, PREV)

    # Game name display
    MakeText("Choose Game", 115)

    pygame.display.update()

def GAME1(CURRENT, PREV):
    PREV = CURRENT
    CURRENT = 4

    global pause
    #dodged = 0 # This is User Score

    gameExit = False

    while not gameExit :
        # use same cmamera(avi, mp4...)
        ret, frame = camera.read()
        frame = video_setting(frame)
        screen.blit(frame, (0,0))

        pygame.display.update()
        clock.tick(20)

        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_p :
                    pause = True
                    PAUSED(CURRENT, PREV)

def GAME2(CURRENT, PREV):
    PREV = CURRENT
    CURRENT = 5

    MakeText("Game2", 115)

    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_p :
                pause = True
                PAUSED(CURRENT, PREV)

MENU = {0: INTRO, 1: PAUSED, 2: QUIT, 3: CHOOSE_GAME, 4: GAME1, 5: GAME2}

# =============================================================================
# This is main function
# =============================================================================
def main() :
    try:
        CURRENT = 0
        PREV = 0
        while True :

            ret, frame = camera.read()
            import matplotlib.pyplot as plt

            frame = video_setting(frame)
            screen.blit(frame, (0,0))

            num_where = np.argmax(MENU_LIST)
            MENU[num_where](CURRENT, PREV)

            Text = pygame.font.Font('freesansbold.ttf', 70) # font & size
            TextSurf, TextRect = text_objects(str(MENU_LIST), Text)
            TextRect.center = ((display_width/2),TextRect.height*2)
            screen.blit(TextSurf, TextRect)

            for event in pygame.event.get() :
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_q:
                        QUIT()


    except KeyboardInterrupt or SystemExit :
        QUIT()

if __name__ == "__main__":
    main()
