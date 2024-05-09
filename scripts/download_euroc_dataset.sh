#!/bin/bash
DIRECTORY="Dataset/EuRoC"
mkdir -p "$DIRECTORY"
cd "$DIRECTORY"
mkdir MH_01_easy
wget http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/machine_hall/MH_01_easy/MH_01_easy.zip
unzip MH_01_easy.zip
mv mav0 MH_01_easy


mkdir MH_02_easy
wget http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/machine_hall/MH_02_easy/MH_02_easy.zip
unzip MH_02_easy.zip
mv mav0 MH_02_easy

mkdir MH_03_medium
wget http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/machine_hall/MH_03_medium/MH_03_medium.zip
unzip MH_03_medium.zip
mv mav0 MH_03_medium

mkdir MH_04_difficult
wget http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/machine_hall/MH_04_difficult/MH_04_difficult.zip
unzip MH_04_difficult.zip
mv mav0 MH_04_difficult

mkdir MH_05_difficult
wget http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/machine_hall/MH_05_difficult/MH_05_difficult.zip
unzip MH_05_difficult.zip
mv mav0 MH_05_difficult

mkdir V1_01_easy
wget http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/vicon_room1/V1_01_easy/V1_01_easy.zip
unzip V1_01_easy.zip
mv mav0 V1_01_easy

mkdir V1_02_medium
wget http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/vicon_room1/V1_02_medium/V1_02_medium.zip
unzip V1_02_medium.zip
mv mav0 V1_02_medium

mkdir V1_03_difficult
wget http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/vicon_room1/V1_03_difficult/V1_03_difficult.zip
unzip V1_03_difficult.zip
mv mav0 V1_03_difficult

mkdir V2_01_easy
wget http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/vicon_room2/V2_01_easy/V2_01_easy.zip
unzip V2_01_easy.zip
mv mav0 V2_01_easy

mkdir V2_02_medium
wget http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/vicon_room2/V2_02_medium/V2_02_medium.zip
unzip V2_02_medium.zip
mv mav0 V2_02_medium

mkdir V2_03_difficult
wget http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/vicon_room2/V2_03_difficult/V2_03_difficult.zip
unzip V2_03_difficult.zip
mv mav0 V2_03_difficult

# Check if the directory exists and is accessible
if [ $? -eq 0 ]; then
    # Remove all zip files in the directory
    rm -f *.zip
    echo "All zip files have been deleted from $DIRECTORY."
else
    echo "Failed to access directory: $DIRECTORY"
fi


