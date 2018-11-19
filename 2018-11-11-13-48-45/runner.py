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


##------Generating Edge ID---------##
f = open("edges.txt","w")
for edge in sumolib.output.parse_fast("osm.net.xml", 'edge', ['id']):
    print(edge.id)
    f.write(edge.id)
f.close()


if __name__ == "__main__":

    sumoBinary = checkBinary('sumo-gui')

    # net = 'osm.net.xml'
    # subprocess.call([checkBinary('netconvert'),
    #                  '-c', 'osm.netccfg'],
    #                 stdout=sys.stdout, stderr=sys.stderr)


    traci.start([sumoBinary, "-c", "osm.sumocfg"])
    # while traci.simulation.getMinExpectedNumber() > 0: 
    #    for veh_id in traci.vehicle.getIDList():
    #         position = traci.vehicle.getSpeed(veh_id)
    #    traci.simulationStep()
    # traci.close()

    # while traci.simulation.getMinExpectedNumber() > 0: 
    #    for veh_id in traci.simulation.getDepartedIDList():
    #        traci.vehicle.subscribe(veh_id, [traci.constants.VAR_POSITION])
    #        positions = traci.vehicle.getSubscriptionResults(veh_id)
    #        print(positions)
    #    traci.simulationStep()
    edges = [e for e in sumolib.output.parse_fast("osm.net.xml", 'edge', ['id'])]
    lanes = [l for l in sumolib.output.parse_fast('osm.net.xml', 'lane', ['id'])]
    step = 0
    
    while step < 100:
        traci.simulationStep()
      
        if step % 10 == 0:

            for e in edges:
                lane_ID = e.id
                co = traci.edge.getCOEmission(lane_ID)
                noise = traci.edge.getNoiseEmission(lane_ID)
                num_veh = traci.edge.getLastStepVehicleNumber(lane_ID)
                ped = traci.edge.getLastStepPersonIDs(lane_ID)
                print("Step: " + str(step) +  "Edge ID: " + e.id + " CO Emission: " + str(co))
        step += 1

    traci.close()

