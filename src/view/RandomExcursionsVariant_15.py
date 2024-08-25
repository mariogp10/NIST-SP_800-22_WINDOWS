import scipy.special as sp
ALPHA = 0.01

def RandomExcursionsVariant(n, random_number, dir_location):
    X = [0] * n
    S = [0] * n
    J = 0
    state = [-9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    times_state_occurs = [0]*18
    p_values = [0]*18
    for i in range(n):
        X[i] = 2*int(random_number[i]) - 1
    for i in range(n):
        if i == 0:
            S[i] = X[i]
        else:
            S[i] = S[i-1] + X[i]
    S = [0] + S + [0]
    i = 1
    while i < len(S):
        if S[i] == 0:
            J = J + 1
        elif S[i] in state:
            times_state_occurs[state.index(S[i])] = times_state_occurs[state.index(S[i])] + 1
        i = i + 1
    if J < 500:
        with open(dir_location + "/RandomExcursionsVariant/stats.txt", 'a') as stats_file:
            stats_file.write("\t\t\t  RANDOM EXCURSIONS VARIANT TEST\n")
            stats_file.write("\t\t--------------------------------------------\n")
            stats_file.write("\t\tCOMPUTATIONAL INFORMATION:\n")
            stats_file.write("\t\t--------------------------------------------\n")
            stats_file.write(f"\t\t(a) Number Of Cycles (J) = {J}\n")
            stats_file.write(f"\t\t(b) Sequence Length (n)  = {n}\n")
            stats_file.write("\t\t---------------------------------------------\n")
            stats_file.write("\t\tWARNING:  TEST NOT APPLICABLE.  THERE ARE AN\n")
            stats_file.write("\t\t\t  INSUFFICIENT NUMBER OF CYCLES.\n")
            stats_file.write("\t\t---------------------------------------------\n")
        stats_file.close()
        with open(dir_location + "/RandomExcursionsVariant/results.txt", 'a') as results_file:
            for _ in range(18):
                results_file.write("0.0\n")
        results_file.close()
    else:
        for i in range(len(state)):
            p_values[i] = sp.erfc(abs(times_state_occurs[i] - J) / (2*J*(4*abs(state[i]) - 2))**(1/2))
        p_values = [float(v) for v in p_values]
        with open(dir_location + "/RandomExcursionsVariant/stats.txt", 'a') as stats_file:
            stats_file.write("\t\t\tRANDOM EXCURSIONS VARIANT TEST\n")
            stats_file.write("\t\t--------------------------------------------\n")
            stats_file.write("\t\tCOMPUTATIONAL INFORMATION:\n")
            stats_file.write("\t\t--------------------------------------------\n")
            stats_file.write(f"\t\t(a) Number Of Cycles (J) = {J}\n")
            stats_file.write(f"\t\t(b) Sequence Length (n)  = {n}\n")
            stats_file.write("\t\t--------------------------------------------\n")
            for i in range(18):
                if p_values[i] < 0 or p_values[i] > 1:
                    stats_file.write("WARNING:  P_VALUE IS OUT OF RANGE.\n")
                result_status = "FAILURE" if p_values[i] < ALPHA else "SUCCESS"
                stats_file.write(f"{result_status}\t\tx = {state[i]:2d} Total visits = {times_state_occurs[i]} p_value = {p_values[i]:.6f}\n")
        stats_file.close()

        with open(dir_location + "/RandomExcursionsVariant/results.txt", 'a') as results_file:
            for i in range(18):
                results_file.write(f"{p_values[i]:.6f}\n")
        results_file.close()