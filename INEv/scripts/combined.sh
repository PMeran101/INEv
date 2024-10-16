#!/bin/sh
echo "conflicting"
./conflicting_qwl.sh
echo "EventSkew"
./eventSkew_qwl.sh
echo "Execution Time: $(date)"
echo "NWSize"
./nwSize_qwl.sh
echo "Execution Time: $(date)"
echo "EventNode"
./eventNode_qwl.sh
echo "Execution Time: $(date)"
echo "Lower Bound"
./lower_bound.sh
echo "Execution Time: $(date)"
echo "NSEQ, KLEENE"
./negated_unnegated.sh
echo "Execution Time: $(date)"
echo "Computation Time"
./computation_time.sh
cd ../res
./plots.sh
cd figs
cp * ../../../Figures
