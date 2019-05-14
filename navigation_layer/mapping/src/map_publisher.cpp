#include <ros/ros.h>
#include <grid_map_ros/grid_map_ros.hpp>
#include <grid_map_msgs/GridMap.h>
#include <cmath>
#include "yaml-cpp/yaml.h"
#include<string>

using namespace grid_map;
std::string map_yaml_location = "/home/ayush/Projects/anahita_ws/src/Anahita/navigation_layer/mapping/config/transdec.yaml";

void loadMapFromYAML(GridMap &map)
{
    YAML::Node yaml_map = YAML::LoadFile(map_yaml_location);
    ROS_INFO("Loaded: %d", yaml_map["map"]["gate"]["x"].as<int>());
    Position gate_position(yaml_map["map"]["gate"]["x"].as<int>(),yaml_map["map"]["gate"]["y"].as<int>());
    Position torpedo_position(yaml_map["map"]["torpedo"]["x"].as<int>(),yaml_map["map"]["torpedo"]["y"].as<int>());
    map.atPosition("occupancy", gate_position) = 1;
    map.atPosition("occupancy", torpedo_position) = 1;
    ROS_INFO("Loaded map file");
}

int main(int argc, char** argv)
{
  // Initialize node and publisher.
  ros::init(argc, argv, "map_publisher_node");
  ros::NodeHandle nh("~");
  ros::Publisher publisher = nh.advertise<grid_map_msgs::GridMap>("grid_map", 1, true);

  // Create grid map.
  GridMap map({"elevation", "occupancy"});
  map.setFrameId("map");
  map.setGeometry(Length(30,30), 1);
  ROS_INFO("Created map with size %f x %f m (%i x %i cells).",
    map.getLength().x(), map.getLength().y(),
    map.getSize()(0), map.getSize()(1));

  Position origin_position;
  Index origin_index(0);
  getPositionFromIndex(origin_position, origin_index, map.getLength(), map.getPosition(), map.getResolution(), Size(1,1));
  map.setPosition(origin_position);
        
  for (GridMapIterator it(map); !it.isPastEnd(); ++it) {
      Position position;
      map.getPosition(*it, position);
      map.at("elevation", *it) = 0;
      map.at("occupancy", *it) = 0;
  }

  loadMapFromYAML(map);
  // Work with grid map in a loop.
  ros::Rate rate(30.0);
  while (nh.ok()) {

    // Add data to grid map.
    ros::Time time = ros::Time::now();
    // Publish grid map.
    map.setTimestamp(time.toNSec());
    grid_map_msgs::GridMap message;
    GridMapRosConverter::toMessage(map, message);
    publisher.publish(message);
    ROS_INFO_THROTTLE(1.0, "Grid map (timestamp %f) published.", message.info.header.stamp.toSec());

    // Wait for next cycle.
    rate.sleep();
  }

  return 0;
}

