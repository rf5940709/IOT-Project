#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Nathaniel'

import class_M2MFS_Obj
import class_M2MFS_MQTTManager
import json
import copy
from terminalColor import bcolors
import M2MFunctionServer

# RuleID, InputNode, InputNode, InputIO, OutputNode, OutputNode, OutputIO, TargetValueOverride
# _g_M2MRulesMappingList = [["1", "Node1", "N1", "SW1", "Node2", "N2", "LED3", "DEF"],
#                         ["2", "Node1", "N1", "SW1", "Node2", "N2", "LED4", "0"],
#                         ["3", "Node2", "N2", "SW2", "Node1", "N1", "LED2", "1"]]

_g_M2MRulesMappingList = [{"RuleID": "1", "InputNode": "NODE1_EnvironmentalSensor@NODE-550e8400-e29b-41d4-a716-0001", "InputIO": "QUAKE",
                           "OutputNode": "NODE6_EvacuationIndicator@NODE-550e8400-e29b-41d4-a716-0006", "OutputIO": "EvacuationIndicator", "TargetValueOverride": "Comfort Level"},

                          {"RuleID": "2", "InputNode": "NODE1_EnvironmentalSensor@NODE-550e8400-e29b-41d4-a716-0001", "InputIO": "QUAKE",
                           "OutputNode": "NODE7_DynamicDetector@NODE-550e8400-e29b-41d4-a716-0007", "OutputIO": "DynamicDetector", "TargetValueOverride": "Comfort Level"},

                          {"RuleID": "3", "InputNode": "NODE1_EnvironmentalSensor@NODE-550e8400-e29b-41d4-a716-0001", "InputIO": "CO2",
                           "OutputNode": "NODE8_FireGate@NODE-550e8400-e29b-41d4-a716-0008", "OutputIO": "FireGate", "TargetValueOverride": "Comfort Level"},

                          {"RuleID": "4", "InputNode": "NODE1_EnvironmentalSensor@NODE-550e8400-e29b-41d4-a716-0001", "InputIO": "QUAKE",
                           "OutputNode": "NODE8_FireGate@NODE-550e8400-e29b-41d4-a716-0008", "OutputIO": "FireGate", "TargetValueOverride": "Comfort Level"},

                          {"RuleID": "5", "InputNode": "NODE1_EnvironmentalSensor@NODE-550e8400-e29b-41d4-a716-0001", "InputIO": "STOP",
                           "OutputNode": "NODE2_AirConditioner@NODE-550e8400-e29b-41d4-a716-0002", "OutputIO": "AirConditioner", "TargetValueOverride": "Comfort Level"},

                          {"RuleID": "6", "InputNode": "NODE1_EnvironmentalSensor@NODE-550e8400-e29b-41d4-a716-0001", "InputIO": "STOP",
                           "OutputNode": "NODE3_AirCleaner@NODE-550e8400-e29b-41d4-a716-0003", "OutputIO": "AirCleaner", "TargetValueOverride": "Comfort Level"},

                          {"RuleID": "7", "InputNode": "NODE1_EnvironmentalSensor@NODE-550e8400-e29b-41d4-a716-0001", "InputIO": "STOP",
                           "OutputNode": "NODE4_Blower@NODE-550e8400-e29b-41d4-a716-0004", "OutputIO": "Blower", "TargetValueOverride": "Comfort Level"},

                          {"RuleID": "8", "InputNode": "NODE1_EnvironmentalSensor@NODE-550e8400-e29b-41d4-a716-0001", "InputIO": "STOP",
                           "OutputNode": "NODE5_Sprinklers@NODE-550e8400-e29b-41d4-a716-0005", "OutputIO": "Sprinklers", "TargetValueOverride": "Comfort Level"},
                          ]


