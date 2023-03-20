# import the libraries
import numpy as np
import pandas as pd
import folium
import utm
from fixed_length_rdp import simplifyDouglasPeucker
import webbrowser
import os
import hdbscan

class TrajectoryClustering:
    def read_data(self, path):
        taxi_traj_df = pd.read_pickle("data/taxi_1500_sample.pkl")
        return taxi_traj_df

    def get_trajectories(self, traj_df):
        trajectories = list(traj_df["TRAJECTORY"])
        return trajectories

    def latitude_longtitude_coord_conversion(self, trajectories):
        trajectories_coordinates_xy = []
        for index, traj in enumerate(trajectories):
            if len(traj) >= 2:
                coords = np.array([list(utm.from_latlon(ll[0], ll[1])[:2]) for ll in traj])
            else:
                coords = []
            # slicing the returned result to retrieve the latitude and longtitude
            trajectories_coordinates_xy.append(coords)
        return trajectories_coordinates_xy
    
    def rdp_reduce(self, trajectories_in_latlon, trajectories_in_xy, output_len):
        traj_in_xy_reduced = []
        traj_in_lat_lon_keep = []
        for i, p in enumerate(trajectories_in_xy):
            try:
                traj_in_xy_reduced.append(simplifyDouglasPeucker(p.tolist(), output_len))
                traj_in_lat_lon_keep.append(trajectories_in_latlon[i])
            except:
                pass
        return traj_in_lat_lon_keep, traj_in_xy_reduced
    
    def reshape_trajectories(self, fixed_length, traj_in_xy_reduced):
        a=np.empty((len(traj_in_xy_reduced), fixed_length, 2), dtype=float)
        for i, x in enumerate(traj_in_xy_reduced):
            for j, y in enumerate(x):
                if (j == 15):
                    break
                a[i][j][0] = y[0]
                a[i][j][1] = y[1]
        dims = np.array(a).shape
        a_reshaped = np.array(a).reshape(dims[0], dims[1]*dims[2])
        print(a_reshaped.shape)
        return a_reshaped

    def trajectories_hdbscan(self, reshaped_trajectory_samples, min_size):
        hdb = hdbscan.HDBSCAN(min_cluster_size=min_size, gen_min_span_tree=True).fit(reshaped_trajectory_samples)
        labels = hdb.labels_
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise_ = list(labels).count(-1)
        print("Estimated number of clusters: %d" % n_clusters_)
        print("Estimated number of noise points: %d" % n_noise_)
        return labels
    
    def map_trajectory_with_cluster_labels(self, traj_to_keep, labels):
        hdb_clustered_trajectories_dict = dict()
        hdb_cluster_id = 1
        for i in range(0, len(traj_to_keep)):
            trajectory_lab = labels[i]
            if trajectory_lab in hdb_clustered_trajectories_dict.keys():
                hdb_clustered_trajectories_dict[trajectory_lab]['count'] += 1
                hdb_clustered_trajectories_dict[trajectory_lab]['trajectories'].append(traj_to_keep[i])
            else:
                hdb_clustered_trajectories_dict[trajectory_lab] = {
                    'cluster_id': hdb_cluster_id,
                    'count': 1,
                    'trajectories': [traj_to_keep[i]]
                }
                hdb_cluster_id += 1
        for key in hdb_clustered_trajectories_dict.keys():
            print(f"label: {key}, #traj: {len(hdb_clustered_trajectories_dict[key]['trajectories'])}")
        return hdb_clustered_trajectories_dict

    def plot_group_trajectories(self, groupNo, traj_clustered_dict, relative_path):
        label_group = traj_clustered_dict[groupNo]['trajectories']
        label_group_start = list(traj_clustered_dict[groupNo]['trajectories'][0][0])
        m = folium.Map(location=label_group_start, zoom_start=12)
        for index, x in enumerate(label_group):
            folium.PolyLine(label_group[index]).add_to(m)
        m.save(relative_path)
        print("saved")
        return m

    def plot_group_trajectories_only(self, groupNo, traj_clustered_dict):
        label_group = traj_clustered_dict[groupNo]['trajectories']
        label_group_first = list(traj_clustered_dict[groupNo]['trajectories'][0])
        label_group_start = [(label_group_first[0][0] + label_group_first[-1][0])/2, \
                    (label_group_first[0][1] + label_group_first[-1][1])/2]
        m = folium.Map(location=label_group_start, zoom_start=11)
        for index, x in enumerate(label_group):
            folium.PolyLine(label_group[index]).add_to(m)
        return m

    def plot_all_trajectories_using_folium(self, traj_to_plot, path="html_map_output/all_trajectories.html"):
        m = folium.Map(location=traj_to_plot[0][0], zoom_start=11)
        for index, x in enumerate(traj_to_plot):
            folium.PolyLine(traj_to_plot[index]).add_to(m)
        m.save(path)
        return m

    def plot_all_trajectories_only(self, traj_to_plot):
        start_loc = [(traj_to_plot[0][0][0] + traj_to_plot[0][-1][0])/2, \
                    (traj_to_plot[0][0][1] + traj_to_plot[0][-1][1])/2]
        m = folium.Map(location=traj_to_plot[0][0], zoom_start=9)
        for index, x in enumerate(traj_to_plot):
            folium.PolyLine(traj_to_plot[index]).add_to(m)
        return m
        
    
    def all_trajectories(self):
        rdp_output_length = 15
        file_path = "data/taxi_1500_sample.pkl"
        df = self.read_data(file_path)
        trajectories = self.get_trajectories(df)
        trajectories_xy = self.latitude_longtitude_coord_conversion(trajectories)
        traj_to_keep, traj_xy_reduced = self.rdp_reduce(trajectories, trajectories_xy, rdp_output_length)
        return traj_to_keep, traj_xy_reduced

    def grouped_trajectories(self):
        rdp_output_length = 15
        traj_to_keep, traj_xy_reduced = self.all_trajectories()
        reshaped_traj = self.reshape_trajectories(rdp_output_length, traj_xy_reduced)
        labels = self.trajectories_hdbscan(reshaped_traj)
        traj_dict = self.map_trajectory_with_cluster_labels(traj_to_keep, labels)
        groups = [0, 1, 2]
        res_traj_groups = []
        for grpNo in groups:
            res_traj_groups.append(traj_dict[grpNo]['trajectories'])
        return res_traj_groups



