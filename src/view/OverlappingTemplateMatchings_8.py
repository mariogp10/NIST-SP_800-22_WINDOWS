import scipy.special as sp
from scipy.special import gammaln
import numpy as np
ALPHA = 0.01

def OverlappingTemplateMatchings(n, m, random_number, dir_location):
    #pi = [0.364091, 0.185659, 0.139381, 0.100571, 0.070432, 0.139865]
    pi = [0] * 6
    B = [1] * m
    M = 1032
    N = int(n/M)
    V = [0, 0, 0, 0, 0, 0]
    blocks = []
    chain = []
    j = 0
    for i in range(N):
        k = 0
        blocks = blocks + [[]]
        while k < M:
            blocks[i] = blocks[i] + [random_number[j]]
            j = j + 1
            k = k + 1
    #for i in range(N):
    #    start_index = i * M
    #    end_index = start_index + M
    #    blocks.append(random_number[start_index:end_index])
    occurrences = 0
    for block in blocks:
        for i in range(len(block)):
            if (len(chain)<len(B)):
                chain = chain + [block[i]]
            if chain == B:
                occurrences = occurrences + 1
            if (len(chain) == len(B)):
                chain.pop(0)
        chain = []
        if occurrences >= 5:
            V[5] = V[5] + 1
        else:
            V[occurrences] = V[occurrences] + 1
        occurrences = 0

    lambd = (M-m+1)/(2**m)
    eta = lambd/2.0
    pi[0] = np.exp(-eta)
    sum_probs = pi[0]
    for i in range(1,5):
        sum = 0
        for l in range(1,i+1):
            sum = sum + np.exp(-eta - i*np.log(2) + l*np.log(eta) - gammaln(l+1) + gammaln(i) - gammaln(l) - gammaln(i-l+1))
        pi[i] = sum
        sum_probs = sum_probs + pi[i]
    pi[5] = 1 - sum_probs
    chi_2 = 0.0
    for i in range(len(V)):
        chi_2 = chi_2 + ((V[i] - N*pi[i])**2)/(N*pi[i])
    p_value = sp.gammaincc(5.0/2.0, chi_2/2.0)

    with open(dir_location + "/OverlappingTemplateMatchings/stats.txt", 'a') as stats_file:
        stats_file.write("\t\t    OVERLAPPING TEMPLATE OF ALL ONES TEST\n")
        stats_file.write("\t\t-----------------------------------------------\n")
        stats_file.write("\t\tCOMPUTATIONAL INFORMATION:\n")
        stats_file.write("\t\t-----------------------------------------------\n")
        stats_file.write(f"\t\t(a) n (sequence_length)      = {n}\n")
        stats_file.write(f"\t\t(b) m (block length of 1s)   = {m}\n")
        stats_file.write(f"\t\t(c) M (length of substring)  = {M}\n")
        stats_file.write(f"\t\t(d) N (number of substrings) = {N}\n")
        stats_file.write(f"\t\t(e) lambda [(M-m+1)/2^m]     = {lambd:.6f}\n")
        stats_file.write(f"\t\t(f) eta                      = {eta:.6f}\n")
        stats_file.write("\t\t-----------------------------------------------\n")
        stats_file.write("\t\t   F R E Q U E N C Y\n")
        stats_file.write("\t\t  0   1   2   3   4 >=5   Chi^2   P-value  Assignment\n")
        stats_file.write("\t\t-----------------------------------------------\n")
        stats_file.write(f"\t\t{V[0]:3d} {V[1]:3d} {V[2]:3d} {V[3]:3d} {V[4]:3d} {V[5]:3d}  {chi_2:.6f} ")
        if p_value < 0 or p_value > 1:
            stats_file.write("WARNING: P_VALUE IS OUT OF RANGE.\n")
        stats_file.write(f"{p_value:.6f} {'FAILURE' if p_value < ALPHA else 'SUCCESS'}\n\n")
    stats_file.close()

    with open(dir_location + "/OverlappingTemplateMatchings/results.txt", 'a') as results_file:
        results_file.write(f"{p_value:.6f}\n")
    results_file.close()
