"""
Generalised CDCI Gillespie model
Preserves EXACT n=2 behaviour
Author: Original by A. Reina, generalised faithfully
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
def gillespieStep(
        state, qualities, pA,
        vectorsOfChange, timeLeft,
        noisevalue, t_d, t_e):

    probabilitiesOfChange = []
    n = len(qualities)

    D = state[:n]
    E = state[n:]
    p_other = (1 - pA) / (n - 1)
    opt_names = [chr(ord('A') + i) for i in range(n)]

    for i in range(n):
        src = opt_names[i]

        ########### Cross-inhibition #########
        ##AD * BD → AE 
        ##BD * AD → BE 

        for j in range(n):
            if i == j:
                continue

            inh = opt_names[j]

            if sum(D) <= 1:
                rate = 0
            else:
                rate = (
                    D[i] * D[j]
                    * ((1 - noisevalue) / (qualities[i] * t_d))
                    / (sum(D) - 1)
                )

            probabilitiesOfChange.append(rate)

            #print(
            #    f"[CI] {src}D * {inh}D → {src}E | "
            #    f"D{i}={D[i]}, D{j}={D[j]}, "
            #    f"q{i}={qualities[i]} "
            #)

        ########### No cross-inhibition cause met same #########
        ###AD * AD → AE
        ####BD * BD → BE

        if sum(D) <= 1:
            rate = 0
        else:
            rate = (
                D[i] * D[i]
                * ((1 - noisevalue) / (qualities[i] * t_d))
                / (sum(D) - 1)
            )

        probabilitiesOfChange.append(rate)

        #print(
        #    f"[NCI] {src}D * {src}D → {src}E | "
        #    f"D{i}={D[i]}, "
        #    f"q{i}={qualities[i]} "
        #)

        ############## Exploration end ##########
        ###  AE → AD , BE → BD
        rate = E[i] * (1 / t_e)
        probabilitiesOfChange.append(rate)

        #print(
        #    f"[E→D] {src}E → {src}D | E{i}={E[i]}"
        #)

        # ###### Noisy switches: D[i] → E[j] ########
        ####AD → AE, AD → BE
        #### BD → AE,  BD → BE
        for j in range(n):
            tgt = opt_names[j]

            pij = pA if j == 0 else p_other

            rate = D[i] * ((noisevalue * pij) / (qualities[i] * t_d))
            probabilitiesOfChange.append(rate)

            #print(
            #    f"[ND] {src}D → {tgt}E | "
            ##    f"p={pij}, "
            #    f"q{i}={qualities[i]}"
            #)

    # ########### Gillespie selecting ########
    probSum = sum(probabilitiesOfChange)
    if probSum <= 0:
        return True, timeLeft

    dt = np.random.exponential(1 / probSum)

    # The transition happens after the maximum time length, so we do not include it and terminate the step

    if dt > timeLeft:
        return True, timeLeft


    # Normalising probOfChange in the range [0,1]
    probabilitiesOfChange = [p / probSum for p in probabilitiesOfChange]

    # Selecting the occurred reaction in a randomly, proportionally to their probabilities
    # Get a random between [0,1) (but we don't want 0!)
    r = np.random.random()
    bottom = 0.0
    index = -1
    for i, p in enumerate(probabilitiesOfChange):
        if bottom <= r < bottom + p:
            index = i
            break
        bottom += p

    if index == -1:
        print("ERROR: transition not found")
        sys.exit(1)

    state += np.array(vectorsOfChange[index])
    return False, dt


####################################################
# VECTORS OF CHANGE
####################################################

def build_vectors_of_change(n):

    vectors = []

    for i in range(n):
        Di = i
        Ei = i + n

        # -------- Cross-inhibition --------
        for j in range(n):
            if j == i:
                continue
            v = [0] * (2 * n) #[-1,0,1,0]
            v[Di] -= 1
            v[n+j] += 1
            vectors.append(v)

        # -------- No cross-inhibition --------
        v = [0] * (2 * n)
        v[Di] -= 1
        v[Ei] += 1
        vectors.append(v)

        # -------- Exploration end --------
        v = [0] * (2 * n)
        v[Ei] -= 1
        v[Di] += 1
        vectors.append(v)

        # -------- Noisy switches --------
        for j in range(n):
            v = [0] * (2 * n)
            v[Di] -= 1
            v[n + j] += 1
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
        #print(vectorsOfChange)
        prev = copy.deepcopy(state)

        finished, dt = gillespieStep(
            state,qualities,pA,
            vectorsOfChange, T - t,
            noisevalue, t_d, t_e
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

    # -------- qualities --------
    qualities = [qa] + [1.0] * (n - 1)
    print (qualities)
    # -------- noise probabilities --------
    nr1 = [pA] + [(1 - pA)/(n-1)] * (n-1)
    nr2 = [(1 - pA)] + [pA/(n-1)] * (n-1)

    quorum = 0

    #spd = [(N+1) for _ in range(N+1)]
    theexploration = int((t_e / (t_e + t_d)) * N)
    state =  [round((N - theexploration) / n)] * n + \
            [round(theexploration / n)] * n

    spd = [[0] * (N + 1) for _ in range(N + 1)]
    print(N, "Finding CDCI:", "(", state, ")  QRatio: ", qualities)

    temporalEvolution = 'popevo_vm0.05_' + str(state) + str(t_u) + "td" + str(t_d) + "te" + str(t_e) + "_" + str(
        pA) + "noise_" + "500ksteps_" + str(repetitions) + "runs_" + str(N) + "agents_" + str(qualities) + str(
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

    for i in range(N+1):
        for j in range(N+1):
            spd[i][j] /= (repetitions * T)

    outputname = "vm0.05_outputoftu" + str(state) + str(t_u) + "td" + str(t_d) + "te" + str(t_e) + "_" + str(
        nr2[0]) + "noise_" + "500ksteps_" + str(repetitions) + "runs_" + str(N) + "agents" + str(qualities) + ".txt"
    print(spd, file=open(outputname, "a"))
