import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import reportWebVitals from "./reportWebVitals";
import MapTab from "./components/mapTab";
import "bootstrap/dist/css/bootstrap.min.css";
import "leaflet/dist/leaflet.css";
import getAllTrajData from "./components/readAllTrajData";

const root = ReactDOM.createRoot(document.getElementById("root"));
const traj = getAllTrajData();
root.render(
  <React.StrictMode>
    <h1 id="pageTitle"> Trajectory Clustering Result Demo </h1>
    <br></br>
    <MapTab allTraj1={traj} />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
