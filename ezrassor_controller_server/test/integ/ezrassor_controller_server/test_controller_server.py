"""Integration tests for the controller_server."""
import ament_index_python.packages as ament
import concurrent.futures
import geometry_msgs.msg
import launch
import launch.launch_description_sources as description_sources
import launch_testing
import rclpy
import requests
import std_msgs.msg
import time
import unittest


NODE = "test_controller_server"
PACKAGE = "ezrassor_controller_server"
TEST_ENDPOINT = "http://127.0.0.1:5000/"
CONTROLLER_SERVER_LAUNCH_FILE_FORMAT = "{0}/launch/controller_server.py"
# WHEEL_ACTIONS_TOPIC = "wheel_actions"
# FRONT_ARM_ACTIONS_TOPIC = "front_arm_actions"
# BACK_ARM_ACTIONS_TOPIC = "back_arm_actions"
# FRONT_DRUM_ACTIONS_TOPIC = "front_drum_actions"
# BACK_DRUM_ACTIONS_TOPIC = "back_drum_actions"
# ROUTINE_ACTIONS_TOPIC = "routine_actions"
JOINT_1_ACTION_TOPIC = "/ezrassor/joint_1_action"
JOINT_2_ACTION_TOPIC = "/ezrassor/joint_2_action"
JOINT_3_ACTION_TOPIC = "/ezrassor/joint_3_action"
JOINT_4_ACTION_TOPIC = "/ezrassor/joint_4_action"
JOINT_5_ACTION_TOPIC = "/ezrassor/joint_5_action"
CLAW_ACTION_TOPIC = "/ezrassor/claw_action"
PARTIAL_AUTONOMY_TOPIC = "/ezrassor/partial_autonomy"

QUEUE_SIZE = 10
SHORT_TIMEOUT = 0.2
LONG_TIMEOUT = 2.0


# DRIVE_FORWARD_REQUEST = {"wheel_action": {"linear_x": 1.0, "angular_z": 0.0}}
# TURN_LEFT_REQUEST = {"wheel_action": {"linear_x": 0.0, "angular_z": 1.0}}
# DRIVE_BACKWARD_REQUEST = {"wheel_action": {"linear_x": -1.0, "angular_z": 0.0}}
# TURN_RIGHT_REQUEST = {"wheel_action": {"linear_x": 0.0, "angular_z": -1.0}}
# STOP_DRIVING_REQUEST = {"wheel_action": {"linear_x": 0.0, "angular_z": 0.0}}
# RAISE_FRONT_ARM_REQUEST = {"front_arm_action": "RAISE"}
# LOWER_FRONT_ARM_REQUEST = {"front_arm_action": "LOWER"}
# STOP_FRONT_ARM_REQUEST = {"front_arm_action": "STOP"}
# RAISE_BACK_ARM_REQUEST = {"back_arm_action": "RAISE"}
# LOWER_BACK_ARM_REQUEST = {"back_arm_action": "LOWER"}
# STOP_BACK_ARM_REQUEST = {"back_arm_action": "STOP"}
# DIG_FRONT_DRUM_REQUEST = {"front_drum_action": "DIG"}
# DUMP_FRONT_DRUM_REQUEST = {"front_drum_action": "DUMP"}
# STOP_FRONT_DRUM_REQUEST = {"front_drum_action": "STOP"}
# DIG_BACK_DRUM_REQUEST = {"back_drum_action": "DIG"}
# DUMP_BACK_DRUM_REQUEST = {"back_drum_action": "DUMP"}
# STOP_BACK_DRUM_REQUEST = {"back_drum_action": "STOP"}
# EXECUTE_AUTO_DRIVE_ROUTINE_REQUEST = {"routine_action": "AUTO_DRIVE"}
# EXECUTE_AUTO_DIG_ROUTINE_REQUEST = {"routine_action": "AUTO_DIG"}
# EXECUTE_AUTO_DUMP_ROUTINE_REQUEST = {"routine_action": "AUTO_DUMP"}
# EXECUTE_AUTO_DOCK_ROUTINE_REQUEST = {"routine_action": "AUTO_DOCK"}
# EXECUTE_FULL_AUTONOMY_ROUTINE_REQUEST = {"routine_action": "FULL_AUTONOMY"}
# STOP_ROUTINE_REQUEST = {"routine_action": "STOP"}

