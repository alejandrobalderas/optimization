import numpy as np

file_location = "./data/ks_30_0"
with open(file_location,"r") as input_data_file:
    input_data = input_data_file.read()
    
print(input_data)

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

lines = input_data.split('\n')

firstLine = lines[0].split()
item_count = int(firstLine[0])
capacity = int(firstLine[1])

items = []

for i in range(1, item_count + 1):
    line = lines[i]
    parts = line.split()
    items.append(Item(i - 1, int(parts[0]), int(parts[1])))
    
weights = [0]
values = [0]
for i in range(len(items)):
    weights.append(items[i].weight)
    values.append(items[i].value)
    
    
K = np.zeros([capacity + 1, item_count + 1])
for i in range(1,item_count+1):
    for w in range(capacity+1):
        if i==0 or w==0:
            K[w,i]=0
        elif w<weights[i]:
            K[w,i]= K[w,i-1]
        else:
            K[w,i]=np.maximum(K[w-weights[i],i-1]+values[i], K[w,i-1])
    
ctr = 0
x = [0]*item_count
remove_weight=0
max_val = np.max(K)
for i in range(item_count,0,-1):
    if K[-1 - remove_weight,i-1] != K[-1 - remove_weight,i]:
        max_val = K[-1-remove_weight,i]
        remove_weight += weights[i]
        x[i-1] = 1


total_weight=0
for i in range(len(x)):
    total_weight += x[i]*values[i+1]
total_weight


## Branch and Bound

import queue


values = [45,48,35]
weights = [5,8,3]
capacity = 10
densities = [v/w for v,w in zip(values,weights)]
item_count = len(values)

class Node:
    def __init__(self, value, weight, estimate, level, contains):
        self.value = value
        self.weight = weight
        self.estimate = estimate
        self.level = level
        self.contains = contains
        
value = 0
best = []
ctr = 0

root = Node(value=0, weight=0, estimate=sum(values), level=0, contains=[])
q = queue.Queue()
q.put(root)
while not q.empty():
    n = q.get()
    
    if n.level < item_count:
        left = Node(value=n.value+values[n.level], weight=n.weight+weights[n.level], estimate=n.estimate, level=n.level+1, contains=n.contains[:])
        left.contains.append(1)
    
        if left.weight<=capacity:
            if left.value > value:
                value = left.value
                best = left.contains
            if left.estimate > value:
                q.put(left)
            
    
        right = Node(value=n.value, weight=n.weight, estimate=n.estimate-values[n.level], level=n.level+1, contains=n.contains[:])
        right.contains.append(0)

        if right.weight<=capacity:
            if right.value > value:
                value = right.value
                best = right.contains
            if right.estimate > value:
                q.put(right)
            
print("Value:",value,"\tX:", best)
