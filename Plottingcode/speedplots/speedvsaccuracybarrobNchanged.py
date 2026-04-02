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
plt.rcParams["figure.figsize"] = (25, 18)
plt.rcParams["figure.figsize"] = (20, 12)

colours = ["#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"]
symbols=["o","v","*","d","h","X","P","+"]
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

# data directory

opdir='/Volumes/My_Passport/240423_journal_speedN/selected1.08/'

data_files = []
data_files += [file for file in os.listdir(opdir)]

N = 100
xx = 0
position = {}
xtimes = 0
node_colors = {}
assortivity = {}
xaxisrange = []

NumofFiles = 30

typemodall = []
typemodallN = []


thetotaltimevalsA = [0]*100001
thetotaltimevalsB = [0]*100001
filesnum  = 0
findnoise = '0.0noise'
findqr = '[1.08, 1]1.0'
findstdv = 'stdDv-1'
swarmcom= 'swarm_comp_'
tuconf='1000'
vmconf='0000'


xaxis = []
yaxis = []
#N=100
reachedquorum = 0
timestepquorumrreached=0
timestepquorumrreachedconverged=0
#swarm_comp_[0.9,0.1]_mdl
normcomp_xaxis = []
accuracy = []
dectime = []
stddec=[]
filecount = 0
noise =0
reachedquorum = 0
timestepsstd=[]
for subdir, dirs, files in sorted(os.walk(opdir)):
    for name in sorted(dirs):
        print(name.split('_'))
        print(name.split('_')[7])
        typemod = name.split('_')[1]
        #print(typemod)
        quorum = float(name.split('_')[7].split(']')[1])
        noise = float(name.split('_')[3].split('n')[0])
        N = float(name.split('_')[6].split('a')[0])
        print(quorum,N,quorum*N,typemod, noise)

        if(name.split('_')[3] == str(findnoise) and name.split('_')[7] == str(findqr) and (N == 50 or N ==200 or N==400)):
                print("The chosen is",name)
                reachedquorum = 0
                typemodall.append(typemod)
                for file in sorted(os.listdir(os.path.join(subdir, name))):
                    if file.startswith("evo"):  # ci_te3300td1300_   
                        if file.endswith(".txt"):  # _0000_COORD_0.txt
                            with open(os.path.join(subdir,name, file)) as f:
                                filesnum += 1
                                for i, line in enumerate(f):
                                        if(typemod == 'ci'):
                                            if(((int(line.split()[2])+int(line.split()[4]))>=(N*quorum))): 
                                                        timestepquorumrreached = timestepquorumrreached + float(line.split()[0])
                                                        timestepquorumrreachedconverged = timestepquorumrreachedconverged + float(line.split()[0])

                                                        timestepsstd.append(float(line.split()[0]))

                                                        reachedquorum +=1
                                                        xx = 0
                                                        check = 0
                                            else:
                                                timestepquorumrreached = timestepquorumrreached + 100000
                                        else:
                                            if(int(int(line.split()[1])+int(line.split()[3]))>=(N*quorum)):
                                                      #  print(line)
                                                        timestepquorumrreached = timestepquorumrreached + float(line.split()[0])
                                                        timestepquorumrreachedconverged = timestepquorumrreachedconverged + float(line.split()[0])
                                                        timestepsstd.append(float(line.split()[0]))
                                                        reachedquorum +=1
                                                        break
                                                        xx = 0
                                                        check = 0
                                            else:
                                                timestepquorumrreached = timestepquorumrreached + 100000



                print("stats: ",filesnum, reachedquorum)
                normcomp_xaxis.append((noise))
                accuracy.append(reachedquorum/filesnum)
                typemodallN.append(N)
                if(reachedquorum == 0):
                    dectime.append(0)
                else:
                    dectime.append(timestepquorumrreachedconverged/reachedquorum)
                stddec.append(np.array(timestepsstd).std())
                filesnum = 0
                reachedquorum = 0
                timestepquorumrreached = 0
                timestepquorumrreachedconverged = 0
                timestepsstd =[]



print(normcomp_xaxis, len(normcomp_xaxis))
print(accuracy, len(accuracy))#dectime
print(dectime, len(dectime))#dectime
print(typemodallN, len(typemodallN))#dectime
print(stddec, len(stddec))


df = pd.DataFrame({"range": typemodall,"N": typemodallN, "time":dectime,"error":stddec})
fig, ax = plt.subplots()
#yerr = df.pivot(index='class1', columns='class2', values='se')
ax = df.pivot("range", "N", "time")
yerr = df.pivot("range", "N", "error")
ax.plot(kind='bar',colormap='viridis', rot=0,yerr=yerr,error_kw=dict(lw=5, capsize=20, capthick=4))
ax = plt.gca()
ax.set_ylim([0, 200000])
#plt.show()
index_order = ['ci', 'vm']
print(df)
ax.tick_params(labelsize=50)
ax.tick_params(labelsize=50)
#ax2.tick_params(labelsize=50)
ax.legend(fontsize=45) # using a size in points

ax.set_ylabel(r'Timesteps', fontsize=66)

#plt.savefig('/Volumes/My_Passport/argosim2/Runs/journal/images/dec_cahnged_newNspeed_n0.00_speed_qr1.08_1.pdf', dpi=300, bbox_inches='tight')

plt.show()
