#!/usr/bin/env python

import rospy
from std_srvs.srv import SetBool
import RPi.GPIO as GPIO

# definicija GPIO za gumb
BUTTON_GPIO = 11
# definicija globalne spremenljivke
LED_STATE = False

def button_callback(channel):
    # funkcija, ki se izvede ob prekinitvi
    global LED_STATE
    # preberi stanje gumba
    power_on_led = GPIO.input(BUTTON_GPIO)

    # zamenjaj stanje LED
    LED_STATE = not LED_STATE

    # cakaj, dokler ni na voljo zeljen service
    rospy.wait_for_service('set_led_state')
    try:
        # definicija proxya 
        # rospy.ServiceProxy('service_name', varType)
        set_led_state = rospy.ServiceProxy('set_led_state', SetBool)
        # poslji request, dobi response
        resp = set_led_state(LED_STATE)
        # izpis odgovora
        print(resp)
    except rospy.ServiceException as e:
        # v primeru napake jo zapisi v log
        rospy.logwarn(e)

if __name__=='__main__':
    # inicializacija noda
    rospy.init_node('button_monitor')
    # nastavitve GPIO
    GPIO.setmode(GPIO.BCM)
    # nastavi GPIO za gumb kot vhod
    GPIO.setup(BUTTON_GPIO, GPIO.IN)
    # definiranje prekinitve
    # GPIO.add_event_detect(gpio_num, fronta, callback, bouncetime)
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.RISING, callback=button_callback, bouncetime=500)

    # vrtenje zanke
    rospy.spin()

    # pobrisi GPIO nastavitve
    GPIO.cleanup()
