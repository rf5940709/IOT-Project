#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import threading
import time
import json
import RPi.GPIO as GPIO

# 上層目錄
sys.path.append("../NIT_Module")
import NIT_Node_Module
from terminalColor import bcolors

NodeUUID = "NODE3_AirCleaner@NODE-550e8400-e29b-41d4-a716-0003"
# NodeUUID ="NODE-" +uuid.uuid1()

Functions = ["DUST"]
NodeFunctions = ['BasicProtection_FS']#,'AdvancedProtection_FS']#, 'IPCams']

print("::::::::::::::::::::::::::::::::::::::::::\n")
print("::::::::::::::::::::::::::::::::::::::::::\n")
print("'##::: ##::'#######::'########::'########:")
print(" ###:: ##:'##.... ##: ##.... ##: ##.....::")
print(" ####: ##: ##:::: ##: ##:::: ##: ##:::::::")
print(" ## ## ##: ##:::: ##: ##:::: ##: ######:::")
print(" ##. ####: ##:::: ##: ##:::: ##: ##...::::")
print(" ##:. ###: ##:::: ##: ##:::: ##: ##:::::::")
print(" ##::. ##:. #######:: ########:: ########:")
print("..::::..:::.......:::........:::........::")
print("::::::::::::::::::::::::::::::::::::::::::\n")

nit = NIT_Node_Module.NIT_Node(NodeUUID, Functions, NodeFunctions)


# Connect to MQTT Server for communication
def NodeToServerMQTTThread():
    # print("thread name：　" + threading.current_thread().getName())

    # callback
    nit.CallBackRxRouting = RxRouting
    print(bcolors.HEADER + '===============================================\n' + bcolors.ENDC)
    print(bcolors.HEADER + '---------------Node(%s)--->>>Server in MQTT-\n' % NodeUUID + bcolors.ENDC)
    print(bcolors.HEADER + '>>>Start connect Server %s<<<' % (
        time.asctime(time.localtime(time.time()))) + bcolors.ENDC)
    print(bcolors.HEADER + '===============================================\n' + bcolors.ENDC)
    print(bcolors.HEADER + 'Register to IoT Server successful! \n' + bcolors.ENDC)

    try:

        nit.RegisterNoode();

    except (RuntimeError, TypeError, NameError) as e:
        print(bcolors.FAIL + "[INFO]Register error." + str(e) + bcolors.ENDC)
        raise
        sys.exit(1)


########### Keyboard interactive ##############
def RxRouting(self, _obj_json_msg):
    result = nit.M2M_RxRouting(_obj_json_msg)
    if(result != None):
        lop(result)

def lop(result):
    print(result)
    if(int(result) > 30):
        GPIO.output(16, GPIO.HIGH)
    elif(int(result) <=30):
        GPIO.output(16, GPIO.LOW)
"""    global tag
    #print(tag)
    if(result == "os-off"):
        print(result)
        tag = 7  #這邊關閉冷氣
    elif(result == "on" and tag<0):
        print(result)
    elif(result == "off" and tag<0):
        print(result)
    tag-=1"""

if __name__ == "__main__":
    MQTT_Thread = threading.Thread(target=NodeToServerMQTTThread, name="main_thread")
    MQTT_Thread.start()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(16, GPIO.OUT)
