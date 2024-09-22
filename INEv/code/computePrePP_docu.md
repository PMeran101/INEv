
# Evaluating Push-Pull Optimization in Complex Event Processing (CEP)

## Quick Explanation
This script calculates the potential savings in network transmissions when using push-pull communication strategies in a Complex Event Processing (CEP) system. It processes an evaluation plan, calculates event rates, and compares the total transmissions with and without optimization. The goal is to determine how much network traffic can be reduced by strategically pushing or pulling events based on their rates and selectivities.

## Detailed Explanation

### Overview
In CEP systems, events are processed and transmitted across a network of nodes. Efficient communication is crucial to reduce network congestion and improve performance. The push-pull strategy optimizes transmissions by deciding whether to push (send proactively) or pull (request when needed) events based on their occurrence rates and selectivities.

This script performs the following:
- Loads the evaluation plan and necessary data.
- Processes each projection in the evaluation plan.
- Calculates event rates and selectivities.
- Determines the optimal push-pull strategy.
- Calculates and compares total transmissions with and without optimization.
- Outputs the potential savings.

### Workflow Breakdown

#### 1. Loading Necessary Data
The script begins by loading data from pickle files:
- **EvaluationPlan**: Contains projections and events to be processed.
- **Network Nodes**: Represents the network topology and node information.
- **Selectivities**: Represents the probability that a combination of events occurs.
- **SingleSelectivities**: Represents the selectivity of individual events given a context.

```python
eval_plan = load_pickle('EvaluationPlan')
nodes_dict = {node.id: node for node in load_pickle('network')}
selectivities = load_pickle('selectivities')
single_select = load_pickle('singleSelectivities')
```

#### 2. Processing Each Projection
For each projection in the evaluation plan, the script:
- Extracts the projection name and events.
- Parses events to identify primitive and composite events (e.g., events combined with operators like AND or SEQ).
- Collects source node names and paths.
- Calculates event rates per event type and per node instance.

```python
for item in eval_plan:
    if isinstance(item, EvaluationPlan):
        for proj in item.projections:
            # Extract and process projection details
            ...
```

#### 3. Calculating Event Rates
The function `calculate_event_rates` computes:
- **Event Rates**: Total occurrence rates of each event type across all nodes.
- **Rates Per Node**: Occurrence rates of events at each node.

Example:

Suppose we have the following source nodes:
- H2 (Event type H at node 2)
- P3 (Event type P at node 3)

Assuming:
- Node 2 generates event H at a rate of 100 events per second.
- Node 3 generates event P at a rate of 50 events per second.

Event Rates:
```
{'H': 100, 'P': 50}
```

Rates Per Node:
```
{'H2': 100, 'P3': 50}
```

```python
event_rates, rates_per_node = calculate_event_rates(source_node_names, nodes_dict)
```

#### 4. Determining the Push-Pull Strategy
The function `calculate_dynamic_push_pull_transmissions` determines which events to push and which to pull:
- **Adjusted Event Rates**: Event rates adjusted by selectivities.
- **Minimum Adjusted Event Rate**: The event with the lowest adjusted rate is chosen to be pushed.
- **Push Events**: Sent proactively from source nodes to the sink.
- **Pull Events**: Requested by the sink when needed, reducing unnecessary transmissions.

Example:

Given adjusted event rates:
- Event H: Adjusted rate = 5
- Event P: Adjusted rate = 2

Event P has the minimum adjusted rate and will be pushed. Event H will be pulled.

#### 5. Calculating Transmissions
Without Optimization: Total transmissions are calculated by multiplying the event rate by the number of hops in the network path.

Formula:
```
Transmissions = Event Rate × Number of Hops
```

With Push-Pull Optimization:
- **Pushed Events**: Same as without optimization.
- **Pulled Events**: Event rates are adjusted by selectivity (since only relevant events are pulled).

Adjusted Event Rate for Pulled Events:
```
Adjusted Rate = Event Rate × Selectivity
```

Example:
- Event H: Event rate = 100 events/sec
- Number of hops = 3
- Selectivity = 0.1

