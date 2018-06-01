import cv2
import numpy as np
import pygame
from settings import *
from load import click_sound

MENU_LIST = np.array((True, False, False, False))

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


def video_setting(frame, flag=False):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (display_width, display_height))
    frame = np.rot90(frame)
    if flag:
        frame = cv2.flip(frame, 0)
    frame = pygame.surfarray.make_surface(frame)

    return frame
