
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
from moviepy.editor import VideoFileClip

white = (255,255,255)
cyan = (0,200,200)

# initialize video parameters
VIDEO = "./image/data.mp4"
#VIDEO = 0
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
#Sound
pygame.mixer.music.load("./sound/bgm2.mp3")

#pygame.mixer.music.fadeout(2000)

click_sound = pygame.mixer.Sound("./sound/click.wav")
click_sound.set_volume(0.7)
time_one = pygame.mixer.Sound("./sound/1.wav")
time_one.set_volume(1.5)
time_two = pygame.mixer.Sound("./sound/2.wav")
time_two.set_volume(1.5)
time_three = pygame.mixer.Sound("./sound/3.wav")
time_three.set_volume(1.5)
time_four = pygame.mixer.Sound("./sound/4.wav")
time_four.set_volume(1.5)
time_five = pygame.mixer.Sound("./sound/5.wav")
time_five.set_volume(1.5)

sound_list = ["time_five", "time_four", "time_three", "time_two", "time_one"]
#pygame.mixer.music.play(-1, 0.0)
#pygame.mixer.music.set_volume(0.7)

# button size to use
button_width = display_width//3
button_height = display_height//5

screen = pygame.display.set_mode([display_width, display_height], pygame.FULLSCREEN | pygame.NOFRAME | pygame.HWSURFACE, 32)
#screen = pygame.display.set_mode([display_width, display_height])
clock = pygame.time.Clock()
# button position
button_pos_x = display_width-button_width
button_pos_y = display_height-button_height


# Music
#music_path = "./music/" # music folder
#pygame.mixer.music.load(music_path+"Kim Ximya X D. Sanders - Process.mp3")
#crash_sound = pygame.mixer.Sound()

# buttom
START_norm = pygame.image.load("./image/b_01_start.png")
START_high = pygame.image.load("./image/bb_01_start.png")
QUIT_norm = pygame.image.load("./image/b_03_quit.png")
QUIT_high = pygame.image.load("./image/bb_03_quit.png")

GAME1_norm = pygame.image.load("./image/b_02_1.png")
GAME1_high = pygame.image.load("./image/bb_02_1.png")
GAME2_norm = pygame.image.load("./image/b_02_2.png")
GAME2_high = pygame.image.load("./image/bb_02_2.png")

CONTINUE_norm = pygame.image.load("./image/b_04_continue.png")
CONTINUE_high = pygame.image.load("./image/bb_04_continue.png")

YES_norm = pygame.image.load("./image/b_06_y.png")
YES_high = pygame.image.load("./image/bb_06_yes.png")
NO_norm = pygame.image.load("./image/b_06_n.png")
NO_high = pygame.image.load("./image/bb_06_no.png")

BUTTON_SHAPE = pygame.surfarray.array2d(START_norm).shape

QUIT_IMAGE = pygame.image.load("./image/p_13_2_end.png")
QUIT_IMAGE_SHAPE = pygame.surfarray.array2d(QUIT_IMAGE).shape
QUIT_MENTION = pygame.image.load("./image/p_13_1_end.png")
QUIT_MENTION_SHAPE = pygame.surfarray.array2d(QUIT_MENTION).shape

# =============================================================================
# function
# =============================================================================

#def intro_movie():
#        clip = VideoFileClip('./sound/intro.mpeg')
#        clip.preview()
#        pygame.display.update()
#        clock.tick(20)

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
                click_sound.play()
                if event.type == pygame.MOUSEBUTTONUP :
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


def video_setting(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (display_width, display_height))
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)

    return frame


