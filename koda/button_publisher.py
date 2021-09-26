#!/usr/bin/env python

import rospy
import RPi.GPIO as GPIO
from std_msgs.msg import Bool

# definicija GPIO pina za gumb
BUTTON_GPIO = 11
# gumb 1 - gpio 11
# gumb 2 - gpio 12

if  __name__ == '__main__':
    # inicializacija noda, annonymouse = True, ce je potrebno veckrat poganjat isto kodo
    rospy.init_node('button_state_publisher')

    # definicija publisherja
    # rospy.Publisher("topic_name", varType, queue_size)
    pub = rospy.Publisher('button_state', Bool, queue_size=10)

    # nastavitev GPIO kot BCM
    GPIO.setmode(GPIO.BCM)
    # nastavitev IO za gumb kot input
    GPIO.setup(BUTTON_GPIO, GPIO.IN)

    # nastavitev izvajanja zanke na 10 Hz
    rate = rospy.Rate(10)

    # izvajaj program dokler ni node terminiran
    while not rospy.is_shutdown():
        # preberi GPIO pin/gumb
        gpio_state = GPIO.input(BUTTON_GPIO)
        # definicija msg kot Bool spremenljivke
        msg = Bool()
        # msg ima podatek "data"
        msg.data = gpio_state
        # poslji sporocilo
        pub.publish(msg)
        # rate.sleep() poskrbi za posiljanje z 10 Hz
        rate.sleep()

    # ko se zakljuci izvajanje node, pobrisi nastavitve GPIO pinov
    GPIO.cleanup()






