import pygame

white = (255,255,255)
cyan = (0,200,200)


#initial
pygame.init()
pygame.display.set_caption("MOTION GAME!")

# Display for fullscreen
display_width = pygame.display.Info().current_w
display_height = pygame.display.Info().current_h

# for fullscreen
#screen = pygame.display.set_mode([display_width, display_height], pygame.FULLSCREEN | pygame.NOFRAME | pygame.HWSURFACE, 32)
screen = pygame.display.set_mode([display_width, display_height])
