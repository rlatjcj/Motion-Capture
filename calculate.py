import math
import numpy as np

PERCENTILE_THRESHOLD = 0.01
ANGLE_THRESHOLD = 40 # angle thresholds


# GANE1
def change(res_num, SUCCESS=False, FAIL=False):
    if res_num == 0:
        SUCCESS = True
    else:
        FAIL = True

    return SUCCESS, FAIL



# GAME2
def all_parts_list(parts_list, person_keypoints, img_shape) :
    '''
    person_keypoints : 0 ~ 17, the number of 18
    parts_list : insterest parts listom
    person_keypoints : x, y

    output : parts_list'x angle list
    '''
    result = []
    for i in range(len(parts_list)) :
        three_points = parts_list[i]
        keypoint_list = person_keypoints

        img_y = img_shape[0]

        side_one = keypoint_list[three_points[0]][:2]
        origin = keypoint_list[three_points[1]][:2]
        side_two = keypoint_list[three_points[2]][:2]

        cord_x, cord_y = (side_one[0]-origin[0]), ((img_y-side_one[1])-(img_y-origin[1]))
        cord_x2, cord_y2 = (side_two[0]-origin[0]), ((img_y-side_two[1])-(img_y-origin[1]))

        inner_a_b = (cord_x*cord_x2) + (cord_y*cord_y2)
        abs_a = np.sqrt(cord_x**2+cord_y**2)
        abs_b = np.sqrt(cord_x2**2+cord_y2**2)
        output = (inner_a_b)/(abs_a*abs_b)

        angle = math.degrees(math.acos(output))
        result.append(angle)
    return(result)


def check_angles(abs_distances, thresholds = ANGLE_THRESHOLD) :
    idx = np.where(np.array(abs_distances) > thresholds)
    print(len(idx[0]))

    if len(idx[0]) < 5 :
        SUCCESS = True
        FAIL = False
        return  SUCCESS, FAIL
    else :
        SUCCESS = False
        FAIL = True
        return  SUCCESS, FAIL
