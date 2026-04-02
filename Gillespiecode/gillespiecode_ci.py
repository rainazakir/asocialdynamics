'''
Created on 24 Jun 2016
@author: Andreagiovanni Reina.
University of Sheffield, UK.
'''

# import RungeKutta.bestOfN
import math
import numpy as np
import sys
import os
import copy
import random

# import matplotlib.pyplot as plt
# from plotting import plotit

DEBUG = False
listA = []
listB = []
opdir = '/scratch/data2/'  # os.getcwd()
data_files = []
statusofNA = "none"
time1 = "none"
time2 = "none"
totaltime = 0
alltimes = []
totallist = []


#################FUNCTIONS#########################
def gillespieStep(state, N, gammas, alphas, rhos, sigmas, vectorsOfChange, timeLeft):
    # Computing the probabilities of change
    probabilitiesOfChange = []
    ## A -(x)-> B
    ## x=5   1/s
    ## when the change will happen?
    ## 0.2s  # on average for one A
    ## but you have many A
    ## a is the number of guys in state A
    ## population level transition rate = a*x
    ## A -(x)-> B
    ## B -(y)-> A
    ## B+A -(y)-> A+A
    ## sum of all rates at population level Z = a*x + b*y + b*a*y / (N)^(number of agents involved minus 1)
    ## (N)^(number of agents involved minus 1) --> it means that for
    ###### number of agents involved=1 ---> a*x/ (N^0)  = a*x/1 = a*x
    ###### number of agents involved=2 ---> b*a*y/ (N^1)  = b*a*x/N
    ## sum of all rates at population level Z = a*x + b*y + b*a*y/N
    ## from Z we compute WHEN the change will happen
    ## what about which change (that is, if x or y)?
    ## probabilitiesOfChange = [ a*x , b*y , b*a*x/N ]
    numOptions = int((len(state) - 1) / 2)
    for i in range(0, numOptions):  # PAY ATTENTION THAT i IS NOT THE CORRECT state[i] BUT IT MUST BE state[i+1], WHILE WORKS FOR gammas[i], alphas[i], rhos[i]
        # Discovery
        # probabilitiesOfChange.append( state[0]*gammas[i]) # U -> A and U -> B
        # Abandonment
        # probabilitiesOfChange.append( state[i+1]*alphas[i] )# A -> U and B -> U

        #############Cross-inhibition#############
        # [ U, AD, BD, AE, BE ]
        # probabilitiesOfChange.append(state[1] * state[2] * ((1 - noisevalue) / (qualities[i] * t_d)) / (N - 1))
        if ((state[1] + state[2])) <= 1:
            probabilitiesOfChange.append(0)
        else:
            probabilitiesOfChange.append(
                state[1] * state[2] * ((1 - noisevalue) / (qualities[i] * t_d)) / ((state[1] + state[2]) - 1))

        ############Recruitment###################
        # probabilitiesOfChange.append(state[0] * state[i + 1] * rhos[i] / (N - 1))  # U + A -> A + A
        # U + Ad --(1-n/tu)-->  Ad + Ae
        # U + Bd  --(1-n/tu)-->  Bd + Be
        if ((state[1] + state[2])) == 0:
            probabilitiesOfChange.append(0)
        else:
            probabilitiesOfChange.append((state[0] * state[i + 1] * ((1 - noisevalue) / t_u)) / (state[1] + state[2]))

        ############# No Cross-inhibtion #############
        # probabilitiesOfChange.append(state[i+1] * state[i+1] * ((1-noisevalue)/(qualities[i]*t_d)) / (N - 1))
        if ((state[1] + state[2])) <= 1:
            probabilitiesOfChange.append(0)
        else:
            probabilitiesOfChange.append(
                state[i + 1] * state[i + 1] * ((1 - noisevalue) / (qualities[i] * t_d)) / ((state[1] + state[2]) - 1))

        ############# Go to Dissemination after Exploration #############
        probabilitiesOfChange.append(state[i + 3] * (1 / t_e))  # AE -> AD and BE -> BD

        ############# Noisy Switch from Kilogrid #############
        probabilitiesOfChange.append(state[i + 1] * ((noisevalue * nr1[i]) / (qualities[i] * t_d)))  # AD->BE and BD->AE
        probabilitiesOfChange.append(state[i + 1] * ((noisevalue * nr2[i])/ (qualities[i] * t_d)))  # AD->AE and BD->BE
        probabilitiesOfChange.append(state[0] * ((noisevalue* nr2[i]) / (t_u)))  # U->AE and U->BE

    #  print("PoC:", probabilitiesOfChange)

    probSum = sum(probabilitiesOfChange)
    timeInterval = np.random.exponential(1 / probSum)
    # print(timeInterval)
    # The transition happens after the maximum time length, so we do not include it and terminate the step
    if timeInterval > timeLeft:
        return True, timeLeft

    # Selecting the occurred reaction in a randomly, proportionally to their probabilities
    bottom = 0.0
    # Get a random between [0,1) (but we don't want 0!)
    reaction = 0.0
    while (reaction == 0.0):
        reaction = np.random.random_sample()
    # print("reaction is: ", reaction)

    ## probabilitiesOfChange = [ 0.5 , 0.7 , 0.1 ]  ->> WHICH? the first with prob 0.5/(0.5+0.7+0) and second with prob 0.7/(0.5+0.7+0)
    ## probabilitiesOfChange = [ 0.38 , 0.54 , 0.08 ]  ->> WHICH? the first with prob 0.5/(0.5+0.7+0) and second with prob 0.7/(0.5+0.7+0)
    ## random is 0.6
    ## pick 1 if random <0.38
    ## pick 2 if 0.38 < random < (0.38+0.54)
    ## pick 3 if (0.38+0.54) < random < (0.38+0.54+0.08)
    # Normalising probOfChange in the range [0,1]
    probabilitiesOfChange = [pc / probSum for pc in probabilitiesOfChange]
    #  print("Norm PoC:", probabilitiesOfChange)
    # print("Add Norm PoC:", sum(probabilitiesOfChange))

    index = -1
    for i, prob in enumerate(probabilitiesOfChange):
      #  print("prob in arr:", prob)
        if (reaction >= bottom and reaction < (bottom + prob)):
            index = i
            break
        bottom += prob
    #  print(i, prob, bottom)

    # print("timeInterval is", timeInterval)
    # print("reaction is", reaction)
    # print("index is ", index)

    if (index == -1):
        print("Transition not found. Error in the algorithm execution.")
        # sys.exit()
    # print(state)
    #  print(vectorsOfChange[index])
    state += np.array(vectorsOfChange[index])
    print(state)
    if (state[0] < 0):
        print("exittinngggg!!!!")
        print("len of poc", len(probabilitiesOfChange))
        print("len of vectors of change", len(vectorsOfChange))

        sys.exit()
    return False, timeInterval


