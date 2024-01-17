"""This module is an extended example of using the libximc library to control 8SMC series using the Python language"""
import os
import sys
import platform
from time import sleep
from abc import ABC
from enum import Enum
import libximc.highlevel as ximc


def interface_repeater(func):
    """Supporting decorator. It allows repeat command request if enter invalid value."""
    def wrapper(*args, **kwargs):
        while True:
            try:
                func(*args, **kwargs)
            except KeyboardInterrupt:
                print("Exiting...")
                exit()
            except Exception:
                print("Incorrect input! Try again.")
    return wrapper


class SelectionManager:
    """Helps you to select the device to connect to"""
    class DeviceType(Enum):
        COM_DEVICE = 1
        VIRT_DEVICE = 2
        NETWORK_DEVICE = 3
        ALL_DEVICES = 4

    def get_uri(self) -> str:
        """Device selection Manager.

        :return: URI of the device to open
        :rtype: str
        """
        device_type = self.get_device_type()
        if device_type == SelectionManager.DeviceType.COM_DEVICE:
            uri = self.get_com_uri()
        elif device_type == SelectionManager.DeviceType.VIRT_DEVICE:
            uri = self.get_virt_uri()
        elif device_type == SelectionManager.DeviceType.NETWORK_DEVICE:
            uri = self.get_network_uri()
        elif device_type == SelectionManager.DeviceType.ALL_DEVICES:
            devenum = self.get_devices_enumeration()

            if len(sys.argv) > 1:  # TODO: probably it should be taken out of here
                uri = sys.argv[1]
            elif len(devenum) > 0:
                index = self.get_device_index(devenum)
                uri = devenum[index]["uri"]
            else:
                # set path to virtual device file to be created
                tempdir = os.path.join(os.path.expanduser('~'), "testdevice.bin")
                uri = "xi-emu:///" + tempdir
        else:
            raise RuntimeError("Wrong device type! Got {}".format(device_type))
        return uri

    def get_device_type(self) -> DeviceType:
        while True:
            print("What XIMC device do you want to open?\n"
                  "Press the key:\n"
                  "1 - for COM device\n"
                  "2 - for virtual device\n"
                  "3 - network device\n"
                  "4 - search for all available devices.")
            try:
                key = int(input())
                return SelectionManager.DeviceType(key)
            except Exception:
                print("Wrong input! Try again.")

    def get_com_uri(self) -> str:
        if platform.system() == "Windows":
            print(r"Enter the port number: \\.\COM")
            uri = r"xi-com:\\.\COM" + input()
        else:
            print("Enter the port number: dev/tty.s")
            uri = "xi-com:/dev/tty.s" + input()
        return uri

    def get_virt_uri(self) -> str:
        return "xi-emu:///" + os.path.join(os.path.expanduser('~'), "virtual_controller.bin")

    def get_network_uri(self) -> str:
        print("Enter the device's network address:")
        print("Example: 192.168.0.1/89ABCDEF, where 192.168.0.1 is an IP of the device and 89ABCDEF"
              " is a serial number.")
        return "xi-net://" + input()

    def get_devices_enumeration(self) -> 'list':
        # ******************************************** #
        #         Device searching and probing         #
        # ******************************************** #

        # Flags explanation:
        # ximc.EnumerateFlags.ENUMERATE_PROBE   -   Probing found devices for detailed info.
        # ximc.EnumerateFlags.ENUMERATE_NETWORK -   Check network devices.
        enum_flags = ximc.EnumerateFlags.ENUMERATE_PROBE | ximc.EnumerateFlags.ENUMERATE_NETWORK

        # Hint explanation:
        # "addr=" hint is used for broadcast network enumeration
        enum_hints = "addr="
        return ximc.enumerate_devices(enum_flags, enum_hints)

    @interface_repeater
    def get_device_index(self, devenum: 'list[dict]') -> int:
        for i, dev in enumerate(devenum):
            print("#{} - {}, {}, SN{}: ".format(i, dev["ControllerName"], dev["uri"], dev["device_serial"]))
        print("Enter the device number:")
        index = int(input())
        if index > len(devenum) or index < 0:
            print("Index is out of range! Try again.")
            raise ValueError("Device index is out of range!")
        return index