JOINT_1_ROTATE_LEFT_REQUEST = {"joint_1_action": "ROTATELEFT"}
JOINT_1_ROTATE_RIGHT_REQUEST = {"joint_1_action": "ROTATERIGHT"}
JOINT_1_ROTATE_UP_REQUEST = {"joint_1_action": "ROTATEUP"}
JOINT_1_ROTATE_DOWN_REQUEST = {"joint_1_action": "ROTATEDOWN"}
JOINT_1_STOP_REQUEST = {"joint_1_action": "STOP"}

JOINT_2_ROTATE_LEFT_REQUEST = {"joint_2_action": "ROTATELEFT"}
JOINT_2_ROTATE_RIGHT_REQUEST = {"joint_2_action": "ROTATERIGHT"}
JOINT_2_ROTATE_UP_REQUEST = {"joint_2_action": "ROTATEUP"}
JOINT_2_ROTATE_DOWN_REQUEST = {"joint_2_action": "ROTATEDOWN"}
JOINT_2_STOP_REQUEST = {"joint_2_action": "STOP"}

JOINT_3_ROTATE_LEFT_REQUEST = {"joint_3_action": "ROTATELEFT"}
JOINT_3_ROTATE_RIGHT_REQUEST = {"joint_3_action": "ROTATERIGHT"}
JOINT_3_ROTATE_UP_REQUEST = {"joint_3_action": "ROTATEUP"}
JOINT_3_ROTATE_DOWN_REQUEST = {"joint_3_action": "ROTATEDOWN"}
JOINT_3_STOP_REQUEST = {"joint_3_action": "STOP"}

JOINT_4_ROTATE_LEFT_REQUEST = {"joint_4_action": "ROTATELEFT"}
JOINT_4_ROTATE_RIGHT_REQUEST = {"joint_4_action": "ROTATERIGHT"}
JOINT_4_ROTATE_UP_REQUEST = {"joint_4_action": "ROTATEUP"}
JOINT_4_ROTATE_DOWN_REQUEST = {"joint_4_action": "ROTATEDOWN"}
JOINT_4_STOP_REQUEST = {"joint_4_action": "STOP"}

JOINT_5_ROTATE_LEFT_REQUEST = {"joint_5_action": "ROTATELEFT"}
JOINT_5_ROTATE_RIGHT_REQUEST = {"joint_5_action": "ROTATERIGHT"}
JOINT_5_ROTATE_UP_REQUEST = {"joint_5_action": "ROTATEUP"}
JOINT_5_ROTATE_DOWN_REQUEST = {"joint_5_action": "ROTATEDOWN"}
JOINT_5_STOP_REQUEST = {"joint_5_action": "STOP"}

CLAW_OPEN_REQUEST = {"claw_action": "OPEN"}
CLAW_CLOSE_REQUEST = {"claw_action": "CLOSE"}

AUTONOMY_HOME_REQUEST = {"partial_autonomy": "HOME"}
AUTONOMY_PLACE_REQUEST = {"partial_autonomy": "PLACE"}
AUTONOMY_PICKUP_REQUEST = {"partial_autonomy": "PICKUP"}



def generate_test_description():
    """Create a test description with the controller_server launch file."""
    controller_server_launch_file = CONTROLLER_SERVER_LAUNCH_FILE_FORMAT.format(
        ament.get_package_share_directory(PACKAGE),
    )

    return launch.LaunchDescription(
        [
            launch.actions.IncludeLaunchDescription(
                description_sources.PythonLaunchDescriptionSource(
                    controller_server_launch_file,
                ),
            ),
            launch_testing.actions.ReadyToTest(),
        ]
    )


