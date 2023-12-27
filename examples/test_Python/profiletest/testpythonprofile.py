from ctypes import *
import time
import os
import sys
import platform
import tempfile
import re

if sys.version_info >= (3,0):
    import urllib.parse

print("//***************************************************************//")
print("// This example demonstrates loading a profile for a positioner. //")
print("//           The example uses the profile 8MT173-25-MEn1.        //")
print("//If you use a different positioner, these settings may break it.//")
print("//***************************************************************//")
print(" ")
confirm = input("To continue with the example, press y/n and press Enter: ")

if not(confirm in {"y", "yes", "Y", "Yes"}):
    exit()

# Dependences
    
# For correct usage of the library libximc,
# you need to add the file pyximc.py wrapper with the structures of the library to python path.
cur_dir = os.path.abspath(os.path.dirname(__file__)) # Specifies the current directory.
ximc_dir = os.path.join(cur_dir, "..", "..", "..", "ximc") # Formation of the directory name with all dependencies. The dependencies for the examples are located in the ximc directory.
ximc_package_dir = os.path.join(ximc_dir, "crossplatform", "wrappers", "python") # Formation of the directory name with python dependencies.
sys.path.append(ximc_package_dir)  # add pyximc.py wrapper to python path

try: 
    from libximc import *
except ImportError as err:
    print ("Can't import libximc module. The most probable reason is that you changed the relative location of the test_Python.py and libximc module. See developers' documentation for details.")
    exit()
except OSError as err:
    if platform.system() == "Windows":
        if err.winerror == 193:   # The bit depth of one of the libraries bindy.dll, libximc.dll, xiwrapper.dll does not correspond to the operating system bit.
            print("Err: The bit depth of one of the libraries bindy.dll, libximc.dll, xiwrapper.dll does not correspond to the operating system bit.")
        elif err.winerror == 126: # One of the library bindy.dll, libximc.dll, xiwrapper.dll files is missing.
            print("Err: One of the library bindy.dll, libximc.dll, xiwrapper.dll is missing.")
        else:           # Other errors the value of which can be viewed in the code.
            print(err)
        print("Warning: If you are using the example as the basis for your module, make sure that the dependencies installed in the dependencies section of the example match your directory structure.")
    else:
        print(err)
        print ("Can't load libximc library. Please add all shared libraries to the appropriate places. It is described in detail in developers' documentation. On Linux make sure you installed libximc-dev package.\nmake sure that the architecture of the system and the interpreter is the same")
    exit()

# A compilation of the profile file
exec(compile(open('8MT173-25-MEn1.py').read(), '8MT173-25-MEn1', 'exec'))

# variable 'lib' points to a loaded library
# note that ximc uses stdcall on win
print("Library loaded")

sbuf = create_string_buffer(64)
lib.ximc_version(sbuf)
print("Library version: " + sbuf.raw.decode().rstrip("\0"))

# This is device search and enumeration with probing. It gives more information about devices.
probe_flags = EnumerateFlags.ENUMERATE_NETWORK#EnumerateFlags.ENUMERATE_PROBE + EnumerateFlags.ENUMERATE_NETWORK
enum_hints = b"addr="
# enum_hints = b"addr=" # Use this hint string for broadcast enumerate
devenum = lib.enumerate_devices(probe_flags, enum_hints)
print("Device enum handle: " + repr(devenum))
print("Device enum handle type: " + repr(type(devenum)))

dev_count = lib.get_device_count(devenum)
print("Device count: " + repr(dev_count))

controller_name = controller_name_t()
for dev_ind in range(0, dev_count):
    enum_name = lib.get_device_name(devenum, dev_ind)
    #result = lib.get_enumerate_device_controller_name(devenum, dev_ind, byref(controller_name))
    if result == Result.Ok:
        print("Enumerated device #{} name (port name): ".format(dev_ind) + repr(enum_name) + ". Friendly name: ")# + repr(controller_name.ControllerName) + ".")

flag_virtual = 0

open_name = -1
open_name = lib.get_device_name(devenum, 0)
if len(sys.argv) > 1:
    open_name = sys.argv[1]
elif dev_count > 0:
    open_name = lib.get_device_name(devenum, 0)
elif sys.version_info >= (3,0):
    # use URI for virtual device when there is new urllib python3 API
    tempdir = os.path.expanduser('~') + "/testdevice.bin"
    if os.altsep:
        tempdir = tempdir.replace(os.sep, os.altsep)
    # urlparse build wrong path if scheme is not file
    uri = urllib.parse.urlunparse(urllib.parse.ParseResult(scheme="file", \
            netloc=None, path=tempdir, params=None, query=None, fragment=None))
    open_name = re.sub(r'^file', 'xi-emu', uri).encode()
    flag_virtual = 1
    print("The real controller is not found or busy with another app.")
    print("The virtual controller is opened to check the operation of the library.")
    print("If you want to open a real controller, connect it or close the application that uses it.")

if not open_name:
    exit(1)

if type(open_name) is str:
    open_name = open_name.encode()

print("\nOpen device " + repr(open_name))
device_id = lib.open_device(open_name)
print("Device id: " + repr(device_id))

if set_profile_8MT173_25_MEn1(lib, device_id) == Result.Ok:
    print("Download profile has been successfully completed.")
else:
    print("The profile was loaded with errors.")

print("\nClosing")

# The device_t device parameter in this function is a C pointer, unlike most library functions that use this parameter
lib.close_device(byref(cast(device_id, POINTER(c_int))))
print("Done")

if flag_virtual == 1:
    print(" ")
    print("The real controller is not found or busy with another app.")
    print("The virtual controller is opened to check the operation of the library.")
    print("If you want to open a real controller, connect it or close the application that uses it.")
