# SCSE22-0161：Mining Big Spatial Data
## Project Introduction:
This is my final year project. A large [geospatial taxi trajectory dataset](https://www.kaggle.com/datasets/crailtap/taxi-trajectory) is used as dataset.
The goal of project is to mine the patterns of trajectories and cluster trajectories into groups based on the pattern. To achieve this goal, two trajectory clustering models are presented, and a web-based front-end application is developed for visualization. \
The first trajectory clustering model mainly contains a trajectory reduction layer and a trajectory clustering layer. The trajectory reduction layer utilizes Ramer–Douglas–Peucker Algorithm to reduce the size of trajectories, while preserving the geometric shape. The trajectory clustering layer adopts Hierarchical Density-Based Spatial Clustering of Applications with Noise (HDBSCAN) algorithm to produce clusters out of the reduced trajectories. This model is able to cluster long trajectories, but it cannot identify intertwined and dense trajectories.\
The second model resolves the bottleneck by introducing Reccurent Neural Network (RNN) with a behavior extraction algorithm. The model consists of three layers: trajectory feature extraction, trajectory pattern mining and trajectory clustering. Trajectory feature extraction layer summarizes the trajectory moving pattern using sliding window. Trajectory pattern mining layer accepts the patterns and learns vector representation from them, using sequence-to-sequence encoder-decoder model with attention. The vectors are then clustered by K-means in trajectory clustering layer. This 3-layer model outperforms our first model as it is able to produce fairly distributed clusters, and group the trajectories with higher precision.\
To facilitate the visualization, a web-based front-end application is developed using React.js. It displays the trajectory cluster on the map, and interacts with user to render details of the cluster.\
Kindly refer to my [final year paper](https://docs.google.com/document/d/1j8JpARGWVxokr4WceYHK6qNbG8tF7QNtXqWZQ1kavv0/edit?usp=sharing) for more details and technicals.
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
A demo with 1000 trajectories has been saved in [model_1/Model Demo](./model_1/Model%201%20Demo.pdf).
The original jupyter notebook with interactive map visualization is also provided as [model_1/Model 1 Demo.ipynb](./model_1/Model%201%20Demo.ipynb). This notebook experiments with 1000 trajectories, and produces cluster results. You can run it if necessary.

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
### To run:
1. cd to local directory and then cd to ```frontend``` directory.
```
cd frontend
```
3. run ```npm start```.
&nbsp;
&nbsp;