class GeneralManager:
    class Action(Enum):
        QUIT = "q"
        MOVE = "m"
        MOVE_CALB = "c"
        EXTIO = "i"
        CHANGE_SETTINGS = "s"

    def __init__(self, axis: ximc.Axis):
        self.axis = axis
        self.move_manager = MovementManager(axis)
        self.move_manage_calb = MovementManagerCalb(axis)
        self.extio_manager = EXTIOManager(axis)
        self.settings_manager = SettingsManager(axis)

        # Set default 1:1 scaling for *_calb commands
        self.axis.set_calb(1, self.axis.get_engine_settings().MicrostepMode)

    def start(self):
        action = self.get_action()
        while action != GeneralManager.Action.QUIT:
            if action == GeneralManager.Action.MOVE:
                self.move_manager.start()
            if action == GeneralManager.Action.MOVE_CALB:
                self.move_manage_calb.start()
            elif action == GeneralManager.Action.EXTIO:
                self.extio_manager.start()
            elif action == GeneralManager.Action.CHANGE_SETTINGS:
                self.settings_manager.start()
            action = self.get_action()
        print("Exit program...")

    @interface_repeater
    def get_action(self) -> Action:
        print("Actions with the XIMC device\n"
              "Press key:\n"
              "Q or q keys\t-\texit\n"
              "M or m key\t-\tmove\n"
              "C or c key\t-\tmove (user-units)\n"
              "I or i keys\t-\texternal I/O EXTIO\n"
              "E or e keys\t-\tEEPROM\n"
              "S or s keys\t-\tchange settings\n"
              "Selected action.\n"
              " ")
        key = input()
        return GeneralManager.Action(key.lower())


class MovementManagerBase(ABC):
    class Action(Enum):
        QUIT = "q"
        LEFT = "l"
        RIGHT = "r"
        MOVE = "m"
        SHIFT = "s"
        HOME = "h"
        ZERO = "z"

    def __init__(self, axis: ximc.Axis):
        self.axis = axis

    def start(self):
        action = self.get_action()
        while action != MovementManager.Action.QUIT:
            if action == MovementManager.Action.MOVE:
                print("Moving to position...")
                self.axis.command_move(*self.get_position())
                self.verbose_wait_for_stop(0.10)

            elif action == MovementManager.Action.SHIFT:
                print("Shifting on position delta...")
                self.axis.command_movr(*self.get_delta_position())
                self.verbose_wait_for_stop(0.10)

            elif action == MovementManager.Action.LEFT:
                self.axis.command_left()
                print("Moving to the left... Press Enter to stop.")
                input()
                self.axis.command_sstp()

            elif action == MovementManager.Action.RIGHT:
                self.axis.command_right()
                print("Moving to the right... Press Enter to stop.")
                input()
                self.axis.command_sstp()

            elif action == MovementManager.Action.HOME:
                print("Homing...")
                self.axis.command_home()
                self.verbose_wait_for_stop(0.10)

            elif action == MovementManager.Action.ZERO:
                print("Zeroing...")
                self.axis.command_zero()

            print("Waiting for movement completion...")
            self.axis.command_wait_for_stop(10)

    @interface_repeater
    def get_action(self) -> Action:
        print("Actions with the XIMC device\n"
              "Press key:"
              "Q or q keys\t-\treturn to the main menu\n"
              "L or l keys\t-\tmove to the left\n"
              "R or r keys\t-\tmove to the right. Press and hold the key\n"
              "M or m keys\t-\tmove to position(mov)\n"
              "S or s keys\t-\tposition shift(movr)\n"
              "H or h keys\t-\tHOME position\n"
              "Z or z keys\t-\tZERO position\n"
              "Selected action")
        key = input()
        return MovementManagerBase.Action(key.lower())

    def get_position(self):
        pass

    def get_delta_position(self):
        pass

    def verbose_wait_for_stop(self, refresh_interval_ms):
        pass


class MovementManager(MovementManagerBase):
    @interface_repeater
    def get_position(self) -> "tuple":
        print("Enter target position")
        print("An integer part (in steps): ", end="")
        position = int(input())
        print("A fractional part (in micro steps): ", end="")
        uposition = int(input())
        return position, uposition

    @interface_repeater
    def get_delta_position(self) -> "tuple":
        print("Enter position delta")
        print("An integer part (in steps): ", end="")
        delta = int(input())
        print("A fractional part (in micro steps): ", end="")
        udelta = int(input())
        return delta, udelta

    def verbose_wait_for_stop(self, refresh_interval_ms: int) -> None:
        """This function performs dynamic output coordinate in the process of moving."""
        while self.axis.get_status().MvCmdSts & ximc.MvcmdStatus.MVCMD_RUNNING:
            position = self.axis.get_position()
            print("Position: {} steps {} microsteps".format(position.Position, position.uPosition))
            sleep(refresh_interval_ms * 1000)


