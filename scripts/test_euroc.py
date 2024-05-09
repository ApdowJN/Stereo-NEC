import sys
import pandas as pd
from tqdm import tqdm
import numpy as np
import os
import glob 
import time
import argparse
import matplotlib.pyplot as plt

def extract_number(s):
    return int(s[s.find('(') + 1 : s.find(')')])

def load_gt_file(gt_file):
    df = pd.read_csv(gt_file)

    # timestamp
    timestamp_column = (df['#timestamp'].to_numpy(dtype=float))/1e9
    
    # position
    px = df[" p_RS_R_x [m]"]
    py = df[" p_RS_R_y [m]"]
    pz = df[" p_RS_R_z [m]"]

    # orientation
    qw = df[" q_RS_w []"]
    qx = df[" q_RS_x []"]
    qy = df[" q_RS_y []"]
    qz = df[" q_RS_z []"]

    xyz = np.column_stack((px, py, pz))
    quat = np.column_stack((qw, qx, qy, qz))

    gt_traj = PoseTrajectory3D(xyz, quat, timestamp_column)
    return gt_traj


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument("--datapath", help="path to euroc sequence")
    parser.add_argument("--est_folder_path", help="path to est folder")
    parser.add_argument("--gt", help="path to gt file")

    args = parser.parse_args()

    import evo
    from evo.core.trajectory import PoseTrajectory3D
    from evo.tools import file_interface
    from evo.core import sync
    import evo.main_ape as main_ape
    import evo.main_rpe as main_rpe
    from evo.core.metrics import PoseRelation
    from evo.core.metrics import Unit
    import math

    # Load gt
    traj_gt = load_gt_file(args.gt)

    # Load est traj files
    csv_files = [file for file in os.listdir(args.est_folder_path) if file.endswith('.csv')]
    indices = np.lexsort((csv_files, [extract_number(s) for s in csv_files]))
    csv_sorted_files = np.array(csv_files)[indices]

    ate_rmses_imuonly = []
    rre_rmses_imuonly = []

    ate_rmses_viba = []
    rre_rmses_viba = []

    for csv_file in csv_sorted_files:
        csv_file_path = os.path.join(args.est_folder_path, csv_file) #args_folder_path => args.est_folder_path
        if  "imuonly" in csv_file_path:
            df = pd.read_csv(csv_file_path, sep=' ', header=None)
            timestamps = df.iloc[:, 0].values
            positions = df.iloc[:, 1:4].values
            orientations = df.iloc[:, 4:9].values
            # Convert Quaternion (qx, qy, qz, qw) to (qw, qx, qy, qz) convention for orientation
            orientations = np.roll(orientations, shift=1, axis=1)

            traj_est = np.column_stack((positions, orientations))
            traj_est = PoseTrajectory3D(
            positions_xyz= traj_est[:,:3],
            orientations_quat_wxyz=traj_est[:,3:],
            timestamps=timestamps)


            # Evaluate ATE
            ref_traj, est_traj = sync.associate_trajectories(traj_gt, traj_est)
            result = main_ape.ape(ref_traj, est_traj, est_name='traj', 
            pose_relation=PoseRelation.translation_part, align=True, correct_scale=False)
            # print(result)
            err = result.np_arrays["error_array"]
            squared_errors = np.power(err, 2)
            traj_rmse = math.sqrt(np.mean(squared_errors))
            ate_rmses_imuonly.append(traj_rmse)

            # Evaluate RRE
            # ref_traj, est_traj = sync.associate_trajectories(traj_gt, traj_est)
            result = main_rpe.rpe(ref_traj, est_traj, est_name='rot', 
            pose_relation=PoseRelation.rotation_angle_deg, delta= 1.0, delta_unit=Unit.frames,  align=True, correct_scale=False)
            err = result.np_arrays["error_array"]
            squared_errors = np.power(err, 2)
            rot_rmse = math.sqrt(np.mean(squared_errors))
            rre_rmses_imuonly.append(rot_rmse)

        if  "viba" in csv_file_path:
            df = pd.read_csv(csv_file_path, sep=' ', header=None)
            timestamps = df.iloc[:, 0].values
            positions = df.iloc[:, 1:4].values
            orientations = df.iloc[:, 4:9].values
            # Convert Quaternion (qx, qy, qz, qw) to (qw, qx, qy, qz) convention for orientation
            orientations = np.roll(orientations, shift=1, axis=1)

            traj_est = np.column_stack((positions, orientations))
            traj_est = PoseTrajectory3D(
            positions_xyz= traj_est[:,:3],
            orientations_quat_wxyz=traj_est[:,3:],
            timestamps=timestamps)


            # Evaluate ATE
            ref_traj, est_traj = sync.associate_trajectories(traj_gt, traj_est)
            result = main_ape.ape(ref_traj, est_traj, est_name='traj', 
            pose_relation=PoseRelation.translation_part, align=True, correct_scale=False)
            # print(result)
            err = result.np_arrays["error_array"]
            squared_errors = np.power(err, 2)
            traj_rmse = math.sqrt(np.mean(squared_errors))
            ate_rmses_viba.append(traj_rmse)

            # Evaluate RRE
            # ref_traj, est_traj = sync.associate_trajectories(traj_gt, traj_est)
            result = main_rpe.rpe(ref_traj, est_traj, est_name='rot', 
            pose_relation=PoseRelation.rotation_angle_deg, delta= 1.0, delta_unit=Unit.frames,  align=True, correct_scale=False)
            err = result.np_arrays["error_array"]
            squared_errors = np.power(err, 2)
            rot_rmse = math.sqrt(np.mean(squared_errors))
            rre_rmses_viba.append(rot_rmse)
            

    # Print the results
    print("ATE of W/O VIBA")
    # Compute the mean
    ate_rmses_arr = np.array(ate_rmses_imuonly)
    mean_value = np.mean(ate_rmses_arr)
    median_value = np.median(ate_rmses_arr)
    # Compute the variance
    variance_value = np.std(ate_rmses_arr)
    print("Mean:", mean_value)
    print("Median:", median_value)
    print("std:", variance_value)


    # print("-----"*10)

    print("RRE of W/O VIBA")
    rre_rmses_arr = np.array(rre_rmses_imuonly)
    mean_value = np.mean(rre_rmses_arr)
    median_value = np.median(rre_rmses_arr)
    variance_value = np.std(rre_rmses_arr)
    print("Mean:", mean_value)
    print("Median:", median_value)
    print("std:", variance_value)

    print("- - -"*10)

    print("ATE of W/ VIBA")
    # Compute the mean
    ate_rmses_arr = np.array(ate_rmses_viba)
    mean_value = np.mean(ate_rmses_arr)
    median_value = np.median(ate_rmses_arr)
    # Compute the variance
    variance_value = np.std(ate_rmses_arr)
    min_value = np.min(ate_rmses_arr)
    print("Mean:", mean_value)
    print("Median:", median_value)
    print("Min:", min_value)
    # print("std:", variance_value)

    print("RRE of W/ VIBA")
    rre_rmses_arr = np.array(rre_rmses_viba)
    mean_value = np.mean(rre_rmses_arr)
    median_value = np.median(rre_rmses_arr)
    variance_value = np.std(rre_rmses_arr)
    min_value = np.min(rre_rmses_arr)
    print("Mean:", mean_value)
    print("Min:", min_value)
    print("Median:", median_value)
    # print("std:", variance_value)
    print("====="*10)



