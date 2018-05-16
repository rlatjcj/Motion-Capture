import pygame
import os
from pygame.locals import *
import cv2
import time

dir = os.chdir

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

# for checking fps!
font = pygame.font.Font("consola.ttf", 32)

while not finished:
	start = time.time()
	ret, myImg = cam.read()
	if not ret:
		print('video is end')
		break

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

	# for checking fps!
	fps = time.time() - start
	text = font.render("{:.4f} fps".format(1/fps), True, (0, 0, 0))
	ourScreen.blit(text, (0, 0))

	if colorBlue: color = (0, 128, 255)
	else: color = (255, 255, 255)

	pygame.draw.rect(ourScreen, color, pygame.Rect(x, y, 60, 60))
	pygame.display.flip()


pygame.quit()
quit()
