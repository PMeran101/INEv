#First Figures in Operator Placement Experiment in Paper
python3 plot_generic.py -i OP_MaxParents_3.csv OP_MaxParents_4.csv OP_MaxParents_6.csv -x EventTypes -y TransmissionRatio -l MaxParents_3 MaxParents_4 MaxParents_6 -o Fig_TransmissionRatio_EventTypes_MaxParents_3_4_6.pdf
python3 multi_variate_bar.py -i OP_MaxParents_3.csv OP_MaxParents_4.csv OP_MaxParents_6.csv \
    -y TransmissionRatio -x EventTypes -l MaxParents_3 MaxParents_4 MaxParents_6 -o Fig_TransmissionRatio_Whisker_MaxParents_3_4_6.pdf -c tab:blue tab:orange tab:green

#Second Figures in Operator Placement Experiment in Paper
python3 plot_generic.py -i OP_Query_Sizes_5.csv OP_Query_Sizes_10.csv OP_Query_Sizes_20.csv -x EventTypes -y TransmissionRatio -l Query_Size_5 Query_Size_10 Query_Size_20 -o Fig_TransmissionRatio_QuerySizes_MaxParents.pdf
python3 multi_variate_bar.py -i OP_Query_Sizes_5.csv OP_Query_Sizes_10.csv OP_Query_Sizes_20.csv \
    -y TransmissionRatio -x EventTypes -l Query_Size_5 Query_Size_10 Query_Size_20 -o Fig_Bar_TransmissionRatio_Query_Size_5_10.pdf -c tab:blue tab:orange tab:green

#Third Figure in Operator Placement Experiment in Paper
python3 plot_bars.py -i OP_SweetSpot_MaxParents_2.csv OP_SweetSpot_MaxParents_3.csv OP_SweetSpot_MaxParents_4.csv OP_SweetSpot_MaxParents_5.csv OP_SweetSpot_MaxParents_6.csv OP_SweetSpot_MaxParents_7.csv OP_SweetSpot_MaxParents_8.csv OP_SweetSpot_MaxParents_9.csv OP_SweetSpot_MaxParents_10.csv OP_SweetSpot_MaxParents_11.csv OP_SweetSpot_MaxParents_12.csv OP_SweetSpot_MaxParents_13.csv OP_SweetSpot_MaxParents_14.csv OP_SweetSpot_MaxParents_15.csv -y TransmissionRatio -l MaxParents_2 MaxParents_3 MaxParents_4 MaxParents_5 MaxParents_6 MaxParents_7 MaxParents_8 MaxParents_9 MaxParents_10 MaxParents_11 MaxParents_12 MaxParents_13 MaxParents_14 MaxParents_15 -o Fig_Bar_TransmissionRatio_AllMaxParents.pdf

#Fourh Figure in Operator Placement Experiment in Paper
python3 plot_generic.py -i OP_NER_Combined.csv -x EventNodeRatio -y TransmissionRatio -l AvgTransmissionRatio -o Fig_Transmission_Ratio_NER_Combined.pdf
python3 multi_variate_bar.py -i OP_NER_Combined.csv -y TransmissionRatio -x EventNodeRatio -l AvgTransmissionRatio -o Fig_Bar_TransmissionRatio_NER_Combined.pdf -c tab:blue

