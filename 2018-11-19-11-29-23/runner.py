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

from tqdm import tqdm

net = sumolib.net.readNet('osm.net.xml')
edges = net.getEdges()
nodes = net.getNodes()
tl = net.getTrafficLights()



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

    suffix = '.csv'
    file_name = str(data_id) + '_' + str(data_type)
    destination_path = os.path.join(path, file_name + suffix)
    with open(destination_path, 'a') as f:
        df = pd.DataFrame(df).T
        df.to_csv(destination_path, header=False, mode='a', index=False, )
    return 

if __name__ == "__main__":

    # Sumo init
    sumoBinary = checkBinary('sumo')
    sumo_cmd = [sumoBinary, "-c", "osm.sumocfg"]
    traci.start(sumo_cmd)
    step = 0           
    total_steps = 10000 # steps taken by the simulation
    num_entries = 1000  # number of edges or traffic lights you want to create files for

    # path parameters
    dir_name = r'\edge_data' 
    datafile_path = os.path.dirname(os.path.abspath(__file__)) + dir_name

    tl_dir_name = r'\tl_data'
    tl_datafile_path = os.path.dirname(os.path.abspath(__file__)) + tl_dir_name

    # Make new directories to store data for edge and traffic lights
    if not os.path.exists(datafile_path):
        os.makedirs(datafile_path)

    if not os.path.exists(tl_datafile_path):
        os.makedirs(tl_datafile_path)

    print("Starting Simulation...")

    # Ticks for simulation
    for step in tqdm(range(total_steps)):
        traci.simulationStep()
        if step % 5 == 0:
            print("Step: %d / %d " % (step, total_steps))
            print("Getting edge data...")

            # Create the data per edge
            edge_data = {}
            for e in edges[:num_entries]:
                edge_id = e.getID()
                edge_data[edge_id] = get_edge_data(e)

            edge_df = pd.DataFrame.from_dict(edge_data, orient='index')
            edge_df.insert(0,'step', step)
            edge_df.columns = ['step', 'street_name', 'co', 'co2', 'noise', 'num_veh','ped','hc_emission','nox_emission'] 

            # Write edge data files
            for index, row in edge_df[:num_entries].iterrows():
                write_data_to_file(datafile_path, index, row, 'edge', step)

            print("Getting tl data...")

            # Create the data per traffic light / junction
            tl_data = {}
            for t in tl:
                t_id = t.getID()
                tl_data[t_id] = get_tl_data(t)
            tl_df = pd.DataFrame.from_dict(tl_data, orient='index')
            tl_df.insert(0,'step', step)
            tl_df.columns = ['step', 'phase', 'state', 'switch']
            for index, row in tl_df[:num_entries].iterrows():
                write_data_to_file(tl_datafile_path, index, row, 'tl', step)

        # step += 1

    traci.close()

