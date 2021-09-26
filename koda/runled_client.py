#!/usr/bin/env python

import rospy
# vkljuci knjiznico actionlib
import actionlib
# vkljucitev ustreznih action tipov
from rpi_msgs.msg import runningLedAction, runningLedGoal, runningLedResult

# definicija statusa action serverja
PENDING = 0
ACTIVE = 1
DONE = 2
WARN = 3
ERROR = 4

# globalna definicija client spremenljivke
client = None

def resetLed():
    # nastavi in resetiraj vse LED
    for ii in range(2,8):
        GPIO.setup(ii,GPIO.OUT)
        GPIO.output(ii,False)

def run_led_client(goalNum):
    # koda, ki poslje zahtevo action serverju
    global client
    # definicija simple action clienta 
    # actionlib.SimpleActionClient('action:name', actionType)
    client = actionlib.SimpleActionClient('run_led', runningLedAction)

    # pocakaj, dokler ni server aktiven
    client.wait_for_server()

    # definiraj goal, ki ga zelis poslati
    goal = runningLedGoal()
    goal.numberRuns = goalNum

    # poslji goal 
    client.send_goal(goal)

    ###################################
    # za testiranje preempta
    # po 3 s poslji nov cilj
    # rospy.sleep(3)
    # goal.numberRuns = 2
    # client.send_goal(goal)
    ###################################
    
    # MOZNOST A - pocakaj, dokler server ne konca (podobno kot service)
    client.wait_for_result()


    """ # MOZNOST B - vmes, ko cakas, naredi kaj drugega    

    ## preberi trenutno stanje serverja
    current_state = client.get_state()

    ## definiraj izvajanje zanke 1 Hz
    r2 = rospy.Rate(1)

    # dokler server ne zakljuci (DONE), delaj kaj drugega
    while current_state < DONE:
        # akcija se poteka, naredi kaj produktivnega
        
        # preveri stanje
        current_state = client.get_state()
        # cikel zanke 1 Hz
        r2.sleep()

    # ce je stanje serverja WARN
    if current_state == WARN:
        rospy.logwarn("[Warn] Warning on the action server side.")

    # ce je stanje serverja ERROR
    if current_state == ERROR:
        rospy.logerr("[Error] Error on the action server side.") """

    
    # vrni rezultat
    return client.get_result() 


if __name__ == '__main__':
    # inicializacija noda
    rospy.init_node('run_led_client')

    try:
        # poslji goal         
        result = run_led_client(goalNum = 10)
        # izpisi rezultat
        print("Result: %i" % result.finalRuns)
    except rospy.ROSInterruptException:
        # v primeru napake
        print("Program interrupted before completion.")
