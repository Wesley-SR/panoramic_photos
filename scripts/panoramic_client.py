#!/usr/bin/env python

from __future__ import print_function

import math
import rospy
from pantilt_control_ros_node_test.srv import PantiltControl
from sony_camera_ptp.srv import SonyCameraManager


def move_pantilt(axis, new_angle):
    rospy.wait_for_service('pantilt_control')

    try:
        pt_send_command = rospy.ServiceProxy('pantilt_control', PantiltControl)
        response = pt_send_command('panoramic', axis, new_angle)

        return response.response_sucess

    except rospy.ServiceException as e:
        print("Service call failed: %e" % e)


def sony_take_picture(enable_liveview, enable_take_picture, key_property,
                      value_property, file_name, path_name):
    rospy.wait_for_service('sony_camera_manager')

    try:
        sony_send_command = rospy.ServiceProxy(
            'sony_camera_manager', SonyCameraManager)
        response = sony_send_command(
            enable_liveview, enable_take_picture, key_property, value_property,
            file_name, path_name)

        return response.msg_feedback

    except rospy.ServiceException as e:
        print("Service call failed {0}".format(e))


def fluke_take_picture():
    print("fluke_take_picture\n")
    msg_feedback = True
    return msg_feedback


def panoramic_client():

    pan_tilt_limit = 360
    # H: 34 V: 25.5 - Sobreposicao=30%
    tilt = [0, 17.85, 35.7, 53.55, 71.4, 90]
    # pan_fotosH = [16, 16, 15, 12, 9, 1]
    pan_steps = [22.5, 22.5, 24, 30, 40, 360]
    returning = False
    name_photos_count = 0

    for idx, tilt_angle in enumerate(tilt):

        if tilt_angle >= pan_tilt_limit:
            tilt_angle = pan_tilt_limit - 1

        pantilt_feedback = move_pantilt('tilt', tilt_angle)
        if pantilt_feedback:

            current_step = pan_steps[idx]
            steps_count = math.ceil(360 / current_step)
            pan_photos_count = 0

            while pan_photos_count < steps_count:
                if returning:
                    current_angle = 360 - pan_photos_count * current_step

                else:
                    current_angle = pan_photos_count * current_step

                if current_angle >= pan_tilt_limit:
                    current_angle = pan_tilt_limit - 1

                pantilt_feedback = move_pantilt('pan', current_angle)

                if pantilt_feedback:
                    sony_feedback = sony_take_picture(
                        , False, True, "", "", str(name_photos_count), "")
 
                    fluke_feedback = fluke_take_picture()

                    if sony_feedback == "Values are setted" and
                                        fluke_feedback == True:
                        pan_photos_count = pan_photos_count + 1
                        name_photos_count = name_photos_count + 1

        returning = not returning  # Reverse direction of rotation


if __name__ == "__main__":
    
    panoramic.panoramic_client()
