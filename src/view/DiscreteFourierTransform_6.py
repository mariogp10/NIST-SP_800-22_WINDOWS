import scipy.special as sp
import numpy as np
ALPHA = 0.01

def DiscreteFourierTransform(n, random_number, dir_location):
    X = [0]*n
    m = [0]*int(n/2)
    N_1 = 0
    for i in range(n):
        X[i] = 2*int(random_number[i]) - 1
    S = np.fft.fft(X)
    m[0] = np.sqrt(S[0].real**2 + S[0].imag**2)
    for i in range(int(n / 2)-1):
        m[i+1] = np.sqrt(S[i+1].real**2 + S[i+1].imag**2)
    T = (n*np.log(1/0.05))**(1/2)
    N_0 = 0.95*n/2
    for i in range(len(m)):
        if (round(m[i],6) < round(T,6)):
            N_1 = N_1 + 1
    d = (N_1 - N_0) / (n * 0.95 * 0.05 / 4.0)**(1/2)
    p_value = sp.erfc(abs(d) / (2)**(1/2))
    with open(dir_location + "/DiscreteFourierTransform/stats.txt", 'a') as stats_file:
        stats_file.write("\t\t\t\t\tFFT TEST\n")
        stats_file.write("\t\t\t-------------------------------------------\n")
        stats_file.write("\t\t\tCOMPUTATIONAL INFORMATION:\n")
        stats_file.write("\t\t\t-------------------------------------------\n")
        stats_file.write(f"\t\t\t(a) N_1        = {N_1:.6f}\n")
        stats_file.write(f"\t\t\t(b) N_0        = {N_0:.6f}\n")
        stats_file.write(f"\t\t\t(c) d          = {d:.6f}\n")
        stats_file.write("\t\t\t-------------------------------------------\n")
        stats_file.write(f"{'FAILURE' if p_value < ALPHA else 'SUCCESS'}\t\tp_value = {p_value:.6f}\n\n")
    stats_file.close()

    with open(dir_location + "/DiscreteFourierTransform/results.txt", 'a') as results_file:
        results_file.write(f"{p_value:.6f}\n")
    results_file.close()