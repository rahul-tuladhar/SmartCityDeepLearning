# SmartCityDeepLearning
This repo holds scripts to generate simulation data from [SUMO](http://sumo.dlr.de/wiki). 

[Useful python functions for getting TraCI data](file:///C:/Users/rahul/Sumo/doc/pydoc/traci.html)

The repo uses the current [`python 3.7.0`](https://www.python.org/downloads/release/python-370/). Install on your local machine according to your OS of choice. 

# Description of Map
SUMO generated a map of lower Manhattan to be used in its simulation of pedestrians, trucks, and vehicles along its streets and pathways.

# Useful Files
## requirements.txt
Current packages used:
numpy==1.16.1
pandas==0.24.0
python-dateutil==2.7.5
pytz==2018.9
six==1.12.0

## runner.py
Runs the simulation and collects data from edges and traffic light junctions. Data is stored in new directories `~\edge_data` and `~\tl_data`. There are approximately 11,000 edges and 1,000 traffic light junctions for this SUMO map. 

`cd` into the corresponding folder with a `runner.py` file after cloning the repo.

To run the `runner.py` file, run ```python runner.py```  