def runGillespie(state, T, N, gammas, alphas, rhos, sigmas, rnd_seed, finalStateFile, temporalEvolution, plot_evo,
                 extraLog, quorum):
    np.random.seed(rnd_seed)
    n = len(gammas)
    state = np.array(state)
    print("State on enteringg: ", state)
    t = 0
    # if DEBUG:
    #    print("t: ", t, "state: ", state)

    # Opening output file if needed
    if (temporalEvolution != "none"):
        os.makedirs(os.path.dirname(temporalEvolution), exist_ok=True)
        evoStream = open(temporalEvolution, "w+")
        out = str(t) + "\t" + '\t'.join(str(x) for x in state) + "\t" + str(noisevalue) + "\n"
        evoStream.write(out)

    # Creating the list of vector of change
    vectorsOfChange = []
    for i in [1, 2]:
        if (i == 1):  # pop A
            # [U AD BD AE BE]  # the important thing is that sum is ZERO
            negative = [1, -1, 0, 0, 0]  # for cross inhibition
            plus = [-1, 0, 0, 1, 0]  # for recruitment
            sameplus = [0, -1, 0, 1, 0]  # for no-crossinhibition in voting
            expplorationend = [0, 1, 0, -1, 0]
            noiseopposite = [0, -1, 0, 0, 1]
            noisesame = [0, -1, 0, 1, 0]
            noiseuncommitted = [-1, 0, 0, 1, 0]

        if (i == 2):  # pop B
            negative = [1, 0, -1, 0, 0]
            plus = [-1, 0, 0, 0, 1]
            sameplus = [0, 0, -1, 0, 1]
            expplorationend = [0, 0, 1, 0, -1]
            noiseopposite = [0, 0, -1, 1, 0]
            noisesame = [0, 0, -1, 0, 1]
            noiseuncommitted = [-1, 0, 0, 0, 1]

        #         # Positive change
        #         plus = [-1] + [0]*n
        #         plus[i+1] = 1
        #         # Negative change
        #         negative = [1] + [0]*n
        #         negative[i+1] = -1

        # Discovery
        # vectorsOfChange.append( plus )
        # Abandonment
        # vectorsOfChange.append( negative )
        # Recruitment
        vectorsOfChange.append(negative)
        vectorsOfChange.append(plus)

        vectorsOfChange.append(sameplus)
        vectorsOfChange.append(expplorationend)
        vectorsOfChange.append(noiseopposite)
        vectorsOfChange.append(noisesame)
        vectorsOfChange.append(noiseuncommitted)
        ## vectorsOfChange for the case n=2        ## plusDicoveryOfA  minusAbandonmentOfA  plusRecruitA  plusInhibitionA plusRecruitFromZealotA  plusInhibitionFromZealotA  plusDicoveryOfB minusAbandonmentOfB  plusRecruitB  plusInhibitionB plusRecruitFromZealotB  plusInhibitionFromZealotB

    print("VoC:", vectorsOfChange)

    quorum_reached = False
    while t < T:
        previous_state = copy.deepcopy(state)

        sim_finished, time_step = gillespieStep(state, N, gammas, alphas, rhos, sigmas, vectorsOfChange, T - t)
        # update time variable
        print(state[1])
        t += time_step
        # update SPD matrix which keeps track of the time spent in each state
        spd[int(previous_state[1]) + int(previous_state[3])][int(previous_state[2]) + int(previous_state[4])] += time_step

        if (temporalEvolution != "none"):
        # if (t>1000000):#999000
            out = str(t) + "\t" + '\t'.join(str(x) for x in state) + "\t" + str(noisevalue) + "\n"
            evoStream.write(out)
       # print("out", out)
        # out = str(t) + "\t" + '\t'.join(str(x) for x in state) + "\t"
        # evoStream.write(out)
        #   #print("t: ", t, "state: ", state)
        """
        if whichAvg == "Aavg":
            if float(state[1] > S*0.5):
                listA.append(float(state[1]))
        else:
            if float(state[2] > S*0.5):
                listB.append(float(state[2]))
        """
        ## Checking each timestep if the quorum is reached
        if (quorum > 0):  # 0.79>0 true
            # quorum_reached = False
            for i in np.arange(1, len(state) - 2):
                # print (i);
                # if (int(state[i]) > (N-Z)*quorum):
                if ((state[i]+state[i+2]) >= N * quorum):
                    # print("reaches quorum")
                    quorum_reached = True
                    break
        if sim_finished or quorum_reached:
            break
    #print((np.array(spd)).shape)
    out = str(t) + "\t" + '\t'.join(str(x) for x in state) + "\t" + str(noisevalue)
    #print(out)
    if (finalStateFile != "none"):
        os.makedirs(os.path.dirname(finalStateFile), exist_ok=True)
        with open(finalStateFile, "a") as f:
            out = '\t'.join(str(x) for x in extraLog)
            if (len(out) > 0): out += '\t'
            out += str(t) + "\t" + '\t'.join(str(x) for x in state) + "\n"
            f.write(out)
    # if DEBUG:
    #     out = '\t'.join(str(x) for x in extraLog)
    #     if (len(out)>0): out += '\t'
    #     out += str(t) + "\t" + '\t'.join(str(x) for x in state) + "\n"
    #     print(out)
    """
    theAavg = 0
    theBAvg = 0
    if whichAvg == "Aavg":
        if len(listA) !=0:
            theAavg = np.mean(listA)
            print("A-Average:",theAavg)
    else:
        if len(listB) !=0:
            theBAvg = np.mean(listB)
            print("B-Average:",theBAvg)
    """
    if (plot_evo):
        if (temporalEvolution == "none"):
            print(
                "WARNING! - to plot the temporal evolution, please specify a temporalEvolution file (e.g., a temp-file)")
        # else:
        #   plotit(temporalEvolution, T, state, N, evoStream, 0, state[1], state[2], state[3],state[4], qualities[0])


