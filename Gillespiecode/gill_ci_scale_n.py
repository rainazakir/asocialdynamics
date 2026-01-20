"""
n>2 CDCI Gillespie model, EXACT n=2 behaviour
Author: Original by A. Reina
"""

import numpy as np
import sys
import os
import copy
import random

DEBUG = False

####################################################
# GILLESPIE STEP
####################################################

def gillespieStep(state, N, qualities, nr1, nr2,pA,
                  vectorsOfChange, timeLeft,
                  noisevalue, t_u, t_d, t_e):

    probabilitiesOfChange = []
    n = len(qualities)

    U = state[0]
    D = state[1:1+n] #[1,] #Dissemination statee
    E = state[1+n:1+2*n]   #Exploration state
    p_other = (1 - pA) / (n - 1)
    opt_names = [chr(ord('A') + i) for i in range(n)]  # ['A','B','C',...] for Debugginf
    ##print(n, U,D,E)
    for i in range(n):  # source option
        src = opt_names[i]

        # ############ Cross inhibition #############

        ##### AD * BD * (1-η)/(qB·td) → U 

        for j in range(n):  # inhibitor option
            if i == j:
                continue

            inh = opt_names[j]

            if sum(D) <= 1:
                probabilitiesOfChange.append(0)
                print(f"[CI] {src}D * {inh}D = 0 (sum(D)<=1)")
            else:
                rate = (
                        D[i] * D[j]
                        * ((1 - noisevalue) / (qualities[i] * t_d))
                        / (sum(D) - 1)
                )
                probabilitiesOfChange.append(rate)

                print(
                    f"[CI] {src}D * {inh}D * (1-η)/(q{src}·td)  → U | "
                    f"{src}D={D[i]}, {inh}D={D[j]}, q{src}={qualities[i]}"
                )

        ################### Recruitment for U state ##########
        
        #### U * BD * (1-η)/tu → BE 

        if sum(D) == 0:
            probabilitiesOfChange.append(0)
            print(f"[R] U * {src}D = 0 (sum(D)==0)")
        else:
            rate = (U * D[i] * ((1 - noisevalue) / t_u)) / sum(D)
            probabilitiesOfChange.append(rate)

            print(
                f"[R] U * {src}D * (1-η)/tu  → {src}E | "
                f"U={U}, {src}D={D[i]}"
            )

        ############ No cross inhibition caus met own $$$$$$$$$$$$$$$$
        ####] BD * BD * (1-η)/(qB·td) → BE,  AD * AD * (1-η)/(qA·td) → AE 
        if sum(D) <= 1:
            probabilitiesOfChange.append(0)
            print(f"[NCI] {src}D * {src}D = 0 (sum(D)<=1)")
        else:
            rate = (
                    D[i] * D[i]
                    * ((1 - noisevalue) / (qualities[i] * t_d))
                    / (sum(D) - 1)
            )
            probabilitiesOfChange.append(rate)

            print(
                f"[NCI] {src}D * {src}D * (1-η)/(q{src}·td) → {src}E | "
                f"{src}D={D[i]}, q{src}={qualities[i]}"
            )

        ############# Go to Dissemination ###########
        # AE * 1/te → AD
        rate = E[i] * (1 / t_e)
        probabilitiesOfChange.append(rate)

        print(
            f"[E→D] {src}E * 1/te → {src}D | {src}E={E[i]}"
        )

        # -------- Noisy switches: D[i] → E[j] and vice versa #############
        ##AD → AE | AD * η * p(A→A)/(qA·td)
        ###AD → BE | AD * η * p(A→B)/(qA·td)  
        ### BD → AE | BD * η * p(B→A)/(qB·td) 
        ### BD → BE | BD * η * p(B→B)/(qB·td)
        for j in range(n):
            tgt = opt_names[j]

            #if i == 0:
            #    pij = pA if j == 0 else p_other
            #else:
            pij = pA if j == 0 else p_other

            rate = D[i] * ((noisevalue * pij) / (qualities[i] * t_d))
            probabilitiesOfChange.append(rate)

            print(
                f"[ND] {src}D → {tgt}E | "
                f"{src}D * η * p({src}→{tgt})/(q{src}·td) = "
                f"{pij}"
            )

        # -------- Noisy switches: U → E[i] --------
        #### U → BE | U * η * p(U→B)/tu 
        #### U → AE | U * η * p(U→A)/tu 
        pn = pA if i == 0 else p_other
        rate = U * ((noisevalue * pn) / t_u)
        probabilitiesOfChange.append(rate)

        print(
            f"[NU] U → {src}E | U * η * p(U→{src})/tu = {pn}"
        )

        #U--pA --> AE     [-1, 0, 0, 1, 0]
            # U--pB --> BE    [-1, 0, 0, 0, 1]
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
    #print(state)
    if (state[0] < 0):
        print("exittinngggg!!!!")
        print("len of poc", len(probabilitiesOfChange))
        print("len of vectors of change", len(vectorsOfChange))

        sys.exit()
    return False, timeInterval

####################################################
# VECTORS OF CHANGE
####################################################

