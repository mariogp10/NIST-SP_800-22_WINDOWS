from scipy.stats import norm
ALPHA = 0.01

def CumulativeSums(n, random_number, dir_location):
    X = [0] * n
    S_forward = [0] * n
    S_backward = [0] * n
    sum_1_forward = 0
    sum_2_forward = 0
    sum_1_backward = 0
    sum_2_backward = 0
    for i in range(n):
        X[i] = 2*int(random_number[i]) - 1
    for i in range(n):
        if i == 0:
            S_forward[i] = X[i]
            S_backward[i] = X[n-1-i]
        else:
            S_forward[i] = S_forward[i-1] + X[i]
            S_backward[i] = S_backward[i-1] + X[n-1-i]
    # FORWARD
    max_in_S_forward = max(S_forward)
    min_in_S_forward = min(S_forward)
    if abs(max_in_S_forward) >= abs(min_in_S_forward):
        z_forward = abs(max_in_S_forward)
    else:
        z_forward = abs(min_in_S_forward)
    for k in range(int((-n/z_forward + 1)/4), int((n/z_forward - 1)/4 + 1), 1):
        sum_1_forward = sum_1_forward + norm.cdf((4*k+1)*z_forward/(n**(1/2))) - norm.cdf((4*k-1)*z_forward/(n**(1/2)))
    for k in range(int((-n/z_forward - 3)/4), int((n/z_forward - 1)/4 + 1), 1):
        sum_2_forward = sum_2_forward + norm.cdf((4*k+3)*z_forward/(n**(1/2))) - norm.cdf((4*k+1)*z_forward/(n**(1/2)))
    p_value_forward = 1 - sum_1_forward + sum_2_forward
    # END FORWARD

    # BACKWARD
    max_in_S_backward = max(S_backward)
    min_in_S_backward = min(S_backward)
    if abs(max_in_S_backward) >= abs(min_in_S_backward):
        z_backward = abs(max_in_S_backward)
    else:
        z_backward = abs(min_in_S_backward)
    for k in range(int((-n/z_backward + 1)/4), int((n/z_backward - 1)/4 + 1), 1):
        sum_1_backward = sum_1_backward + norm.cdf((4*k+1)*z_backward/(n**(1/2))) - norm.cdf((4*k-1)*z_backward/(n**(1/2)))
    for k in range(int((-n/z_backward - 3)/4), int((n/z_backward - 1)/4 + 1), 1):
        sum_2_backward = sum_2_backward + norm.cdf((4*k+3)*z_backward/(n**(1/2))) - norm.cdf((4*k+1)*z_backward/(n**(1/2)))
    p_value_backward = 1 - sum_1_backward + sum_2_backward
    # END BACKWARD

    # WRITE
    with open(dir_location + "/CumulativeSums/stats.txt", 'a') as stats_file:
        stats_file.write("\t\t      CUMULATIVE SUMS (FORWARD) TEST\n")
        stats_file.write("\t\t-------------------------------------------\n")
        stats_file.write("\t\tCOMPUTATIONAL INFORMATION:\n")
        stats_file.write("\t\t-------------------------------------------\n")
        stats_file.write(f"\t\t(a) The maximum partial sum = {z_forward}\n")
        stats_file.write("\t\t-------------------------------------------\n")
        if p_value_forward < 0 or p_value_forward > 1:
            stats_file.write("WARNING:  P_VALUE IS OUT OF RANGE.\n")
        stats_file.write(f"{'FAILURE' if p_value_forward < ALPHA else 'SUCCESS'}\t\tp_value = {p_value_forward:.6f}\n\n")
        stats_file.write("\t\t      CUMULATIVE SUMS (BACKWARD) TEST\n")
        stats_file.write("\t\t-------------------------------------------\n")
        stats_file.write("\t\tCOMPUTATIONAL INFORMATION:\n")
        stats_file.write("\t\t-------------------------------------------\n")
        stats_file.write(f"\t\t(a) The maximum partial sum = {z_backward}\n")
        stats_file.write("\t\t-------------------------------------------\n")
        if p_value_backward < 0 or p_value_backward > 1:
            stats_file.write("WARNING:  P_VALUE IS OUT OF RANGE.\n")
        stats_file.write(f"{'FAILURE' if p_value_backward < ALPHA else 'SUCCESS'}\t\tp_value = {p_value_backward:.6f}\n\n")
    stats_file.close()

    with open(dir_location + "/CumulativeSums/results.txt", 'a') as results_file:
        results_file.write(f"{p_value_forward:.6f}\n")
        results_file.write(f"{p_value_backward:.6f}\n")
    results_file.close()
