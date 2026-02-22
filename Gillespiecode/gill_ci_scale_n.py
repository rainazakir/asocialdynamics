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

def gillespieStep(state, N, qualities,pA,
                  vectorsOfChange, timeLeft,
                  noisevalue, t_u, t_d, t_e):
    # Computing the probabilities of change
    probabilitiesOfChange = []

    n = len(qualities)
    U = state[0]
    D = state[1:1+n]
    E = state[1+n:1+2*n]
    p_other = (1 - pA) / (n - 1)

    opt_names = [chr(ord('A') + i) for i in range(n)]  # For debugging

    # Reactions that change each state
    if DEBUG: print(n, U,D,E)

    for i in range(n):
        src = opt_names[i]

        # -------- Cross inhibition -------- #
        for j in range(n):
            if i == j:
                continue

            inh = opt_names[j]

            if sum(D) <= 1:
                probabilitiesOfChange.append(0)
                if DEBUG: print(f"[CI] {src}D * {inh}D = 0 (sum(D)<=1)")
            else:
                rate = (
                        D[i] * D[j]
                        * ((1 - noisevalue) / (qualities[i] * t_d))
                        / (sum(D) - 1)
                )
                probabilitiesOfChange.append(rate)

                if DEBUG:
                    print(
                    f"[CI] {src}D * {inh}D * (1-η)/(q{src}·td)  → U | "
                    f"{src}D={D[i]}, {inh}D={D[j]}, q{src}={qualities[i]}"
                    )

        # -------- Recruitment -------- #
        if sum(D) == 0:
            probabilitiesOfChange.append(0)
            if DEBUG: print(f"[R] U * {src}D = 0 (sum(D)==0)")
        else:
            rate = (U * D[i] * ((1 - noisevalue) / t_u)) / sum(D)
            probabilitiesOfChange.append(rate)

            if DEBUG:
                print(
                f"[R] U * {src}D * (1-η)/tu  → {src}E | "
                f"U={U}, {src}D={D[i]}"
                )

        # -------- No cross inhibition -------- #
        if sum(D) <= 1:
            probabilitiesOfChange.append(0)
            if DEBUG: print(f"[NCI] {src}D * {src}D = 0 (sum(D)<=1)")
        else:
            rate = (
                    D[i] * D[i]
                    * ((1 - noisevalue) / (qualities[i] * t_d))
                    / (sum(D) - 1)
            )
            probabilitiesOfChange.append(rate)

            if DEBUG:
                print(
                f"[NCI] {src}D * {src}D * (1-η)/(q{src}·td) → {src}E | "
                f"{src}D={D[i]}, q{src}={qualities[i]}"
                )

        # -------- End exploration -------- #
        rate = E[i] * (1 / t_e)
        probabilitiesOfChange.append(rate)

        if DEBUG: print(
            f"[E→D] {src}E * 1/te → {src}D | {src}E={E[i]}"
        )

        # -------- Noisy switch: D[i] → E[j] -------- #
        for j in range(n):
            tgt = opt_names[j]

            pij = pA if j == 1 else p_other

            rate = D[i] * ((noisevalue * pij) / (qualities[i] * t_d))
            probabilitiesOfChange.append(rate)

            if DEBUG:
                print(
                f"[ND] {src}D → {tgt}E | "
                f"{src}D * η * p({src}→{tgt})/(q{src}·td) = "
                f"{pij}"
                )

        # -------- Noisy switch: U → E[i] -------- #

        pn = pA if i == 1 else p_other

        rate = U * ((noisevalue * pn) / t_u)
        probabilitiesOfChange.append(rate)

        if DEBUG: print(
            f"[NU] U → {src}E | U * η * p(U→{src})/tu = {pn}"
        )


    # Sampling reaction time: if the transition happens after the maximum time length, do not include it and terminate the step
    probSum = sum(probabilitiesOfChange)
    timeInterval = np.random.exponential(1 / probSum)
    if DEBUG: print(timeInterval)
    if timeInterval > timeLeft:
        return True, timeLeft

    # Select the occurred reaction in a random, proportional to their probabilities order
    bottom = 0.0
    reaction = 0.0
    while (reaction == 0.0):
        reaction = np.random.random_sample()
    if DEBUG: print("reaction is: ", reaction)

    # Normalising probOfChange in the range [0,1]
    probabilitiesOfChange = [pc / probSum for pc in probabilitiesOfChange]
    if DEBUG: print("Norm PoC:", probabilitiesOfChange)
    if DEBUG: print("Add Norm PoC:", sum(probabilitiesOfChange))

    index = -1
    for i, prob in enumerate(probabilitiesOfChange):
        if (reaction >= bottom and reaction < (bottom + prob)):
            index = i
            break
        bottom += prob

    if DEBUG: print("timeInterval is", timeInterval)
    if DEBUG: print("reaction is", reaction)
    if DEBUG: print("index is ", index)

    if (index == -1):
        print("Transition not found. Error in the algorithm execution.")

    # Update population state
    state += np.array(vectorsOfChange[index])
    if DEBUG: print(state)

    if (state[0] < 0):
        print("exiting!!!!")
        print("len of poc", len(probabilitiesOfChange))
        print("len of vectors of change", len(vectorsOfChange))

        sys.exit()
    return False, timeInterval

