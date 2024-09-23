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
# the combined matrix for all runs of each zealot proportion)  =====#
#opdir = 'D:/Pycharm/PycharmProjects/Eq10MobiliaPRE/cdcigillnewmatrix/check/modified105/'
##opdir = 'D:/Pycharm/PycharmProjects/Eq10MobiliaPRE/cdcigillnewmatrix/selectedspdfilesforcdci/qr105/'
opdir = '/Users/raina/Documents/fromasus/2022/Eq10MobiliaPRE/cdcigillnewmatrix/check/modified1/'
#opdir = 'D:/Pycharm/PycharmProjects/Eq10MobiliaPRE/dmvdgillnewmatrix/selectedspdfilesfordmvd/qr105/'
opdir = '/Users/raina/Documents/fromasus/2022/Eq10MobiliaPRE/cdcigillnewmatrix/noise/modifiednoise2/'
#opdir = '/Users/raina/Documents/fromasus/2022/Eq10MobiliaPRE/cdcigillnewmatrix/noise/selectednoise2/'
opdir = '/Volumes/My_Passport/060423_gilltest/gillespienoise/matrix/'
opdir = '/Volumes/My_Passport/argosim2/Runs/getoutputfile/nfilesphytypeB/'
opdir = '/Volumes/My_Passport/argosim2/Runs/journal/data/cispd_qr1.22/'
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
####Zproportion = [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.3,0.31,0.32,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.5,0.51,0.52,0.53,0.54,0.55,0.56,0.57,0.58,0.59,0.6,0.61,0.62,0.63,0.64,0.65,0.66,0.67,0.68,0.69,0.7,0.71,0.72,0.73,0.74,0.75,0.76,0.77,0.78,0.79,0.8,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99]
# print(len(Zproportion))

##Specify the total number of agents
# ==============================#

# colour blind friendly scheme for SPd plots  ///add more if needed
colours = ["#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#999999", "#E69F00","#2271B2","#f0e442","#d65e00"]
#colours = ["#000000","#3DB7E9", "#F748A5", "#359B73","#e69f00","#2271B2","#f0e442","#d55e00"]
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
    #if(file1.split('_')[5]=='1.0noisetype' and  file1.split('_')[6]==  'TypeBnoise'):
        with open(opdir + file1) as f:
            print("file", f)

            spd = json.load(f)  # load the spd matrix from the file
           # print((spd))

            print((file1.split('_')))
            num = int(((file1.split('_'))[5]).split('a')[0])

            #        zealot = int(file1[12:14]) + int(file1[12:14])  # get no of zealots in file from file name
            zealot = float(((file1.split('_'))[2]).split('n')[0])
            ##  zealot = Zproportion[0] # for noise
            print(zealot, num)
            # zealot = int(file1[14:20]) # for noise

            # print(zealot, (float(zealot/ N)))
            N.append(int(num))  # save zealot files in list- to be used for heatmap plotting

            Zproportion.append(float(zealot))  # save zealot files in list- to be used for heatmap plotting

            ########print("zealot", zealot/N)
            ########print(np.array(spd).shape)
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
                   ## OldRange = (-num - num)
                   ## NewRange = (-100 - 100)
                   ## NewValue = (((number - -num) * NewRange) / OldRange) + -100
                    #print(number, int(NewValue))

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
           # if (num == 19):
              #  num = 20
            #plt.xlim(-1, 1)
            #plt.ylim(0, 0.175)
            y = zero_to_nan(y)
            d = {'xax': x, 'yax': y}
            newdf = pd.DataFrame(data=d)
            #plt.plot(newdf['yax'].dropna(),'-*', color=colours[xx], markersize=24,linewidth=4)
            #s1 = pd.Series(y, index=x)
            #plt.plot(*splitSerToArr(s1.dropna()), linestyle='-', marker='o')
            plt.plot([a / 100 for a in x], y, '-*', color=colours[xx], markersize=24,linewidth=4)
            #plt.plot([a / 100 for a in x], y, '-', color=colours[xx], linewidth=12)
            patch.append(mlines.Line2D([], [], color=colours[xx], linewidth=17, label=str(Zproportion[xx])))  # legend
            # plt.plot(listx, listy, '*', markersize=12, color=colours[xx])

        # reset variables for next zealot value
        listx_y = []
        spd = []
        x = []
        y = []
        result = []

        xx = xx + 1
    # plt.hist2d(dump_list_x_points, dump_list_y_points, bins=[99, 36], cmap='Reds', norm=M.colors.LogNorm())
    # plt.imshow(pbavg, cmap='Reds', norm=M.colors.LogNorm(), aspect='auto')

if showDebugMatrix:
    print(Zproportion)

if heatmaps:
    # for i in heatMatrix:
    # print("yhis line",i)
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
#linthresh="0.0001"--> for cdci  #    plt.imshow(heatMatrixFull, cmap='Reds', norm=M.colors.SymLogNorm(linthresh="0.00000001"), aspect='auto')

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
                        ###without formatting:
                        ###bix.append(float(line1.split()[0]))
                        ###bix.append(float(line1.split()[1]))
                        plt.plot(bix, biy, linewidth=14, linestyle='dashed', color="royalblue")
                        # plt.axhline(y=200,linewidth=14, linestyle='dashed', color="royalblue",zorder=1)
                        # plt.plot(bix,biy,linewidth=14, color=[0.0, 01.0, 0.0])

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
    # plt.title("GILLESPIE HEATMAP QRatio-2, CDCI, N=200", fontsize=32)
    #plt.xlabel(r'asocial behavior $z_x+z_y$', fontsize=48)
    plt.xlabel(r'swarm size $S$', fontsize=62)

   ## plt.xlabel(r'asocial behavior $z_x+z_y$', fontsize=62)
  ##  plt.ylabel(r'population $X-Y$', fontsize=62)
    ax = plt.gca()
    ax.margins(0)
    xfmt = tkr.FuncFormatter(numfmt)  # create your custom formatter function
    yfmt = tkr.FuncFormatter(numfmty)
    plt.gca().xaxis.set_major_formatter(xfmt)
    plt.gca().yaxis.set_major_formatter(yfmt)

if not heatmaps:
    # plt.title("GILLESPIE EQ QRatio-2, CDCI, N=200", fontsize=32)
    plt.xlabel(r'population $A-B$', fontsize=68)#62

    #plt.ylabel(r'spd', fontsize=62)
   # plt.xlabel(r'swarm size $S$', fontsize=62)
   # legend1 = plt.legend(handles=patch, title=r'noise''\n''type 1', fontsize=48)#44

    legend1 = plt.legend(handles=patch, title=r'self-sourced''\n' ' noise $\u03B7$', fontsize=48)#44
    plt.setp(legend1.get_title(), fontsize=68)#62
    # axis range
    #plt.xlim(-1, 1)
    plt.ylim(0, 255000)
    plt.ylim(0, 120000)

    #plt.yticks([])
    ax = plt.gca()  # grab the current axis
    #ax.set_yticks([0.00,0.01,0.02,0.03,0.04])  # choose which x locations to have ticks

plt.xticks(fontsize=50)#44
plt.yticks(fontsize=50)#44

plt.savefig('/Volumes/My_Passport/argosim2/Runs/journal/images/NEW_JUN2024_SPD_gill_ci_qr1_1.pdf', dpi=300, bbox_inches='tight')
plt.show()
