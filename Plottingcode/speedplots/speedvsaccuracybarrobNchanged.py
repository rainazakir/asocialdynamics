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
opdir='/Volumes/My_Passport/240423_journal_speedN/selected1.08/'

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
typemodallN = []

#for filenum in range(NumofFiles-1):

thetotaltimevalsA = [0]*100001
thetotaltimevalsB = [0]*100001
filesnum  = 0
findnoise = '0.0noise'
findqr = '[1.08, 1]1.0'
findstdv = 'stdDv-1'
swarmcom= 'swarm_comp_'
tuconf='1000'
vmconf='0000'

#swarmcom= 'swarm_comp_[0.96,0.04]_mdl'
#type-swarm_comp_[0.01,0.99]_mdl-[direct,direct]_rle-[majority,minority]_qvl-[1,1]_op-2_stdDv-1_agt-200_agtRad-0.2
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
       # print(name.split('_')[3].split('n')[0])
        print(name.split('_')[7])
        typemod = name.split('_')[1]
        #print(typemod)
        quorum = float(name.split('_')[7].split(']')[1])
        noise = float(name.split('_')[3].split('n')[0])
        N = float(name.split('_')[6].split('a')[0])
        print(quorum,N,quorum*N,typemod, noise)
        #qr = float(name.split('_')[7])
       # print(noise,qr)
        #quorum = 0.8 * (norm*100)
        #print(name.split('_'))
        #name.split('_')[3] == str(findnoise) and
        if(name.split('_')[3] == str(findnoise) and name.split('_')[7] == str(findqr) and (N == 50 or N ==200 or N==400)):
           # if(name.split('-')[2] == findfolder and name.split('-')[1] == swarmcom ):
                print("The chosen is",name)
                reachedquorum = 0
                typemodall.append(typemod)
                for file in sorted(os.listdir(os.path.join(subdir, name))):
                #for file in os.path.join(subdir, name):
                    #print(file)
                    if file.startswith("evo"):  # ci_te3300td1300_   ci_te3300td1300_highcomm0.5forcoord_42_exp_Quality_50_50_200k_100_N_2_Noise_0.05_UncommT_0000_COORD_0
                        if file.endswith(".txt"):  # _0000_COORD_0.txt
                            with open(os.path.join(subdir,name, file)) as f:
                              #  print("The files2 is", file)
                                filesnum += 1
                                for i, line in enumerate(f):
                                    #print(line)
                                    # #print(line.split())
                                        if(typemod == 'ci'):
                                           # print(((int(line.split()[2]) + int(line.split()[4]))),
                                             #    ((int(line.split()[3]) + int(line.split()[5]))))

                                            if(((int(line.split()[2])+int(line.split()[4]))>=(N*quorum))): #or ((int(line.split()[3])+int(line.split()[5]))>=(N*quorum))):
                                                      #  print(line)
                                                        timestepquorumrreached = timestepquorumrreached + float(line.split()[0])
                                                        timestepquorumrreachedconverged = timestepquorumrreachedconverged + float(line.split()[0])

                                                        timestepsstd.append(float(line.split()[0]))

                                                        reachedquorum +=1
                                                        xx = 0
                                                        check = 0
                                            else:
                                                timestepquorumrreached = timestepquorumrreached + 100000
                                                #timestepquorumrreachedconverged = 0
                                        else:
                                            if(int(int(line.split()[1])+int(line.split()[3]))>=(N*quorum)): #or int(int(line.split()[2])+int(line.split()[4]))>=(N*quorum)):
                                                      #  print(line)
                                                        timestepquorumrreached = timestepquorumrreached + float(line.split()[0])
                                                        timestepquorumrreachedconverged = timestepquorumrreachedconverged + float(line.split()[0])
                                                        timestepsstd.append(float(line.split()[0]))
                                                        reachedquorum +=1
                                                        break
                                                        #print("comes here to check")
                                                        xx = 0
                                                        check = 0
                                            else:
                                                timestepquorumrreached = timestepquorumrreached + 100000

                                                #timestepquorumrreachedconverged = 0


                            # timestepquorumrreached = 50000
                print("stats: ",filesnum, reachedquorum)
                normcomp_xaxis.append((noise))
                accuracy.append(reachedquorum/filesnum)
                typemodallN.append(N)
                #dectime.append(timestepquorumrreached/ filesnum)
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


print(normcomp_xaxis, len(normcomp_xaxis))
print(accuracy, len(accuracy))#dectime
print(dectime, len(dectime))#dectime
print(typemodallN, len(typemodallN))#dectime
print(stddec, len(stddec))
#print(timestepquorumrreached/reachedquorum)
#fig, ax1 = plt.subplots()

#typemodall = ['ci','vm']

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
#test_df = df.set_index('time').T
#print(test_df)

#test_df.plot(kind='bar', rot=0)


#print(timestepquorumrreached/reachedquorum)
#ax = df['time'].plot(kind="bar", color=['tab:blue','tab:pink'], alpha=1)

#ax2 = ax.twinx()
#ax2.plot(ax2.get_xticks(),df['accuracy'],marker='o', c='navy', markersize=20, linewidth=14)
#ax.set_xticklabels(df['range'], fontsize=45)
#ax2.tick_params(labelsize=38)


##ax1 = fig.add_subplot(111) # Create matplotlib axes
##ind = np.arange(N)  # the x locations for the groups
##width = 0.27       # the width of the bars


##ax1.bar(x-0.2, accuracy, width=0.1, color='b', align='center')
##ax2.bar(x, dectime, width=0.1, color='g', align='center')

##ax1.set_xticklabels( ('ci', 'vm') )
#plt.plot([n for n in enumerate(thetotaltimevalsB)], thetotaltimevalsB, 'b-', linewidth=8)
#ax.set_ylim([0, 6000])
#ax2.set_ylim([0, 1])

ax.tick_params(labelsize=50)
ax.tick_params(labelsize=50)
#ax2.tick_params(labelsize=50)
ax.legend(fontsize=45) # using a size in points
#ax.set_xlabel(r'model', fontsize=66)
#ax2.set_ylabel(r'Accuracy', fontsize=66)
ax.set_ylabel(r'Timesteps', fontsize=66)

#plt.savefig('/Volumes/My_Passport/argosim2/Runs/journal/images/dec_cahnged_newNspeed_n0.00_speed_qr1.08_1.pdf', dpi=300, bbox_inches='tight')

plt.show()
        #print(pos)
        #G = nx.random_geometric_graph(100, 0.2, pos=pos)
   # nx.draw(G, pos=pos, with_labels=False, font_size=8,node_size=1000,node_color=node_color)#print(len(probofsameA), len(probofsameB))
#plt.bar(range(len(probofsameA)), list(probofsameA.values()), align='center')
#Plt.xticks(range(len(probofsameA)), list(probofsameA.keys()))
#lists
#val = list(probofsameB.values())
#keysd =list(probofsameB.keys())
