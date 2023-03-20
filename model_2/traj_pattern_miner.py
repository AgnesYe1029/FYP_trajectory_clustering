from trajectory_behavior_extraction import TrajectoryBehaviorExtraction
from traj2vec import Traj2Vec
import numpy as np
import utm
import folium
from sklearn.cluster import KMeans

class TrajPatternMiner:
    def __init__(self, traj, learning_rate, training_epochs, display_step, units, batch_size, max_n_steps, frame_dim, window_size) -> None:
        self.traj = traj
        self.learning_rate = learning_rate
        self.training_epochs = training_epochs
        self.display_step = display_step
        self.units = units
        self.batch_size = batch_size
        self.max_n_steps = max_n_steps
        self.frame_dim = frame_dim
        self.window_size = window_size
        self.txc = TrajectoryBehaviorExtraction()
        self.t2v = Traj2Vec(self.learning_rate, self.training_epochs, self.display_step, self.units, self.batch_size, self.frame_dim)
    
    def latitude_longtitude_coord_conversion(self, trajectories):
        trajectories_coordinates = []
        for index, traj in enumerate(trajectories):
            if len(traj) >= 2:
                coords = np.array([list(utm.from_latlon(ll[0], ll[1])[:2]) for ll in traj])
            else:
                coords = []
            # slicing the returned result to retrieve the latitude and longtitude
            trajectories_coordinates.append(coords)
        return trajectories_coordinates

    def plot_all_traj(self, traj):
        m = folium.Map(location=traj[0][0], zoom_start=11)
        for index, x in enumerate(traj):
            folium.PolyLine(traj[index]).add_to(m)
        return m
    
    def runTheModel(self):
        traj_xy = self.latitude_longtitude_coord_conversion(self.traj)
        
        # behavior extraction
        trajs = self.txc.add_timestamps(traj_xy)
        self.txc.complete_trajectories(trajs)
        self.txc.computeFeatures()
        self.txc.generate_behavior_sequences(self.window_size)
        behave_seq_norm = self.txc.generate_normalized_behavior_sequence()

        traj_vecs = self.t2v.traj2vec_model(behave_seq_norm)

        return traj_vecs
    
    def cluster_by_kmeans(self, trajectoryVecs, n_clusters):
        new_vecs = []
        for i, vec in enumerate(trajectoryVecs):
            new_vecs.append(vec[0][0])
        kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init="auto").fit(new_vecs)
        labels = kmeans.labels_
        
        clustered_trajectories_dict = dict()
        cluster_id = 1
        for i in range(0, len(self.traj)):
            trajectory_lab = labels[i]
            if trajectory_lab in clustered_trajectories_dict.keys():
                clustered_trajectories_dict[trajectory_lab]['count'] += 1
                clustered_trajectories_dict[trajectory_lab]['trajectories'].append(self.traj[i])
            else:
                clustered_trajectories_dict[trajectory_lab] = {
                    'cluster_id': cluster_id,
                    'count': 1,
                    'trajectories': [self.traj[i]]
                }
                cluster_id += 1
        for key in clustered_trajectories_dict.keys():
            print(f"label: {key}, #traj: {len(clustered_trajectories_dict[key]['trajectories'])}")
        return clustered_trajectories_dict






