import math

class Implicant(object):
    '''implicant class
    '''

    def __init__(self, *args):
        self.minterms = set()
        self.distance = set()
        self.prime = True
        if len(args) > 0:
            self.minterms.add(args[0])

    def __eq__(self, imp):
        return self.minterms == imp.minterms and self.distance == imp.distance

    def __hash__(self):
        b = ''
        for i in range(max(self.minterms) + 1):
            b += '1' if i in self.minterms else '0'
        b = b[::-1]
        return int(b, 2)


    def __repr__(self):
        return 'Imp ' + str(self.minterms)



    def calc_distance(self, imp):
        return min(imp.minterms) - min(self.minterms)

    def merge(self, imp):
        if self.distance != imp.distance:
            return
        new_imp = Implicant()
        new_imp.minterms = self.minterms | imp.minterms
        new_imp.distance = self.distance | imp.distance
        new_imp.distance.add(self.calc_distance(imp))
        return new_imp

    def mark_not_prime(self):
        self.prime = False

    def is_adjacent(self, imp):
        dist = self.calc_distance(imp)
        is_power_2 = dist > 0 and (dist & (dist - 1) == 0)
        return self.distance == imp.distance and is_power_2


    def binary(self, literals):
        '''generates binary representation of implicant
        returns implicant in binary, 'X' as don't care
        '''
        b = ''
        # populate with 0 or X to start
        for i in range(literals):
            b += 'X' if 2**i in self.distance else '0'
        # then fill with 1 as necessary
        minterm = bin(next(iter(self.minterms)))[2:][::-1]
        for i, d in enumerate(minterm):
            if d == '1' and b[i] == '0':
                b = b[0:i] + '1' + b[i+1:]
        return b[::-1]


    def boolean_product(self, literals):
        bool_prod = ''
        b = self.binary(literals)
        for i, c in enumerate(b):
            bool_prod += chr(i + 65) if c != 'X' else ''
            bool_prod += "'" if c == '0' else ''
        if bool_prod == '' and len(self.minterms) > 0:
            bool_prod = '1'
        return bool_prod

    def boolean_dual(self, literals):
        bool_dual = ''
        b = self.binary(literals)
        for i, c in enumerate(b):
            if c != 'X':
                bool_dual += chr(i + 65)
                bool_dual += "'" if c == '1' else ''
                bool_dual += '+'
        bool_dual = bool_dual[:-1]
        if bool_dual == '' and len(self.minterms) > 0:
            bool_dual = '0'
        return bool_dual

