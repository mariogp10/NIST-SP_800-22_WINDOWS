import scipy.special as sp
ALPHA = 0.01

# TODOS LOS VALORES DE M, K, V, PI SE HAN OBTENIDO DEL PDF DE NIST
def LongestRunOfOnes(n, random_number, dir_location):
    if n < 128:
        with open(dir_location + "/LongestRunOfOnes/stats.txt", 'a') as stats_file:
            stats_file.write("\t\t\t\t\t  LONGEST RUNS OF ONES TEST\n")
            stats_file.write("\t\t\t------------------------------------------\n")
            stats_file.write(f"\t\t\t   n={n} is too short\n")
        stats_file.close()
        return
    elif n < 6572:
        M = 8
        K = 3
        # V sirve para tomar una referencia a la hora de contabilizar la longitud de las cadenas
        # el vector nu nos indica cuantas cadenas de longitud M con rachas de V[i] unos hay
        # en cada número aleatorio
        V = [1, 2, 3, 4]
        nu = [0, 0, 0, 0]
        #pi = [0.2148, 0.3672, 0.2305, 0.1875]
        pi = [0.21484375, 0.3671875, 0.23046875, 0.1875]
    elif n < 750000:
        M = 128
        K = 5
        V = [4, 5, 6, 7, 8, 9]
        nu = [0, 0, 0, 0, 0, 0]
        #pi = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
        pi = [0.1174035788, 0.242955959, 0.249363483, 0.17517706, 0.102701071, 0.112398847]
    else:
        M = 10000
        K = 6
        V = [10, 11, 12, 13, 14, 15, 16]
        nu = [0, 0, 0, 0, 0, 0, 0]
        pi = [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]
    N = n//M
    for i in range(N):
        max_run_of_ones = 0
        current_run_of_ones = 0
        for j in range(M):
            if random_number[i*M + j] == 1:
                current_run_of_ones = current_run_of_ones + 1
                if current_run_of_ones > max_run_of_ones:
                    max_run_of_ones = current_run_of_ones
            else:
                current_run_of_ones = 0
        if max_run_of_ones < V[0]:
            nu[0] = nu[0] + 1
        for j in range(K + 1):
            if max_run_of_ones == V[j]:
                nu[j] = nu[j] + 1
        if max_run_of_ones > V[K]:
            nu[K] = nu[K] + 1
    chi_2 = 0.0
    i = 0
    while (i < K + 1):
        chi_2 = chi_2 + (((nu[i] - N*pi[i])**2) / (N*pi[i]))
        i = i + 1
    p_value = sp.gammaincc(K / 2.0, chi_2 / 2.0)

    with open(dir_location + "/LongestRunOfOnes/stats.txt", 'a') as stats_file:
        stats_file.write("\t\t\t  LONGEST RUNS OF ONES TEST\n")
        stats_file.write("\t\t---------------------------------------------\n")
        stats_file.write("\t\tCOMPUTATIONAL INFORMATION:\n")
        stats_file.write("\t\t---------------------------------------------\n")
        stats_file.write(f"\t\t(a) N (# of substrings)  = {N}\n")
        stats_file.write(f"\t\t(b) M (Substring Length) = {M}\n")
        stats_file.write(f"\t\t(c) Chi^2                = {chi_2:.6f}\n")
        stats_file.write("\t\t---------------------------------------------\n")
        stats_file.write("\t\t      F R E Q U E N C Y\n")
        stats_file.write("\t\t---------------------------------------------\n")

        if K == 3:
            stats_file.write("\t\t  <=1     2     3    >=4   P-value  Assignment")
            stats_file.write(f"\n\t\t {nu[0]:3d} {nu[1]:3d} {nu[2]:3d}  {nu[3]:3d} ")
        elif K == 5:
            stats_file.write("\t\t<=4  5  6  7  8  >=9 P-value  Assignment")
            stats_file.write(f"\n\t\t {nu[0]:3d} {nu[1]:3d} {nu[2]:3d} {nu[3]:3d} {nu[4]:3d}  {nu[5]:3d} ")
        else:
            stats_file.write("\t\t<=10  11  12  13  14  15 >=16 P-value  Assignment")
            stats_file.write(f"\n\t\t {nu[0]:3d} {nu[1]:3d} {nu[2]:3d} {nu[3]:3d} {nu[4]:3d} {nu[5]:3d}  {nu[6]:3d} ")

        if p_value < 0 or p_value > 1:
            stats_file.write("WARNING:  P_VALUE IS OUT OF RANGE.\n")

        stats_file.write(f"{'FAILURE' if p_value < ALPHA else 'SUCCESS'}\t\tp_value = {p_value:.6f}\n\n")
    stats_file.close()

    with open(dir_location + "/LongestRunOfOnes/results.txt", 'a') as results_file:
        results_file.write(f"{p_value:.6f}\n")
    results_file.close()