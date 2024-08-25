import scipy.special as sp
ALPHA = 0.01

def Runs(n, random_number, dir_location):
    S = 0.0
    for i in random_number:
        S = S + i
    pi = S/n
    if abs(pi - 0.5) >= (2.0 / n**(1/2)):
        p_value = 0.0
        with open(dir_location + "/Runs/stats.txt", 'a') as stats_file:
            stats_file.write("\t\t\t\t\tRUNS TEST\n")
            stats_file.write("\t\t\t------------------------------------------\n")
            stats_file.write(f"\t\t\tPI ESTIMATOR CRITERIA NOT MET! PI = {pi:.6f}\n")
        stats_file.close()
    else:
        V = 1
        for j in range(0,n - 1):
            if random_number[j] != random_number[j+1]:
                V = V + 1
        p_value = sp.erfc(abs(V - 2*n*pi*(1-pi)) / (((2*n)**(1/2))*2*pi*(1-pi)))
        with open(dir_location + "/Runs/stats.txt", 'a') as stats_file:
            stats_file.write("\t\t\t\t\tRUNS TEST\n")
            stats_file.write("\t\t\t------------------------------------------\n")
            stats_file.write("\t\t\tCOMPUTATIONAL INFORMATION:\n")
            stats_file.write("\t\t\t------------------------------------------\n")
            stats_file.write(f"\t\t\t(a) Pi                        = {pi:.6f}\n")
            stats_file.write(f"\t\t\t(b) V_n_obs (Total # of runs) = {int(V)}\n")
            stats_file.write("\t\t\t(c) V_n_obs - 2 n pi (1-pi)\n")
            stats_file.write(f"\t\t\t    -----------------------   = {abs(V - 2*n*pi*(1-pi)) / (((2*n)**(1/2))*2*pi*(1-pi)):.6f}\n")
            stats_file.write("\t\t\t      2 sqrt(2n) pi (1-pi)\n")
            stats_file.write("\t\t\t------------------------------------------\n")
            if p_value < 0 or p_value > 1:
                stats_file.write("WARNING:  P_VALUE IS OUT OF RANGE.\n")
            stats_file.write(f"{'FAILURE' if p_value < ALPHA else 'SUCCESS'}\t\tp_value = {p_value:.6f}\n\n")
        stats_file.close()

    with open(dir_location + "/Runs/results.txt", 'a') as results_file:
        results_file.write(f"{p_value:.6f}\n")