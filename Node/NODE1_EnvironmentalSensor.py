#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import threading
import time
import json

##add##
import RPi.GPIO as GPIO
import dht11
import datetime
# 上層目錄
sys.path.append("../NIT_Module")
import NIT_Node_Module
from terminalColor import bcolors

NodeUUID = "NODE1_EnvironmentalSensor@NODE-550e8400-e29b-41d4-a716-0001"
# NodeUUID ="NODE-" +uuid.uuid1()

Functions = ["CO1", "CO2", "SMOKE","TEMP","DUST","QUAKE"]
NodeFunctions = ['']#'BasicProtection_FS','AdvancedProtection_FS']

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
    nit.M2M_RxRouting(_obj_json_msg)




################ add #################
def QUAKE():
    global quake
    while True:
        quake = GPIO.input(18)
        #print(GPIO.input(12))
        time.sleep(1)
def TEMP():
    global temp,hum
    # read data using pin 4
    instance = dht11.DHT11(pin=4)
    while True:
        result = instance.read()
        if result.is_valid():
            temp = result.temperature
            hum = result.humidity
            #print("Last valid input: " + str(datetime.datetime.now()))
            #print("Temperature: %d C" % result.temperature)
            #print("Humidity: %d %%" % result.humidity)
        time.sleep(1)
#####################################

def loop():
    decide = "g"
    #decide = input("enter 't' to trigger")
    #print(decide)
    initMSGObj = {'TopicName': "NODE1_EnvironmentalSensor@NODE-550e8400-e29b-41d4-a716-0001/QUAKE", 'Control': 'M2M_SET', 'Source': "NODE1_EnvironmentalSensor@NODE-550e8400-e29b-41d4-a716-0001", 'M2M_Value': ["QUAKE",quake]}
    initMSGSTR = json.dumps(initMSGObj)
    nit.DirectMSG("NODE1_EnvironmentalSensor@NODE-550e8400-e29b-41d4-a716-0001/QUAKE", initMSGSTR)
    initMSGObj = {'TopicName': "NODE1_EnvironmentalSensor@NODE-550e8400-e29b-41d4-a716-0001/TEMP", 'Control': 'M2M_SET', 'Source': "NODE1_EnvironmentalSensor@NODE-550e8400-e29b-41d4-a716-0001", 'M2M_Value': ["TEMP",temp]}
    initMSGSTR = json.dumps(initMSGObj)
    nit.DirectMSG("NODE1_EnvironmentalSensor@NODE-550e8400-e29b-41d4-a716-0001/TEMP", initMSGSTR)
    initMSGObj = {'TopicName': "NODE1_EnvironmentalSensor@NODE-550e8400-e29b-41d4-a716-0001/DUST", 'Control': 'M2M_SET', 'Source': "NODE1_EnvironmentalSensor@NODE-550e8400-e29b-41d4-a716-0001", 'M2M_Value': ["DUST",hum]}
    initMSGSTR = json.dumps(initMSGObj)
    nit.DirectMSG("NODE1_EnvironmentalSensor@NODE-550e8400-e29b-41d4-a716-0001/DUST", initMSGSTR)
    print("----------------------sent!!-----------------------")
    time.sleep(1)

if __name__ == "__main__":
    MQTT_Thread = threading.Thread(target=NodeToServerMQTTThread, name="main_thread")
    MQTT_Thread.start()
    ###add###
    global quake
    quake = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN)
    QUAKE_Thread = threading.Thread(target=QUAKE, name="main_thread1")
    QUAKE_Thread.start()
    global temp,hum
    temp = hum = 0
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    temp = hum = 0
    TEMP_Thread = threading.Thread(target=TEMP, name="main_thread2")
    TEMP_Thread.start()
    while True:
        loop()
