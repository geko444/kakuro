from copy import deepcopy
from collections import defaultdict

def possible_combinations(total, parts, head=[], tail=list(range(1,10))):
    if total == 0 and parts == 0:
        return [sorted(head)]
    if total < 0 or len(tail) == 0:
        return []
    first = tail[0]
    rest = tail[1:]
    return possible_combinations(total-first, parts-1, head+[first], rest) \
        + possible_combinations(total, parts, head, rest)

def combinations(total, parts, inc=[], exc=[]):
    head = inc
    tail = [i for i in list(range(1,10)) if i not in inc+exc]
    return parts(total-sum(inc), parts-len(inc), head, tail)

def all_numbers(combs):
    return [i for i in range(1,10) if any([i in c for c in combs])]

def numbers_in_all(combs):
    return [i for i in range(1,10) if all([i in c for c in combs])]

def numbers_in_none(combs):
    return [i for i in range(1,10) if not any([i in c for c in combs])]

example = open('example.txt').read().split('\n')[:-1]
input1 = open('input1.txt').read().split('\n')[:-1]
input2 = open('input2.txt').read().split('\n')[:-1]

def import_puzzle(text):
    size = [int(t) for t in text[0].split(' ')[:2]]
    rules = []
    values = defaultdict(list)
    for line in text[1:]:
        l = line.split(' ')
        rules.append([int(l[0]), l[1:]])
        for v in l[1:]:
            values[v]
    return size, rules, values

size, rules, values = import_puzzle(input1)
