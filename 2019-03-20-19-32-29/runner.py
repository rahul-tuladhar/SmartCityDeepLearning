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
from datetime import datetime



def get_edge_data(edge):
    """ Returns a list of numerical and string data per edge """
    edge_id = edge.getID()
    street_name = traci.edge.getStreetName(edge_id)
    noise = traci.edge.getNoiseEmission(edge_id)
    num_veh = traci.edge.getLastStepVehicleNumber(edge_id)
    num_lane = traci.edge.getLaneNumber(edge_id)
    wait_time = traci.edge.getWaitingTime(edge_id)
    occupancy = traci.edge.getLastStepOccupancy(edge_id)
    fuel = traci.edge.getFuelConsumption(edge_id)
    electricity= traci.edge.getElectricityConsumption(edge_id)
    co = traci.edge.getCOEmission(edge_id)
    co2 = traci.edge.getCO2Emission(edge_id)
    hc = traci.edge.getHCEmission(edge_id)
    nox = traci.edge.getNOxEmission(edge_id)
    pmx = traci.edge.getPMxEmission(edge_id)
    ped = traci.edge.getLastStepPersonIDs(edge_id) 
    data = [street_name,noise, num_veh, num_lane, wait_time, occupancy, fuel, electricity, co, co2, hc, nox, pmx, ped]
    return data

def get_tl_data(tl):
    """ returns list of numerical and string data per tl
     string format is necessary to view in stdout
    """
    t_id = tl.getID()
    phase = traci.trafficlight.getPhase(t_id)
    duration = traci.trafficlight.getPhaseDuration(t_id)
    state = str(traci.trafficlight.getRedYellowGreenState(t_id))
    data = [phase, duration, state]
    return data    

def write_data_to_file(path, data_id, df, str_data_type, step):
    """ Writes values from dataframe to .csv file"""
    #   path: where to save the files
    #   data_id: name of kind of data; edge, tl, etc
    #   df: dataframe 
    #   str_data_type: type_data
    #   step: time interval in ticks

    suffix = '.csv'
    file_name = str(data_id) + '_' + str(str_data_type)
    destination_path = os.path.join(path, file_name + suffix)
    with open(destination_path, 'w') as f:
        df = pd.DataFrame(df)
        df.to_csv(destination_path, header=True, mode='w', index=False)
    return 

def generate_edge_data(total_steps, num_entries, traci, edges, step):
    """ Returns dictionary of edge data for given series.
        Stores the values in memory in a single batch.
        Step size is 5 which was arbitrarily chosen.         
    """
    edge_series_data = {}
    for step in tqdm(range(total_steps)):
        traci.simulationStep()
        if step % 5 == 0:
            # Create the data per edge
            for e in edges[:num_entries]:
                edge_id = e.getID()
                edge_data = [step] + get_edge_data(e)
                # print(edge_id,edge_data)
                if edge_id not in edge_series_data:
                    edge_series_data[edge_id] = [['step','street_name','noise', 'num_veh', 'num_lane', 'wait_time', 'occupancy', 'fuel', 'electricity', 'co','co2', 'hc', 'nox', 'pmx', 'ped']]
                else:
                    edge_series_data[edge_id].append(edge_data)
    return edge_series_data

def generate_tl_data(total_steps, num_entries, traci, tl, step):
    """ TODO: Figure out if the simulation steps are synced for both 
        edge and tl. Most likely this is not the case
    """
    tl_series_data = {}
    for step in tqdm(range(total_steps)):
        traci.simulationStep()
        if step % 5 == 0:
            # Create the data per edge
            for t in tl[:num_entries]:
                tl_id = t.getID()
                tl_data = [step] + get_tl_data(t)
                # print("edge_data",edge_data)
                if tl_id not in tl_series_data:
                    tl_series_data[tl_id] = [['step', 'phase', 'state', 'switch']]
                else:
                    tl_series_data[tl_id].append(tl_data)
    return tl_series_data
    
def get_df(edge_data):
    """ Returns dataframe given dictionary of edge values """
    edge_data = np.array(edge_data)
    df = pd.DataFrame(data=edge_data[1:,1:], index=edge_data[1:,0], columns=edge_data[0,1:])  # 1st row as the column names
    return df




if __name__ == "__main__":

    # Sumo init and global simulatio parameters
    sumoBinary = checkBinary('sumo')
    sumo_cmd = [sumoBinary, "-c", "osm.sumocfg"]
    traci.start(sumo_cmd)
    step = 0           
    total_steps = int(sys.argv[1]) if sys.argv[1] else 1000# steps taken by the simulation
    num_entries = int(sys.argv[2]) if sys.argv[1] else 10000# number of edges or traffic lights you want to create files for
    # total_steps = 30 # steps taken by the simulation
    # num_entries = 100  # number of edges or traffic lights you want to create files for
    date = datetime.now().strftime("%I-%M-%S-%B-%d-%Y") # path parameter
    edge_dir_name = r'\edge_data-{}-{}-{}'.format(total_steps, num_entries, date)
    edge_datafile_path = os.path.dirname(os.path.abspath(__file__)) + edge_dir_name
    tl_dir_name = r'\tl_data-{}-{}-{}'.format(total_steps, num_entries, date)
    tl_datafile_path = os.path.dirname(os.path.abspath(__file__)) + tl_dir_name

    net = sumolib.net.readNet('osm.net.xml')
    edges = net.getEdges()
    nodes = net.getNodes()
    tl = net.getTrafficLights()


    # Make new directories to store data for edge and traffic lights
   

    print("Starting Simulation...")
    print("Generating Edge Data...")
    edge_series_data = generate_edge_data(total_steps, num_entries, traci, edges, step)

    if not os.path.exists(edge_datafile_path):
        os.makedirs(edge_datafile_path)

    print("Writing Edge Data Files to {}...".format(edge_datafile_path))
    for edge_id, edge_data in tqdm(edge_series_data.items()):
        edge_series_df = get_df(edge_data)
        write_data_to_file(edge_datafile_path, edge_id, edge_data, 'edge', step)

    print("Generating Traffic Light Data...")
    tl_series_data = generate_tl_data(total_steps, num_entries, traci, tl, step)

    if not os.path.exists(tl_datafile_path):
        os.makedirs(tl_datafile_path)

    print("Writing Traffic Light Data Files to {}...".format(tl_datafile_path))
    for tl_id, tl_data in tqdm(tl_series_data.items()):
        # print("edge_data:", edge_data)
        tl_series_df = get_df(tl_data)
        write_data_to_file(tl_datafile_path, tl_id, tl_data, 'tl', step)

    traci.close()