class MovementManagerCalb(MovementManagerBase):
    @interface_repeater
    def get_position(self) -> float:
        print("Enter target position")
        print("An integer part: ", end="")
        position = float(input())
        return position

    @interface_repeater
    def get_delta_position(self) -> float:
        print("Enter position delta")
        print("An integer part: ", end="")
        delta = float(input())
        return delta

    def verbose_wait_for_stop(self, refresh_interval_ms: int) -> None:
        """This function performs dynamic output coordinate in the process of moving."""
        while self.axis.get_status().MvCmdSts & ximc.MvcmdStatus.MVCMD_RUNNING:
            position = self.axis.get_position_calb()
            print("Position: {}".format(position.Position))
            sleep(refresh_interval_ms * 1000)


class EXTIOManager:
    """External input / output settings Manager."""
    class InputFlag(Enum):
        EXTIO_SETUP_MODE_IN_STOP = 1
        EXTIO_SETUP_MODE_IN_PWOF = 2
        EXTIO_SETUP_MODE_IN_MOVR = 3
        EXTIO_SETUP_MODE_IN_HOME = 4
        EXTIO_SETUP_MODE_IN_ALARM = 5

    class OutputFlag(Enum):
        EXTIO_SETUP_MODE_OUT_MOVING = 1
        EXTIO_SETUP_MODE_OUT_ALARM = 2
        EXTIO_SETUP_MODE_OUT_MOTOR_ON = 3

    class Direction(Enum):
        INPUT = "i"
        OUTPUT = "o"
        INV_OUTPUT = "r"

    def __init__(self, axis: ximc.Axis):
        self.axis = axis

    def start(self) -> None:
        direction = self.get_direction()
        extio_settings = self.axis.get_extio_settings()
        if direction == EXTIOManager.Direction.INPUT:
            extio_settings.EXTIOSetupFlags = 0  # Set input direction

            flag = self.get_input_flag()
            if flag == EXTIOManager.InputFlag.EXTIO_SETUP_MODE_IN_STOP:
                extio_settings.EXTIOModeFlags = ximc.ExtioModeFlags.EXTIO_SETUP_MODE_IN_STOP
                print("The device will stop moving on external input.")
            elif flag == EXTIOManager.InputFlag.EXTIO_SETUP_MODE_IN_PWOF:
                extio_settings.EXTIOModeFlags = ximc.ExtioModeFlags.EXTIO_SETUP_MODE_IN_PWOF
                print("The device will perform power OFF on external input.")
            elif flag == EXTIOManager.InputFlag.EXTIO_SETUP_MODE_IN_MOVR:
                extio_settings.EXTIOModeFlags = ximc.ExtioModeFlags.EXTIO_SETUP_MODE_IN_MOVR
                print("The device will launch movr command with previous settings on external input.")
            elif flag == EXTIOManager.InputFlag.EXTIO_SETUP_MODE_IN_HOME:
                extio_settings.EXTIOModeFlags = ximc.ExtioModeFlags.EXTIO_SETUP_MODE_IN_HOME
                print("The device will perform homing on external input.")
            elif flag == EXTIOManager.InputFlag.EXTIO_SETUP_MODE_IN_ALARM:
                extio_settings.EXTIOModeFlags = ximc.ExtioModeFlags.EXTIO_SETUP_MODE_IN_ALARM
                print("The device will enter an alarm state on external input.")
        elif direction == EXTIOManager.Direction.OUTPUT or direction == EXTIOManager.Direction.INV_OUTPUT:
            extio_settings.EXTIOSetupFlags = ximc.ExtioSetupFlags.EXTIO_SETUP_OUTPUT
            if direction == EXTIOManager.Direction.INV_OUTPUT:
                extio_settings.EXTIOSetupFlags |= ximc.ExtioSetupFlags.EXTIO_SETUP_INVERT

            flag = self.get_output_flag
            if flag == EXTIOManager.OutputFlag.EXTIO_SETUP_MODE_OUT_MOVING:
                extio_settings.EXTIOModeFlags = ximc.ExtioModeFlags.EXTIO_SETUP_MODE_OUT_MOVING
                print("EXTIO output will stay active during moving.")
            elif flag == EXTIOManager.OutputFlag.EXTIO_SETUP_MODE_OUT_ALARM:
                extio_settings.EXTIOModeFlags = ximc.ExtioModeFlags.EXTIO_SETUP_MODE_OUT_ALARM
                print("EXTIO output will stay active during alarm state")
            elif flag == EXTIOManager.OutputFlag.EXTIO_SETUP_MODE_OUT_MOTOR_ON:
                extio_settings.EXTIOModeFlags = ximc.ExtioModeFlags.EXTIO_SETUP_MODE_OUT_MOTOR_ON
                print("EXTIO output will stay active during the windings are powered")
        else:
            raise RuntimeError("Wrong direction! Got {}".format(direction))
        self.axis.set_extio_settings(extio_settings)

    @interface_repeater
    def get_input_flag(self) -> InputFlag:
        print("Set EXTIO input mode.\n"
              "Press the key:\n"
              "1 - EXTIO_SETUP_MODE_IN_STO\n"
              "2 - EXTIO_SETUP_MODE_IN_PWOF\n"
              "3 - EXTIO_SETUP_MODE_IN_MOVR\n"
              "4 - EXTIO_SETUP_MODE_IN_HOME\n"
              "5 - EXTIO_SETUP_MODE_IN_ALARM\n")
        return EXTIOManager.InputFlag(input())

    @interface_repeater
    def get_output_flag(self) -> OutputFlag:
        print("Set EXTIO input mode.\n"
              "Press the key:\n"
              "1 - EXTIO_SETUP_MODE_OUT_MOVING\n"
              "2 - EXTIO_SETUP_MODE_OUT_ALARM\n"
              "3 - EXTIO_SETUP_MODE_OUT_MOTOR_ON\n")
        return EXTIOManager.OutputFlag(input())

    @interface_repeater
    def get_direction(self) -> Direction:
        print("Use output as input or output?"
              "Press the key:\n"
              "I or i keys - input\n"
              "O or o keys - output\n"
              "R or r keys - inverted output\n")
        return EXTIOManager.Direction(input().lower)


