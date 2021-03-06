from __future__ import absolute_import
from __future__ import print_function

import os, sys
import optparse
import random

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



    step = 0
    
    while step < 1:
      traci.simulationStep()
      

      for e in sumolib.output.parse_fast("osm.net.xml", 'edge', ['id']):
        lane_ID = e.id
        co = traci.edge.getCOEmission(lane_ID)
        noise = traci.edge.getNoiseEmission(lane_ID)
        num_veh = traci.edge.getLastStepVehicleNumber(lane_ID)
        ped = traci.edge.getLastStepPersonIDs(lane_ID)
        print("Edge ID: " + e.id + " CO Emission: " + str(co))
      step += 1

    traci.close()

