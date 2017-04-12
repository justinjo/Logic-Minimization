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

    def binary(self):
        b = bin(next(iter(self.minterms)))[2:][::-1]
        for d in iter(self.distance):
            i = int(math.log(d, 2))
            b = b[0:i] + 'X' + b[i + 1:]
        return b[::-1]
