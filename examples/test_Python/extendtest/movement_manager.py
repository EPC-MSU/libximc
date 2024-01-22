from abc import ABC
from enum import Enum
from time import sleep
from support_routines import interface_repeater
import libximc.highlevel as ximc


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
        action = self.ask_for_action()
        while action != MovementManager.Action.QUIT:
            if action == MovementManager.Action.MOVE:
                print("Moving to position...")
                self.move(*self.ask_for_position())
                self.verbose_wait_for_stop(100)

            elif action == MovementManager.Action.SHIFT:
                print("Shifting on position delta...")
                self.movr(*self.get_delta_position())
                self.verbose_wait_for_stop(100)

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
                self.verbose_wait_for_stop(100)

            elif action == MovementManager.Action.ZERO:
                print("Zeroing...")
                self.axis.command_zero()

            print("Waiting for movement completion...")
            self.axis.command_wait_for_stop(100)
            action = self.ask_for_action()

    @interface_repeater
    def ask_for_action(self) -> Action:
        print("\n===== Movement menu =====\n"
              "Choose movement:\n"
              "Q or q keys\t-\treturn to the main menu\n"
              "L or l keys\t-\tmove to the left\n"
              "R or r keys\t-\tmove to the right. Press and hold the key\n"
              "M or m keys\t-\tmove to position(mov)\n"
              "S or s keys\t-\tposition shift(movr)\n"
              "H or h keys\t-\tHOME position\n"
              "Z or z keys\t-\tZERO position\n")
        key = input("Your choice: ")
        return MovementManagerBase.Action(key.lower())

    def move(self, *args) -> None:
        pass

    def movr(self, *args) -> None:
        pass

    def ask_for_position(self):
        pass

    def get_delta_position(self):
        pass

    def verbose_wait_for_stop(self, refresh_interval_ms):
        pass


class MovementManager(MovementManagerBase):
    @interface_repeater
    def ask_for_position(self) -> "tuple":
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

    def move(self, *args) -> None:
        self.axis.command_move(*args)

    def movr(self, *args) -> None:
        self.axis.command_movr(*args)

    def verbose_wait_for_stop(self, refresh_interval_ms: int) -> None:
        """This function performs dynamic output coordinate in the process of moving."""
        while self.axis.get_status().MvCmdSts & ximc.MvcmdStatus.MVCMD_RUNNING:
            position = self.axis.get_position()
            print("Position: {} steps {} microsteps".format(position.Position, position.uPosition))
            sleep(refresh_interval_ms / 1000)
        position = self.axis.get_position()
        print("Position: {} steps {} microsteps".format(position.Position, position.uPosition))


class MovementManagerCalb(MovementManagerBase):
    @interface_repeater
    def ask_for_position(self) -> float:
        print("Enter target position.")
        position = float(input("Target position: "))
        return (position, )

    @interface_repeater
    def get_delta_position(self) -> float:
        print("Enter position delta.")
        delta = float(input("Position delta: "))
        return (delta, )

    def move(self, *args) -> None:
        self.axis.command_move_calb(*args)

    def movr(self, *args) -> None:
        self.axis.command_movr_calb(*args)

    def verbose_wait_for_stop(self, refresh_interval_ms: int) -> None:
        """This function performs dynamic output coordinate in the process of moving."""
        while self.axis.get_status().MvCmdSts & ximc.MvcmdStatus.MVCMD_RUNNING:
            position = self.axis.get_position_calb()
            print("Position: {}".format(position.Position))
            sleep(refresh_interval_ms / 1000)
        position = self.axis.get_position_calb()
        print("Position: {}".format(position.Position))
