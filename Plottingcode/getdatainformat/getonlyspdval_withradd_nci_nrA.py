import os

opdir='/Volumes/My_Passport/140423_journal_4/'
#noiselist = ['0.00' ,'0.02' ,'0.04' ,'0.06' ,'0.08' ,'0.10' ,'0.12' ,'0.14' ,'0.16' ,'0.18' ,'0.20' ,'0.22' ,'0.24' ,'0.26' ,'0.28' ,'0.30']
#noiselist = ['0.26' ,'0.28' ,'0.30']
#noiselist = ['0.00' ,'0.02' ,'0.04' ,'0.06' ,'0.08' ,'0.10','0.12' ,'0.14']
noiselist = ['00' ,'10' ,'20' ,'30' ,'40' ,'50' ,'60' ,'70' ,'80' ,'90' ,'100']
noiselist2 = ['100' ,'90' ,'80' ,'70' ,'60' ,'50' ,'40' ,'30' ,'20' ,'10' ,'00']

#noiselist = ['0.00','0.01' ,'0.02' ,'0.03' ,'0.04' ,'0.05' ,'0.06' ,'0.07' ,'0.08' ,'0.09' ,'0.10' ,'0.11' ,'0.12' ,'0.13' ,'0.14' ,'0.15' ,'0.16' ,'0.17' ,'0.18' ,'0.19' ,'0.20' ,'0.21' ,'0.22' ,'0.23' ,'0.24' ,'0.25' ,'0.26' ,'0.27' ,'0.28' ,'0.29' ,'0.30']
#outfile = open( "/Volumes/My_Passport/argosim2/Runs/journal/data/vmqr1_varynoise/outfile_cimod_noise_0.02_laststep1000s_uncommtime_1000_quality_50_50_lowcomm0.1.txt", "w")
#outfile = open( "../Plottingspdfile/histnoisepaper1.5/outfile_cimod_qr1.5_uncommtime_2000_antsconfig_noise0.20.txt", "w")
#outfile = open( "../Plottingspdfile/histnoisetypeA1.5/outfile_cimod_qr1.5_uncommtime_2000_antsconfig_noise0.02_typeA.txt", "w")

temp_list = []
xc=0
xcheck = 0
numc = 0
for  nrA in noiselist:
    print(nrA, numc)
    outfile = open(
        "/Volumes/My_Passport/argosim2/Runs/journal/data/an_ds_qr0.925_varynrA/outfile_vmmod_noise_"+str((nrA))+"_laststep1000s_uncommtime_0000_quality_lowcomm0.1.txt",
        "w")

    for subdir, dirs, files in os.walk(opdir):
        for file in files:
    
            # if file.startswith("ci_te330k130k):
             if file.startswith("vm_te3300td1300_highcomm0.1forechob"):
               # print(file)
                #if file.endswith("40_60_dqs__600k_100_N_qs2_Noise_0.05_UncommT_0000_15k_0.txt"):
                  #if file.endswith("Quality_60_40_yqs_typeA__600k_100_N_qs2_Noise_0.02_UncommT_2000_15k_0.txt"):

                if file.endswith("Quality_"+str(nrA)+"_"+str(noiselist2[numc])+"_dqs_an__600k_100_N_qs2_Noise_0.10_UncommT_0000_15k_0.txt"):
              #   if file.endswith("Noise_" + str(noise) + "_UncommT_2000_noqs_0.txt"):
                 #if file.endswith("hyb_allci_100_Quality_55_45_yqs_200k_100_N_2_Noise_0.00_UncommT_2000_15k_0.txt"):
    
                    if (xc<51):
                        xc+=1
                        print(file)
                        touch200= 0
                        for line in open(os.path.join(subdir, file)).readlines():
                              #print(line.split())
                              if (line.split()[0]) != 'time;1':
                                    #print(int(line.split()[0]))
                                    if int(str(line.split()[0])) > 199000:
                                        if (touch200 !=1):
                                            ####print(line.split())
                                            xcheck +=1;
                                            outfile.write(
                                                "1" + "\t" + "1" + "\t" + "1" + "\t" + "1" + "\t" + (line.split()[0]) + "\t" + (
                                                line.split()[1]) + "\t" + (line.split()[2]) + "\t" + (line.split()[3]) + "\n")
                                            if(int(line.split()[0]) == 200010):
                                                touch200 = 1
                                                break
                                                print("comes to touch point")
    numc +=1
    print(xc)
    xc= 0
                                  # if (xcheck>50):
                                     #   xcheck = 0


"""
for cur_file in os.listdir(opdir):
    print(cur_file)
    if cur_file.endswith(".out"):
        for line in open(opdir+cur_file, "r").readlines():
            if "50000" in line:
                outfile.write("1"+"\t"+"1"+"\t"+"1"+"\t"+"1"+"\t"+line)
outfile.close()

"""