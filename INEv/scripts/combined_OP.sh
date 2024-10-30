# Log file for errors
LOGFILE="error_log.txt"

# Redirect only stderr to the log file
exec 2> "$LOGFILE"


echo "Graph Density"
./sim_OP_GraphDensity.sh
echo "Query Size"
./sim_OP_Query.sh
echo "Sweet Spot"
./sim_OP_sweetSpot.sh
cd ../res
./compare_fog_plots.sh
./create_mulit_variate.sh