class SettingsManager:
    class Action(Enum):
        QUIT = "q"
        MOVE_SETTINGS = "m"
        MOVE_SETTINGS_CALB = "c"
        FEEDBACK_SETTINGS = "f"
        EDGES_SETTINGS = "e"
        MICROSTEP_SETTINGS = "s"
        USER_UNIT_SETTINGS = "u"
        LOAD_CORRECTION_TABLE = "l"

    def __init__(self, axis: ximc.Axis):
        self.axis = axis
        self.feedback_settings_manager = FeedbackSettings(axis)

    def start(self) -> None:
        """
        Manager of the controller settings.

        This function, among other settings, allows you to load the coordinate correction table.
        Follow the on-screen instructions to change the settings.

        :param lib: structure for accessing the functionality of the libximc library.
        :param device_id: device id.

        note:
            The device_id parameter in this function is a C pointer, unlike most library functions that use this
            parameter
        """
        action = self.get_action()
        while action != SettingsManager.Action.QUIT:
            if action == SettingsManager.Action.MOVE_SETTINGS:
                self.change_move_settings()
            if action == SettingsManager.Action.MOVE_SETTINGS_CALB:
                self.change_move_settings_calb()
            if action == SettingsManager.Action.FEEDBACK_SETTINGS:
                self.feedback_settings_manager.start()
            if action == SettingsManager.Action.EDGES_SETTINGS:
                self.change_edges_settings()
            if action == SettingsManager.Action.MICROSTEP_SETTINGS:
                self.change_microstep_mode()
            if action == SettingsManager.Action.USER_UNIT_SETTINGS:
                self.change_user_unit_mode()
            if action == SettingsManager.Action.LOAD_CORRECTION_TABLE:
                print("Correction table loading...\n"
                      "You can use a short or full file name.")
                namefile = input("Enter the file name: ")
                if type(namefile) is str:
                    namefile = namefile.encode("utf-8")
                self.axis.set_correction_table(namefile)
            action = self.get_action()

    @interface_repeater
    def get_action(self) -> Action:
        print("Select a group of settings:\n"
              "Q or q keys\t-\treturn to the main menu\n"
              "M or m keys\t-\movement settings\n"
              "C or c keys\t-\tcalb motion settings\n"
              "F or f keys\t-\tfeedback settings\n"
              "E or e keys\t-\tedges settings\n"
              "S or s keys\t-\tmicro step mode settings\n"
              "U or u keys\t-\tuser unit settings\n"
              "L or l keys\t-\tload correction table\n")
        return SettingsManager.Action(input().lower())

    def change_move_settings(self) -> None:
        """Set speed, acceleration, and deceleration"""
        print("\nGet motion settings")
        move_settings = self.axis.get_move_settings()
        print("Current speed: {}".format(move_settings.Speed))
        print("Current acceleration: {}".format(move_settings.Accel))
        print("Current deceleration: {}".format(move_settings.Decel) + "\n")

        new_speed = interface_repeater(lambda: int(input("Input speed: ")))
        new_asel = interface_repeater(lambda: int(input("Input acceleration: ")))
        new_decel = interface_repeater(lambda: int(input("Input deceleration: ")))

        move_settings.Speed = new_speed
        move_settings.Accel = new_asel
        move_settings.Decel = new_decel

        self.axis.set_move_settings(move_settings)

    def change_move_settings_calb(self) -> None:
        """Set speed, acceleration, and deceleration"""
        print("\nGet motion settings")
        move_settings = self.axis.get_move_settings_calb()
        print("Current speed: {}".format(move_settings.Speed))
        print("Current acceleration: {}".format(move_settings.Accel))
        print("Current deceleration: {}".format(move_settings.Decel) + "\n")

        new_speed = interface_repeater(lambda: float(input("Input speed: ")))()
        new_asel = interface_repeater(lambda: float(input("Input acceleration: ")))()
        new_decel = interface_repeater(lambda: float(input("Input deceleration: ")))()

        move_settings.Speed = new_speed
        move_settings.Accel = new_asel
        move_settings.Decel = new_decel

        self.axis.set_move_settings_calb(move_settings)

    def change_edges_settings(self) -> None:
        """View and configure the limit switch mode."""
        # Get current feedback settings from controller
        edgst = edges_settings_t()
        result = lib.get_edges_settings(device_id, byref(edgst))
        # Print command return status. It will be 0 if all is OK
        if result == Result.Ok:
            # Print The current edge settings
            # BorderFlags
            Border_Flags = ["BorderFlags", "BORDER_IS_ENCODER", "BORDER_STOP_LEFT", "BORDER_STOP_RIGHT", "BORDERS_SWAP_MISSET_DETECTION"]
            print("BorderFlags {0:x}".format(edgst.BorderFlags))
            if (edgst.BorderFlags & BorderFlags.BORDER_IS_ENCODER):
                print("BORDER_IS_ENCODER 1:The borders are set with coordinates.")
            else:
                print("BORDER_IS_ENCODER 0:The position of the borders is set by limit switches.")

            if (edgst.BorderFlags & BorderFlags.BORDER_STOP_LEFT):
                print("BORDER_STOP_LEFT 1:The motor stops when it reaches the left border.")
            else:
                print("BORDER_STOP_LEFT 0:The motor continues to move when it reaches the left border.")

            if (edgst.BorderFlags & BorderFlags.BORDER_STOP_RIGHT):
                print("BORDER_STOP_RIGHT 1:The motor stops when it reaches the rigth border.")
            else:
                print("BORDER_STOP_RIGHT 0:The motor continues to move when it reaches the rigth border.")

            if (edgst.BorderFlags & BorderFlags.BORDERS_SWAP_MISSET_DETECTION):
                print("BORDERS_SWAP_MISSET_DETECTION 1:Detection of incorrect setting of limit switches is enabled.")
            else:
                print("BORDERS_SWAP_MISSET_DETECTION 0:Detection of incorrect setting of limit switches is disabled.")

            # EnderFlags
            Ender_Flags = ["EnderFlags", "ENDER_SWAP", "ENDER_SW1_ACTIVE_LOW", "ENDER_SW2_ACTIVE_LOW"]
            print("EnderFlags {0:x}".format(edgst.EnderFlags))
            if (edgst.EnderFlags & EnderFlags.ENDER_SWAP):
                print("ENDER_SWAP 1:The first limit switch is located on the right.")
            else:
                print("ENDER_SWAP 0:The first limit switch is located on the left.")

            if (edgst.EnderFlags & EnderFlags.ENDER_SW1_ACTIVE_LOW):
                print("ENDER_SW1_ACTIVE_LOW 1:Low-level SW1 triggering.")
            else:
                print("ENDER_SW1_ACTIVE_LOW 0:High-level SW1 triggering.")

            if (edgst.EnderFlags & EnderFlags.ENDER_SW2_ACTIVE_LOW):
                print("ENDER_SW2_ACTIVE_LOW 1:Low-level SW2 triggering.")
            else:
                print("ENDER_SW2_ACTIVE_LOW 0:High-level SW2 triggering.")

            # The position of the boundaries.
            print("The positions of the borders")
            print("Coordinate of the left border:Pos {0}, uPos {1}".format(edgst.LeftBorder, edgst.uLeftBorder))
            print("Coordinate of the right border:Pos {0}, uPos {1} \n".format(edgst.RightBorder, edgst.uRightBorder))

            # Enter the values for the flags.
            print("Enter the values for the flags 0 or 1.")
            print("Leave the value unchanged any k.")
            edgst.BorderFlags = input_flags(edgst.BorderFlags, Border_Flags)
            edgst.EnderFlags = input_flags(edgst.EnderFlags, Ender_Flags)

            # Enter borders.
            print("To enter the border Y/N ?")
            key_press = getch()
            if ord(key_press) == 89 or ord(key_press) == 121:  # Press "Y"
                print("Enter borders.")
                try:
                    edgst.LeftBorder = int(input_new("Enter the left border: "))
                    edgst.RightBorder = int(input_new("Enter the right border: "))
                except:
                    print("Left border {0}, right border {1}".format(edgst.LeftBorder, edgst.RightBorder))
            result = lib.set_edges_settings(device_id, byref(edgst))

    def change_microstep_mode(self) -> None:
        """
        Setting the microstep mode. Works only for stepper motors"""
        print("\nMicrostep mode settings.")
        print("This setting is only available for stepper motors.")
        # Get current engine settings from controller
        result = lib.get_engine_settings(device_id, byref(eng))
        if result == Result.Ok:
            # Current MICROSTEP_MODE
            Microstep_Mode = ["", "MICROSTEP_MODE_FULL", "MICROSTEP_MODE_FRAC_2", "MICROSTEP_MODE_FRAC_4",
                            "MICROSTEP_MODE_FRAC_8", "MICROSTEP_MODE_FRAC_16", "MICROSTEP_MODE_FRAC_32",
                            "MICROSTEP_MODE_FRAC_64", "MICROSTEP_MODE_FRAC_128", "MICROSTEP_MODE_FRAC_256"]
            print("The mode is set to",  Microstep_Mode[eng.MicrostepMode], "\n")
            # Change MicrostepMode parameter
            # (use MICROSTEP_MODE_FULL to MICROSTEP_MODE_FRAC_256 - 9 microstep modes)
            for range_val in range(len(Microstep_Mode)):
                if range_val > 0:
                    print("Set mode {0} - press {1}".format(Microstep_Mode[range_val], range_val))
            try:
                in_val = int(getch())
                if in_val > 0 and in_val <=9:
                    eng.MicrostepMode = in_val
                    user_unit.MicrostepMode = in_val
                print("The mode is set to", Microstep_Mode[eng.MicrostepMode])
            except:
                print("The mode is set to",  Microstep_Mode[eng.MicrostepMode])
            result = lib.set_engine_settings(device_id, byref(eng))
            if result != Result.Ok:
                print("Error recording microstep mode.")
            print("")

    def change_user_unit_mode(self) -> None:
        """User unit mode settings"""
        print("\nUser unit mode settings.")
        print("User unit coordinate multiplier = {0} \n".format(user_unit.A) )
        try:
            fl_val = float(input_new("Set new coordinate multiplier = "))
            user_unit.A = fl_val
        except:
            print("User unit coordinate multiplier = ", user_unit.A )


