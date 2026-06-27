import matplotlib.pyplot as plt
import glob, os
from pathlib import Path
import pathlib
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
# from scipy.interpolate import make_interp_spline, BSpline
import matplotlib.lines as mlines
import pandas as pd
import scipy as sp
import networkx as nx

import random
import pandas as pd
plt.rcParams["figure.figsize"] = (30, 24)
#plt.rcParams["figure.figsize"] = (20, 12)



#colours = ['#fde725', '#5ec962', '#21918c',
 #                 '#3b528b', '#2c728e', '#440154',
 #                 '#999999', '#e41a1c', '#dede00']
#colours = ["#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"]
# plt.rcParams.update({'font.size': 14})
colours = ["#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"]
symbols=["o","v","*","d","h","X","P","+"]
# plt.gca().set_color_cycle (['red', 'blue', 'yellow', 'green','orange','black'])
axis = list(range(0, 1))
op1 = []
op2 = []
op3 = []
un = []
#plt.xlim(-1, 1)
#plt.ylim(0, 0.04)
listFiles = []
x = 0
mysum = 0
pointxaxis = []
patch = []
pointyaxis = []
# for file in glob.glob("*.txt"):
# listFiles.append(file)
# opdir = 'D:/Simpaperresults/probabilitydistfromGillespieandsim/datafiles/'  # os.getcwd()

opdir= '/Users/raina/Documents/argosim2/Runs/Plottingspdfile/hist/'
##opdir='/Users/raina/Documents/argosim2/Runs/kilogridci/echocoord1/data_cluster/'
opdir='/Volumes/My_Passport/dem1/results/type-swarm_mdl-[direct]_rle-[random]_qvl-[1,1]_op-2_stdDv-1_agt-100_agtRad-0.2/'
opdir='/Users/raina/Documents/AAMASruns/justonefile/'
opdir ='/Users/raina/Documents/AAMASruns/runs/results/'
opdir='/Volumes/My_Passport/demself/results/'
opdir='/Volumes/My_Passport/dem_self_majorana/'
opdir='/Volumes/My_Passport/dem_self_majorana/'
opdir='/Volumes/My_Passport/020323_gillespietu/gillespie'
opdir='/Volumes/My_Passport/240223_gillespiespeed/gillespie'
opdir='/Volumes/My_Passport/030323_nemtestspd/data_cluster/'
opdir='/Volumes/My_Passport/journal_rob_na/data_cluster/'

data_files = []
data_files += [file for file in os.listdir(opdir)]

# files1 = Path().cwd().glob("**/*.txt")
# for f in files1:
#    nm=pathlib.Path(*f.parts[8:])
#    listFiles.append(str(nm))
# print(listFiles)
#listFiles= ["statistics_39972450.txt", "statistics_197411160.txt", "statistics_870119300.txt"]
#print(data_files)
N = 100
xx = 0
position = {}
xtimes = 0
node_colors = {}
assortivity = {}
xaxisrange = []

NumofFiles = 30

typemodall = []
type = []
#for filenum in range(NumofFiles-1):

thetotaltimevalsA = [0]*100001
thetotaltimevalsB = [0]*100001
filesnum  = 0
findnoise = '0.00'
findqr = '50'
findstdv = 'stdDv-1'
swarmcom= 'swarm_comp_'
tuconf='1000'
vmconf='0000'

#swarmcom= 'swarm_comp_[0.96,0.04]_mdl'
#type-swarm_comp_[0.01,0.99]_mdl-[direct,direct]_rle-[majority,minority]_qvl-[1,1]_op-2_stdDv-1_agt-200_agtRad-0.2
xaxis = []
yaxis = []
N=100

"""
#noise0.04,n_a=0.5
ciA = [0.88,0.54,0.9,1]
ciT = [94617.568,72692.296,63747.6889,39878]
dsA=[0.04,0.08,0.5,0.98]
dsT=[131045.5,113510.25,113474.16,81250.204]
"""
"""
#n_a=0.1 , noise=0.05
ciA = [1,0.1176,0.431373,0.98]
ciT = [53884.7,95852.667,106025.771,66447.56]
dsA=[0.49,0,0.039216,0.627451]
dsT=[122306.44,0,112327.00,106170.46875]
"""
"""
#n_a=0.1 , noise=0.05
ciA = [1,0.274,0.568,0.96]
ciT = [37035.4,64226.3,58023.8,39787.3]

dsA=[1,0.333,0.921,1]
dsT=[75167.2,98989.94,75374.4,27497.47]
"""
#n_a=0.5 , noise=0.05
ciA = [0.96,0.725,0.961,1]
ciT = [56304.7,48160.9,36855.1,19874.9]

dsA=[0.902,0.921,1,0.99]
dsT=[85956.7,76083.78,39074.21,19678.4]

plt.scatter(ciA,ciT,marker='o',s=3200,color=['pink','orange','red','darkred'])
plt.scatter(dsA,dsT,marker='s',s=3200,color=['pink','orange','red','darkred'])


plt.ylim(-3000, 140000)
plt.xlim(-0.01, 1.03)

plt.xticks(fontsize=56)#51,51
plt.yticks(fontsize=56)

plt.ylabel(r'timesteps', fontsize=64)#60,60
plt.xlabel(r'' 'accuracy', fontsize=64)

#plt.savefig('/Volumes/My_Passport/argosim2/Runs/journal/images/26_rob_exp_newp_pf_na0.5_n0.05.pdf', dpi=600, bbox_inches='tight')

plt.show()
