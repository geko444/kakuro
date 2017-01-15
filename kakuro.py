from copy import deepcopy
from collections import defaultdict
import string

class Kakuro(object):

    def possible_combinations(self, total, parts, head=[], tail=list(range(1,10))):
        if total == 0 and parts == 0:
            return [sorted(head)]
        if total < 0 or len(tail) == 0:
            return []
        first = tail[0]
        rest = tail[1:]
        return self.possible_combinations(total-first, parts-1, head+[first], rest) \
            + self.possible_combinations(total, parts, head, rest)

    def combinations(self, total, parts, inc=[], exc=[]):
        head = inc
        tail = [i for i in list(range(1,10)) if i not in inc+exc]
        return self.possible_combinations(total-sum(inc), parts-len(inc), head, tail)

    @staticmethod
    def all_numbers(combs):
        return [i for i in range(1,10) if any([i in c for c in combs])]

    @staticmethod
    def numbers_in_all(combs):
        return [i for i in range(1,10) if all([i in c for c in combs])]

    @staticmethod
    def numbers_in_none(combs):
        return [i for i in range(1,10) if not any([i in c for c in combs])]

    @staticmethod
    def import_puzzle(name):
        text = open('{}.txt'.format(name)).read().split('\n')[:-1]
        size = [int(t) for t in text[0].split(' ')[:2]]
        rules = []
        values = defaultdict(list)
        for line in text[1:]:
            l = line.split(' ')
            rules.append([int(l[0]), l[1:]])
            for v in l[1:]:
                values[v] = list(range(1,10))
        return size, rules, values

    @staticmethod
    def common(list1, list2):
        return [n for n in list1 if n in list2]

    def __init__(self, name):
        self.size, self.rules, self.values = self.import_puzzle(name)

    def print(self):
        x, y = self.size
        row1 = [' '] + list(string.ascii_uppercase[:x])
        grid = [row1] + [[str(i)] + ['#']*x for i in range(1, y+1)]
        for val in self.values:
            if len(self.values[val]) == 1:
                num = self.values[val][0]
                i = string.ascii_uppercase.index(val[0]) + 1
                j = int(val[1:])
                grid[j][i] = str(num)
        print('\n'.join([' '.join(row) for row in grid]))

    def values_length(self):
        return sum([len(self.values[val]) for val in self.values])

    def possible_values_for_rule(self, rule):
        pos_values = [self.values[v] for v in rule[1]]
        include = [pv[0] for pv in pos_values if len(pv) == 1]
        exclude = self.numbers_in_none(pos_values)
        combs = self.combinations(rule[0], len(rule[1]), include, exclude)
        all = self.all_numbers(combs)
        for v in rule[1]:
            common = self.common(self.values[v], all)
            if len(common) > 1:
                if len(include) > 0:
                    for i in include:
                        try:
                            common.remove(i)
                        except ValueError:
                            pass
            self.values[v] = common

    def cycle_through_rules(self):
        for rule in self.rules:
            self.possible_values_for_rule(rule)

    def is_solved(self):
        if len(self.values) == self.values_length():
            return True
        else:
            return False

    def is_possible(self):
        for val in self.values:
            if len(self.values[val]) == 0:
                return False
        return True

    def cycle_until_no_change(self):
        old = self.values_length()
        while True:
            self.cycle_through_rules()
            new = self.values_length()
            if new == old:
                return False
            else:
                old = new

    def guesswork(self):
        if self.is_solved():
            return
        old = deepcopy(self.values)
        for val in old:
            if len(old[val]) > 1:
                for num in old[val]:
                    self.values[val] = [num]
                    self.cycle_until_no_change()
                    if self.is_possible():
                        return self.guesswork()
                    self.values = deepcopy(old)

    def solve(self):
        self.cycle_until_no_change()
        if not self.is_solved():
            self.guesswork()
        self.print()

kak = Kakuro('input3')
kak.solve()