class FeedbackSettings:
    def __init__(self, axis: ximc.Axis):
        self.axis = axis
        self.feedback_settings = axis.get_feedback_settings()

    def start(self):
        pass

    def change_feedback_settings(self) -> None:
        # Get current feedback settings from controller
        feedback_settings = self.axis.get_feedback_settings()

        print("Feedback type: {}".format(feedback_settings.FeedbackType))
        if feedback_settings.FeedbackFlags & ximc.FeedbackFlags.FEEDBACK_ENC_REVERSE:
            print("Encoder mode: ENC_REVERSE")
        else:
            print("Encoder mode: ENC_NO_REVERSE")

        if feedback_settings.FeedbackFlags & ximc.FeedbackFlags.FEEDBACK_ENC_TYPE_SINGLE_ENDED:
            print("Encoder type: FEEDBACK_ENC_TYPE_SINGLE_ENDED")
        if feedback_settings.FeedbackFlags & ximc.FeedbackFlags.FEEDBACK_ENC_TYPE_DIFFERENTIAL:
            print("Encoder type: FEEDBACK_ENC_TYPE_DIFFERENTIAL")

        # Select a new feedback mode
        print("Select a new feedback mode")
        print("5 - NONE")
        print("4 - EMF")
        print("1 - ENCODER")
        print("6 - ENCODER_MEDIATED")
        print("Any other key - cancel")
        key_press = getch()
        if ord(key_press) == 49:  # Press "1"
            print("You need to convert the movement parameters to rpm")
            print("New feedback mode  ENCODER")
            feedback_settings.FeedbackType = ximc.FeedbackType.FEEDBACK_ENCODER
        elif ord(key_press) == 52:  # Press "4"
            print("You need to convert the movement parameters to step/s")
            print("New feedback mode  EMF")
            feedback_settings.FeedbackType = ximc.FeedbackType.FEEDBACK_EMF
        elif ord(key_press) == 53:  # Press "5"
            print("You need to convert the movement parameters to step/s")
            print("New feedback mode  NONE")
            feedback_settings.FeedbackType = ximc.FeedbackType.FEEDBACK_NONE
        elif ord(key_press) == 54:  # Press "6"
            print("CYou need to convert the movement parameters to rpm")
            print("New feedback mode  ENCODER_MEDIATED")
            feedback_settings.FeedbackType = ximc.FeedbackType.FEEDBACK_ENCODER_MEDIATED

        # Invert the reverse
        print("\nR or r key invert the reverse")
        print("Any other key - cancel")
        key_press = getch()
        if ord(key_press) == 82 or ord(key_press) == 114:  # Press "R"            
            if feedback_settings.FeedbackFlags & ximc.FeedbackFlags.FEEDBACK_ENC_REVERSE == ximc.FeedbackFlags.FEEDBACK_ENC_REVERSE:
                print("ENC_NO_REVERSE")
                feedback_settings.FeedbackFlags = feedback_settings.FeedbackFlags & ~ximc.FeedbackFlags.FEEDBACK_ENC_REVERSE
            else:
                print("ENC_REVERSE")
                feedback_settings.FeedbackFlags = feedback_settings.FeedbackFlags | ximc.FeedbackFlags.FEEDBACK_ENC_REVERSE

        # Select new feedback type
        print("\nSelect a new feedback type")
        print("S or s key - SINGLE_ENDED")
        print("D or d key - DIFFERENTIAL")
        print("Any other key - cancel")
        key_press = getch()
        if ord(key_press) == 68 or ord(key_press) == 100:  # Press "D"
            feedback_settings.FeedbackFlags = (feedback_settings.FeedbackFlags & 0x0F) | ximc.FeedbackFlags.FEEDBACK_ENC_TYPE_DIFFERENTIAL
            print("New feedback type DIFFERENTIAL")
        elif ord(key_press) == 83 or ord(key_press) == 115:  # Press "S"
            feedback_settings.FeedbackFlags = (feedback_settings.FeedbackFlags & 0x0F) | ximc.FeedbackFlags.FEEDBACK_ENC_TYPE_SINGLE_ENDED
            print("New feedback type SINGLE_ENDED")
            axis.set_feedback_settings(feedback_settings)



def main():
    """
    Starts Selection Manager and General Manager.
    """
    print("Library version: " + ximc.ximc_version())

    uri = SelectionManager().get_uri()

    # ******************************************** #
    #              Create axis object              #
    # ******************************************** #
    # Axis is the main libximc.highlevel class. It allows you to interact with the device.
    # Axis takes one argument - URI of the device.
    axis = ximc.Axis(uri)
    print("\nOpen device " + axis.uri)
    axis.open_device()  # The connection must be opened manually

    GeneralManager(axis).start()

    print("\nClosing")
    axis.close_device()
    print("Done")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print(e)
