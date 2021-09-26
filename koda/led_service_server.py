#!/usr/bin/env python

import rospy
from std_srvs.srv import SetBool
import RPi.GPIO as GPIO

# definiranje GPIO za LED
LED_GPIO = 2

def resetLed():
    # nastavi in resetiraj vse LED
    for ii in range(2,8):
        GPIO.setup(ii,GPIO.OUT)
        GPIO.output(ii,False)

def set_led_status_callback(req): 
    # koda, ki se izvede, ko proxy poslje zahtevo
    # postavi LED na req.data
    GPIO.output(LED_GPIO, req.data)
    # odgovor serverja
    return {'success': True, 'message':'Successfully changed LED state.'}

if __name__ == '__main__':
    # inicializacija noda
    rospy.init_node('led_actuator')

    # nastavitve GPIO
    GPIO.setmode(GPIO.BCM)
    resetLed()
    GPIO.setup(LED_GPIO, GPIO.OUT)   

    # definicija servica
    # rospy.Service('service_name',varType,callback)
    rospy.Service('set_led_state',SetBool,set_led_status_callback)
    # logiranje
    rospy.loginfo("Service server started. Ready to get request.")

    # vrtenje zanke
    rospy.spin()

    # pobrisi GPIO nastavitve
    GPIO.cleanup()