class ControllerServerIntegrationTests(unittest.TestCase):
    """A suite of integration tests for the controller_server."""

    @classmethod
    def setUpClass(*arguments):
        """Initialize ROS before testing begins.

        This method name is required by unittest.
        """
        rclpy.init()

    def setUp(self):
        """Initialize testing infrastructure before each test.

        This method name is required by unittest.
        """
        self._node = rclpy.create_node(NODE)

        # Save the output of each controller_server topic to a list.
        # self._wheel_actions = []
        # self._node.create_subscription(
        #     geometry_msgs.msg.Twist,
        #     WHEEL_ACTIONS_TOPIC,
        #     lambda message: self._wheel_actions.append(
        #         (message.linear.x, message.angular.z),
        #     ),
        #     QUEUE_SIZE,
        # )
        # self._front_arm_actions = []
        # self._node.create_subscription(
        #     std_msgs.msg.Float32,
        #     FRONT_ARM_ACTIONS_TOPIC,
        #     lambda message: self._front_arm_actions.append(message.data),
        #     QUEUE_SIZE,
        # )
        # self._back_arm_actions = []
        # self._node.create_subscription(
        #     std_msgs.msg.Float32,
        #     BACK_ARM_ACTIONS_TOPIC,
        #     lambda message: self._back_arm_actions.append(message.data),
        #     QUEUE_SIZE,
        # )
        # self._front_drum_actions = []
        # self._node.create_subscription(
        #     std_msgs.msg.Float32,
        #     FRONT_DRUM_ACTIONS_TOPIC,
        #     lambda message: self._front_drum_actions.append(message.data),
        #     QUEUE_SIZE,
        # )
        # self._back_drum_actions = []
        # self._node.create_subscription(
        #     std_msgs.msg.Float32,
        #     BACK_DRUM_ACTIONS_TOPIC,
        #     lambda message: self._back_drum_actions.append(message.data),
        #     QUEUE_SIZE,
        # )
        # self._routine_actions = []
        # self._node.create_subscription(
        #     std_msgs.msg.Int8,
        #     ROUTINE_ACTIONS_TOPIC,
        #     lambda message: self._routine_actions.append(message.data),
        #     QUEUE_SIZE,
        # )

        self._joint_1_actions = []
        self._node.create_subscription(
            std_msgs.msg.Float64,
            JOINT_1_ACTION_TOPIC,
            lambda message: self._joint_1_actions.append(message.data),
            QUEUE_SIZE,
        )
        self._joint_2_actions = []
        self._node.create_subscription(
            std_msgs.msg.Float64,
            JOINT_2_ACTION_TOPIC,
            lambda message: self._joint_2_actions.append(message.data),
            QUEUE_SIZE,
        )
        self._joint_3_actions = []
        self._node.create_subscription(
            std_msgs.msg.Float64,
            JOINT_3_ACTION_TOPIC,
            lambda message: self._joint_3_actions.append(message.data),
            QUEUE_SIZE,
        )
        self._joint_4_actions = []
        self._node.create_subscription(
            std_msgs.msg.Float64,
            JOINT_4_ACTION_TOPIC,
            lambda message: self._joint_4_actions.append(message.data),
            QUEUE_SIZE,
        )
        self._joint_5_actions = []
        self._node.create_subscription(
            std_msgs.msg.Float64,
            JOINT_5_ACTION_TOPIC,
            lambda message: self._joint_5_actions.append(message.data),
            QUEUE_SIZE,
        )
        self._claw_actions = []
        self._node.create_subscription(
            std_msgs.msg.Float64,
            CLAW_ACTION_TOPIC,
            lambda message: self._claw_actions.append(message.data),
            QUEUE_SIZE,
        )
        self._autonomy_actions = []
        self._node.create_subscription(
            std_msgs.msg.Float64,
            PARTIAL_AUTONOMY_TOPIC,
            lambda message: self._autonomy_actions.append(message.data),
            QUEUE_SIZE,
        )

        # Sleep for some time to give ROS a moment to warm up.
        time.sleep(LONG_TIMEOUT)

    def tearDown(self):
        """Destroy testing infrastructure after each test.

        This method name is required by unittest.
        """
        self._node.destroy_node()

    @classmethod
    def tearDownClass(*arguments):
        """Shut down ROS after testing is complete.

        This method name is required by unittest.
        """
        rclpy.shutdown()

    def _post(self, request):
        """Post a pre-defined request to the controller_server endpoint."""
        response = requests.post(TEST_ENDPOINT, json=request)
        self.assertEqual(response.status_code, requests.codes.ok)
        time.sleep(SHORT_TIMEOUT)

    def _spin_for_subscribers(self):
        """Spin the node for a brief period of time.

        This is necessary to give the testing subscribers enough spins to
        collect all required outputs.
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(time.sleep, LONG_TIMEOUT)
            rclpy.spin_until_future_complete(
                self._node,
                future,
                timeout_sec=LONG_TIMEOUT,
            )

    # def _verify_wheel_actions(self, expected_actions):
    #     """Verify the received wheel actions are as expected."""
    #     self.assertEqual(self._wheel_actions, expected_actions)

    # def _verify_front_arm_actions(self, expected_actions):
    #     """Verify the received front arm actions are as expected."""
    #     self.assertEqual(self._front_arm_actions, expected_actions)

    # def _verify_back_arm_actions(self, expected_actions):
    #     """Verify the received back arm actions are as expected."""
    #     self.assertEqual(self._back_arm_actions, expected_actions)

    # def _verify_front_drum_actions(self, expected_actions):
    #     """Verify the received front drum actions are as expected."""
    #     self.assertEqual(self._front_drum_actions, expected_actions)

    # def _verify_back_drum_actions(self, expected_actions):
    #     """Verify the received back drum actions are as expected."""
    #     self.assertEqual(self._back_drum_actions, expected_actions)

    # def _verify_routine_actions(self, expected_actions):
    #     """Verify the received routine actions are as expected."""
    #     self.assertEqual(self._routine_actions, expected_actions)

    def _verify_joint_1_actions(self, expected_actions):
        """Verify the received joint 1 actions are as expected."""
        self.assertEqual(self._joint_1_actions, expected_actions)

    def _verify_joint_2_actions(self, expected_actions):
        """Verify the received joint 2 actions are as expected."""
        self.assertEqual(self._joint_2_actions, expected_actions)

    def _verify_joint_3_actions(self, expected_actions):
        """Verify the received joint 3 actions are as expected."""
        self.assertEqual(self._joint_3_actions, expected_actions)

    def _verify_joint_4_actions(self, expected_actions):
        """Verify the received joint 4 actions are as expected."""
        self.assertEqual(self._joint_4_actions, expected_actions)

    def _verify_joint_5_actions(self, expected_actions):
        """Verify the received joint 5 actions are as expected."""
        self.assertEqual(self._joint_5_actions, expected_actions)

    def _verify_claw_actions(self, expected_actions):
        """Verify the received claw actions are as expected."""
        self.assertEqual(self._claw_actions, expected_actions)

    def _verify_autonomy_actions(self, expected_actions):
        """Verify the received autonomyactions are as expected."""
        self.assertEqual(self._autonomy_actions, expected_actions)

    # def test_controller_server_produces_accurate_wheel_actions(self):
    #     """Should produce wheel actions from wheel-related requests."""
    #     self._post(DRIVE_FORWARD_REQUEST)
    #     self._post(TURN_LEFT_REQUEST)
    #     self._post(DRIVE_BACKWARD_REQUEST)
    #     self._post(TURN_RIGHT_REQUEST)
    #     self._post(STOP_DRIVING_REQUEST)

    #     self._spin_for_subscribers()

    #     self._verify_wheel_actions(
    #         [(1.0, 0.0), (0.0, 1.0), (-1.0, 0.0), (0.0, -1.0), (0.0, 0.0)],
    #     )
    #     self._verify_front_arm_actions([])
    #     self._verify_back_arm_actions([])
    #     self._verify_front_drum_actions([])
    #     self._verify_back_drum_actions([])
    #     self._verify_routine_actions([])

    # def test_controller_server_produces_accurate_arm_actions(self):
    #     """Should produce arm actions from arm-related requests."""
    #     self._post(RAISE_FRONT_ARM_REQUEST)
    #     self._post(LOWER_FRONT_ARM_REQUEST)
    #     self._post(STOP_FRONT_ARM_REQUEST)
    #     self._post(RAISE_BACK_ARM_REQUEST)
    #     self._post(LOWER_BACK_ARM_REQUEST)
    #     self._post(STOP_BACK_ARM_REQUEST)

    #     self._spin_for_subscribers()

    #     self._verify_wheel_actions([])
    #     self._verify_front_arm_actions([1.0, -1.0, 0.0])
    #     self._verify_back_arm_actions([1.0, -1.0, 0.0])
    #     self._verify_front_drum_actions([])
    #     self._verify_back_drum_actions([])
    #     self._verify_routine_actions([])

    # def test_controller_server_produces_accurate_drum_actions(self):
    #     """Should produce drum actions from drum-related requests."""
    #     self._post(DIG_FRONT_DRUM_REQUEST)
    #     self._post(DUMP_FRONT_DRUM_REQUEST)
    #     self._post(STOP_FRONT_DRUM_REQUEST)
    #     self._post(DIG_BACK_DRUM_REQUEST)
    #     self._post(DUMP_BACK_DRUM_REQUEST)
    #     self._post(STOP_BACK_DRUM_REQUEST)

    #     self._spin_for_subscribers()

    #     self._verify_wheel_actions([])
    #     self._verify_front_arm_actions([])
    #     self._verify_back_arm_actions([])
    #     self._verify_front_drum_actions([1.0, -1.0, 0.0])
    #     self._verify_back_drum_actions([1.0, -1.0, 0.0])
    #     self._verify_routine_actions([])

    # def test_controller_server_produces_accurate_routine_actions(self):
    #     """Should produce routine actions from routine-related requests."""
    #     self._post(EXECUTE_AUTO_DRIVE_ROUTINE_REQUEST)
    #     self._post(EXECUTE_AUTO_DIG_ROUTINE_REQUEST)
    #     self._post(EXECUTE_AUTO_DUMP_ROUTINE_REQUEST)
    #     self._post(EXECUTE_AUTO_DOCK_ROUTINE_REQUEST)
    #     self._post(EXECUTE_FULL_AUTONOMY_ROUTINE_REQUEST)
    #     self._post(STOP_ROUTINE_REQUEST)

    #     self._spin_for_subscribers()

    #     self._verify_wheel_actions([])
    #     self._verify_front_arm_actions([])
    #     self._verify_back_arm_actions([])
    #     self._verify_front_drum_actions([])
    #     self._verify_back_drum_actions([])
    #     self._verify_routine_actions(
    #         [
    #             0b000001,
    #             0b000010,
    #             0b000100,
    #             0b001000,
    #             0b010000,
    #             0b100000,
    #         ],
    #     )


    def test_controller_server_produces_accurate_joint_1_actions(self):
        """Should produce joint 1 actions from joint1-related requests."""
        self._post(JOINT_1_ROTATE_LEFT_REQUEST)
        self._post(JOINT_1_ROTATE_RIGHT_REQUEST)
        self._post(JOINT_1_ROTATE_UP_REQUEST)
        self._post(JOINT_1_ROTATE_DOWN_REQUEST)
        self._post(JOINT_1_STOP_REQUEST)

        self._spin_for_subscribers()

        self._verify_joint_1_actions([0.2, -0.2, -0.2, 0.2, 0.0])
        self._verify_joint_2_actions([])
        self._verify_joint_3_actions([])
        self._verify_joint_4_actions([])
        self._verify_joint_5_actions([])
        self._verify_claw_actions([])
        self._verify_autonomy_actions([])

    def test_controller_server_produces_accurate_joint_2_actions(self):
        """Should produce joint 2 actions from joint2-related requests."""
        self._post(JOINT_2_ROTATE_LEFT_REQUEST)
        self._post(JOINT_2_ROTATE_RIGHT_REQUEST)
        self._post(JOINT_2_ROTATE_UP_REQUEST)
        self._post(JOINT_2_ROTATE_DOWN_REQUEST)
        self._post(JOINT_2_STOP_REQUEST)

        self._spin_for_subscribers()

        self._verify_joint_1_actions([])
        self._verify_joint_2_actions([0.2, -0.2, -0.2, 0.2, 0.0])
        self._verify_joint_3_actions([])
        self._verify_joint_4_actions([])
        self._verify_joint_5_actions([])
        self._verify_claw_actions([])
        self._verify_autonomy_actions([])

    def test_controller_server_produces_accurate_joint_3_actions(self):
        """Should produce joint 3 actions from joint3-related requests."""
        self._post(JOINT_3_ROTATE_LEFT_REQUEST)
        self._post(JOINT_3_ROTATE_RIGHT_REQUEST)
        self._post(JOINT_3_ROTATE_UP_REQUEST)
        self._post(JOINT_3_ROTATE_DOWN_REQUEST)
        self._post(JOINT_3_STOP_REQUEST)

        self._spin_for_subscribers()

        self._verify_joint_1_actions([])
        self._verify_joint_2_actions([])
        self._verify_joint_3_actions([0.2, -0.2, -0.2, 0.2, 0.0])
        self._verify_joint_4_actions([])
        self._verify_joint_5_actions([])
        self._verify_claw_actions([])
        self._verify_autonomy_actions([])

    def test_controller_server_produces_accurate_joint_4_actions(self):
        """Should produce joint 4 actions from joint4-related requests."""
        self._post(JOINT_4_ROTATE_LEFT_REQUEST)
        self._post(JOINT_4_ROTATE_RIGHT_REQUEST)
        self._post(JOINT_4_ROTATE_UP_REQUEST)
        self._post(JOINT_4_ROTATE_DOWN_REQUEST)
        self._post(JOINT_4_STOP_REQUEST)

        self._spin_for_subscribers()

        self._verify_joint_1_actions([])
        self._verify_joint_2_actions([])
        self._verify_joint_3_actions([])
        self._verify_joint_4_actions([0.2, -0.2, -0.2, 0.2, 0.0])
        self._verify_joint_5_actions([])
        self._verify_claw_actions([])
        self._verify_autonomy_actions([])

    def test_controller_server_produces_accurate_joint_5_actions(self):
        """Should produce joint 5 actions from joint5-related requests."""
        self._post(JOINT_5_ROTATE_LEFT_REQUEST)
        self._post(JOINT_5_ROTATE_RIGHT_REQUEST)
        self._post(JOINT_5_ROTATE_UP_REQUEST)
        self._post(JOINT_5_ROTATE_DOWN_REQUEST)
        self._post(JOINT_5_STOP_REQUEST)

        self._spin_for_subscribers()

        self._verify_joint_1_actions([])
        self._verify_joint_2_actions([])
        self._verify_joint_3_actions([])
        self._verify_joint_4_actions([])
        self._verify_joint_5_actions([0.2, -0.2, -0.2, 0.2, 0.0])
        self._verify_claw_actions([])
        self._verify_autonomy_actions([])

    def test_controller_server_produces_accurate_claw_actions(self):
        """Should produce claw actions from claw-related requests."""
        self._post(CLAW_OPEN_REQUEST)
        self._post(CLAW_CLOSE_REQUEST)

        self._spin_for_subscribers()

        self._verify_joint_1_actions([])
        self._verify_joint_2_actions([])
        self._verify_joint_3_actions([])
        self._verify_joint_4_actions([])
        self._verify_joint_5_actions([])
        self._verify_claw_actions([-6.0, 6.0])
        self._verify_autonomy_actions([])

    def test_controller_server_produces_accurate_autonomy_actions(self):
        """Should produce autonomy actions from autonomy-related requests."""
        self._post(AUTONOMY_HOME_REQUEST)
        self._post(AUTONOMY_PLACE_REQUEST)
        self._post(AUTONOMY_PICKUP_REQUEST)

        self._spin_for_subscribers()

        self._verify_joint_1_actions([])
        self._verify_joint_2_actions([])
        self._verify_joint_3_actions([])
        self._verify_joint_4_actions([])
        self._verify_joint_5_actions([])
        self._verify_claw_actions([])
        self._verify_autonomy_actions([1.0, 2.0, 3.0])


if __name__ == '__main__':
    unittest.main()