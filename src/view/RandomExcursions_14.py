import scipy.special as sp
ALPHA = 0.01

def RandomExcursions(n, random_number, dir_location):
    X = [0] * n
    S = [0] * n
    J = 0
    cycles = [[0]]
    frequency_of_states = []
    state = [-4, -3, -2, -1, 1, 2, 3, 4]
    table = []
    chi_2 = [0]*8
    p_values = [0]*8
    #pi = [[0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
    #      [0.5000, 0.2500, 0.1250, 0.0625, 0.0312, 0.0312],
    #      [0.7500, 0.0625, 0.0469, 0.0352, 0.0264, 0.0791],
    #      [0.8333, 0.0278, 0.0231, 0.0193, 0.0161, 0.0804],
    #      [0.8750, 0.0156, 0.0137, 0.0120, 0.0105, 0.0733]]
    pi = [[0.0000000000, 0.00000000000, 0.00000000000, 0.00000000000, 0.00000000000, 0.0000000000],
         [0.5000000000, 0.25000000000, 0.12500000000, 0.06250000000, 0.03125000000, 0.0312500000],
         [0.7500000000, 0.06250000000, 0.04687500000, 0.03515625000, 0.02636718750, 0.0791015625],
         [0.8333333333, 0.02777777778, 0.02314814815, 0.01929012346, 0.01607510288, 0.0803755143],
         [0.8750000000, 0.01562500000, 0.01367187500, 0.01196289063, 0.01046752930, 0.0732727051]]
    for i in range(n):
        X[i] = 2*int(random_number[i]) - 1
    for i in range(n):
        if i == 0:
            S[i] = X[i]
        else:
            S[i] = S[i-1] + X[i]
    S = [0] + S + [0]
    for i in range(1,len(S)):
        cycles[J].append(S[i])
        if S[i] == 0:
            cycles.append([0])
            J = J + 1
    cycles.pop()
    if J < 500:
        with open(dir_location + "/RandomExcursions/stats.txt", 'a') as stats_file:
            stats_file.write("\t\t\t  RANDOM EXCURSIONS TEST\n")
            stats_file.write("\t\t--------------------------------------------\n")
            stats_file.write("\t\tCOMPUTATIONAL INFORMATION:\n")
            stats_file.write("\t\t--------------------------------------------\n")
            stats_file.write(f"\t\t(a) Number Of Cycles (J) = {J:04d}\n")
            stats_file.write(f"\t\t(b) Sequence Length (n)  = {n}\n")
            stats_file.write("\t\t---------------------------------------------\n")
            stats_file.write("\t\tWARNING:  TEST NOT APPLICABLE.  THERE ARE AN\n")
            stats_file.write("\t\t\t  INSUFFICIENT NUMBER OF CYCLES.\n")
            stats_file.write("\t\t---------------------------------------------\n")
        stats_file.close()
        with open(dir_location + "/RandomExcursions/results.txt", 'a') as results_file:
            for _ in range(8):
                results_file.write("0.0\n")
        results_file.close()
    else:
        for i in range(len(cycles)):
            frequency_of_states = frequency_of_states + [[0]*8]
            for j in range(len(cycles[i])):
                if cycles[i][j] in state:
                    frequency_of_states[i][state.index(cycles[i][j])] = frequency_of_states[i][state.index(cycles[i][j])] + 1
        for i in range(len(state)):
            table = table + [[0]*6]
            for j in range(J):
                freq = frequency_of_states[j][i]
                if freq >= 5:
                    table[i][5] = table[i][5] + 1
                else:
                    table[i][freq] = table[i][freq] + 1
        k = 0
        for i in state:
            for j in range(6):
                chi_2[k] = chi_2[k] + ((table[k][j] - J*pi[abs(i)][j])**2/(J*pi[abs(i)][j]))
            k = k + 1
        for i in range(len(state)):
            p_values[i] = sp.gammaincc(5 / 2, chi_2[i] / 2)
        p_values = [float(v) for v in p_values]
        with open(dir_location + "/RandomExcursions/stats.txt", 'a') as stats_file:
            stats_file.write("\t\t\t  RANDOM EXCURSIONS TEST\n")
            stats_file.write("\t\t--------------------------------------------\n")
            stats_file.write("\t\tCOMPUTATIONAL INFORMATION:\n")
            stats_file.write("\t\t--------------------------------------------\n")
            stats_file.write(f"\t\t(a) Number Of Cycles (J) = {J:04d}\n")
            stats_file.write(f"\t\t(b) Sequence Length (n)  = {n}\n")
            stats_file.write(f"\t\t(c) Rejection Constraint = {500:04d}\n")
            stats_file.write("\t\t-------------------------------------------\n")
            for i in range(8):
                if p_values[i] < 0 or p_values[i] > 1:
                    stats_file.write("WARNING:  P_VALUE IS OUT OF RANGE.\n")
                result_status = "FAILURE" if p_values[i] < ALPHA else "SUCCESS"
                stats_file.write(f"{result_status}\t\tx = {state[i]:2d} chi^2 = {chi_2[i]:9.6f} p_value = {p_values[i]:.6f}\n")
        stats_file.close()

        with open(dir_location + "/RandomExcursions/results.txt", 'a') as results_file:
            for i in range(8):
                results_file.write(f"{p_values[i]:.6f}\n")
        results_file.close()