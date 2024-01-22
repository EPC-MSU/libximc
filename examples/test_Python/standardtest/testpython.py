import libximc.highlevel as ximc
import time
import os
import sys


def test_status(axis: ximc.Axis) -> None:
    print("\nGet status")
    status = axis.get_status()
    print("Status.Ipwr: {}".format(status.Ipwr))
    print("Status.Upwr: {}".format(status.Upwr))
    print("Status.Iusb: {}".format(status.Iusb))
    print("Status.Flags: {}".format(status.Flags))


def test_get_position(axis: ximc.Axis) -> 'tuple':
    print("\nRead position")
    pos = axis.get_position()
    print("Position: {0} steps, {1} microsteps".format(pos.Position, pos.uPosition))
    return pos.Position, pos.uPosition


def test_left(axis: ximc.Axis) -> None:
    print("\nMoving left")
    axis.command_left()


def test_move(axis: ximc.Axis, distance: int, udistance: int) -> None:
    print("\nGoing to {0} steps, {1} microsteps".format(distance, udistance))
    axis.command_move(distance, udistance)


def test_wait_for_stop(axis: ximc.Axis, interval: int) -> None:
    print("\nWaiting for stop...")
    axis.command_wait_for_stop(interval)


def test_get_speed(axis: ximc.Axis) -> int:
    print("\nGet speed")
    move_settings = axis.get_move_settings()
    return move_settings.Speed


def test_set_speed(axis: ximc.Axis, speed: int) -> None:
    print("\nSet speed")
    move_settings = axis.get_move_settings()
    print("The speed was equal to {0}. We will change it to {1}".format(move_settings.Speed, speed))
    move_settings.Speed = speed
    axis.set_move_settings(move_settings)


def test_set_microstep_mode_256(axis: ximc.Axis) -> None:
    print("\nSet microstep mode to 256")
    engine_settings = axis.get_engine_settings()

    # Change MicrostepMode parameter to MICROSTEP_MODE_FRAC_256
    # (use MICROSTEP_MODE_FRAC_128, MICROSTEP_MODE_FRAC_64 ... for other microstep modes)
    engine_settings.MicrostepMode = ximc.MicrostepMode.MICROSTEP_MODE_FRAC_256

    axis.set_engine_settings(engine_settings)


print("Library version: " + ximc.ximc_version())

# ******************************************** #
#               Device searching               #
# ******************************************** #

# Flags explanation:
# ximc.EnumerateFlags.ENUMERATE_PROBE   -   Probing found devices for detailed info.
# ximc.EnumerateFlags.ENUMERATE_NETWORK -   Check network devices.
enum_flags = ximc.EnumerateFlags.ENUMERATE_PROBE | ximc.EnumerateFlags.ENUMERATE_NETWORK

# Hint explanation:
# "addr=" hint is used for broadcast network enumeration
enum_hints = "addr="
devenum = ximc.enumerate_devices(enum_flags, enum_hints)
print("Device count: {}".format(len(devenum)))
print("Found devices:\n", devenum)

flag_virtual = 0

open_name = None
if len(sys.argv) > 1:
    open_name = sys.argv[1]
elif len(devenum) > 0:
    open_name = devenum[0]["uri"]
else:
    # set path to virtual device file to be created
    tempdir = os.path.join(os.path.expanduser('~'), "testdevice.bin")
    open_name = "xi-emu:///" + tempdir
    flag_virtual = 1
    print("The real controller is not found or busy with another app.")
    print("The virtual controller is opened to check the operation of the library.")
    print("If you want to open a real controller, connect it or close the application that uses it.")


# ******************************************** #
#              Create axis object              #
# ******************************************** #
# Axis is the main libximc.highlevel class. It allows you to interact with the device.
# Axis takes one argument - URI of the device
axis = ximc.Axis(open_name)
print("\nOpen device " + axis.uri)
axis.open_device()  # The connection must be opened manually


# ******************************************* #
#                    Tests                    #
# ******************************************* #
test_status(axis)
test_set_microstep_mode_256(axis)
start_pos, ustart_pos = test_get_position(axis)
# First move
test_left(axis)
time.sleep(3)
test_get_position(axis)
# Second move
current_speed = test_get_speed(axis)
test_set_speed(axis, current_speed // 2)
test_move(axis, start_pos, ustart_pos)
test_wait_for_stop(axis, 100)
test_status(axis)

print("\nClosing")
axis.close_device()
print("Done")

if flag_virtual == 1:
    print(" ")
    print("The real controller is not found or busy with another app.")
    print("The virtual controller is opened to check the operation of the library.")
    print("If you want to open a real controller, connect it or close the application that uses it.")
