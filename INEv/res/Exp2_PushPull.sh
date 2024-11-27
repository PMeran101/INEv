#Firt Figure in Experiment in Paper
python3 plot_PP_generic.py -i PP_MaxParents_3.csv PP_MaxParents_6.csv -l MaxParents3 MaxParents6 -x EventTypes \
    -y TransmissionRatio TransmissionRatioCentral -c tab:blue tab:blue tab:orange tab:orange -s "-" "dashed" "-" "dashed" \
    --x_label "Event types" --y_label "Transmission ratio" \
    -legend_labels "Max parents 3 Base" "Max parents 3 Hybrid" "Max parents 6 Base" "Max parents 6 Hybrid" \
    -o PP_MaxParents_3_6.pdf

python3 multi_variate_PP_bar.py -i PP_MaxParents_3.csv PP_MaxParents_6.csv -l MaxParents3 MaxParents6 -x EventTypes \
    -y TransmissionRatio TransmissionRatioCentral -c tab:blue tab:blue tab:orange tab:orange -t "" "//" "" "//" \
    -ln "Max parents 3 Base" "Max parents 3 Hybrid" "Max parents 6 Base" "Max parents 6 Hybrid" \
    -o PP_MaxParents_Whisker.pdf --x_label "Event types" --y_label "Transmission ratio"

#Secind Figure in Experiment in Paper
python3 plot_PP_generic.py -i combined_output.csv -l Ratio -x EventSkew -y TransmissionRatio TransmissionRatioINEv TransmissionRatioCentral \
    -c tab:blue tab:orange tab:green -s "-" "-" "-" --x_label "Event skew" --y_label "Transmission ratio" \
    -legend_labels "Base" "Improvement by push-pull" "Hybrid" -o PP_EventSkew.pdf

python3 multi_variate_PP_bar.py -i combined_output.csv -l Ratio -x EventSkew \
    -y TransmissionRatio TransmissionRatioINEv TransmissionRatioCentral -c tab:blue tab:orange tab:green \
    -t "" "" "" -ln "Base" "Improvement by push-pull" "Hybrid" \
    --x_label "Event skew" --y_label "Transmission ratio" -o PP_EventSkew_Whisker.pdf

#Third Figure in Experiment in Paper
python3 plot_PP_bars.py -i PP_MaxParents_3.csv PP_MaxParents_4.csv PP_MaxParents_5.csv PP_MaxParents_6.csv PP_MaxParents_7.csv PP_MaxParents_8.csv  \
    -l 3 4 5 6 7 8 -y TransmissionRatio TransmissionRatioCentral -o PP_MaxParents.pdf \
    --x_label "Max parents" --y_label "Transmission ratio" --legend_tags "Base" "Hybrid"

#Fourth Figure in Experiment in Paper
python3 plot_PP_generic.py -i PP_NER_Combined.csv -x EventNodeRatio -y TransmissionRatio TransmissionRatioCentral \
    -l AvgTransmissionRatio -c tab:blue tab:orange -s "-" "-" --x_label "Node event ratio" --y_label "Transmission ratio" \
    -o Fig_Transmission_Ratio_NER_PP_Combined.pdf -legend_labels "Base" "Hybrid"

python3 multi_variate_PP_bar.py -i PP_NER_Combined.csv -y TransmissionRatio TransmissionRatioCentral -x EventNodeRatio \
    -l AvgTransmissionRatio -o Fig_Bar_TransmissionRatio_NER_Combined.pdf -c tab:blue tab:orange \
    --x_label "Node event ratio" --y_label "Transmission ratio" -ln "Base" "Hybrid"
