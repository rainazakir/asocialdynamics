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


# data directory
opdir= '/Volumes/My_Passport/argosim2/Runs/journal/data/an_ds_qr0.66_varynrA/'
data_files = []
data_files += [file for file in os.listdir(opdir)]

N = 100
xx = 0


x = []
a = []
b = []
xx = 0

#plotting bifurcations
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

                        x.append(float(line.split()[4]))
                        a.append(((float(line.split()[0]) + float(line.split()[2]))))
                        b.append(((float(line.split()[1]) + float(line.split()[3]))))

                if(file.split('_')[4]=='1.txt' or file.split('_')[4]=='1.txt'):
                    plt.plot(x, a, 'limegreen', alpha=1, linewidth=24)
                    plt.plot(x, b, 'limegreen', alpha=1, linewidth=24)

                else:
                    plt.plot(x, a, 'b', alpha=1, linewidth=24)
                    plt.plot(x, b, '#F9D576', alpha=1, linewidth=24)

                x = []
                a = []
                b = []
                un = []

                xx += 1

plt.ylim(0, 1)
plt.xticks(fontsize=56)
plt.yticks(fontsize=56)

plt.ylabel(r'population $A-B$, $B-A$', fontsize=64)#60,60
plt.xlabel(r'' ' $q$', fontsize=64)

plt.savefig('/Volumes/My_Passport/argosim2/Runs/journal/images/an_rob_bif_heatmaps_n0.05_0.05_varyq_ds.pdf', dpi=300, bbox_inches='tight')

plt.show()


