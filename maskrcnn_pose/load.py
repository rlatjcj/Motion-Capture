import pygame
from settings import *

################################################################################
# SOUND LOAD
################################################################################

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



################################################################################
# IMAGE LOAD
################################################################################

# INTRO
START_norm = pygame.image.load("./image/b_START.png")
START_high = pygame.image.load("./image/bb_START.png")
SETTING_norm = pygame.image.load("./image/b_SETTING.png")
SETTING_high = pygame.image.load("./image/bb_SETTING.png")
QUIT_norm = pygame.image.load("./image/b_EXIT.png")
QUIT_high = pygame.image.load("./image/bb_EXIT.png")

# SETTING
PERSON_PRINT = pygame.image.load("./image/p_PERSON.png")
PERSON_PRINT_SHAPE = pygame.surfarray.array2d(PERSON_PRINT).shape
UP_norm = pygame.image.load("./image/b_UP.png")
UP_high = pygame.image.load("./image/bb_UP.png")
DOWN_norm = pygame.image.load("./image/b_DOWN.png")
DOWN_high = pygame.image.load("./image/bb_DOWN.png")
UPDOWN_SHAPE = pygame.surfarray.array2d(UP_norm).shape
TEAMBATTLE_PRINT = pygame.image.load("./image/p_TEAMBATTLE.png")
TEAMBATTLE_PRINT_SHAPE = pygame.surfarray.array2d(TEAMBATTLE_PRINT).shape
ON = pygame.image.load("./image/b_ON.png")
OFF = pygame.image.load("./image/b_OFF.png")
ONOFF_SHAPE = pygame.surfarray.array2d(ON).shape
GOBACK_norm = pygame.image.load("./image/b_BACK.png")
GOBACK_high = pygame.image.load("./image/bb_BACK.png")

# CHOOSE_GAME
GAME1_norm = pygame.image.load("./image/b_GAME1.png")
GAME1_high = pygame.image.load("./image/bb_GAME1.png")
GAME2_norm = pygame.image.load("./image/b_GAME2.png")
GAME2_high = pygame.image.load("./image/bb_GAME2.png")

# PAUSE
PAUSE_PRINT = pygame.image.load("./image/p_PAUSE.png")
PAUSE_PRINT_SHAPE = pygame.surfarray.array2d(PAUSE_PRINT).shape
PAUSE_PRINT = pygame.transform.scale(PAUSE_PRINT, (PAUSE_PRINT_SHAPE[0]*2, PAUSE_PRINT_SHAPE[1]*2))
PAUSE_PRINT_SHAPE = pygame.surfarray.array2d(PAUSE_PRINT).shape
CONTINUE_norm = pygame.image.load("./image/b_CONTINUE.png")
CONTINUE_high = pygame.image.load("./image/bb_CONTINUE.png")

CHALLENGE_PRINT = pygame.image.load("./image/p_CHALLENGE.png")
CHALLENGE_PRINT_SHAPE = pygame.surfarray.array2d(CHALLENGE_PRINT).shape
CHALLENGE_IMAGE = pygame.image.load("./image/img_CHALLENGE.png")
CHALLENGE_IMAGE_SHAPE = pygame.surfarray.array2d(CHALLENGE_IMAGE).shape

YES_norm = pygame.image.load("./image/b_YES.png")
YES_high = pygame.image.load("./image/bb_YES.png")
NO_norm = pygame.image.load("./image/b_NO.png")
NO_high = pygame.image.load("./image/bb_NO.png")

QUIT_IMAGE = pygame.image.load("./image/img_END.png")
QUIT_IMAGE_SHAPE = pygame.surfarray.array2d(QUIT_IMAGE).shape
QUIT_MENTION = pygame.image.load("./image/p_END.png")
QUIT_MENTION_SHAPE = pygame.surfarray.array2d(QUIT_MENTION).shape

FIRSTTIME_norm = pygame.image.load("./image/b_FIRSTTIME.png")
FIRSTTIME_high = pygame.image.load("./image/bb_FIRSTTIME.png")
RESTART_norm = pygame.image.load("./image/b_RESTART.png")
RESTART_high = pygame.image.load("./image/bb_RESTART.png")
RESTART_IMAGE = pygame.image.load("./image/img_RESTART.png")
RESTART_IMAGE_SHAPE = pygame.surfarray.array2d(RESTART_IMAGE).shape

BUTTON_SHAPE = pygame.surfarray.array2d(START_norm).shape

# load images for GAME1
FIT_POSE = pygame.image.load("./image/img_POSITION.png")
FIT_POSE = pygame.transform.scale(FIT_POSE, (display_width//2, display_height*4//5))
FIT_SHAPE = pygame.surfarray.array2d(FIT_POSE).shape
READY_PRINT = pygame.image.load("./image/p_READY.png")
READY_PRINT_SHAPE = pygame.surfarray.array2d(READY_PRINT).shape
READY_IMAGE = pygame.image.load("./image/img_READY.png")
READY_IMAGE_SHAPE = pygame.surfarray.array2d(READY_IMAGE).shape
LOADING = pygame.image.load("./image/p_LOADING.png")
LOADING_SHAPE = pygame.surfarray.array2d(LOADING).shape
LOADING_IMAGE = pygame.image.load("./image/img_LOADING.png")
LOADING_IMAGE_SHAPE = pygame.surfarray.array2d(LOADING_IMAGE).shape
FIT_PRINT = pygame.image.load("./image/p_POSITION.png")
FIT_PRINT_SHAPE = pygame.surfarray.array2d(FIT_PRINT).shape
NOPERSON_PRINT = pygame.image.load("./image/p_NOPERSON.png")
NOPERSON_PRINT_SHAPE = pygame.surfarray.array2d(NOPERSON_PRINT).shape

SUCCESS_PRINT = pygame.image.load("./image/p_SUCCESS.png")
SUCCESS_PRINT_SHAPE = pygame.surfarray.array2d(SUCCESS_PRINT).shape
FAIL_PRINT = pygame.image.load("./image/p_FAIL.png")
FAIL_PRINT_SHAPE = pygame.surfarray.array2d(FAIL_PRINT).shape
SUCCESS_IMAGE = pygame.image.load("./image/img_SUCCESS.png")
SUCCESS_IMAGE_SHAPE = pygame.surfarray.array2d(SUCCESS_IMAGE).shape
FAIL_IMAGE = pygame.image.load("./image/img_FAIL.png")
FAIL_IMAGE_SHAPE = pygame.surfarray.array2d(FAIL_IMAGE).shape
ROUND_CLEAR_PRINT = pygame.image.load("./image/p_CLEAR.png")
ROUND_CLEAR_PRINT_SHAPE = pygame.surfarray.array2d(ROUND_CLEAR_PRINT).shape

# load images about stages
STAGE_1 = pygame.image.load("./image/img_GAME1_ROUND1.png")
STAGE_2 = pygame.image.load("./image/img_GAME1_ROUND2.png")
STAGE_3 = pygame.image.load("./image/img_GAME1_ROUND3.png")
STAGE_DICT = {1: STAGE_1, 2: STAGE_2, 3: STAGE_3}
STAGE_SHAPE = pygame.surfarray.array2d(STAGE_1).shape
