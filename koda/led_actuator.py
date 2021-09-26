#!/usr/bin/env python

import rospy
from std_msgs.msg import Bool
import RPi.GPIO as GPIO

# definiranje GPIO za LED
LED_GPIO = 7
# Green 1 - GPIO 2
# Green 2 - GPIO 3
# Yellow 1 - GPIO 4
# Yellow 2 - GPIO 5
# Red 1 - GPIO 6
# Red 2 - GPIO 7

def resetLed():
     # nastavi in resetiraj vse LED
    for ii in range(2,8):
        # nastavi IO kot izhode
        GPIO.setup(ii,GPIO.OUT)
        # postavi izhode na nizek nivo
        GPIO.output(ii,False)

def button_state_callback(msg):
    # koda, ki se izvede, ko subsriber dobi podatek
    # prizgi definirano LED
    GPIO.output(LED_GPIO, msg.data)

if __name__ == '__main__':
    # inicializacija node
    rospy.init_node('led_actuator')

    # nastavited GPIO kot BCM
    GPIO.setmode(GPIO.BCM)
    # ugasni vse LED
    resetLed()
    # nastavi LED GPIO kot izhod
    GPIO.setup(LED_GPIO, GPIO.OUT)
    
    # definicija subsriberja
    # rospy.Subscriber('topic_name', varType, callback)
    rospy.Subscriber('button_state', Bool, button_state_callback)

    # vrtenje zanke
    rospy.spin()

    # pobrisi nastavitve GPIO
    GPIO.cleanup()