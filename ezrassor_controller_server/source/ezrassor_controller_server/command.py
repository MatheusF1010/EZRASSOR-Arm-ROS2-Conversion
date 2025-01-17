"""Data structures that make up an EZRASSOR command."""
import enum
import ezrassor_controller_server as server

def create_command(request):
    """Create a command from a remote request.

    This function presumes that the request is valid.
    """

    # Set a routine action, if available in the request.
    routine_action = None
    if server.ROUTINE_ACTION_KEY in request:
        routine_action = RoutineAction[request[server.ROUTINE_ACTION_KEY]]

    # Set the wheel action, if available in the request.
    wheel_action = None
    if server.WHEEL_ACTION_KEY in request:
        wheel_action = WheelAction(
            linear_x=request[server.WHEEL_ACTION_KEY][server.LINEAR_X_KEY],
            angular_z=request[server.WHEEL_ACTION_KEY][server.ANGULAR_Z_KEY],
        )

    # Set the back arm action, if available in the request.
    back_arm_action = None
    if server.BACK_ARM_ACTION_KEY in request:
        back_arm_action = ArmAction[request[server.BACK_ARM_ACTION_KEY]]

    # Set the back drum action, if available in the request.
    back_drum_action = None
    if server.BACK_DRUM_ACTION_KEY in request:
        back_drum_action = DrumAction[request[server.BACK_DRUM_ACTION_KEY]]

    #Set the Joints action, if available in the request.
    joint_1_action = None
    if server.JOINT_1_ACTION_KEY in request:
        joint_1_action = AllJointAction[request[server.JOINT_1_ACTION_KEY]]

    joint_2_action = None
    if server.JOINT_2_ACTION_KEY in request:
        joint_2_action = AllJointAction[request[server.JOINT_2_ACTION_KEY]]

    joint_3_action = None
    if server.JOINT_3_ACTION_KEY in request:
        joint_3_action = AllJointAction[request[server.JOINT_3_ACTION_KEY]]
    
    joint_4_action = None
    if server.JOINT_4_ACTION_KEY in request:
        joint_4_action = AllJointAction[request[server.JOINT_4_ACTION_KEY]]
        
    joint_5_action = None
    if server.JOINT_5_ACTION_KEY in request:
        joint_5_action = AllJointAction[request[server.JOINT_5_ACTION_KEY]]

    claw_action = None
    if server.CLAW_ACTION_KEY in request:
        claw_action = ClawAction[request[server.CLAW_ACTION_KEY]]
    
    partial_autonomy = None
    if server.PARTIAL_AUTONOMY_KEY in request:
        partial_autonomy = PartialAutonomy[request[server.PARTIAL_AUTONOMY_KEY]]

    return Command(
        wheel_action,
        back_arm_action,
        back_drum_action,
        routine_action,
        joint_1_action,
        joint_2_action,
        joint_3_action,
        joint_4_action,
        joint_5_action,
        claw_action,
        partial_autonomy
    )


class Command:
    """A command containing actions for an EZRASSOR."""

    def __init__(
        self,
        wheel_action,
        back_arm_action,
        back_drum_action,
        routine_action,
        joint_1_action,
        joint_2_action,
        joint_3_action,
        joint_4_action,
        joint_5_action,
        claw_action,
        partial_autonomy
    ):
        """Initialize this command with actions."""
        self.wheel_action = wheel_action
        self.back_arm_action = back_arm_action
        self.back_drum_action = back_drum_action
        self.routine_action = routine_action
        self.joint_1_action = joint_1_action
        self.joint_2_action = joint_2_action
        self.joint_3_action = joint_3_action
        self.joint_4_action = joint_4_action
        self.joint_5_action = joint_5_action
        self.claw_action = claw_action
        self.partial_autonomy = partial_autonomy


class MetaActionEnum(enum.EnumMeta):
    """Metaclass which modifies the enum creation procedure.

    Metaclasses are like class templates (they define how to create other
    classes). Due to the nature of the Python enum system, new enum
    functionality must be provided via a metaclass. This metaclass is used to
    create enums that support 'in' checks (e.g. '"KEY" in MyEnum') and
    stringification (e.g. 'str(MyEnum)').
    """

    def __contains__(self, key):
        """Check if a key exists in the enum."""
        try:
            self[key]

            return True
        except KeyError:
            return False

    def __str__(self):
        """Create a string containing all keys in the enum."""
        return ", ".join(self.__members__.keys())

class WheelAction:
    """This action describes how to move the wheels of an EZRASSOR."""

    def __init__(self, linear_x, angular_z):
        """Initialize this action with movement floats."""
        self.linear_x = linear_x
        self.angular_z = angular_z

class ArmAction(enum.Enum, metaclass=MetaActionEnum):
    """This action describes how to move the arms of an EZRASSOR."""

    LOWER = -1.0
    STOP = 0.0
    RAISE = 1.0

class DrumAction(enum.Enum, metaclass=MetaActionEnum):
    """This action describes how to move the drums of an EZRASSOR."""

    DUMP = -1.0
    STOP = 0.0
    DIG = 1.0

class RoutineAction(enum.Enum, metaclass=MetaActionEnum):
    """This action describes which routine to execute for an EZRASSOR."""

    AUTO_DRIVE = 0b000001
    AUTO_DIG = 0b000010
    AUTO_DUMP = 0b000100
    AUTO_DOCK = 0b001000
    FULL_AUTONOMY = 0b010000
    STOP = 0b100000

class AllJointAction(enum.Enum, metaclass=MetaActionEnum):
    """These are the actions All joints have in common to exeecute for an EZRASSOR"""
    ROTATELEFT = 0.2
    ROTATERIGHT = -0.2
    ROTATEUP = -0.2
    ROTATEDOWN = 0.2
    STOP = 0.0

class ClawAction(enum.Enum, metaclass=MetaActionEnum):
    """This action describes which joint to execute for an EZRASSOR."""
    OPEN = -6.0
    CLOSE = 6.0

class PartialAutonomy(enum.Enum, metaclass=MetaActionEnum):
    """This action describes autonomous movement for the EZRASSSOR ARM"""
    # Home = (0.0, 0.0, 0.0, 0.0, 0.0)

    # Pickup_Test = [0.0, 0.0, 0.0, 0.0, 3.0]
    
    HOME = 1.0
    PLACE = 2.0
    PICKUP = 3.0
  

    # Simple_Place_Prep = (0.00, -0.8505, 1.6489, -1.3017, 0.00)

    # Simple_Place_Exec = (0.00, -0.3645, 1.6489, -1.3017, 0.00)

    # Pickup_First_Paver_Prep = (2.5167, -1.3500, 1.1900, 0.1562, -0.1709)

    # Pickup_First_Paver_Exec = (2.5861, -1.0800, 1.7050, -0.6300, -0.1709)

    # Pickup_First_Paver_After = (2.5861, -0.9200, 0.9300, 0.0000, 0.0000)

    