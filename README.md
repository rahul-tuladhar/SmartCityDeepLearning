# SmartCityDeepLearning

This repo holds scripts to generate simulation data from [SUMO](http://sumo.dlr.de/wiki). 

[Useful python functions for getting TraCI data](file:///C:/Users/rahul/Sumo/doc/pydoc/traci.html)

## Installing [SUMO](http://sumo.dlr.de/wiki/Installing)
 Follow the instructions listed below
> There are four different binary packages for Windows depending on the platform (32 vs. 64 bit) you have and what you want to do with SUMO. If you want to install it locally and have administrator rights on your machine you should download and execute one of the installers (preferably 64 bit). If you need a "portable" version or do not have admin rights, use the correct zip, extract it into a desired folder using 7Zip, Winzip, or a similar tool. Every package contains the binaries, all dlls needed, the examples, tools, and documentation in HTML format.
>
>    Download 64 bit installer: sumo-win64-1.0.1.msi
>    Download 64 bit zip: sumo-win64-1.0.1.zip
>    Download 32 bit installer: sumo-win32-1.0.1.msi
>    Download 32 bit zip: sumo-win32-1.0.1.zip
>
>Within the installation folder, you will find a folder named "bin". Here, you can find the executables (programs). You may double click on SUMO-GUI and take a look at the examples located in docs/examples. All other applications (DUAROUTER, DFROUTER, etc.) have to be run from the command line. To facilitate this there is also a start-commandline.bat which sets up the whole environment for you. If you feel unsure about the command line, please read Basics/Basic_Computer_Skills#Running_Programs_from_the_Command_Line.
>
>If you want a bleeding edge nightly build or need tests or source files, you can download them from the Download page.
>
>For building SUMO from source see building SUMO under Windows. 

## Running SUMO

After installing SUMO and setting up the `SUMO_HOME` system variable accordingly, you can run the generated file using the `runner.py` file.
Make sure you are within the correct directory where `runner.py` is in. From that directory, you can run:
```python runner.py```
A SUMO window should appear, you can click the 'run' button at the top to start the simulation. Output can be visible in the console.
 
## 2018-10-28-14-39-53 
This file holds a generated New York City map and corresponding `.xml` files. 
Use `python runner.py` within the directory in order to run the corresponding generated map file.

## 2018-11-11-13-13-48-45
This file holds a different generated New York City map and corresponding `.xml` files. 
Use `python runner.py` within the directory in order to run the corresponding generated map file.

## Runner.py

This script is used to run the `.osm` file and output the simulation data.

## Troubleshooting 
 List of errors encountered:
  - If there are import errors such as `module traci not found` make sure in your `system variables` that `SUMO_HOME` does not have any trailing semicolons `;` otherwise when concatenating the path in `tools = os.path.join(os.environ['SUMO_HOME'], 'tools')` that tools will not be concatentated into the right string. Example: `C:\user\Sumo\;\tools` 
 
