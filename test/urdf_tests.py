# Copyright (c) 2026 Franka Robotics GmbH
# Copyright (c) 2026 Agile Robots SE (modifications: adapted for Diana robots)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from os import path
import xml.etree.ElementTree as ET

from ament_index_python.packages import get_package_share_directory
import pytest
import xacro

TEST_PARAMETERS = [
    pytest.param('diana3',  id='diana3'),
    pytest.param('diana7', id='diana7'),
    pytest.param('diana7g2', id='diana7g2'),
]


def get_diana_urdf_xacro(robot_type: str):
    return path.join(
        get_package_share_directory('diana_description'),
        'robots',
        robot_type,
        robot_type+'.urdf.xacro',
    )

@pytest.mark.parametrize('robot_type', TEST_PARAMETERS)
def test_diana_urdf_is_well_formed(robot_type: str):
    urdf = xacro.process_file(
        get_diana_urdf_xacro(robot_type), 
        mappings={'gazebo': 'false'}
    ).toxml()
    root = ET.fromstring(urdf)

    assert root.tag == 'robot', 'urdf must have topmost level robot tag'
    assert len(root) > 0, 'urdf cannot be empty'

@pytest.mark.parametrize('robot_type', TEST_PARAMETERS)
def test_diana_without_ee(robot_type: str):
    urdf = xacro.process_file(
        get_diana_urdf_xacro(robot_type),
        mappings={'ee_id': 'none'},
    ).toxml()
    root = ET.fromstring(urdf)

    assert root.find(f".//joint[@name='{robot_type}_finger_joint1']") is None
    assert root.find(f".//joint[@name='{robot_type}_finger_joint2']") is None

@pytest.mark.parametrize('robot_type', TEST_PARAMETERS)
def test_diana_has_main_joints(robot_type: str):
    urdf = xacro.process_file(
        get_diana_urdf_xacro(robot_type), 
        mappings={'gazebo': 'false'}
    ).toxml()
    root = ET.fromstring(urdf)

    for joint_index in range(1, 8):
        joint_name = f"{robot_type}_joint{joint_index}"
        assert root.find(f".//joint[@name='{joint_name}']") is not None, (
            f'diana urdf must contain {joint_name}'
        )
