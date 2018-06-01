import time
import cv2
import math

from visualize import *
from load import *
from settings import *

camera = cv2.VideoCapture(0)

def INTRO(CURRENT, PREV):
    PREV = CURRENT
    CURRENT = 0
    button(START_norm, START_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*2//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], CURRENT, 1)
    button(SETTING_norm, SETTING_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*4//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], CURRENT, 1)
    button_pose_quit(QUIT_norm, QUIT_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*6//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], QUIT)
    pygame.display.flip()


def PAUSE() :
    pygame.mixer.music.pause() # music pause
    click_sound.play()
    global pause
    pause = True
    screen.fill(white)

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
            button_pose_quit(FIRSTTIME_norm, FIRSTTIME_high, (display_width-RESTART_IMAGE_SHAPE[0])//2+50, (display_height-RESTART_IMAGE_SHAPE[1])//2+500, BUTTON_SHAPE[0], BUTTON_SHAPE[1], UNPAUSE)
            if not pause:
                return True
            button_pose_quit(RESTART_norm, RESTART_high, (display_width-RESTART_IMAGE_SHAPE[0])//2+RESTART_IMAGE_SHAPE[0]-50-BUTTON_SHAPE[0], (display_height-RESTART_IMAGE_SHAPE[1])//2+500, BUTTON_SHAPE[0], BUTTON_SHAPE[1], UNPAUSE)
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
    global screen
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
                        global go_menu
                        go_menu = REGAME("SUCCESS", frame)
                        if go_menu:
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
