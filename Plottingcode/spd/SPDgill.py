# checking program
import math
import pandas as pd
from functools import reduce
import matplotlib.pyplot as plt
import glob, os
import numpy as np
import matplotlib.lines as mlines
import matplotlib as M
import json
import matplotlib.ticker as tkr  # has classes for tick-locating and -formatting
# for cdci Gillespie--> noise type 2 Heatmaps and SPD, cdci zealots heatmaps and SPD
plt.rcParams["figure.figsize"] = (25, 18)

# ==If plotting heatmaps set to true otherwise false will generate SPD==#
heatmaps = False
# ==If plotting heatmaps set to true and want bifurcation lines==#
withBif = False
# =============================#

# ==== specify the directory to get the matrix files from (each file should only have
# the combined matrix for all runs of each noise)  =====#

opdir = '/Volumes/My_Passport/argosim2/Runs/journal/data/cispd_qr1/'

# =========DIRECTORIES FOR bifurcation data -if withBif set to true=========#
opdir_bifurcation = '/Users/raina/Documents/fromasus/2022/Eq10MobiliaPRE/bifurcationlines/N2/'  # os.gtcwd()

# ============================================================#
ra = 2


"""
#NOTE: the format of spd files in opdir have to be 'outputofspd_05zealots.txt', 'outputofspd_20zealots.txt' etc
#otherwise alter line61 to read zealot value for file name or enable Zproportion commented below
"""
Zproportion = []  # used for heatmap plotting, if specifying manually them comment out
N = []


##Specify the total number of agents
# ==============================#

# colour blind friendly scheme for SPd plots  ///add more if needed
colours = ["#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#999999", "#E69F00","#2271B2","#f0e442","#d65e00"]
xx = 0  # to iterate colours and symbols

heatMatrix = []  # to store the matrix for heatmaps

patch = []  # to store legend values for SPD plot
data_files = []  # to store list of files to iterate (teh files are same for heatmap and spd
data_files += [file for file in sorted(os.listdir(opdir))]
print(data_files)

# array to load bifurcation files
data_files_bif = []

dx = 0  # to keep count of files-- number of files == number of Susceptibles for gillespie

showDebugMatrix = False

# to store bifurcation points to plot
bix = []
biy = []


def zero_to_nan(values):
    """Replace every 0 with 'nan' and return a copy."""
    return [float('nan') if x<0.0000001 else x for x in values]

def numfmt(x, pos):  # your custom formatter function: divide by 100.0
    s = '{}'.format(x * 20)
    return s


def numfmty(y, pos):  # your custom formatter function: divide by 100.0
    s = '{}'.format(-1.00 * ((y - 100) / 100) + 0)
    return s


def splitSerToArr(ser):
    return [ser.index, ser.as_matrix()]


def increaseSize(lst, N):
    return reduce(lambda x, y: x + y, [[el] * N for el in lst])

######################===################

for file1 in sorted(data_files):
        print(file1.split('_'))
        with open(opdir + file1) as f:
            print("file", f)

            spd = json.load(f)  # load the spd matrix from the file

            print((file1.split('_')))
            num = int(((file1.split('_'))[5]).split('a')[0])

            zealot = float(((file1.split('_'))[2]).split('n')[0])
            ##  zealot = Zproportion[0] # for noise
            print(zealot, num)

            N.append(int(num))  # save zealot files in list- to be used for heatmap plotting

            Zproportion.append(float(zealot))  # save zealot files in list- to be used for heatmap plotting

            if showDebugMatrix:
                plt.imshow(spd, cmap='hot', interpolation='nearest')
                plt.colorbar()
                plt.show()
                # exit()
            pbavg = {}
            # iterate through the spd matrix
            for a in range(len(spd)):
                for b in range((len(spd))):
                    NewValue = (a - b)  # points in x axis

                    if pbavg.get(int(NewValue)) is not None:
                        # print("there is already a number in this index")
                        pbavg[int(NewValue)] = pbavg.get(int(NewValue)) + (spd[a][b])  # points in y axis (probability / number of runs that generated the matrix)
                    else:
                        # print("this is the first number for this difference")
                        pbavg[int(NewValue)] = (spd[a][b])
            for d, v in pbavg.items():
                pbavg[d] = v / num
            # sort the dictionary containing X points and Y points
            listx_y = sorted(pbavg.items())
            #correspDay = list(range(-100, 101))
            # separate them into lists
            x, y = zip(*listx_y)
           # fee_dict = dict(zip(x, fees))
            result = []
            #x = [i / 100 for i in x]
            print(len(x),x)
            print(len(y),y)
            print(y[120],y[110],y[125],y[150])


            print(dx)
            print(num)
            line = [0] * (100*2 + 1)
            if heatmaps:
                heatMatrix.append(line)
                for x, y in listx_y:
                        #print(x, y)
                    heatMatrix[dx][x + 100] = y
        dx += 1

        if not heatmaps:  # plot spd

            y = zero_to_nan(y)
            d = {'xax': x, 'yax': y}
            newdf = pd.DataFrame(data=d)

            plt.plot([a / 100 for a in x], y, '-*', color=colours[xx], markersize=24,linewidth=4)
            patch.append(mlines.Line2D([], [], color=colours[xx], linewidth=17, label=str(Zproportion[xx])))  # legend

        # reset variables for next zealot value
        listx_y = []
        spd = []
        x = []
        y = []
        result = []

        xx = xx + 1