####################################################
# VECTORS OF CHANGE
####################################################

def build_vectors_of_change(n, type):
    # Creating the list of vector of change
    vectors = []

    for i in range(n):
        Di = 1 + i
        Ei = 1 + n + i

        # -------- Cross inhibition: Di inhibited by Dj -------- #
        for j in range(n):
            if j == i:
                continue
            v = [0] * (1 + 2*n)
            v[Di] -= 1   # Di -> U
            v[0]  += 1
            vectors.append(v)

        # -------- Recruitment -------- #
        v = [0] * (1 + 2*n)
        v[0] -= 1
        v[Ei] += 1
        vectors.append(v)

        # -------- No cross inhibition -------- #
        v = [0] * (1 + 2*n)
        v[Di] -= 1
        v[Ei] += 1
        vectors.append(v)

        # -------- Exploration end -------- #
        v = [0] * (1 + 2*n)
        v[Ei] -= 1
        if type==1:
            v[0] += 1
        else:
            v[Di] += 1
        vectors.append(v)

        # -------- Noise: Di → Ej (ALL j) -------- #
        for j in range(n):
            v = [0] * (1 + 2*n)
            v[Di] -= 1
            v[1 + n + j] += 1
            vectors.append(v)

        # -------- Noise: U → Ei -------- #
        v = [0] * (1 + 2*n)
        v[0] -= 1
        v[Ei] += 1
        vectors.append(v)

    return vectors


####################################################
# RUN GILLESPIE
####################################################

def runGillespie(state, T, N, qualities,pA,
                 rnd_seed, finalStateFile,
                 temporalEvolution, plot_evo,
                 extraLog, quorum,
                 noisevalue, t_u, t_d, t_e, spd, type):

    np.random.seed(rnd_seed)
    state = np.array(state, dtype=int)
    t = 0

    if temporalEvolution != "none": #logging
        os.makedirs(os.path.dirname(temporalEvolution), exist_ok=True)
        evo = open(temporalEvolution, "w+")
        evo.write(str(t) + "\t" + "\t".join(map(str, state)) + "\n")

    vectorsOfChange = build_vectors_of_change(len(qualities),type)

    # Iterating Gillespie step until time T
    while t < T:
        if DEBUG: (vectorsOfChange)
        prev = copy.deepcopy(state)

        finished, dt = gillespieStep(
            state, N, qualities,pA,
            vectorsOfChange, T - t,
            noisevalue, t_u, t_d, t_e
        )

        t += dt


        if temporalEvolution != "none": #logging
            evo.write(str(t) + "\t" + "\t".join(map(str, state)) + "\n")

        # Checking each timestep if the quorum is reached
        if quorum > 0:
            for i in range(len(qualities)):
                if state[1+i] + state[1+len(qualities)+i] >= N * quorum:
                    finished = True
                    break

        if finished:
            break

    if finalStateFile != "none": #logging
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

    # -------- number of experiment to repeat -------- #

    repetitions = 100

    # -------- input params -------- #

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
    n = int(sys.argv[10])
    type = 1
    quorum = 0

    # -------- qualities -------- #
    qualities = [qa] + [1.0] * (n - 1)
    if DEBUG: print (qualities)


    # -------- Setup the initial state -------- #

    spd = [[0]*(N+1) for _ in range(N+1)]
    theexploration = int((t_e / (t_e + t_d)) * N)
    state = [0] + \
            [round((N - theexploration) / n)] * n + \
            [round(theexploration / n)] * n

    if DEBUG: print(N, "Finding CDCI:", "(", state, ")  QRatio: ", qualities)

    # -------- Output file: temporal evolution data  -------- #
    temporalEvolution = 'popevo_ci0.05_' + str(state) + str(t_u) + "td" + str(t_d) + "te" + str(t_e) + "_" + str(
        pA) + "noise_" + "500ksteps_" + str(repetitions) + "runs_" + str(N) + "agents_" + str(qualities) + str(
        quorum)  + '_evo-N' + "_n_"+str(n)+"_vn_"+str(noisevalue)
    for run in range(repetitions):

        rnd_seed = np.random.randint(1e9)


        runGillespie(
            state, T, N, qualities,pA,
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
            spd=spd,
            type=type
        )

