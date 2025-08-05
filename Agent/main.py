
from Agent import Agent
from AgentCatalog import AgentCatalog
import tensorflow as tf
from ObjectiveTypes import ObjectiveTypes
import sys
import os
#from tensorflow.keras import layers, models

#Main program for launching agents and test-cases.
def test_0():
    agent_1=Agent("localhost", 9999, "", "", "", "", "", "")

def test_01():
    agentCatalog=AgentCatalog("localhost", 1100)
    agent_1=Agent("localhost", 1000, "localhost", 1100, "", "", "", "", "", "")

def test_02():
    ip="localhost"
    catalogPort=1100
    agentPort=1000
    AgentCatalog(ip, catalogPort)
    for i in range(3):
        Agent(ip, agentPort, ip, catalogPort, "", "", "", "", "", "")
        agentPort+=1

def test_03():
    AgentCatalog("localhost", 1100)
    Agent("localhost", 1000, "localhost", 1100, ObjectiveTypes.IMPROVED_ACCURACY, "", "", "", "", 2, 3)

def test_04():
    AgentCatalog("localhost", 1100)
    #Agent("localhost", 1007, "localhost", 1100, ObjectiveTypes.IMPROVED_ACCURACY, "", "", "", "", 3, 4,4)
    Agent("localhost", 1005, "localhost", 1100, ObjectiveTypes.PROFIT, "", "", "", "", 2, 4, 1)
    #Agent("localhost", 1006, "localhost", 1100, ObjectiveTypes.IMPROVED_ACCURACY, "", "", "", "", 6, 4,7)
    Agent("localhost", 1004, "localhost", 1100, ObjectiveTypes.IMPROVED_ACCURACY, "", "", "", "", 2, 2,3)
    Agent("localhost", 1000, "localhost", 1100, ObjectiveTypes.IMPROVED_ACCURACY, "", "", "", "", 3, 8,1)
    Agent("localhost", 1001, "localhost", 1100, ObjectiveTypes.PROFIT, "", "", "", "", 2, 4, 7)
    Agent("localhost", 1002, "localhost", 1100, ObjectiveTypes.IMPROVED_ACCURACY, "", "", "", "", 2, 6,2)
    Agent("localhost", 1003, "localhost", 1100, ObjectiveTypes.IMPROVED_ACCURACY, "", "", "", "", 2, 5,6)
    #Agent("localhost", 1009, "localhost", 1100, ObjectiveTypes.PROFIT, "", "", "", "", 3, 2, 9)
    

def test_05():
    ip="localhost"
    catalogPort=1100
    agentPort=1000
    AgentCatalog(ip, catalogPort)
    for i in range(3):
        Agent(ip, agentPort, ip, catalogPort, ObjectiveTypes.IMPROVED_ACCURACY, "", "", "", "", 2, 3)
        agentPort+=1
  
def main():
    test_04()
    
if __name__=="__main__":
    main()