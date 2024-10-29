# Introduction 
**Overview:**
In this simulation we will explore the Potential of transmission savings in a CEP Context in a hierarchical fog-cloud environment using two State-of-the-Art approaches from [INEv](link-to-repo.com) and [PrePP](Link-to-repo.com). We expect that the combination of these two appraoches with some adjustments for the fog-cloud environment can enhance performance in Query evaluation. 

**Objective:** Exploring the adjustments needed to make to combine the approach in a hierarchical network topology and proving the potential transmission savings of using both approaches of Operator Placement and Push-Pull communication on a synthetical Dataset. 

**Background:** This simulation uses a randomized hierarchical, heterogenous network representing the Fog-Cloud topology with the Cloud at the top most level with virtually infinite resources and the nodes cascading downwards with fewer resources the more we get to the edge. The Leaf nodes in this simulation represents the sole event generating nodes while all other nodes are capable of evaluating the queries. 

**Key Features** Generation of a hierarchical heteregoneous network topology. Placing operators at respective nodes. Simulating transmission costs in this netwokr using the networkx python library. 

# Prerequisites
**Hardware Requirements:** Due to the sequential nature of the simulation, to yield enough data it is recommended to use some sort of server/virtual machine, as simulations can take up several days to finish. The simulation in the paper was done on 60GB of RAM on a linux cluster. 

**Software Requirements**
- Only Tested on Linux Environments
- Requires Python3.8 or higher 
- Required Libraries are in the [Requirements](INEv/requirements.txt) file

# Installation
1. clone the Repository
2. Install all packages from the [Requirements](INEv/requirements.txt) into selected Environment (virtual Environment or Conda Environment)

# Usage
For the simulation we offer a default script running the experiments and plotting scripts used in the provided Paper. It can be executed by running 
```bash
sh combined.sh
```
in the [Scripts](INEv/scripts/) folder. 

If needed adjustments can be made in the corresponding folder adjusting all the variious shell scripts. 

