import React, { Component } from "react";
import "leaflet/dist/leaflet.css";
import SingleTrajMap from "./singleTrajMap";
import { popupWindow } from "./popupWindowStyle";
import { popupContent } from "./popupStylesGrp1";

class PatternDetails extends Component {
  constructor(props) {
    super(props);
    this.groupTrajs = this.props.groupTrajs;
  }

  getTrajMapArrays() {
    const trajNo = this.groupTrajs.length;
    let maps = [];
    for (let i = 0; i < trajNo; i++) {
      maps.push(
        <SingleTrajMap
          key={"group1traj" + i}
          traj={this.groupTrajs[i]}
        ></SingleTrajMap>
      );
    }
    return maps;
  }

  render() {
    return (
      <div style={popupWindow}>
        <h5>Trajectory Group Members</h5>
        <br></br>
        <div style={popupContent}>{this.getTrajMapArrays()}</div>
      </div>
    );
  }
}

export default PatternDetails;
