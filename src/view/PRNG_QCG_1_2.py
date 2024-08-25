def PRNG_QCG_1_2(p, seed_hex, length, number_of_chains):
    seed = int(seed_hex,16)
    p = int(p,16)
    results = []
    for _ in range(((length * number_of_chains)//512) + 1):
        bin_str = bin(seed)[2:]
        results.append(bin_str.zfill(512))
        seed = (2*(seed**2) + 3*seed + 1) % p
    return ''.join(results)

def transform_to_format(p, seed_hex, length, number_of_chains):
    result = PRNG_QCG_1_2(p, seed_hex, length, number_of_chains)
    prn = []
    results = []
    for bit in result:
        prn.append(int(bit))
        if len(prn) == length:
            results.append(prn)
            prn = []
        if len(results) == number_of_chains:
            break
    print(len(results))
    return results