if showDebugMatrix:
    print(Zproportion)

if heatmaps:

    heatMatrixFull = []
    for z in np.arange(0, 400, 10):
        found = False
        for zi, zVal in enumerate(N):
            if np.abs(zVal - z) < 0.0001:
                print(zi, zVal)
                print(heatMatrix[zi])
                heatMatrixFull.append(heatMatrix[zi])
                found = True
                break
        if not found:
            #heatMatrixFull.append([0] * (200 * 2 + 1)) #ENABEL FOR ZEALOT CDCI
            print("On the x-axis the value " + str(z) + " has not been found.")
    heatMatrixFull = list(reversed(list(zip(*heatMatrixFull))))
    # plot the heatmap
    plt.imshow(heatMatrixFull, cmap='Reds', norm=M.colors.SymLogNorm(linthresh=0.01), aspect='auto')

# plot bifurcations
if withBif:
    data_files_bif += [file1 for file1 in os.listdir(opdir_bifurcation)]  # for adding your i
    name1 = sorted(data_files_bif, reverse=True)
    print(data_files_bif)
    for file1 in data_files_bif:
        print(file1)
        with open(opdir_bifurcation + file1, 'r') as f1:
            if (file1.endswith('.txt')):
                plt.axhline(y=200,linewidth=14, linestyle='dashed', color="royalblue",zorder=1)
                if (file1.endswith('P3.txt')):
                    for line1 in f1:
                        bix.append(float(line1.split()[0]) * 100)
                        biy.append((-1 * (200 * float(line1.split()[1])) + 200))

                        plt.plot(bix, biy, linewidth=14, linestyle='dashed', color="royalblue")


                else:
                    # if ra == 1:
                    print("nothing")
                    # else:
                    for line1 in f1:
                        bix.append(float(line1.split()[0]) * 100)
                        biy.append((-1 * (200 * float(line1.split()[1])) + 200))
                        ###without formatting:
                        ###bix.append(float(line1.split()[0]))
                        ###bix.append(float(line1.split()[1]))
                        plt.plot(bix, biy, linewidth=14, color=[0.0, 01.0, 0.0])
                bix = []
                biy = []

if heatmaps:

    plt.xlabel(r'swarm size $S$', fontsize=62)

    ax = plt.gca()
    ax.margins(0)
    xfmt = tkr.FuncFormatter(numfmt)  # create your custom formatter function
    yfmt = tkr.FuncFormatter(numfmty)
    plt.gca().xaxis.set_major_formatter(xfmt)
    plt.gca().yaxis.set_major_formatter(yfmt)

if not heatmaps:
    plt.xlabel(r'population $A-B$', fontsize=68)#62


    legend1 = plt.legend(handles=patch, title=r'self-sourced''\n' ' noise $\u03B7$', fontsize=48)#44
    plt.setp(legend1.get_title(), fontsize=68)#62
    # axis range
    #plt.xlim(-1, 1)
    plt.ylim(0, 255000)
    plt.ylim(0, 120000)

    #plt.yticks([])
    ax = plt.gca()  # grab the current axis

plt.xticks(fontsize=50)#44
plt.yticks(fontsize=50)#44

plt.savefig('/Volumes/My_Passport/argosim2/Runs/journal/images/NEW_JUN2024_SPD_gill_ci_qr1_1.pdf', dpi=300, bbox_inches='tight')
plt.show()

