import scipy.special as sp
ALPHA = 0.01

def BlockFrequency(n, M, random_number, dir_location):
    N = n//M
    sum = 0.0
    for i in range(N):
        BlockSum = 0
        for j in range(M):
            BlockSum = BlockSum + random_number[j + i*M]
        pi = BlockSum / M
        v = pi - 0.5
        sum = sum + v**2
    chi_squared = 4.0 * M * sum
    p_value = sp.gammaincc(N / 2.0, chi_squared / 2.0)

    with open(dir_location + "/BlockFrequency/stats.txt", 'a') as stats_file:
        stats_file.write("\t\t\t\tBLOCK FREQUENCY TEST\n")
        stats_file.write("\t\t\t---------------------------------------------\n")
        stats_file.write("\t\t\tCOMPUTATIONAL INFORMATION:\n")
        stats_file.write("\t\t\t---------------------------------------------\n")
        stats_file.write(f"\t\t\t(a) Chi^2           = {chi_squared:.6f}\n")
        stats_file.write(f"\t\t\t(b) # of substrings = {N}\n")
        stats_file.write(f"\t\t\t(c) block length    = {M}\n")
        stats_file.write(f"\t\t\t(d) Note: {n % M} bits were discarded.\n")
        stats_file.write("\t\t\t---------------------------------------------\n")
        stats_file.write(f"{'FAILURE' if p_value < ALPHA else 'SUCCESS'}\t\tp_value = {p_value:.6f}\n\n")
    stats_file.close()

    with open(dir_location + "/BlockFrequency/results.txt", 'a') as results_file:
        results_file.write(f"{p_value:.6f}\n")
    results_file.close()
