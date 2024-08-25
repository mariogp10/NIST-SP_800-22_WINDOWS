import scipy.special as sp
import numpy as np
ALPHA = 0.01

def SerialTest(n, m, random_number, dir_location):
    for i in range(m):
        random_number = random_number + [random_number[i]]
    psim_0 = psi2(m, n, random_number)
    psim_1 = psi2(m-1, n, random_number)
    psim_2 = psi2(m-2, n, random_number)
    grad1 = psim_0 - psim_1
    grad2 = psim_0 - 2*psim_1 + psim_2
    p_value1 = sp.gammaincc(2**(m-2), grad1/2.0)
    p_value2 = sp.gammaincc(2**(m-3), grad2/2.0)

    with open(dir_location + "/SerialTest/stats.txt", 'a') as stats_file:
        stats_file.write("\t\t\t\t       SERIAL TEST\n")
        stats_file.write("\t\t\t---------------------------------------------\n")
        stats_file.write("\t\t\t COMPUTATIONAL INFORMATION:          \n")
        stats_file.write("\t\t\t---------------------------------------------\n")
        stats_file.write(f"\t\t\t(a) Block length    (m) = {m}\n")
        stats_file.write(f"\t\t\t(b) Sequence length (n) = {n}\n")
        stats_file.write(f"\t\t\t(c) Psi_m               = {psim_0:.6f}\n")
        stats_file.write(f"\t\t\t(d) Psi_m-1             = {psim_1:.6f}\n")
        stats_file.write(f"\t\t\t(e) Psi_m-2             = {psim_2:.6f}\n")
        stats_file.write(f"\t\t\t(f) Del_1               = {grad1:.6f}\n")
        stats_file.write(f"\t\t\t(g) Del_2               = {grad2:.6f}\n")
        stats_file.write("\t\t\t---------------------------------------------\n")
        stats_file.write(f"{'FAILURE' if p_value1 < ALPHA else 'SUCCESS'}\t\tp_value = {p_value1:.6f}\n")
        stats_file.write(f"{'FAILURE' if p_value2 < ALPHA else 'SUCCESS'}\t\tp_value = {p_value2:.6f}\n\n")
    stats_file.close()

    with open(dir_location + "/SerialTest/results.txt", 'a') as results_file:
        results_file.write(f"{p_value1:.6f}\n")
        results_file.write(f"{p_value2:.6f}\n")
    results_file.close()


def psi2(m, n, random_number):
    if m == 0:
        return 0.0
    pow_len = 2**(m + 1) - 1
    P = np.zeros(pow_len, dtype=int)

    for i in range(n):
        k = 1
        for j in range(m):
            if random_number[(i + j) % n] == 0:
                k = 2 * k
            else:
                k = 2 * k + 1
        P[k - 1] += 1

    sum_ = np.sum(P[(2**m - 1):(2**(m + 1) - 1)]**2)
    sum_ = (sum_ * 2**m / n) - n

    return sum_