import libximc.highlevel as ximc
import os
import sys

print("//***************************************************************//")
print("// This example demonstrates loading a profile for a positioner. //")
print("//           The example uses the profile 8MT173-25-MEn1.        //")
print("//If you use a different positioner, these settings may break it.//")
print("//***************************************************************//")
print(" ")
confirm = input("To continue with the example, press y/n and press Enter: ")

if not (confirm in {"y", "yes", "Y", "Yes"}):
    exit()

# A compilation of the profile file
exec(compile(open('8MT173-25-MEn1.py').read(), '8MT173-25-MEn1', 'exec'))

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


if set_profile_8MT173_25_MEn1(lib, device_id) == Result.Ok:
    print("Download profile has been successfully completed.")
else:
    print("The profile was loaded with errors.")

print("\nClosing")
axis.close_device()
print("Done")

if flag_virtual == 1:
    print(" ")
    print("The real controller is not found or busy with another app.")
    print("The virtual controller is opened to check the operation of the library.")
    print("If you want to open a real controller, connect it or close the application that uses it.")
