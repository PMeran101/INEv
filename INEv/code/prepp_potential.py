
import pickle
import os
import sys
from EvaluationPlan import EvaluationPlan, Projection, Instance
from tree import Tree

print(sys.version)



with open('EvaluationPlan', 'rb') as f:
    eval_plan = pickle.load(f)

for i in eval_plan:

    if isinstance(i,EvaluationPlan):
        print("Projections")
        for x in i.projections:
            print(x)
            print("-----------------")
        print("Instances")
        for y in i.instances:
            print(y)
            print("-----------------")
    elif isinstance(i,int):
        print("Number")
        print(i)
        print("-----------------")
    elif isinstance(i,dict):
        print("Dict")
        for key in i:
            print(key)
            print(i[key])
        print("-----------------")
