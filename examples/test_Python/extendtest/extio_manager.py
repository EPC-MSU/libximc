from enum import Enum
from support_routines import interface_repeater
import libximc.highlevel as ximc


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

            flag = self.get_output_flag()
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
              "Choose flag:\n"
              "1 - EXTIO_SETUP_MODE_IN_STOP\n"
              "2 - EXTIO_SETUP_MODE_IN_PWOF\n"
              "3 - EXTIO_SETUP_MODE_IN_MOVR\n"
              "4 - EXTIO_SETUP_MODE_IN_HOME\n"
              "5 - EXTIO_SETUP_MODE_IN_ALARM\n")
        return EXTIOManager.InputFlag(int(input("Your choice: ")))

    @interface_repeater
    def get_output_flag(self) -> OutputFlag:
        print("Set EXTIO output mode.\n"
              "Choose flag:\n"
              "1 - EXTIO_SETUP_MODE_OUT_MOVING\n"
              "2 - EXTIO_SETUP_MODE_OUT_ALARM\n"
              "3 - EXTIO_SETUP_MODE_OUT_MOTOR_ON\n")
        return EXTIOManager.OutputFlag(int(input("Your choice: ")))

    @interface_repeater
    def get_direction(self) -> Direction:
        print("Use output as input or output?\n"
              "Choose mode:\n"
              "I or i keys - input\n"
              "O or o keys - output\n"
              "R or r keys - inverted output\n")
        return EXTIOManager.Direction(input("Your choice: ").lower())