Without Optimization:
```
100 × 3 = 300 transmissions/sec
```

With Optimization:
```
(100 × 0.1) × 3 = 30 transmissions/sec
```

#### 6. Calculating Savings
The savings are calculated as:
```
Savings = Transmissions Without Optimization − Transmissions With Optimization
```

The savings percentage is:
```
Savings Percentage = (Savings / Transmissions Without Optimization) × 100%
```

Example:
- Transmissions without optimization: 300 transmissions/sec
- Transmissions with optimization: 30 transmissions/sec
- Savings: 300 − 30 = 270 transmissions/sec
- Savings Percentage: (270 / 300) × 100% = 90%

#### 7. Outputting Results
For each projection, the script outputs:
- Projection name
- Total transmissions without optimization
- Total transmissions with push-pull optimization
- Savings percentage

Overall totals are also calculated and displayed.

### Function Descriptions and Examples

#### `load_pickle(file_name)`
Purpose: Load data from a pickle file.

```python
nodes_dict = load_pickle('network')
```

#### `calculate_event_rates(source_node_names, nodes_dict)`
Purpose: Calculate event rates per event type and per node instance.

Example:

Given `source_node_names = ['H2', 'P3']` and `nodes_dict` containing node event rates.

Output:
```
event_rates = {'H': 100, 'P': 50}
rates_per_node = {'H2': 100, 'P3': 50}
```

#### `calculate_transmissions(event_rate, path)`
Purpose: Calculate total transmissions for an event instance based on event rate and path length.

Example:
- Event rate: 100 events/sec
- Path: [2, 5, 7] (Number of hops = 2)

Calculation:
```
Transmissions = 100 × 2 = 200 transmissions/sec
```

#### `calculate_selectivity(event_structure, single_select, selectivities)`
Purpose: Calculate the selectivity of an event or composite event.

Example:
- For primitive event H, selectivity is 1.0.
- For composite event AND(H, P), selectivity might be 0.05.

#### `calculate_dynamic_push_pull_transmissions(...)`
Purpose: Calculate transmissions with and without push-pull optimization.

Example:
- Event rates: `{'H': 100, 'P': 50}`
- Rates per node: `{'H2': 100, 'P3': 50}`
- Paths: `{'H2': [2, 5, 7], 'P3': [3, 5, 7]}`
- Selectivities: `{'HP': 0.05}`
- Single selectivities: `{'H|HP': 0.1, 'P|HP': 0.2}`
- Projection structure: ` [{'operator': 'AND', 'events': ['H', 'P']}]`

#### `extract_events_with_operators(projection_events)`
Purpose: Parse projection events to identify operators and structure.

Example:
- Input: `['M', 'K', 'AND(P, R, S)']`
- Output:
```python
[
    'M',
    'K',
    {
        'operator': 'AND',
        'events': ['P', 'R', 'S']
    }
]
```

#### `calculate_transmission_savings()`
Purpose: Calculate and compile transmission savings for all projections.

Example Output:
```python
[
    {
        'projection': 'GH',
        'total_transmissions_no_optimization': 3000,
        'total_transmissions_with_push_pull': 1500,
        'savings_percentage': 50.0
    },
    ...
]
```

#### `calculate_complete_transmission_savings(results)`
Purpose: Sum total transmissions across all projections.

Example:
- Total without optimization: 10,000 transmissions/sec
- Total with optimization: 7,000 transmissions/sec
- Overall savings: 30%

### Running the Script
When you run the script, it processes all projections in the evaluation plan and outputs the results:

```
Projection: GH
Total transmissions without optimization: 3000
Total transmissions with push-pull: 1500
Savings percentage: 50.00%

...

Overall total transmissions without optimization: 10000
Overall total transmissions with push-pull: 7000
Overall savings percentage: 30.00%
```

## Conclusion
This script demonstrates how applying a push-pull strategy in CEP systems can significantly reduce network transmissions, leading to better performance and resource utilization. By dynamically deciding which events to push or pull based on event rates and selectivities, the system optimizes communication without compromising on event detection capabilities.
