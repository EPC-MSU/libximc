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
                      "You can use a relative or absolute file path.")
                path = input("Enter the path: ")
                path = path.encode("utf-8")
                self.axis.set_correction_table(path)
            action = self.get_action()

    @interface_repeater
    def get_action(self) -> Action:
        print("Select a group of settings:\n"
              "Q or q keys\t-\treturn to the main menu\n"
              "M or m keys\t-\tmovement settings\n"
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
        edges_settings = self.axis.get_edges_settings()

        print("BorderFlags: {}".format(edges_settings.BorderFlags))
        if (edges_settings.BorderFlags & ximc.BorderFlags.BORDER_IS_ENCODER):
            print("BORDER_IS_ENCODER is set: The borders are fixed by predetermined encoder values.")
        else:
            print("BORDER_IS_ENCODER is unset: The borders are placed on limit switches.")

        if (edges_settings.BorderFlags & ximc.BorderFlags.BORDER_STOP_LEFT):
            print("BORDER_STOP_LEFT is set: The motor stops when it reaches the left border.")
        else:
            print("BORDER_STOP_LEFT is unset: The motor continues to move when it reaches the left border.")

        if (edges_settings.BorderFlags & ximc.BorderFlags.BORDER_STOP_RIGHT):
            print("BORDER_STOP_RIGHT is set: The motor stops when it reaches the right border.")
        else:
            print("BORDER_STOP_RIGHT is unset: The motor continues to move when it reaches the right border.")

        if (edges_settings.BorderFlags & ximc.BorderFlags.BORDERS_SWAP_MISSET_DETECTION):
            print("BORDERS_SWAP_MISSET_DETECTION is set: Detection of incorrect setting of limit switches is enabled. "
                  "The motor will stop on both borders.")
        else:
            print("BORDERS_SWAP_MISSET_DETECTION is unset: Detection of incorrect setting of limit switches is "
                  "disabled.")

        if (edges_settings.EnderFlags & ximc.EnderFlags.ENDER_SWAP):
            print("ENDER_SWAP is set: The first limit switch is on the right side.")
        else:
            print("ENDER_SWAP is unset: The first limit switch is on the right side.")

        if (edges_settings.EnderFlags & ximc.EnderFlags.ENDER_SW1_ACTIVE_LOW):
            print("ENDER_SW1_ACTIVE_LOW is set: Limit switch connected to pin SW1 is triggered by a low level on pin.")
        else:
            print("ENDER_SW1_ACTIVE_LOW is unset:Limit switch connected to pin SW1 is triggered by a high level on "
                  "pin.")

        if (edges_settings.EnderFlags & ximc.EnderFlags.ENDER_SW2_ACTIVE_LOW):
            print("ENDER_SW2_ACTIVE_LOW is set: Limit switch connected to pin SW2 is triggered by a low level on pin.")
        else:
            print("ENDER_SW2_ACTIVE_LOW is unset: Limit switch connected to pin SW2 is triggered by a high level on "
                  "pin.")

        # The position of the boundaries.
        print("The positions of the borders")
        print("Coordinate of the left border: Pos {0}, uPos {1}".format(edges_settings.LeftBorder,
                                                                        edges_settings.uLeftBorder))
        print("Coordinate of the right border: Pos {0}, uPos {1} \n".format(edges_settings.RightBorder,
                                                                            edges_settings.uRightBorder))

        # Enter the values for the flags.
        edges_settings.BorderFlags = self.ask_for_border_flags()
        edges_settings.EnderFlags = self.ask_for_ender_flags()

        # Enter borders.
        print("To enter the border Y/N ?")
        key_press = input("Do you want to set the borders? Y/N")
        if key_press == "Y" or key_press == "y":
            try:
                edges_settings.LeftBorder = interface_repeater(lambda: int(input("Enter the left border: ")))()
                edges_settings.RightBorder = interface_repeater(lambda: int(input("Enter the right border: ")))()
            except Exception:
                print("Left border {0}, right border {1}".format(edges_settings.LeftBorder, edges_settings.RightBorder))
        self.axis.set_edges_settings()

    def ask_for_border_flags(self) -> None:
        res = ximc.BorderFlags(0)
        for flag in ximc.BorderFlags:
            print("Set {}? Y/N".format(flag.name))
            key_pressed = input()
            res |= (flag if key_pressed == "Y" or key_pressed == "y" else res)
        return res

    def ask_for_ender_flags(self) -> None:
        res = ximc.EnderFlags(0)
        for flag in ximc.EnderFlags:
            print("Set {}? Y/N".format(flag.name))
            key_pressed = input()
            res |= (flag if key_pressed == "Y" or key_pressed == "y" else res)
        return res

    def change_microstep_mode(self) -> None:
        """Setting the microstep mode. Works only with stepper motors"""
        print("\nMicrostep mode settings. This setting is only available for stepper motors.")
        # Get current engine settings from controller
        engine_settings = self.axis.get_engine_settings()
        print("Current mode: {}".format(engine_settings.MicrostepMode.name))
        engine_settings.MicrostepMode = self.get_microstep_mode()
        self.axis.set_engine_settings(engine_settings)
        print("The mode is set to",  engine_settings.MicrostepMode.name)

    @interface_repeater
    def get_microstep_mode(self) -> ximc.MicrostepMode:
        print("Select microstep mode:")
        modes = [mode for mode in ximc.MicrostepMode]
        for i, mode in enumerate(modes):
            print("To set mode {0} - enter {1}".format(mode.name, i))
        choosen_index = int(input())
        if choosen_index < 0 or choosen_index >= len(modes):
            raise ValueError("Wrong index!")
        return modes[choosen_index]

    def change_user_unit_mode(self) -> None:
        """User unit mode settings"""
        print("\nUser unit mode settings.")
        print("Current user unit coordinate multiplier = {0} \n".format(self.axis.get_calb()[0]))
        engine_settings = self.axis.get_engine_settings()
        self.axis.set_calb(interface_repeater(lambda: float(input("Set new coordinate multiplier: ")))(),
                           engine_settings.MicrostepMode)


class FeedbackSettings:
    def __init__(self, axis: ximc.Axis):
        self.axis = axis

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
        print("NOTE: in case of Encoder or Encoder-Mediated type, controller uses rpm instead of steps/sec.")
        feedback_settings.FeedbackType = self.ask_for_feedback_type()
        feedback_settings.FeedbackFlags = self.ask_for_feedback_flag()
        self.axis.set_feedback_settings(feedback_settings)

    @interface_repeater
    def ask_for_feedback_type(self) -> ximc.FeedbackType:
        types = [t for t in ximc.FeedbackType]
        print("Select a new feedback type:")
        for i, t in enumerate(types):
            print("To set {0} - enter {1}".format(t.name, i))
        choosen_index = int(input())
        if choosen_index < 0 or choosen_index >= len(types):
            raise ValueError("Wrong index!")
        return types[choosen_index]

    @interface_repeater
    def ask_for_feedback_flag(self) -> ximc.FeedbackFlags:
        flags = (ximc.FeedbackFlags.FEEDBACK_ENC_TYPE_AUTO,
                 ximc.FeedbackFlags.FEEDBACK_ENC_TYPE_DIFFERENTIAL,
                 ximc.FeedbackFlags.FEEDBACK_ENC_TYPE_SINGLE_ENDED)

        print("Select a new feedback flag:")
        for i, f in enumerate(flags):
            print("To set {0} - enter {1}".format(f.name, i))
        choosen_index = int(input())
        if choosen_index < 0 or choosen_index >= len(flags):
            raise ValueError("Wrong index!")

        key = input("Do you want to enable reverse? Y/N")
        if key == "Y" or key == "y":
            return flags[choosen_index] | ximc.FeedbackFlags.FEEDBACK_ENC_REVERSE
        else:
            return flags[choosen_index]


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
