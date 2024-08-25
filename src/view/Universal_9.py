import scipy.special as sp
import numpy as np
ALPHA = 0.01

def Universal(n, L, Q, random_number, dir_location):
    expectedValue = [0, 0, 0, 0, 0, 0, 5.2177052, 6.1962507, 7.1836656,
                     8.1764248, 9.1723243, 10.170032, 11.168765,
                     12.168070, 13.167693, 14.167488, 15.167379]
    variance = [0, 0, 0, 0, 0, 0, 2.954, 3.125, 3.238, 3.311, 3.356, 3.384,
                3.401, 3.410, 3.416, 3.419, 3.421]
    Q_bit_chains = []
    K_bit_chains = []
    if n >= 387840:
        L = 6
    if n >= 904960:
        L = 7
    if n >= 2068480:
        L = 8
    if n >= 4654080:
        L = 9
    if n >= 10342400:
        L = 10
    if n >= 22753280:
        L = 11
    if n >= 49643520:
        L = 12
    if n >= 107560960:
        L = 13
    if n >= 231669760:
        L = 14
    if n >= 496435200:
        L = 15
    if n >= 1059061760:
        L = 16
    K = n//L - Q
    if (L < 6) or (L > 16) or (Q < 10*(2**L)):
        with open(dir_location + "/Universal/stats.txt", 'a') as stats_file:
            stats_file.write("\t\tUNIVERSAL STATISTICAL TEST\n")
            stats_file.write("\t\t---------------------------------------------\n")
            if L < 6 or L > 16:
                stats_file.write("\t\tERROR:  L IS OUT OF RANGE.\n")
            if Q < 10*(2**L):
                stats_file.write(f"\t\t-OR- :  Q IS LESS THAN {10 *(2**L):.2f}.\n")
            if n < (Q+K)*L:
                stats_file.write("\t\tERROR:  n IS TOO SHORT.\n")
    else:
        number_of_chains = 0
        table = {}
        sum = 0.0
        for i in range(n-n%L):
            if number_of_chains < Q:
                if i%L == 0:
                    Q_bit_chains = Q_bit_chains + [[]]
                Q_bit_chains[number_of_chains] = Q_bit_chains[number_of_chains] + [random_number[i]]
                if len(Q_bit_chains[number_of_chains]) == L:
                    number_of_chains = number_of_chains + 1
            else:
                if i%L == 0:
                    K_bit_chains = K_bit_chains + [[]]
                K_bit_chains[number_of_chains-Q] = K_bit_chains[number_of_chains-Q] + [random_number[i]]
                if len(K_bit_chains[number_of_chains-Q]) == L:
                    number_of_chains = number_of_chains + 1
        counter = 0
        for i in range(len(Q_bit_chains)):
            counter = counter + 1
            if str(Q_bit_chains[i]) in table:
                table[str(Q_bit_chains[i])] = str(counter)
            else:
                table[str(Q_bit_chains[i])] = str(counter)
        for i in range(len(K_bit_chains)):
            counter = counter + 1
            if str(K_bit_chains[i]) in table:
                sum = sum + np.log2(counter - int(table[str(K_bit_chains[i])]))
                table[str(K_bit_chains[i])] = str(counter)
            else:
                sum = sum + np.log2(counter)
                table[str(K_bit_chains[i])] = str(counter)
        f_n = sum/K
        c = 0.7 - 0.8/L + (4 + 32/L)*((K**(-3/L))/15)
        sigma = c*(variance[L]/K)**(1/2)
        p_value = sp.erfc(abs((f_n - expectedValue[L])/(sigma*((2)**(1/2)))))

        with open(dir_location + "/Universal/stats.txt", 'a') as stats_file:
            stats_file.write("\t\t\tUNIVERSAL STATISTICAL TEST\n")
            stats_file.write("\t\t\t--------------------------------------------\n")
            stats_file.write("\t\t\tCOMPUTATIONAL INFORMATION:\n")
            stats_file.write("\t\t\t--------------------------------------------\n")
            stats_file.write(f"\t\t\t(a) L         = {L}\n")
            stats_file.write(f"\t\t\t(b) Q         = {Q}\n")
            stats_file.write(f"\t\t\t(c) K         = {K}\n")
            stats_file.write(f"\t\t\t(d) sum       = {sum:.6f}\n")
            stats_file.write(f"\t\t\t(e) sigma     = {sigma:.6f}\n")
            stats_file.write(f"\t\t\t(f) variance  = {variance[L]:.6f}\n")
            stats_file.write(f"\t\t\t(g) exp_value = {expectedValue[L]:.6f}\n")
            stats_file.write(f"\t\t\t(h) f_n       = {f_n:.6f}\n")
            stats_file.write(f"\t\t\t(i) WARNING:  {n - (Q + K) * L} bits were discarded.\n")
            stats_file.write("\t\t\t-----------------------------------------\n")
            if p_value < 0 or p_value > 1:
                stats_file.write("WARNING:  P_VALUE IS OUT OF RANGE.\n")
            stats_file.write(f"{'FAILURE' if p_value < ALPHA else 'SUCCESS'}\t\tp_value = {p_value:.6f}\n\n")
        stats_file.close()

        with open(dir_location + "/Universal/results.txt", 'a') as results_file:
            results_file.write(f"{p_value:.6f}\n")
        results_file.close()