echo "Operator Placement Experiments"
./combined_OP.sh
cd ../res
./Exp1_OperatorPlacement.sh
cd ../scripts

echo "Push Pull and Operator Placement combination"
./combined_PP.sh
cd ../res
./Exp2_PushPull.sh
cd ../scripts

echo "Scaling to real Network Sizes"
./combined_OP_scaled.sh
