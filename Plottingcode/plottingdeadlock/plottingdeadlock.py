import matplotlib.pyplot as plt
import glob, os
import pandas as pd
import seaborn as sns
fig, ax = plt.subplots()


# Define the folder path containing the text files
folder_path = '/content/drive/MyDrive/red_blue/0.66_n/'
noiselist = []
noiseA =[]
val = []
# Iterate through all files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is a text file
    if filename.endswith('.txt'):
        # Open the file
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            noise_val = float((filename.split('_')[1]).split('n')[1])
            # Read the contents of the file
            for line in file:
            # Process the contents as needed
              #print(line)
              noiselist.append(noise_val)
              noiseA.append(float(line.split()[4]))
              val.append((float(line.split()[0])+float(line.split()[2])) - (float(line.split()[1])+float(line.split()[3])))

print(noiselist)
print(noiseA)
print(val)
data = pd.DataFrame({'X': noiseA, 'Y': noiselist, 'Z': val})
#data_pivoted = data.pivot("X", "Y", "Z")
sc = plt.scatter(noiseA,noiselist,c=val, cmap="seismic", s=150)

fig.colorbar(sc, ax=ax)
#plt.pcolormesh(noiseA, noiselist, val, shading='nearest')

noiselist= [0,0.0001,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1]
qb = 0.66
noiseA = []

for n in noiselist:
    if (n>0):
      v = (-1 + n + qb + n*qb)/(2*n + 2 *n*qb)
      noiseA.append(v)
    else:
      noiseA.append(0)

print(noiseA)
plt.xlim(0,1)
            #print(contents)
            #print("--------------------------------")

ax.tick_params(labelsize=18)

ax.plot(noiseA,noiselist,linewidth=6,color='black')
plt.show()
