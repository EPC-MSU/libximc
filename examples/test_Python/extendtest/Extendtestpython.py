"""This module is an extended example of using the libximc library to control 8SMC series using the Python language"""
import os
import platform
from enum import Enum
from support_routines import interface_repeater
from extio_manager import EXTIOManager
from movement_manager import MovementManager, MovementManagerCalb
from settings_manager import SettingsManager
import libximc.highlevel as ximc


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
        device_type = self.ask_for_device_type()
        if device_type == SelectionManager.DeviceType.COM_DEVICE:
            uri = self.ask_for_com_uri()
        elif device_type == SelectionManager.DeviceType.VIRT_DEVICE:
            uri = self.get_virt_uri()
        elif device_type == SelectionManager.DeviceType.NETWORK_DEVICE:
            uri = self.ask_for_network_uri()
        elif device_type == SelectionManager.DeviceType.ALL_DEVICES:
            devenum = self.get_devices_enumeration()

            if len(devenum) > 0:
                index = self.ask_for_device_index(devenum)
                uri = devenum[index]["uri"]
            else:
                # set path to virtual device file to be created
                tempdir = os.path.join(os.path.expanduser('~'), "testdevice.bin")
                uri = "xi-emu:///" + tempdir
        else:
            raise RuntimeError("Wrong device type! Got {}".format(device_type))
        return uri

    @interface_repeater
    def ask_for_device_type(self) -> DeviceType:
        print("What XIMC device do you want to open?\n"
              "Enter the key:\n"
              "1 - for COM device\n"
              "2 - for virtual device\n"
              "3 - network device\n"
              "4 - search for all available devices.\n")
        key = int(input("Your choice: "))
        return SelectionManager.DeviceType(key)

    def ask_for_com_uri(self) -> str:
        if platform.system() == "Windows":
            print(r"Enter the port number:")
            uri = r"xi-com:\\.\COM" + input(r"xi-com:\\.\COM")
        else:
            print("Enter the port number:")
            uri = "xi-com:/dev/tty.s" + input("xi-com:/dev/tty.s")
        return uri

    def get_virt_uri(self) -> str:
        return "xi-emu:///" + os.path.join(os.path.expanduser('~'), "virtual_controller.bin")

    def ask_for_network_uri(self) -> str:
        print("Enter the device's network address:")
        print("Example: 192.168.0.1/89ABCDEF, where 192.168.0.1 is an IP of the device and 89ABCDEF "
              "is a serial number.")
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
    def ask_for_device_index(self, devenum: 'list[dict]') -> int:
        for i, dev in enumerate(devenum, 1):
            print("#{} - {}, {}, SN{}: ".format(i, dev["ControllerName"], dev["uri"], dev["device_serial"]))
        print("Enter the device number:")
        index = int(input()) - 1
        if index >= len(devenum) or index < 0:
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
        action = self.ask_for_action()
        while action != GeneralManager.Action.QUIT:
            if action == GeneralManager.Action.MOVE:
                self.move_manager.start()
            if action == GeneralManager.Action.MOVE_CALB:
                self.move_manage_calb.start()
            elif action == GeneralManager.Action.EXTIO:
                self.extio_manager.start()
            elif action == GeneralManager.Action.CHANGE_SETTINGS:
                self.settings_manager.start()
            action = self.ask_for_action()
        print("Exiting initialized...")

    @interface_repeater
    def ask_for_action(self) -> Action:
        print("\n===== Main menu =====\n"
              "Choose action:\n"
              "Q or q keys\t-\texit\n"
              "M or m key\t-\tmove\n"
              "C or c key\t-\tmove (user-units)\n"
              "I or i keys\t-\texternal I/O EXTIO\n"
              "S or s keys\t-\tchange settings\n")
        key = input("Your choice: ")
        return GeneralManager.Action(key.lower())


axis: ximc.Axis = None


def main():
    """
    Starts Selection Manager and General Manager.
    """
    global axis

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

    print("\nClosing device connection... ", end="")
    axis.close_device()
    print("Done!")
    print("Exiting...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting initialized...")
        print("Powering off the device's windings... ", end="")
        axis.command_power_off()
        print("Done!")
        print("Exit program...")
