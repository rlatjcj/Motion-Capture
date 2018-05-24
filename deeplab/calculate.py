
PERCENTILE_THRESHOLD = 0.01

# for calculating percentile
def percentile(res_num, seg_num, success=False, fail=False):
    percent = res_num / seg_num

    if percent < PERCENTILE_THRESHOLD:
        print('percentile is {:.2f}! SUCCESS!'.format(percent))
        success = True
    else:
        print('percentile is {:.2f}! FAIL!'.format(percent))
        fail = True

    return success, fail

def change(res_num, success=False, fail=False):
    if res_num == 0:
        success = True
    else:
        fail = True

    return success, fail
