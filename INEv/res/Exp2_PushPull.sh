#Firt Figure in Experiment in Paper
python3 plot_PP_generic.py -i PP_MaxParents_3.csv PP_MaxParents_6.csv -l MaxParents3 MaxParents6 -x EventTypes \
    -y TransmissionRatio TransmissionRatioCentral -c tab:blue tab:blue tab:orange tab:orange -s "-" "dashed" "-" "dashed" \
    --x_label "Event Types" --y_label "Transmission ratio" \
    -legend_labels "Max parents 3 operator placement" "Max parents 3 push pull" "Max parents 6 operator placement" "Max parents 6 push pull" \
    -o PP_MaxParents_3_6.pdf
python3 multi_variate_PP_bar.py -i PP_MaxParents_3.csv PP_MaxParents_6.csv -l MaxParents3 MaxParents6 -x EventTypes \
    -y TransmissionRatio TransmissionRatioCentral -c tab:blue tab:blue tab:orange tab:orange -t "" "//" "" "//" \
    -ln "Max parents 3 operator placement" "Max parents 3 push pull" "Max parents 6 operator placement" "Max parents 6 push pull" \
    -o PP_MaxParents_Whisker.pdf --x_label "Event Types" --y_label "Transmission ratio"
#Secind Figure in Experiment in Paper
python3 plot_PP_generic.py -i combined_output.csv -l Ratio -x EventSkew -y TransmissionRatio TransmissionRatioINEv TransmissionRatioCentral \
    -c tab:blue tab:orange tab:green -s "-" "-" "-" --x_label "Event skew" --y_label "Transmission ratio" \
    -legend_labels "Operator placement ratio to central" "Push pull ratio to operator placement" "Push pull ratio to central" -o PP_EventSkew.pdf
python3 multi_variate_PP_bar.py -i combined_output.csv -l Ratio -x EventSkew \
    -y TransmissionRatio TransmissionRatioINEv TransmissionRatioCentral -c tab:blue tab:orange tab:green \
    -t "" "" "" -ln "Operator placement ratio to central" "Push pull ratio to operator placement" "Push pull ratio to central" \
    --x_label "Event skew" --y_label "Transmission ratio" -o PP_EventSkew_Whisker.pdf

#Third Figure in Experiment in Paper
python3 plot_PP_bars.py -i PP_MaxParents_3.csv PP_MaxParents_4.csv PP_MaxParents_5.csv PP_MaxParents_6.csv PP_MaxParents_7.csv PP_MaxParents_8.csv  \
    -l 3 4 5 6 7 8 -y TransmissionRatio TransmissionRatioCentral -o PP_MaxParents.pdf \
    --x_label "Max parents" --y_label "Transmission ratio" --legend_tags "Transmission ratio operator placement" "Transmission ratio push pull"
#Fourth Figure in Experiment in Paper
python3 plot_PP_generic.py -i PP_NER_Combined.csv -x EventNodeRatio -y TransmissionRatio TransmissionRatioCentral \
    -l AvgTransmissionRatio -c tab:blue tab:orange -s "-" "-" --x_label "Event node ratio" --y_label "Transmission ratio" \
    -o Fig_Transmission_Ratio_NER_PP_Combined.pdf -legend_labels "Transmission ratio operator placement" "Transmission ratio push pull"
python3 multi_variate_PP_bar.py -i PP_NER_Combined.csv -y TransmissionRatio TransmissionRatioCentral -x EventNodeRatio \
    -l AvgTransmissionRatio -o Fig_Bar_TransmissionRatio_NER_Combined.pdf -c tab:blue tab:orange \
    --x_label "Event node ratio" --y_label "Transmission ratio" -ln "Transmission ratio operator placement" "Transmission ratio push pull"
