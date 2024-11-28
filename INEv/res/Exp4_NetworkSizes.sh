python plot_exp4_generic.py -i latency_test.csv -x Nodes -y TransmissionRatio -groupC MaximumParents \
    -group_values 0.8  1.2 1.8 2.0 -c tab:blue tab:orange tab:green tab:purple\
    -l "Max parents 0.8" "Max parents 1.2" "Max parents 1.8" "Max parents 2.0" -o Exp4_TransmissionRatioDensity.pdf \
    --x_label "Nodes" --y_label "Transmission ratio"

python plot_latency_exp4.py -i latency_test.csv -x Nodes -y PlacementComputationTime -groupC MaximumParents \
    -group_values 0.8  1.2 1.8 2.0 -c tab:blue tab:orange tab:green tab:purple\
    -l "Max parents 0.8" "Max parents 1.2" "Max parents 1.8" "Max parents 2.0" -o Exp4_ComputationTimeDensity.pdf \
    --x_label "Nodes" --y_label "Computation time in s"

python plot_latency_exp4.py -i latency_test.csv -x Nodes -y TransmissionRatioCentral -groupC MaximumParents \
    -group_values 0.8  1.2 1.8 2.0 -c tab:blue tab:orange tab:green tab:purple\
    -l "Max parents 0.8" "Max parents 1.2" "Max parents 1.8" "Max parents 2.0" -o Exp4_HybridTransmissionRatioDensity.pdf \
    --x_label "Nodes" --y_label "Transmission ratio"


python plot_latency_exp4.py -i latency_test.csv -x Nodes -y MaxPushPullLatency -groupC MaximumParents \
    -group_values 0.8  1.2 1.8 2.0 -c tab:blue tab:orange tab:green tab:purple\
    -l "Max parents 0.8" "Max parents 1.2" "Max parents 1.8" "Max parents 2.0" -o Exp4_LatencyDensity.pdf \
    --x_label "Nodes" --y_label "Latency"


python plot_latency_exp4.py -i latency_test.csv -x Nodes -y PushPullTime -groupC MaximumParents \
    -group_values 0.8  1.2 1.8 2.0 -c tab:blue tab:orange tab:green tab:purple\
    -l "Max parents 0.8" "Max parents 1.2" "Max parents 1.8" "Max parents 2.0" -o Exp4_HybridComputationTimeDensity.pdf \
    --x_label "Nodes" --y_label "Computation time in s"

python plot_bars_new.py -i latency_test.csv -x MaximumParents -y "TransmissionRatio" TransmissionRatioCentral \
    -c tab:blue tab:orange \
    -l "Base" "Hybrid" -o Exp4_MaxParents_total.pdf \
    --x_label "Max parents" --y_label "Transmission ratio"
