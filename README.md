# SCSE22-0161：Mining Big Spatial Data
&nbsp;
## Model 1: Trajectory Clustering with Polyline Reduction
### Requirements
numpy==1.21.5\
pandas==1.4.4\
folium==0.14.0\
hdbscan==0.8.29\
utm==0.7.0\
The package requirements has been consolidated at model_1/requirements.txt.
&nbsp;

### Quick Demo
A demo with 1000 trajectories has been saved in https://github.com/AgnesYe1029/FYP_trajectory_clustering/blob/141bb4df901f9879a0a0fbe663a95b92a1ee7e9d/model_1/Model%201%20Demo.pdf.
The original jupyter notebook with interactive map visualization is also provided as model_1/Model 1 Demo. This notebook experiments with 1000 trajectories, and produces cluster results. You can run it if necessary.

&nbsp;
&nbsp;
&nbsp;

## Model 2: Trajectory Clustering with Deep Learning
### Requirements
numpy==1.21.5\
pandas==1.4.4\
tensorflow==2.11.0\
tensorflow-addons==0.19.0\
tensorflow-estimator==2.11.0\
keras==2.11.0\
folium==0.14.0\
hdbscan==0.8.29\
scikit-learn==1.0.2\
utm==0.7.0\
The package requirements has been consolidated at model_2/requirements.txt.
&nbsp;

### Training and Clustering
Due to the file size limit imposed by Git, only partial checkpoint files are uploaded. \
To run the model, first initiate an TrajPatternMiner object and supply the parameters:\
```
tpm = TrajPatternMiner(traj_to_try, learning_rate, training_epochs, \
                      display_step, units, batch_size, max_n_steps, frame_dim, window_size)
```
Start training by calling: 
```
trajVec = tpm.runTheModel()
```
Perform clustering on the vectors:
```
tpm.cluster_by_kmeans(trajVec, number_of_clusters)
```
&nbsp;
&nbsp;

## React.js Front-end Web Application
### Requirements:

&nbsp;
### To run:
1. cd to local directory and then cd to ```frontend``` directory.
```
cd frontend
```
3. run ```npm start```.
&nbsp;
&nbsp;
