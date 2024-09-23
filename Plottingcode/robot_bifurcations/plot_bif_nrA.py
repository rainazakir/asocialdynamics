import matplotlib.pyplot as plt
import glob, os
from pathlib import Path
import pathlib
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
# from scipy.interpolate import make_interp_spline, BSpline
import matplotlib.lines as mlines
import matplotlib as M
from matplotlib.colors import from_levels_and_colors
from matplotlib import cm as CM
plt.rcParams["figure.figsize"] = (25, 18)


def smooth(y, box_pts):
    box = np.ones(box_pts) / box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


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
#plt.ylim(-1, 1)
#plt.ylim(0, 0.04)
listFiles = []
x = 0
mysum = 0
pointxaxis = []
patch = []
pointyaxis = []
# to store heatmap data
dump_list_x_points = []
dump_list_y_points = []

withBif = True
# for file in glob.glob("*.txt"):
# listFiles.append(file)
# opdir = 'D:/Simpaperresults/probabilitydistfromGillespieandsim/datafiles/'  # os.getcwd()
#####opdir = 'D:/Simpaperresults/DMVDGillespie/data1.05/VaryingZealots/'
# opdir = 'C:/Users/raina/Desktop/Runs/RunsVZ1.5/'
# opdir= 'D:/Simpaperresults/probabilitydistfromGillespieandsim/datafiles_dmvd_varyZ/'

#opdir = '/Users/rzakir/Documents/fromasus/probabilitydistfromGillespieandsim/datafiles_dmvd_varyZqr2/'
#opdir= '/Users/rzakir/Documents/fromasus/probabilitydistfromGillespieandsim/datafiles_dmvd_varyZ/'
#opdir= '/Users/rzakir/Documents/fromasus/probabilitydistfromGillespieandsim/datafiles_dmvd_varyZ/'

opdir= '/Volumes/My_Passport/argosim2/Runs/journal/data/an_ds_qr0.66_varynrA/'
data_files = []
data_files += [file for file in os.listdir(opdir)]

# files1 = Path().cwd().glob("**/*.txt")
# for f in files1:
#    nm=pathlib.Path(*f.parts[8:])
#    listFiles.append(str(nm))
# print(listFiles)
# listFiles= ["statistics_39972450.txt", "statistics_197411160.txt", "statistics_870119300.txt"]
# print(data_files)
N = 100
xx = 0

#plt.hist2d(dump_list_x_points, dump_list_y_points, bins=[10,22], cmap='bwr', vmin=-1, vmax=1)
#24,33

#plt.pcolormesh(xedges, yedges, Z, cmap='seismic', norm=M.colors.LogNorm(),vmin=-1, vmax=1)
#plt.pcolormesh(xedges, yedges, Z, cmap=CM.RdBu_r, vmin=-1, vmax=1)
#plt.colorbar()

x = []
a = []
b = []
xx = 0
if withBif:
    for root, dirs, files in os.walk('/Volumes/My_Passport/argosim2/Runs/journal/data/dbifnr_0.05ds/'):
        for file in files:
            print(file.split('_'))
            with open(os.path.join(root, file), "r") as auto:
                print(auto)
                lines = list(line for line in (l.strip() for l in auto) if line)

                for line in lines:
                    print(line)
                    print(line.split())
                    if(float(line.split()[4])<1.1 and float(line.split()[4])>0):
                    # if(int(line.split()[0])<3000)
                    #   print("comes to second loop here")
                        #x.append(float(line.split()[4]))
                        #a.append((float(line.split()[0]) + float(line.split()[2]))-(float(line.split()[1]) + float(line.split()[3])))
                        #b.append((float(line.split()[1]) + float(line.split()[3])) - (
                              #  float(line.split()[0]) + float(line.split()[2])))
                        x.append(float(line.split()[4]))
                        a.append(((float(line.split()[0]) + float(line.split()[2]))))
                        b.append(((float(line.split()[1]) + float(line.split()[3]))))
                    #b.append(int(line.split()[3]) + int(line.split()[5]))
                    #un.append(int(line.split()[1]))
                # plt.figure(xx)
                if(file.split('_')[4]=='1.txt' or file.split('_')[4]=='1.txt'):
                    plt.plot(x, a, 'limegreen', alpha=1, linewidth=24)
                    plt.plot(x, b, 'limegreen', alpha=1, linewidth=24)

                else:
                    plt.plot(x, a, 'b', alpha=1, linewidth=24)
                    plt.plot(x, b, '#F9D576', alpha=1, linewidth=24)

                #plt.plot(x, b, 'b', alpha=0.7, linewidth=5)
                #plt.plot(x, un, 'k', alpha=0.7)
                x = []
                a = []
                b = []
                un = []

                xx += 1
#cbar = plt.colorbar(ticks=[1, 10, 100, 1000, 10000, 20000])#20000
# t.set_fontsize(29)
#for l in cbar.ax.get_yticklabels():
 #   l.set_fontsize(58)#42

# ticks= [i for i in cbar.get_ticks()]
# ticks.append(18000)#
#ticks = ['{:.1e}'.format(i / 20000) for i in cbar.get_ticks()]

# ticks.append('0.5')
#print(ticks)

# cbar= plt.colorbar(orientation='horizontal')
#cbar.ax.set_yticklabels(ticks, rotation=-90)  # set ticks of your format for t in cbar.ax.get_yticklabels():
#cbar.ax.set_position((1, 3, 0.5, 0.6))
# Z = 180
# Zplus = Z // 2
# Zminus = Z // 2
# S = N - Zplus - Zminus
# n = S//2
# nmax = N-Z
plt.ylim(0, 1)
plt.xticks(fontsize=56)#51,51
plt.yticks(fontsize=56)

plt.ylabel(r'population $A-B$, $B-A$', fontsize=64)#60,60
plt.xlabel(r'' ' $q$', fontsize=64)
#plt.title('Noise SPD CI Model 550 runs', fontsize=32)
#legend1 = plt.legend(handles=patch, title='Noise', fontsize=32)
#plt.setp(legend1.get_title(), fontsize=32)
plt.savefig('/Volumes/My_Passport/argosim2/Runs/journal/images/an_rob_bif_heatmaps_n0.05_0.05_varyq_ds.pdf', dpi=300, bbox_inches='tight')

    # plt.plot(axis, pointyaxis)
#legend1 = plt.legend(['0.1', '0.2', '0.3', '0.5', '0.8', '0.9'], title='Zealot Proportion', fontsize=32)
#plt.setp(legend1.get_title(), fontsize=32)
#plt.savefig('images/2308_22_densityp1.pdf', dpi=800, bbox_inches='tight')
plt.show()

