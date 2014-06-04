#!/usr/bin/env python
import roslib; roslib.load_manifest('irobot_mudd')
import rospy
import irobot_mudd
from std_msgs.msg import String
from irobot_mudd.srv import *
from irobot_mudd.msg import *
import time
import math


####
# robot0.py ~ starter file for scripting the Create with ROS
####


####
# D is our global system state
####

class Data: pass    # empty class for a generic data holder
D = Data()  # an object to hold our system's services and state
stream_name = 'text_data'


####
# main and init
####


def main():
    """ the main program that gives our node a name,
       sets up service objects, subscribes to topics (with a callback),
       and then lets interactions happen!
    """
    global D

    # set up services and subscribe to data streams
    init()

    

    # sing!
    #D.song([82,84,80,68,75], # notes
    #       [45,55,45,45,65]) # durations
    
    # move!
    #D.tank(100,100)
    #time.sleep(2.0)
    
    # reminder of Python's for loop:
    #for i in range(2):
    #    print "i is", i

    # finish up...
    #D.tank(0,0)
    #print "Goodbye!"

    #D.led(1,1,50,100)
    #print "Just kidding, Goodbye now!"

    rospy.spin()


    

def init():
    """ returns an object (tank) that allows you
       to set the velocities of the robot's wheels
    """
    global D # to hold system state
    global message

    rospy.Subscriber( 'text_data', String, callback )


    # we need to give our program a ROS node name
    # the name is not important, so we use "lab1_node"
    rospy.init_node('lab1_node', anonymous=True)
    
    # we obtain the tank service
    rospy.wait_for_service('tank') # wait until the motors are available
    D.tank = rospy.ServiceProxy('tank', Tank) # D.tank is our "driver"
    
    # we obtain the song service
    rospy.wait_for_service('song') # wait until our voice is available
    D.song = rospy.ServiceProxy('song', Song) # D.song is our "speaker" 

    # blinky blinky
    rospy.wait_for_service('leds')
    D.leds = rospy.ServiceProxy('leds', Leds)

    # set up a callback for the sensorPacket stream, i.e., "topic"
    


####
# callback ~ called with each published message
####
def callback(data):
    """ This function is called for each published message
    """
    message = data.data
    print "I received the string", message

    if message == 'w' :
        D.tank(50,50)

    if message == 'a' :
        D.tank(0,25) 

    if message == 'd' :
        D.tank(25,0)

    if message == 's' :
        D.tank(-50,-50)

    if message == ' ' :
        D.tank(0,0)

    if message == '1' :
        D.song([82,84,80,68,75], # notes
            [45,55,45,45,65]) # durations

    if message == '2' :
        rospy.Subscriber( 'sensorPacket', SensorPacket, sensor_callback )
        D.pausetime = time.time()
    
    # if the message is the string 'q', we shutdown
    if message == 'q':
        rospy.signal_shutdown("Quit requested.")


def sensor_callback( data ):
    """ sensor_callback is called for each sensorPacket message
    """
    global D
    # let's give our two front IR sensor values more convenient names:
    left = data.cliffFrontLeftSignal
    right = data.cliffFrontRightSignal

    # let's print them out:
    print "L,R front sensors:", left, right
    if time.time() >= D.pausetime:
        # wheeldrop? stop!
        if data.wheeldropCaster == True:
            D.tank(0,0)

        elif data.bumpLeft == True or data.bumpRight == True:
            D.tank(0,0)
            rospy.signal_shutdown("Quit requested.")

        elif data.cliffFrontRightSignal < 250 and data.cliffFrontLeftSignal < 200:
            D.tank(40,40)


        elif data.cliffFrontLeftSignal > 250:
            right_correct
            D.tank(0,25)

        elif data.cliffFrontRightSignal > 200:
            D.tank(25,0)
            
    if message == 'q' :
        rospy.signal_shutdown("Quit requested.")

def right_correct( data ):
    time.sleep(0.5)
    D.tank(-30,-30)
    


####
# It all starts here...
#
# This is the "main" trick: it tells Python what code to run
# when you execute this file as a stand-alone script:
#### 

if __name__ == "__main__":
   main()