if __name__ == "__main__":
    # print("Start Reading") # Hello
    # rdp_output_length = 15
    # file_path = "data/taxi_1500_sample.pkl"
    # df = TrajectoryClustering.read_data(file_path)
    # trajectories = TrajectoryClustering.get_trajectories(df)
    # trajectories_xy = TrajectoryClustering.latitude_longtitude_coord_conversion(trajectories)
    # traj_to_keep, traj_xy_reduced = TrajectoryClustering.rdp_reduce(trajectories, trajectories_xy, rdp_output_length)
    # TrajectoryClustering.plot_all_trajectories_using_folium(traj_to_keep)
    # # all_traj_map_path = 'file:///'+os.getcwd()+'/'+"html_map_output/all_trajectories.html"
    # # webbrowser.open_new_tab(all_traj_map_path)
    # reshaped_traj = TrajectoryClustering.reshape_trajectories(rdp_output_length, traj_xy_reduced)
    # labels = TrajectoryClustering.trajectories_hdbscan(reshaped_traj)
    # traj_dict = TrajectoryClustering.map_trajectory_with_cluster_labels(traj_to_keep, labels)
    
    # grp_no = 2
    # relative_map_path = "html_map_output/grp_" + str(grp_no) + "_trajectories.html"
    # grp_traj_map_path = 'file:///'+os.getcwd()+'/'+ relative_map_path
    # TrajectoryClustering.plot_group_trajectories(grp_no, traj_dict, relative_map_path)
    # webbrowser.open_new_tab(grp_traj_map_path)

    tc = TrajectoryClustering()
    print(tc.grouped_trajectories())



    