#Second Figure in Experiment in Paper
python3 plot_ComputationTime.py -i combined_for_latency.csv -l Latency -x EventTypes \
    -y PlacementComputationTime PushPullTime -o Fig_Computation_Time_Network_50.pdf \
    --legend_labels "Base" "Hybrid" --x_label "Event types" --y_label "Computation time in s"

python3 plot_latency_bars.py -i combined_for_latency.csv -l Latency -x MaximumParents \
    -y centralHopLatency MaxPushPullLatency -o Fig_Latency_Density.pdf \
    --legend_labels "Base" "Hybrid" --x_label "Max parents" --y_label "Latency"

#Third Figure in Experiment in Paper
python3 plot_latency_bars.py -i combined_for_latency_scaled.csv -x Nodes -l Latency \
    -y centralHopLatency MaxPushPullLatency -o Fig_Latency_Scaled.pdf \
    --legend_labels "Base" "Hybrid" --x_label "Nodes" --y_label "Latency"

#Fourth Figure in Experiment in Paper
python3 plot_latency_bars.py -i combined_for_latency_scaled.csv -x Nodes -l ComputationTime \
    -y PlacementComputationTime PushPullTime -o Fig_ComputationTime_Scaled.pdf \
    --legend_labels "Base" "Hybrid" --x_label "Nodes" --y_label "Computation time in s"
    
python3 multi_variate_latency.py -i combined_for_latency_scaled.csv -l ComputationTime \
    -x Nodes -y PlacementComputationTime PushPullTime \
    -o Fig_ComputationTime_Scaled_whisker.pdf --x_label "Nodes" --y_label "Computation time in s" \
    --legend_labels "Base" "Hybrid"