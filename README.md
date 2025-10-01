# Bio-inspired decision making in swarms under biases from stubborn robots, corrupted communication, and independent discovery

Repo contains the code to run Gillespie simulation, the robot simulation code and the code to process Gillespie and robot simulation data to generate the figures. For all the installations, we assume a clean installation of Ubuntu20.04 or Ubuntu22.04.

## Running Robot simulations
ArgosCode_antagonistic contains the robot controller to run experiments with antagonistic asocial dynamics and ArgosCode_notantagonistic contains code to run experiments with synergetic bias.
The robot controller can be found at `ARGoS_simulation/behaviours/agent_red.c`. We simulate the Kilogrid environment that robots use to source opinions, for which the module controller can be found at `ARGoS_simulation/loopfunctions/kilogrid_stub.cpp`.

You need to have argos3 and Kilobot plugin for argos3 to run the simulations. 

Install argos3:

```
git clone https://github.com/ilpincy/argos3
cd argos3
mkdir build
cd build
cmake ../ARGoS_simulation
make 
``` 

Install Kilobot-Plugin

```
git clone https://github.com/ilpincy/argos3-kilobot.git
cd argos3-kilobot
```

Renew the link to argos3  (first remove it).

```
cd src/
rm argos3
cd ..
ln -s ~/Programs/argos3-kilobot/src/ src/argos3
cmake -DCMAKE_BUILD_TYPE=Release ../src
make -j4
make install
```

How to run experiments

```
cd ArgosCode_antagonistic/ARGoS_simulation/data_generation_scripts/
sh local_create_argos_files_and_run.sh <start> <end> 
```

This runs the experiments local. (You have to proper build it first!)

The results are saved at data_cluster/<experiment>/...

## Running Gillespie simulations

There are two files, one for running Gillespie simulations using cross-inhibition mechanism and the other for direct-switch mechanism. The main dependency is python.
To run the experiment:
```
python3 <Timesteps> <No._of_agents> <t_u> <t_d> <t_e> <q_a> <eta> <plot_or_no> <eta_a>
```
Vary <eta> to include asocial dynamics to the system and <eta_a> to bias the dynamics synergetically or antagonistically. Specify the number of repetitions within the code. 
The output file can be of two types:  (i) evolution of agents in each state A_D, B_D, A_E, B_E and U (for CI) across last X timesteps or (ii) normalized stationary probability distribution matrix for easier plotting.

## Plotting data
To generate the figures in the study, generate data using Gillespie or Robot simulations. Then use the following python based scripts to get the plots:

* [Formatting](https://github.com/rainazakir/asocialdynamics/tree/main/Plottingcode/getdatainformat) folder contains two scripts (one for CI and one for DS) to get robot simulation data to reduce the simulation data into the right format to generate the heatmaps for Figure 4 and Figure 7.

