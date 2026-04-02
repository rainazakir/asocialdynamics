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
opdir='/Volumes/My_Passport/journal_hmap_newq/ci_1.50'

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
findqr = '[1.0, 1]'
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
popA =0
popB= 0
totpop = 0
filecount = 0
avgval = 0
filesnum = 0
#quorumtocheckfor = "q0.75" #q0.75, 0.66,1-m,2f
for subdir, dirs, files in sorted(os.walk(opdir)):
    for name in sorted(dirs):
        print(name.split('_'))
       # print(name.split('_')[3].split('n')[0])
        #print(name.split('_')[7])
        typemod = name.split('_')[1]
        #print(typemod)
        #quorum = float(name.split('_')[7].split(']')[1])
        ##quorum = 0.75

        noiseA = float(name.split('_')[3].split('n')[0])
        noiseT = float(name.split('_')[7].split(']')[1])
        qr = (name.split('_')[7])
       # print(noise,qr)
        #quorum = 0.8 * (norm*100)
        #print(name.split('_'))
        #name.split('_')[3] == str(findnoise) and
        ##########if(name.split('_')[3] == str(findnoise) and name.split('_')[7] == str(findqr) and (name.split('_')[2] == str(vmconf) or name.split('_')[2] == str(tuconf) ) ):
           # if(name.split('-')[2] == findfolder and name.split('-')[1] == swarmcom ):
               ######### print("The chosen is",name)
        print(N,typemod,noiseA)

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
                                checkQuorum= False
                                for i, line in enumerate(f):
                                    #print(line)
                                    # #print(line.split())
                                        if(typemod == 'ci0.05'):
                                           # print(((int(line.split()[2]) + int(line.split()[4]))),
                                             #    ((int(line.split()[3]) + int(line.split()[5]))))
                                               #if(line.split()[7]==quorumtocheckfor):
                                                 #  checkQuorum = True
                                               if (line.split()[7]=='end'):

                                                           ####### print(line)
                                                                timestepquorumrreached = timestepquorumrreached + float(line.split()[0])
                                                                timestepquorumrreachedconverged = timestepquorumrreachedconverged + float(line.split()[0])
                                                                reachedquorum +=1
                                                                popA =  (int(line.split()[2])+int(line.split()[4]))
                                                                popB =  ((int(line.split()[3])+int(line.split()[5])))
                                                                avgval = avgval  + abs(popA - popB)/N
                                                                break
                                                                xx = 0
                                                                check = 0
                                                               ################## print(file, line)
                                               #else:
                                                 #       timestepquorumrreached = timestepquorumrreached + 100000
                                                        #print(file, line)
                                                        #timestepquorumrreachedconverged = 0
                                        else:
                                            #if(line.split()[6]==quorumtocheckfor):
                                            #    checkQuorum = True
                                                    ######### print(line)
                                            if(line.split()[6]=='end'):
                                                        timestepquorumrreached = timestepquorumrreached + float(line.split()[0])
                                                        timestepquorumrreachedconverged = timestepquorumrreachedconverged + float(line.split()[0])
                                                        reachedquorum +=1
                                                        popA =  (int(line.split()[1]) + int(line.split()[3]))
                                                        popB =  ((int(line.split()[2]) + int(line.split()[4])))
                                                        avgval = avgval  + abs(popA - popB)/N
                                                        break
                                                        #print("comes here to check")
                                                        xx = 0
                                                        check = 0
                                            #else:
                                                    ###0print(file)
                                                   # timestepquorumrreached = timestepquorumrreached + 100000



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
                totpop = (avgval/reachedquorum)

                ci_accuracy.append(totpop)
                ci_time.append(timestepquorumrreachedconverged / reachedquorum)
        else:
           # ds_noiseA.append(noise)
            if (reachedquorum == 0):
                ds_accuracy.append(0)

                ds_time.append(0)
            else:
                totpop = (avgval/reachedquorum)

                ds_accuracy.append(totpop)
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
        totpop = 0
        popB = 0
        popA = 0
        avgval =0
        filesnum=0

fig, ax = plt.subplots()
# ax2 = ax1.twinx()
print(len(yaxis),len(xaxis),len(ci_time))
data = pd.DataFrame({'h': xaxis, 'k': yaxis, 'br': ci_time})
data_pivoted = data.pivot("h", "k", "br")
print(data_pivoted.to_string())

# print(hval)
#ax = sns.heatmap(data_pivoted, annot=False, cmap="viridis")

ax = sns.heatmap(data_pivoted, annot=False, cmap="viridis",vmin=0,vmax=200000)
ax.invert_yaxis()
ax.tick_params(axis='y', rotation=0)
ax.tick_params(labelsize=80)
cax = ax.figure.axes[-1]
cax.tick_params(labelsize=72)
plt.savefig('/Volumes/My_Passport/argosim2/Runs/journal/imageshmap/GABSnoQ_norm_hmap_'+str(typemod)+'_cohTime_q'+str(qr)+'_'+'.pdf', dpi=300, bbox_inches='tight')

plt.show()

                                      #  thetotaltimevalsA[int(line.split()[0])] = thetotaltimevalsA[
                                       #                                               int(line.split()[0])] + int(
                                        #    line.split()[2])
                                        # thetotaltimevalsA.insert(int(line.split()[0]), thetotaltimevalsA[int(line.split()[0])]+int(line.split()[2]))
                                        #thetotaltimevalsB[int(line.split()[0])] = thetotaltimevalsB[
                                                                                 #     int(line.split()[0])] + int(
                                         #   line.split()[3])
                            # print(float(file1[40:44]) * 200)   # print(float(file1[40:44]) * 200)
                               # noise = float(file1[20:25])

                               # print("The Noise is: ", noise)
                               # print("The Z+ is: ", Z)



                                        #G.add_node(xx,pos=[(line.split()[4]),(line.split()[5])])
                                         #   if(line.split()[3] != 0 and line.split()[4]!=0):
                                   #     therealprobdissemA = int(line.split()[3])/(int(line.split()[4])+int(line.split()[3]))
                                  #      therealprobdissemB = int(line.split()[4])/(int(line.split()[4])+int(line.split()[3]))

                                     #   if (therealprobdissemB>therealprobdissemA and (int(line.split()[1])==1 and int(line.split()[1])==1)):
                                     #       xx = xx + 1
                                    #    if (therealprobdissemA>therealprobdissemB and (int(line.split()[1])==2 and int(line.split()[1])==2)):

       ##             if assortivity.get((assort)) is not None:
                ##        assortivity[(assort)] = assortivity.get((assort)) + nx.attribute_assortativity_coefficient(H, "node_color")  # points in y axis (probability / number of runs that generated the matrix)
                  ##  else:
                       # print("this is the first number for this difference")
                    ###    assortivity[assort] = nx.attribute_assortativity_coefficient(H, "node_color")

                    #assortivity.append(nx.attribute_assortativity_coefficient(H, "node_color"))
                    #plt.show()

#plt.ylim(0, 1.05)





#plt.savefig('/Volumes/My_Passport/argosim2/Runs/journal/images/new_speed_cohesion_qr1.5_0.66.pdf', dpi=300, bbox_inches='tight')

#plt.show()

