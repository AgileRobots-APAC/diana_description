#!/bin/bash

args=$*
shift $#

cd /workspaces
colcon build --packages-select diana_description > /dev/null
source install/setup.bash

ros2 launch diana_description visualize_diana.launch.py ${args}