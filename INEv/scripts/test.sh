nwsize=16
log2=$(echo "scale=5; l($nwsize)/l(2)" | bc -l)
echo $log2