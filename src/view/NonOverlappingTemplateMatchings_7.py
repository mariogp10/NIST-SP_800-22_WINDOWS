import scipy.special as sp
ALPHA = 0.01

def NonOverlappingTemplateMatchings(n, m, random_number, dir_location):
    N = 8
    M = n//N
    nu = (M-m+1)/(2**m)
    sigma_2 = M*((1/(2**m)) - ((2*m-1)/(2**(2*m))))
    directorio = "C:/Users/mario/Desktop/CUARTO/TFG/APP_TFG/templates/template" + str(m)
    with open(dir_location + "/NonOverlappingTemplateMatchings/stats.txt", 'a') as stats_file:
        stats_file.write("\t\t  NONPERIODIC TEMPLATES TEST\n")
        stats_file.write("-------------------------------------------------------------------------------------\n")
        stats_file.write("\t\t  COMPUTATIONAL INFORMATION\n")
        stats_file.write("-------------------------------------------------------------------------------------\n")
        stats_file.write(f"\tNU = {nu:.6f}\tM = {M}\tN = {N}\tm = {m}\tn = {n}\n")
        stats_file.write("-------------------------------------------------------------------------------------\n")
        stats_file.write("\t\tF R E Q U E N C Y\n")
        stats_file.write("Template   W_1  W_2  W_3  W_4  W_5  W_6  W_7  W_8    Chi^2   P_value Assignment Index\n")
        stats_file.write("-------------------------------------------------------------------------------------\n")
    with (open(directorio, "r") as templates_files):
        jj = 0
        for line in templates_files:
            processed_line = line.strip().replace(' ', '')
            B = []
            for char in processed_line:
                # Comprobar si el carácter es '0' o '1'
                if char in '01':
                    # Convertir el carácter a entero y añadir a la lista
                    B.append(int(char))

            W = []
            blocks = []
            chain = []
            j = 0
            for i in range(N):
                W = W + [0]
                k = 0
                blocks = blocks + [[]]
                blocks[i] = [0]*int(M)
                while k < M:
                    blocks[i][k] = random_number[j]
                    j = j + 1
                    k = k + 1
            block_number = 0
            for block in blocks:
                for i in range(len(block)):
                    chain = chain + [block[i]]
                    if chain == B:
                        W[block_number] = W[block_number] + 1
                        chain = []
                    if (len(chain) == len(B)):
                        chain.pop(0)
                block_number = block_number + 1
                chain = []
            chi_2 = 0.0
            for i in range(len(W)):
                chi_2 = chi_2 + ((W[i] - nu)**2)/sigma_2
            p_value = sp.gammaincc(N/2.0, chi_2/2.0)

            with open(dir_location + "/NonOverlappingTemplateMatchings/stats.txt", 'a') as stats_file:
                if p_value < 0 or p_value > 1:
                    stats_file.write("WARNING:  P_VALUE IS OUT OF RANGE.\n")
                B_str =''.join(str(num) for num in B)
                stats_file.write(f"{B_str}")
                for i in range(8):
                    stats_file.write(f"{W[i]:5d}")
                stats_file.write(f" {chi_2:9.6f} {p_value:9.6f} \t{'FAILURE' if p_value < ALPHA else 'SUCCESS'} {jj:3d}\n")
            stats_file.close()
            if jj == 0:
                with open(dir_location + "/NonOverlappingTemplateMatchings/results.txt", 'a') as results_file:
                    results_file.write(f"{p_value:.6f}\n")
                results_file.close()
            else:
                with open(dir_location + "/NonOverlappingTemplateMatchings/results.txt", 'a') as results_file:
                    results_file.write(f"{p_value:.6f}\n")
                results_file.close()
            jj = jj + 1
    templates_files.close()