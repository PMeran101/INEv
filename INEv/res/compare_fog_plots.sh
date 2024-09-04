#!/bin/sh
# lowerbound -> to parametrize
# python3 switchRows.py
#lower+0.01_real.csv lower+0.001_real.csv 
# python3 plot_generic.py -i lower+0.01_INEv_100.csv lower+0.01_fog_100.csv -x EventSkew -y TransmissionRatio -l INEv0.1 lower0.1 INEv0.01 lower0.01 -o Fig_4e_lowerbound_0.01
# python3 plot_generic.py -i lower+0.001_INEv_100.csv lower+0.001_fog_100.csv -x EventSkew -y TransmissionRatio -l INEv0.1 lower0.1 INEv0.01 lower0.01 -o Fig_4e_lowerbound_0.001

python3.8 plot_generic.py -i nodesize100/QWL5_INEv_100.csv nodesize100/QWL5_fog_100.csv -x EventTypes -y TransmissionRatio -l QWL5_INEv QWL5_Fog -o Fig_6a_overlap_QWL5_100Nodes.pdf # OVERLAP
python3.8 plot_generic.py -i nodesize100/QWL10_INEv_100.csv nodesize100/QWL10_fog_100.csv -x EventTypes -y TransmissionRatio -l QWL10_INEv QWL10_Fog -o Fig_6a_overlap_QWL10_100Nodes.pdf # OVERLAP
python3.8 plot_generic.py -i nodesize100/QWL20_INEv_100.csv nodesize100/QWL20_fog_100.csv -x EventTypes -y TransmissionRatio -l QWL20_INEv QWL20_Fog -o Fig_6a_overlap_QWL20_100Nodes.pdf # OVERLAP

python3 plot_generic.py -i nodesize100/eventSkew_qwl+5_INEv_100.csv nodesize100/eventSkew_qwl+5_fog_100.csv -x EventSkew -y TransmissionRatio -l QWL5_INEv QWL5_Fog -o Fig_6b_eventSkew_QWL5_100Nodes.pdf # eventSkew
python3 plot_generic.py -i nodesize100/eventSkew_qwl+10_INEv_100.csv nodesize100/eventSkew_qwl+10_fog_100.csv -x EventSkew -y TransmissionRatio -l QWL10_INEv QWL10_Fog -o Fig_6b_eventSkew_QWL10_100Nodes.pdf # eventSkew
python3 plot_generic.py -i nodesize100/eventSkew_qwl+20_INEv_100.csv nodesize100/eventSkew_qwl+20_fog_100.csv -x EventSkew -y TransmissionRatio -l QWL20_INEv QWL20_Fog -o Fig_6b_eventSkew_QWL20_100Nodes.pdf # eventSkew

python3 plot_generic.py -i nodesize100/eventNode_qwl+10_INEv_100.csv nodesize100/eventNode_qwl+10_fog_100.csv -x EventNodeRatio -y TransmissionRatio -l QWL10_INEv QWL10_Fog -o Fig_6d_eventNodeRatio_QWL10_100Nodes.pdf #eventNodeRatio
python3 plot_generic.py -i nodesize100/eventNode_qwl+20_INEv_100.csv nodesize100/eventNode_qwl+20_fog_100.csv -x EventNodeRatio -y TransmissionRatio -l QWL20_INEv QWL20_Fog -o Fig_6d_eventNodeRatio_QWL20_100Nodes.pdf #eventNodeRatio

python3 plot_generic.py -i nodesize100/nwSize_qwl+10_INEv_100.csv nodesize100/nwSize_qwl+10_fog_100.csv -x Nodes -y TransmissionRatio -l QWL10_INEv QWL10_Fog -o Fig_6c_Nodes_QWL10_100Nodes.pdf #NWSize
python3 plot_generic.py -i nodesize100/nwSize_qwl+20_INEv_100.csv nodesize100/nwSize_qwl+20_fog_100.csv -x Nodes -y TransmissionRatio -l QWL20_INEv QWL20_Fog -o Fig_6c_Nodes_QWL20_100Nodes.pdf #NWSize

### KLEENE & NSEQ -> maybe use other line types

# python3 plot_generic.py -i KL+min+1.csv KL+min+0.csv KL+max+1.csv KL+max+0.csv -x EventSkew -y TransmissionRatio -l min_KL min_nKL max_KL max_nKL -o Fig_7a_Kleene.pdf # KLEENE, no KLeene

# python3 plot_generic.py -i NSEQ+min+1.csv KL+min+0.csv NSEQ+max+1.csv KL+max+0.csv -x EventSkew -y TransmissionRatio -l min_NSEQ min_SEQ max_NSEQ max_SEQ -o Fig_7b_NSEQ.pdf # NSEQ, no NSEQ



#computation Time
#merge all csv files for computation time projection

# python3 plot_generic_scatter.py -i eventSkew_qwl+20.csv  -x NumberProjections -y CombigenComputationTime -o Fig_10_computationTime_Projections
# python3 plot_generic_scatter.py -i computationTime.csv -x EventTypes -y CombigenComputationTime -o Fig_10_computationTime_QueryLen



