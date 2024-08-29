#!/bin/sh
# lowerbound -> to parametrize
# python3 switchRows.py
#lower+0.01_real.csv lower+0.001_real.csv 
# python3 plot_generic.py -i lower+0.01_normal.csv lower+0.01_fog.csv -x EventSkew -y TransmissionRatio -l INEv0.1 lower0.1 INEv0.01 lower0.01 -o Fig_4e_lowerbound_0.01
# python3 plot_generic.py -i lower+0.001_normal.csv lower+0.001_fog.csv -x EventSkew -y TransmissionRatio -l INEv0.1 lower0.1 INEv0.01 lower0.01 -o Fig_4e_lowerbound_0.001

python3 plot_generic.py -i QWL5_normal.csv QWL5_fog.csv -x EventTypes -y TransmissionRatio -l QWL5_INEv QWL5_Fog -o Fig_6a_overlap_QWL5.pdf # OVERLAP
python3 plot_generic.py -i QWL10_normal.csv QWL10_fog.csv -x EventTypes -y TransmissionRatio -l QWL10_INEv QWL10_Fog -o Fig_6a_overlap_QWL10.pdf # OVERLAP
python3 plot_generic.py -i QWL20_normal.csv QWL20_fog.csv -x EventTypes -y TransmissionRatio -l QWL20_INEv QWL20_Fog -o Fig_6a_overlap_QWL20.pdf # OVERLAP

python3 plot_generic.py -i eventSkew_qwl+5_normal.csv eventSkew_qwl+5_fog.csv -x EventSkew -y TransmissionRatio -l QWL5_INEv QWL5_Fog -o Fig_6b_eventSkew_QWL5.pdf # eventSkew
python3 plot_generic.py -i eventSkew_qwl+10_normal.csv eventSkew_qwl+10_fog.csv -x EventSkew -y TransmissionRatio -l QWL10_INEv QWL10_Fog -o Fig_6b_eventSkew_QWL10.pdf # eventSkew
python3 plot_generic.py -i eventSkew_qwl+20_normal.csv eventSkew_qwl+20_fog.csv -x EventSkew -y TransmissionRatio -l QWL20_INEv QWL20_Fog -o Fig_6b_eventSkew_QWL20.pdf # eventSkew

python3 plot_generic.py -i eventNode_qwl+10_normal.csv eventNode_qwl+10_fog.csv -x EventNodeRatio -y TransmissionRatio -l QWL10_INEv QWL10_normal -o Fig_6d_eventNodeRatio_QWL10.pdf #eventNodeRatio
python3 plot_generic.py -i eventNode_qwl+20_normal.csv eventNode_qwl+20_fog.csv -x EventNodeRatio -y TransmissionRatio -l QWL20_INEv QWL20_normal -o Fig_6d_eventNodeRatio_QWL20.pdf #eventNodeRatio

python3 plot_generic.py -i nwSize_qwl+10_normal.csv nwSize_qwl+10_fog.csv -x Nodes -y TransmissionRatio -l QWL10_INEv QWL10_Fog -o Fig_6c_Nodes_QWL10.pdf #NWSize
python3 plot_generic.py -i nwSize_qwl+20_normal.csv nwSize_qwl+20_fog.csv -x Nodes -y TransmissionRatio -l QWL20_INEv QWL20_Fog -o Fig_6c_Nodes_QWL20.pdf #NWSize

### KLEENE & NSEQ -> maybe use other line types

# python3 plot_generic.py -i KL+min+1.csv KL+min+0.csv KL+max+1.csv KL+max+0.csv -x EventSkew -y TransmissionRatio -l min_KL min_nKL max_KL max_nKL -o Fig_7a_Kleene.pdf # KLEENE, no KLeene

# python3 plot_generic.py -i NSEQ+min+1.csv KL+min+0.csv NSEQ+max+1.csv KL+max+0.csv -x EventSkew -y TransmissionRatio -l min_NSEQ min_SEQ max_NSEQ max_SEQ -o Fig_7b_NSEQ.pdf # NSEQ, no NSEQ



#computation Time
#merge all csv files for computation time projection

# python3 plot_generic_scatter.py -i eventSkew_qwl+20.csv  -x NumberProjections -y CombigenComputationTime -o Fig_10_computationTime_Projections
# python3 plot_generic_scatter.py -i computationTime.csv -x EventTypes -y CombigenComputationTime -o Fig_10_computationTime_QueryLen



