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
plt.rcParams["figure.figsize"] = (48, 18)
#plt.rcParams["figure.figsize"] = (22, 12)



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


opdir='/Volumes/My_Passport/020323_gillespietu/gillespie'
opdir='/Volumes/My_Passport/journal_perrobN/gillespie'
opdir = '/Volumes/My_Passport/journal_perrobN/gillespienewt1'
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

NumofFiles = 100

typemodall = []
#for filenum in range(NumofFiles-1):

thetotaltimevalsA = [0]*100001
thetotaltimevalsB = [0]*100001
filesnum  = 0
findnoise = '0.3noise'
findqr = '[1.0, 1]0.7'
tuconf='[0, 14, 14, 36, 36]1000.0td1300te3300'
vmconf='[14, 14, 36, 36]1e-07td1300te3300'

#swarmcom= 'swarm_comp_[0.96,0.04]_mdl'
#type-swarm_comp_[0.01,0.99]_mdl-[direct,direct]_rle-[majority,minority]_qvl-[1,1]_op-2_stdDv-1_agt-200_agtRad-0.2
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

ds_accuracy =[]
ds_noiseA =[]
ds_time = []
ds_noiseT = []

filecount = 0
for subdir, dirs, files in sorted(os.walk(opdir)):
    for name in sorted(dirs):
        print(name.split('_'))
       # print(name.split('_')[3].split('n')[0])
        #print(name.split('_')[7])
        typemod = name.split('_')[1]
        #print(typemod)
        quorum = float(name.split('_')[7].split(']')[1])
        print(quorum,N,quorum*N,typemod)
        noise = float(name.split('_')[3].split('n')[0])
        N = float(name.split('_')[6].split('a')[0])
        #qr = float(name.split('_')[7])
       # print(noise,qr)
        #quorum = 0.8 * (norm*100)
        #print(name.split('_'))
        #name.split('_')[3] == str(findnoise) and
        ##########if(name.split('_')[3] == str(findnoise) and name.split('_')[7] == str(findqr) and (name.split('_')[2] == str(vmconf) or name.split('_')[2] == str(tuconf) ) ):
           # if(name.split('-')[2] == findfolder and name.split('-')[1] == swarmcom ):
               ######### print("The chosen is",name)
        reachedquorum = 0
        typemodall.append(typemod)
        if(N<260):
            for file in sorted(os.listdir(os.path.join(subdir, name))):
                    #for file in os.path.join(subdir, name):
                       ### print(file)
                        if file.startswith("evo"):  # ci_te3300td1300_   ci_te3300td1300_highcomm0.5forcoord_42_exp_Quality_50_50_200k_100_N_2_Noise_0.05_UncommT_0000_COORD_0
                            if file.endswith(".txt"):  # _0000_COORD_0.txt
                                with open(os.path.join(subdir,name, file)) as f:
                                   # print("The files2 is", file)
                                    filesnum += 1
                                    for i, line in enumerate(f):
                                        #print(line)
                                        # #print(line.split())
                                            if(typemod == 'ci0.05'):
                                               # print(((int(line.split()[2]) + int(line.split()[4]))),
                                                 #    ((int(line.split()[3]) + int(line.split()[5]))))

                                                if(((int(line.split()[2])+int(line.split()[4]))>=(N*quorum))): #or ((int(line.split()[3])+int(line.split()[5]))>=(N*quorum))):
                                                           ####### print(line)
                                                            timestepquorumrreached = timestepquorumrreached + float(line.split()[0])
                                                            timestepquorumrreachedconverged = timestepquorumrreachedconverged + float(line.split()[0])
                                                            reachedquorum +=1
                                                            break
                                                            xx = 0
                                                            check = 0
                                                            #print(file, line)
                                                else:
                                                    timestepquorumrreached = timestepquorumrreached + 0
                                                    #print(file, line)
                                                    #timestepquorumrreachedconverged = 0
                                            else:
                                                if(int(int(line.split()[1])+int(line.split()[3]))>=(N*quorum)): #or int(int(line.split()[2])+int(line.split()[4]))>=(N*quorum)):
                                                           ######### print(line)
                                                            timestepquorumrreached = timestepquorumrreached + float(line.split()[0])
                                                            timestepquorumrreachedconverged = timestepquorumrreachedconverged + float(line.split()[0])
                                                            reachedquorum +=1
                                                            break
                                                            #print("comes here to check")
                                                            xx = 0
                                                            check = 0
                                                else:
                                                    timestepquorumrreached = timestepquorumrreached + 0

                                                    #timestepquorumrreachedconverged = 0


                                # timestepquorumrreached = 50000
            print("stats: ",filesnum, reachedquorum)
            normcomp_xaxis.append((N))
            if typemod == 'ci0.05':
                ci_noiseA.append(N)
                ci_accuracy.append(reachedquorum/filesnum)
                if (reachedquorum == 0):
                    ci_time.append(0)
                else:
                    #ci_time.append((timestepquorumrreachedconverged / reachedquorum)/N)
                    ci_time.append(timestepquorumrreachedconverged / reachedquorum)
            else:
                ds_noiseA.append(N)
                ds_accuracy.append(reachedquorum / filesnum)
                if (reachedquorum == 0):
                    ds_time.append(0)
                else:
                    #ds_time.append((timestepquorumrreachedconverged / reachedquorum)/N)
                    ds_time.append(timestepquorumrreachedconverged / reachedquorum)
            #accuracy.append(reachedquorum/filesnum)
            #dectime.append(timestepquorumrreached/ filesnum)
    #                    if(reachedquorum == 0):
    #                       dectime.append(0)
    #                   else:
    #                       dectime.append(timestepquorumrreachedconverged/reachedquorum)"
            filesnum = 0
            reachedquorum = 0
            timestepquorumrreached = 0
            timestepquorumrreachedconverged = 0