def INTRO(CURRENT, PREV):
    PREV = CURRENT
    CURRENT = 0
    button(START_norm, START_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*2//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], CURRENT, 1)
    button_pose_quit(QUIT_norm, QUIT_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*5//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], QUIT)
    pygame.display.flip()


def PAUSE() :
    pygame.mixer.music.pause() # music pause
    global pause
    pause = True

    while pause :
        MakeText("PAUSE", 200)
        button_pose_quit(CONTINUE_norm, CONTINUE_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*2//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], UNPAUSE)
        button_pose_quit(QUIT_norm, QUIT_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*5//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], QUIT)

        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_q:
                    click_sound.play()
                    screen.fill(white)
                    QUIT()
                if event.key == pygame.K_p:
                    click_sound.play()
                    pygame.mixer.music.unpause()
                    pause = not pause

        pygame.display.update()

def REGAME(FLAG, frame):
    pygame.mixer.music.pause() # music pause
    start = time.time()
    global pause
    pause = True
    while pause:
        screen.blit(frame, (0,0))
        MakeText("{}".format(math.ceil(10-(time.time()-start))), 200)
        if time.time()-start >= 10:
            screen.fill(white)
            QUIT()

        if FLAG == "FAIL":
            button_pose_quit(YES_norm, YES_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*2//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], UNPAUSE)
            button_pose_quit(NO_norm, NO_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*5//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], QUIT)
        else:
            button_pose_quit(YES_norm, YES_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*2//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], UNPAUSE)
            if not pause:
                return True
            button_pose_quit(NO_norm, NO_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*5//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], QUIT)

        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_p:
                    click_sound.play()
                    pause = not pause


        pygame.display.update()

def UNPAUSE() :
    pygame.mixer.music.unpause()
    global pause
    #pygame.mixer.music.unpause()
    pause = False

def QUIT() :
    '''
    start = time.time()
    while True:
        if time.time()-start >= 5:
            break
        screen.blit(QUIT_IMAGE, (0,0))
        screen.blit(QUIT_MENTION, ((display_width-QUIT_MENTION_SHAPE[0])//2, (display_height-QUIT_MENTION_SHAPE[1])//2))
    '''
    pygame.quit()
    quit()


def CHOOSE_GAME(CURRENT, PREV):
    PREV = CURRENT
    CURRENT = 1
    button(GAME1_norm, GAME1_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*2//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], CURRENT, 2)
    button(GAME2_norm, GAME2_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*5//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], CURRENT, 3)

    pygame.display.flip()

def GAME1(CURRENT, PREV):
    global screen, display_width, display_height
    PREV = CURRENT
    CURRENT = 2
    pygame.mixer.music.fadeout(2000)
    # load images for GAME1
    FIT_POSE = pygame.image.load("./image/p_00_position.png")
    FIT_POSE = pygame.transform.scale(FIT_POSE, (display_width//2, display_height*4//5))
    FIT_SHAPE = pygame.surfarray.array2d(FIT_POSE).shape
    HEY = pygame.image.load("./image/b_05_1_hey.png")
    READY_PRINT = pygame.image.load("./image/b_05_2_ready.png")
    READY_PRINT_SHAPE = pygame.surfarray.array2d(READY_PRINT).shape
    LOADING_SHAPE = pygame.surfarray.array2d(LOADING).shape
    FIT_PRINT = pygame.image.load("./image/p_00_position_1.png")
    FIT_PRINT_SHAPE = pygame.surfarray.array2d(FIT_PRINT).shape
    NOPERSON_PRINT = pygame.image.load("./image/p_00_position_2.png")
    NOPERSON_PRINT_SHAPE = pygame.surfarray.array2d(NOPERSON_PRINT).shape

    SUCCESS_PRINT = pygame.image.load("./image/p_08_success_word.png")
    SUCCESS_PRINT_SHAPE = pygame.surfarray.array2d(SUCCESS_PRINT).shape
    FAIL_PRINT = pygame.image.load("./image/p_10_fail_word.png")
    FAIL_PRINT_SHAPE = pygame.surfarray.array2d(FAIL_PRINT).shape
    SUCCESS_IMAGE = pygame.image.load("./image/p_09_success.png")
    SUCCESS_IMAGE_SHAPE = pygame.surfarray.array2d(SUCCESS_IMAGE).shape
    ROUND_CLEAR_PRINT = pygame.image.load("./image/p_09_clear_word.png")
    ROUND_CLEAR_PRINT_SHAPE = pygame.surfarray.array2d(ROUND_CLEAR_PRINT).shape

    # LOADING...
    screen.fill(white)
    screen.blit(LOADING, ((display_width-LOADING_SHAPE[0])//2,(display_height-LOADING_SHAPE[1])//2))
    pygame.display.flip()

    TIME_INIT = 5
    TIME_STAGE = 3
    # initialize flags
    FIT = True
    READY = False
    SUCCESS = False
    FAIL = False
    PRINT_SUCCESS = False
    NO_PERSON = False

    # load images about stages
    STAGE_1 = pygame.image.load("./image/pb_07_1_1.png")
    STAGE_2 = pygame.image.load("./image/pb_07_1_2.png")
    STAGE_3 = pygame.image.load("./image/pb_07_1_3.png")
    STAGE_DICT = {1: STAGE_1, 2: STAGE_2, 3: STAGE_3}
    STAGE_SHAPE = pygame.surfarray.array2d(STAGE_1).shape

    # for initializing
    from segmentation import SegImg
    from stage import DETERMINE_STAGE

    ret, img = camera.read()
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
                    click_sound.play()
                    start = time.time()
                    READY = True
                if event.key == pygame.K_p :
                    click_sound.play()
                    PAUSE()

        if not READY:
            if NO_PERSON:
                screen.blit(NOPERSON_PRINT, ((display_width-NOPERSON_PRINT_SHAPE[0])//2,(display_height-NOPERSON_PRINT_SHAPE[1])//2))
                if (time.time()-print_time) >= 5:
                    NO_PERSON = False
            elif FIT:
                screen.blit(FIT_PRINT, (display_width-FIT_PRINT_SHAPE[0],10))
                screen.blit(FIT_POSE, ((display_width-FIT_SHAPE[0])//2,display_height-FIT_SHAPE[1]))
                if TIME_INIT < time.time() - FIT_time:
                    FIT = False
            elif not SUCCESS and not FAIL:
                screen.blit(READY_PRINT, ((display_width-READY_PRINT_SHAPE[0])//2,(display_height-READY_PRINT_SHAPE[1])//2))
        else:
            if TIME_STAGE-(time.time()-start) <= 0.01:
                for i in len(sound_list) :
                    timer = "{}".format(math.ceil(TIME_INIT-(time.time()-start-TIME_STAGE)))
                    if float(timer) <= 0.01:
                        SUCCESS, FAIL = SegImg(img, READY, STAGE)
                        if not SUCCESS and not FAIL:
                            NO_PERSON = True
                        READY = False
                        PRINT_SUCCESS = True
                        print_time = time.time()

                    screen = STAGE.determine_stage(screen, False)
                    sound_list[i].play()
                    MakeText(timer, 200)
            else:
                screen.blit(STAGE_DICT[STAGE.ROUND], ((display_width-STAGE_SHAPE[0])//2,(display_height-STAGE_SHAPE[1])//2))

        if SUCCESS:
            if (time.time()-print_time) >= 5:
                STAGE.ROUND += 1
                if STAGE.ROUND > STAGE.ROUND_LIMIT:
                    READY = False
                    SUCCESS = True
                    FAIL = False
                    PRINT_SUCCESS = False
                    NO_PERSON = False

                    screen.blit(ROUND_CLEAR_PRINT, ((display_width-ROUND_CLEAR_PRINT_SHAPE[0])//2+300,ROUND_CLEAR_PRINT_SHAPE[1]//2))
                    screen.blit(SUCCESS_IMAGE, ((display_width-SUCCESS_IMAGE_SHAPE[0])//2-200,(display_height-SUCCESS_IMAGE_SHAPE[1])//2+100))
                    if (time.time()-print_time) >= 10:
                        screen.blit(frame, (0,0))
                        menu = REGAME("SUCCESS", frame)
                        if menu:
                            break

                else:
                    STAGE.version = {1: np.random.choice(STAGE.ROUND_1),
                                     2: np.random.choice(STAGE.ROUND_2)}.get(STAGE.ROUND)
                    SUCCESS = False
                    PRINT_SUCCESS = False

            else:
                screen.blit(SUCCESS_PRINT, ((display_width-SUCCESS_PRINT_SHAPE[0])//2+300,SUCCESS_PRINT_SHAPE[1]//2))
                screen.blit(SUCCESS_IMAGE, ((display_width-SUCCESS_IMAGE_SHAPE[0])//2-200,(display_height-SUCCESS_IMAGE_SHAPE[1])//2+100))

        elif FAIL:
            screen.blit(frame, (0,0))
            STAGE.version = {1: np.random.choice(STAGE.ROUND_1),
                             2: np.random.choice(STAGE.ROUND_2)}.get(STAGE.ROUND)
            screen.blit(FAIL_PRINT, ((display_width-FAIL_PRINT_SHAPE[0])//2+300,FAIL_PRINT_SHAPE[1]//2))
            screen.blit(SUCCESS_IMAGE, ((display_width-SUCCESS_IMAGE_SHAPE[0])//2-200,(display_height-SUCCESS_IMAGE_SHAPE[1])//2+100))
            if (time.time()-print_time) >= 5:
                FAIL = False
                PRINT_SUCCESS = False
                screen.blit(frame, (0,0))
                REGAME("FAIL", frame)

        pygame.display.flip()


def GAME2(CURRENT, PREV):
    screen.fill(white)
    QUIT()

MENU_LIST = np.array((True, False, False, False))
MENU = {0: INTRO, 1: CHOOSE_GAME, 2: GAME1, 3: GAME2}

def main():
    try:
        CURRENT = 0
        PREV = 0
        #intro_movie()
        pygame.mixer.music.play(-1, 0.0)
        while True:
            screen.fill(white)
            num_where = np.argmax(MENU_LIST)
            MENU[num_where](CURRENT, PREV)

            if num_where == 2 or num_where == 3:
                MENU_LIST[1] = True
                MENU_LIST[2] = False
                MENU_LIST[3] = False

            for event in pygame.event.get() :
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_q:
                        click_sound.play()
                        screen.fill(white)
                        QUIT()
                    if event.key == pygame.K_p:
                        click_sound.play()
                        screen.fill(white)
                        PAUSE()

    except KeyboardInterrupt or SystemExit :
        QUIT()

if __name__ == "__main__":
    main()
