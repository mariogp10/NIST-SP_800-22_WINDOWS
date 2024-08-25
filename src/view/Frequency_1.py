import scipy.special as sp
ALPHA = 0.01

def Frequency(n, random_number, dir_location):
    sum = 0.0
    for i in range(n):
        sum = sum + 2*int(random_number[i]) - 1
    s_obs = abs(sum)/(n**(1/2))
    p_value = sp.erfc(s_obs/(2)**(1/2))

    with open(dir_location + "/Frequency/stats.txt", "a") as stats_file:
        stats_file.write("\t\t\t\t      FREQUENCY TEST\n")
        stats_file.write("\t\t\t---------------------------------------------\n")
        stats_file.write("\t\t\tCOMPUTATIONAL INFORMATION:\n")
        stats_file.write("\t\t\t---------------------------------------------\n")
        stats_file.write(f"\t\t\t(a) The nth partial sum = {int(sum)}\n")
        stats_file.write(f"\t\t\t(b) S_n/n               = {sum / n:.6f}\n")
        stats_file.write("\t\t\t---------------------------------------------\n")
        stats_file.write(f"{'FAILURE' if p_value < ALPHA else 'SUCCESS'}\t\tp_value = {p_value:.6f}\n\n")
    stats_file.close()

    with open(dir_location + "/Frequency/results.txt", "a") as results_file:
        results_file.write(f"{p_value:.6f}\n")
    results_file.close()

