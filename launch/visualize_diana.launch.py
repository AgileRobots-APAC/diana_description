# Copyright (c) 2023 Franka Robotics GmbH
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

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchContext, LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node
import xacro


def robot_state_publisher_spawner(context: LaunchContext, robot_type):
    robot_type_str = context.perform_substitution(robot_type)

    diana_xacro_filepath = os.path.join(
        get_package_share_directory('diana_description'),
        'robots',
        robot_type_str,
        robot_type_str + '.urdf.xacro',
    )

   
    robot_description = xacro.process_file(
        diana_xacro_filepath,
        mappings={
            'hand': 'false',   
            'ee_id': 'none'  
        },
    ).toprettyxml(indent='  ')

    return [
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description}],
        )
    ]


def generate_launch_description():

    robot_type_parameter_name = 'robot_type'
    robot_type = LaunchConfiguration(robot_type_parameter_name)

    rviz_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        'rviz',
        'visualize_diana.rviz',
    )
    rviz_file = os.path.abspath(rviz_file)

    robot_state_publisher_spawner_opaque_function = OpaqueFunction(
        function=robot_state_publisher_spawner,
        args=[robot_type]
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                robot_type_parameter_name,
                default_value='diana3',
                description='Robot type (diana, etc.)',
            ),

            robot_state_publisher_spawner_opaque_function,

            Node(
                package='joint_state_publisher_gui',
                executable='joint_state_publisher_gui',
                name='joint_state_publisher_gui',
                parameters=[{'source_list':['manual_joint_states']}]
            ),

            Node(
                package='rviz2',
                executable='rviz2',
                name='rviz2',
                arguments=['--display-config', rviz_file],
            ),
        ]
    )
