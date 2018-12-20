from __future__ import absolute_import
from __future__ import print_function

import os, sys
import optparse
import random

# Sets up the right 
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  
import traci  
import traci.constants as tc
import subprocess
import sumolib

net = sumolib.net.readNet('osm.net.xml')
edges = net.getEdges()
nodes = net.getNodes()
tl = net.getTrafficLights()


### Generating nodes_map ###
"""
f = open("nodes_map.txt","w")
for node in nodes:
    f.write(str(node.getID())+"||"+str(node.getType())+"||"+str(node.getCoord())+"||")
    incoming = node.getIncoming()
    outgoing = node.getOutgoing()
    for i in incoming:
        f.write(str(i.getID())+" ")
    f.write("||")
    for i in outgoing:
        f.write(str(i.getID())+" ")
    f.write('\n')
f.close()
"""

### Generating traffic_light ###
"""
f = open("traffic_lights.txt","w")
for t in tl:
    f.write(str(t.getID())+"||")
    for edge in t.getEdges():
        f.write(str(edge.getID())+" ")
    f.write("\n")
f.close()
"""

### Generating edges_map ###
"""
f = open("edges_map.txt","w")
for e in edges:
    nextNodeID = e.getToNode().getID()
    prevNodeID = e.getFromNode().getID()
    f.write(e.getID()+'|')
    f.write(str(net.getNode(prevNodeID).getCoord())+'|')
    f.write(str(net.getNode(nextNodeID).getCoord())+'\n')
f.close()
"""

if __name__ == "__main__":

    sumoBinary = checkBinary('sumo')

    traci.start([sumoBinary, "-c", "osm.sumocfg"])

    step = 0
    
    while step < 1000:
        traci.simulationStep()
      
        if step % 10 == 0:
            #for e in edges:
                # edge_id = e.getID()
                # co = traci.edge.getCOEmission(edge_id)
                # co2 = traci.edge.getCO2Emission(edge_id)
                # noise = traci.edge.getNoiseEmission(edge_id)
                # num_veh = traci.edge.getLastStepVehicleNumber(edge_id)
                # ped = traci.edge.getLastStepPersonIDs(edge_id) 
                               
                # filename = str(edge_id)+".txt"
                # f = open(filename,"a")
                # f.write(str(step)+"|")
                # f.write(str(co)+"|")
                # f.write(str(co2)+"|")
                # f.write(str(noise)+"|")
                # f.write(str(num_veh)+"|")
                # f.write(str(ped)+"\n")
                # f.close()
                # print(str(step)+": "+str(edge_id)+" is done.")
        
            t_id = tl[0].getID()
            phase = traci.trafficlight.getPhase(t_id)
            definition = traci.trafficlight.getCompleteRedYellowGreenDefinition(t_id)
            state = traci.trafficlight.getRedYellowGreenState(t_id)
            switch = traci.trafficlight.getNextSwitch(t_id)
           # print(str(t_id)+" has switch "+str(switch))
            print(str(step))
            print(str(t_id)+" has state "+str(state))
            print(str(t_id)+" has phase "+str(phase))
            
        step += 1

    traci.close()

