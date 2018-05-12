import pygame
import sys
from pygame.locals import *
import cv2
import time

pygame.init()
display_width = 800
display_height = 600

ourScreen = pygame.display.set_mode((display_width, display_height))

colorBlue = True
x = 30
y = 30
clock = pygame.time.Clock()
cam = cv2.VideoCapture(0)
finished = False
# 이건 폰트 받아서 사용해야함!
# fps 확인용 필요없으면 주석!
font = pygame.font.Font("D:\KT\miniproj\motioncapture\consola.ttf", 32)

while not finished:
	start = time.time()
	_, myImg = cam.read()
	myImg = cv2.cvtColor(myImg, cv2.COLOR_BGR2RGB)
	myImg = cv2.resize(myImg, (display_width, display_height))
	myImg = cv2.rotate(myImg, cv2.ROTATE_90_COUNTERCLOCKWISE)
	myImg = pygame.surfarray.make_surface(myImg)

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			finished = True

		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			colorBlue = not colorBlue

	# save pressed keys
	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_UP]: y -= 10
	if pressed[pygame.K_DOWN]: y += 10
	if pressed[pygame.K_LEFT]: x -= 10
	if pressed[pygame.K_RIGHT]: x += 10

	ourScreen.blit(myImg, (0, 0))

	# fps 확인용 필요없으면 주석!
	end = (time.time() - start) * 1000
	text = font.render("{:.4f} fps".format(end), True, (0, 0, 0))
	ourScreen.blit(text, (0, 0))

	if colorBlue: color = (0, 128, 255)
	else: color = (255, 255, 255)

	pygame.draw.rect(ourScreen, color, pygame.Rect(x, y, 60, 60))
	pygame.display.flip()


pygame.quit()
quit()
