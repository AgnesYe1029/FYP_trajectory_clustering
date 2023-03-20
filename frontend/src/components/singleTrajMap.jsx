import React, { Component, createRef } from "react";
import { MapContainer, TileLayer, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";

class SingleTrajMap extends Component {
  constructor(props) {
    super(props);
    this.mapRef = createRef();
    this.traj = this.props.traj;
  }

  componentDidMount() {
    setTimeout(() => {
      this.mapRef.current.invalidateSize(false);
    }, 50);
  }

  render() {
    console.log("inside singleTrajMap");
    const blackOptions = { color: "black" };
    const trajLen = this.traj.length;
    const centerPosition = [
      (this.traj[0][0] + this.traj[trajLen - 1][0]) / 2,
      (this.traj[0][1] + this.traj[trajLen - 1][1]) / 2,
    ];
    console.log("centerPosition", centerPosition);
    return (
      <div>
        <br></br>
        <MapContainer
          style={{ height: "400px", width: "400px" }}
          ref={this.mapRef}
          center={centerPosition}
          zoom={10}
          scrollWheelZoom={false}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <Polyline pathOptions={blackOptions} positions={this.traj} />
        </MapContainer>
        <br></br>
      </div>
    );
  }
}

export default SingleTrajMap;
