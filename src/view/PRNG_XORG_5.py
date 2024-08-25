def PRNG_XORG_5(seed, length, number_of_chains):
    results = []
    for bit in seed:
        results.append(int(bit))
    for i in range(127, length*number_of_chains):
        results.append((results[i-127] + results[i-1]) % 2)
    return results

def transform_to_format(seed, length, number_of_chains):
    result = PRNG_XORG_5(seed, length, number_of_chains)
    prn = []
    results = []
    for bit in result:
        prn.append(bit)
        if len(prn) == length:
            results.append(prn)
            prn = []
        if len(results) == number_of_chains:
            break
    return results

#semilla = "0001111100110000101001100100010101001001110110001010111010110000111110000000011011110111001001110000110001100011100011111010101"
#lista_de_listas = transform_to_format(semilla, 1000000, 1)
#lista = lista_de_listas[0]
#bit_string = ''.join(str(bit) for bit in lista)
#with open('output.txt', 'w') as file:
#    file.write(bit_string)