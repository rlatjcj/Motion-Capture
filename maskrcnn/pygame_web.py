import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys
import time

# sungchuls
import os
import cv2
import math
from segmentation_yeop import SegImg


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
display_width = 1280
display_height = 720

# button size to use
button_width = 200
button_height = 130

# button position
button_pos_x = display_width-button_width
button_pos_y = display_height-button_height

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
# Display
screen = pygame.display.set_mode([display_width, display_height])
clock = pygame.time.Clock()
# Music
#music_path = current_path + str("/music") # music folder
#pygame.mixer.music.load(music_path+"/"+"Kim Ximya X D. Sanders - Process.mp3")
#crash_sound = pygame.mixer.Sound()


# =============================================================================
# function
# =============================================================================

def quitgame() :
    pygame.quit()
    quit()


def unpause() :
    global pause
    #pygame.mixer.music.unpause()
    pause = False


def paused() :
    #pygame.mixer.music.pause() # music pause
    pauseText = pygame.font.Font('freesansbold.ttf', 115) # font & size
    pauseTextSurf, pauseTextRect = text_objects("Paused", pauseText)
    pauseTextRect.center = ((display_width/2),(display_height/2))
    screen.blit(pauseTextSurf, pauseTextRect)

    while pause :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                quit()

        button("Continue!", int(button_pos_x/2), int(button_pos_y/5*2), button_width, button_height, green, bright_green, unpause)
        button("Quit", int(button_pos_x/2), int(button_pos_y/5*4), button_width, button_height, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(20)


def text_objects(text, font) :
    # pass trough text, font
    textSurface = font.render(text, True, black)
    # get_rect() : rectecgular area of the surface
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, ic, ac, action=None) :
    mouse = pygame.mouse.get_pos()
    # =============================================================================
    # print(mouse)
    # (656, 632) ....
    # mouse[0] = x_value, mouse[1] = y_value
    # =============================================================================
    click = pygame.mouse.get_pressed()
    #(0, 0, 0) (left_button, middle_button, right_button)

    if x+w > mouse[0] >x and y+h > mouse[1] > y :
        pygame.draw.rect(screen, ac, (x,y,w,h)) # 장소, action_color, top left w, h
        if click[0] == 1 and action != None :
            action()
    else :
        pygame.draw.rect(screen, ic, (x,y,w,h)) # 장소, inaction_color, top left w, h

    buttonText = pygame.font.Font("freesansbold.ttf", 20) # font 종류, size
    butTextSurf, butTextRect = text_objects(msg, buttonText)
    butTextRect.center = ((x+(w/2)),(y+(h/2)))
    screen.blit(butTextSurf, butTextRect)


def game_loop() :
    #pygame.mixer.music.play(-1) # 5 is 6 times , -1 is loop
    global pause # default is False

    gameExit = False # 게임 루프 나가기 위한 것
    flag = False

    while not gameExit :
        # use same cmamera(avi, mp4...)
        ret, frame = camera.read()
        framed = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        framed = cv2.resize(framed, (display_width, display_height))
        framed = np.rot90(np.fliplr(framed))
        framed = pygame.surfarray.make_surface(framed)
        screen.blit(framed, (0,0))

        # flag default가 False이므로 while문 안에서 계속 "ready" 문구 display
        if not flag:
            readyText = pygame.font.Font('freesansbold.ttf', 115) # font & size
            readyTextSurf, readyTextRect = text_objects("READY?", readyText)
            readyTextRect.center = ((display_width/2),(display_height/2))
            screen.blit(readyTextSurf, readyTextRect)
        else:
            SegImg(frame)
            flag = False

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_q:
                    sys.exit(0)
                if event.key == pygame.K_p :
                    pause = True
                    paused()
                if event.key == pygame.K_SPACE :
                    flag = True

        # 다시봐야 할 부분
        if cv2.waitKey(10) & 0xFF == ord('q'):
            camera.release()
            cv2.destroyAllWindows()
            break

        pygame.display.update()
        clock.tick(20)


# =============================================================================
# This is main function
# =============================================================================
def main() :
    try:

        intro = True
        # if intro is true while is running

        while intro :
            # read camera
            ret, frame = camera.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (display_width, display_height))
            frame = np.rot90(np.fliplr(frame))
            frame = pygame.surfarray.make_surface(frame)
            screen.blit(frame, (0,0))


            # button architecture
            # (message, x, y, w, h, inaction_button_color, action_button_color, event_function_name)
            button("Go motion!", int(button_pos_x/2), int(button_pos_y/5*2), button_width, button_height, green, bright_green, game_loop)
            button("Quit", int(button_pos_x/2), int(button_pos_y/5*4), button_width, button_height, red, bright_red, quitgame)

            # Game name display
            mainText = pygame.font.Font('freesansbold.ttf', 115)
            mainTextSurface, mainTextRect = text_objects("Motion GAME", mainText)
            mainTextRect.center = ((display_width/2),(display_height/5))
            screen.blit(mainTextSurface, mainTextRect)

            pygame.display.update()
            clock.tick(20) # 20 is frame per sec

            for event in pygame.event.get() :
                if event.type == pygame.KEYDOWN :
                    if event.key == K_q:
                        sys.exit(0)

    except KeyboardInterrupt or SystemExit :
        pygame.quit()
        cv2.destroyAllWindows()



# =============================================================================
# START
# =============================================================================
main()







# =============================================================================
# garbage code
# =============================================================================
#k = cv2.waitKey(0)
#if k == 27: # esc key
#    cv2.destroyAllWindow()
#elif k = ord('s'): # 's' key
#    cv2.imwrite('testgray.png',img)
#    cv2.destroyAllWindow()



# USER
# self.dodged = 0 User 점수
# slef.difficulty = 0 User 난이도
# tmp_dodged, tmp_difficutly = check(self.dodged, self.difficulty)

# Condition
# if tmp_difficulty == "low" :
# ...


# =============================================================================
# Appendix
# =============================================================================
# event.KEY
# https://stackoverflow.com/questions/25494726/how-to-use-pygame-keydown
