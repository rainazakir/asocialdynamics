# Bio-inspired decision making in swarms under biases from stubborn robots, corrupted communication, and independent discovery

Repo contains the code to run Gillespie simulation, the robot simulation code and the code to process Gillespie and robot simulation data to generate the figures. For all the installations, we assume a clean installation of Ubuntu20.04 or Ubuntu22.04.

### Running Robot simulations
ArgosCode_antagonistic contains the robot controller to run experiments with antagonistic asocial dynamics and ArgosCode_notantagonistic contains code to run experiments with synergetic bias.
The robot controller can be found at `ARGoS_simulation/behaviours/agent_red.c`. 

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

### Running Gillespie simulations


