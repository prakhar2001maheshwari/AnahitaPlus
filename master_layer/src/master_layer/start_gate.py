#!/usr/bin/env python

import rospy

from master_layer.srv import GoToIncremental
from master_layer.srv import GoTo
from master_layer.msg import Waypoint
from master_layer.srv import ChangeOdom
from master_layer.srv import CurrentTask
from master_layer.srv import GoToPose
from master_layer.srv import Hold
from master_layer.srv import TrajectoryComplete
from master_layer.srv import PoseReach
from master_layer.srv import StallVehicle
from master_layer.srv import GetMaxDepth
from master_layer.srv import TargetNormal
from master_layer.srv import ResetIMU

import time
from std_msgs.msg import Time, String

from anahita_utils import *

from geometry_msgs.msg import Pose, Point, Quaternion

from nav_msgs.msg import Odometry
from rospy.numpy_msg import numpy_msg
import tf.transformations as trans

current_p = Pose()

def odometry_callback(msg):
    global current_p
    current_p = msg.pose.pose

if __name__ == '__main__':

    rospy.init_node('start_gate')

    sub_odometry = rospy.Subscriber('/anahita/pose_gt', numpy_msg(Odometry), odometry_callback)
    
    try:
        go_to_incremental = rospy.ServiceProxy('anahita/go_to_incremental', GoToIncremental)
        go_to = rospy.ServiceProxy('anahita/go_to', GoTo)
        current_task = rospy.ServiceProxy('anahita/current_task', CurrentTask)
        change_odom = rospy.ServiceProxy('odom_source', ChangeOdom)
        go_to_pose = rospy.ServiceProxy('anahita/go_to_pose', GoToPose)
        hold_vehicle = rospy.ServiceProxy('anahita/hold_vehicle', Hold)
        trajectory_complete = rospy.ServiceProxy('anahita/trajectory_complete', TrajectoryComplete)
        pose_reach = rospy.ServiceProxy('anahita/pose_reach', PoseReach)
        get_max_depth = rospy.ServiceProxy('anahita/get_max_depth', GetMaxDepth)
        stall_vehicle = rospy.ServiceProxy('/anahita/stall_vehicle', StallVehicle)
        target_normal = rospy.ServiceProxy('anahita/target_normal', TargetNormal)
        reset_imu = rospy.ServiceProxy('/anahita/reset_imu', ResetIMU)
    except:
        print ('failed to connect to servers')

    point = Point()
    pose = Pose()

    # stall_vehicle(status=True)
    # rospy.loginfo('vehicle stalled')

    # reset_imu()
    # rospy.loginfo('imu reset')

    # current_task(current_task="start_gate")
    # rospy.loginfo('vision task changed to start_gate')

    # change_odom(odom="vision")
    # rospy.loginfo('odom source changes to vision')

    # rospy.sleep(1)
    
    # stall_vehicle(status=False)
    # rospy.loginfo('vehicle unstalled')

    # pose = current_p
    # pose.position.y = 0
    # pose.position.z = 0

    # go_to_pose(target_pose=pose)
    # rospy.loginfo('cmd to align to the gate center')

    # pose_reach(time_out=30)
    # rospy.loginfo('aligned to the center')

    depth_to_cover = get_max_depth(task="start_gate")

    stall_vehicle(status=True)
    rospy.loginfo('vehicle stalled')

    change_odom(odom="zvision")
    rospy.loginfo('odom source changd to zvision')

    rospy.sleep(1)

    stall_vehicle(status=False)
    rospy.loginfo('vehicle unstalled')

    # if depth_to_cover.depth - 3 < 2:
    pose = current_p
    pose.position.x = pose.position.x + depth_to_cover.depth - 3
    pose.position.z = 0

    # to add a conditional to choose gotopose only if near else gotoincremental
    go_to_pose(target_pose=pose)
    rospy.loginfo('cmd to go infront of the gate')

    pose_reach(time_out=30)
    rospy.loginfo('in front of the gate')
    # else:
    #     point.x = depth_to_cover.depth - 3
    #     point.y = 0
    #     point.z = 0

    #     go_to_incremental(step=point, interpolator='lipb', max_forward_speed=0.2)
    #     rospy.loginfo('cmd to go infront of the gate')

    #     trajectory_complete(time_out=120)
    #     rospy.loginfo('infront of the gate')

    # yaw_to_move = target_normal(task="start_gate").angle
    # print ("yaw to move: {}".format(yaw_to_move))

    # _, _, euler_yaw = quaternion_to_eulerRPY(current_p.orientation)
    # euler_yaw = euler_yaw - yaw_to_move

    # print ("euler to turn: {}".format(euler_yaw))

    # q = eulerRPY_to_quaternion(0, 0, euler_yaw)
    # print ("qauternion: {}".format(q))
    # pose = current_p
    # pose.orientation.x = q[0]
    # pose.orientation.y = q[1]
    # pose.orientation.z = q[2]
    # pose.orientation.w = q[3]

    # go_to_pose(target_pose=pose)
    # rospy.loginfo('cmd to turn')

    # pose_reach(time_out=30)
    # rospy.loginfo('turned')

    # stall_vehicle(status=True)
    # rospy.loginfo('vehicle stalled')

    # reset_imu()
    # rospy.loginfo('reset imu')

    # change_odom(odom="vision")
    # rospy.loginfo('odom source changed')

    # rospy.sleep(1)

    # pose = current_p
    # pose.position.y = 0
    # pose.position.z = 0

    # go_to_pose(target_pose=pose)
    # rospy.loginfo('cmd to align to the center again')

    # pose_reach(time_out=30)
    # rospy.loginfo('aligned to the center')

    # stall_vehicle(status=True)

    # change_odom(odom="dvl")
    # rospy.loginfo('odom source changed')

    # rospy.sleep(1)

    # depth_to_cover = get_max_depth(task="start_gate")

    # point.x = depth_to_cover.depth*2
    # point.y = 0
    # point.z = 0

    # go_to_incremental(step=point, interpolator='lipb', max_forward_speed=0.5)
    # rospy.loginfo('cmd to cross the gate')

    # trajectory_complete(time_out=120)
    # rospy.loginfo('completed gate task')