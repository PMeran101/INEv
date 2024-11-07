#echo "Creating bar plot for MaxParents CSV files..."
python3 multi_variate_bar.py -i OP_MaxParents_4.csv OP_MaxParents_6.csv \
    -y TransmissionRatio -x EventTypes -l MaxParents_4 MaxParents_6 -o Fig_Bar_TransmissionRatio_MaxParents_4_6.pdf -c tab:orange green

# Create bar plots for the second set of CSV files (Query Sizes)
#echo "Creating bar plot for Query Size CSV files..."
python3 multi_variate_bar.py -i OP_Query_Sizes_5.csv OP_Query_Sizes_10.csv OP_Query_Sizes_20.csv \
    -y TransmissionRatio -x EventTypes -l Query_Size_5 Query_Size_10 Query_Size_20 -o Fig_Bar_TransmissionRatio_Query_Size_5_10.pdf -c tab:blue tab:orange tab:green

python3 multi_variate_bar.py -i OP_NER_Combined.csv -y TransmissionRatio -x EventNodeRatio -l AvgTransmissionRatio -o Fig_Bar_TransmissionRatio_NER_Combined.pdf -c tab:blue

python3 multi_variate_PP_bar.py -i PP_NER_Combined.csv -y TransmissionRatio TransmissionRatioCentral -x EventNodeRatio -l AvgTransmissionRatio -o Fig_Bar_TransmissionRatio_NER_Combined.pdf -c tab:blue tab:orange
