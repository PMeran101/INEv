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


# Max Parents Transmission Ratio plotting
python3 plot_PP_generic.py -i PP_MaxParents_3.csv PP_MaxParents_6.csv -l MaxParents3 MaxParents6 -x EventTypes -y TransmissionRatio TransmissionRatioCentral -o PP_MaxParents_3_6.pdf
python3 multi_variate_PP_bar.py -i PP_MaxParents_3.csv PP_MaxParents_6.csv -l MaxParents3 MaxParents6 -x EventTypes -y TransmissionRatio TransmissionRatioCentral -o PP_MaxParents_Whisker.pdf

#Max Parents bar plotting
python3 plot_PP_bars.py -i PP_MaxParents_3.csv PP_MaxParents_4.csv PP_MaxParents_5.csv PP_MaxParents_6.csv PP_MaxParents_7.csv PP_MaxParents_8.csv -l 3 4 5 6 7 8 -y TransmissionRatio TransmissionRatioCentral -o PP_MaxParents.pdf

## Event Skew Plotting
python3 plot_PP_generic.py -i combined_output.csv -l Ratio -x EventSkew -y TransmissionRatio TransmissionRatioINEv TransmissionRatioCentral -o PP_EventSkew.pdf


python3 multi_variate_PP_bar.py -i combined_output.csv -l Ratio -x EventSkew -y TransmissionRatio TransmissionRatioINEv TransmissionRatioCentral -o PP_EventSkew_Whisker.pdf