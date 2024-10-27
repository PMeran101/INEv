# Script for generating Transmission Ratio graphs with varying MaxParents values
# This script generates graphs for different combinations of MaxParents
# and allows for insights into the impact of graph density on Transmission Ratio.

# Transmission Ratio vs Event Types
#Part 1: MaxParents 2, 3, 4
# python3 plot_generic.py -i OP_MaxParents_2.csv OP_MaxParents_3.csv OP_MaxParents_4.csv -x EventTypes -y TransmissionRatio -l MaxParents_2 MaxParents_3 MaxParents_4 -o Fig_TransmissionRatio_EventTypes_MaxParents_2to4.pdf
# # Part 2: MaxParents 5, 6, 7
# python3 plot_generic.py -i OP_MaxParents_5.csv OP_MaxParents_6.csv OP_MaxParents_7.csv -x EventTypes -y TransmissionRatio -l MaxParents_5 MaxParents_6 MaxParents_7 -o Fig_TransmissionRatio_EventTypes_MaxParents_5to7.pdf
# Extra: MaxParents 2 and 7 (drastic comparison)
python3 plot_generic.py -i OP_MaxParents_3.csv OP_MaxParents_4.csv OP_MaxParents_6.csv -x EventTypes -y TransmissionRatio -l MaxParents_3 MaxParents_4 MaxParents_6 -o Fig_TransmissionRatio_EventTypes_MaxParents_3_4_6.pdf

# Transmission Ratio vs Workload Size
# Part 1: MaxParents 2, 3, 4
# python3 plot_generic.py -i OP_MaxParents_2.csv OP_MaxParents_3.csv OP_MaxParents_4.csv -x WorkloadSize -y TransmissionRatio -l MaxParents_2 MaxParents_3 MaxParents_4 -o Fig_TransmissionRatio_WorkloadSize_MaxParents_2to4.pdf
# # Part 2: MaxParents 5, 6, 7
# python3 plot_generic.py -i OP_MaxParents_5.csv OP_MaxParents_6.csv OP_MaxParents_7.csv -x WorkloadSize -y TransmissionRatio -l MaxParents_5 MaxParents_6 MaxParents_7 -o Fig_TransmissionRatio_WorkloadSize_MaxParents_5to7.pdf
# # Extra: MaxParents 2 and 7 (drastic comparison)
# python3 plot_generic.py -i OP_MaxParents_2.csv OP_MaxParents_7.csv -x WorkloadSize -y TransmissionRatio -l MaxParents_2 MaxParents_7 -o Fig_TransmissionRatio_WorkloadSize_MaxParents_2and7.pdf

python3 plot_generic.py -i OP_Query_Sizes_5.csv OP_Query_Sizes_10.csv OP_Query_Sizes_20.csv -x EventTypes -y TransmissionRatio -l Query_Size_5 Query_Size_10 Query_Size_20 -o Fig_TransmissionRatio_QuerySizes_MaxParents.pdf

# Example 3: All MaxParents files
python3 plot_bars.py -i OP_SweetSpot_MaxParents_2.csv OP_SweetSpot_MaxParents_3.csv OP_SweetSpot_MaxParents_4.csv OP_SweetSpot_MaxParents_5.csv OP_SweetSpot_MaxParents_6.csv OP_SweetSpot_MaxParents_7.csv OP_SweetSpot_MaxParents_8.csv OP_SweetSpot_MaxParents_9.csv OP_SweetSpot_MaxParents_10.csv OP_SweetSpot_MaxParents_11.csv OP_SweetSpot_MaxParents_12.csv OP_SweetSpot_MaxParents_13.csv OP_SweetSpot_MaxParents_14.csv OP_SweetSpot_MaxParents_15.csv -y TransmissionRatio -l MaxParents_2 MaxParents_3 MaxParents_4 MaxParents_5 MaxParents_6 MaxParents_7 MaxParents_8 MaxParents_9 MaxParents_10 MaxParents_11 MaxParents_12 MaxParents_13 MaxParents_14 MaxParents_15 -o Fig_Bar_TransmissionRatio_AllMaxParents.pdf