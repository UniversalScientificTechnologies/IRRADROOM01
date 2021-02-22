# IRRADROOM01


## Řidící počítač

* Odroid C2
* Ubuntu 20.04.4 minimal ()
* ROS 2 Foxy; Debain binaries (https://index.ros.org/doc/ros2/Installation/Foxy/Linux-Install-Debians/)
  * ros-foxy-ros-base
* `sudo apt install git htop nano mc python3-colcon-common-extensions   `
* `pip3 install serial tornado pymongo  `
* Pymlab, i2c-tools (fork)
* Create ROS2 WS
* Setup enviroment
* `export ROS_DOMAIN_ID=35`
* Install `rosbridge_server` (from git; branch `ros2`)


### ROS 2
Jako základní framework je použit ROS2. Domain ID je nastaveno na 35 v `~/.bashrc`.
