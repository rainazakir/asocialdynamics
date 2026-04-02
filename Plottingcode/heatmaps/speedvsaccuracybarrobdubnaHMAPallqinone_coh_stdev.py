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
import seaborn as sns

import random
import pandas as pd
plt.rcParams["figure.figsize"] = (88, 58)

colours = ["#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"]
symbols=["o","v","*","d","h","X","P","+"]
# plt.gca().set_color_cycle (['red', 'blue', 'yellow', 'green','orange','black'])
axis = list(range(0, 1))
op1 = []
op2 = []
op3 = []
un = []

listFiles = []
x = 0
mysum = 0
pointxaxis = []
patch = []
pointyaxis = []


#data directory
opdir='/Volumes/My_Passport/020323_gillespietu/gillespie'
opdir='/Volumes/My_Passport/journal_hmap_newq/ds_1.5'

data_files = []
data_files += [file for file in os.listdir(opdir)]

N = 100
xx = 0
position = {}
xtimes = 0
node_colors = {}
assortivity = {}
xaxisrange = []

NumofFiles = 100

typemodall = []

thetotaltimevalsA = [0]*100001
thetotaltimevalsB = [0]*100001
filesnum  = 0
findnoise = '0.3noise'
findqr = '[1.0, 1]'
tuconf='[0, 14, 14, 36, 36]1000.0td1300te3300'
vmconf='[14, 14, 36, 36]1e-07td1300te3300'


xaxis = []
yaxis = []
N=100
reachedquorum = 0
timestepquorumrreached=0
timestepquorumrreachedconverged=0
#swarm_comp_[0.9,0.1]_mdl
normcomp_xaxis = []
accuracy = []
dectime = []
ci_accuracy =[]
ci_noiseA =[]
ci_time = []
ci_noiseT = []
stddec=[]
timestepsstd=[]

ds_accuracy =[]
ds_noiseA =[]
ds_time = []
ds_noiseT = []
popA =0
popB= 0
totpop = 0
filecount = 0
avgval = 0
filesnum = 0
quorumtocheckfor = "q0.75" #q0.75, 0.66,1-m,2f
for subdir, dirs, files in sorted(os.walk(opdir)):
    for name in sorted(dirs):
        print(name.split('_'))

        typemod = name.split('_')[1]

        noiseA = float(name.split('_')[3].split('n')[0])
        noiseT = float(name.split('_')[7].split(']')[1])
        qr = (name.split('_')[7])

        print(N,quorumtocheckfor,typemod,noiseA)

        reachedquorum = 0
        typemodall.append(typemod)

        for file in sorted(os.listdir(os.path.join(subdir, name))):
                #for file in os.path.join(subdir, name):
                    #print(file)
                 if filesnum<=100:
                    if file.startswith("evo"):  # ci_te3300td1300_   ci_te3300td1300_highcomm0.5forcoord_42_exp_Quality_50_50_200k_100_N_2_Noise_0.05_UncommT_0000_COORD_0
                        if file.endswith(".txt"):  # _0000_COORD_0.txt
                            #filesnum = filesnum + 1
                            with open(os.path.join(subdir,name, file)) as f:
                               # print("The files2 is", file)
                                filesnum += 1
                                for i, line in enumerate(f):
                                    #print(line)
                                    # #print(line.split())
                                        if(typemod == 'ci0.05'):

                                               if(line.split()[7]==quorumtocheckfor):
                                                           ####### print(line)
                                                                timestepquorumrreached = timestepquorumrreached + float(line.split()[0])
                                                                timestepquorumrreachedconverged = timestepquorumrreachedconverged + float(line.split()[0])
                                                                reachedquorum +=1
                                                                timestepsstd.append(float(line.split()[0]))

                                                                popB =  popB + ((int(line.split()[3])+int(line.split()[5])))
                                                                avgval = avgval  + abs(popA - popB)/N
                                                                break
                                                                xx = 0
                                                                check = 0
                                                               ################## print(file, line)
                                               else:
                                                        timestepquorumrreached = timestepquorumrreached + 100000

                                        else:
                                            if(line.split()[6]==quorumtocheckfor):
                                                    ######### print(line)
                                                        timestepquorumrreached = timestepquorumrreached + float(line.split()[0])
                                                        timestepquorumrreachedconverged = timestepquorumrreachedconverged + float(line.split()[0])
                                                        reachedquorum +=1
                                                        timestepsstd.append(float(line.split()[0]))
                                                        popA = popA + (int(line.split()[1]) + int(line.split()[3]))
                                                        popB = popB + ((int(line.split()[2]) + int(line.split()[4])))
                                                        avgval = avgval  + abs(popA - popB)/N
                                                        break
                                                        #print("comes here to check")
                                                        xx = 0
                                                        check = 0
                                            else:
                                                    ###0print(file)
                                                    timestepquorumrreached = timestepquorumrreached + 100000



                            # timestepquorumrreached = 50000
        print("stats: ",filesnum, reachedquorum)
        print("pop: ",popA/N, popB/N,(popA/N) -(popB/N),avgval,reachedquorum)
        xaxis.append(round(noiseT,2))
        yaxis.append(round(noiseA,2))

        if typemod == 'ci0.05':
            #ci_noiseA.append(noise)

            if (reachedquorum == 0):
                ci_accuracy.append(0)
                ci_time.append(0)
            else:
                totpop = (popA / reachedquorum) - (popB / reachedquorum)

                ci_accuracy.append(reachedquorum/filesnum)
                ci_time.append(timestepquorumrreachedconverged / reachedquorum)
            stddec.append(np.array(timestepsstd).std())
        else:
            if (reachedquorum == 0):
                ds_accuracy.append(0)

                ds_time.append(0)
            else:
                totpop = (popA / reachedquorum) - (popB / reachedquorum)

                ds_accuracy.append(reachedquorum/filesnum)
                ds_time.append(timestepquorumrreachedconverged / reachedquorum)
            stddec.append(np.array(timestepsstd).std())

        filesnum = 0
        reachedquorum = 0
        timestepquorumrreached = 0
        timestepquorumrreachedconverged = 0
        totpop = 0
        popB = 0
        popA = 0
        avgval =0
        filesnum=0
        timestepsstd = []

fig, ax = plt.subplots()
# ax2 = ax1.twinx()
print(len(yaxis),len(xaxis),len(ci_time))
data = pd.DataFrame({'h': xaxis, 'k': yaxis, 'br': stddec})
data_pivoted = data.pivot("h", "k", "br")
print(data_pivoted.to_string())

# print(hval)
#ax = sns.heatmap(data_pivoted, annot=False, cmap="viridis")

ax = sns.heatmap(data_pivoted, annot=False, cmap="viridis",vmin=0,vmax=100000)
ax.invert_yaxis()
ax.tick_params(axis='y', rotation=0)
ax.tick_params(labelsize=80)
cax = ax.figure.axes[-1]
cax.tick_params(labelsize=72)
plt.savefig('/Volumes/My_Passport/argosim2/Runs/journal/imageshmap/STDEVnewqset_norm_hmap_'+str(typemod)+'_Tcoh_q'+str(qr)+'_'+str(quorumtocheckfor)+'.pdf', dpi=300, bbox_inches='tight')

plt.show()


#plt.savefig('/Volumes/My_Passport/argosim2/Runs/journal/images/new_speed_cohesion_qr1.5_0.66.pdf', dpi=300, bbox_inches='tight')


