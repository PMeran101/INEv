"""
Initialize selectivities for given tuple of primitive event types (projlist) within interval [x,y].
"""
import random as rd
import numpy as np
import sys
from generate_qwls import *



with open('network',  'rb') as  nw_file:
        nw = pickle.load(nw_file)
    
PrimitiveEvents = list(string.ascii_uppercase[:len(nw[0].eventrates)])

def initialize_selectivities(primEvents,x,y): 

   
    projlist = generate_twosets(primEvents)       
    projlist = list(set(projlist))
    selectivities = {}
    selectivity = 0
    for i in projlist: 
        #if len(filter_numbers(i)) >1 :                  
            selectivity = rd.uniform(0.0,0.3)             
            if selectivity > 0.2:
                selectivity = 1
                selectivities[str(i)] =  selectivity
                selectivities[str(changeorder(i))] =  selectivity
            if selectivity < 0.2: 
                selectivity = rd.uniform(x,y)                
                selectivities[str(i)] =  selectivity
                selectivities[str(changeorder(i))] =  selectivity
    return selectivities



    
def increase_selectivities(percentage, selectivities): # multiply x percent of selectivities with factor ? -> 10 for starters
    number =int( len(list(selectivities.keys())) / 100) * percentage
    mylist = list(selectivities.keys())
    rd.shuffle(mylist)
    projs = mylist[0:number]
    for proj in projs:
        selectivities[proj] = selectivities[proj]  * 10 
    return selectivities
    
def main():
  """default selectivity interval"""
  x = 0.1
  y = 0.01
  percentage = 0

  primEvents = PrimitiveEvents
  
  if len(sys.argv) > 1: 
      x = float(sys.argv[1])
      
  if len(sys.argv) >2 :
      x = float(sys.argv[1])
      y = float(sys.argv[2])
      
  if len(sys.argv) > 3 :
      percentage = int(sys.argv[3])
 
  selectivities = initialize_selectivities(primEvents,x,y)
  

  #export minimal selectivity, average/median selectivity
  selectivitiesExperimentData = [x, np.median(list(selectivities.values()))]
  with open('selectivitiesExperimentData', 'wb') as selectivitiesExperimentDataFile:
      pickle.dump(selectivitiesExperimentData, selectivitiesExperimentDataFile)

  with open('selectivities', 'wb') as selectivity_file:
    pickle.dump(selectivities,  selectivity_file)   
    
 
  
if __name__ == "__main__":
    main()



    
