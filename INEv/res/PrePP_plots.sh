# Data Cleaning

# for b in 2 3 4 5 6 7 8
# do 
#   for k in 5 10 20 # qwl size
#   do 
#          python PrePP_transmission_ratio.py --input_file  PP_MaxParents_${b}_Query_${k}.csv
# done
# done



# for k in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2
# do
#     python PrePP_transmission_ratio.py --input_file PP_EventSkew_$k.csv

# done

#   for k in 5 10 20 # qwl size
#   do 
#     python PrePP_transmission_ratio.py --input_file PP_MaxParents_1_Query_$k.csv
# done

#  for k in 5 10 15 20 25 # qwl size
#   do 
#         for j in 4 5 6 7 8 9 10
#         do

#             python PrePP_transmission_ratio.py --input_file PP_Query_${k}_QuerySize_${j}.csv
# done
# done



python plot_PP_generic.py -i PP_MaxParents_1_Query_5.csv PP_MaxParents_1_Query_10.csv PP_MaxParents_1_Query_20.csv -l Query_5 Query_10 Query_20 -x EventTypes -y TransmissionRatioINEv TransmissionRatioCentral -o PP_MaxParents_1_Query.pdf
python plot_PP_generic.py -i PP_MaxParents_2_Query_5.csv PP_MaxParents_2_Query_10.csv PP_MaxParents_2_Query_20.csv -l Query_5 Query_10 Query_20 -x EventTypes -y TransmissionRatioINEv TransmissionRatioCentral -o PP_MaxParents_2_Query.pdf
python plot_PP_generic.py -i PP_MaxParents_3_Query_5.csv PP_MaxParents_3_Query_10.csv PP_MaxParents_3_Query_20.csv -l Query_5 Query_10 Query_20 -x EventTypes -y TransmissionRatioINEv TransmissionRatioCentral -o PP_MaxParents_3_Query.pdf
python plot_PP_generic.py -i PP_MaxParents_4_Query_5.csv PP_MaxParents_4_Query_10.csv PP_MaxParents_4_Query_20.csv -l Query_5 Query_10 Query_20 -x EventTypes -y TransmissionRatioINEv TransmissionRatioCentral -o PP_MaxParents_4_Query.pdf
python plot_PP_generic.py -i PP_MaxParents_5_Query_5.csv PP_MaxParents_5_Query_10.csv PP_MaxParents_5_Query_20.csv -l Query_5 Query_10 Query_20 -x EventTypes -y TransmissionRatioINEv TransmissionRatioCentral -o PP_MaxParents_5_Query.pdf
python plot_PP_generic.py -i PP_MaxParents_6_Query_5.csv PP_MaxParents_6_Query_10.csv PP_MaxParents_6_Query_20.csv -l Query_5 Query_10 Query_20 -x EventTypes -y TransmissionRatioINEv TransmissionRatioCentral -o PP_MaxParents_6_Query.pdf
python plot_PP_generic.py -i PP_MaxParents_7_Query_5.csv PP_MaxParents_7_Query_10.csv PP_MaxParents_7_Query_20.csv -l Query_5 Query_10 Query_20 -x EventTypes -y TransmissionRatioINEv TransmissionRatioCentral -o PP_MaxParents_7_Query.pdf
python plot_PP_generic.py -i PP_MaxParents_8_Query_5.csv PP_MaxParents_8_Query_10.csv PP_MaxParents_8_Query_20.csv -l Query_5 Query_10 Query_20 -x EventTypes -y TransmissionRatioINEv TransmissionRatioCentral -o PP_MaxParents_8_Query.pdf


python plot_PP_generic.py -i combined_output.csv -l Ratio -x EventSkew -y TransmissionRatioINEv TransmissionRatioCentral -o PP_EventSkew.pdf