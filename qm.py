import implicant as imp

def minimize(args):
    '''
    Minimizes the given minterms and don't care conditions
    returns two strings representing the minimized function in SOP and POS form
    '''
    if args == []:
        return ['NONE', 'NONE']

    minterms = remove_duplicates(args[0])
    dcs = [] if len(args) < 2 else remove_duplicates(args[1])

    if terms_overlap(minterms, dcs):
        return ['NONE', 'NONE']

    literals = num_literals(max(minterms + dcs))
    imp_list = generate_implicants(minterms, dcs, literals)
    pi_list = implicate(imp_list)
    
    # lo - leftover
    [lo_minterms, lo_pi, epi_list] = extract_epi(minterms, pi_list)
    
    sop = '='
    pos = '='
    if lo_minterms == []:
        # no need to petrick
        for epi in epi_list:
            sop += epi.boolean_product(literals) + '+'
        sop = sop[:-1]
        for epi in epi_list:
            pos += '(' + epi.boolean_dual(literals) + ')'
    else:
        pass

    return [sop, pos]


def remove_duplicates(li):
    return list(set(li))


def terms_overlap(minterms, dcs):
    return (set(minterms) & set(dcs)) != set()


def hamming_weight(num):
    return bin(num).count('1')


def num_literals(num):
    return len(bin(num)) - 2


def generate_implicants(minterms, dcs, literals):
    '''
    Given a list of minterms and don't care conditions, generates implicants
    returns list of list of implicants grouped by hamming weight
    '''
    #list of sets of implicants
    imp_los = [set() for i in range(literals + 1)]
    for term in minterms:
        imp_los[hamming_weight(term)].add(imp.Implicant(term))
    for term in dcs:
        imp_los[hamming_weight(term)].add(imp.Implicant(term))
    return imp_los


def implicate(implicants):
    '''
    Groups implicants and recurses
    returns a list of all prime implicants
    '''
    num_elem = len(implicants)
    if implicants.count(set()) == num_elem:
        return []
    if num_elem == 1:
        return list(implicants[0])

    pi_list = []
    next_imps = [set() for i in range(num_elem - 1)]
    for i in range(num_elem - 1):
        for imp1 in implicants[i]:
            for imp2 in implicants[i + 1]:
                if imp1.is_adjacent(imp2):
                    next_imps[i].add(imp1.merge(imp2))
                    imp1.mark_not_prime()
                    imp2.mark_not_prime()
            if imp1.prime:
                pi_list.append(imp1)
    for imp in implicants[-1]:
        if imp.prime:
            pi_list.append(imp)

    pi_list.extend(implicate(next_imps))
    return pi_list


def extract_epi(minterms, primes):
    '''
    returns list of essential prime implicants
    '''
    epi_list = []
    still_extracting = True
    while still_extracting:
        [covered, inner_epis, still_extracting] = extract(minterms, primes)
        minterms = list(set(minterms) - covered)
        primes = list(set(primes) - set(inner_epis))
        epi_list.extend(list(set(inner_epis)))
    return [minterms, primes, epi_list]


def extract(minterms, primes):
    '''
    extracts essential prime implicants
    returns:
        minterms covered by epi
        epis extracted
        whether more epis can be extracted
    '''
    cover = set()
    epi = []

    if len(minterms) == 1:
        epi.append(primes.pop())
        minterms = []

    for m in minterms:
        #list of prime implicants that cover m
        pi_cover = []
        for pi in primes:
            if m in pi.minterms:
                pi_cover.append(pi)
        if len(pi_cover) == 1:
            epi.append(pi_cover.pop())

    for e in epi:
        cover.update(e.minterms)

    return [cover, epi, cover != set()]
