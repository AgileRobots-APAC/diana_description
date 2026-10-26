#!/bin/bash

args=$*
shift $#

source /ros_entrypoint.sh

cd /workspaces
colcon build --packages-select diana_description > /dev/null
source install/setup.bash

cd src/diana_description

python3 scripts/create_urdf.py $args