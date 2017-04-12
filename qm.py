import implicant as imp

def minimize(args):
    '''minimizes the given minterms and don't care conditions
    returns two strings representing the minimized function in SOP and POS form
    '''
    if len(args) < 1:
        return
    minterms = args[0]
    dcs = [] if len(args) < 2 else args[1]
    imp_list = generate_implicants(minterms, dcs)
    pi_list = implicate(imp_list)
    #print(minterms)
    #print(imp_list)
    return ['SOP', 'POS']


def generate_implicants(minterms, dcs):
    '''given a list of minterms and don't care conditions, generates implicants
    returns list of list of implicants grouped by hamming weight
    '''
    max_term = max(max(minterms, dcs))
    literals = num_literals(max_term)
    #implicant list of sets
    imp_los = [set() for i in range(literals + 1)]
    for term in minterms:
        imp_los[hamming_weight(term)].add(imp.Implicant(term))
        #imp_los[hamming_weight(term)].add(term)
    for term in dcs:
        imp_los[hamming_weight(term)].add(imp.Implicant(term))
        #imp_los[hamming_weight(term)].add(term)
    return imp_los


def implicate(implicants):
    '''groups implicants and recurses
    returns a list of all prime implicants
    '''
    num_elem = len(implicants)
    if implicants.count(set()) == num_elem:
        return []
    next_imps = [set() for i in range(num_elem - 1)]
    pi_list = []
    print(implicants)
    for i in range(num_elem - 1):
        for imp1 in implicants[i]:
            for imp2 in implicants[i + 1]:
                if imp1.is_adjacent(imp2):
                    print('!')
                    #print(imp1.minterms)
                    #print(imp2.minterms)
                    next_imps[i].add(imp1.merge(imp2))
                    imp1.mark_not_prime()
                    imp2.mark_not_prime()
                if imp1.prime:
                    pi_list.append(imp1)
    for imp in implicants[-1]:
        if imp.prime:
            pi_list.append(imp)
    return pi_list.extend(implicate(next_imps))


def hamming_weight(num):
    '''returns the hamming weight of a number
    '''
    return bin(num).count('1')


def num_literals(num):
    '''returns the number of literals required to represent given number
    '''
    return len(bin(num)) - 2
