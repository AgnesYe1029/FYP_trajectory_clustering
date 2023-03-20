import numpy as np
import pandas as pd
import math
import pickle
from sklearn.cluster import *
from sklearn import preprocessing

class TrajectoryBehaviorExtraction:

    def add_timestamps(self, orig_traj_list):
        print("start adding timestamps...")
        sample_rate = 15 # sample rate is 15s
        input_traj_with_time_stamp = []
        for t in orig_traj_list:
            traj_with_time = []
            timestamp = 0
            for loc_pair in t:
                traj_with_time.append([timestamp, loc_pair[1], loc_pair[0]]) # reverse as long, lat
                timestamp += sample_rate
            input_traj_with_time_stamp.append(traj_with_time)
        print("adding timestamps done!")
        return input_traj_with_time_stamp

    def complete_trajectories(self, input_traj, folder = 'new_output_data'):
        print("start completing trajectories...")
        completed_trajectories = []
        for traj in input_traj:
            completed_single_traj = []
            for i in range(0, len(traj)):
                rec = []
                if i==0:
                    rec = [0, 0, 0, 0]
                else:
                    locC = math.sqrt((traj[i][1]-traj[i-1][1])**2+(traj[i][2]-traj[i-1][2])**2)
                    rec.append(traj[i][0])
                    rec.append(locC)
                    if traj[i][0]-traj[i-1][0] == 0:
                        rec.append(0)
                    else:  
                        rec.append(locC/(traj[i][0]-traj[i-1][0]))
                    if traj[i][1]-traj[i-1][1] == 0:
                        rec.append(0)
                    else:
                        rec.append(math.atan((traj[i][2]-traj[i-1][2])/(traj[i][1]-traj[i-1][1])))
                completed_single_traj.append(rec)
            completed_trajectories.append(completed_single_traj)
        with open("./" + folder + "/completed_trajectories.pkl", "wb") as f:
            pickle.dump(completed_trajectories, f)
        print("completing trajectories done!")
        return completed_trajectories
    
    def computeFeatures(self, folder = 'new_output_data'):
        print("start computing trajectories features...")
        with open("./" + folder + "/completed_trajectories.pkl", "rb") as f:
            completed_traj = pickle.load(f)
        trajectories_features = []
        for t in completed_traj:
            t_features = []
            for i in range(0, len(t)):
                rec = []
                if i == 0:
                    rec = [0, 0, 0, 0] # time, change of location change, change of speed change, change of rot change
                else:
                    locC = t[i][1]
                    locCrate = locC/(t[i][0]-t[i-1][0])
                    rec.append(t[i][0])
                    rec.append(locCrate)
                    rec.append(t[i][2]-t[i-1][2])
                    rec.append(t[i][3]-t[i-1][3])
                t_features.append(rec)
            trajectories_features.append(t_features)
        with open("./" + folder + "/trajectories_features.pkl", "wb") as f:
            pickle.dump(trajectories_features, f)
        print("computing trajectories features done!")
        return trajectories_features
    
    def rolling_window(self, sample, window_size=120, offset=60):
    # offset = 1/2 * window_size achieves better performance
        time_length = sample[-1][0]
        window_length = int(time_length/offset)+1
        windows = []
        for i in range(0, window_length):
            windows.append([])
        
        for rec in sample:
            time = rec[0]
            for i in range(0, window_length):
                if (time > (i * offset) and (time < (i * offset + window_size))):
                    windows[i].append(rec)
        return windows
    
    def extract_behavior(self, windows):
        behavior_sequence = []
        for window in windows:
            behavior_feature = []
            records = np.array(window)
            if len(records) != 0:
                df = pd.DataFrame(records)
                df_des = df.describe()
                # mean values
                behavior_feature.append(df_des[1][1])
                behavior_feature.append(df_des[2][1])
                behavior_feature.append(df_des[3][1])
                # min values
                behavior_feature.append(df_des[1][3])
                behavior_feature.append(df_des[2][3])
                behavior_feature.append(df_des[3][3])
                # 25% percentile
                behavior_feature.append(df_des[1][4])
                behavior_feature.append(df_des[2][4])
                behavior_feature.append(df_des[3][4])
                # 50% percentile
                behavior_feature.append(df_des[1][5])
                behavior_feature.append(df_des[2][5])
                behavior_feature.append(df_des[3][5])
                # 75% percentile
                behavior_feature.append(df_des[1][6])
                behavior_feature.append(df_des[2][6])
                behavior_feature.append(df_des[3][6])
                # max values
                behavior_feature.append(df_des[1][7])
                behavior_feature.append(df_des[2][7])
                behavior_feature.append(df_des[3][7])
                
                behavior_sequence.append(behavior_feature)
        return behavior_sequence
    
    def generate_behavior_sequences(self, window_size, folder = 'new_output_data', ):
        print("start generating behavior sequences...")
        with open("./" + folder + "/trajectories_features.pkl", "rb") as f:
            traj_features = pickle.load(f)
        behavior_sequences = []
        
        for sample in traj_features:
            windows = self.rolling_window(sample, window_size, window_size//2)
            behavior_sequence = self.extract_behavior(windows)
            behavior_sequences.append(behavior_sequence)
        with open("./" + folder + "/traj_behavor_sequences.pkl", "wb") as fout:
            pickle.dump(behavior_sequences, fout)
        print("generating behavior sequences done!")
        return behavior_sequences
    
    def generate_normalized_behavior_sequence(self, folder = 'new_output_data'):
        print("start normalizing behavior sequences...")
        with open("./" + folder + "/traj_behavor_sequences.pkl", "rb") as fread:
            behavior_sequences = pickle.load(fread)
        
        normalized_behavior_sequences = []
        temp_list = []
        for seq in behavior_sequences:
            for s in seq:
                temp_list.append(s)
        min_max_scaler = preprocessing.MinMaxScaler()
        temp_list_normal = min_max_scaler.fit_transform(temp_list).tolist()
        index = 0
        for seq in behavior_sequences:
            normalized_behavior_sequence = []
            for s in seq:
                normalized_behavior_sequence.append(temp_list_normal[index])
                index += 1
            normalized_behavior_sequences.append(normalized_behavior_sequence)
        with open("./" + folder + "/normal_traj_behavior_sequences.pkl", "wb") as fout:
            pickle.dump(normalized_behavior_sequences, fout)
        print("normalizing behavior sequence done!")
        return normalized_behavior_sequences