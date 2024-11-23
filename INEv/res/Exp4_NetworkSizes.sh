#First Plot in Experiment in Paper
python3 plot_PP_bars.py -i OP_Network_Size_100.csv OP_Network_Size_500.csv OP_Network_Size_1000.csv OP_Network_Size_5000.csv OP_Network_Size_10000.csv \
    -l "100" "500" "1.000" "5.000" "10.000" -y TransmissionRatio \
    -o Fig.TransmissionRatio_EventTypes_Scaled.pdf --x_label "Nodes" --legend_tags "Operator placement" --y_label "Transmission ratio"

#Second Plot in Experiment in Paper
python3 plot_latency_bars.py -i OP_Network_Size_10000.csv -x MaximumParents -y TransmissionRatio -l NetworkSize10000 -o Fig_Bar_TransmsissionRatio_10000.pdf
