#include <ros/ros.h>
#include "nav_main.h"

int main(int argc, char** argv) {
  ros::init(argc, argv, "navigation_node");

  ros::NodeHandlePtr nh(new ros::NodeHandle("~"));
  navigation::NavigationNode navigation_node(nh);

  navigation_node.Spin();
}