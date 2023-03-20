function readGroupTrajData(groupName) {
  const traj = require("./json_data/traj_" + groupName + ".json");
  return traj;
}

export default readGroupTrajData;
