from __future__ import absolute_import
from __future__ import print_function

import os, sys
import optparse
import random

# Declares necessary path for SUMO_HOME variable
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
import numpy as np
import pandas as pd

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
# def getEdgeData():
    

if __name__ == "__main__":

    sumoBinary = checkBinary('sumo')
    sumo_cmd = [sumoBinary, "-c", "osm.sumocfg"]
    traci.start(sumo_cmd)

    step = 0
    print("Starting Simulation...")
    while step < 1000:
        traci.simulationStep()
        step_data = []
        if step % 10 == 0:
            print("Step: %d" % step)
            edge_data = {'edge id':['street_name', 'co', 'co2', 'noise', 'num_veh','ped','hc_emission','nox_emission']}
            # Create the data per edge
            for e in edges:
                edge_id = e.getID()
                co = traci.edge.getCOEmission(edge_id)
                co2 = traci.edge.getCO2Emission(edge_id)
                noise = traci.edge.getNoiseEmission(edge_id)
                num_veh = traci.edge.getLastStepVehicleNumber(edge_id)
                ped = traci.edge.getLastStepPersonIDs(edge_id) 
                hc_emission = traci.edge.getHCEmission(edge_id)
                nox_emission = traci.edge.getNOxEmission(edge_id)
                street_name = traci.edge.getStreetName(edge_id)
                data = [street_name,co,co2,noise,num_veh,ped,hc_emission,nox_emission]
                edge_data[edge_id] = data
            edge_data = pd.DataFrame.from_dict(edge_data, orient='index')
            print (edge_data)

            edge_data= getEdgeData()
            state_data = getStateData()
            tl_data = {'t_id': ['phase', 'state', 'switch']}
            for t in tl:
                t_id = t.getID()
                phase = str(traci.trafficlight.getPhase(t_id))
                # definition = str(traci.trafficlight.getCompleteRedYellowGreenDefinition(t_id))
                state = str(traci.trafficlight.getRedYellowGreenState(t_id))
                switch = str(traci.trafficlight.getNextSwitch(t_id))
                data = [phase, state, switch]
                tl_data[t_id] = data
            tl_data = pd.DataFrame.from_dict(tl_data, orient='index')
            print(tl_data)


            # traci.edge.subscribe(vehID, (tc.VAR_ROAD_ID, tc.VAR_LANEPOSITION))
            # print(traci.vehicle.getSubscriptionResults(vehID))
           # # print(str(t_id)+" has switch "+str(switch))
           #  print(str(step))
           #  print(str(t_id)+" has state "+str(state))
           #  print(str(t_id)+" has phase "+str(phase))
            
        step += 1

    traci.close()

