import math
import numpy as np

PERCENTILE_THRESHOLD = 0.01
ANGLE_THRESHOLD = 10 # angle thresholds


# GANE1
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



# GAME2
def all_parts_list(parts_list, person_keypoints) :
    '''
    person_keypoints : 0 ~ 17, the number of 18
    parts_list : insterest parts list
    output : parts_list'x angle list
    '''
    result = []
    for i in range(len(parts_list)) :
        three_points = parts_list[i]
        keypoint_list = person_keypoints

        side_one = keypoint_list[three_points[0]][:2]
        origin = keypoint_list[three_points[1]][:2]
        side_two = keypoint_list[three_points[2]][:2]

        cord_x, cord_y = (side_one[1]-origin[1]), (side_one[0]-origin[0])
        cord_x2, cord_y2 = (side_two[1]-origin[1]), (side_two[0]-origin[0])

        # math.atan2(y,x)
        a = math.degrees(math.atan2(cord_y,cord_x))
        b = math.degrees(math.atan2(cord_y2,cord_x2))

        angle = np.abs(a) + np.abs(b)
        result.append(angle)
    return(result)



def compare_keypoints(distances, thresholds = ANGLE_THRESHOLD) :
    temp = np.array(distances)
    idx = np.where(temp > thresholds)

    if len(temp) < 5 :
        SUCCESS = False
        FAIL = True
        return  SUCCESS, FAIL
    else :
        SUCCESS = True
        FAIL = False
        return  SUCCESS, FAIL