class FunctionServerMappingRules():
    def __init__(self):
        self.jsonObj = class_M2MFS_Obj.JSON_REPTOPICLIST()

    def replyM2MTopicToNode(self, topicName, NodeName):
        self.jsonObj.Gateway = NodeName
        IsNodeHaveM2MMappingRules = False
        readyToReplyTopics = []

        for SingleM2MMappingRule in _g_M2MRulesMappingList:

            if (SingleM2MMappingRule["OutputNode"] == NodeName):
                readyToReplyTopics.append(SingleM2MMappingRule)

        if (len(readyToReplyTopics) > 0):
            IsNodeHaveM2MMappingRules = True
            for SingleM2MMappingRule in readyToReplyTopics:
                #### ASSIGN TO M2M FS ####
                self.SubscribeTopics = class_M2MFS_Obj.SubscribeTopicsObj()
                self.SubscribeTopics.TopicName = SingleM2MMappingRule["InputNode"] + \
                                                 "/" + SingleM2MMappingRule["InputIO"]  # FS1
                self.SubscribeTopics.Node = SingleM2MMappingRule["OutputNode"]  # M2M
                self.SubscribeTopics.Target = SingleM2MMappingRule["OutputIO"]
                self.SubscribeTopics.TargetValueOverride = SingleM2MMappingRule["TargetValueOverride"]

                self.jsonObj.SubscribeTopics.append(self.SubscribeTopics)

        else:
            IsNodeHaveM2MMappingRules = False

        jsonstring = self.jsonObj.to_JSON()

        print(bcolors.OKBLUE + "[Rules] REPTOPICLIST Send to topic:%s" % (topicName) + bcolors.ENDC)

        pm = class_M2MFS_MQTTManager.PublisherManager()
        pm.MQTT_PublishMessage(topicName, jsonstring)

    def replyM2MRulesAll(self, topicName):
        self.jsonObj = class_M2MFS_Obj.JSON_M2MRULE()

        for SingleM2MMappingRule in _g_M2MRulesMappingList:
            self.Rule = class_M2MFS_Obj.RuleObj()
            self.Rule.RuleID = SingleM2MMappingRule["RuleID"]
            self.Rule.InputNode = SingleM2MMappingRule["InputNode"]
            self.Rule.InputIO = SingleM2MMappingRule["InputIO"]
            self.Rule.OutputNode = SingleM2MMappingRule["OutputNode"]
            self.Rule.OutputIO = SingleM2MMappingRule["OutputIO"]
            self.Rule.TargetValueOverride = SingleM2MMappingRule["TargetValueOverride"]
            self.jsonObj.Rules.append(self.Rule)

        jsonstring = self.jsonObj.to_JSON()

        print(bcolors.OKBLUE + "[Rules] REPRULE Send to topic:%s" % (topicName) + bcolors.ENDC)

        pm = class_M2MFS_MQTTManager.PublisherManager()
        pm.MQTT_PublishMessage(topicName, jsonstring)

    def AddM2MRule(self, RuleObjs):
        print(bcolors.OKBLUE + "[Rules] ADDRULE start %s" % (RuleObjs) + bcolors.ENDC)

        NotifyNodes = []

        for SingleM2MMappingRule in RuleObjs:
            NotifyNodes.append(SingleM2MMappingRule["OutputNode"])
            _g_M2MRulesMappingList.append(SingleM2MMappingRule)

        self.ModifyRePublishToNode(NotifyNodes)
        print(bcolors.OKGREEN + "[Rules] ADDRULE end!" + bcolors.ENDC)

    def UpdateM2MRule(self, RuleObjs):
        print(bcolors.OKBLUE + "[Rules] UPDATERULE start %s" % (RuleObjs) + bcolors.ENDC)

        NotifyNodes = []

        for SingleM2MMappingRule in RuleObjs:
            for updateRule in _g_M2MRulesMappingList:
                if (updateRule["RuleID"] == SingleM2MMappingRule["RuleID"]):
                    # 蠻怪的，陣列內dict變動，list內卻沒有跟著變??，只好砍掉重新加入
                    NotifyNodes.append(updateRule["OutputNode"])
                    _g_M2MRulesMappingList.remove(updateRule)
                    _g_M2MRulesMappingList.append(SingleM2MMappingRule.copy())
                    NotifyNodes.append(SingleM2MMappingRule["OutputNode"])

        self.ModifyRePublishToNode(NotifyNodes)
        print(bcolors.OKBLUE + "[Rules] UPDATERULE end!" + bcolors.ENDC)

    def DelM2MRule(self, RuleObjs):
        print(bcolors.OKBLUE + "[Rules] DELRULE start %s" % (RuleObjs) + bcolors.ENDC)

        NotifyNodes = []

        for SingleM2MMappingRule in RuleObjs:
            for delRule in _g_M2MRulesMappingList:
                if (delRule["RuleID"] == SingleM2MMappingRule["RuleID"]):
                    NotifyNodes.append(delRule["OutputNode"])
                    _g_M2MRulesMappingList.remove(delRule)

        self.ModifyRePublishToNode(NotifyNodes)
        print(bcolors.OKGREEN + "[Rules] DELRULE end!" + bcolors.ENDC)

    def ModifyRePublishToNode(self, NotifyNodes):
        print(bcolors.OKBLUE + "[Rules] Republish New M2M Rules for relate Node." + bcolors.ENDC)
        NotifyNodes = list(set(NotifyNodes))
        for Nodes in NotifyNodes:
            self.replyM2MRulesAll(Nodes)
