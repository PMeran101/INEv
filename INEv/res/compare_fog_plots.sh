#!/bin/sh
# lowerbound -> to parametrize
# python3 switchRows.py
#lower+0.01_real.csv lower+0.001_real.csv 
# python3 plot_generic.py -i lower+0.01_normal.csv lower+0.01.csv -x EventSkew -y TransmissionRatio -l INEv0.1 lower0.1 INEv0.01 lower0.01 -o Fig_4e_lowerbound_0.01
# python3 plot_generic.py -i lower+0.001_normal.csv lower+0.001.csv -x EventSkew -y TransmissionRatio -l INEv0.1 lower0.1 INEv0.01 lower0.01 -o Fig_4e_lowerbound_0.001

python3 plot_generic.py -i QWL5_normal.csv QWL5_Fog.csv -x EventTypes -y TransmissionRatio -l QWL5_INEv QWL5_Fog -o Fig_6a_overlap_QWL5.pdf # OVERLAP
echo "Finished QWL 5"
python3 plot_generic.py -i QWL10_normal.csv QWL10_Fog.csv -x EventTypes -y TransmissionRatio -l QWL10_INEv QWL10_Fog -o Fig_6a_overlap_QWL10.pdf # OVERLAP
echo "Finished QWL 10"
python3 plot_generic.py -i QWL20_normal.csv QWL20_Fog.csv -x EventTypes -y TransmissionRatio -l QWL20_INEv QWL20_Fog -o Fig_6a_overlap_QWL20.pdf # OVERLAP

# python3 plot_generic.py -i eventSkew_qwl+5_normal.csv eventSkew_qwl+5.csv -x EventSkew -y TransmissionRatio -l QWL5_INEv QWL5_Fog -o Fig_6b_eventSkew_QWL5normal.pdf # eventSkew
# python3 plot_generic.py -i eventSkew_qwl+10_normal.csv eventSkew_qwl+10.csv -x EventSkew -y TransmissionRatio -l QWL10_INEv QWL10_Fog -o Fig_6b_eventSkew_QWL10normal.pdf # eventSkew
# python3 plot_generic.py -i eventSkew_qwl+20_normal.csv eventSkew_qwl+20.csv -x EventSkew -y TransmissionRatio -l QWL20_INEv QWL20_Fog -o Fig_6b_eventSkew_QWL20normal.pdf # eventSkew

# python3 plot_generic.py -i eventNode_qwl+10_normal.csv eventNode_qwl+10.csv -x EventNodeRatio -y TransmissionRatio -l QWL10_INEv QWL10_Fog -o Fig_6d_eventNodeRatio_QWL10normal.pdf #eventNodeRatio
# python3 plot_generic.py -i eventNode_qwl+20_normal.csv eventNode_qwl+20.csv -x EventNodeRatio -y TransmissionRatio -l QWL20_INEv QWL20_Fog -o Fig_6d_eventNodeRatio_QWL20normal.pdf #eventNodeRatio

# python3 plot_generic.py -i nwSize_qwl+10_normal.csv nwSize_qwl+10.csv -x Nodes -y TransmissionRatio -l QWL10_INEv QWL10_Fog -o Fig_6c_Nodes_QWL10normal.pdf #NWSize
# python3 plot_generic.py -i nwSize_qwl+20_normal.csv nwSize_qwl+20.csv -x Nodes -y TransmissionRatio -l QWL20_INEv QWL20_Fog -o Fig_6c_Nodes_QWL20normal.pdf #NWSize

### KLEENE & NSEQ -> maybe use other line types

# python3 plot_generic.py -i KL+min+1.csv KL+min+0.csv KL+max+1.csv KL+max+0.csv -x EventSkew -y TransmissionRatio -l min_KL min_nKL max_KL max_nKL -o Fig_7a_Kleene.pdf # KLEENE, no KLeene

# python3 plot_generic.py -i NSEQ+min+1.csv KL+min+0.csv NSEQ+max+1.csv KL+max+0.csv -x EventSkew -y TransmissionRatio -l min_NSEQ min_SEQ max_NSEQ max_SEQ -o Fig_7b_NSEQ.pdf # NSEQ, no NSEQ



#computation Time
#merge all csv files for computation time projection

# python3 plot_generic_scatter.py -i eventSkew_qwl+20.csv  -x NumberProjections -y CombigenComputationTime -o Fig_10_computationTime_Projections
# python3 plot_generic_scatter.py -i computationTime.csv -x EventTypes -y CombigenComputationTime -o Fig_10_computationTime_QueryLen



