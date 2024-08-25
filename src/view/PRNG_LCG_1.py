def PRNG_LCG(z0, a, length, number_of_chains):
    mod = 2**31 - 1
    z = z0
    prn = []
    result = []
    n_0s = 0
    uniform_value = z / mod
    if uniform_value <= 0.5:
        prn.append(0)
        n_0s = n_0s + 1
    else:
        prn.append(1)
    for i in range(number_of_chains):
        if i == 0:
            valor = length - 1
        else:
            valor = length
        for _ in range(valor):
            z = (a * z) % mod
            uniform_value = z / mod
            if uniform_value <= 0.5:
                prn.append(0)
                n_0s = n_0s + 1
            else:
                prn.append(1)
            if len(prn) == length:
                result.append(prn)
                prn = []
    return result

#lista_de_lista_XORG = PRNG_LCG(3962406, 1103515245, 127, 1)
#lista_de_XORG = lista_de_lista_XORG[0]
#bit_string = ''.join(str(bit) for bit in lista_de_XORG)
#print(bit_string)