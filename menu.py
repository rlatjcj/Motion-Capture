import time
import cv2
import math

from load import *
from settings import *
from visualize import *

VIDEO = 0
camera = cv2.VideoCapture(VIDEO)
LIMIT = 2
teambattle = False


def INTRO(CURRENT, PREV):
    PREV = CURRENT
    CURRENT = 0
    button(START_norm, START_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*2//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], CURRENT, 1)
    button(SETTING_norm, SETTING_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*4//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], CURRENT, 4)
    button_pose_quit(QUIT_norm, QUIT_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*6//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], QUIT)
    pygame.display.flip()

def SETTING(CURRENT, PREV):
    global LIMIT, teambattle
    PREV = CURRENT
    CURRENT = 4

    screen.blit(PERSON_PRINT, ((display_width-PERSON_PRINT_SHAPE[0])//3, (display_height-PERSON_PRINT_SHAPE[1])*2//8))
    screen.blit(TEAMBATTLE_PRINT, ((display_width-TEAMBATTLE_PRINT_SHAPE[0])//3, (display_height-TEAMBATTLE_PRINT_SHAPE[1])*4//8))
    LIMIT = updown(UP_norm, UP_high, display_width//2+UPDOWN_SHAPE[0], (display_height-PERSON_PRINT_SHAPE[1])*2//8+PERSON_PRINT_SHAPE[1]//2-UPDOWN_SHAPE[1]-10, UPDOWN_SHAPE[0], UPDOWN_SHAPE[1], LIMIT)
    LIMIT = updown(DOWN_norm, DOWN_high, display_width//2+UPDOWN_SHAPE[0], (display_height-PERSON_PRINT_SHAPE[1])*2//8+PERSON_PRINT_SHAPE[1]//2+10, UPDOWN_SHAPE[0], UPDOWN_SHAPE[1], LIMIT)
    MakeText("{}".format(LIMIT), 100)
    # need to change button
    teambattle = onoff(ON, OFF, display_width//2, (display_height-ONOFF_SHAPE[1])*4//8, ONOFF_SHAPE[0], ONOFF_SHAPE[1], teambattle)
    button(GOBACK_norm, GOBACK_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*6//8, BUTTON_SHAPE[0], BUTTON_SHAPE[1], CURRENT, 0)

    pygame.display.flip()


def PAUSE(CURRENT, PREV) :
    pygame.mixer.music.pause() # music pause
    click_sound.play()
    global pause
    pause = True
    screen.fill(white)

    while pause :
        screen.blit(PAUSE_PRINT, ((display_width-PAUSE_PRINT_SHAPE[0])//2, PAUSE_PRINT_SHAPE[1]//4))
        button_pose_quit(FIRSTTIME_norm, FIRSTTIME_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*4//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], UNPAUSE)
        if not pause:
            if CURRENT == 0 or CURRENT == 1 or CURRENT == 4:
                MENU_LIST[CURRENT] = False
                MENU_LIST[0] = True
                break
            elif CURRENT == 2 or CURRENT == 3:
                return True
        button_pose_quit(CONTINUE_norm, CONTINUE_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*2//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], UNPAUSE)
        button_pose_quit(QUIT_norm, QUIT_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*6//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], QUIT)

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
            screen.blit(CHALLENGE_IMAGE, ((display_width-CHALLENGE_IMAGE_SHAPE[0])*2//7, (display_height-CHALLENGE_IMAGE_SHAPE[1])*4//7))
            button_pose_quit(FIRSTTIME_norm, FIRSTTIME_high, (display_width-BUTTON_SHAPE[0])*3//4, (display_height-BUTTON_SHAPE[1])*6//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], UNPAUSE)
            if not pause:
                return True
            button_pose_quit(YES_norm, YES_high, (display_width-BUTTON_SHAPE[0])//4, (display_height-BUTTON_SHAPE[1])*6//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], UNPAUSE)
        else:
            screen.blit(RESTART_PRINT, ((display_width-RESTART_PRINT_SHAPE[0])//2,(display_height-RESTART_PRINT_SHAPE[1])//2))
            button_pose_quit(FIRSTTIME_norm, FIRSTTIME_high, (display_width-RESTART_PRINT_SHAPE[0])//2+50, (display_height-RESTART_PRINT_SHAPE[1])//2+500, BUTTON_SHAPE[0], BUTTON_SHAPE[1], UNPAUSE)
            if not pause:
                return True
            button_pose_quit(RESTART_norm, RESTART_high, (display_width-RESTART_PRINT_SHAPE[0])//2+RESTART_PRINT_SHAPE[0]-BUTTON_SHAPE[0]-50, (display_height-RESTART_PRINT_SHAPE[1])//2+500, BUTTON_SHAPE[0], BUTTON_SHAPE[1], UNPAUSE)
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
    button(GAME2_norm, GAME2_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*4//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], CURRENT, 3)
    button(GOBACK_norm, GOBACK_high, (display_width-BUTTON_SHAPE[0])//2, (display_height-BUTTON_SHAPE[1])*6//7, BUTTON_SHAPE[0], BUTTON_SHAPE[1], CURRENT, 0)

    pygame.display.flip()

def GAME1(CURRENT, PREV):
    pygame.mixer.music.fadeout(2000)
    global screen, LIMIT, teambattle, go_menu
    PREV = CURRENT
    CURRENT = 2

    # LOADING...
    loading()

    TIME_INIT = 5
    TIME_STAGE = 3
    # initialize flags
    FIT = True
    READY = False
    SUCCESS = False
    FAIL = False
    PRINT_SUCCESS = False
    NO_PERSON = False
    MUSIC_FLAG = True
    go_menu = False

    # for initializing
    from segmentation import SegImg
    from stage import DETERMINE_STAGE

    ret, img = camera.read()
    img_ratio = img.shape[0] / img.shape[1]
    STAGE = DETERMINE_STAGE(display_height, display_width, img_ratio)
    SegImg(img, READY, STAGE, LIMIT, GAME=True)

    # for teambattle
    TEAM_LIST = ("DADDY", "MOMMY")
    TEAM_ORDER = ("FITST", "NEXT")
    TEAM_CNT = 0
    SUCCESS_CNT = {0: 0, 1: 0}

    while True:
        ret, img = camera.read()
        if not ret:
            raise

        if MUSIC_FLAG:
            if STAGE.ROUND == 1:
                if TEAM_CNT == 1:
                    loading()
                    pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.load("./sound/game_bgm1.mp3")
                pygame.mixer.music.play(-1, 0.0)
                MUSIC_FLAG = False
            elif STAGE.ROUND == 2:
                loading()
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.load("./sound/game_bgm2.mp3")
                pygame.mixer.music.play(-1, 0.0)
                MUSIC_FLAG = False
            elif STAGE.ROUND == 3:
                loading()
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.load("./sound/game_bgm3.mp3")
                pygame.mixer.music.play(-1, 0.0)
                MUSIC_FLAG = False

        frame = video_setting(img)
        screen.blit(frame, (0,0))

        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_p :
                    click_sound.play()
                    go_menu = PAUSE(CURRENT, PREV)

        # for pause
        if go_menu:
            pygame.mixer.music.fadeout(1000)
            MENU_LIST[0] = True
            MENU_LIST[1] = False
            MENU_LIST[2] = False
            MENU_LIST[3] = False
            break

        if not READY:
            if NO_PERSON:
                NO_PERSON = noperson(print_time)
            elif FIT:
                FIT = position()
            elif not SUCCESS and not FAIL:
                screen.blit(READY_IMAGE, ((display_width-READY_IMAGE_SHAPE[0])//3,(display_height-READY_IMAGE_SHAPE[1])*3//4))
                screen.blit(READY_PRINT, ((display_width-READY_PRINT_SHAPE[0])*3//4,(display_height-READY_PRINT_SHAPE[1])//6))
                if teambattle and STAGE.ROUND == 1:
                    if TEAM_CNT == 0:
                        screen.blit(DADDY_READY_PRINT, ((display_width-DADDY_READY_PRINT_SHAPE[0])*3//4,(display_height-DADDY_READY_PRINT_SHAPE[1])//6))
                    elif TEAM_CNT == 1:
                        screen.blit(MOMMY_READY_PRINT, ((display_width-MOMMY_READY_PRINT_SHAPE[0])*3//4,(display_height-MOMMY_READY_PRINT_SHAPE[1])//6))
                for event in pygame.event.get() :
                    if event.type == pygame.KEYDOWN :
                        if event.key == pygame.K_SPACE:
                            click_sound.play()
                            start = time.time()
                            READY = True
                            timer_sound = 6
        else:
            if TIME_STAGE-(time.time()-start) <= 0.01:
                timer = math.ceil(TIME_INIT-(time.time()-start-TIME_STAGE))

                if float(timer) <= 0.01:
                    SUCCESS, FAIL, result = SegImg(img, READY, STAGE, LIMIT, True)

                    if not SUCCESS and not FAIL:
                        NO_PERSON = True
                    else:
                        # for check segmentation
                        seg_shape = result.shape
                        result = seg_setting(result)
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
                if not MUSIC_FLAG:
                    MUSIC_FLAG = True
                    SUCCESS_CNT[TEAM_CNT] += 1

                # if you done all round
                if STAGE.ROUND > STAGE.ROUND_LIMIT:
                    if not teambattle:
                        READY = False
                        SUCCESS = True
                        FAIL = False
                        PRINT_SUCCESS = False
                        NO_PERSON = False

                        screen.blit(ROUND_CLEAR_PRINT, ((display_width-ROUND_CLEAR_PRINT_SHAPE[0])//2+300,ROUND_CLEAR_PRINT_SHAPE[1]//2))
                        screen.blit(ROUND_CLEAR_IMAGE, ((display_width-ROUND_CLEAR_IMAGE_SHAPE[0])//2-200,(display_height-ROUND_CLEAR_IMAGE_SHAPE[1])//2+100))
                        if (time.time()-print_time) >= 10:
                            screen.blit(frame, (0,0))
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
                        if (time.time()-print_time) >= 10:
                            if TEAM_CNT == 0:
                                TEAM_CNT += 1
                                READY = False
                                SUCCESS = False
                                FAIL = False
                                PRINT_SUCCESS = False
                                NO_PERSON = False
                                STAGE.ROUND = 1
                                STAGE.version = {1: np.random.choice(STAGE.ROUND_1)}.get(STAGE.ROUND)
                            elif TEAM_CNT == 1:
                                    screen.blit(frame, (0,0))
                                    print(SUCCESS_CNT[0], SUCCESS_CNT[1])
                                    if SUCCESS_CNT[0] > SUCCESS_CNT[1]:
                                        screen.blit(DADDY_WIN_PRINT, ((display_width-DADDY_WIN_PRINT_SHAPE[0])//2+300,DADDY_WIN_PRINT_SHAPE[1]//2))
                                        screen.blit(ROUND_CLEAR_IMAGE, ((display_width-ROUND_CLEAR_IMAGE_SHAPE[0])//2-200,(display_height-ROUND_CLEAR_IMAGE_SHAPE[1])//2+100))
                                    elif SUCCESS_CNT[0] < SUCCESS_CNT[1]:
                                        screen.blit(MOMMY_WIN_PRINT, ((display_width-MOMMY_WIN_PRINT_SHAPE[0])//2+300,MOMMY_WIN_PRINT_SHAPE[1]//2))
                                        screen.blit(ROUND_CLEAR_IMAGE, ((display_width-ROUND_CLEAR_IMAGE_SHAPE[0])//2-200,(display_height-ROUND_CLEAR_IMAGE_SHAPE[1])//2+100))
                                    elif SUCCESS_CNT[0] == SUCCESS_CNT[1]:
                                        screen.blit(DRAW_PRINT, ((display_width-DRAW_PRINT_SHAPE[0])//2+300,DRAW_PRINT_SHAPE[1]//2))
                                        screen.blit(DRAW_IMAGE, ((display_width-DRAW_IMAGE_SHAPE[0])//2-200,(display_height-DRAW_IMAGE_SHAPE[1])//2+100))

                                    if (time.time()-print_time) >= 15:
                                        screen.blit(frame, (0,0))
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
                            screen.blit(ROUND_CLEAR_IMAGE, ((display_width-ROUND_CLEAR_IMAGE_SHAPE[0])//2-200,(display_height-ROUND_CLEAR_IMAGE_SHAPE[1])//2+100))
                            if TEAM_CNT == 0:
                                screen.blit(DADDY_ROUND_CLEAR_PRINT, ((display_width-DADDY_ROUND_CLEAR_PRINT_SHAPE[0])//2+300,DADDY_ROUND_CLEAR_PRINT_SHAPE[1]//11))
                            elif TEAM_CNT == 1:
                                screen.blit(MOMMY_ROUND_CLEAR_PRINT, ((display_width-MOMMY_ROUND_CLEAR_PRINT_SHAPE[0])//2+300,MOMMY_ROUND_CLEAR_PRINT_SHAPE[1]//11))


                else:
                    STAGE.version = {1: np.random.choice(STAGE.ROUND_1),
                                     2: np.random.choice(STAGE.ROUND_2),
                                     3: np.random.choice(STAGE.ROUND_3)}.get(STAGE.ROUND)
                    SUCCESS = False
                    PRINT_SUCCESS = False

            else:
                # for check segmentation
                screen.blit(result, (display_width-seg_shape[1],display_height-seg_shape[0]))
                screen.blit(SUCCESS_PRINT, ((display_width-SUCCESS_PRINT_SHAPE[0])//2+300,SUCCESS_PRINT_SHAPE[1]//2))
                screen.blit(SUCCESS_IMAGE, ((display_width-SUCCESS_IMAGE_SHAPE[0])//2-200,(display_height-SUCCESS_IMAGE_SHAPE[1])//2+100))

        elif FAIL:
            pygame.mixer.music.set_volume(1)
            screen.blit(frame, (0,0))
            if not teambattle:
                # for check segmentation
                screen.blit(result, (display_width-seg_shape[1],display_height-seg_shape[0]))
                screen.blit(FAIL_PRINT, ((display_width-FAIL_PRINT_SHAPE[0])*3//4,FAIL_PRINT_SHAPE[1]//2))
                screen.blit(FAIL_IMAGE, ((display_width-FAIL_IMAGE_SHAPE[0])//2-200,(display_height-FAIL_IMAGE_SHAPE[1])//2+100))
                if (time.time()-print_time) >= 5:
                    FAIL = False
                    PRINT_SUCCESS = False
                    screen.blit(frame, (0,0))
                    go_menu = REGAME("FAIL", frame)
                    if go_menu:
                        pygame.mixer.music.fadeout(1000)
                        MENU_LIST[0] = True
                        MENU_LIST[1] = False
                        MENU_LIST[2] = False
                        MENU_LIST[3] = False
                        break
                    STAGE.version = {1: np.random.choice(STAGE.ROUND_1),
                                     2: np.random.choice(STAGE.ROUND_2),
                                     3: np.random.choice(STAGE.ROUND_3)}.get(STAGE.ROUND)

            else:
                if (time.time()-print_time) >= 5:
                    if TEAM_CNT == 0:
                        TEAM_CNT += 1
                        READY = False
                        SUCCESS = False
                        FAIL = False
                        PRINT_SUCCESS = False
                        NO_PERSON = False
                        STAGE.ROUND = 1
                        MUSIC_FLAG = True
                        STAGE.version = {1: np.random.choice(STAGE.ROUND_1)}.get(STAGE.ROUND)
                    else:
                        if SUCCESS_CNT[0] > SUCCESS_CNT[1]:
                            screen.blit(DADDY_WIN_PRINT, ((display_width-DADDY_WIN_PRINT_SHAPE[0])//2+300,DADDY_WIN_PRINT_SHAPE[1]//2))
                            screen.blit(ROUND_CLEAR_IMAGE, ((display_width-ROUND_CLEAR_IMAGE_SHAPE[0])//2-200,(display_height-ROUND_CLEAR_IMAGE_SHAPE[1])//2+100))
                        elif SUCCESS_CNT[0] < SUCCESS_CNT[1]:
                            screen.blit(MOMMY_WIN_PRINT, ((display_width-MOMMY_WIN_PRINT_SHAPE[0])//2+300,MOMMY_WIN_PRINT_SHAPE[1]//2))
                            screen.blit(ROUND_CLEAR_IMAGE, ((display_width-ROUND_CLEAR_IMAGE_SHAPE[0])//2-200,(display_height-ROUND_CLEAR_IMAGE_SHAPE[1])//2+100))
                        elif SUCCESS_CNT[0] == SUCCESS_CNT[1]:
                            screen.blit(DRAW_PRINT, ((display_width-DRAW_PRINT_SHAPE[0])//2+300,DRAW_PRINT_SHAPE[1]//2))
                            screen.blit(DRAW_IMAGE, ((display_width-DRAW_IMAGE_SHAPE[0])//2-200,(display_height-DRAW_IMAGE_SHAPE[1])//2+100))

                        if (time.time()-print_time) >= 10:
                            screen.blit(frame, (0,0))
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
                    # for check segmentation
                    if TEAM_CNT == 0:
                        screen.blit(result, (display_width-seg_shape[1],display_height-seg_shape[0]))
                        screen.blit(FAIL_IMAGE, ((display_width-FAIL_IMAGE_SHAPE[0])//2-200,(display_height-FAIL_IMAGE_SHAPE[1])//2+100))
                        screen.blit(DADDY_FAIL_PRINT, ((display_width-DADDY_FAIL_PRINT_SHAPE[0])//2+300,DADDY_FAIL_PRINT_SHAPE[1]//4))
                    elif TEAM_CNT == 1:
                        screen.blit(result, (display_width-seg_shape[1],display_height-seg_shape[0]))
                        screen.blit(FAIL_IMAGE, ((display_width-FAIL_IMAGE_SHAPE[0])//2-200,(display_height-FAIL_IMAGE_SHAPE[1])//2+100))
                        screen.blit(MOMMY_FAIL_PRINT, ((display_width-DADDY_FAIL_PRINT_SHAPE[0])//2+300,DADDY_FAIL_PRINT_SHAPE[1]//4))

        pygame.display.flip()






def GAME2(CURRENT, PREV):
    pygame.mixer.music.fadeout(2000)
    global screen, LIMIT, teambattle, go_menu
    PREV = CURRENT
    CURRENT = 3

    # LOADING...
    loading()

    TIME_INIT = 5
    TIME_STAGE = 3
    # initialize flags
    FIT = True
    READY = False
    SUCCESS = False
    FAIL = False
    PRINT_SUCCESS = False
    NO_PERSON = False
    MUSIC_FLAG = True
    go_menu = False

    # for initializing
    from segmentation import SegImg
    from stage import DETERMINE_STAGE2

    ret, img = camera.read()
    STAGE = DETERMINE_STAGE2(display_height, display_width)
    SegImg(img, READY, STAGE, LIMIT, GAME=False)

    # for teambattle
    TEAM_LIST = ("DADDY", "MOMMY")
    TEAM_ORDER = ("FITST", "NEXT")
    TEAM_CNT = 0
    SUCCESS_CNT = {0: 0, 1: 0}

    while True:
        ret, img = camera.read()
        if not ret:
            raise

        if MUSIC_FLAG:
            if STAGE.ROUND == 1:
                if TEAM_CNT == 1:
                    loading()
                    pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.load("./sound/game_bgm1.mp3")
                pygame.mixer.music.play(-1, 0.0)
                MUSIC_FLAG = False
            elif STAGE.ROUND == 2:
                loading()
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.load("./sound/game_bgm2.mp3")
                pygame.mixer.music.play(-1, 0.0)
                MUSIC_FLAG = False


        frame = video_setting(img)
        screen.blit(frame, (0,0))

        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_p :
                    click_sound.play()
                    go_menu = PAUSE(CURRENT, PREV)

        # for pause
        if go_menu:
            pygame.mixer.music.fadeout(1000)
            MENU_LIST[0] = True
            MENU_LIST[1] = False
            MENU_LIST[2] = False
            MENU_LIST[3] = False
            break

        if not READY:
            if NO_PERSON:
                NO_PERSON = noperson2(print_time, result)
            elif FIT:
                FIT = position2()
            elif not SUCCESS and not FAIL:
                screen.blit(READY_IMAGE, ((display_width-READY_IMAGE_SHAPE[0])//3,(display_height-READY_IMAGE_SHAPE[1])*3//4))
                screen.blit(READY_PRINT, ((display_width-READY_PRINT_SHAPE[0])*3//4,(display_height-READY_PRINT_SHAPE[1])//6))
                if teambattle and STAGE.ROUND == 1:
                    if TEAM_CNT == 0:
                        screen.blit(DADDY_READY_PRINT, ((display_width-DADDY_READY_PRINT_SHAPE[0])*3//4,(display_height-DADDY_READY_PRINT_SHAPE[1])//6))
                    elif TEAM_CNT == 1:
                        screen.blit(MOMMY_READY_PRINT, ((display_width-MOMMY_READY_PRINT_SHAPE[0])*3//4,(display_height-MOMMY_READY_PRINT_SHAPE[1])//6))
                for event in pygame.event.get() :
                    if event.type == pygame.KEYDOWN :
                        if event.key == pygame.K_SPACE:
                            click_sound.play()
                            start = time.time()
                            READY = True
                            timer_sound = 6
        # if READY = TRUE
        else:
            if TIME_STAGE-(time.time()-start) <= 0.01:
                timer = math.ceil(TIME_INIT-(time.time()-start-TIME_STAGE))

                if float(timer) <= 0.01:
                    SUCCESS, FAIL, result = SegImg(img, READY, STAGE, LIMIT, False)

                    if not SUCCESS and not FAIL:
                        NO_PERSON = True
                    else:
                        # for check segmentation
                        seg_shape = result.shape
                        result = seg_setting(result)
                    READY = False
                    PRINT_SUCCESS = True
                    print_time = time.time()

                screen = STAGE.determine_stage(screen)
                if timer_sound-timer == 1:
                    timer_sound = timer
                    if timer != 0:
                        sound_dict[timer].play()

                pygame.mixer.music.set_volume(0.5)
                MakeText2("{}".format(timer), 200)

            else:
                screen.blit(STAGE_DICT2[STAGE.ROUND], ((display_width-GAME2_STAGE_SHAPE[0])//2,(display_height-GAME2_STAGE_SHAPE[1])//2))

        if SUCCESS:
            pygame.mixer.music.set_volume(1)
            screen.blit(frame, (0,0))
            if (time.time()-print_time) >= 5:
                STAGE.ROUND += 1
                if not MUSIC_FLAG:
                    MUSIC_FLAG = True
                    SUCCESS_CNT[TEAM_CNT] += 1


                # if you done all round
                if STAGE.ROUND > STAGE.ROUND_LIMIT:
                    if not teambattle:
                        READY = False
                        SUCCESS = True
                        FAIL = False
                        PRINT_SUCCESS = False
                        NO_PERSON = False

                        screen.blit(ROUND_CLEAR_PRINT, ((display_width-ROUND_CLEAR_PRINT_SHAPE[0])//2+300,ROUND_CLEAR_PRINT_SHAPE[1]//2))
                        screen.blit(ROUND_CLEAR_IMAGE, ((display_width-ROUND_CLEAR_IMAGE_SHAPE[0])//2-200,(display_height-ROUND_CLEAR_IMAGE_SHAPE[1])//2+100))
                        if (time.time()-print_time) >= 10:
                            screen.blit(frame, (0,0))
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
                        if (time.time()-print_time) >= 10:
                            if TEAM_CNT == 0:
                                TEAM_CNT += 1
                                READY = False
                                SUCCESS = False
                                FAIL = False
                                PRINT_SUCCESS = False
                                NO_PERSON = False
                                STAGE.ROUND = 1
                                STAGE.version = {1: np.random.choice(STAGE.ROUND_1)}.get(STAGE.ROUND)
                            elif TEAM_CNT == 1:
                                    screen.blit(frame, (0,0))
                                    print(SUCCESS_CNT[0], SUCCESS_CNT[1])
                                    if SUCCESS_CNT[0] > SUCCESS_CNT[1]:
                                        screen.blit(DADDY_WIN_PRINT, ((display_width-DADDY_WIN_PRINT_SHAPE[0])//2+300,DADDY_WIN_PRINT_SHAPE[1]//2))
                                        screen.blit(ROUND_CLEAR_IMAGE, ((display_width-ROUND_CLEAR_IMAGE_SHAPE[0])//2-200,(display_height-ROUND_CLEAR_IMAGE_SHAPE[1])//2+100))
                                    elif SUCCESS_CNT[0] < SUCCESS_CNT[1]:
                                        screen.blit(MOMMY_WIN_PRINT, ((display_width-MOMMY_WIN_PRINT_SHAPE[0])//2+300,MOMMY_WIN_PRINT_SHAPE[1]//2))
                                        screen.blit(ROUND_CLEAR_IMAGE, ((display_width-ROUND_CLEAR_IMAGE_SHAPE[0])//2-200,(display_height-ROUND_CLEAR_IMAGE_SHAPE[1])//2+100))
                                    elif SUCCESS_CNT[0] == SUCCESS_CNT[1]:
                                        screen.blit(DRAW_PRINT, ((display_width-DRAW_PRINT_SHAPE[0])//2+300,DRAW_PRINT_SHAPE[1]//2))
                                        screen.blit(DRAW_IMAGE, ((display_width-DRAW_IMAGE_SHAPE[0])//2-200,(display_height-DRAW_IMAGE_SHAPE[1])//2+100))

                                    if (time.time()-print_time) >= 15:
                                        screen.blit(frame, (0,0))
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
                            screen.blit(ROUND_CLEAR_IMAGE, ((display_width-ROUND_CLEAR_IMAGE_SHAPE[0])//2-200,(display_height-ROUND_CLEAR_IMAGE_SHAPE[1])//2+100))
                            if TEAM_CNT == 0:
                                screen.blit(DADDY_ROUND_CLEAR_PRINT, ((display_width-DADDY_ROUND_CLEAR_PRINT_SHAPE[0])//2+300,DADDY_ROUND_CLEAR_PRINT_SHAPE[1]//11))
                            elif TEAM_CNT == 1:
                                screen.blit(MOMMY_ROUND_CLEAR_PRINT, ((display_width-MOMMY_ROUND_CLEAR_PRINT_SHAPE[0])//2+300,MOMMY_ROUND_CLEAR_PRINT_SHAPE[1]//11))

                else:
                    STAGE.version = {1: STAGE.ROUND_1,
                                     2: STAGE.ROUND_2}.get(STAGE.ROUND)
                    SUCCESS = False
                    PRINT_SUCCESS = False

            else:
                # for check segmentation
                screen.blit(result, (display_width-seg_shape[1],display_height-seg_shape[0]))
                screen.blit(SUCCESS_PRINT, ((display_width-SUCCESS_PRINT_SHAPE[0])//2+300,SUCCESS_PRINT_SHAPE[1]//2))
                screen.blit(SUCCESS_IMAGE, ((display_width-SUCCESS_IMAGE_SHAPE[0])//2-200,(display_height-SUCCESS_IMAGE_SHAPE[1])//2+100))

        elif FAIL:
            pygame.mixer.music.set_volume(1)
            screen.blit(frame, (0,0))
            if not teambattle:
                # for check segmentation
                screen.blit(result, (display_width-seg_shape[1],display_height-seg_shape[0]))
                screen.blit(FAIL_PRINT, ((display_width-FAIL_PRINT_SHAPE[0])*3//4,(display_height-FAIL_PRINT_SHAPE[1])*2//7))
                screen.blit(FAIL_IMAGE, ((display_width-FAIL_IMAGE_SHAPE[0])//2-200,(display_height-FAIL_IMAGE_SHAPE[1])//2+100))
                if (time.time()-print_time) >= 5:
                    FAIL = False
                    PRINT_SUCCESS = False
                    screen.blit(frame, (0,0))
                    go_menu = REGAME("FAIL", frame)
                    if go_menu:
                        pygame.mixer.music.fadeout(1000)
                        MENU_LIST[0] = True
                        MENU_LIST[1] = False
                        MENU_LIST[2] = False
                        MENU_LIST[3] = False
                        break
                    STAGE.version = {1: STAGE.ROUND_1,
                                     2: STAGE.ROUND_2}.get(STAGE.ROUND)

            else:
                if (time.time()-print_time) >= 5:
                    if TEAM_CNT == 0:
                        TEAM_CNT += 1
                        READY = False
                        SUCCESS = False
                        FAIL = False
                        PRINT_SUCCESS = False
                        NO_PERSON = False
                        STAGE.ROUND = 1
                        MUSIC_FLAG = True
                        STAGE.version = {1: STAGE.ROUND_1}.get(STAGE.ROUND)
                    else:
                        if SUCCESS_CNT[0] > SUCCESS_CNT[1]:
                            screen.blit(DADDY_WIN_PRINT, ((display_width-DADDY_WIN_PRINT_SHAPE[0])//2+300,DADDY_WIN_PRINT_SHAPE[1]//2))
                            screen.blit(ROUND_CLEAR_IMAGE, ((display_width-ROUND_CLEAR_IMAGE_SHAPE[0])//2-200,(display_height-ROUND_CLEAR_IMAGE_SHAPE[1])//2+100))
                        elif SUCCESS_CNT[0] < SUCCESS_CNT[1]:
                            screen.blit(MOMMY_WIN_PRINT, ((display_width-MOMMY_WIN_PRINT_SHAPE[0])//2+300,MOMMY_WIN_PRINT_SHAPE[1]//2))
                            screen.blit(ROUND_CLEAR_IMAGE, ((display_width-ROUND_CLEAR_IMAGE_SHAPE[0])//2-200,(display_height-ROUND_CLEAR_IMAGE_SHAPE[1])//2+100))
                        elif SUCCESS_CNT[0] == SUCCESS_CNT[1]:
                            screen.blit(DRAW_PRINT, ((display_width-DRAW_PRINT_SHAPE[0])//2+300,DRAW_PRINT_SHAPE[1]//2))
                            screen.blit(DRAW_IMAGE, ((display_width-DRAW_IMAGE_SHAPE[0])//2-200,(display_height-DRAW_IMAGE_SHAPE[1])//2+100))

                        if (time.time()-print_time) >= 10:
                            screen.blit(frame, (0,0))
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
                    # for check segmentation
                    if TEAM_CNT == 0:
                        screen.blit(result, (display_width-seg_shape[1],display_height-seg_shape[0]))
                        screen.blit(FAIL_IMAGE, ((display_width-FAIL_IMAGE_SHAPE[0])//2-200,(display_height-FAIL_IMAGE_SHAPE[1])//2+100))
                        screen.blit(DADDY_FAIL_PRINT, ((display_width-DADDY_FAIL_PRINT_SHAPE[0])//2+300,DADDY_FAIL_PRINT_SHAPE[1]//4))
                    elif TEAM_CNT == 1:
                        screen.blit(result, (display_width-seg_shape[1],display_height-seg_shape[0]))
                        screen.blit(FAIL_IMAGE, ((display_width-FAIL_IMAGE_SHAPE[0])//2-200,(display_height-FAIL_IMAGE_SHAPE[1])//2+100))
                        screen.blit(MOMMY_FAIL_PRINT, ((display_width-DADDY_FAIL_PRINT_SHAPE[0])//2+300,DADDY_FAIL_PRINT_SHAPE[1]//4))

        pygame.display.flip()
