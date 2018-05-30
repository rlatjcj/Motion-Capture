PERCENTILE_THRESHOLD = 0.01

# for calculating percentile
def percentile(res_num, seg_num, SUCCESS=False, FAIL=False):
    percent = res_num / seg_num

    if percent < PERCENTILE_THRESHOLD:
        print('percentile is {:.2f}! SUCCESS!'.format(percent))
        SUCCESS = True
    else:
        print('percentile is {:.2f}! FAIL!'.format(percent))
        FAIL = True

    return SUCCESS, FAIL

def change(res_num, SUCCESS=False, FAIL=False):
    if res_num == 0:
        SUCCESS = True
    else:
        FAIL = True

    return SUCCESS, FAIL
