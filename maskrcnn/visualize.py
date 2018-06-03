import cv2
import numpy as np
import pygame
import time

from load import *
from settings import *

MENU_LIST = np.array((True, False, False, False, False))

def MakeText(msg, size, font='freesansbold.ttf'):
    Text = pygame.font.Font(font, size) # font & size
    TextSurf, TextRect = text_objects(msg, Text)
    if size == 200:
        TextRect.center = (display_width//2,TextRect.height*2//3)
    elif size == 100:
        TextRect.center = (display_width//2,(display_height-PERSON_PRINT_SHAPE[1])*2//8+PERSON_PRINT_SHAPE[1]//2)

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
                    click_sound.play()
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
                    click_sound.play()
                    MENU_LIST[current] = False
                    MENU_LIST[next] = True
    else :
        screen.blit(B_norm, (x, y))

def updown(B_norm, B_high, x, y, w, h, LIMIT):
    LEFT = 1
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y :
        screen.blit(B_high, (x, y))
        for event in pygame.event.get():
            if click[0] == LEFT :
                if event.type == pygame.MOUSEBUTTONUP :
                    click_sound.play()
                    if B_norm == UP_norm:
                        LIMIT += 1
                        if LIMIT > 4:
                            LIMIT = 4
                    elif B_norm == DOWN_norm:
                        LIMIT -= 1
                        if LIMIT < 1:
                            LIMIT = 1

    else :
        screen.blit(B_norm, (x, y))

    return LIMIT

def onoff(B_norm, B_high, x, y, w, h, teambattle):
    LEFT = 1
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if teambattle:
        screen.blit(B_norm, (x, y))
    else:
        screen.blit(B_high, (x, y))

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        for event in pygame.event.get():
            if click[0] == LEFT :
                if event.type == pygame.MOUSEBUTTONUP :
                    click_sound.play()
                    teambattle = not teambattle

    return teambattle

def video_setting(frame, flag=False):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (display_width, display_height))
    frame = np.rot90(frame)
    if flag:
        frame = cv2.flip(frame, 0)
    frame = pygame.surfarray.make_surface(frame)

    return frame

def loading():
    screen.fill(white)
    screen.blit(LOADING, ((display_width-LOADING_SHAPE[0])*2//3,(display_height-LOADING_SHAPE[1])//3))
    screen.blit(LOADING_IMAGE, ((display_width-LOADING_IMAGE_SHAPE[0])//3,(display_height-LOADING_IMAGE_SHAPE[1])*2//3))
    pygame.display.flip()

def noperson(print_time):
    pygame.mixer.music.set_volume(1)
    screen.blit(NOPERSON_PRINT, ((display_width-NOPERSON_PRINT_SHAPE[0])//2,(display_height-NOPERSON_PRINT_SHAPE[1])//2))
    if (time.time()-print_time) >= 5:
        return False
    else:
        return True

def position(TIME_INIT):
    screen.blit(FIT_PRINT, (display_width-FIT_PRINT_SHAPE[0],10))
    screen.blit(FIT_POSE, ((display_width-FIT_SHAPE[0])//2,display_height-FIT_SHAPE[1]))
    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE:
                click_sound.play()
                return False

    return True
