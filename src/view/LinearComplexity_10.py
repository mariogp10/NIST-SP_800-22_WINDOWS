import scipy.special as sp
import numpy as np
ALPHA = 0.01
def LinearComplexity(n, M, random_number, dir_location):
    K = 6
    N = n//M
    L = [0] * N
    T = [0] * N
    v = [0] * 7
    pi = [0.01047, 0.03125, 0.12500, 0.50000, 0.25000, 0.06250, 0.020833]

    W = []
    blocks = []
    j = 0
    for i in range(N):
        W = W + [0]
        k = 0
        blocks = blocks + [[]]
        while k < M:
            blocks[i] = blocks[i] + [random_number[j]]
            j = j + 1
            k = k + 1
    #Cada elemento de la lista blocks es una secuencia de M-bits
    #Algoritmo Berlekamp-Massey para N cadenas de M-bits
    L = [0] * N

    for i in range(N):
        c = np.zeros(M, dtype=int)
        b = np.zeros(M, dtype=int)
        c[0] = 1
        b[0] = 1
        l = 0
        m = -1

        for j in range(M):
            d = blocks[i][j]

            if l > 0:  # Solo iterar si l > 0
                for k in range(1, l + 1):
                    d ^= c[k] * blocks[i][j - k]

            if d == 1:
                if l <= j // 2:
                    temp_c = c.copy()
                    c[j - m:j - m + M - (j - m)] ^= b[:M - (j - m)]
                    b = temp_c
                    l = j + 1 - l
                    m = j
                else:
                    c[j - m:j - m + M - (j - m)] ^= b[:M - (j - m)]

        L[i] = l

    mu = M/2 + (9 + (-1)**(M*1)) / 36 - (M/3 + 2/9) / (2**M)
    for i in range(N):
        T[i] = ((-1)**M) * (L[i] - mu) + 2/9
        if T[i] <= -2.5:
            v[0] = v[0] + 1
        elif -2.5 < T[i] <= -1.5:
            v[1] = v[1] + 1
        elif -1.5 < T[i] <= -0.5:
            v[2] = v[2] + 1
        elif -0.5 < T[i] <= 0.5:
            v[3] = v[3] + 1
        elif 0.5 < T[i] <= 1.5:
            v[4] = v[4] + 1
        elif 1.5 < T[i] <= 2.5:
            v[5] = v[5] + 1
        elif T[i] > 2.5:
            v[6] = v[6] + 1
    chi_2 = 0
    for i in range(K+1):
        chi_2 = chi_2 + (((v[i] - N*pi[i])**2) / (N*pi[i]))
    p_value = sp.gammaincc(K/2.0, chi_2/2.0)
    with open(dir_location + "/LinearComplexity/stats.txt", 'a') as stats_file:
        stats_file.write("-----------------------------------------------------\n")
        stats_file.write("\tL I N E A R  C O M P L E X I T Y\n")
        stats_file.write("-----------------------------------------------------\n")
        stats_file.write(f"\tM (substring length)     = {M}\n")
        stats_file.write(f"\tN (number of substrings) = {N}\n")
        stats_file.write(f"\tNote: {n % M} bits were discarded!\n")
        stats_file.write("-----------------------------------------------------\n")
        stats_file.write("        F R E Q U E N C Y                            \n")
        stats_file.write("-----------------------------------------------------\n")
        stats_file.write("  C0   C1   C2   C3   C4   C5   C6    CHI2    P-value\n")
        stats_file.write("-----------------------------------------------------\n")
        stats_file.write(" ".join(f"{int(val):4d}" for val in v))
        stats_file.write(f" {chi_2:9.6f}{p_value:9.6f}")
        if p_value < 0 or p_value > 1:
            stats_file.write("WARNING:  P_VALUE IS OUT OF RANGE.\n")
        stats_file.write(f"\t{'FAILURE' if p_value < ALPHA else 'SUCCESS'}\n\n")
    stats_file.close()

    with open(dir_location + "/LinearComplexity/results.txt", 'a') as results_file:
        results_file.write(f"{p_value:.6f}\n")
    results_file.close()