# INEv Algorithms

This folder contains the algorithms used to construct INEv graphs for a given network, query workload, network topology and set of selectivities. To this end, it also contains generators for networks and workloads for given characteristics.

## Scripts
The scripts contained can reproduce a subset of the experiments presented in the paper, e.g.:
- *\_qwl execute a set of experiments for query workloads of varying sizes for networks with different event rate distributions (./eventSkew_qwl), event node distributions (./eventNode) and number of nodes (./nwSize)
- conflicting_qwl to reproduce performance of multi-query scenario with varying overlap in event types between queries

Using the `eventSkew_qwl_plan.sh`, saves for each resulting INEv graph as well as for its centralized counter part an evaluation plan in the `plans/` folder. 

Please note, that only only one script can be executed at a time.


## Schema of Results
Results of an experiment can be found in `res/` folder. Each result file contains among others the following  experiment parameters and metrics of the INEv graphs constructed during the respective experiment:
- ID
- TransmissionRatio
- Filters (used output selectors)
- Network Parameters (EventSkew, EventNodeRatio, Number of Eventtypes, NetworkSize, Outdegree)
- Query Parameters (Size of Queryworkload, Length of Query, Median Selectivity, Minimal Selectivity)
- Computation Time for Placement and Combination Construction

## Plotting Results

The results in the `res/` folder can be plotted using `plot.py`, e.g., the following command generates a plot for the resulting files of the eventSkew_single experiment:

`python3.8 plot.py -i eventSkew_5.csv eventSkew_10.csv eventSkew_20.csv -x EventSkew -y TransmissionRatio -l 5 10 20 -o eventSkew_qwl`

Resulting plots are saved in `figs/`.

### Parameters for plot script
Parameter | Meaning
------------ | -------------
-i| Required. Input File(s)
-x| Required. Column in input file(s) to use as x-axis
-y |  Required. Column in input file(s) to use as y-axis
-l |  Required. Labels for line types
-o |  Optional. Name for output file (saved in `figs/` folder) 
-box |  Optional. Adds boxplot for each value

## Evaluation Plans

Using the `_plan.sh`-version of a script, saves for each experiment the resulting INEv graphs in the `plans/` folder. 
The name of an INEv graph plan corresponds to the IDs in the result file for the experiment.
For each INEv graph `_INEv.txt`, a corresponding plan for a centralized placement `_Centralized.txt` is also saved in the  `plans/` folder.
The prefix `_os` denotes that output selectors were used in the INEv graph.
A plan can be used as input to our DCEP engine by passing its path as input parameter.

## Reusability
The repository can be used to generate INEv graphs for custom networks, queries and selectivities. 

### Network Rates
To instantiate an event network of size `n` with event rates `[x,y,z]` (event universe contains three types, with the rate of type `A` being `x`) and with an event node ratio of `w`, use the following command:
`python3.8 generate_network_custom_rates.py -event_rates x y z -networksize n -node_event_ratio w`

### Network Topology
A random graph topology (watts strogatz graph) with an outdegree of `d` per node can be generated with:
`python3.8 generate\_graph.py d`
Internally graphs are represented as adjacency list. Please refer to `python3.8 generate_graph.py` to create a concrete graph topology as adjacency list. 

### Query Workload
To create a query (workload) over the given event universe, refer to the code in `generate_qwls.py` which contains a few exemplary queries. To generate a random query workload of size `k` with queries having a maximal lenght of `l` event types taken from the event defined prior, run `generate_qwls.py l k`.

### Selectivities
For defining pairwise selectivities between event types which model the selectivities of all predicates defined over a tuple of event types in the query, refer to `generate_selectivity.py`. To instantiate random selectivities in the ranging between `x y`, run `generate_selectivity.py x y`. Selectivities are internally represented as dictionary having all possible tuples of event types in the event universe as key and the respective selectivity as value.

### INEv generation
After running instantiatiating the above structures, an INEv graph can be generated by calling `generate_INEv.py`.
The ID of the resulting INEv graph is given by the ID of the last entry in the result file `res/results.csv`. 
The corresponding INEv graph representation can be found in the `plans/` directory. 

