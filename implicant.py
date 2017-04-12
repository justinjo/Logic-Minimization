class Implicant(object):
    minterms = set()
    distance = set()
    prime = True

    def __init__(self, *args):
        if len(args) > 0:
            self.minterms.add(args[0])

    def calc_distance(self, implicant):
        return min(implicant.minterms) - min(self.minterms)

    def merge(self, implicant):
        if self.distance != implicant.distance:
            return
        new_imp = Implicant()
        new_imp.minterms = self.minterms | implicant.minterms
        new_imp.distance = self.distance | implicant.minterms
        new_imp.distance.add(self.calc_distance(implicant))
        return new_imp

    def get_weight(self):
        pass

    def mark_not_prime(self):
        self.prime = False

    def is_adjacent(self, implicant):
        dist = self.calc_distance(implicant)
        is_power_2 = dist > 0 and (dist & (dist - 1) == 0)
        return self.distance == implicant.distance and is_power_2
