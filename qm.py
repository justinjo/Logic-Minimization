import implicant as imp

def minimize(args):
    '''minimizes the given minterms and don't care conditions
    returns two strings representing the minimized function in SOP and POS form
    '''
    if len(args) < 1:
        return ['NONE', 'NONE']
    minterms = remove_duplicates(args[0])
    dcs = [] if len(args) < 2 else remove_duplicates(args[1])

    if terms_overlap(minterms, dcs):
        return ['NONE', 'NONE']

    imp_list = generate_implicants(minterms, dcs)
    pi_list = implicate(imp_list)
    # lo - leftover
    [lo_minterms, lo_pi, epi_list] = extract(minterms, pi_list)
    if lo_minterms == []:
        # no need to petrick
        print('NO NEED TO PETRICK')
    else:
        print('PETRICK TIME')
        pass
    
    return ['SOP', 'POS']


def remove_duplicates(li):
    return list(set(li))

def terms_overlap(minterms, dcs):
    return (set(minterms) & set(dcs)) != set()

def hamming_weight(num):
    '''returns the hamming weight of a number
    '''
    return bin(num).count('1')


def num_literals(num):
    '''returns the number of literals required to represent given number
    '''
    return len(bin(num)) - 2


def generate_implicants(minterms, dcs):
    '''given a list of minterms and don't care conditions, generates implicants
    returns list of list of implicants grouped by hamming weight
    '''
    max_term = max(max(minterms, dcs))
    literals = num_literals(max_term)
    #list of sets of implicants
    imp_los = [set() for i in range(literals + 1)]
    for term in minterms:
        imp_los[hamming_weight(term)].add(imp.Implicant(term))
    for term in dcs:
        imp_los[hamming_weight(term)].add(imp.Implicant(term))
    return imp_los

def implicate(implicants):
    '''groups implicants and recurses
    returns a list of all prime implicants
    '''
    num_elem = len(implicants)
    if implicants.count(set()) == num_elem:
        return []
    if num_elem == 1:
        return list(implicants[0])

    next_imps = [set() for i in range(num_elem - 1)]
    pi_list = []
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


def extract(minterms, primes):
    '''extracts essential prime implicants
    '''
    #list of essential prime implicants
    epi_list = []
    extracting = True

    while extracting:
        covered = set()
        inner_epis = []
        for m in minterms:
            #list of prime implicants that cover m
            pi_cover = []
            for pi in primes:
                if m in pi.minterms:
                    pi_cover.append(pi)
            if len(pi_cover) == 1:
                inner_epis.append(pi_cover.pop())
        for epi in inner_epis:
            covered.update(epi.minterms)
        minterms = list(set(minterms) - covered)
        primes = list(set(primes) - set(inner_epis))
        epi_list.extend(inner_epis)
        extracting = covered != set()
    
    return [minterms, primes, epi_list]

