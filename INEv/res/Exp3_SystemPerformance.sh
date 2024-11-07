#First Figure in Experiment in Paper
python3 plot_Latency.py -i combined_for_latency.csv -x EventTypes -y centralHopLatency MaxPushPullLatency -l Latency -o Fig_Latency_Network_50.pdf


#Second Figure in Experiment in Paper
python3 plot_ComputationTime.py -i combined_for_latency.csv -l Latency -x EventTypes -y CombigenComputationTime PushPullTime -o Fig_Computation_Time_Network_50.pdf

#Third Figure in Experiment in Paper
python3 plot_latency_bars.py -i combined_for_latency_scaled.csv -x Nodes -l Latency -y centralHopLatency MaxPushPullLatency -o Fig_Latency_Scaled.pdf

#Fourth Figure in Experiment in Paper
python3 plot_latency_bars.py -i combined_for_latency_scaled.csv -x Nodes -l Latency -y CombigenComputationTime PushPullTime -o Fig_ComputationTime_Scaled.pdf
python3 multi_variate_latency.py -i combined_for_latency_scaled.csv -l ComputationTime -x Nodes -y CombigenComputationTime PushPullTime -o Fig_ComputationTime_Scaled_whisker.pdf