from enum import Enum
from support_routines import interface_repeater
import libximc.highlevel as ximc


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
        action = self.ask_for_action()
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
                self.axis.set_correction_table(path)
            action = self.ask_for_action()

    @interface_repeater
    def ask_for_action(self) -> Action:
        print("\n===== Settings menu =====\n"
              "Select a group of settings:\n"
              "Q or q keys\t-\treturn to the main menu\n"
              "M or m keys\t-\tmovement settings\n"
              "C or c keys\t-\tmovement settings (calb)\n"
              "F or f keys\t-\tfeedback settings\n"
              "E or e keys\t-\tedges settings\n"
              "S or s keys\t-\tmicro step mode settings\n"
              "U or u keys\t-\tuser unit settings\n"
              "L or l keys\t-\tload correction table\n")
        return SettingsManager.Action(input("Your choice: ").lower())

    def change_move_settings(self) -> None:
        """Set speed, acceleration, and deceleration"""
        print("\nGet motion settings")
        move_settings = self.axis.get_move_settings()
        print("Current speed: {}".format(move_settings.Speed))
        print("Current acceleration: {}".format(move_settings.Accel))
        print("Current deceleration: {}".format(move_settings.Decel) + "\n")

        new_speed = interface_repeater(lambda: int(input("Input speed: ")))()
        new_asel = interface_repeater(lambda: int(input("Input acceleration: ")))()
        new_decel = interface_repeater(lambda: int(input("Input deceleration: ")))()

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

        print("Current BorderFlags: {}".format(edges_settings.BorderFlags))
        if (edges_settings.BorderFlags & ximc.BorderFlags.BORDER_IS_ENCODER):
            print("\tBORDER_IS_ENCODER is set: The borders are fixed by predetermined encoder values.")
        else:
            print("\tBORDER_IS_ENCODER is unset: The borders are placed on limit switches.")

        if (edges_settings.BorderFlags & ximc.BorderFlags.BORDER_STOP_LEFT):
            print("\tBORDER_STOP_LEFT is set: The motor stops when it reaches the left border.")
        else:
            print("\tBORDER_STOP_LEFT is unset: The motor continues to move when it reaches the left border.")

        if (edges_settings.BorderFlags & ximc.BorderFlags.BORDER_STOP_RIGHT):
            print("\tBORDER_STOP_RIGHT is set: The motor stops when it reaches the right border.")
        else:
            print("\tBORDER_STOP_RIGHT is unset: The motor continues to move when it reaches the right border.")

        if (edges_settings.BorderFlags & ximc.BorderFlags.BORDERS_SWAP_MISSET_DETECTION):
            print("\tBORDERS_SWAP_MISSET_DETECTION is set: Detection of incorrect setting of limit switches is "
                  "enabled. The motor will stop on both borders.")
        else:
            print("\tBORDERS_SWAP_MISSET_DETECTION is unset: Detection of incorrect setting of limit switches is "
                  "disabled.")

        if (edges_settings.EnderFlags & ximc.EnderFlags.ENDER_SWAP):
            print("\tENDER_SWAP is set: The first limit switch is on the right side.")
        else:
            print("\tENDER_SWAP is unset: The first limit switch is on the right side.")

        if (edges_settings.EnderFlags & ximc.EnderFlags.ENDER_SW1_ACTIVE_LOW):
            print("\tENDER_SW1_ACTIVE_LOW is set: Limit switch connected to pin SW1 is triggered by a low level on "
                  "pin.")
        else:
            print("\tENDER_SW1_ACTIVE_LOW is unset:Limit switch connected to pin SW1 is triggered by a high level on "
                  "pin.")

        if (edges_settings.EnderFlags & ximc.EnderFlags.ENDER_SW2_ACTIVE_LOW):
            print("\tENDER_SW2_ACTIVE_LOW is set: Limit switch connected to pin SW2 is triggered by a low level on "
                  "pin.")
        else:
            print("\tENDER_SW2_ACTIVE_LOW is unset: Limit switch connected to pin SW2 is triggered by a high level on "
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
        key_press = input("Do you want to reset the borders? Y/N ")
        if key_press == "Y" or key_press == "y":
            try:
                edges_settings.LeftBorder = interface_repeater(lambda: int(input("Enter the left border: ")))()
                edges_settings.RightBorder = interface_repeater(lambda: int(input("Enter the right border: ")))()
            except Exception:
                print("Left border {0}, right border {1}".format(edges_settings.LeftBorder, edges_settings.RightBorder))
        self.axis.set_edges_settings(edges_settings)

    def ask_for_border_flags(self) -> None:
        res = ximc.BorderFlags(0)
        print("New settings:")
        for flag in ximc.BorderFlags:
            print("Set {}? Y/N".format(flag.name), end=" ")
            key_pressed = input()
            res |= (flag if key_pressed == "Y" or key_pressed == "y" else res)
        return res

    def ask_for_ender_flags(self) -> None:
        res = ximc.EnderFlags(0)
        for flag in ximc.EnderFlags:
            print("Set {}? Y/N".format(flag.name), end=" ")
            key_pressed = input()
            res |= (flag if key_pressed == "Y" or key_pressed == "y" else res)
        return res

    def change_microstep_mode(self) -> None:
        """Setting the microstep mode. Works only with stepper motors"""
        print("\nMicrostep mode settings. This setting is only available for stepper motors.")
        # Get current engine settings from controller
        engine_settings = self.axis.get_engine_settings()
        print("Current mode: {}".format(engine_settings.MicrostepMode))
        engine_settings.MicrostepMode = self.get_microstep_mode()
        self.axis.set_engine_settings(engine_settings)
        print("The mode is set to",  engine_settings.MicrostepMode)

    @interface_repeater
    def get_microstep_mode(self) -> ximc.MicrostepMode:
        print("Select microstep mode:")
        modes = [mode for mode in ximc.MicrostepMode]
        for i, mode in enumerate(modes, 1):
            print("To set mode {0} - enter {1}".format(mode, i))
        choosen_index = int(input()) - 1
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

    def start(self) -> None:
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
        for i, t in enumerate(types, 1):
            print("To set {0} - enter {1}".format(t.name, i))
        choosen_index = int(input("\nYour choice: ")) - 1
        if choosen_index < 0 or choosen_index >= len(types):
            raise ValueError("Wrong index!")
        return types[choosen_index]

    @interface_repeater
    def ask_for_feedback_flag(self) -> ximc.FeedbackFlags:
        flags = (ximc.FeedbackFlags.FEEDBACK_ENC_TYPE_AUTO,
                 ximc.FeedbackFlags.FEEDBACK_ENC_TYPE_DIFFERENTIAL,
                 ximc.FeedbackFlags.FEEDBACK_ENC_TYPE_SINGLE_ENDED)

        print("Select a new feedback flag:")
        for i, f in enumerate(flags, 1):
            print("To set {0} - enter {1}".format(f.name, i))
        choosen_index = int(input("\nYour choice: ")) - 1
        if choosen_index < 0 or choosen_index >= len(flags):
            raise ValueError("Wrong index!")

        key = input("Do you want to enable reverse? Y/N ")
        if key == "Y" or key == "y":
            return flags[choosen_index] | ximc.FeedbackFlags.FEEDBACK_ENC_REVERSE
        else:
            return flags[choosen_index]
