#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from operator import itemgetter
import numpy as np
import queue

Item = namedtuple("Item", ['index', 'value', 'weight'])
Item_density = namedtuple("Item", ['index', 'value', 'weight', 'density'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm


    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item_density(i - 1, int(parts[0]), int(parts[1]), float(int(parts[0])/int(parts[1]))))

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full

    values = []
    weights = []
    for item in items:
        values.append(item.value)
        weights.append(item.weight)
    density = [v / w for v, w in zip(values, weights)]

    class Node:
        def __init__(self, value, weight, estimate, level, contains):
            self.value = value
            self.weight = weight
            self.estimate = estimate
            self.level = level
            self.contains = contains

    val_max = 0
    best = []
    q = queue.Queue()

    root = Node(value=0, weight=0, estimate=sum(values), level=0, contains=[])
    q.put(root)
    while not q.empty():
        n = q.get()

        if n.level < item_count:
            left = Node(value=n.value + values[n.level], weight=n.weight + weights[n.level], estimate=n.estimate,
                        level=n.level + 1, contains=n.contains[:])
            left.contains.append(1)

            if left.weight <= capacity:
                if left.value > val_max:
                    val_max = left.value
                    best = left.contains
                if left.estimate > val_max:
                    q.put(left)

            right = Node(value=n.value, weight=n.weight, estimate=n.estimate - values[n.level], level=n.level + 1,
                         contains=n.contains[:])
            right.contains.append(0)

            if right.weight <= capacity:
                if right.value>val_max:
                    val_max = right.value
                    best = right.contains
                if right.estimate>val_max:
                    q.put(right)

    # prepare the solution in the specified output format
    output_data = str(val_max) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, best))

    return output_data



if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