def build_vectors_of_change(n):

    vectors = []

    for i in range(n):
        Di = 1 + i
        Ei = 1 + n + i

        # -------- Cross inhibition: Di inhibited by Dj --------
        for j in range(n):
            if j == i:
                continue
            v = [0] * (1 + 2*n)
            v[Di] -= 1   # Di -> U
            v[0]  += 1
            vectors.append(v)

        # -------- Recruitment --------
        v = [0] * (1 + 2*n)
        v[0] -= 1
        v[Ei] += 1
        vectors.append(v)

        # -------- No cross inhibition --------
        v = [0] * (1 + 2*n)
        v[Di] -= 1
        v[Ei] += 1
        vectors.append(v)

        # -------- Exploration end --------
        v = [0] * (1 + 2*n)
        v[Ei] -= 1
        v[Di] += 1
        vectors.append(v)

        # -------- Noise: Di → Ej (ALL j) --------
        for j in range(n):
            v = [0] * (1 + 2*n)
            v[Di] -= 1
            v[1 + n + j] += 1
            vectors.append(v)

        # -------- Noise: U → Ei --------
        v = [0] * (1 + 2*n)
        v[0] -= 1
        v[Ei] += 1
        vectors.append(v)

    return vectors


####################################################
# RUN GILLESPIE
####################################################

def runGillespie(state, T, N, qualities, nr1, nr2,pA,
                 rnd_seed, finalStateFile,
                 temporalEvolution, plot_evo,
                 extraLog, quorum,
                 noisevalue, t_u, t_d, t_e, spd):

    np.random.seed(rnd_seed)
    state = np.array(state, dtype=int)
    t = 0

    if temporalEvolution != "none":
        os.makedirs(os.path.dirname(temporalEvolution), exist_ok=True)
        evo = open(temporalEvolution, "w+")
        evo.write(str(t) + "\t" + "\t".join(map(str, state)) + "\n")

    vectorsOfChange = build_vectors_of_change(len(qualities))

    while t < T:
        print(vectorsOfChange)
        prev = copy.deepcopy(state)

        finished, dt = gillespieStep(
            state, N, qualities, nr1, nr2,pA,
            vectorsOfChange, T - t,
            noisevalue, t_u, t_d, t_e
        )

        t += dt

        A = sum(prev[1:1+len(qualities)])
        B = sum(prev[1+len(qualities):])
        spd[int(A)][int(B)] += dt

        if temporalEvolution != "none":
            evo.write(str(t) + "\t" + "\t".join(map(str, state)) + "\n")

        if quorum > 0:
            for i in range(len(qualities)):
                if state[1+i] + state[1+len(qualities)+i] >= N * quorum:
                    finished = True
                    break

        if finished:
            break

    if finalStateFile != "none":
        os.makedirs(os.path.dirname(finalStateFile), exist_ok=True)
        with open(finalStateFile, "a") as f:
            f.write(
                "\t".join(map(str, extraLog)) + "\t" +
                str(t) + "\t" +
                "\t".join(map(str, state)) + "\n"
            )


####################################################
# MAIN
####################################################

if __name__ == "__main__":

    repetitions = 5

    T = int(sys.argv[1])
    N = int(sys.argv[2])
    t_u = float(sys.argv[3])
    t_d = int(sys.argv[4])
    t_e = int(sys.argv[5])
    qa = float(sys.argv[6])
    noisevalue = float(sys.argv[7])
    plot_evo = sys.argv[8].lower() == "true"
    pA = float(sys.argv[9])
    nB = 1-float(sys.argv[9])

    # -------- number of options --------
    n = int(sys.argv[10])  # change manually if needed

    # ########## qualities #########
    qualities = [qa] + [1.0] * (n - 1)
    print (qualities)
    # ########### noise probabilities ######Not used anymore
    nr1 = [pA] + [(1 - pA)/(n-1)] * (n-1)
    nr2 = [(1 - pA)] + [pA/(n-1)] * (n-1)

    quorum = 0

    spd = [[0]*(N+1) for _ in range(N+1)]
    theexploration = int((t_e / (t_e + t_d)) * N)
    state = [0] + \
            [round((N - theexploration) / n)] * n + \
            [round(theexploration / n)] * n
    print(N, "Finding CDCI:", "(", state, ")  QRatio: ", qualities)

    temporalEvolution = 'popevo_ci0.05_' + str(state) + str(t_u) + "td" + str(t_d) + "te" + str(t_e) + "_" + str(
        nr2[0]) + "noise_" + "500ksteps_" + str(repetitions) + "runs_" + str(N) + "agents_" + str(qualities) + str(
        quorum)  + '_evo-N' + "_n_"+str(n)+ "_nval_"+str(noisevalue)
    for run in range(repetitions):



        rnd_seed = np.random.randint(1e9)


        runGillespie(
            state, T, N, qualities, nr1, nr2,pA,
            rnd_seed,
            finalStateFile=temporalEvolution + "/final_state.txt",
            temporalEvolution=temporalEvolution + "/" + str(rnd_seed) + '.txt',
            plot_evo=plot_evo,
            extraLog=[qa],
            quorum=quorum,
            noisevalue=noisevalue,
            t_u=t_u,
            t_d=t_d,
            t_e=t_e,
            spd=spd
        )
    #####TO Be FIXED
    for i in range(N+1):
        for j in range(N+1):
            spd[i][j] /= (repetitions * T)

    outputname = "ci0.05_outputoftu" + str(state) + str(t_u) + "td" + str(t_d) + "te" + str(t_e) + "_" + str(
        nr2[0]) + "noise_" + "500ksteps_" + str(repetitions) + "runs_" + str(N) + "agents" + str(qualities) + ".txt"
    print(spd, file=open(outputname, "a"))
