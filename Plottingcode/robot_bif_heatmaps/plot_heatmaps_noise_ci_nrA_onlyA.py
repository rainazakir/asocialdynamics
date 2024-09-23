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
plt.ylim(-1, 1)
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

opdir= '/Volumes/My_Passport/argosim2/Runs/journal/data/an_ds_qr0.82_varynrA/'
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
for file1 in sorted(data_files):
    if file1.endswith(".txt"):

        print(file1.split('_')[3])
        # print(float(file1[40:44]) * 200)
        noise = float(int(file1.split('_')[3])/100)
        #noise = float(file1[20:24])
   #     noise = float(file1[49:53])
        print("The Noise is: ", noise)
       # print("The Z+ is: ", Z)

        # toadd=int(file1[40:42])*0
        with open(opdir + file1) as f:
            for line in f:
                line.strip()  # Removes \n and spaces on the end
                #print(line.split())
                    # mysum += float(line.split()[2])
                    # if(line.split()[2] > 100
               # if line.split()[5] in op1:
                #        print("number in array")
               # else:
                        #op1.append((int(float(line.split()[5]))-int(float(line.split()[6])))/100)
                dump_list_x_points.append(noise)
                dump_list_y_points.append((int(float(line.split()[5]))-int(float(line.split()[6])))/100)
                ##dump_list_x_points.append(noise)
                ##dump_list_y_points.append((int(float(line.split()[6]))-int(float(line.split()[5])))/100)
                    # op2.append(int(line.split()[3]))

                # break
            #print(op1)
            ######plt.hist(op1, bins=50)

            # print(pointxaxis)
            # print(pointyaxis)
            #print("Lenngth od Op1:", len(op1))
  #          for i in range(min(op1), max(op1)):
   #             percen = op1.count(i)

    #            if (percen != 0):
     #               pointxaxis.append(((i)) / (N))
                    #pointxaxis.append(((i) - (N - (i))) / (N))
    #                pointyaxis.append((percen / len(op1)) * 1)
    #        patch.append(mlines.Line2D([], [], linewidth=6,color=colours[xx], marker=symbols[xx], markersize=15, label=str((noise))))
           # plt.plot(pointxaxis, pointyaxis, '-', markersize=15, alpha=.8, color=colours[xx])
    #        plt.hist(pointxaxis, bins= 10)

            #plt.plot(pointxaxis, pointyaxis, symbols[xx], markersize=20, alpha=.8, color=colours[xx])
            xx = xx + 1
            # poly = np.polyfit(pointxaxis,pointyaxis,5)
            # poly_y = np.poly1d(poly)(pointxaxis)
            # plt.plot(pointxaxis,poly_y, linewidth=2)
            # print(pointxaxis)
            # print(pointyaxis)
            # plt.plot(pointxaxis, smooth(pointyaxis,10), lw=1)
            # poly = np.polyfit(pointxaxis, pointyaxis, 6)
            # poly_y = np.poly1d(poly)(pointxaxis)
            # plt.plot(pointxaxis, poly_y, linewidth=2)
            # plt.plot(list_x,list_y)
            ###xarray = np.asarray(pointxaxis, dtype=np.float32)
            ###yarray = np.asarray(pointyaxis, dtype=np.float32)
            ###xnew = np.linspace(xarray.min(), xarray.max(), 6)
            ###@spl = make_interp_spline(xarray, yarray, k=3)  # type: BSpline
            ###power_smooth = spl(xnew)
            ###plt.plot(xnew,power_smooth)

            pointxaxis = []
            pointyaxis = []
            op1 = []
            op2 = []
            # print(line.split()[2])
            # mysum = mysum/100
            # Y.append(mysum)
            # Y1.append(100-mysum)
            # print(str(mysum)+","+ str(100-mysum))
            mysum = 0

# Y.append(100)
# Y1.append(0)

# plt.show()
plt.hist2d(dump_list_x_points, dump_list_y_points, bins=[9,57], cmap='Reds',norm=M.colors.LogNorm())

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
    for root, dirs, files in os.walk('/Volumes/My_Passport/argosim2/Runs/journal/data/an_bif_ds_varynrA_0.82/'):
        for file in files:
            print(files)
            with open(os.path.join(root, file), "r") as auto:
                print(auto)
                lines = list(line for line in (l.strip() for l in auto) if line)

                for line in lines:
                    print(line)
                    print(line.split())
                    if(float(line.split()[4])<1.1):
                    # if(int(line.split()[0])<3000)
                    #   print("comes to second loop here")
                        x.append(float(line.split()[4]))
                        a.append((float(line.split()[0]) + float(line.split()[2]))-(float(line.split()[1]) + float(line.split()[3])))
                        b.append((float(line.split()[1]) + float(line.split()[3])) - (
                                float(line.split()[0]) + float(line.split()[2])))

                    #b.append(int(line.split()[3]) + int(line.split()[5]))
                    #un.append(int(line.split()[1]))
                # plt.figure(xx)
                if(file.split('_')[7]=='2.txt' or file.split('_')[7]=='2.txt'): # 1 and 3
                    plt.plot(x, a, 'limegreen', alpha=1, linewidth=24)
                    #plt.plot(x, b, 'limegreen', alpha=1, linewidth=24)

                else:
                    plt.plot(x, a, 'b', alpha=1, linewidth=14)
                    #plt.plot(x, b, '#F9D576', alpha=1, linewidth=14)

                #plt.plot(x, b, 'b', alpha=0.7, linewidth=5)
                #plt.plot(x, un, 'k', alpha=0.7)
                x = []
                a = []
                b = []
                un = []

                xx += 1
#cbar = plt.colorbar(ticks=[1, 10, 100, 1000, 10000, 20000],orientation='horizontal',aspect=20)#20000
# t.set_fontsize(29)

#cbar.ax.tick_params(labelsize=45)
#ticks= [i for i in cbar.get_ticks()]
# ticks.append(18000)#
#ticks = ['{:.1e}'.format(i / 20000) for i in cbar.get_ticks()]

# ticks.append('0.5')
#print(ticks)

#cbar= plt.colorbar(orientation='horizontal')
#cbar.ax.set_yticklabels(ticks, rotation=-90)  # set ticks of your format for t in cbar.ax.get_yticklabels():
#cbar.ax.set_position((0, 0, 0.5, 0.6))
# Z = 180
# Zplus = Z // 2
# Zminus = Z // 2
# S = N - Zplus - Zminus
# n = S//2
# nmax = N-Z
plt.ylim(-1, 1)
plt.xticks(fontsize=56)#51,51
plt.yticks(fontsize=56)

plt.ylabel(r'population $A-B$', fontsize=64)#60,60
plt.xlabel(r'self-sourcing' ' $\u03B7$r', fontsize=64)
#plt.title('Noise SPD CI Model 550 runs', fontsize=32)
#legend1 = plt.legend(handles=patch, title='Noise', fontsize=32)
#plt.setp(legend1.get_title(), fontsize=32)
###########plt.savefig('/Volumes/My_Passport/argosim2/Runs/journal/images/an_rob_bif_heatmaps_qr1.5_0.925_varynoise_ds_ONLYA.pdf', dpi=300, bbox_inches='tight')

    # plt.plot(axis, pointyaxis)
#legend1 = plt.legend(['0.1', '0.2', '0.3', '0.5', '0.8', '0.9'], title='Zealot Proportion', fontsize=32)
#plt.setp(legend1.get_title(), fontsize=32)
#plt.savefig('images/2308_22_densityp1.pdf', dpi=800, bbox_inches='tight')
plt.show()

