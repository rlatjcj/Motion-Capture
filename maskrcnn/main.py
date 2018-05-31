import pygame
from pygame.locals import *
import cv2
import numpy as np
import time
import math
import sys


white = (255,255,255)
cyan = (0,200,200)

# =============================================================================
# pygame, display, music initialize
# =============================================================================

#initial
pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")
clock = pygame.time.Clock()

# Display for fullscreen
display_width = pygame.display.Info().current_w
display_height = pygame.display.Info().current_h

#Sound

click_sound = pygame.mixer.Sound("./sound/click.wav")
click_sound.set_volume(0.7)
time_one = pygame.mixer.Sound("./sound/1.wav")
time_one.set_volume(1)
time_two = pygame.mixer.Sound("./sound/2.wav")
time_two.set_volume(1)
time_three = pygame.mixer.Sound("./sound/3.wav")
time_three.set_volume(1)
time_four = pygame.mixer.Sound("./sound/4.wav")
time_four.set_volume(1)
time_five = pygame.mixer.Sound("./sound/5.wav")
time_five.set_volume(1)

sound_dict = {5: time_five, 4: time_four, 3: time_three, 2: time_two, 1: time_one}

# for fullscreen
#screen = pygame.display.set_mode([display_width, display_height], pygame.FULLSCREEN | pygame.NOFRAME | pygame.HWSURFACE, 32)
screen = pygame.display.set_mode([display_width, display_height])


# INTRO
START_norm = pygame.image.load("./image/b_01_start.png")
START_high = pygame.image.load("./image/bb_01_start.png")
QUIT_norm = pygame.image.load("./image/b_12_exit.png")
QUIT_high = pygame.image.load("./image/bb_12_exit.png")

# CHOOSE_GAME
GAME1_norm = pygame.image.load("./image/b_02_1.png")
GAME1_high = pygame.image.load("./image/bb_02_1.png")
GAME2_norm = pygame.image.load("./image/b_02_2.png")
GAME2_high = pygame.image.load("./image/bb_02_2.png")

# PAUSE
PAUSE_PRINT = pygame.image.load("./image/p_03_pause.png")
PAUSE_PRINT_SHAPE = pygame.surfarray.array2d(PAUSE_PRINT).shape
PAUSE_PRINT = pygame.transform.scale(PAUSE_PRINT, (PAUSE_PRINT_SHAPE[0]*2, PAUSE_PRINT_SHAPE[1]*2))
PAUSE_PRINT_SHAPE = pygame.surfarray.array2d(PAUSE_PRINT).shape
CONTINUE_norm = pygame.image.load("./image/b_04_continue.png")
CONTINUE_high = pygame.image.load("./image/bb_04_continue.png")

CHALLENGE_PRINT = pygame.image.load("./image/p_11_challenge_word.png")
CHALLENGE_PRINT_SHAPE = pygame.surfarray.array2d(CHALLENGE_PRINT).shape
CHALLENGE_IMAGE = pygame.image.load("./image/p_11_challenge.png")
CHALLENGE_IMAGE_SHAPE = pygame.surfarray.array2d(CHALLENGE_IMAGE).shape

YES_norm = pygame.image.load("./image/b_06_yes.png")
YES_high = pygame.image.load("./image/bb_06_yes.png")
NO_norm = pygame.image.load("./image/b_06_no.png")
NO_high = pygame.image.load("./image/bb_06_no.png")

QUIT_IMAGE = pygame.image.load("./image/p_13_2_end.png")
QUIT_IMAGE_SHAPE = pygame.surfarray.array2d(QUIT_IMAGE).shape
QUIT_MENTION = pygame.image.load("./image/p_13_1_end.png")
QUIT_MENTION_SHAPE = pygame.surfarray.array2d(QUIT_MENTION).shape

FIRSTTIME_norm = pygame.image.load("./image/b_06_firsttime.png")
FIRSTTIME_high = pygame.image.load("./image/bb_06_firsttime.png")
RESTART_norm = pygame.image.load("./image/b_06_restart.png")
RESTART_high = pygame.image.load("./image/bb_06_restart.png")
RESTART_IMAGE = pygame.image.load("./image/p_06_restart.png")
RESTART_IMAGE_SHAPE = pygame.surfarray.array2d(RESTART_IMAGE).shape

BUTTON_SHAPE = pygame.surfarray.array2d(START_norm).shape

