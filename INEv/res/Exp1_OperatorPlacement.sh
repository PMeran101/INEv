#First Figures in Operator Placement Experiment in Paper
python3 plot_generic.py -i OP_MaxParents_3.csv OP_MaxParents_4.csv OP_MaxParents_6.csv -x EventTypes -y TransmissionRatio \
    -l MaxParents_3 MaxParents_4 MaxParents_6 -c tab:blue tab:orange tab:green -o Exp1/Fig_TransmissionRatio_EventTypes_MaxParents_3_4_6.svg \
    -legend_labels "Max parents 3" "Max parents 4" "Max parents 6" --x_label "Event types" --y_label "Transmission ratio"

python3 multi_variate_bar.py -i OP_MaxParents_3.csv OP_MaxParents_4.csv OP_MaxParents_6.csv \
    -y TransmissionRatio -x EventTypes -l "Max parents 3" "Max parents 4" "Max parents 6" \
    -o Exp1/Fig_TransmissionRatio_Whisker_MaxParents_3_4_6.svg -c tab:blue tab:orange tab:green\
    --x_label "Event types" --y_label "Transmission ratio"

#Second Figures in Operator Placement Experiment in Paper
python3 plot_generic.py -i OP_Query_Sizes_5.csv OP_Query_Sizes_10.csv OP_Query_Sizes_20.csv -x EventTypes -y TransmissionRatio \
        -l Query_Size_5 Query_Size_10 Query_Size_20 -o Exp1/Fig_TransmissionRatio_QuerySizes_MaxParents.svg \
        -c tab:blue tab:orange tab:green \
        -legend_labels "5 queries" "10 queries" "20 queries" --x_label "Event types" --y_label "Transmission ratio"

python3 multi_variate_bar.py -i OP_Query_Sizes_5.csv OP_Query_Sizes_10.csv OP_Query_Sizes_20.csv \
    -y TransmissionRatio -x EventTypes -l "5 queries" "10 queries" "20 queries" \
    -o Exp1/Fig_Bar_TransmissionRatio_Query_Size_5_10.svg -c tab:blue tab:orange tab:green \
    --x_label "Event types" --y_label "Transmission ratio"
#Third Figure in Operator Placement Experiment in Paper
python3 plot_bars.py -i OP_SweetSpot_MaxParents_2.csv OP_SweetSpot_MaxParents_3.csv OP_SweetSpot_MaxParents_4.csv OP_SweetSpot_MaxParents_5.csv OP_SweetSpot_MaxParents_6.csv OP_SweetSpot_MaxParents_7.csv OP_SweetSpot_MaxParents_8.csv OP_SweetSpot_MaxParents_9.csv OP_SweetSpot_MaxParents_10.csv OP_SweetSpot_MaxParents_11.csv OP_SweetSpot_MaxParents_12.csv OP_SweetSpot_MaxParents_13.csv OP_SweetSpot_MaxParents_14.csv OP_SweetSpot_MaxParents_15.csv \
    -o Exp1/Fig_Bar_TransmissionRatio_AllMaxParents.svg \
    -y TransmissionRatio \
    -l MaxParents_2 MaxParents_3 MaxParents_4 MaxParents_5 MaxParents_6 MaxParents_7 MaxParents_8 MaxParents_9 MaxParents_10 MaxParents_11 MaxParents_12 MaxParents_13 MaxParents_14 MaxParents_15 \
    --x_label "Max parents" --y_label "Transmission ratio" \

#Fourh Figure in Operator Placement Experiment in Paper
python3 plot_generic.py -i OP_NER_Combined.csv -x EventNodeRatio -y TransmissionRatio -l AvgTransmissionRatio \
    -o Exp1/Fig_Transmission_Ratio_NER_Combined.svg -c tab:blue -legend_labels "Transmission ratio operator placement" \
    --x_label "Node event ratio" --y_label "Transmission ratio"
    
python3 multi_variate_bar.py -i OP_NER_Combined.csv -y TransmissionRatio -x EventNodeRatio \
    -l "Transmission ratio operator placement" -o Exp1/Fig_Bar_TransmissionRatio_NER_Base.svg -c tab:blue \
    --x_label "Node event ratio" --y_label "Transmission ratio"

