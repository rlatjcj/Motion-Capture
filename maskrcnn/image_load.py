from pygame_web_sc import *


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

YES_norm = pygame.image.load("./image/b_06_y.png")
YES_high = pygame.image.load("./image/bb_06_yes.png")
NO_norm = pygame.image.load("./image/b_06_n.png")
NO_high = pygame.image.load("./image/bb_06_no.png")

QUIT_IMAGE = pygame.image.load("./image/p_13_2_end.png")
QUIT_IMAGE_SHAPE = pygame.surfarray.array2d(QUIT_IMAGE).shape
QUIT_MENTION = pygame.image.load("./image/p_13_1_end.png")
QUIT_MENTION_SHAPE = pygame.surfarray.array2d(QUIT_MENTION).shape

FIRSTTIME_norm = pygame.image.load("./image/b_06_firsttime.png")
FIRSTTIME_high = pygame.image.load("./image/bb_06_firsttime.png")
RESTART_norm = pygame.image.load("./image/b_06_restart.png")
RESTART_high = pygame.image.load("./image/bb_06_restart.png")

BUTTON_SHAPE = pygame.surfarray.array2d(START_norm).shape

# load images for GAME1
FIT_POSE = pygame.image.load("./image/p_00_position.png")
FIT_POSE = pygame.transform.scale(FIT_POSE, (display_width//2, display_height*4//5))
FIT_SHAPE = pygame.surfarray.array2d(FIT_POSE).shape
READY_PRINT = pygame.image.load("./image/b_05_2_ready.png")
READY_PRINT_SHAPE = pygame.surfarray.array2d(READY_PRINT).shape
LOADING = pygame.image.load("./image/b_05_3_loading.png")
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

# load images about stages
STAGE_1 = pygame.image.load("./image/pb_07_1_1.png")
STAGE_2 = pygame.image.load("./image/pb_07_1_2.png")
STAGE_3 = pygame.image.load("./image/pb_07_1_3.png")
STAGE_DICT = {1: STAGE_1, 2: STAGE_2, 3: STAGE_3}
STAGE_SHAPE = pygame.surfarray.array2d(STAGE_1).shape