###print(normcomp_xaxis, len(normcomp_xaxis))
###print(accuracy, len(accuracy))#dectime
###print(dectime, len(dectime))#dectime
print(ci_noiseA, len(ci_noiseA))
#print(ci_accuracy, len(ci_accuracy))
print(ci_time, len(ci_time))
print(ds_noiseA, len(ds_noiseA))
#print(ds_accuracy, len(ds_accuracy))
print(ds_time, len(ds_time))

#"#D55E00", "#F0E442"
COLOR_CI_Accuracy = "#009E73"
COLOR_CI_Noise = "#009E73"
COLOR_DS_Accuracy = "#D55E00"
COLOR_DS_Noise = "#D55E00"

fig, ax = plt.subplots()
#ax2 = ax.twinx()



#ax2.plot(ci_noiseA, ci_accuracy, 's:',color=COLOR_CI_Accuracy, markersize=35,linewidth=14)
ax.plot(ci_noiseA, ci_time, 'o',color=COLOR_CI_Accuracy, markersize=35)
#ax2.plot(ds_noiseA, ds_accuracy,'s:', color=COLOR_DS_Accuracy, markersize=35,linewidth=14)
ax.plot(ds_noiseA, ds_time, 'o',color=COLOR_DS_Accuracy, markersize=35)

#circle = mlines.Line2D([], [], color='black', marker='o', linestyle='None',
                    #      markersize=35, label='Timesteps')
#square = mlines.Line2D([], [], color='black', marker='s', linestyle='None',
                       #   markersize=35, label='Accuracy')
#ci_patch = mpatches.Patch(color=COLOR_CI_Accuracy, label='cross-inhibition')
#ds_patch = mpatches.Patch(color=COLOR_DS_Accuracy, label='direct-switch')

#ax2.legend(handles=[ci_patch,ds_patch,circle,square],fontsize=38)

#print(timestepquorumrreached/reachedquorum)
#fig, ax1 = plt.subplots()

#typemodall = ['ci','vm']

###df = pd.DataFrame({"range": typemodall,"accuracy":accuracy, "time":dectime})

###print(timestepquorumrreached/reachedquorum)
###fig, ax = plt.subplots()
###ax = df['time'].plot(kind="bar", alpha=0.7,color=['C0', 'C6', 'C2', 'C3', 'C4'])

###ax2 = ax.twinx()
##ax2.plot(ax2.get_xticks(),df['accuracy'],marker='o', c='navy', linewidth=4)
##ax.set_xticklabels(df['range'], fontsize=45)
#ax2.tick_params(labelsize=38)


##ax1 = fig.add_subplot(111) # Create matplotlib axes
##ind = np.arange(N)  # the x locations for the groups
##width = 0.27       # the width of the bars


##ax1.bar(x-0.2, accuracy, width=0.1, color='b', align='center')
##ax2.bar(x, dectime, width=0.1, color='g', align='center')

##ax1.set_xticklabels( ('ci', 'vm') )
#plt.plot([n for n in enumerate(thetotaltimevalsB)], thetotaltimevalsB, 'b-', linewidth=8)
#ax.set_ylim([0, 140000])
#ax2.set_ylim([0, 1])

ax.tick_params(labelsize=60)
ax.tick_params(labelsize=60)
#ax2.tick_params(labelsize=50)

ax.set_xlabel(r'swarm size' ' $N$', fontsize=86)
#ax2.set_ylabel(r'Cohesion', fontsize=66)
ax.set_ylabel(r'Timesteps', fontsize=86)
#plt.savefig('/Volumes/My_Passport/argosim2/Runs/journal/images/t1_fig5g.pdf', dpi=300, bbox_inches='tight')

plt.show()
