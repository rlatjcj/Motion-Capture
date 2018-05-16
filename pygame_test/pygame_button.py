import pygame
import os
import cv2

pygame.init()

display_width = 1280
display_height = 720

ourScreen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('pygame')
finish = False
clock = pygame.time.Clock()

def TEXT(word):
    text = font.render(word, True, (255, 255, 255))
    text_width = text.get_width()
    text_height = text.get_height()
    return text, text_width, text_height

# setting text
#os.chdir('pygame_test/')
font = pygame.font.Font("consola.ttf", 80)
START, START_width, START_height = TEXT('START')
SETTING, SETTING_width, SETTING_height = TEXT('SETTING')

cam = cv2.VideoCapture(0)

while not finish:
    ret, myImg = cam.read()
    if not ret:
        print('video is end')
        break

    myImg = cv2.cvtColor(myImg, cv2.COLOR_BGR2RGB)
    myImg = cv2.resize(myImg, (display_width, display_height))
    myImg = cv2.rotate(myImg, cv2.ROTATE_90_COUNTERCLOCKWISE)
    myImg = pygame.surfarray.make_surface(myImg)

    #ourScreen.bilt(myImg, (0, 0))
    ourScreen.blit(START, ((display_width-START_width)/2, (display_height-START_height)/2))
    ourScreen.blit(SETTING, ((display_width-SETTING_width)/2, (display_height+SETTING_height)/2))

    # save pressed keys
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_RETURN] or pressed[pygame.K_SPACE]:
        # START, SETTING BUTTON
        break

    if pressed[pygame.K_ESCAPE]:
        # MENU
        break

    pygame.display.flip()
    clock.tick(60)
