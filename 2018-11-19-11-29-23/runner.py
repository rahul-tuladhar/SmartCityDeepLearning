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




# if __name__ == "__main__":

#     sumoBinary = checkBinary('sumo-gui')

#     traci.start([sumoBinary, "-c", "osm.sumocfg"])

#     step = 0
    
#     while step < 100:
#         traci.simulationStep()
      
#         if step % 10 == 0:

#             for e in edges:
#                 lane_ID = e.id
#                 co = traci.edge.getCOEmission(lane_ID)
#                 noise = traci.edge.getNoiseEmission(lane_ID)
#                 num_veh = traci.edge.getLastStepVehicleNumber(lane_ID)
#                 ped = traci.edge.getLastStepPersonIDs(lane_ID)
#                 print("Step: " + str(step) +  "Edge ID: " + e.id + " CO Emission: " + str(co))
#         step += 1

#     traci.close()