##################################################

if __name__ == '__main__':

    repetitions = 250

    # Computing input params
    #     valuesA = np.arange(7.5, 13, 0.5)
    noisevalue = float(sys.argv[7])
    ## noisetype = sys.argv[8]
    ##  if noisetype == "TypeA":
    ##      noisetype1 = noisevalue
    ##      noisetype2 = [0, 0]
    ##  else:
    ##      noisetype1 = 0
    ##      noisetype2 = [noisevalue, noisevalue]
    qualities = [float(sys.argv[6]), 1]
    qa = [float(sys.argv[6])]
    print(qualities)
    #     valuesB = np.arange(6.5, 15.01, 0.1)
    n = 2
    k = 0
    h = 1

    # CHANGED
    # Experiment time length
    T = int(sys.argv[1])
    # Setup the initial state
    N = int(sys.argv[2])
    t_u = float(sys.argv[3])
    t_d = int(sys.argv[4])
    t_e = int(sys.argv[5])
    nr1 =  [1-float(sys.argv[9]), float(sys.argv[9])]
    nr2 =  [float(sys.argv[9]), 1-float(sys.argv[9])]

    quorum=0
    #quorum = float(1-float(sys.argv[7]))
    ##Z = int(sys.argv[2])
    ##whichrun = sys.argv[3]
    # SA = (N - Z) / 2
    # SB = (N - Z) / 2
    # create data structure of the size of all possible states
    spd = [[0] * (int(N) + 1) for _ in range(int(N) + 1)]
    # print(len(spd[2]))
    ## (keep in mind that it may not sum up to N for certain conditions... we may look at this later)
    #    state = [N-Z] + [0]*n + [Z/2] + [Z/2]

    # Reading output file path from config file
    #     finalStateFile = 'data/fs_k-' + str(k) + '_h-' + str(h) + '.txt'
    #     temporalEvolution = 'none's
    # temporalEvolution = 'data/tmp.txt'

    if sys.argv[8].lower() == 'true':
        plot_evo = True
    elif sys.argv[8].lower() == 'false':
        plot_evo = False

    for valueA in qa:
        finalStateFile = 'none'
        # finalStateFile = 'data/fs_k-' + str(k) + '_h-' + str(h) + '_vA-' + str(valueA) + '-r1.txt'
        #         valuesB = np.arange(valueA-3, valueA+3.01, 0.1)
        valuesB = [1]
        for valueB in valuesB:
            gammas = [k * valueA] + [k * valueB] * (n - 1)
            alphas = [k / valueA] + [k / valueB] * (n - 1)
            # gammas = [0] + [0]
            # alphas = [0] + [0]
            rhos = [h * valueA] + [h * valueB] * (n - 1)
            sigmas = [h * valueA] + [h * valueB] * (n - 1)
            for i in range(0, repetitions):
                theexplorationstate = ((t_e / (t_e + t_d)) * N)
                #state = [0, round((N - theexplorationstate) / 2), round((N - theexplorationstate) / 2),
                #         round(theexplorationstate / 2), round(theexplorationstate / 2)]
                #state = [0, 2, 26, 8, 64]
                print(state)
                # state = U, AD, BD, AE, BE
                print(N, "Finding CDCI:", "(", state, ")  QRatio: ", qualities)

                rnd_seed = np.random.randint(4325344)
                temporalEvolution = 'none'
                temporalEvolution = 'popevo_ci0.05_'+str(state) + str(t_u) + "td" + str(t_d) + "te" + str(t_e) + "_" + str(nr2[0]) + "noise_" + "500ksteps_" + str(repetitions) + "runs_"+str(N)+"agents_" +str(qualities)+str(quorum)+'/'+'evo-N'+str(i)+str(rnd_seed)+'.txt'
                rnd_seed = np.random.randint(4325344)
                # rnd_seed = 43431
                print(rnd_seed)
                # S = N
                """
                if whichrun == "Afull":
                    SA = S
                    SB = 0
                    SU = 0
                elif whichrun == "Bfull":
                    SA = 0
                    SB = S
                    SU = 0
                else: 

                # Compute a random point in the 3-simplex [U,A,B]
                r1 = np.sqrt(np.random.rand())
                r2 = np.random.rand()
                SU = int(r1 * (1 - r2) * N)
                SA = int(r1 * r2 * N)
                SB = int((1 - r1 * (1 - r2) - r1 * r2) * N)
                while SU + SA + SB < N:
                    rnd = np.random.rand()
                    if rnd < 0.33333:
                        SU += 1
                    elif rnd < 0.66666:
                        SA += 1
                    else:
                        SB += 1
                n= 5
                total = N
                dividers = sorted(random.sample(range(1, total), n - 1))
                thelistofdivisions = [a - b for a, b in zip(dividers + [total], [0] + dividers)]
                state = [thelistofdivisions[0], thelistofdivisions[1], thelistofdivisions[2],thelistofdivisions[3],thelistofdivisions[4]]
                """
                # state = [0,12,12,12,13]
                #theexplorationstate = ((t_e / (t_e + t_d)) * N)
                #state = [0, round((N - theexplorationstate) / 2), round((N - theexplorationstate) / 2),
                 #        round(theexplorationstate / 2), round(theexplorationstate / 2)]
                # state = [0,N/4,N/4,N/4,N/4]
                #print(state)
                # state = U, AD, BD, AE, BE
                print(N, "Finding CDCI:", "(", state, ")  QRatio: ", qualities)
                # state = [N-Z] + [0]*n + [Z/n]
                plt = runGillespie(state, T, N, gammas, alphas, rhos, sigmas, rnd_seed, finalStateFile,
                                   temporalEvolution, plot_evo, extraLog=[valueA, valueB], quorum=quorum)
# Normalise the SPD: divide every value by the maximum time T
for a in range(int(sum(state[0:3])) + 1):
    for b in range(int(sum(state[0:3])) + 1):
        spd[a][b] /= repetitions * T
print(np.array(spd))

outputname = "ci0.05_outputoftu" + str(state) + str(t_u) + "td" + str(t_d) + "te" + str(t_e) + "_" + str(
    nr2[0]) + "noise_" + "500ksteps_" + str(repetitions) + "runs_" + str(N) + "agents"+str(qualities) + ".txt"
print(spd, file=open(outputname, "a"))
# print(spd, file=open("outputoftu600td1300te3300_0.1noise_500ksteps_500runs_52agents.txt", "a"))
