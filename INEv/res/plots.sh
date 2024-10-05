#!/bin/sh
# lowerbound -> to parametrize
python3 switchRows.py
<<<<<<< HEAD
#lower+0.01_real.csv lower+0.001_real.csv 
python3 plot_generic.py -i lower+0.01.csv lower+0.001.csv -x EventSkew -y TransmissionRatio -l INEv0.1 lower0.1 INEv0.01 lower0.01 -o Fig_4e_lowerbound
python3 plot_generic.py -i QWL5.csv QWL10.csv QWL20.csv -x EventTypes -y TransmissionRatio -l QWL5 QWL10 QWL20 -o Fig_6a_overlap.pdf # OVERLAP
python3 plot_generic.py -i eventSkew_qwl+5.csv eventSkew_qwl+10.csv eventSkew_qwl+20.csv -x EventSkew -y TransmissionRatio -l QWL5 QWL10 QWL20 -o Fig_6b_eventSkew.pdf # eventSkew
python3 plot_generic.py -i eventNode_qwl+10.csv eventNode_qwl+20.csv -x EventNodeRatio -y TransmissionRatio -l QWL5 QWL10 QWL20 -o Fig_6d_eventNodeRatio.pdf #eventNodeRatio
python3 plot_generic.py -i nwSize_qwl+10.csv nwSize_qwl+20.csv -x Nodes -y TransmissionRatio -l QWL5 QWL10 QWL20 -o Fig_6c_Nodes.pdf #NWSize
### KLEENE & NSEQ -> maybe use other line types

python3 plot_generic.py -i KL+min+1.csv KL+min+0.csv KL+max+1.csv KL+max+0.csv -x EventSkew -y TransmissionRatio -l min_KL min_nKL max_KL max_nKL -o Fig_7a_Kleene.pdf # KLEENE, no KLeene

python3 plot_generic.py -i NSEQ+min+1.csv KL+min+0.csv NSEQ+max+1.csv KL+max+0.csv -x EventSkew -y TransmissionRatio -l min_NSEQ min_SEQ max_NSEQ max_SEQ -o Fig_7b_NSEQ.pdf # NSEQ, no NSEQ
=======
#lower+0.01_real_Fog.csv lower+0.001_real_Fog.csv 
python3 plot_generic.py -i lower+0.01_Fog.csv lower+0.001_Fog.csv -x EventSkew -y TransmissionRatio -l INEv0.1 lower0.1 INEv0.01 lower0.01 -o Fig_4e_lowerbound
python3 plot_generic.py -i QWL5_Fog.csv QWL10_Fog.csv QWL20_Fog.csv -x EventTypes -y TransmissionRatio -l QWL5 QWL10 QWL20 -o Fig_6a_overlap.pdf # OVERLAP
python3 plot_generic.py -i eventSkew_qwl+5_Fog.csv eventSkew_qwl+10_Fog.csv eventSkew_qwl+20_Fog.csv -x EventSkew -y TransmissionRatio -l QWL5 QWL10 QWL20 -o Fig_6b_eventSkew.pdf # eventSkew
python3 plot_generic.py -i eventNode_qwl+10_Fog.csv eventNode_qwl+20_Fog.csv -x EventNodeRatio -y TransmissionRatio -l QWL5 QWL10 QWL20 -o Fig_6d_eventNodeRatio.pdf #eventNodeRatio
python3 plot_generic.py -i nwSize_qwl+10_Fog.csv nwSize_qwl+20_Fog.csv -x Nodes -y TransmissionRatio -l QWL5 QWL10 QWL20 -o Fig_6c_Nodes.pdf #NWSize
### KLEENE & NSEQ -> maybe use other line types

python3 plot_generic.py -i KL+min+1_Fog.csv KL+min+0_Fog.csv KL+max+1_Fog.csv KL+max+0_Fog.csv -x EventSkew -y TransmissionRatio -l min_KL min_nKL max_KL max_nKL -o Fig_7a_Kleene.pdf # KLEENE, no KLeene

python3 plot_generic.py -i NSEQ+min+1_Fog.csv KL+min+0_Fog.csv NSEQ+max+1_Fog.csv KL+max+0_Fog.csv -x EventSkew -y TransmissionRatio -l min_NSEQ min_SEQ max_NSEQ max_SEQ -o Fig_7b_NSEQ.pdf # NSEQ, no NSEQ
>>>>>>> fog_cloud_topology

#computation Time
#merge all csv files for computation time projection

<<<<<<< HEAD
python3 plot_generic_scatter.py -i eventSkew_qwl+20.csv  -x NumberProjections -y CombigenComputationTime -o Fig_10_computationTime_Projections
python3 plot_generic_scatter.py -i computationTime.csv -x EventTypes -y CombigenComputationTime -o Fig_10_computationTime_QueryLen
=======
python3 plot_generic_scatter.py -i eventSkew_qwl+20_Fog.csv  -x NumberProjections -y CombigenComputationTime -o Fig_10_computationTime_Projections
python3 plot_generic_scatter.py -i computationTime_Fog.csv -x EventTypes -y CombigenComputationTime -o Fig_10_computationTime_QueryLen
>>>>>>> fog_cloud_topology



