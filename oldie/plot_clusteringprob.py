import matplotlib.pyplot as plt
import glob, os
from pathlib import Path
import pathlib
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
# from scipy.interpolate import make_interp_spline, BSpline
import matplotlib.lines as mlines

plt.rcParams["figure.figsize"] = (25, 18)


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
plt.ylim(-50, 50)
listFiles = []
x = 0
mysum = 0
pointxaxis = []
patch = []
pointyaxis = []
# for file in glob.glob("*.txt"):
# listFiles.append(file)
# opdir = 'D:/Simpaperresults/probabilitydistfromGillespieandsim/datafiles/'  # os.getcwd()
#####opdir = 'D:/Simpaperresults/DMVDGillespie/data1.05/VaryingZealots/'
# opdir = 'C:/Users/raina/Desktop/Runs/RunsVZ1.5/'
# opdir= 'D:/Simpaperresults/probabilitydistfromGillespieandsim/datafiles_dmvd_varyZ/'

#opdir = '/Users/rzakir/Documents/fromasus/probabilitydistfromGillespieandsim/datafiles_dmvd_varyZqr2/'
#opdir= '/Users/rzakir/Documents/fromasus/probabilitydistfromGillespieandsim/datafiles_dmvd_varyZ/'
#opdir= '/Users/rzakir/Documents/fromasus/probabilitydistfromGillespieandsim/datafiles_dmvd_varyZ/'

##opdir= '/Users/raina/Documents/argosim2/Runs/Plottingspdfile/hist/'
opdir='/Users/raina/Documents/argosim2/Runs/kilogridci/echocoord2/'
opdir='/Volumes/My_Passport/2908_echocoord/'
opdir='/Volumes/My_Passport/191211_robotexppollchng/'

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

       # print(float(file1[40:44]) * 200)
       # noise = float(file1[20:25])

       # print("The Noise is: ", noise)
       # print("The Z+ is: ", Z)
same = {}
diff = {}

probofsame = {}

for subdir, dirs, files in os.walk(opdir):
        for file in files: #ci_te3300td1300_highcomm_17_exp_Quality_50_50_200k_100_N_2_Noise_0.05_UncommT_0000_ECHOC_0.txt
            if file.startswith("ci_te3300td1300_highcomm0.1forechobutevenlongcorrected"):#ci_te3300td1300_lowcomm,ci_te3300td1300_lowcomm0.1forechobutcorrectednorm_45
                #print(file)
                if file.endswith("800_UECHOC_0.txt"): #ci_te3300td1300_lowcomm
                    print(file)
                    for line in open(os.path.join(subdir, file)).readlines():
                        print(file)
                        line.strip()  # Removes \n and spaces on the end
                        if(len(line.split())==5):
                            print(line.split())
                            therealprobdissemA = round(int(line.split()[3])/(int(line.split()[4])+int(line.split()[3]))*100) # the da/da+db
                            therealprobdissemB = round(int(line.split()[4])/(int(line.split()[4])+int(line.split()[3]))*100) #da/da+db
                            thecurrentop = int(line.split()[1])
                            theneighbourop = int(line.split()[2])

                            if (thecurrentop != theneighbourop):
                                    print("there is already a number in this index")
                                    if(thecurrentop == 1):
                                        if diff.get((therealprobdissemA)) is not None:
                                            diff[(therealprobdissemA)] = diff.get((therealprobdissemA)) + 1  # points in y axis (probability / number of runs that generated the matrix)
                                        else:
                                            diff[(therealprobdissemA)] = 1  # points in y axis (probability / number of runs that generated the matrix)
                                    if(thecurrentop == 2):
                                        if diff.get((therealprobdissemB)) is not None:
                                            diff[(therealprobdissemB)] = diff.get((therealprobdissemB)) + 1  # points in y axis (probability / number of runs that generated the matrix)
                                        else:
                                            diff[(therealprobdissemB)] = 1  # points in y axis (probability / number of runs that generated the matrix)                 else:
                            elif(thecurrentop==theneighbourop):
                                if (thecurrentop == 1):
                                    if same.get((therealprobdissemA)) is not None:
                                        print("there is already a number in this index")
                                        same[(therealprobdissemA)] = same.get((therealprobdissemA)) + 1  # points in y axis (probability / number of runs that generated the matrix)
                                    else:
                                        print("this is the first number for this difference")
                                        same[(therealprobdissemA)] = 1
                                if (thecurrentop == 2):
                                    if same.get((therealprobdissemB)) is not None:
                                        same[(therealprobdissemB)] = same.get((therealprobdissemB)) + 1  # points in y axis (probability / number of runs that generated the matrix)
                                    else:
                                        print("this is the first number for this difference")
                                        same[(therealprobdissemB)] = 1

                            #   if(line.split()[3] != 0 and line.split()[4]!=0):
                       #     therealprobdissemA = int(line.split()[3])/(int(line.split()[4])+int(line.split()[3]))
                      #      therealprobdissemB = int(line.split()[4])/(int(line.split()[4])+int(line.split()[3]))

                         #   if (therealprobdissemB>therealprobdissemA and (int(line.split()[1])==1 and int(line.split()[1])==1)):
                         #       xx = xx + 1
                        #    if (therealprobdissemA>therealprobdissemB and (int(line.split()[1])==2 and int(line.split()[1])==2)):
                         #       xx = xx + 1

print(diff)
print(same)

for key in diff.keys() & same.keys():
    print(key)
    print(diff[key]+same[key])
    probofsame[key] = (same[key]/(diff[key]+same[key]))*100
print(probofsame)


keyssAbove = []
keyssBelow = []


valsAbove = []
valsBelow =[]

for key, value in sorted(probofsame.items()): #iterate through actual probability of A and compare it with real prob of A
    if key == 42:
        print(key)

    if (value > key):
        #print("comes here", value, key)
        keyssAbove.append(key)
        valsAbove.append(value-key)
    else:
        #print("comes 2here", value, key)
        keyssBelow.append(key)
        valsBelow.append(value-key)

#plt.scatter(keyss, vals)
#print(len(keyss), len(vals))
print( keyssAbove)
print( keyssBelow)
plt.xlabel(r'Real Probability', fontsize=45)
plt.ylabel(r'Actual Probability', fontsize=45)
# # for python 2.x:
plt.bar(keyssAbove, valsAbove, color = 'red')  # python 2.x
plt.bar(keyssBelow, valsBelow, color = 'blue')  # python 2.x
plt.xticks(fontsize=32)
plt.yticks(fontsize=32)
plt.show()                # else:
