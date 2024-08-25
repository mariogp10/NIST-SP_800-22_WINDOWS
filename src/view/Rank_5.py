import numpy as np
import copy
ALPHA = 0.01

def Rank(n, random_number, dir_location):
    M = 32
    Q = 32
    N = n // (M*Q)
    if N ==0:
        p_value = 0.0
        with open(dir_location + "/Rank/stats.txt", 'a') as stats_file:
            stats_file.write("\t\t\t\t\tRANK TEST\n")
            stats_file.write(f"\t\tError: Insufficient # Of Bits To Define A 32x32 (32x32) Matrix\n")
        stats_file.close()
    else:
        matrix = np.zeros((M,Q), dtype=int)
        F_m = 0
        F_m_1 = 0
        P_m = 0
        P_m_1 = 0
        P_m_2 = 0
        # CALCULAMOS LAS PROBABILIDADES
        r = min(M,Q)
        product = 1
        for i in range(r):
            product = product * (((1 - 2**(i-Q)) * (1 - 2**(i-M))) / (1 - 2**(i-r)))
        P_m = product * 2**(r*(Q + M - r) - M*Q)
        product = 1
        r = r - 1
        for i in range(r):
            product = product * (((1 - 2**(i-Q)) * (1 - 2**(i-M))) / (1 - 2**(i-r)))
        P_m_1 = product * 2**(r*(Q + M - r) - M*Q)
        P_m_2 = 1-(P_m + P_m_1)
        r = min(M,Q)

        #EMPEZAMOS A OPERAR
        for k in range(N):
            for i in range(M):
                for j in range(Q):
                    matrix[i][j] = random_number[k*(M*Q)+j+i*M]
            rank = compute_rank(M,Q,matrix)
            if rank == M:
                F_m = F_m + 1
            elif (rank == M - 1):
                F_m_1 = F_m_1 + 1
        chi_2 = ((F_m - P_m*N)**2)/(P_m*N) + ((F_m_1 - P_m_1*N)**2)/(P_m_1*N) + ((N - F_m - F_m_1 - P_m_2*N)**2)/(P_m_2*N)
        p_value = np.exp(-chi_2 / 2.0)
        with open(dir_location + "/Rank/stats.txt", 'a') as stats_file:
            stats_file.write("\t\t\t\t\tRANK TEST\n")
            stats_file.write("\t\t\t---------------------------------------------\n")
            stats_file.write("\t\t\tCOMPUTATIONAL INFORMATION:\n")
            stats_file.write("\t\t\t---------------------------------------------\n")
            stats_file.write(f"\t\t\t(a) Probability P_{r} = {P_m:.6f}\n")
            stats_file.write(f"\t\t\t(b)             P_{r-1} = {P_m_1:.6f}\n")
            stats_file.write(f"\t\t\t(c)             P_{r-2} = {P_m_2:.6f}\n")
            stats_file.write(f"\t\t\t(d) Frequency   F_M = {int(F_m)}\n")
            stats_file.write(f"\t\t\t(e)             F_M-{1} = {int(F_m_1)}\n")
            stats_file.write(f"\t\t\t(f)             N - F_M - F_M-{1} = {int(N-F_m-F_m_1)}\n")
            stats_file.write(f"\t\t\t(g) # of matrices    = {N}\n")
            stats_file.write(f"\t\t\t(h) Chi^2            = {chi_2:.6f}\n")
            stats_file.write(f"\t\t\t(i) NOTE: {n % (32 * 32)} BITS WERE DISCARDED.\n")
            stats_file.write("\t\t\t---------------------------------------------\n")
            if p_value < 0 or p_value > 1:
                stats_file.write("WARNING:  P_VALUE IS OUT OF RANGE.\n")
    with open(dir_location + "/Rank/stats.txt", 'r') as stats_file:
        archivo = stats_file.read()
    line = f"{'FAILURE' if p_value < ALPHA else 'SUCCESS'}\t\tp_value = {p_value:.6f}\n\n"
    new_content = archivo + line
    with open(dir_location + "/Rank/stats.txt", 'w') as stats_file:
        stats_file.write(new_content)
    with open(dir_location + "/Rank/results.txt", 'a') as results_file:
        results_file.write(f"{p_value:.6f}\n")
    results_file.close()


# FUNCTIONS TO CALCULATE BINARY RANK OF A MATRIX
MATRIX_FORWARD_ELIMINATION = 0
MATRIX_BACKWARD_ELIMINATION = 1

def compute_rank(M, Q, matrix):
    m = min(M, Q)
    # FORWARD APPLICATION OF ELEMENTARY ROW OPERATIONS
    for i in range(0, m-1):
        if matrix[i][i] == 1:
            perform_elementary_row_operations(MATRIX_FORWARD_ELIMINATION, i, M, Q, matrix)
        else:
            if find_unit_element_and_swap(MATRIX_FORWARD_ELIMINATION, i, M, Q, matrix) == 1:
                perform_elementary_row_operations(MATRIX_FORWARD_ELIMINATION, i, M, Q, matrix)
    # BACKWARD APPLICATION OF ELEMENTARY ROW OPERATIONS
    for i in range(m - 1, 0, -1):
        if matrix[i][i] == 1:
            perform_elementary_row_operations(MATRIX_BACKWARD_ELIMINATION, i, M, Q, matrix)
        else:
            if find_unit_element_and_swap(MATRIX_BACKWARD_ELIMINATION, i , M, Q, matrix) == 1:
                perform_elementary_row_operations(MATRIX_BACKWARD_ELIMINATION, i, M, Q, matrix)
    rank = determine_rank(m, M, Q, matrix)
    return rank

def perform_elementary_row_operations(flag, i, M, Q, matrix):
    if flag == 0:
        for j in range(i+1,M):
            if matrix[j][i] == 1:
                for k in range(i,Q):
                    matrix[j][k] = (matrix[j][k] + matrix[i][k]) % 2
    else:
        for j in range(i - 1, -1, -1):
            if matrix[j][i] == 1:
                for k in range(Q):
                    matrix[j][k] = (matrix[j][k] + matrix[i][k]) % 2

def find_unit_element_and_swap(flag, i , M, Q, matrix):
    row_op = 0
    if flag == 0:
        index = i + 1
        while index < M and matrix[index][i] == 0:
            index = index + 1
        if index < M:
            row_op = swap_rows(i, index, Q, matrix)
    else:
        index = i - 1
        while index >= 0 and matrix[index][i] == 0:
            index = index - 1
        if index >= 0:
            row_op = swap_rows(i, index, Q, matrix)
    return row_op

def swap_rows(i, index, Q, matrix):
    for p in range(Q):
        temp = matrix[i][p]
        matrix[i][p] = matrix[index][p]
        matrix[index][p] = temp
    return 1

def determine_rank(m, M, Q, matrix):
    rank = m
    for i in range(M):
        allZeroes = 1
        for j in range(Q):
            if matrix[i][j] == 1:
                allZeroes = 0
                break
        if allZeroes == 1:
            rank = rank - 1
    return rank