# load images for GAME1
FIT_POSE = pygame.image.load("./image/p_00_position.png")
FIT_POSE = pygame.transform.scale(FIT_POSE, (display_width//2, display_height*4//5))
FIT_SHAPE = pygame.surfarray.array2d(FIT_POSE).shape
READY_PRINT = pygame.image.load("./image/b_05_2_ready.png")
READY_PRINT_SHAPE = pygame.surfarray.array2d(READY_PRINT).shape
READY_IMAGE = pygame.image.load("./image/p_05_ready_1.png")
READY_IMAGE_SHAPE = pygame.surfarray.array2d(READY_IMAGE).shape
LOADING = pygame.image.load("./image/b_05_3_loading.png")
LOADING_SHAPE = pygame.surfarray.array2d(LOADING).shape
LOADING_IMAGE = pygame.image.load("./image/p_05_ready_2.png")
LOADING_IMAGE_SHAPE = pygame.surfarray.array2d(LOADING_IMAGE).shape
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
FAIL_IMAGE = pygame.image.load("./image/p_10_fail.png")
FAIL_IMAGE_SHAPE = pygame.surfarray.array2d(FAIL_IMAGE).shape
ROUND_CLEAR_PRINT = pygame.image.load("./image/p_09_clear_word.png")
ROUND_CLEAR_PRINT_SHAPE = pygame.surfarray.array2d(ROUND_CLEAR_PRINT).shape

# load images about stages
STAGE_1 = pygame.image.load("./image/pb_07_1_1.png")
STAGE_2 = pygame.image.load("./image/pb_07_1_2.png")
STAGE_3 = pygame.image.load("./image/pb_07_1_3.png")
STAGE_DICT = {1: STAGE_1, 2: STAGE_2, 3: STAGE_3}
STAGE_SHAPE = pygame.surfarray.array2d(STAGE_1).shape


# =============================================================================
# function
# =============================================================================


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
        screen.blit(PAUSE_PRINT, ((display_width-PAUSE_PRINT_SHAPE[0])//2, PAUSE_PRINT_SHAPE[1]//4))
        button_pose_quit(CONTINUE_norm, CONTINUE_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*2//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], UNPAUSE)
        button_pose_quit(QUIT_norm, QUIT_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*5//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], QUIT)

        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_p:
                    click_sound.play()
                    pygame.mixer.music.unpause()
                    pause = not pause

        pygame.display.update()

def REGAME(FLAG, frame):
    global pause
    pause = True

    while pause:
        screen.blit(frame, (0,0))

        if FLAG == "FAIL":
            screen.blit(CHALLENGE_PRINT, ((display_width-CHALLENGE_PRINT_SHAPE[0])*3//4, (display_height-CHALLENGE_PRINT_SHAPE[1])*2//7))
            screen.blit(CHALLENGE_IMAGE, ((display_width-CHALLENGE_IMAGE_SHAPE[0])//4, (display_height-CHALLENGE_IMAGE_SHAPE[1])*4//7))
            button_pose_quit(YES_norm, YES_high, (display_width-BUTTON_SHAPE[0])//4, (display_height-BUTTON_SHAPE[1])*6//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], UNPAUSE)
            button_pose_quit(NO_norm, NO_high, (display_width-BUTTON_SHAPE[0])*3//4, (display_height-BUTTON_SHAPE[1])*6//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], QUIT)
        else:
            screen.blit(RESTART_IMAGE, ((display_width-RESTART_IMAGE_SHAPE[0])//2,(display_height-RESTART_IMAGE_SHAPE[1])//2))
            button_pose_quit(FIRSTTIME_norm, FIRSTTIME_high, (display_width-BUTTON_SHAPE[0])*2//7, (display_height-BUTTON_SHAPE[1])*5//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], UNPAUSE)
            if not pause:
                return True
            button_pose_quit(RESTART_norm, RESTART_high, (display_width-BUTTON_SHAPE[0])*5//7, (display_height-BUTTON_SHAPE[1])*5//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], UNPAUSE)
            if not pause:
                return False

        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_p:
                    click_sound.play()
                    pygame.mixer.music.unpause()
                    pause = not pause

        pygame.display.update()

def UNPAUSE() :
    pygame.mixer.music.unpause()
    global pause
    pause = False

def QUIT() :
    screen.fill(white)
    #screen.blit(QUIT_IMAGE, (0,0))
    #screen.blit(QUIT_MENTION, ((display_width-QUIT_MENTION_SHAPE[0])//2, (display_height-QUIT_MENTION_SHAPE[1])//2))

    #time.sleep(5)
    pygame.quit()
    quit()


def CHOOSE_GAME(CURRENT, PREV):
    PREV = CURRENT
    CURRENT = 1
    button(GAME1_norm, GAME1_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*2//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], CURRENT, 2)
    button(GAME2_norm, GAME2_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*5//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], CURRENT, 3)

    pygame.display.flip()

def GAME1(CURRENT, PREV):
    pygame.mixer.music.fadeout(2000)
    global screen, display_width, display_height
    PREV = CURRENT
    CURRENT = 2

    # LOADING...
    screen.fill(white)
    screen.blit(LOADING, ((display_width-LOADING_SHAPE[0])*2//3,(display_height-LOADING_SHAPE[1])//3))
    screen.blit(LOADING_IMAGE, ((display_width-LOADING_IMAGE_SHAPE[0])//3,(display_height-LOADING_IMAGE_SHAPE[1])*2//3))
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

    # for initializing
    from segmentation import SegImg
    from stage import DETERMINE_STAGE

    camera = cv2.VideoCapture(0)
    ret, img = camera.read()
    STAGE = DETERMINE_STAGE(display_height, display_width)
    SegImg(img, READY, STAGE)

    FIT_time = time.time()
    MUSIC_FLAG = True

    while True:
        ret, img = camera.read()
        if not ret:
            raise

        if MUSIC_FLAG:
            if STAGE.ROUND == 1:
                pygame.mixer.music.load("./sound/game_bgm1.mp3")
                pygame.mixer.music.play(-1, 0.0)
                MUSIC_FLAG = False
            elif STAGE.ROUND == 2:
                screen.fill(white)
                screen.blit(LOADING, ((display_width-LOADING_SHAPE[0])*2//3,(display_height-LOADING_SHAPE[1])//3))
                screen.blit(LOADING_IMAGE, ((display_width-LOADING_IMAGE_SHAPE[0])//3,(display_height-LOADING_IMAGE_SHAPE[1])*2//3))
                pygame.display.flip()
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.load("./sound/game_bgm2.mp3")
                pygame.mixer.music.play(-1, 0.0)
                MUSIC_FLAG = False
            elif STAGE.ROUND == 3:
                screen.fill(white)
                screen.blit(LOADING, ((display_width-LOADING_SHAPE[0])*2//3,(display_height-LOADING_SHAPE[1])//3))
                screen.blit(LOADING_IMAGE, ((display_width-LOADING_IMAGE_SHAPE[0])//3,(display_height-LOADING_IMAGE_SHAPE[1])*2//3))
                pygame.display.flip()
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.load("./sound/game_bgm3.mp3")
                pygame.mixer.music.play(-1, 0.0)
                MUSIC_FLAG = False

        frame = video_setting(img)
        screen.blit(frame, (0,0))

        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE:
                    click_sound.play()
                    start = time.time()
                    READY = True
                    TIMER = True
                    timer_sound = 6
                if event.key == pygame.K_p :
                    click_sound.play()
                    PAUSE()

        if not READY:
            if NO_PERSON:
                pygame.mixer.music.set_volume(1)
                screen.blit(NOPERSON_PRINT, ((display_width-NOPERSON_PRINT_SHAPE[0])//2,(display_height-NOPERSON_PRINT_SHAPE[1])//2))
                if (time.time()-print_time) >= 5:
                    NO_PERSON = False
            elif FIT:
                screen.blit(FIT_PRINT, (display_width-FIT_PRINT_SHAPE[0],10))
                screen.blit(FIT_POSE, ((display_width-FIT_SHAPE[0])//2,display_height-FIT_SHAPE[1]))
                if TIME_INIT < time.time() - FIT_time:
                    FIT = False
            elif not SUCCESS and not FAIL:
                screen.blit(READY_IMAGE, ((display_width-READY_IMAGE_SHAPE[0])//3,(display_height-READY_IMAGE_SHAPE[1])*2//3))
                screen.blit(READY_PRINT, ((display_width-READY_PRINT_SHAPE[0])*2//3,(display_height-READY_PRINT_SHAPE[1])//3))
        else:
            if TIME_STAGE-(time.time()-start) <= 0.01:
                timer = math.ceil(TIME_INIT-(time.time()-start-TIME_STAGE))

                if float(timer) <= 0.01:
                    SUCCESS, FAIL = SegImg(img, READY, STAGE)
                    if not SUCCESS and not FAIL:
                        NO_PERSON = True
                    READY = False
                    PRINT_SUCCESS = True
                    print_time = time.time()

                screen = STAGE.determine_stage(screen, False)
                if timer_sound-timer == 1:
                    timer_sound = timer
                    if timer != 0:
                        sound_dict[timer].play()

                pygame.mixer.music.set_volume(0.5)
                MakeText("{}".format(timer), 200)


            else:
                screen.blit(STAGE_DICT[STAGE.ROUND], ((display_width-STAGE_SHAPE[0])//2,(display_height-STAGE_SHAPE[1])//2))

        if SUCCESS:
            pygame.mixer.music.set_volume(1)
            screen.blit(frame, (0,0))
            if (time.time()-print_time) >= 5:
                STAGE.ROUND += 1
                MUSIC_FLAG = True
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
                        global menu
                        menu = REGAME("SUCCESS", frame)
                        if menu:
                            pygame.mixer.music.fadeout(1000)
                            MENU_LIST[0] = True
                            MENU_LIST[1] = False
                            MENU_LIST[2] = False
                            MENU_LIST[3] = False
                            break
                        else:
                            break

                else:
                    STAGE.version = {1: np.random.choice(STAGE.ROUND_1),
                                     2: np.random.choice(STAGE.ROUND_2),
                                     3: np.random.choice(STAGE.ROUND_3)}.get(STAGE.ROUND)
                    SUCCESS = False
                    PRINT_SUCCESS = False

            else:
                screen.blit(SUCCESS_PRINT, ((display_width-SUCCESS_PRINT_SHAPE[0])//2+300,SUCCESS_PRINT_SHAPE[1]//2))
                screen.blit(SUCCESS_IMAGE, ((display_width-SUCCESS_IMAGE_SHAPE[0])//2-200,(display_height-SUCCESS_IMAGE_SHAPE[1])//2+100))

        elif FAIL:
            pygame.mixer.music.set_volume(1)
            screen.blit(frame, (0,0))
            STAGE.version = {1: np.random.choice(STAGE.ROUND_1),
                             2: np.random.choice(STAGE.ROUND_2),
                             3: np.random.choice(STAGE.ROUND_3)}.get(STAGE.ROUND)
            screen.blit(FAIL_PRINT, ((display_width-FAIL_PRINT_SHAPE[0])*3//4,(display_height-FAIL_PRINT_SHAPE[1])*2//7))
            screen.blit(FAIL_IMAGE, ((display_width-FAIL_IMAGE_SHAPE[0])//2-200,(display_height-FAIL_IMAGE_SHAPE[1])//2+100))
            if (time.time()-print_time) >= 5:
                FAIL = False
                PRINT_SUCCESS = False
                screen.blit(frame, (0,0))
                REGAME("FAIL", frame)

        pygame.display.flip()


def GAME2(CURRENT, PREV):
    QUIT()

MENU_LIST = np.array((True, False, False, False))
MENU = {0: INTRO, 1: CHOOSE_GAME, 2: GAME1, 3: GAME2}

def main():
    try:
        intro = cv2.VideoCapture("./sound/kt_motion_intro.mp4")
        while True:
            ret, img = intro.read()
            if not ret:
                break
            frame_intro = video_setting(img, True)
            screen.blit(frame_intro, (0,0))
            pygame.display.flip()
            clock.tick(30)

        CURRENT = 0
        PREV = 0
        INTRO_MUSIC = True
        global menu
        menu = False

        while True:
            if INTRO_MUSIC:
                pygame.mixer.music.load("./sound/bgm4.mp3")
                pygame.mixer.music.play(-1, 0.0)
                INTRO_MUSIC = False

            screen.fill(white)
            num_where = np.argmax(MENU_LIST)
            MENU[num_where](CURRENT, PREV)
            if (num_where == 2 or num_where == 3) and menu:
                INTRO_MUSIC =True

            for event in pygame.event.get() :
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_p:
                        click_sound.play()
                        PAUSE()

    except KeyboardInterrupt or SystemExit :
        QUIT()

if __name__ == "__main__":
    main()
