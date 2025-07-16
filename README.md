# Multi-Map Navigation Implementation using ANSCER A100 AMR

This repo shows the multi-map multi-room autonomous navigation implementation using wormholes for AR100 robot by Anscer robotics in a custom environment 

## Prerequisites

* [Ubuntu version : 20.04](https://ubuntu.com/download/desktop)
* [ROS version : Noetic](http://wiki.ros.org/noetic/Installation/Ubuntu)
* Editor used : [Vscode](https://code.visualstudio.com/download)
* Compiler  : catkin

## Building, Installation Setup & Usage
* Follow the the instructions [here](https://github.com/anscer/AR100) and install Anscer Robotics AR100 ROS package. 

* Replace the World folder with the one given in this repo (custom world with 3 room setup).

* Replace the map.pgm and map.yaml files in the map folder inside anscer_navigation folder with the map1.pgm and map1.yaml file in this repo and rename it to the default names.

* After this, you will have a working AR100 simulation for working with this repo.

#### 1. Clone the Package into Your Catkin Workspace:

```sh
cd ~/catkin_ws/src
git clone https://github.com/jerinpeter/ar100-multimap-nav.git

```

#### 2. Build the Workspace

```sh
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

#### 3. Launch the navigation server:

```
roslaunch multi_map_nav navigation_server.launch
```

#### 4. Send a navigation goal: You can send a goal using an action client, or use a custom script like:

You can send navigation goals using the ROS action client or directly with rostopic:

- Using `rostopic`:

  ```bash
  rostopic pub /navigate_to_goal/goal multi_map_nav/NavigateToGoalActionGoal "header:
    seq: 0
    stamp:
      secs: 0
      nsecs: 0
    frame_id: ''
  goal_id:
    stamp:
      secs: 0
      nsecs: 0
    id: ''
  goal:
    target_x: -5.0
    target_y: -6.0
    target_map: 'map2'"
  ```
