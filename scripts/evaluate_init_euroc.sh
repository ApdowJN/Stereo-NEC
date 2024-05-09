#!/bin/bash
EUROC_PATH=PATH_TO_EuRoC #Stereo-NEC/Datasets/EuRoC/
EST_PATH=PATH_TO_RESULTS_FOLDER #Stereo-NEC/results/
evalset=(
    MH_01_easy
    MH_02_easy
    MH_03_medium
    MH_04_difficult
    MH_05_difficult
    V1_01_easy
    V1_02_medium
    V1_03_difficult
    V2_01_easy
    V2_02_medium
    V2_03_difficult
)
cd Stereo-NEC/ # Ensure you are in the Stereo-NEC folder.
seqIndex=0
seqName=("MH01" "MH02" "MH03" "MH04" "MH05" "V101" "V102" "V103" "V201" "V202" "V203") 
for seq in ${evalset[@]}; do
    echo "Evaluate ours on $seq(${seqName[$seqIndex]})"
    python3 scripts/test_euroc.py --est_folder_path=$EST_PATH/${seqName[$seqIndex]} --gt=$EUROC_PATH/$seq/mav0/state_groundtruth_estimate0/data.csv $@
    echo "=================================================================================="
    echo "Evaluate ORB-SLAM3 on $seq(${seqName[$seqIndex]})"
    python3 scripts/test_euroc.py --est_folder_path=$EST_PATH/${seqName[$seqIndex]} --gt=$EUROC_PATH/$seq/mav0/state_groundtruth_estimate0/data.csv $@
    ((seqIndex++))
done
