import scipy.special as sp
import numpy as np
ALPHA = 0.01

def ApproximateEntropy(n, m, random_number, dir_location):
    original_random_number = random_number
    phi_m = 0
    phi_m_plus_1 = 0
    chi_2 = 0.0

    block = []
    Count_tuples = [0] * 2**m
    C = [0] * 2**m
    for i in range(m-1):
        random_number = random_number + [original_random_number[i]]
    for i in range(len(random_number)):
        block = block + [random_number[i]]
        if len(block) != m:
            pass
        else:
            C_subindex = 0
            for j in range(m):
                C_subindex = C_subindex + block[j]*(2**(m-1-j))
            Count_tuples[C_subindex] = Count_tuples[C_subindex] + 1
            block.pop(0)
    for i in range(2**m):
        C[i] = Count_tuples[i]/n
    for i in range(2**m):
        if C[i] == 0:
            pass
        else:
            phi_m = phi_m + C[i]*np.log(C[i])

    block = []
    Count_tuples = [0] * 2**(m+1)
    C = [0] * 2**(m+1)
    random_number = original_random_number
    for i in range(m):
        random_number = random_number + [original_random_number[i]]
    for i in range(len(random_number)):
        block = block + [random_number[i]]
        if len(block) != (m+1):
            pass
        else:
            C_subindex = 0
            for j in range((m+1)):
                C_subindex = C_subindex + block[j]*(2**(m-j))
            Count_tuples[C_subindex] = Count_tuples[C_subindex] + 1
            block.pop(0)
    for i in range(2**(m+1)):
        C[i] = Count_tuples[i]/n
    for i in range(2**(m+1)):
        if C[i] == 0:
            pass
        else:
            phi_m_plus_1 = phi_m_plus_1 + C[i]*np.log(C[i])

    chi_2 = 2*n*(np.log(2) - (phi_m - phi_m_plus_1))
    p_value = sp.gammaincc(2**(m-1), chi_2/2)
    with open(dir_location + "/ApproximateEntropy/stats.txt", 'a') as stats_file:
        stats_file.write("\t\t\t\tAPPROXIMATE ENTROPY TEST\n")
        stats_file.write("\t\t\t--------------------------------------------\n")
        stats_file.write("\t\t\tCOMPUTATIONAL INFORMATION:\n")
        stats_file.write("\t\t\t--------------------------------------------\n")
        stats_file.write(f"\t\t\t(a) m (block length)    = {m}\n")
        stats_file.write(f"\t\t\t(b) n (sequence length) = {n}\n")
        stats_file.write(f"\t\t\t(c) Chi^2               = {chi_2:.6f}\n")
        stats_file.write(f"\t\t\t(d) Phi(m)              = {phi_m:.6f}\n")
        stats_file.write(f"\t\t\t(e) Phi(m+1)            = {phi_m_plus_1:.6f}\n")
        stats_file.write(f"\t\t\t(f) ApEn                = {phi_m - phi_m_plus_1:.6f}\n")
        stats_file.write(f"\t\t\t(g) Log(2)              = {np.log(2.0):.6f}\n")
        stats_file.write("\t\t\t--------------------------------------------\n")
        if m > (int(np.log2(n)) - 5):
            stats_file.write(f"\t\t\tNote: The blockSize = {m} exceeds recommended value of {int(np.log2(n)) - 5}\n")
            stats_file.write("\t\t\tResults are inaccurate!\n")
            stats_file.write("\t\t\t--------------------------------------------\n")
        stats_file.write(f"{'FAILURE' if p_value < ALPHA else 'SUCCESS'}\t\tp_value = {p_value:.6f}\n\n")
    stats_file.close()

    with open(dir_location + "/ApproximateEntropy/results.txt", 'a') as results_file:
        results_file.write(f"{p_value:.6f}\n")
    results_file.close()