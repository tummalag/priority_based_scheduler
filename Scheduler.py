import pandas as pd
from pulp import *

tasks = pd.read_excel('tasks.xlsx', 'tasks')

tasks.iloc[1,0]

schedule = pd.read_excel('tasks.xlsx','timeBlock',usecols="B",header=None)
availability = pd.read_excel('tasks.xlsx','timeBlock',usecols="C",header=None)
ti = pd.read_excel('tasks.xlsx','timeBlock',usecols="A",header=None)

#print(ti.iloc[4,0])

problem = LpProblem('scheduler',LpMaximize)

# Input Params
s = list(tasks['Priority'])
d = list(tasks['No. of blocks'])
b = list(availability.iloc[1:-1,0])
B = len(b)
n = len(s)
A = sum(b)

y = LpVariable.dicts('Block', [(i,t) for i in range(n) for t in range(B)],cat='Binary')

problem += lpSum(s[i]*b[t]*y[(i,t)] for i in range(n) for t in range(B))

problem += lpSum(y[(i,t)] for i in range(n) for t in range(B)) <= A #1

for i in range(n):
    problem += lpSum(y[(i,t)] for t in range(B)) <= d[i] #2
    
for t in range(B):
    problem += lpSum(y[(i,t)] for i in range(n)) <= 1 #3

problem.solve()

print("Assignment accomplished!")
print("___________________________________")
print("Task wise scheduling")
print("___________________________________")
for i in range(n):
    for t in range(B):
        if y[(i,t)].varValue ==1:
            #print(tasks.iloc[i,0],'at',ti.iloc[t,0])
            print('{0:20} at    {1}'.format(tasks.iloc[i,0], ti.iloc[t,0]))

print("___________________________________")
print("Time wise scheduling")
print("___________________________________")
for t in range(B):
    for i in range(n):
        if y[(i,t)].varValue ==1:
            #print(tasks.iloc[i,0],'at',ti.iloc[t,0])
            print('{0:20} at    {1}'.format(tasks.iloc[i,0], ti.iloc[t,0]))
