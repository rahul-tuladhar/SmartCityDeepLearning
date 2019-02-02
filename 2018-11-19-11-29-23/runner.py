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

def get_edge_data(edge):
    # numerical data per edge
    edge_id = edge.getID()
    street_name = traci.edge.getStreetName(edge_id)
    co = traci.edge.getCOEmission(edge_id)
    co2 = traci.edge.getCO2Emission(edge_id)
    noise = traci.edge.getNoiseEmission(edge_id)
    num_veh = traci.edge.getLastStepVehicleNumber(edge_id)
    ped = traci.edge.getLastStepPersonIDs(edge_id) 
    hc_emission = traci.edge.getHCEmission(edge_id)
    nox_emission = traci.edge.getNOxEmission(edge_id)
    data = [street_name, co, co2, noise, num_veh, ped, hc_emission, nox_emission]
    return data

def get_tl_data(tl):
    # string format is necessary to view in stdout
    t_id = tl.getID()
    phase = str(traci.trafficlight.getPhase(t_id))
    state = str(traci.trafficlight.getRedYellowGreenState(t_id))
    switch = str(traci.trafficlight.getNextSwitch(t_id))
    data = [phase, state, switch]
    return data    

def write_data_to_file(path, data_id, df, data_type, step):
    #   path: where to save the files
    #   data_filename: name of kind of data; edge, tl, etc
    #   df: dataframe 
    #   data_type: type_data
    #   step: time interval in ticks

    # construct file
    file_name = path + '_' + str(data_type) + '_' + str(data_id) + '.csv'
    with open(file_name, 'a') as f:
        df['step'] = step
        print(file_name)
        print(data_id)
        print(df)    
        df.to_csv(file_name, sep='\t')
    # print("Wrote data to file!")
    return 
        # f.write()
if __name__ == "__main__":

    sumoBinary = checkBinary('sumo')
    sumo_cmd = [sumoBinary, "-c", "osm.sumocfg"]
    traci.start(sumo_cmd)

    step = 0

    # path parameters
    datafile_path = os.path.dirname(os.path.abspath(__file__)) + '\edge_data'
    if not os.path.exists(datafile_path):
        os.makedirs(datafile_path)

    print("Starting Simulation...")
    while step < 1000:
        traci.simulationStep()
        step_data = []
        if step % 10 == 0:
            print("Step: %d" % step)
            edge_data = {}
            print("Getting edge data...")
            # Create the data per edge
            for e in edges:
                edge_id = e.getID()
                edge_data[edge_id] = get_edge_data(e)
            edge_df = pd.DataFrame.from_dict(edge_data, orient='index')

            edge_df.columns =['street_name', 'co', 'co2', 'noise', 'num_veh','ped','hc_emission','nox_emission'] 

            # print(edge_df)
            # print(datafile_path)
            for index, row in edge_df.iterrows():
                # print(edge_df[col])
                # print(index)
                # print(row[:])
            # for e in edges:
            #     edge_id = e.getID()
            #     print(edge_df[edge_id])
                write_data_to_file(datafile_path, index, row[:], 'edge', step)
            





            print("Getting tl data...")
            # state_data = getStateData()
            tl_data = {'t_id': ['phase', 'state', 'switch']}
            for t in tl:
                t_id = t.getID()
                tl_data[t_id] = get_tl_data(t)
            tl_df = pd.DataFrame.from_dict(tl_data, orient='index')
            # print(tl_df)


            # traci.edge.subscribe(vehID, (tc.VAR_ROAD_ID, tc.VAR_LANEPOSITION))
            # print(traci.vehicle.getSubscriptionResults(vehID))
           # # print(str(t_id)+" has switch "+str(switch))
           #  print(str(step))
           #  print(str(t_id)+" has state "+str(state))
           #  print(str(t_id)+" has phase "+str(phase))
            
        step += 1

    traci.close()

