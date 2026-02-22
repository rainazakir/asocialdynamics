"""
n>2 DS Gillespie model, Preserves EXACT n=2 behaviour
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
def gillespieStep(
        state, qualities, pA,
        vectorsOfChange, timeLeft,
        noisevalue, t_d, t_e):

    # Computing the probabilities of change

    probabilitiesOfChange = []
    n = len(qualities)
    D = state[:n]
    E = state[n:]
    p_other = (1 - pA) / (n - 1)

    opt_names = [chr(ord('A') + i) for i in range(n)] # For debugging

    for i in range(n):
        src = opt_names[i]

        # -------- Direct-switch -------- #
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
            if DEBUG: print(
                f"[CI] {src}D * {inh}D → {src}E | "
                f"D{i}={D[i]}, D{j}={D[j]}, "
                f"q{i}={qualities[i]} "
            )

        # -------- Direct-switch same opinion  -------- #
        if sum(D) <= 1:
            rate = 0
        else:
            rate = (
                D[i] * D[i]
                * ((1 - noisevalue) / (qualities[i] * t_d))
                / (sum(D) - 1)
            )

        probabilitiesOfChange.append(rate)
        if DEBUG:
            print(
            f"[NCI] {src}D * {src}D → {src}E | "
            f"D{i}={D[i]}, "
            f"q{i}={qualities[i]} "
            )

        # -------- End exploration -------- #
        rate = E[i] * (1 / t_e)
        probabilitiesOfChange.append(rate)

        if DEBUG: print(
            f"[E→D] {src}E → {src}D | E{i}={E[i]}"
        )

        # -------- Noisy switch: D[i] → E[j] -------- #
        for j in range(n):
            tgt = opt_names[j]

            pij = pA if j == 0 else p_other

            rate = D[i] * ((noisevalue * pij) / (qualities[i] * t_d))
            probabilitiesOfChange.append(rate)

            if DEBUG:
                print(
                f"[ND] {src}D → {tgt}E | "
                f"p={pij}, "
                f"q{i}={qualities[i]}"
                )

    # Sampling reaction time: if the transition happens after the maximum time length, do not include it and terminate the step
    probSum = sum(probabilitiesOfChange)
    if probSum <= 0:
        return True, timeLeft

    dt = np.random.exponential(1 / probSum)
    if dt > timeLeft:
        return True, timeLeft


    # Normalising probOfChange in the range [0,1]
    probabilitiesOfChange = [p / probSum for p in probabilitiesOfChange]

    # Select the occurred reaction in a random, proportional to their probabilities order

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

    # Update population state
    state += np.array(vectorsOfChange[index])
    return False, dt


####################################################
# VECTORS OF CHANGE
####################################################

def build_vectors_of_change(n):
    # Creating the list of vector of change
    vectors = []

    for i in range(n):
        Di = i
        Ei = i + n

        # -------- Direct-switch --------
        for j in range(n):
            if j == i:
                continue
            v = [0] * (2 * n) #[-1,0,1,0]
            v[Di] -= 1
            v[n+j] += 1
            vectors.append(v)

        # -------- Direct-switch same opinion --------
        v = [0] * (2 * n)
        v[Di] -= 1
        v[Ei] += 1
        vectors.append(v)

        # -------- Exploration end --------
        v = [0] * (2 * n)
        v[Ei] -= 1
        v[Di] += 1
        vectors.append(v)

        # -------- Noisy switch --------
        for j in range(n):
            v = [0] * (2 * n)
            v[Di] -= 1
            v[n + j] += 1
            vectors.append(v)

    return vectors


####################################################
# RUN GILLESPIE
####################################################

def runGillespie(state, T, N, qualities,pA,
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

    # Iterating Gillespie step until time T
    while t < T:
        if DEBUG: (vectorsOfChange)
        prev = copy.deepcopy(state)

        finished, dt = gillespieStep(
            state,qualities,pA,
            vectorsOfChange, T - t,
            noisevalue, t_d, t_e
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
    repetitions = 5

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
    n = int(sys.argv[10])  # change manually if needed
    quorum = 0

    # -------- qualities --------
    qualities = [qa] + [1.0] * (n - 1)
    if DEBUG: print (qualities)

    # -------- Setup the initial state -------- #

    theexploration = int((t_e / (t_e + t_d)) * N)
    state =  [round((N - theexploration) / n)] * n + \
            [round(theexploration / n)] * n

    spd = [[0] * (N + 1) for _ in range(N + 1)]
    if DEBUG: print(N, "Finding CDCI:", "(", state, ")  QRatio: ", qualities)

    temporalEvolution = 'popevo_vm0.05_' + str(state) + str(t_u) + "td" + str(t_d) + "te" + str(t_e) + "_" + str(
        pA) + "noise_" + "500ksteps_" + str(repetitions) + "runs_" + str(N) + "agents_" + str(qualities) + str(
        quorum)  + '_evo-N' + "_n_"+str(n)+ "_nval_"+str(noisevalue)
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
            spd=spd
        )
