#!/usr/bin/env python

import rospy
import RPi.GPIO as GPIO
# vkljuci knjiznico actionlib
import actionlib
# vkljucitev ustreznih action tipov
from rpi_msgs.msg import runningLedFeedback, runningLedResult, runningLedAction

# globalna definicija spremenljivke action serverja
ACserver = None

def resetLed():
    # nastavi in resetiraj vse LED
    for ii in range(2,8):
        GPIO.setup(ii,GPIO.OUT)
        GPIO.output(ii,False)

def goal_callback(goal):

    # definicija spremenljivke - feedback
    feedback1 = runningLedFeedback()
    # definicija spremenljivke - result
    result1 = runningLedResult()

    # Do lots of awesome groundbreaking robot stuff here
    resetLed()

    # izpisi dobljeno stevilo iteracij 
    print("Stevilo iteracij: %i" % goal.numberRuns)
    
    # definicija drekvence izvajanja zanke (6 Hz)
    r = rospy.Rate(6)
    success = True
    doPreemt = False

    # izvanje zahtevano stevilo ponovitev
    for kk in range(1,goal.numberRuns+1):
        # priziganje vsake posamezne LED (GPIO 2 - GPIO 7)
        for ii in range(2,8):
            # pred vsako LED preveri, ce je preemt zahtevan
            if ACserver.is_preempt_requested():
                # preskoci zahtevo
                print('Goal preempted.')
                # definiraj rezultat
                result1.finalRuns = kk
                # v primeru preemt poslji rezultat in tekst
                ACserver.set_preempted(result=result1,text='Goal preemted.')
                success = False 
                doPreemt = True
                # prekini notranjo zanko - priziganje posameznih LED
                break
            ###############################
            # AKCIJA
            # pobrisi vse LED
            resetLed()
            # prizgi i-to LED
            GPIO.output(ii,True)
            # izvanje s 6 Hz
            r.sleep()
            ###############################	
        # ce je bil preemt, prekini zunanjo zanko - ponovitve
        if doPreemt:
            break
        # po izvedbi celotne sekvence LED poslji feedback
        feedback1.currentRun = kk
        ACserver.publish_feedback(feedback1)

    # po izvedbi vseh ponovitev poslji result
    if success:
        # definicija rezultata
        result1.finalRuns = feedback1.currentRun
        # logiranje
        rospy.loginfo('Zakljuceno - Succeeded') 
        # poslji rezultat
        ACserver.set_succeeded(result1)


if __name__ == '__main__':
    # inicializacija node
    rospy.init_node('run_led_server')
    
    # definicija GPIO
    GPIO.setmode(GPIO.BCM)
    # pobrisi LED
    resetLed()

    # defnicija simple action serverja
    # actionlib.SimpleActionServer('action_name', actionType, callback, autostart)
    ACserver = actionlib.SimpleActionServer('run_led', runningLedAction, goal_callback, False)
    # zazeni server
    ACserver.start()
    print('Server pripravljen')

    # vrtenje zanke
    rospy.spin()

    # pobrisi GPIO nastavitve
    GPIO.cleanup()