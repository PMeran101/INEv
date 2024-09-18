
# Workflow Explanation

## Overview
This script calculates the potential transmission savings when using a push-pull communication strategy in a Complex Event Processing (CEP) context. The goal is to optimize the number of transmissions by selectively pushing and pulling events based on their rates and selectivities.

## Workflow Steps

### 1. Imports and Helper Functions
- **Import necessary modules**: `pickle`, `os`, `sys`, custom modules like `EvaluationPlan` and `tree`, and the `string` module for character operations.
- **Define `load_pickle` function**: A helper function to load data from pickle files.

### 2. Defining Core Functions
#### `calculate_event_rates`
- **Purpose**: Calculates event rates for each primitive event and per node instance.
- **Inputs**:
  - `source_node_names`: List of node names (e.g., `['H2', 'P3']`).
  - `nodes_dict`: Dictionary mapping node IDs to Node objects.
- **Outputs**:
  - `event_rates`: Total event rates per event type (e.g., `{'H': 3855, 'P': 60}`).
  - `rates_per_node`: Event rates per node instance (e.g., `{'H2': 1285, 'P3': 20}`).

#### `calculate_transmissions`
- **Purpose**: Calculates total transmissions for an event instance.
- **Inputs**:
  - `event_rate`: The event rate of the instance.
  - `path`: The path the event takes (list of node IDs).
- **Output**: Total transmissions, calculated as `event_rate * number_of_hops`.

#### `calculate_selectivity`
- **Purpose**: Calculates the selectivity based on the event structure.
- **Inputs**:
  - `event_structure`: Can be a primitive event (string) or a composite event (dictionary).
  - `single_select`: Dictionary of single selectivities for events.
  - `selectivities`: Dictionary of selectivities for composite events.
- **Output**: The calculated selectivity value.

#### `calculate_dynamic_push_pull_transmissions`
- **Purpose**: Calculates total transmissions with and without optimization using the push-pull strategy.
- **Inputs**:
  - `event_rates`: Dictionary of event rates for each event type.
  - `rates_per_node`: Event rate per node instance.
  - `paths`: Routing paths for each event instance.
  - `single_select`: Single selectivities for events.
  - `selectivities`: Selectivities for composite events.
  - `projection_structure`: Structured representation of the projection, including operators.
  - `projection_events`: List of events in the projection.
- **Outputs**: Prints transmission statistics and savings.

#### `extract_primitive_events`
- **Purpose**: Extracts all primitive events from the projection, ignoring operators like AND and SEQ.
- **Input**: `projection_events` — List of events or nested operators.
- **Output**: `flat_events` — A flat list of primitive events.

#### `extract_events_with_operators`
- **Purpose**: Extracts events and operators from the projection into a structured representation.
- **Input**: `projection_events` — List of events or nested operators.
- **Output**: `structured_events` — List where primitive events are strings and composite events are dictionaries.

### 3. Main Execution Flow
#### Loading Data
- Load the evaluation plan: Contains the projections (queries) to process.
- Load the network nodes: Each node contains event rates and other properties.
- Load selectivities: Contains selectivity values for composite events.
- Load single selectivities: Contains selectivity values for events conditioned on other events.

#### Processing Each Projection
- **Iterate over the evaluation plan** and process each projection.
- **Extract projection information**:
  - Projection name.
  - List of events in the projection.
  - Parse events to include operators, creating a structured representation.
- **Collect source nodes and paths**:
  - Source node names (primitive event instances) involved in the projection.
  - Routing paths for each event instance.
- **Calculate event rates**:
  - Use `calculate_event_rates` to get total event rates per event type and per node instance.
- **Apply push-pull strategy**:
  - Use `calculate_dynamic_push_pull_transmissions` to calculate transmissions with and without optimization.
  - Determine which event to push (the one with the minimum adjusted event rate).
  - Adjust transmissions for pulled events based on selectivities.

### 4. Function Details
#### `calculate_event_rates`
- For each source node name:
  - Extract the event type (first character) and node ID (remaining characters).
  - Retrieve the node from `nodes_dict` using the node ID.
  - Retrieve the event rate for the event type from the node's `eventrates`.
  - Accumulate event rates per event type and per node instance.
- **Note**: Skips any node names that do not follow the expected format.

#### `calculate_transmissions`
- Calculates total transmissions by multiplying the event rate by the number of hops in the path.

#### `calculate_selectivity`
- **For primitive events**:
  - Returns a selectivity of `1.0`.
- **For composite events (AND, SEQ)**:
  - Constructs a key by concatenating event names.
  - Looks up the selectivity in the `selectivities` dictionary.
  - For AND operators, considers permutations of event names if the selectivity is not found.
  - Defaults to `1.0` if selectivity is not found.

#### `calculate_dynamic_push_pull_transmissions`
- Calculates adjusted event rates for each event or composite event using selectivities.
- Determines the event with the minimum adjusted event rate to push.
- For each event instance:
  - Calculates transmissions without optimization.
  - If the event is the pushed event, uses the original event rate.
  - If the event is a pulled event, adjusts the event rate using the appropriate selectivity from `single_select`.
  - Calculates transmissions with push-pull optimization.
- Sums up the total transmissions and calculates the savings.

#### `extract_primitive_events`
- Parses the projection events and extracts all primitive events, ignoring operators.

#### `extract_events_with_operators`
- Parses the projection events and creates a structured representation:
  - Primitive events are represented as strings.
  - Composite events are represented as dictionaries with an operator and a list of events.

### 5. Execution and Output
- Prints information during execution, including:
  - Python version and loaded nodes.
  - Details of processing each projection.
  - Event rates and structured events.
  - Transmissions with and without optimization.
  - Transmission savings achieved.

## Key Concepts
- **Primitive Events**: Basic events that occur in the system (e.g., 'G', 'H', 'P').
- **Composite Events**: Events composed of multiple primitive events combined using operators like AND or SEQ.
- **Event Rate**: The frequency at which an event occurs.
- **Selectivity**: The probability that a composite event occurs given the occurrence of its component events.
- **Push-Pull Strategy**: A communication strategy where low-rate events are pushed towards the sink, and high-rate events are pulled based on the occurrence of the pushed events to optimize transmissions.

## Conclusion
This script provides a dynamic method to calculate the potential transmission savings in a CEP system by applying a push-pull communication strategy. By accurately calculating event rates and applying selectivities, it determines the optimal events to push and adjusts the transmissions accordingly, leading to optimized network communication.


Test