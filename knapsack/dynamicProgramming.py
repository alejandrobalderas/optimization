#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from operator import itemgetter
import numpy as np

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

    weights = [0]
    values = [0]
    for i in range(len(items)):
        weights.append(items[i].weight)
        values.append(items[i].value)

    K = np.zeros([capacity + 1, item_count + 1])
    for i in range(1, item_count + 1):
        for w in range(capacity + 1):
            if i == 0 or w == 0:
                K[w, i] = 0
            elif w < weights[i]:
                K[w, i] = K[w, i - 1]
            else:
                K[w, i] = np.maximum(K[w - weights[i], i - 1] + values[i], K[w, i - 1])

    ctr = 0
    x = [0] * item_count
    remove_weight = 0
    max_val = np.max(K)
    for i in range(item_count, 0, -1):
        if K[-1 - remove_weight, i - 1] != K[-1 - remove_weight, i]:
            max_val = K[-1 - remove_weight, i]
            remove_weight += weights[i]
            x[i - 1] = 1

    total_weight = 0
    for i in range(len(x)):
        total_weight += x[i] * values[i + 1]
    total_weight

    # prepare the solution in the specified output format
    output_data = str(total_weight) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, x))

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

