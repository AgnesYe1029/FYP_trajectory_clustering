import React, { createRef, Component } from "react";
import { Tabs, Tab } from "react-bootstrap";
import * as L from "leaflet";
import {
  MapContainer,
  Marker,
  Popup,
  TileLayer,
  Polyline,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import readGroupTrajData from "./readGroupTrajData";
import PatternDetails from "./patternDetails";

class MapTab extends Component {
  constructor(props) {
    super(props);
    this.mapDiv1Ref = createRef();
    this.mapDiv2Ref = createRef();
    this.mapDiv3Ref = createRef();
    this.mapDiv4Ref = createRef();
    this.mapDiv5Ref = createRef();
    this.mapDiv6Ref = createRef();
    this.map1Ref = createRef();
    this.map2Ref = createRef();
    this.map3Ref = createRef();
    this.map4Ref = createRef();
    this.map5Ref = createRef();
    this.map6Ref = createRef();
    this.allTraj1 = props.allTraj1;
    this.state = {
      key: 1,
    };
  }

  onSelect(key) {
    this.setState({ key });
    console.log("key: " + key);
    if (key == 1) {
      setTimeout(() => {
        this.map1Ref.current.invalidateSize(false);
      }, 10);
    } else if (key == 2) {
      setTimeout(() => {
        this.map2Ref.current.invalidateSize(false);
      }, 10);
    } else if (key == 3) {
      setTimeout(() => {
        this.map3Ref.current.invalidateSize(false);
      }, 10);
    } else if (key == 4) {
      setTimeout(() => {
        this.map4Ref.current.invalidateSize(false);
      }, 10);
    } else if (key == 5) {
      setTimeout(() => {
        this.map5Ref.current.invalidateSize(false);
      }, 10);
    } else {
      setTimeout(() => {
        this.map6Ref.current.invalidateSize(false);
      }, 10);
    }
  }

  calculateMarkerPos(group_traj) {
    const pos = [
      (group_traj[0][0][0] + group_traj[group_traj.length - 1][0][0]) / 2,
      (group_traj[0][0][1] + group_traj[group_traj.length - 1][0][1]) / 2,
    ];
    return pos;
  }

  render() {
    const startPosition = [
      this.allTraj1[0][0][0] + 0.1,
      this.allTraj1[0][0][1] + 0.1,
    ];
    const blackOptions = { color: "#3483eb" };
    const group1Trajectories = readGroupTrajData("grp0");
    const marker1Pos = this.calculateMarkerPos(group1Trajectories);
    const group2Trajectories = readGroupTrajData("grp8");
    const marker2Pos = this.calculateMarkerPos(group2Trajectories);
    const group3Trajectories = readGroupTrajData("grp1");
    const marker3Pos = this.calculateMarkerPos(group3Trajectories);
    const group4Trajectories = readGroupTrajData("grp6");
    const marker4Pos = this.calculateMarkerPos(group4Trajectories);
    const group5Trajectories = readGroupTrajData("grp2");
    const marker5Pos = this.calculateMarkerPos(group5Trajectories);
    const group6Trajectories = readGroupTrajData("grp3");
    const marker6Pos = this.calculateMarkerPos(group6Trajectories);

    const group1Option = { color: "black" };

    const LeafIcon = L.Icon.extend({
      options: {},
    });

    return (
      <Tabs
        defaultActiveKey={this.state.key}
        id="uncontrolled-tab-example"
        className="mb-3"
        onSelect={this.onSelect.bind(this)}
      >
        <Tab eventKey="1" title="cluster 1">
          <div id="mapdiv1" ref={this.mapDiv1Ref}>
            <MapContainer
              id="map1"
              ref={this.map1Ref}
              center={startPosition}
              zoom={10}
              scrollWheelZoom={false}
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <Polyline pathOptions={blackOptions} positions={this.allTraj1} />
              <Polyline
                pathOptions={group1Option}
                positions={group1Trajectories}
              />
              <Marker
                position={marker1Pos}
                icon={
                  new LeafIcon({
                    iconUrl:
                      "https://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|abcdef&chf=a,s,ee00FFFF",
                    iconSize: [20, 32],
                    iconAnchor: [12, 41],
                  })
                }
              >
                <Popup maxWidth="600px" maxHeight="auto">
                  <PatternDetails
                    groupTrajs={group1Trajectories}
                  ></PatternDetails>
                </Popup>
              </Marker>
            </MapContainer>
          </div>
        </Tab>
        <Tab eventKey="2" title="cluster 2">
          <div id="mapdiv2" ref={this.mapDiv2Ref}>
            <MapContainer
              id="map2"
              ref={this.map2Ref}
              center={startPosition}
              zoom={10}
              scrollWheelZoom={false}
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <Polyline pathOptions={blackOptions} positions={this.allTraj1} />
              <Polyline
                pathOptions={group1Option}
                positions={group2Trajectories}
              />
              <Marker
                position={marker2Pos}
                icon={
                  new LeafIcon({
                    iconUrl:
                      "https://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|abcdef&chf=a,s,ee00FFFF",
                    iconSize: [20, 32],
                    iconAnchor: [12, 41],
                  })
                }
              >
                <Popup maxWidth="600px" maxHeight="auto">
                  <PatternDetails
                    groupTrajs={group2Trajectories}
                  ></PatternDetails>
                </Popup>
              </Marker>
            </MapContainer>
          </div>
        </Tab>
        <Tab eventKey="3" title="cluster 3">
          <div id="mapdiv3" ref={this.mapDiv3Ref}>
            <MapContainer
              id="map3"
              ref={this.map3Ref}
              center={startPosition}
              zoom={10}
              scrollWheelZoom={false}
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <Polyline pathOptions={blackOptions} positions={this.allTraj1} />
              <Polyline
                pathOptions={group1Option}
                positions={group3Trajectories}
              />
              <Marker
                position={marker3Pos}
                icon={
                  new LeafIcon({
                    iconUrl:
                      "https://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|abcdef&chf=a,s,ee00FFFF",
                    iconSize: [20, 32],
                  })
                }
              >
                <Popup maxWidth="600px" maxHeight="auto">
                  <PatternDetails
                    groupTrajs={group3Trajectories}
                  ></PatternDetails>
                </Popup>
              </Marker>
            </MapContainer>
          </div>
        </Tab>
        <Tab eventKey="4" title="cluster 4">
          <div id="mapdiv4" ref={this.mapDiv4Ref}>
            <MapContainer
              id="map4"
              ref={this.map4Ref}
              center={startPosition}
              zoom={10}
              scrollWheelZoom={false}
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <Polyline pathOptions={blackOptions} positions={this.allTraj1} />
              <Polyline
                pathOptions={group1Option}
                positions={group4Trajectories}
              />
              <Marker
                position={marker4Pos}
                icon={
                  new LeafIcon({
                    iconUrl:
                      "https://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|abcdef&chf=a,s,ee00FFFF",
                    iconSize: [20, 32],
                  })
                }
              >
                <Popup maxWidth="600px" maxHeight="auto">
                  <PatternDetails
                    groupTrajs={group4Trajectories}
                  ></PatternDetails>
                </Popup>
              </Marker>
            </MapContainer>
          </div>
        </Tab>
        <Tab eventKey="5" title="cluster 5">
          <div id="mapdiv5" ref={this.mapDiv5Ref}>
            <MapContainer
              id="map5"
              ref={this.map5Ref}
              center={startPosition}
              zoom={10}
              scrollWheelZoom={false}
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <Polyline pathOptions={blackOptions} positions={this.allTraj1} />
              <Polyline
                pathOptions={group1Option}
                positions={group5Trajectories}
              />
              <Marker
                position={marker5Pos}
                icon={
                  new LeafIcon({
                    iconUrl:
                      "https://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|abcdef&chf=a,s,ee00FFFF",
                    iconSize: [20, 32],
                  })
                }
              >
                <Popup maxWidth="600px" maxHeight="auto">
                  <PatternDetails
                    groupTrajs={group5Trajectories}
                  ></PatternDetails>
                </Popup>
              </Marker>
            </MapContainer>
          </div>
        </Tab>
        <Tab eventKey="6" title="cluster 6">
          <div id="mapdiv6" ref={this.mapDiv6Ref}>
            <MapContainer
              id="map6"
              ref={this.map6Ref}
              center={startPosition}
              zoom={10}
              scrollWheelZoom={false}
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <Polyline pathOptions={blackOptions} positions={this.allTraj1} />
              <Polyline
                pathOptions={group1Option}
                positions={group6Trajectories}
              />
              <Marker
                position={marker6Pos}
                icon={
                  new LeafIcon({
                    iconUrl:
                      "https://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|abcdef&chf=a,s,ee00FFFF",
                    iconSize: [20, 32],
                  })
                }
              >
                <Popup maxWidth="600px" maxHeight="auto">
                  <PatternDetails
                    groupTrajs={group6Trajectories}
                  ></PatternDetails>
                </Popup>
              </Marker>
            </MapContainer>
          </div>
        </Tab>
      </Tabs>
    );
  }
}

export default MapTab;
