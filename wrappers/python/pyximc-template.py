#!/usr/bin/python
import os
import platform
from ctypes import CDLL, RTLD_GLOBAL, POINTER, byref, cast
if platform.system() == "Windows":
    from ctypes import WinDLL
from ctypes import (c_double, c_int, c_uint, c_uint8, c_uint32,
                    c_ulonglong, c_float, c_char, c_char_p, c_long,
                    c_longlong, c_ubyte)
from ctypes import Structure, LittleEndianStructure
import struct
import sys


print("WARNING: This binding version is an experimental one! Use with caution.")


def _load_for_win():
    if 8 * struct.calcsize("P") == 32:
        lib_dir = "." + os.sep + "win32"
    else:
        lib_dir = "." + os.sep + "win64"

    error_messages = []
    for path_to_search in (lib_dir, os.path.abspath("")):
        try:
            if sys.version_info[0] == 3 and sys.version_info[1] >= 8:
                WinDLL(path_to_search + os.sep + "bindy.dll",
                       winmode=RTLD_GLOBAL)
                WinDLL(path_to_search + os.sep + "xiwrapper",
                       winmode=RTLD_GLOBAL)
                libximc = WinDLL(path_to_search + os.sep + "libximc.dll",
                                 winmode=RTLD_GLOBAL)
            else:
                WinDLL(path_to_search + os.sep + "bindy.dll")
                WinDLL(path_to_search + os.sep + "xiwrapper")
                libximc = WinDLL(path_to_search + os.sep + "libximc.dll")
        except Exception:
            error_messages.append("Searched in {}".format(path_to_search))
        else:
            return libximc
    raise RuntimeError(
                    "Unable to load at least one of libraries:"
                    "libximc.dll, xiwrapper.dll, bindy.dll.\n{}."
                    .format("\n".join(error_messages))
                )


def _load_for_linux():
    cpu_kind = platform.machine().lower()
    if cpu_kind == "arm":
        cpu_path = "." + os.sep + "debian-armhf"
    elif cpu_kind == "i386":
        cpu_path = "." + os.sep + "debian-i386"
    else:
        cpu_path = "." + os.sep + "debian-amd64"
    print("Type of CPU detected: ", cpu_kind)

    error_messages = []
    for path_to_search in (cpu_path, os.path.abspath("")):
        try:
            CDLL(path_to_search + os.sep + "libbindy.so")
            CDLL(path_to_search + os.sep + "libxiwrapper.so")
            libximc = CDLL(path_to_search + os.sep + "libximc.so")
        except Exception:
            error_messages.append("Searched in {}".format(path_to_search))
        else:
            return libximc
    raise RuntimeError(
                    "Unable to load at least one of libraries:"
                    "libximc.so, libxiwrapper.so, libbindy.so.\n{}."
                    .format("\n".join(error_messages))
                )


def _load_for_darwin():
    try:
        CDLL("macosx/libjximc.dylib")
        libximc = CDLL("libximc.framework/libximc")
    except Exception as exc:
        raise RuntimeError(
                "Unable to load ./macosx/libjximc.dylib."
                "\n\nAdditional error messages: {}"
                .format(str(exc))
            )
    return libximc


def load_libximc():
    """Returns an object of libximc library

    :raises RuntimeError: In case of inability to load the lib or its
    dependencies: bindy and xiwrapper.
    """
    os_kind = platform.system().lower()
    # Please note! lib sequence is matter! First - bindy, second - wrapper,
    # third - libximc. Thank you for your attention
    if os_kind == "windows":
        libximc = _load_for_win()
    elif os_kind == "linux":
        libximc = _load_for_linux()
    elif os_kind == "darwin":
        libximc = _load_for_darwin()
    else:
        raise RuntimeError("Unexpected OS: {}".format(os_kind))
    return libximc


lib = load_libximc()


# Common declarations
class Result:
    Ok = 0
    Error = -1
    NotImplemented = -2
    ValueError = -3
    NoDevice = -4


class calibration_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('A', c_double),
        ('MicrostepMode', c_uint)
    ]


class device_enumeration_t(LittleEndianStructure):
    pass


class device_network_information_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('ipv4', c_uint32),
        ('nodename', c_char * 16),
        ('axis_state', c_uint),
        ('locker_username', c_char * 16),
        ('locker_nodename', c_char * 16),
        ('locked_time', c_ulonglong),
    ]


# Clarify function types
lib.enumerate_devices.restype = POINTER(device_enumeration_t)
lib.get_device_name.restype = c_char_p

# ------------------ API v1 ------------------
# @@GENERATED_CODE@@


# ------------------ API v2 ------------------
# --- Public API v2 data types starts here ---
DeviceT = int

# -------- Internal utility functions --------


def _check_device_id(device_id: DeviceT) -> None:
    try:
        id_int = int(device_id)
    except ValueError:
        raise ValueError("device_id should be integer, got device_id="
                         "{} of type {}".format(device_id, type(device_id)))

    if id_int < 0:
        raise ValueError("Got negative device_id ({}). It seems the device was"
                         " not opened correctly".format(device_id))


def _check_result(result: int) -> None:
    if result == Result.Ok:
        return
    if result == Result.Error:
        raise RuntimeError("General Error")

    if result == Result.NotImplemented:
        raise NotImplementedError(
            "This function is not implemented in the device."
            "Firmware update may be required: "
            "https://doc.xisupport.com/en/8smc5-usb/8SMCn-USB/"
            "XILab_application_Users_guide/Controller_Settings/"
            "About_controller.html"
        )

    if result == Result.ValueError:
        raise ValueError(
            "The input was rejected by device. Some parameters may have "
            "incorrect values."
            "Check documentation: "
            "https://libximc.xisupport.com/doc-en/ximc_8h.html"
        )

    if result == Result.NoDevice:
        raise ConnectionError(
            "Cannot send command to the device. Check connection and power. "
            "The device_id is invalid. To resume operation you should reopen"
            " the device."
        )


def _check_castability(val, cast_type, varname):
    try:
        cast_type(val)
    except Exception:
        raise TypeError("Unable to cast {} to {}".format(varname, cast_type))
# -------- Public API v2 data classes --------
# -*- coding: utf-8 -*-


class Calibration:

    def __init__(
            self,
            A,
            MicrostepMode):

        self.A = A
        self.MicrostepMode = MicrostepMode

    # getters
    @property
    def A(self):
        return self._A

    @property
    def MicrostepMode(self):
        return self._MicrostepMode

    # setters
    @A.setter
    def A(self, val):
        _check_castability(val,
                           c_double,
                           varname="A")
        self._A = val

    @MicrostepMode.setter
    def MicrostepMode(self, val):
        _check_castability(val,
                           c_uint,
                           varname="MicrostepMode")
        self._MicrostepMode = val


class DeviceNetworkInformation:

    def __init__(
            self,
            ipv4,
            nodename,
            axis_state,
            locker_username,
            locker_nodename,
            locked_time):

        self.ipv4 = ipv4
        self.nodename = nodename
        self.axis_state = axis_state
        self.locker_username = locker_username
        self.locker_nodename = locker_nodename
        self.locked_time = locked_time

    # getters
    @property
    def ipv4(self):
        return self._ipv4

    @property
    def nodename(self):
        return self._nodename

    @property
    def axis_state(self):
        return self._axis_state

    @property
    def locker_username(self):
        return self._locker_username

    @property
    def locker_nodename(self):
        return self._locker_nodename

    @property
    def locked_time(self):
        return self._locked_time

    # setters
    @ipv4.setter
    def ipv4(self, val):
        _check_castability(val,
                           c_uint32,
                           varname="ipv4")
        self._ipv4 = val

    @nodename.setter
    def nodename(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="nodename")
        self._nodename = val

    @axis_state.setter
    def axis_state(self, val):
        _check_castability(val,
                           c_uint32,
                           varname="axis_state")
        self._axis_state = val

    @locker_username.setter
    def locker_username(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="locker_username")
        self._locker_username = val

    @locker_nodename.setter
    def locker_nodename(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="locker_nodename")
        self._locker_nodename = val

    @locked_time.setter
    def locked_time(self, val):
        _check_castability(val,
                           c_int,
                           varname="locked_time")
        self._locked_time = val


class FeedbackSettings:

    def __init__(
            self,
            IPS,
            FeedbackType,
            FeedbackFlags,
            CountsPerTurn):

        self.IPS = IPS
        self.FeedbackType = FeedbackType
        self.FeedbackFlags = FeedbackFlags
        self.CountsPerTurn = CountsPerTurn

    # getters
    @property
    def IPS(self):
        return self._IPS

    @property
    def FeedbackType(self):
        return self._FeedbackType

    @property
    def FeedbackFlags(self):
        return self._FeedbackFlags

    @property
    def CountsPerTurn(self):
        return self._CountsPerTurn

    # setters
    @IPS.setter
    def IPS(self, val):
        _check_castability(val,
                           c_uint,
                           varname="IPS")
        self._IPS = val

    @FeedbackType.setter
    def FeedbackType(self, val):
        _check_castability(val,
                           c_uint,
                           varname="FeedbackType")
        self._FeedbackType = val

    @FeedbackFlags.setter
    def FeedbackFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="FeedbackFlags")
        self._FeedbackFlags = val

    @CountsPerTurn.setter
    def CountsPerTurn(self, val):
        _check_castability(val,
                           c_uint,
                           varname="CountsPerTurn")
        self._CountsPerTurn = val


class HomeSettings:

    def __init__(
            self,
            FastHome,
            uFastHome,
            SlowHome,
            uSlowHome,
            HomeDelta,
            uHomeDelta,
            HomeFlags):

        self.FastHome = FastHome
        self.uFastHome = uFastHome
        self.SlowHome = SlowHome
        self.uSlowHome = uSlowHome
        self.HomeDelta = HomeDelta
        self.uHomeDelta = uHomeDelta
        self.HomeFlags = HomeFlags

    # getters
    @property
    def FastHome(self):
        return self._FastHome

    @property
    def uFastHome(self):
        return self._uFastHome

    @property
    def SlowHome(self):
        return self._SlowHome

    @property
    def uSlowHome(self):
        return self._uSlowHome

    @property
    def HomeDelta(self):
        return self._HomeDelta

    @property
    def uHomeDelta(self):
        return self._uHomeDelta

    @property
    def HomeFlags(self):
        return self._HomeFlags

    # setters
    @FastHome.setter
    def FastHome(self, val):
        _check_castability(val,
                           c_uint,
                           varname="FastHome")
        self._FastHome = val

    @uFastHome.setter
    def uFastHome(self, val):
        _check_castability(val,
                           c_uint,
                           varname="uFastHome")
        self._uFastHome = val

    @SlowHome.setter
    def SlowHome(self, val):
        _check_castability(val,
                           c_uint,
                           varname="SlowHome")
        self._SlowHome = val

    @uSlowHome.setter
    def uSlowHome(self, val):
        _check_castability(val,
                           c_uint,
                           varname="uSlowHome")
        self._uSlowHome = val

    @HomeDelta.setter
    def HomeDelta(self, val):
        _check_castability(val,
                           c_int,
                           varname="HomeDelta")
        self._HomeDelta = val

    @uHomeDelta.setter
    def uHomeDelta(self, val):
        _check_castability(val,
                           c_int,
                           varname="uHomeDelta")
        self._uHomeDelta = val

    @HomeFlags.setter
    def HomeFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="HomeFlags")
        self._HomeFlags = val


class HomeSettingsCalb:

    def __init__(
            self,
            FastHome,
            SlowHome,
            HomeDelta,
            HomeFlags):

        self.FastHome = FastHome
        self.SlowHome = SlowHome
        self.HomeDelta = HomeDelta
        self.HomeFlags = HomeFlags

    # getters
    @property
    def FastHome(self):
        return self._FastHome

    @property
    def SlowHome(self):
        return self._SlowHome

    @property
    def HomeDelta(self):
        return self._HomeDelta

    @property
    def HomeFlags(self):
        return self._HomeFlags

    # setters
    @FastHome.setter
    def FastHome(self, val):
        _check_castability(val,
                           c_float,
                           varname="FastHome")
        self._FastHome = val

    @SlowHome.setter
    def SlowHome(self, val):
        _check_castability(val,
                           c_float,
                           varname="SlowHome")
        self._SlowHome = val

    @HomeDelta.setter
    def HomeDelta(self, val):
        _check_castability(val,
                           c_float,
                           varname="HomeDelta")
        self._HomeDelta = val

    @HomeFlags.setter
    def HomeFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="HomeFlags")
        self._HomeFlags = val


class MoveSettings:

    def __init__(
            self,
            Speed,
            uSpeed,
            Accel,
            Decel,
            AntiplaySpeed,
            uAntiplaySpeed,
            MoveFlags):

        self.Speed = Speed
        self.uSpeed = uSpeed
        self.Accel = Accel
        self.Decel = Decel
        self.AntiplaySpeed = AntiplaySpeed
        self.uAntiplaySpeed = uAntiplaySpeed
        self.MoveFlags = MoveFlags

    # getters
    @property
    def Speed(self):
        return self._Speed

    @property
    def uSpeed(self):
        return self._uSpeed

    @property
    def Accel(self):
        return self._Accel

    @property
    def Decel(self):
        return self._Decel

    @property
    def AntiplaySpeed(self):
        return self._AntiplaySpeed

    @property
    def uAntiplaySpeed(self):
        return self._uAntiplaySpeed

    @property
    def MoveFlags(self):
        return self._MoveFlags

    # setters
    @Speed.setter
    def Speed(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Speed")
        self._Speed = val

    @uSpeed.setter
    def uSpeed(self, val):
        _check_castability(val,
                           c_uint,
                           varname="uSpeed")
        self._uSpeed = val

    @Accel.setter
    def Accel(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Accel")
        self._Accel = val

    @Decel.setter
    def Decel(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Decel")
        self._Decel = val

    @AntiplaySpeed.setter
    def AntiplaySpeed(self, val):
        _check_castability(val,
                           c_uint,
                           varname="AntiplaySpeed")
        self._AntiplaySpeed = val

    @uAntiplaySpeed.setter
    def uAntiplaySpeed(self, val):
        _check_castability(val,
                           c_uint,
                           varname="uAntiplaySpeed")
        self._uAntiplaySpeed = val

    @MoveFlags.setter
    def MoveFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="MoveFlags")
        self._MoveFlags = val


class MoveSettingsCalb:

    def __init__(
            self,
            Speed,
            Accel,
            Decel,
            AntiplaySpeed,
            MoveFlags):

        self.Speed = Speed
        self.Accel = Accel
        self.Decel = Decel
        self.AntiplaySpeed = AntiplaySpeed
        self.MoveFlags = MoveFlags

    # getters
    @property
    def Speed(self):
        return self._Speed

    @property
    def Accel(self):
        return self._Accel

    @property
    def Decel(self):
        return self._Decel

    @property
    def AntiplaySpeed(self):
        return self._AntiplaySpeed

    @property
    def MoveFlags(self):
        return self._MoveFlags

    # setters
    @Speed.setter
    def Speed(self, val):
        _check_castability(val,
                           c_float,
                           varname="Speed")
        self._Speed = val

    @Accel.setter
    def Accel(self, val):
        _check_castability(val,
                           c_float,
                           varname="Accel")
        self._Accel = val

    @Decel.setter
    def Decel(self, val):
        _check_castability(val,
                           c_float,
                           varname="Decel")
        self._Decel = val

    @AntiplaySpeed.setter
    def AntiplaySpeed(self, val):
        _check_castability(val,
                           c_float,
                           varname="AntiplaySpeed")
        self._AntiplaySpeed = val

    @MoveFlags.setter
    def MoveFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="MoveFlags")
        self._MoveFlags = val


class EngineSettings:

    def __init__(
            self,
            NomVoltage,
            NomCurrent,
            NomSpeed,
            uNomSpeed,
            EngineFlags,
            Antiplay,
            MicrostepMode,
            StepsPerRev):

        self.NomVoltage = NomVoltage
        self.NomCurrent = NomCurrent
        self.NomSpeed = NomSpeed
        self.uNomSpeed = uNomSpeed
        self.EngineFlags = EngineFlags
        self.Antiplay = Antiplay
        self.MicrostepMode = MicrostepMode
        self.StepsPerRev = StepsPerRev

    # getters
    @property
    def NomVoltage(self):
        return self._NomVoltage

    @property
    def NomCurrent(self):
        return self._NomCurrent

    @property
    def NomSpeed(self):
        return self._NomSpeed

    @property
    def uNomSpeed(self):
        return self._uNomSpeed

    @property
    def EngineFlags(self):
        return self._EngineFlags

    @property
    def Antiplay(self):
        return self._Antiplay

    @property
    def MicrostepMode(self):
        return self._MicrostepMode

    @property
    def StepsPerRev(self):
        return self._StepsPerRev

    # setters
    @NomVoltage.setter
    def NomVoltage(self, val):
        _check_castability(val,
                           c_uint,
                           varname="NomVoltage")
        self._NomVoltage = val

    @NomCurrent.setter
    def NomCurrent(self, val):
        _check_castability(val,
                           c_uint,
                           varname="NomCurrent")
        self._NomCurrent = val

    @NomSpeed.setter
    def NomSpeed(self, val):
        _check_castability(val,
                           c_uint,
                           varname="NomSpeed")
        self._NomSpeed = val

    @uNomSpeed.setter
    def uNomSpeed(self, val):
        _check_castability(val,
                           c_uint,
                           varname="uNomSpeed")
        self._uNomSpeed = val

    @EngineFlags.setter
    def EngineFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="EngineFlags")
        self._EngineFlags = val

    @Antiplay.setter
    def Antiplay(self, val):
        _check_castability(val,
                           c_int,
                           varname="Antiplay")
        self._Antiplay = val

    @MicrostepMode.setter
    def MicrostepMode(self, val):
        _check_castability(val,
                           c_uint,
                           varname="MicrostepMode")
        self._MicrostepMode = val

    @StepsPerRev.setter
    def StepsPerRev(self, val):
        _check_castability(val,
                           c_uint,
                           varname="StepsPerRev")
        self._StepsPerRev = val


class EngineSettingsCalb:

    def __init__(
            self,
            NomVoltage,
            NomCurrent,
            NomSpeed,
            EngineFlags,
            Antiplay,
            MicrostepMode,
            StepsPerRev):

        self.NomVoltage = NomVoltage
        self.NomCurrent = NomCurrent
        self.NomSpeed = NomSpeed
        self.EngineFlags = EngineFlags
        self.Antiplay = Antiplay
        self.MicrostepMode = MicrostepMode
        self.StepsPerRev = StepsPerRev

    # getters
    @property
    def NomVoltage(self):
        return self._NomVoltage

    @property
    def NomCurrent(self):
        return self._NomCurrent

    @property
    def NomSpeed(self):
        return self._NomSpeed

    @property
    def EngineFlags(self):
        return self._EngineFlags

    @property
    def Antiplay(self):
        return self._Antiplay

    @property
    def MicrostepMode(self):
        return self._MicrostepMode

    @property
    def StepsPerRev(self):
        return self._StepsPerRev

    # setters
    @NomVoltage.setter
    def NomVoltage(self, val):
        _check_castability(val,
                           c_uint,
                           varname="NomVoltage")
        self._NomVoltage = val

    @NomCurrent.setter
    def NomCurrent(self, val):
        _check_castability(val,
                           c_uint,
                           varname="NomCurrent")
        self._NomCurrent = val

    @NomSpeed.setter
    def NomSpeed(self, val):
        _check_castability(val,
                           c_float,
                           varname="NomSpeed")
        self._NomSpeed = val

    @EngineFlags.setter
    def EngineFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="EngineFlags")
        self._EngineFlags = val

    @Antiplay.setter
    def Antiplay(self, val):
        _check_castability(val,
                           c_float,
                           varname="Antiplay")
        self._Antiplay = val

    @MicrostepMode.setter
    def MicrostepMode(self, val):
        _check_castability(val,
                           c_uint,
                           varname="MicrostepMode")
        self._MicrostepMode = val

    @StepsPerRev.setter
    def StepsPerRev(self, val):
        _check_castability(val,
                           c_uint,
                           varname="StepsPerRev")
        self._StepsPerRev = val


class EntypeSettings:

    def __init__(
            self,
            EngineType,
            DriverType):

        self.EngineType = EngineType
        self.DriverType = DriverType

    # getters
    @property
    def EngineType(self):
        return self._EngineType

    @property
    def DriverType(self):
        return self._DriverType

    # setters
    @EngineType.setter
    def EngineType(self, val):
        _check_castability(val,
                           c_uint,
                           varname="EngineType")
        self._EngineType = val

    @DriverType.setter
    def DriverType(self, val):
        _check_castability(val,
                           c_uint,
                           varname="DriverType")
        self._DriverType = val


class PowerSettings:

    def __init__(
            self,
            HoldCurrent,
            CurrReductDelay,
            PowerOffDelay,
            CurrentSetTime,
            PowerFlags):

        self.HoldCurrent = HoldCurrent
        self.CurrReductDelay = CurrReductDelay
        self.PowerOffDelay = PowerOffDelay
        self.CurrentSetTime = CurrentSetTime
        self.PowerFlags = PowerFlags

    # getters
    @property
    def HoldCurrent(self):
        return self._HoldCurrent

    @property
    def CurrReductDelay(self):
        return self._CurrReductDelay

    @property
    def PowerOffDelay(self):
        return self._PowerOffDelay

    @property
    def CurrentSetTime(self):
        return self._CurrentSetTime

    @property
    def PowerFlags(self):
        return self._PowerFlags

    # setters
    @HoldCurrent.setter
    def HoldCurrent(self, val):
        _check_castability(val,
                           c_uint,
                           varname="HoldCurrent")
        self._HoldCurrent = val

    @CurrReductDelay.setter
    def CurrReductDelay(self, val):
        _check_castability(val,
                           c_uint,
                           varname="CurrReductDelay")
        self._CurrReductDelay = val

    @PowerOffDelay.setter
    def PowerOffDelay(self, val):
        _check_castability(val,
                           c_uint,
                           varname="PowerOffDelay")
        self._PowerOffDelay = val

    @CurrentSetTime.setter
    def CurrentSetTime(self, val):
        _check_castability(val,
                           c_uint,
                           varname="CurrentSetTime")
        self._CurrentSetTime = val

    @PowerFlags.setter
    def PowerFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="PowerFlags")
        self._PowerFlags = val


class SecureSettings:

    def __init__(
            self,
            LowUpwrOff,
            CriticalIpwr,
            CriticalUpwr,
            CriticalT,
            CriticalIusb,
            CriticalUusb,
            MinimumUusb,
            Flags):

        self.LowUpwrOff = LowUpwrOff
        self.CriticalIpwr = CriticalIpwr
        self.CriticalUpwr = CriticalUpwr
        self.CriticalT = CriticalT
        self.CriticalIusb = CriticalIusb
        self.CriticalUusb = CriticalUusb
        self.MinimumUusb = MinimumUusb
        self.Flags = Flags

    # getters
    @property
    def LowUpwrOff(self):
        return self._LowUpwrOff

    @property
    def CriticalIpwr(self):
        return self._CriticalIpwr

    @property
    def CriticalUpwr(self):
        return self._CriticalUpwr

    @property
    def CriticalT(self):
        return self._CriticalT

    @property
    def CriticalIusb(self):
        return self._CriticalIusb

    @property
    def CriticalUusb(self):
        return self._CriticalUusb

    @property
    def MinimumUusb(self):
        return self._MinimumUusb

    @property
    def Flags(self):
        return self._Flags

    # setters
    @LowUpwrOff.setter
    def LowUpwrOff(self, val):
        _check_castability(val,
                           c_uint,
                           varname="LowUpwrOff")
        self._LowUpwrOff = val

    @CriticalIpwr.setter
    def CriticalIpwr(self, val):
        _check_castability(val,
                           c_uint,
                           varname="CriticalIpwr")
        self._CriticalIpwr = val

    @CriticalUpwr.setter
    def CriticalUpwr(self, val):
        _check_castability(val,
                           c_uint,
                           varname="CriticalUpwr")
        self._CriticalUpwr = val

    @CriticalT.setter
    def CriticalT(self, val):
        _check_castability(val,
                           c_uint,
                           varname="CriticalT")
        self._CriticalT = val

    @CriticalIusb.setter
    def CriticalIusb(self, val):
        _check_castability(val,
                           c_uint,
                           varname="CriticalIusb")
        self._CriticalIusb = val

    @CriticalUusb.setter
    def CriticalUusb(self, val):
        _check_castability(val,
                           c_uint,
                           varname="CriticalUusb")
        self._CriticalUusb = val

    @MinimumUusb.setter
    def MinimumUusb(self, val):
        _check_castability(val,
                           c_uint,
                           varname="MinimumUusb")
        self._MinimumUusb = val

    @Flags.setter
    def Flags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Flags")
        self._Flags = val


class EdgesSettings:

    def __init__(
            self,
            BorderFlags,
            EnderFlags,
            LeftBorder,
            uLeftBorder,
            RightBorder,
            uRightBorder):

        self.BorderFlags = BorderFlags
        self.EnderFlags = EnderFlags
        self.LeftBorder = LeftBorder
        self.uLeftBorder = uLeftBorder
        self.RightBorder = RightBorder
        self.uRightBorder = uRightBorder

    # getters
    @property
    def BorderFlags(self):
        return self._BorderFlags

    @property
    def EnderFlags(self):
        return self._EnderFlags

    @property
    def LeftBorder(self):
        return self._LeftBorder

    @property
    def uLeftBorder(self):
        return self._uLeftBorder

    @property
    def RightBorder(self):
        return self._RightBorder

    @property
    def uRightBorder(self):
        return self._uRightBorder

    # setters
    @BorderFlags.setter
    def BorderFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="BorderFlags")
        self._BorderFlags = val

    @EnderFlags.setter
    def EnderFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="EnderFlags")
        self._EnderFlags = val

    @LeftBorder.setter
    def LeftBorder(self, val):
        _check_castability(val,
                           c_int,
                           varname="LeftBorder")
        self._LeftBorder = val

    @uLeftBorder.setter
    def uLeftBorder(self, val):
        _check_castability(val,
                           c_int,
                           varname="uLeftBorder")
        self._uLeftBorder = val

    @RightBorder.setter
    def RightBorder(self, val):
        _check_castability(val,
                           c_int,
                           varname="RightBorder")
        self._RightBorder = val

    @uRightBorder.setter
    def uRightBorder(self, val):
        _check_castability(val,
                           c_int,
                           varname="uRightBorder")
        self._uRightBorder = val


class EdgesSettingsCalb:

    def __init__(
            self,
            BorderFlags,
            EnderFlags,
            LeftBorder,
            RightBorder):

        self.BorderFlags = BorderFlags
        self.EnderFlags = EnderFlags
        self.LeftBorder = LeftBorder
        self.RightBorder = RightBorder

    # getters
    @property
    def BorderFlags(self):
        return self._BorderFlags

    @property
    def EnderFlags(self):
        return self._EnderFlags

    @property
    def LeftBorder(self):
        return self._LeftBorder

    @property
    def RightBorder(self):
        return self._RightBorder

    # setters
    @BorderFlags.setter
    def BorderFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="BorderFlags")
        self._BorderFlags = val

    @EnderFlags.setter
    def EnderFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="EnderFlags")
        self._EnderFlags = val

    @LeftBorder.setter
    def LeftBorder(self, val):
        _check_castability(val,
                           c_float,
                           varname="LeftBorder")
        self._LeftBorder = val

    @RightBorder.setter
    def RightBorder(self, val):
        _check_castability(val,
                           c_float,
                           varname="RightBorder")
        self._RightBorder = val


class PidSettings:

    def __init__(
            self,
            KpU,
            KiU,
            KdU,
            Kpf,
            Kif,
            Kdf):

        self.KpU = KpU
        self.KiU = KiU
        self.KdU = KdU
        self.Kpf = Kpf
        self.Kif = Kif
        self.Kdf = Kdf

    # getters
    @property
    def KpU(self):
        return self._KpU

    @property
    def KiU(self):
        return self._KiU

    @property
    def KdU(self):
        return self._KdU

    @property
    def Kpf(self):
        return self._Kpf

    @property
    def Kif(self):
        return self._Kif

    @property
    def Kdf(self):
        return self._Kdf

    # setters
    @KpU.setter
    def KpU(self, val):
        _check_castability(val,
                           c_uint,
                           varname="KpU")
        self._KpU = val

    @KiU.setter
    def KiU(self, val):
        _check_castability(val,
                           c_uint,
                           varname="KiU")
        self._KiU = val

    @KdU.setter
    def KdU(self, val):
        _check_castability(val,
                           c_uint,
                           varname="KdU")
        self._KdU = val

    @Kpf.setter
    def Kpf(self, val):
        _check_castability(val,
                           c_float,
                           varname="Kpf")
        self._Kpf = val

    @Kif.setter
    def Kif(self, val):
        _check_castability(val,
                           c_float,
                           varname="Kif")
        self._Kif = val

    @Kdf.setter
    def Kdf(self, val):
        _check_castability(val,
                           c_float,
                           varname="Kdf")
        self._Kdf = val


class SyncInSettings:

    def __init__(
            self,
            SyncInFlags,
            ClutterTime,
            Position,
            uPosition,
            Speed,
            uSpeed):

        self.SyncInFlags = SyncInFlags
        self.ClutterTime = ClutterTime
        self.Position = Position
        self.uPosition = uPosition
        self.Speed = Speed
        self.uSpeed = uSpeed

    # getters
    @property
    def SyncInFlags(self):
        return self._SyncInFlags

    @property
    def ClutterTime(self):
        return self._ClutterTime

    @property
    def Position(self):
        return self._Position

    @property
    def uPosition(self):
        return self._uPosition

    @property
    def Speed(self):
        return self._Speed

    @property
    def uSpeed(self):
        return self._uSpeed

    # setters
    @SyncInFlags.setter
    def SyncInFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="SyncInFlags")
        self._SyncInFlags = val

    @ClutterTime.setter
    def ClutterTime(self, val):
        _check_castability(val,
                           c_uint,
                           varname="ClutterTime")
        self._ClutterTime = val

    @Position.setter
    def Position(self, val):
        _check_castability(val,
                           c_int,
                           varname="Position")
        self._Position = val

    @uPosition.setter
    def uPosition(self, val):
        _check_castability(val,
                           c_int,
                           varname="uPosition")
        self._uPosition = val

    @Speed.setter
    def Speed(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Speed")
        self._Speed = val

    @uSpeed.setter
    def uSpeed(self, val):
        _check_castability(val,
                           c_uint,
                           varname="uSpeed")
        self._uSpeed = val


class SyncInSettingsCalb:

    def __init__(
            self,
            SyncInFlags,
            ClutterTime,
            Position,
            Speed):

        self.SyncInFlags = SyncInFlags
        self.ClutterTime = ClutterTime
        self.Position = Position
        self.Speed = Speed

    # getters
    @property
    def SyncInFlags(self):
        return self._SyncInFlags

    @property
    def ClutterTime(self):
        return self._ClutterTime

    @property
    def Position(self):
        return self._Position

    @property
    def Speed(self):
        return self._Speed

    # setters
    @SyncInFlags.setter
    def SyncInFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="SyncInFlags")
        self._SyncInFlags = val

    @ClutterTime.setter
    def ClutterTime(self, val):
        _check_castability(val,
                           c_uint,
                           varname="ClutterTime")
        self._ClutterTime = val

    @Position.setter
    def Position(self, val):
        _check_castability(val,
                           c_float,
                           varname="Position")
        self._Position = val

    @Speed.setter
    def Speed(self, val):
        _check_castability(val,
                           c_float,
                           varname="Speed")
        self._Speed = val


class SyncOutSettings:

    def __init__(
            self,
            SyncOutFlags,
            SyncOutPulseSteps,
            SyncOutPeriod,
            Accuracy,
            uAccuracy):

        self.SyncOutFlags = SyncOutFlags
        self.SyncOutPulseSteps = SyncOutPulseSteps
        self.SyncOutPeriod = SyncOutPeriod
        self.Accuracy = Accuracy
        self.uAccuracy = uAccuracy

    # getters
    @property
    def SyncOutFlags(self):
        return self._SyncOutFlags

    @property
    def SyncOutPulseSteps(self):
        return self._SyncOutPulseSteps

    @property
    def SyncOutPeriod(self):
        return self._SyncOutPeriod

    @property
    def Accuracy(self):
        return self._Accuracy

    @property
    def uAccuracy(self):
        return self._uAccuracy

    # setters
    @SyncOutFlags.setter
    def SyncOutFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="SyncOutFlags")
        self._SyncOutFlags = val

    @SyncOutPulseSteps.setter
    def SyncOutPulseSteps(self, val):
        _check_castability(val,
                           c_uint,
                           varname="SyncOutPulseSteps")
        self._SyncOutPulseSteps = val

    @SyncOutPeriod.setter
    def SyncOutPeriod(self, val):
        _check_castability(val,
                           c_uint,
                           varname="SyncOutPeriod")
        self._SyncOutPeriod = val

    @Accuracy.setter
    def Accuracy(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Accuracy")
        self._Accuracy = val

    @uAccuracy.setter
    def uAccuracy(self, val):
        _check_castability(val,
                           c_uint,
                           varname="uAccuracy")
        self._uAccuracy = val


class SyncOutSettingsCalb:

    def __init__(
            self,
            SyncOutFlags,
            SyncOutPulseSteps,
            SyncOutPeriod,
            Accuracy):

        self.SyncOutFlags = SyncOutFlags
        self.SyncOutPulseSteps = SyncOutPulseSteps
        self.SyncOutPeriod = SyncOutPeriod
        self.Accuracy = Accuracy

    # getters
    @property
    def SyncOutFlags(self):
        return self._SyncOutFlags

    @property
    def SyncOutPulseSteps(self):
        return self._SyncOutPulseSteps

    @property
    def SyncOutPeriod(self):
        return self._SyncOutPeriod

    @property
    def Accuracy(self):
        return self._Accuracy

    # setters
    @SyncOutFlags.setter
    def SyncOutFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="SyncOutFlags")
        self._SyncOutFlags = val

    @SyncOutPulseSteps.setter
    def SyncOutPulseSteps(self, val):
        _check_castability(val,
                           c_uint,
                           varname="SyncOutPulseSteps")
        self._SyncOutPulseSteps = val

    @SyncOutPeriod.setter
    def SyncOutPeriod(self, val):
        _check_castability(val,
                           c_uint,
                           varname="SyncOutPeriod")
        self._SyncOutPeriod = val

    @Accuracy.setter
    def Accuracy(self, val):
        _check_castability(val,
                           c_float,
                           varname="Accuracy")
        self._Accuracy = val


class ExtioSettings:

    def __init__(
            self,
            EXTIOSetupFlags,
            EXTIOModeFlags):

        self.EXTIOSetupFlags = EXTIOSetupFlags
        self.EXTIOModeFlags = EXTIOModeFlags

    # getters
    @property
    def EXTIOSetupFlags(self):
        return self._EXTIOSetupFlags

    @property
    def EXTIOModeFlags(self):
        return self._EXTIOModeFlags

    # setters
    @EXTIOSetupFlags.setter
    def EXTIOSetupFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="EXTIOSetupFlags")
        self._EXTIOSetupFlags = val

    @EXTIOModeFlags.setter
    def EXTIOModeFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="EXTIOModeFlags")
        self._EXTIOModeFlags = val


class BrakeSettings:

    def __init__(
            self,
            t1,
            t2,
            t3,
            t4,
            BrakeFlags):

        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.t4 = t4
        self.BrakeFlags = BrakeFlags

    # getters
    @property
    def t1(self):
        return self._t1

    @property
    def t2(self):
        return self._t2

    @property
    def t3(self):
        return self._t3

    @property
    def t4(self):
        return self._t4

    @property
    def BrakeFlags(self):
        return self._BrakeFlags

    # setters
    @t1.setter
    def t1(self, val):
        _check_castability(val,
                           c_uint,
                           varname="t1")
        self._t1 = val

    @t2.setter
    def t2(self, val):
        _check_castability(val,
                           c_uint,
                           varname="t2")
        self._t2 = val

    @t3.setter
    def t3(self, val):
        _check_castability(val,
                           c_uint,
                           varname="t3")
        self._t3 = val

    @t4.setter
    def t4(self, val):
        _check_castability(val,
                           c_uint,
                           varname="t4")
        self._t4 = val

    @BrakeFlags.setter
    def BrakeFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="BrakeFlags")
        self._BrakeFlags = val


class ControlSettings:

    def __init__(
            self,
            MaxSpeed,
            uMaxSpeed,
            Timeout,
            MaxClickTime,
            Flags,
            DeltaPosition,
            uDeltaPosition):

        self.MaxSpeed = MaxSpeed
        self.uMaxSpeed = uMaxSpeed
        self.Timeout = Timeout
        self.MaxClickTime = MaxClickTime
        self.Flags = Flags
        self.DeltaPosition = DeltaPosition
        self.uDeltaPosition = uDeltaPosition

    # getters
    @property
    def MaxSpeed(self):
        return self._MaxSpeed

    @property
    def uMaxSpeed(self):
        return self._uMaxSpeed

    @property
    def Timeout(self):
        return self._Timeout

    @property
    def MaxClickTime(self):
        return self._MaxClickTime

    @property
    def Flags(self):
        return self._Flags

    @property
    def DeltaPosition(self):
        return self._DeltaPosition

    @property
    def uDeltaPosition(self):
        return self._uDeltaPosition

    # setters
    @MaxSpeed.setter
    def MaxSpeed(self, val):
        _check_castability(val,
                           c_uint,
                           varname="MaxSpeed")
        self._MaxSpeed = val

    @uMaxSpeed.setter
    def uMaxSpeed(self, val):
        _check_castability(val,
                           c_uint,
                           varname="uMaxSpeed")
        self._uMaxSpeed = val

    @Timeout.setter
    def Timeout(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Timeout")
        self._Timeout = val

    @MaxClickTime.setter
    def MaxClickTime(self, val):
        _check_castability(val,
                           c_uint,
                           varname="MaxClickTime")
        self._MaxClickTime = val

    @Flags.setter
    def Flags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Flags")
        self._Flags = val

    @DeltaPosition.setter
    def DeltaPosition(self, val):
        _check_castability(val,
                           c_int,
                           varname="DeltaPosition")
        self._DeltaPosition = val

    @uDeltaPosition.setter
    def uDeltaPosition(self, val):
        _check_castability(val,
                           c_int,
                           varname="uDeltaPosition")
        self._uDeltaPosition = val


class ControlSettingsCalb:

    def __init__(
            self,
            MaxSpeed,
            Timeout,
            MaxClickTime,
            Flags,
            DeltaPosition):

        self.MaxSpeed = MaxSpeed
        self.Timeout = Timeout
        self.MaxClickTime = MaxClickTime
        self.Flags = Flags
        self.DeltaPosition = DeltaPosition

    # getters
    @property
    def MaxSpeed(self):
        return self._MaxSpeed

    @property
    def Timeout(self):
        return self._Timeout

    @property
    def MaxClickTime(self):
        return self._MaxClickTime

    @property
    def Flags(self):
        return self._Flags

    @property
    def DeltaPosition(self):
        return self._DeltaPosition

    # setters
    @MaxSpeed.setter
    def MaxSpeed(self, val):
        _check_castability(val,
                           c_float,
                           varname="MaxSpeed")
        self._MaxSpeed = val

    @Timeout.setter
    def Timeout(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Timeout")
        self._Timeout = val

    @MaxClickTime.setter
    def MaxClickTime(self, val):
        _check_castability(val,
                           c_uint,
                           varname="MaxClickTime")
        self._MaxClickTime = val

    @Flags.setter
    def Flags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Flags")
        self._Flags = val

    @DeltaPosition.setter
    def DeltaPosition(self, val):
        _check_castability(val,
                           c_float,
                           varname="DeltaPosition")
        self._DeltaPosition = val


class JoystickSettings:

    def __init__(
            self,
            JoyLowEnd,
            JoyCenter,
            JoyHighEnd,
            ExpFactor,
            DeadZone,
            JoyFlags):

        self.JoyLowEnd = JoyLowEnd
        self.JoyCenter = JoyCenter
        self.JoyHighEnd = JoyHighEnd
        self.ExpFactor = ExpFactor
        self.DeadZone = DeadZone
        self.JoyFlags = JoyFlags

    # getters
    @property
    def JoyLowEnd(self):
        return self._JoyLowEnd

    @property
    def JoyCenter(self):
        return self._JoyCenter

    @property
    def JoyHighEnd(self):
        return self._JoyHighEnd

    @property
    def ExpFactor(self):
        return self._ExpFactor

    @property
    def DeadZone(self):
        return self._DeadZone

    @property
    def JoyFlags(self):
        return self._JoyFlags

    # setters
    @JoyLowEnd.setter
    def JoyLowEnd(self, val):
        _check_castability(val,
                           c_uint,
                           varname="JoyLowEnd")
        self._JoyLowEnd = val

    @JoyCenter.setter
    def JoyCenter(self, val):
        _check_castability(val,
                           c_uint,
                           varname="JoyCenter")
        self._JoyCenter = val

    @JoyHighEnd.setter
    def JoyHighEnd(self, val):
        _check_castability(val,
                           c_uint,
                           varname="JoyHighEnd")
        self._JoyHighEnd = val

    @ExpFactor.setter
    def ExpFactor(self, val):
        _check_castability(val,
                           c_uint,
                           varname="ExpFactor")
        self._ExpFactor = val

    @DeadZone.setter
    def DeadZone(self, val):
        _check_castability(val,
                           c_uint,
                           varname="DeadZone")
        self._DeadZone = val

    @JoyFlags.setter
    def JoyFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="JoyFlags")
        self._JoyFlags = val


class CtpSettings:

    def __init__(
            self,
            CTPMinError,
            CTPFlags):

        self.CTPMinError = CTPMinError
        self.CTPFlags = CTPFlags

    # getters
    @property
    def CTPMinError(self):
        return self._CTPMinError

    @property
    def CTPFlags(self):
        return self._CTPFlags

    # setters
    @CTPMinError.setter
    def CTPMinError(self, val):
        _check_castability(val,
                           c_uint,
                           varname="CTPMinError")
        self._CTPMinError = val

    @CTPFlags.setter
    def CTPFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="CTPFlags")
        self._CTPFlags = val


class UartSettings:

    def __init__(
            self,
            Speed,
            UARTSetupFlags):

        self.Speed = Speed
        self.UARTSetupFlags = UARTSetupFlags

    # getters
    @property
    def Speed(self):
        return self._Speed

    @property
    def UARTSetupFlags(self):
        return self._UARTSetupFlags

    # setters
    @Speed.setter
    def Speed(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Speed")
        self._Speed = val

    @UARTSetupFlags.setter
    def UARTSetupFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="UARTSetupFlags")
        self._UARTSetupFlags = val


class NetworkSettings:

    def __init__(
            self,
            DHCPEnabled,
            IPv4Address,
            SubnetMask,
            DefaultGateway):

        self.DHCPEnabled = DHCPEnabled
        self.IPv4Address = IPv4Address
        self.SubnetMask = SubnetMask
        self.DefaultGateway = DefaultGateway

    # getters
    @property
    def DHCPEnabled(self):
        return self._DHCPEnabled

    @property
    def IPv4Address(self):
        return self._IPv4Address

    @property
    def SubnetMask(self):
        return self._SubnetMask

    @property
    def DefaultGateway(self):
        return self._DefaultGateway

    # setters
    @DHCPEnabled.setter
    def DHCPEnabled(self, val):
        _check_castability(val,
                           c_uint,
                           varname="DHCPEnabled")
        self._DHCPEnabled = val

    @IPv4Address.setter
    def IPv4Address(self, val):
        _check_castability(val,
                           c_uint,
                           varname="IPv4Address")
        self._IPv4Address = val

    @SubnetMask.setter
    def SubnetMask(self, val):
        _check_castability(val,
                           c_uint,
                           varname="SubnetMask")
        self._SubnetMask = val

    @DefaultGateway.setter
    def DefaultGateway(self, val):
        _check_castability(val,
                           c_uint,
                           varname="DefaultGateway")
        self._DefaultGateway = val


class PasswordSettings:

    def __init__(
            self,
            UserPassword):

        self.UserPassword = UserPassword

    # getters
    @property
    def UserPassword(self):
        return self._UserPassword

    # setters
    @UserPassword.setter
    def UserPassword(self, val):
        _check_castability(val,
                           c_uint,
                           varname="UserPassword")
        self._UserPassword = val


class CalibrationSettings:

    def __init__(
            self,
            CSS1_A,
            CSS1_B,
            CSS2_A,
            CSS2_B,
            FullCurrent_A,
            FullCurrent_B):

        self.CSS1_A = CSS1_A
        self.CSS1_B = CSS1_B
        self.CSS2_A = CSS2_A
        self.CSS2_B = CSS2_B
        self.FullCurrent_A = FullCurrent_A
        self.FullCurrent_B = FullCurrent_B

    # getters
    @property
    def CSS1_A(self):
        return self._CSS1_A

    @property
    def CSS1_B(self):
        return self._CSS1_B

    @property
    def CSS2_A(self):
        return self._CSS2_A

    @property
    def CSS2_B(self):
        return self._CSS2_B

    @property
    def FullCurrent_A(self):
        return self._FullCurrent_A

    @property
    def FullCurrent_B(self):
        return self._FullCurrent_B

    # setters
    @CSS1_A.setter
    def CSS1_A(self, val):
        _check_castability(val,
                           c_float,
                           varname="CSS1_A")
        self._CSS1_A = val

    @CSS1_B.setter
    def CSS1_B(self, val):
        _check_castability(val,
                           c_float,
                           varname="CSS1_B")
        self._CSS1_B = val

    @CSS2_A.setter
    def CSS2_A(self, val):
        _check_castability(val,
                           c_float,
                           varname="CSS2_A")
        self._CSS2_A = val

    @CSS2_B.setter
    def CSS2_B(self, val):
        _check_castability(val,
                           c_float,
                           varname="CSS2_B")
        self._CSS2_B = val

    @FullCurrent_A.setter
    def FullCurrent_A(self, val):
        _check_castability(val,
                           c_float,
                           varname="FullCurrent_A")
        self._FullCurrent_A = val

    @FullCurrent_B.setter
    def FullCurrent_B(self, val):
        _check_castability(val,
                           c_float,
                           varname="FullCurrent_B")
        self._FullCurrent_B = val


class ControllerName:

    def __init__(
            self,
            ControllerName,
            CtrlFlags):

        self.ControllerName = ControllerName
        self.CtrlFlags = CtrlFlags

    # getters
    @property
    def ControllerName(self):
        return self._ControllerName

    @property
    def CtrlFlags(self):
        return self._CtrlFlags

    # setters
    @ControllerName.setter
    def ControllerName(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="ControllerName")
        self._ControllerName = val

    @CtrlFlags.setter
    def CtrlFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="CtrlFlags")
        self._CtrlFlags = val


class NonvolatileMemory:

    def __init__(
            self,
            UserData):

        self.UserData = UserData

    # getters
    @property
    def UserData(self):
        return self._UserData

    # setters
    @UserData.setter
    def UserData(self, val):
        _check_castability(val,
                           c_uint * 7,
                           varname="UserData")
        self._UserData = val


class EmfSettings:

    def __init__(
            self,
            L,
            R,
            Km,
            BackEMFFlags):

        self.L = L
        self.R = R
        self.Km = Km
        self.BackEMFFlags = BackEMFFlags

    # getters
    @property
    def L(self):
        return self._L

    @property
    def R(self):
        return self._R

    @property
    def Km(self):
        return self._Km

    @property
    def BackEMFFlags(self):
        return self._BackEMFFlags

    # setters
    @L.setter
    def L(self, val):
        _check_castability(val,
                           c_float,
                           varname="L")
        self._L = val

    @R.setter
    def R(self, val):
        _check_castability(val,
                           c_float,
                           varname="R")
        self._R = val

    @Km.setter
    def Km(self, val):
        _check_castability(val,
                           c_float,
                           varname="Km")
        self._Km = val

    @BackEMFFlags.setter
    def BackEMFFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="BackEMFFlags")
        self._BackEMFFlags = val


class EngineAdvansedSetup:

    def __init__(
            self,
            stepcloseloop_Kw,
            stepcloseloop_Kp_low,
            stepcloseloop_Kp_high):

        self.stepcloseloop_Kw = stepcloseloop_Kw
        self.stepcloseloop_Kp_low = stepcloseloop_Kp_low
        self.stepcloseloop_Kp_high = stepcloseloop_Kp_high

    # getters
    @property
    def stepcloseloop_Kw(self):
        return self._stepcloseloop_Kw

    @property
    def stepcloseloop_Kp_low(self):
        return self._stepcloseloop_Kp_low

    @property
    def stepcloseloop_Kp_high(self):
        return self._stepcloseloop_Kp_high

    # setters
    @stepcloseloop_Kw.setter
    def stepcloseloop_Kw(self, val):
        _check_castability(val,
                           c_uint,
                           varname="stepcloseloop_Kw")
        self._stepcloseloop_Kw = val

    @stepcloseloop_Kp_low.setter
    def stepcloseloop_Kp_low(self, val):
        _check_castability(val,
                           c_uint,
                           varname="stepcloseloop_Kp_low")
        self._stepcloseloop_Kp_low = val

    @stepcloseloop_Kp_high.setter
    def stepcloseloop_Kp_high(self, val):
        _check_castability(val,
                           c_uint,
                           varname="stepcloseloop_Kp_high")
        self._stepcloseloop_Kp_high = val


class ExtendedSettings:

    def __init__(
            self,
            Param1):

        self.Param1 = Param1

    # getters
    @property
    def Param1(self):
        return self._Param1

    # setters
    @Param1.setter
    def Param1(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Param1")
        self._Param1 = val


class GetPosition:

    def __init__(
            self,
            Position,
            uPosition,
            EncPosition):

        self.Position = Position
        self.uPosition = uPosition
        self.EncPosition = EncPosition

    # getters
    @property
    def Position(self):
        return self._Position

    @property
    def uPosition(self):
        return self._uPosition

    @property
    def EncPosition(self):
        return self._EncPosition

    # setters
    @Position.setter
    def Position(self, val):
        _check_castability(val,
                           c_int,
                           varname="Position")
        self._Position = val

    @uPosition.setter
    def uPosition(self, val):
        _check_castability(val,
                           c_int,
                           varname="uPosition")
        self._uPosition = val

    @EncPosition.setter
    def EncPosition(self, val):
        _check_castability(val,
                           c_long,
                           varname="EncPosition")
        self._EncPosition = val


class GetPositionCalb:

    def __init__(
            self,
            Position,
            EncPosition):

        self.Position = Position
        self.EncPosition = EncPosition

    # getters
    @property
    def Position(self):
        return self._Position

    @property
    def EncPosition(self):
        return self._EncPosition

    # setters
    @Position.setter
    def Position(self, val):
        _check_castability(val,
                           c_float,
                           varname="Position")
        self._Position = val

    @EncPosition.setter
    def EncPosition(self, val):
        _check_castability(val,
                           c_longlong,
                           varname="EncPosition")
        self._EncPosition = val


class SetPosition:

    def __init__(
            self,
            Position,
            uPosition,
            EncPosition,
            PosFlags):

        self.Position = Position
        self.uPosition = uPosition
        self.EncPosition = EncPosition
        self.PosFlags = PosFlags

    # getters
    @property
    def Position(self):
        return self._Position

    @property
    def uPosition(self):
        return self._uPosition

    @property
    def EncPosition(self):
        return self._EncPosition

    @property
    def PosFlags(self):
        return self._PosFlags

    # setters
    @Position.setter
    def Position(self, val):
        _check_castability(val,
                           c_int,
                           varname="Position")
        self._Position = val

    @uPosition.setter
    def uPosition(self, val):
        _check_castability(val,
                           c_int,
                           varname="uPosition")
        self._uPosition = val

    @EncPosition.setter
    def EncPosition(self, val):
        _check_castability(val,
                           c_longlong,
                           varname="EncPosition")
        self._EncPosition = val

    @PosFlags.setter
    def PosFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="PosFlags")
        self._PosFlags = val


class SetPositionCalb:

    def __init__(
            self,
            Position,
            EncPosition,
            PosFlags):

        self.Position = Position
        self.EncPosition = EncPosition
        self.PosFlags = PosFlags

    # getters
    @property
    def Position(self):
        return self._Position

    @property
    def EncPosition(self):
        return self._EncPosition

    @property
    def PosFlags(self):
        return self._PosFlags

    # setters
    @Position.setter
    def Position(self, val):
        _check_castability(val,
                           c_float,
                           varname="Position")
        self._Position = val

    @EncPosition.setter
    def EncPosition(self, val):
        _check_castability(val,
                           c_longlong,
                           varname="EncPosition")
        self._EncPosition = val

    @PosFlags.setter
    def PosFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="PosFlags")
        self._PosFlags = val


class Status:

    def __init__(
            self,
            MoveSts,
            MvCmdSts,
            PWRSts,
            EncSts,
            WindSts,
            CurPosition,
            uCurPosition,
            EncPosition,
            CurSpeed,
            uCurSpeed,
            Ipwr,
            Upwr,
            Iusb,
            Uusb,
            CurT,
            Flags,
            GPIOFlags,
            CmdBufFreeSpace):

        self.MoveSts = MoveSts
        self.MvCmdSts = MvCmdSts
        self.PWRSts = PWRSts
        self.EncSts = EncSts
        self.WindSts = WindSts
        self.CurPosition = CurPosition
        self.uCurPosition = uCurPosition
        self.EncPosition = EncPosition
        self.CurSpeed = CurSpeed
        self.uCurSpeed = uCurSpeed
        self.Ipwr = Ipwr
        self.Upwr = Upwr
        self.Iusb = Iusb
        self.Uusb = Uusb
        self.CurT = CurT
        self.Flags = Flags
        self.GPIOFlags = GPIOFlags
        self.CmdBufFreeSpace = CmdBufFreeSpace

    # getters
    @property
    def MoveSts(self):
        return self._MoveSts

    @property
    def MvCmdSts(self):
        return self._MvCmdSts

    @property
    def PWRSts(self):
        return self._PWRSts

    @property
    def EncSts(self):
        return self._EncSts

    @property
    def WindSts(self):
        return self._WindSts

    @property
    def CurPosition(self):
        return self._CurPosition

    @property
    def uCurPosition(self):
        return self._uCurPosition

    @property
    def EncPosition(self):
        return self._EncPosition

    @property
    def CurSpeed(self):
        return self._CurSpeed

    @property
    def uCurSpeed(self):
        return self._uCurSpeed

    @property
    def Ipwr(self):
        return self._Ipwr

    @property
    def Upwr(self):
        return self._Upwr

    @property
    def Iusb(self):
        return self._Iusb

    @property
    def Uusb(self):
        return self._Uusb

    @property
    def CurT(self):
        return self._CurT

    @property
    def Flags(self):
        return self._Flags

    @property
    def GPIOFlags(self):
        return self._GPIOFlags

    @property
    def CmdBufFreeSpace(self):
        return self._CmdBufFreeSpace

    # setters
    @MoveSts.setter
    def MoveSts(self, val):
        _check_castability(val,
                           c_uint,
                           varname="MoveSts")
        self._MoveSts = val

    @MvCmdSts.setter
    def MvCmdSts(self, val):
        _check_castability(val,
                           c_uint,
                           varname="MvCmdSts")
        self._MvCmdSts = val

    @PWRSts.setter
    def PWRSts(self, val):
        _check_castability(val,
                           c_uint,
                           varname="PWRSts")
        self._PWRSts = val

    @EncSts.setter
    def EncSts(self, val):
        _check_castability(val,
                           c_uint,
                           varname="EncSts")
        self._EncSts = val

    @WindSts.setter
    def WindSts(self, val):
        _check_castability(val,
                           c_uint,
                           varname="WindSts")
        self._WindSts = val

    @CurPosition.setter
    def CurPosition(self, val):
        _check_castability(val,
                           c_int,
                           varname="CurPosition")
        self._CurPosition = val

    @uCurPosition.setter
    def uCurPosition(self, val):
        _check_castability(val,
                           c_int,
                           varname="uCurPosition")
        self._uCurPosition = val

    @EncPosition.setter
    def EncPosition(self, val):
        _check_castability(val,
                           c_longlong,
                           varname="EncPosition")
        self._EncPosition = val

    @CurSpeed.setter
    def CurSpeed(self, val):
        _check_castability(val,
                           c_int,
                           varname="CurSpeed")
        self._CurSpeed = val

    @uCurSpeed.setter
    def uCurSpeed(self, val):
        _check_castability(val,
                           c_int,
                           varname="uCurSpeed")
        self._uCurSpeed = val

    @Ipwr.setter
    def Ipwr(self, val):
        _check_castability(val,
                           c_int,
                           varname="Ipwr")
        self._Ipwr = val

    @Upwr.setter
    def Upwr(self, val):
        _check_castability(val,
                           c_int,
                           varname="Upwr")
        self._Upwr = val

    @Iusb.setter
    def Iusb(self, val):
        _check_castability(val,
                           c_int,
                           varname="Iusb")
        self._Iusb = val

    @Uusb.setter
    def Uusb(self, val):
        _check_castability(val,
                           c_int,
                           varname="Uusb")
        self._Uusb = val

    @CurT.setter
    def CurT(self, val):
        _check_castability(val,
                           c_int,
                           varname="CurT")
        self._CurT = val

    @Flags.setter
    def Flags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Flags")
        self._Flags = val

    @GPIOFlags.setter
    def GPIOFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="GPIOFlags")
        self._GPIOFlags = val

    @CmdBufFreeSpace.setter
    def CmdBufFreeSpace(self, val):
        _check_castability(val,
                           c_uint,
                           varname="CmdBufFreeSpace")
        self._CmdBufFreeSpace = val


class StatusCalb:

    def __init__(
            self,
            MoveSts,
            MvCmdSts,
            PWRSts,
            EncSts,
            WindSts,
            CurPosition,
            EncPosition,
            CurSpeed,
            Ipwr,
            Upwr,
            Iusb,
            Uusb,
            CurT,
            Flags,
            GPIOFlags,
            CmdBufFreeSpace):

        self.MoveSts = MoveSts
        self.MvCmdSts = MvCmdSts
        self.PWRSts = PWRSts
        self.EncSts = EncSts
        self.WindSts = WindSts
        self.CurPosition = CurPosition
        self.EncPosition = EncPosition
        self.CurSpeed = CurSpeed
        self.Ipwr = Ipwr
        self.Upwr = Upwr
        self.Iusb = Iusb
        self.Uusb = Uusb
        self.CurT = CurT
        self.Flags = Flags
        self.GPIOFlags = GPIOFlags
        self.CmdBufFreeSpace = CmdBufFreeSpace

    # getters
    @property
    def MoveSts(self):
        return self._MoveSts

    @property
    def MvCmdSts(self):
        return self._MvCmdSts

    @property
    def PWRSts(self):
        return self._PWRSts

    @property
    def EncSts(self):
        return self._EncSts

    @property
    def WindSts(self):
        return self._WindSts

    @property
    def CurPosition(self):
        return self._CurPosition

    @property
    def EncPosition(self):
        return self._EncPosition

    @property
    def CurSpeed(self):
        return self._CurSpeed

    @property
    def Ipwr(self):
        return self._Ipwr

    @property
    def Upwr(self):
        return self._Upwr

    @property
    def Iusb(self):
        return self._Iusb

    @property
    def Uusb(self):
        return self._Uusb

    @property
    def CurT(self):
        return self._CurT

    @property
    def Flags(self):
        return self._Flags

    @property
    def GPIOFlags(self):
        return self._GPIOFlags

    @property
    def CmdBufFreeSpace(self):
        return self._CmdBufFreeSpace

    # setters
    @MoveSts.setter
    def MoveSts(self, val):
        _check_castability(val,
                           c_uint,
                           varname="MoveSts")
        self._MoveSts = val

    @MvCmdSts.setter
    def MvCmdSts(self, val):
        _check_castability(val,
                           c_uint,
                           varname="MvCmdSts")
        self._MvCmdSts = val

    @PWRSts.setter
    def PWRSts(self, val):
        _check_castability(val,
                           c_uint,
                           varname="PWRSts")
        self._PWRSts = val

    @EncSts.setter
    def EncSts(self, val):
        _check_castability(val,
                           c_uint,
                           varname="EncSts")
        self._EncSts = val

    @WindSts.setter
    def WindSts(self, val):
        _check_castability(val,
                           c_uint,
                           varname="WindSts")
        self._WindSts = val

    @CurPosition.setter
    def CurPosition(self, val):
        _check_castability(val,
                           c_float,
                           varname="CurPosition")
        self._CurPosition = val

    @EncPosition.setter
    def EncPosition(self, val):
        _check_castability(val,
                           c_longlong,
                           varname="EncPosition")
        self._EncPosition = val

    @CurSpeed.setter
    def CurSpeed(self, val):
        _check_castability(val,
                           c_float,
                           varname="CurSpeed")
        self._CurSpeed = val

    @Ipwr.setter
    def Ipwr(self, val):
        _check_castability(val,
                           c_int,
                           varname="Ipwr")
        self._Ipwr = val

    @Upwr.setter
    def Upwr(self, val):
        _check_castability(val,
                           c_int,
                           varname="Upwr")
        self._Upwr = val

    @Iusb.setter
    def Iusb(self, val):
        _check_castability(val,
                           c_int,
                           varname="Iusb")
        self._Iusb = val

    @Uusb.setter
    def Uusb(self, val):
        _check_castability(val,
                           c_int,
                           varname="Uusb")
        self._Uusb = val

    @CurT.setter
    def CurT(self, val):
        _check_castability(val,
                           c_int,
                           varname="CurT")
        self._CurT = val

    @Flags.setter
    def Flags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Flags")
        self._Flags = val

    @GPIOFlags.setter
    def GPIOFlags(self, val):
        _check_castability(val,
                           c_uint,
                           varname="GPIOFlags")
        self._GPIOFlags = val

    @CmdBufFreeSpace.setter
    def CmdBufFreeSpace(self, val):
        _check_castability(val,
                           c_uint,
                           varname="CmdBufFreeSpace")
        self._CmdBufFreeSpace = val


class Measurements:

    def __init__(
            self,
            Speed,
            Error,
            Length):

        self.Speed = Speed
        self.Error = Error
        self.Length = Length

    # getters
    @property
    def Speed(self):
        return self._Speed

    @property
    def Error(self):
        return self._Error

    @property
    def Length(self):
        return self._Length

    # setters
    @Speed.setter
    def Speed(self, val):
        _check_castability(val,
                           c_int,
                           varname="Speed")
        self._Speed = val

    @Error.setter
    def Error(self, val):
        _check_castability(val,
                           c_int,
                           varname="Error")
        self._Error = val

    @Length.setter
    def Length(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Length")
        self._Length = val


class ChartData:

    def __init__(
            self,
            WindingVoltageA,
            WindingVoltageB,
            WindingVoltageC,
            WindingCurrentA,
            WindingCurrentB,
            WindingCurrentC,
            Pot,
            Joy,
            DutyCycle):

        self.WindingVoltageA = WindingVoltageA
        self.WindingVoltageB = WindingVoltageB
        self.WindingVoltageC = WindingVoltageC
        self.WindingCurrentA = WindingCurrentA
        self.WindingCurrentB = WindingCurrentB
        self.WindingCurrentC = WindingCurrentC
        self.Pot = Pot
        self.Joy = Joy
        self.DutyCycle = DutyCycle

    # getters
    @property
    def WindingVoltageA(self):
        return self._WindingVoltageA

    @property
    def WindingVoltageB(self):
        return self._WindingVoltageB

    @property
    def WindingVoltageC(self):
        return self._WindingVoltageC

    @property
    def WindingCurrentA(self):
        return self._WindingCurrentA

    @property
    def WindingCurrentB(self):
        return self._WindingCurrentB

    @property
    def WindingCurrentC(self):
        return self._WindingCurrentC

    @property
    def Pot(self):
        return self._Pot

    @property
    def Joy(self):
        return self._Joy

    @property
    def DutyCycle(self):
        return self._DutyCycle

    # setters
    @WindingVoltageA.setter
    def WindingVoltageA(self, val):
        _check_castability(val,
                           c_int,
                           varname="WindingVoltageA")
        self._WindingVoltageA = val

    @WindingVoltageB.setter
    def WindingVoltageB(self, val):
        _check_castability(val,
                           c_int,
                           varname="WindingVoltageB")
        self._WindingVoltageB = val

    @WindingVoltageC.setter
    def WindingVoltageC(self, val):
        _check_castability(val,
                           c_int,
                           varname="WindingVoltageC")
        self._WindingVoltageC = val

    @WindingCurrentA.setter
    def WindingCurrentA(self, val):
        _check_castability(val,
                           c_int,
                           varname="WindingCurrentA")
        self._WindingCurrentA = val

    @WindingCurrentB.setter
    def WindingCurrentB(self, val):
        _check_castability(val,
                           c_int,
                           varname="WindingCurrentB")
        self._WindingCurrentB = val

    @WindingCurrentC.setter
    def WindingCurrentC(self, val):
        _check_castability(val,
                           c_int,
                           varname="WindingCurrentC")
        self._WindingCurrentC = val

    @Pot.setter
    def Pot(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Pot")
        self._Pot = val

    @Joy.setter
    def Joy(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Joy")
        self._Joy = val

    @DutyCycle.setter
    def DutyCycle(self, val):
        _check_castability(val,
                           c_int,
                           varname="DutyCycle")
        self._DutyCycle = val


class DeviceInformation:

    def __init__(
            self,
            Manufacturer,
            ManufacturerId,
            ProductDescription,
            Major,
            Minor,
            Release):

        self.Manufacturer = Manufacturer
        self.ManufacturerId = ManufacturerId
        self.ProductDescription = ProductDescription
        self.Major = Major
        self.Minor = Minor
        self.Release = Release

    # getters
    @property
    def Manufacturer(self):
        return self._Manufacturer

    @property
    def ManufacturerId(self):
        return self._ManufacturerId

    @property
    def ProductDescription(self):
        return self._ProductDescription

    @property
    def Major(self):
        return self._Major

    @property
    def Minor(self):
        return self._Minor

    @property
    def Release(self):
        return self._Release

    # setters
    @Manufacturer.setter
    def Manufacturer(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="Manufacturer")
        self._Manufacturer = val

    @ManufacturerId.setter
    def ManufacturerId(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="ManufacturerId")
        self._ManufacturerId = val

    @ProductDescription.setter
    def ProductDescription(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="ProductDescription")
        self._ProductDescription = val

    @Major.setter
    def Major(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Major")
        self._Major = val

    @Minor.setter
    def Minor(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Minor")
        self._Minor = val

    @Release.setter
    def Release(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Release")
        self._Release = val


class SerialNumber:

    def __init__(
            self,
            SN,
            Key,
            Major,
            Minor,
            Release):

        self.SN = SN
        self.Key = Key
        self.Major = Major
        self.Minor = Minor
        self.Release = Release

    # getters
    @property
    def SN(self):
        return self._SN

    @property
    def Key(self):
        return self._Key

    @property
    def Major(self):
        return self._Major

    @property
    def Minor(self):
        return self._Minor

    @property
    def Release(self):
        return self._Release

    # setters
    @SN.setter
    def SN(self, val):
        _check_castability(val,
                           c_uint,
                           varname="SN")
        self._SN = val

    @Key.setter
    def Key(self, val):
        _check_castability(val,
                           c_uint8 * 32,
                           varname="Key")
        self._Key = val

    @Major.setter
    def Major(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Major")
        self._Major = val

    @Minor.setter
    def Minor(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Minor")
        self._Minor = val

    @Release.setter
    def Release(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Release")
        self._Release = val


class AnalogData:

    def __init__(
            self,
            A1Voltage_ADC,
            A2Voltage_ADC,
            B1Voltage_ADC,
            B2Voltage_ADC,
            SupVoltage_ADC,
            ACurrent_ADC,
            BCurrent_ADC,
            FullCurrent_ADC,
            Temp_ADC,
            Joy_ADC,
            Pot_ADC,
            L5_ADC,
            H5_ADC,
            A1Voltage,
            A2Voltage,
            B1Voltage,
            B2Voltage,
            SupVoltage,
            ACurrent,
            BCurrent,
            FullCurrent,
            Temp,
            Joy,
            Pot,
            L5,
            H5,
            deprecated,
            R,
            L):

        self.A1Voltage_ADC = A1Voltage_ADC
        self.A2Voltage_ADC = A2Voltage_ADC
        self.B1Voltage_ADC = B1Voltage_ADC
        self.B2Voltage_ADC = B2Voltage_ADC
        self.SupVoltage_ADC = SupVoltage_ADC
        self.ACurrent_ADC = ACurrent_ADC
        self.BCurrent_ADC = BCurrent_ADC
        self.FullCurrent_ADC = FullCurrent_ADC
        self.Temp_ADC = Temp_ADC
        self.Joy_ADC = Joy_ADC
        self.Pot_ADC = Pot_ADC
        self.L5_ADC = L5_ADC
        self.H5_ADC = H5_ADC
        self.A1Voltage = A1Voltage
        self.A2Voltage = A2Voltage
        self.B1Voltage = B1Voltage
        self.B2Voltage = B2Voltage
        self.SupVoltage = SupVoltage
        self.ACurrent = ACurrent
        self.BCurrent = BCurrent
        self.FullCurrent = FullCurrent
        self.Temp = Temp
        self.Joy = Joy
        self.Pot = Pot
        self.L5 = L5
        self.H5 = H5
        self.deprecated = deprecated
        self.R = R
        self.L = L

    # getters
    @property
    def A1Voltage_ADC(self):
        return self._A1Voltage_ADC

    @property
    def A2Voltage_ADC(self):
        return self._A2Voltage_ADC

    @property
    def B1Voltage_ADC(self):
        return self._B1Voltage_ADC

    @property
    def B2Voltage_ADC(self):
        return self._B2Voltage_ADC

    @property
    def SupVoltage_ADC(self):
        return self._SupVoltage_ADC

    @property
    def ACurrent_ADC(self):
        return self._ACurrent_ADC

    @property
    def BCurrent_ADC(self):
        return self._BCurrent_ADC

    @property
    def FullCurrent_ADC(self):
        return self._FullCurrent_ADC

    @property
    def Temp_ADC(self):
        return self._Temp_ADC

    @property
    def Joy_ADC(self):
        return self._Joy_ADC

    @property
    def Pot_ADC(self):
        return self._Pot_ADC

    @property
    def L5_ADC(self):
        return self._L5_ADC

    @property
    def H5_ADC(self):
        return self._H5_ADC

    @property
    def A1Voltage(self):
        return self._A1Voltage

    @property
    def A2Voltage(self):
        return self._A2Voltage

    @property
    def B1Voltage(self):
        return self._B1Voltage

    @property
    def B2Voltage(self):
        return self._B2Voltage

    @property
    def SupVoltage(self):
        return self._SupVoltage

    @property
    def ACurrent(self):
        return self._ACurrent

    @property
    def BCurrent(self):
        return self._BCurrent

    @property
    def FullCurrent(self):
        return self._FullCurrent

    @property
    def Temp(self):
        return self._Temp

    @property
    def Joy(self):
        return self._Joy

    @property
    def Pot(self):
        return self._Pot

    @property
    def L5(self):
        return self._L5

    @property
    def H5(self):
        return self._H5

    @property
    def deprecated(self):
        return self._deprecated

    @property
    def R(self):
        return self._R

    @property
    def L(self):
        return self._L

    # setters
    @A1Voltage_ADC.setter
    def A1Voltage_ADC(self, val):
        _check_castability(val,
                           c_uint,
                           varname="A1Voltage_ADC")
        self._A1Voltage_ADC = val

    @A2Voltage_ADC.setter
    def A2Voltage_ADC(self, val):
        _check_castability(val,
                           c_uint,
                           varname="A2Voltage_ADC")
        self._A2Voltage_ADC = val

    @B1Voltage_ADC.setter
    def B1Voltage_ADC(self, val):
        _check_castability(val,
                           c_uint,
                           varname="B1Voltage_ADC")
        self._B1Voltage_ADC = val

    @B2Voltage_ADC.setter
    def B2Voltage_ADC(self, val):
        _check_castability(val,
                           c_uint,
                           varname="B2Voltage_ADC")
        self._B2Voltage_ADC = val

    @SupVoltage_ADC.setter
    def SupVoltage_ADC(self, val):
        _check_castability(val,
                           c_uint,
                           varname="SupVoltage_ADC")
        self._SupVoltage_ADC = val

    @ACurrent_ADC.setter
    def ACurrent_ADC(self, val):
        _check_castability(val,
                           c_uint,
                           varname="ACurrent_ADC")
        self._ACurrent_ADC = val

    @BCurrent_ADC.setter
    def BCurrent_ADC(self, val):
        _check_castability(val,
                           c_uint,
                           varname="BCurrent_ADC")
        self._BCurrent_ADC = val

    @FullCurrent_ADC.setter
    def FullCurrent_ADC(self, val):
        _check_castability(val,
                           c_uint,
                           varname="FullCurrent_ADC")
        self._FullCurrent_ADC = val

    @Temp_ADC.setter
    def Temp_ADC(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Temp_ADC")
        self._Temp_ADC = val

    @Joy_ADC.setter
    def Joy_ADC(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Joy_ADC")
        self._Joy_ADC = val

    @Pot_ADC.setter
    def Pot_ADC(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Pot_ADC")
        self._Pot_ADC = val

    @L5_ADC.setter
    def L5_ADC(self, val):
        _check_castability(val,
                           c_uint,
                           varname="L5_ADC")
        self._L5_ADC = val

    @H5_ADC.setter
    def H5_ADC(self, val):
        _check_castability(val,
                           c_uint,
                           varname="H5_ADC")
        self._H5_ADC = val

    @A1Voltage.setter
    def A1Voltage(self, val):
        _check_castability(val,
                           c_int,
                           varname="A1Voltage")
        self._A1Voltage = val

    @A2Voltage.setter
    def A2Voltage(self, val):
        _check_castability(val,
                           c_int,
                           varname="A2Voltage")
        self._A2Voltage = val

    @B1Voltage.setter
    def B1Voltage(self, val):
        _check_castability(val,
                           c_int,
                           varname="B1Voltage")
        self._B1Voltage = val

    @B2Voltage.setter
    def B2Voltage(self, val):
        _check_castability(val,
                           c_int,
                           varname="B2Voltage")
        self._B2Voltage = val

    @SupVoltage.setter
    def SupVoltage(self, val):
        _check_castability(val,
                           c_int,
                           varname="SupVoltage")
        self._SupVoltage = val

    @ACurrent.setter
    def ACurrent(self, val):
        _check_castability(val,
                           c_int,
                           varname="ACurrent")
        self._ACurrent = val

    @BCurrent.setter
    def BCurrent(self, val):
        _check_castability(val,
                           c_int,
                           varname="BCurrent")
        self._BCurrent = val

    @FullCurrent.setter
    def FullCurrent(self, val):
        _check_castability(val,
                           c_int,
                           varname="FullCurrent")
        self._FullCurrent = val

    @Temp.setter
    def Temp(self, val):
        _check_castability(val,
                           c_int,
                           varname="Temp")
        self._Temp = val

    @Joy.setter
    def Joy(self, val):
        _check_castability(val,
                           c_int,
                           varname="Joy")
        self._Joy = val

    @Pot.setter
    def Pot(self, val):
        _check_castability(val,
                           c_int,
                           varname="Pot")
        self._Pot = val

    @L5.setter
    def L5(self, val):
        _check_castability(val,
                           c_int,
                           varname="L5")
        self._L5 = val

    @H5.setter
    def H5(self, val):
        _check_castability(val,
                           c_int,
                           varname="H5")
        self._H5 = val

    @deprecated.setter
    def deprecated(self, val):
        _check_castability(val,
                           c_uint,
                           varname="deprecated")
        self._deprecated = val

    @R.setter
    def R(self, val):
        _check_castability(val,
                           c_int,
                           varname="R")
        self._R = val

    @L.setter
    def L(self, val):
        _check_castability(val,
                           c_int,
                           varname="L")
        self._L = val


class StageName:

    def __init__(
            self,
            PositionerName):

        self.PositionerName = PositionerName

    # getters
    @property
    def PositionerName(self):
        return self._PositionerName

    # setters
    @PositionerName.setter
    def PositionerName(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="PositionerName")
        self._PositionerName = val


class StageInformation:

    def __init__(
            self,
            Manufacturer,
            PartNumber):

        self.Manufacturer = Manufacturer
        self.PartNumber = PartNumber

    # getters
    @property
    def Manufacturer(self):
        return self._Manufacturer

    @property
    def PartNumber(self):
        return self._PartNumber

    # setters
    @Manufacturer.setter
    def Manufacturer(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="Manufacturer")
        self._Manufacturer = val

    @PartNumber.setter
    def PartNumber(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="PartNumber")
        self._PartNumber = val


class StageSettings:

    def __init__(
            self,
            LeadScrewPitch,
            Units,
            MaxSpeed,
            TravelRange,
            SupplyVoltageMin,
            SupplyVoltageMax,
            MaxCurrentConsumption,
            HorizontalLoadCapacity,
            VerticalLoadCapacity):

        self.LeadScrewPitch = LeadScrewPitch
        self.Units = Units
        self.MaxSpeed = MaxSpeed
        self.TravelRange = TravelRange
        self.SupplyVoltageMin = SupplyVoltageMin
        self.SupplyVoltageMax = SupplyVoltageMax
        self.MaxCurrentConsumption = MaxCurrentConsumption
        self.HorizontalLoadCapacity = HorizontalLoadCapacity
        self.VerticalLoadCapacity = VerticalLoadCapacity

    # getters
    @property
    def LeadScrewPitch(self):
        return self._LeadScrewPitch

    @property
    def Units(self):
        return self._Units

    @property
    def MaxSpeed(self):
        return self._MaxSpeed

    @property
    def TravelRange(self):
        return self._TravelRange

    @property
    def SupplyVoltageMin(self):
        return self._SupplyVoltageMin

    @property
    def SupplyVoltageMax(self):
        return self._SupplyVoltageMax

    @property
    def MaxCurrentConsumption(self):
        return self._MaxCurrentConsumption

    @property
    def HorizontalLoadCapacity(self):
        return self._HorizontalLoadCapacity

    @property
    def VerticalLoadCapacity(self):
        return self._VerticalLoadCapacity

    # setters
    @LeadScrewPitch.setter
    def LeadScrewPitch(self, val):
        _check_castability(val,
                           c_float,
                           varname="LeadScrewPitch")
        self._LeadScrewPitch = val

    @Units.setter
    def Units(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="Units")
        self._Units = val

    @MaxSpeed.setter
    def MaxSpeed(self, val):
        _check_castability(val,
                           c_float,
                           varname="MaxSpeed")
        self._MaxSpeed = val

    @TravelRange.setter
    def TravelRange(self, val):
        _check_castability(val,
                           c_float,
                           varname="TravelRange")
        self._TravelRange = val

    @SupplyVoltageMin.setter
    def SupplyVoltageMin(self, val):
        _check_castability(val,
                           c_float,
                           varname="SupplyVoltageMin")
        self._SupplyVoltageMin = val

    @SupplyVoltageMax.setter
    def SupplyVoltageMax(self, val):
        _check_castability(val,
                           c_float,
                           varname="SupplyVoltageMax")
        self._SupplyVoltageMax = val

    @MaxCurrentConsumption.setter
    def MaxCurrentConsumption(self, val):
        _check_castability(val,
                           c_float,
                           varname="MaxCurrentConsumption")
        self._MaxCurrentConsumption = val

    @HorizontalLoadCapacity.setter
    def HorizontalLoadCapacity(self, val):
        _check_castability(val,
                           c_float,
                           varname="HorizontalLoadCapacity")
        self._HorizontalLoadCapacity = val

    @VerticalLoadCapacity.setter
    def VerticalLoadCapacity(self, val):
        _check_castability(val,
                           c_float,
                           varname="VerticalLoadCapacity")
        self._VerticalLoadCapacity = val


class MotorInformation:

    def __init__(
            self,
            Manufacturer,
            PartNumber):

        self.Manufacturer = Manufacturer
        self.PartNumber = PartNumber

    # getters
    @property
    def Manufacturer(self):
        return self._Manufacturer

    @property
    def PartNumber(self):
        return self._PartNumber

    # setters
    @Manufacturer.setter
    def Manufacturer(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="Manufacturer")
        self._Manufacturer = val

    @PartNumber.setter
    def PartNumber(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="PartNumber")
        self._PartNumber = val


class MotorSettings:

    def __init__(
            self,
            MotorType,
            ReservedField,
            Poles,
            Phases,
            NominalVoltage,
            NominalCurrent,
            NominalSpeed,
            NominalTorque,
            NominalPower,
            WindingResistance,
            WindingInductance,
            RotorInertia,
            StallTorque,
            DetentTorque,
            TorqueConstant,
            SpeedConstant,
            SpeedTorqueGradient,
            MechanicalTimeConstant,
            MaxSpeed,
            MaxCurrent,
            MaxCurrentTime,
            NoLoadCurrent,
            NoLoadSpeed):

        self.MotorType = MotorType
        self.ReservedField = ReservedField
        self.Poles = Poles
        self.Phases = Phases
        self.NominalVoltage = NominalVoltage
        self.NominalCurrent = NominalCurrent
        self.NominalSpeed = NominalSpeed
        self.NominalTorque = NominalTorque
        self.NominalPower = NominalPower
        self.WindingResistance = WindingResistance
        self.WindingInductance = WindingInductance
        self.RotorInertia = RotorInertia
        self.StallTorque = StallTorque
        self.DetentTorque = DetentTorque
        self.TorqueConstant = TorqueConstant
        self.SpeedConstant = SpeedConstant
        self.SpeedTorqueGradient = SpeedTorqueGradient
        self.MechanicalTimeConstant = MechanicalTimeConstant
        self.MaxSpeed = MaxSpeed
        self.MaxCurrent = MaxCurrent
        self.MaxCurrentTime = MaxCurrentTime
        self.NoLoadCurrent = NoLoadCurrent
        self.NoLoadSpeed = NoLoadSpeed

    # getters
    @property
    def MotorType(self):
        return self._MotorType

    @property
    def ReservedField(self):
        return self._ReservedField

    @property
    def Poles(self):
        return self._Poles

    @property
    def Phases(self):
        return self._Phases

    @property
    def NominalVoltage(self):
        return self._NominalVoltage

    @property
    def NominalCurrent(self):
        return self._NominalCurrent

    @property
    def NominalSpeed(self):
        return self._NominalSpeed

    @property
    def NominalTorque(self):
        return self._NominalTorque

    @property
    def NominalPower(self):
        return self._NominalPower

    @property
    def WindingResistance(self):
        return self._WindingResistance

    @property
    def WindingInductance(self):
        return self._WindingInductance

    @property
    def RotorInertia(self):
        return self._RotorInertia

    @property
    def StallTorque(self):
        return self._StallTorque

    @property
    def DetentTorque(self):
        return self._DetentTorque

    @property
    def TorqueConstant(self):
        return self._TorqueConstant

    @property
    def SpeedConstant(self):
        return self._SpeedConstant

    @property
    def SpeedTorqueGradient(self):
        return self._SpeedTorqueGradient

    @property
    def MechanicalTimeConstant(self):
        return self._MechanicalTimeConstant

    @property
    def MaxSpeed(self):
        return self._MaxSpeed

    @property
    def MaxCurrent(self):
        return self._MaxCurrent

    @property
    def MaxCurrentTime(self):
        return self._MaxCurrentTime

    @property
    def NoLoadCurrent(self):
        return self._NoLoadCurrent

    @property
    def NoLoadSpeed(self):
        return self._NoLoadSpeed

    # setters
    @MotorType.setter
    def MotorType(self, val):
        _check_castability(val,
                           c_uint,
                           varname="MotorType")
        self._MotorType = val

    @ReservedField.setter
    def ReservedField(self, val):
        _check_castability(val,
                           c_uint,
                           varname="ReservedField")
        self._ReservedField = val

    @Poles.setter
    def Poles(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Poles")
        self._Poles = val

    @Phases.setter
    def Phases(self, val):
        _check_castability(val,
                           c_uint,
                           varname="Phases")
        self._Phases = val

    @NominalVoltage.setter
    def NominalVoltage(self, val):
        _check_castability(val,
                           c_float,
                           varname="NominalVoltage")
        self._NominalVoltage = val

    @NominalCurrent.setter
    def NominalCurrent(self, val):
        _check_castability(val,
                           c_float,
                           varname="NominalCurrent")
        self._NominalCurrent = val

    @NominalSpeed.setter
    def NominalSpeed(self, val):
        _check_castability(val,
                           c_float,
                           varname="NominalSpeed")
        self._NominalSpeed = val

    @NominalTorque.setter
    def NominalTorque(self, val):
        _check_castability(val,
                           c_float,
                           varname="NominalTorque")
        self._NominalTorque = val

    @NominalPower.setter
    def NominalPower(self, val):
        _check_castability(val,
                           c_float,
                           varname="NominalPower")
        self._NominalPower = val

    @WindingResistance.setter
    def WindingResistance(self, val):
        _check_castability(val,
                           c_float,
                           varname="WindingResistance")
        self._WindingResistance = val

    @WindingInductance.setter
    def WindingInductance(self, val):
        _check_castability(val,
                           c_float,
                           varname="WindingInductance")
        self._WindingInductance = val

    @RotorInertia.setter
    def RotorInertia(self, val):
        _check_castability(val,
                           c_float,
                           varname="RotorInertia")
        self._RotorInertia = val

    @StallTorque.setter
    def StallTorque(self, val):
        _check_castability(val,
                           c_float,
                           varname="StallTorque")
        self._StallTorque = val

    @DetentTorque.setter
    def DetentTorque(self, val):
        _check_castability(val,
                           c_float,
                           varname="DetentTorque")
        self._DetentTorque = val

    @TorqueConstant.setter
    def TorqueConstant(self, val):
        _check_castability(val,
                           c_float,
                           varname="TorqueConstant")
        self._TorqueConstant = val

    @SpeedConstant.setter
    def SpeedConstant(self, val):
        _check_castability(val,
                           c_float,
                           varname="SpeedConstant")
        self._SpeedConstant = val

    @SpeedTorqueGradient.setter
    def SpeedTorqueGradient(self, val):
        _check_castability(val,
                           c_float,
                           varname="SpeedTorqueGradient")
        self._SpeedTorqueGradient = val

    @MechanicalTimeConstant.setter
    def MechanicalTimeConstant(self, val):
        _check_castability(val,
                           c_float,
                           varname="MechanicalTimeConstant")
        self._MechanicalTimeConstant = val

    @MaxSpeed.setter
    def MaxSpeed(self, val):
        _check_castability(val,
                           c_float,
                           varname="MaxSpeed")
        self._MaxSpeed = val

    @MaxCurrent.setter
    def MaxCurrent(self, val):
        _check_castability(val,
                           c_float,
                           varname="MaxCurrent")
        self._MaxCurrent = val

    @MaxCurrentTime.setter
    def MaxCurrentTime(self, val):
        _check_castability(val,
                           c_float,
                           varname="MaxCurrentTime")
        self._MaxCurrentTime = val

    @NoLoadCurrent.setter
    def NoLoadCurrent(self, val):
        _check_castability(val,
                           c_float,
                           varname="NoLoadCurrent")
        self._NoLoadCurrent = val

    @NoLoadSpeed.setter
    def NoLoadSpeed(self, val):
        _check_castability(val,
                           c_float,
                           varname="NoLoadSpeed")
        self._NoLoadSpeed = val


class EncoderInformation:

    def __init__(
            self,
            Manufacturer,
            PartNumber):

        self.Manufacturer = Manufacturer
        self.PartNumber = PartNumber

    # getters
    @property
    def Manufacturer(self):
        return self._Manufacturer

    @property
    def PartNumber(self):
        return self._PartNumber

    # setters
    @Manufacturer.setter
    def Manufacturer(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="Manufacturer")
        self._Manufacturer = val

    @PartNumber.setter
    def PartNumber(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="PartNumber")
        self._PartNumber = val


class EncoderSettings:

    def __init__(
            self,
            MaxOperatingFrequency,
            SupplyVoltageMin,
            SupplyVoltageMax,
            MaxCurrentConsumption,
            PPR,
            EncoderSettings):

        self.MaxOperatingFrequency = MaxOperatingFrequency
        self.SupplyVoltageMin = SupplyVoltageMin
        self.SupplyVoltageMax = SupplyVoltageMax
        self.MaxCurrentConsumption = MaxCurrentConsumption
        self.PPR = PPR
        self.EncoderSettings = EncoderSettings

    # getters
    @property
    def MaxOperatingFrequency(self):
        return self._MaxOperatingFrequency

    @property
    def SupplyVoltageMin(self):
        return self._SupplyVoltageMin

    @property
    def SupplyVoltageMax(self):
        return self._SupplyVoltageMax

    @property
    def MaxCurrentConsumption(self):
        return self._MaxCurrentConsumption

    @property
    def PPR(self):
        return self._PPR

    @property
    def EncoderSettings(self):
        return self._EncoderSettings

    # setters
    @MaxOperatingFrequency.setter
    def MaxOperatingFrequency(self, val):
        _check_castability(val,
                           c_float,
                           varname="MaxOperatingFrequency")
        self._MaxOperatingFrequency = val

    @SupplyVoltageMin.setter
    def SupplyVoltageMin(self, val):
        _check_castability(val,
                           c_float,
                           varname="SupplyVoltageMin")
        self._SupplyVoltageMin = val

    @SupplyVoltageMax.setter
    def SupplyVoltageMax(self, val):
        _check_castability(val,
                           c_float,
                           varname="SupplyVoltageMax")
        self._SupplyVoltageMax = val

    @MaxCurrentConsumption.setter
    def MaxCurrentConsumption(self, val):
        _check_castability(val,
                           c_float,
                           varname="MaxCurrentConsumption")
        self._MaxCurrentConsumption = val

    @PPR.setter
    def PPR(self, val):
        _check_castability(val,
                           c_uint,
                           varname="PPR")
        self._PPR = val

    @EncoderSettings.setter
    def EncoderSettings(self, val):
        _check_castability(val,
                           c_uint,
                           varname="EncoderSettings")
        self._EncoderSettings = val


class HallsensorInformation:

    def __init__(
            self,
            Manufacturer,
            PartNumber):

        self.Manufacturer = Manufacturer
        self.PartNumber = PartNumber

    # getters
    @property
    def Manufacturer(self):
        return self._Manufacturer

    @property
    def PartNumber(self):
        return self._PartNumber

    # setters
    @Manufacturer.setter
    def Manufacturer(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="Manufacturer")
        self._Manufacturer = val

    @PartNumber.setter
    def PartNumber(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="PartNumber")
        self._PartNumber = val


class HallsensorSettings:

    def __init__(
            self,
            MaxOperatingFrequency,
            SupplyVoltageMin,
            SupplyVoltageMax,
            MaxCurrentConsumption,
            PPR):

        self.MaxOperatingFrequency = MaxOperatingFrequency
        self.SupplyVoltageMin = SupplyVoltageMin
        self.SupplyVoltageMax = SupplyVoltageMax
        self.MaxCurrentConsumption = MaxCurrentConsumption
        self.PPR = PPR

    # getters
    @property
    def MaxOperatingFrequency(self):
        return self._MaxOperatingFrequency

    @property
    def SupplyVoltageMin(self):
        return self._SupplyVoltageMin

    @property
    def SupplyVoltageMax(self):
        return self._SupplyVoltageMax

    @property
    def MaxCurrentConsumption(self):
        return self._MaxCurrentConsumption

    @property
    def PPR(self):
        return self._PPR

    # setters
    @MaxOperatingFrequency.setter
    def MaxOperatingFrequency(self, val):
        _check_castability(val,
                           c_float,
                           varname="MaxOperatingFrequency")
        self._MaxOperatingFrequency = val

    @SupplyVoltageMin.setter
    def SupplyVoltageMin(self, val):
        _check_castability(val,
                           c_float,
                           varname="SupplyVoltageMin")
        self._SupplyVoltageMin = val

    @SupplyVoltageMax.setter
    def SupplyVoltageMax(self, val):
        _check_castability(val,
                           c_float,
                           varname="SupplyVoltageMax")
        self._SupplyVoltageMax = val

    @MaxCurrentConsumption.setter
    def MaxCurrentConsumption(self, val):
        _check_castability(val,
                           c_float,
                           varname="MaxCurrentConsumption")
        self._MaxCurrentConsumption = val

    @PPR.setter
    def PPR(self, val):
        _check_castability(val,
                           c_uint,
                           varname="PPR")
        self._PPR = val


class GearInformation:

    def __init__(
            self,
            Manufacturer,
            PartNumber):

        self.Manufacturer = Manufacturer
        self.PartNumber = PartNumber

    # getters
    @property
    def Manufacturer(self):
        return self._Manufacturer

    @property
    def PartNumber(self):
        return self._PartNumber

    # setters
    @Manufacturer.setter
    def Manufacturer(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="Manufacturer")
        self._Manufacturer = val

    @PartNumber.setter
    def PartNumber(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="PartNumber")
        self._PartNumber = val


class GearSettings:

    def __init__(
            self,
            ReductionIn,
            ReductionOut,
            RatedInputTorque,
            RatedInputSpeed,
            MaxOutputBacklash,
            InputInertia,
            Efficiency):

        self.ReductionIn = ReductionIn
        self.ReductionOut = ReductionOut
        self.RatedInputTorque = RatedInputTorque
        self.RatedInputSpeed = RatedInputSpeed
        self.MaxOutputBacklash = MaxOutputBacklash
        self.InputInertia = InputInertia
        self.Efficiency = Efficiency

    # getters
    @property
    def ReductionIn(self):
        return self._ReductionIn

    @property
    def ReductionOut(self):
        return self._ReductionOut

    @property
    def RatedInputTorque(self):
        return self._RatedInputTorque

    @property
    def RatedInputSpeed(self):
        return self._RatedInputSpeed

    @property
    def MaxOutputBacklash(self):
        return self._MaxOutputBacklash

    @property
    def InputInertia(self):
        return self._InputInertia

    @property
    def Efficiency(self):
        return self._Efficiency

    # setters
    @ReductionIn.setter
    def ReductionIn(self, val):
        _check_castability(val,
                           c_float,
                           varname="ReductionIn")
        self._ReductionIn = val

    @ReductionOut.setter
    def ReductionOut(self, val):
        _check_castability(val,
                           c_float,
                           varname="ReductionOut")
        self._ReductionOut = val

    @RatedInputTorque.setter
    def RatedInputTorque(self, val):
        _check_castability(val,
                           c_float,
                           varname="RatedInputTorque")
        self._RatedInputTorque = val

    @RatedInputSpeed.setter
    def RatedInputSpeed(self, val):
        _check_castability(val,
                           c_float,
                           varname="RatedInputSpeed")
        self._RatedInputSpeed = val

    @MaxOutputBacklash.setter
    def MaxOutputBacklash(self, val):
        _check_castability(val,
                           c_float,
                           varname="MaxOutputBacklash")
        self._MaxOutputBacklash = val

    @InputInertia.setter
    def InputInertia(self, val):
        _check_castability(val,
                           c_float,
                           varname="InputInertia")
        self._InputInertia = val

    @Efficiency.setter
    def Efficiency(self, val):
        _check_castability(val,
                           c_float,
                           varname="Efficiency")
        self._Efficiency = val


class AccessoriesSettings:

    def __init__(
            self,
            MagneticBrakeInfo,
            MBRatedVoltage,
            MBRatedCurrent,
            MBTorque,
            MBSettings,
            TemperatureSensorInfo,
            TSMin,
            TSMax,
            TSGrad,
            TSSettings,
            LimitSwitchesSettings):

        self.MagneticBrakeInfo = MagneticBrakeInfo
        self.MBRatedVoltage = MBRatedVoltage
        self.MBRatedCurrent = MBRatedCurrent
        self.MBTorque = MBTorque
        self.MBSettings = MBSettings
        self.TemperatureSensorInfo = TemperatureSensorInfo
        self.TSMin = TSMin
        self.TSMax = TSMax
        self.TSGrad = TSGrad
        self.TSSettings = TSSettings
        self.LimitSwitchesSettings = LimitSwitchesSettings

    # getters
    @property
    def MagneticBrakeInfo(self):
        return self._MagneticBrakeInfo

    @property
    def MBRatedVoltage(self):
        return self._MBRatedVoltage

    @property
    def MBRatedCurrent(self):
        return self._MBRatedCurrent

    @property
    def MBTorque(self):
        return self._MBTorque

    @property
    def MBSettings(self):
        return self._MBSettings

    @property
    def TemperatureSensorInfo(self):
        return self._TemperatureSensorInfo

    @property
    def TSMin(self):
        return self._TSMin

    @property
    def TSMax(self):
        return self._TSMax

    @property
    def TSGrad(self):
        return self._TSGrad

    @property
    def TSSettings(self):
        return self._TSSettings

    @property
    def LimitSwitchesSettings(self):
        return self._LimitSwitchesSettings

    # setters
    @MagneticBrakeInfo.setter
    def MagneticBrakeInfo(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="MagneticBrakeInfo")
        self._MagneticBrakeInfo = val

    @MBRatedVoltage.setter
    def MBRatedVoltage(self, val):
        _check_castability(val,
                           c_float,
                           varname="MBRatedVoltage")
        self._MBRatedVoltage = val

    @MBRatedCurrent.setter
    def MBRatedCurrent(self, val):
        _check_castability(val,
                           c_float,
                           varname="MBRatedCurrent")
        self._MBRatedCurrent = val

    @MBTorque.setter
    def MBTorque(self, val):
        _check_castability(val,
                           c_float,
                           varname="MBTorque")
        self._MBTorque = val

    @MBSettings.setter
    def MBSettings(self, val):
        _check_castability(val,
                           c_uint,
                           varname="MBSettings")
        self._MBSettings = val

    @TemperatureSensorInfo.setter
    def TemperatureSensorInfo(self, val):
        _check_castability(val,
                           c_char_p,
                           varname="TemperatureSensorInfo")
        self._TemperatureSensorInfo = val

    @TSMin.setter
    def TSMin(self, val):
        _check_castability(val,
                           c_float,
                           varname="TSMin")
        self._TSMin = val

    @TSMax.setter
    def TSMax(self, val):
        _check_castability(val,
                           c_float,
                           varname="TSMax")
        self._TSMax = val

    @TSGrad.setter
    def TSGrad(self, val):
        _check_castability(val,
                           c_float,
                           varname="TSGrad")
        self._TSGrad = val

    @TSSettings.setter
    def TSSettings(self, val):
        _check_castability(val,
                           c_uint,
                           varname="TSSettings")
        self._TSSettings = val

    @LimitSwitchesSettings.setter
    def LimitSwitchesSettings(self, val):
        _check_castability(val,
                           c_uint,
                           varname="LimitSwitchesSettings")
        self._LimitSwitchesSettings = val


class InitRandom:

    def __init__(
            self,
            key):

        self.key = key

    # getters
    @property
    def key(self):
        return self._key

    # setters
    @key.setter
    def key(self, val):
        _check_castability(val,
                           c_uint8 * 16,
                           varname="key")
        self._key = val


class GloballyUniqueIdentifier:

    def __init__(
            self,
            UniqueID0,
            UniqueID1,
            UniqueID2,
            UniqueID3):

        self.UniqueID0 = UniqueID0
        self.UniqueID1 = UniqueID1
        self.UniqueID2 = UniqueID2
        self.UniqueID3 = UniqueID3

    # getters
    @property
    def UniqueID0(self):
        return self._UniqueID0

    @property
    def UniqueID1(self):
        return self._UniqueID1

    @property
    def UniqueID2(self):
        return self._UniqueID2

    @property
    def UniqueID3(self):
        return self._UniqueID3

    # setters
    @UniqueID0.setter
    def UniqueID0(self, val):
        _check_castability(val,
                           c_uint,
                           varname="UniqueID0")
        self._UniqueID0 = val

    @UniqueID1.setter
    def UniqueID1(self, val):
        _check_castability(val,
                           c_uint,
                           varname="UniqueID1")
        self._UniqueID1 = val

    @UniqueID2.setter
    def UniqueID2(self, val):
        _check_castability(val,
                           c_uint,
                           varname="UniqueID2")
        self._UniqueID2 = val

    @UniqueID3.setter
    def UniqueID3(self, val):
        _check_castability(val,
                           c_uint,
                           varname="UniqueID3")
        self._UniqueID3 = val


# --- Public API v2 functions ---
def set_feedback_settings(device_id: DeviceT,
                          settings: FeedbackSettings) -> None:
    """Feedback settings.
    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param: feedback settings
    :type settings: FeedbackSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, FeedbackSettings):
        raise TypeError("settings must be of type FeedbackSettings. <{}>"
                        "was got.".format(type(settings)))
    feedback_settings = feedback_settings_t(settings.IPS,
                                            settings.FeedbackType,
                                            settings.FeedbackFlags,
                                            settings.CountsPerTurn)
    _check_result(lib.set_feedback_settings(device_id,
                                            byref(feedback_settings)))


def get_feedback_settings(device_id: DeviceT) -> FeedbackSettings:
    """Feedback settings.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: feedback settings
    :rtype: FeedbackSettings
    """
    _check_device_id(device_id)
    feedback_settings = feedback_settings_t()
    _check_result(lib.get_feedback_settings(device_id,
                                            byref(feedback_settings)))
    return FeedbackSettings(feedback_settings.IPS,
                            feedback_settings.FeedbackType,
                            feedback_settings.FeedbackFlags,
                            feedback_settings.CountsPerTurn)


def set_home_settings(device_id: DeviceT,
                      settings: HomeSettings) -> None:
    """Set home settings.

    This function send structure with calibrating position settings to
    controller's memory.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: home settings
    :type settings: HomeSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, HomeSettings):
        raise TypeError("settings must be of type HomeSettings. <{}>"
                        " was got.".format(type(settings)))
    home_settings = home_settings_t(settings.FastHome,
                                    settings.uFastHome,
                                    settings.SlowHome,
                                    settings.uSlowHome,
                                    settings.HomeDelta,
                                    settings.uHomeDelta,
                                    settings.HomeFlags)
    _check_result(lib.set_home_settings(device_id, byref(home_settings)))


def get_home_settings(device_id: DeviceT) -> HomeSettings:
    """Read home settings.

    This function fill structure with settings of calibrating position.
    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: home settings
    :rtype: HomeSettings
    """
    _check_device_id(device_id)
    home_settings = home_settings_t()
    _check_result(lib.get_home_settings(device_id, byref(home_settings)))
    return HomeSettings(home_settings.FastHome,
                        home_settings.uFastHome,
                        home_settings.SlowHome,
                        home_settings.uSlowHome,
                        home_settings.HomeDelta,
                        home_settings.uHomeDelta,
                        home_settings.HomeFlags)


def set_home_settings_calb(device_id: DeviceT,
                           settings: HomeSettingsCalb,
                           calibration: Calibration) -> None:
    """Set home settings which use user units.

    This function send structure with calibrating position settings to
    controller's memory.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: calibration home settings
    :type settings: HomeSettingsCalb
    :param calibration: calibration
    :type calibration: Calibration
    """
    _check_device_id(device_id)
    if not isinstance(settings, HomeSettingsCalb):
        raise TypeError("settings must be of type HomeSettingsCalb. <{}>"
                        " was got.".format(type(settings)))
    if not isinstance(calibration, Calibration):
        raise TypeError("calibration must be of type Calibration. <{}>"
                        " was got.".format(type(calibration)))
    home_settings = home_settings_calb_t(settings.FastHome,
                                         settings.SlowHome,
                                         settings.HomeDelta,
                                         settings.HomeFlags)
    calib = calibration_t(calibration.A, calibration.MicrostepMode)
    _check_result(lib.set_home_settings_calb(device_id,
                                             byref(home_settings),
                                             byref(calib)))


def get_home_settings_calb(device_id: DeviceT,
                           calibration: Calibration) -> HomeSettingsCalb:
    """Read home settings which use user units.

    This function fill structure with settings of calibrating position.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param calibration: calibration
    :type calibration: Calibration
    :return: calibration home settings
    :rtype: HomeSettingsCalb
    """
    _check_device_id(device_id)
    if not isinstance(calibration, Calibration):
        raise TypeError("calibration must be of type Calibration. <{}>"
                        " was got.".format(type(calibration)))
    home_settings = home_settings_calb_t()
    calib = calibration_t(calibration.A, calibration.MicrostepMode)
    _check_result(lib.get_home_settings_calb(device_id,
                                             byref(home_settings),
                                             byref(calib)))
    return HomeSettingsCalb(home_settings.FastHome,
                            home_settings.SlowHome,
                            home_settings.HomeDelta,
                            home_settings.HomeFlags)


def set_move_settings(device_id: DeviceT,
                      settings: MoveSettings) -> None:
    _check_device_id(device_id)
    if not isinstance(settings, MoveSettings):
        raise TypeError("settings must be of type MoveSettings. <{}>"
                        " was MoveSettings.".format(type(settings)))
    move_settings = move_settings_t(settings.Speed,
                                    settings.uSpeed,
                                    settings.Accel,
                                    settings.Decel,
                                    settings.AntiplaySpeed,
                                    settings.uAntiplaySpeed,
                                    settings.MoveFlags)
    _check_result(lib.set_move_settings(device_id, move_settings))


def set_move_settings_calb(device_id: DeviceT,
                           settings: MoveSettingsCalb,
                           calibration: Calibration) -> None:
    """Set command setup movement which use user units (speed, acceleration,
    threshold and etc).

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: calibration move settings
    :type settings: MoveSettingsCalb
    :param calibration: calibration
    :type calibration: Calibration
    """
    _check_device_id(device_id)
    if not isinstance(settings, MoveSettingsCalb):
        raise TypeError("settings must be of type MoveSettingsCalb."
                        " <{}> was got.".format(type(settings)))
    if not isinstance(calibration, Calibration):
        raise TypeError("calibration must be of type Calibration. <{}>"
                        " was got.".format(type(calibration)))
    move_settings = move_settings_calb_t(settings.Speed,
                                         settings.Accel,
                                         settings.Decel,
                                         settings.AntiplaySpeed,
                                         settings.MoveFlags)
    calib = calibration_t(calibration.A, calibration.MicrostepMode)
    _check_result(lib.set_move_settings_calb(device_id,
                                             byref(move_settings),
                                             byref(calib)))


def get_move_settings(device_id: DeviceT) -> MoveSettings:
    """Read command setup movement (speed, acceleration, threshold and etc).

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: move settings
    :rtype: MoveSettings
    """
    _check_device_id(device_id)
    move_settings = move_settings_t()
    _check_result(lib.get_move_settings(device_id, byref(move_settings)))
    return MoveSettings(move_settings.Speed,
                        move_settings.uSpeed,
                        move_settings.Accel,
                        move_settings.Decel,
                        move_settings.AntiplaySpeed,
                        move_settings.uAntiplaySpeed,
                        move_settings.MoveFlags)


def get_move_settings_calb(device_id: DeviceT,
                           calibration: Calibration) -> MoveSettingsCalb:
    """Read command setup movement which use user units (speed, acceleration,
    threshold and etc).

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param calibration: calibration
    :type calibration: Calibration
    :retunr: calibration move settings
    :rtype: MoveSettingsCalb
    """
    _check_device_id(device_id)
    if not isinstance(calibration, Calibration):
        raise TypeError("calibration must be of type Calibration. <{}>"
                        " was got.".format(type(calibration)))
    move_settings = move_settings_calb_t()
    calib = calibration_t(calibration.A, calibration.MicrostepMode)
    _check_result(lib.get_move_settings_calb(device_id,
                                             byref(move_settings),
                                             byref(calib)))
    return MoveSettingsCalb(move_settings.Speed,
                            move_settings.Accel,
                            move_settings.Decel,
                            move_settings.AntiplaySpeed,
                            move_settings.MoveFlags)


def set_engine_settings(device_id: DeviceT,
                        settings: EngineSettings) -> None:
    """Set engine settings.

    This function send structure with set of engine settings to controller's
    memory. These settings specify motor shaft movement algorithm, list of
    limitations and rated characteristics. Use it when you change motor,
    encoder, positioner etc. Please note that wrong engine settings lead to
    device malfunction, can lead to irreversible damage of board.

    :param device_id: _descran identifier of deviceiption_
    :type device_id: DeviceT
    :param settings: engine settings
    :type settings: EngineSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, EngineSettings):
        raise TypeError("settings must be of type EngineSettings."
                        " <{}> was got.".format(type(settings)))
    engine_settings = engine_settings_t(settings.NomVoltage,
                                        settings.NomCurrent,
                                        settings.NomSpeed,
                                        settings.uNomSpeed,
                                        settings.EngineFlags,
                                        settings.Antiplay,
                                        settings.MicrostepMode,
                                        settings.StepsPerRev)
    _check_result(lib.set_engine_settings(device_id, byref(engine_settings)))


def set_engine_settings_calb(device_id: DeviceT,
                             settings: EngineSettingsCalb,
                             calibration: Calibration) -> None:
    """Set engine settings which use user units.

    This function send structure with set of engine settings to controller's
    memory. These settings specify motor shaft movement algorithm, list of
    limitations and rated characteristics. Use it when you change motor,
    encoder, positioner etc. Please note that wrong engine settings lead to
    device malfunction, can lead to irreversible damage of board.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: calibration engine settings
    :type settings: EngineSettingsCalb
    :param calibration: calibration
    :type calibration: Calibration
    """
    _check_device_id(device_id)
    if not isinstance(settings, EngineSettingsCalb):
        raise TypeError("settings must be of type EngineSettingsCalb."
                        " <{}> was got.".format(type(settings)))
    if not isinstance(calibration, Calibration):
        raise TypeError("calibration must be of type Calibration. <{}>"
                        " was got.".format(type(calibration)))
    engine_settings = engine_settings_calb_t(settings.NomVoltage,
                                             settings.NomCurrent,
                                             settings.NomSpeed,
                                             settings.EngineFlags,
                                             settings.Antiplay,
                                             settings.MicrostepMode,
                                             settings.StepsPerRev)
    calib = calibration_t(calibration.A, calibration.MicrostepMode)
    _check_result(lib.set_engine_settings_calb(device_id,
                                               byref(engine_settings),
                                               byref(calib)))


def get_engine_settings(device_id: DeviceT) -> EngineSettings:
    """Read engine settings.

    This function fill structure with set of useful motor settings stored in
    controller's memory. These settings specify motor shaft movement algorithm,
    list of limitations and rated characteristics.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: engine settings
    :rtype: EngineSettings
    """
    _check_device_id(device_id)
    engine_settings = engine_settings_t()
    _check_result(lib.get_engine_settings(device_id, byref(engine_settings)))
    return EngineSettings(engine_settings.NomVoltage,
                          engine_settings.NomCurrent,
                          engine_settings.NomSpeed,
                          engine_settings.uNomSpeed,
                          engine_settings.EngineFlags,
                          engine_settings.Antiplay,
                          engine_settings.MicrostepMode,
                          engine_settings.StepsPerRev)


def get_engine_settings_calb(device_id: DeviceT,
                             calibration: Calibration) -> EngineSettingsCalb:
    """Read engine settings which use user units.

    This function fill structure with set of useful motor settings stored in
    controller's memory. These settings specify motor shaft movement algorithm,
    list of limitations and rated characteristics.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: calibration engine settings
    :rtype: EngineSettingsCalb
    """
    _check_device_id(device_id)
    if not isinstance(calibration, Calibration):
        raise TypeError("calibration must be of type Calibration. <{}>"
                        " was got.".format(type(calibration)))
    engine_settings = engine_settings_calb_t()
    calib = calibration_t(calibration.A, calibration.MicrostepMode)
    _check_result(lib.get_engine_settings_calb(device_id,
                                               byref(engine_settings),
                                               byref(calib)))
    return EngineSettingsCalb(engine_settings.NomVoltage,
                              engine_settings.NomCurrent,
                              engine_settings.NomSpeed,
                              engine_settings.EngineFlags,
                              engine_settings.Antiplay,
                              engine_settings.MicrostepMode,
                              engine_settings.StepPerRev)


def set_entype_settings(device_id: DeviceT,
                        settings: EntypeSettings) -> None:
    """Set engine type and driver type.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: entype settings
    :type settings: EntypeSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, EntypeSettings):
        raise TypeError("settings must be of type EntypeSettings."
                        " <{}> was got.".format(type(settings)))
    entype_settings = entype_settings_t(settings.EngineType,
                                        settings.DriverType)
    _check_result(lib.set_entype_settings(device_id,
                                          byref(entype_settings)))


def get_entype_settings(device_id: DeviceT) -> EntypeSettings:
    """Return engine type and driver type.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: entype settings
    :rtype: EntypeSettings
    """
    _check_device_id(device_id)
    entype_settings = entype_settings_t()
    _check_result(lib.get_entype_settings(device_id,
                                          byref(entype_settings)))
    return EntypeSettings(entype_settings.EngineType,
                          entype_settings.DriverType)


def set_power_settings(device_id: DeviceT,
                       settings: PowerSettings) -> None:
    """Set settings of step motor power control.

    Used with stepper motor only.

    :param device_id: an identifier of devic
    :type device_id: DeviceT
    :param settings: power settings
    :type settings: PowerSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, PowerSettings):
        raise TypeError("settings must be of type PowerSettings."
                        " <{}> was got.".format(type(settings)))
    power_settings = power_settings_t(settings.HoldCurrent,
                                      settings.CurrReductDelay,
                                      settings.PowerOffDelay,
                                      settings.CurrentSetTime,
                                      settings.PowerFlags)
    _check_result(lib.set_power_settings(device_id, byref(power_settings)))


def get_power_settings(device_id: DeviceT) -> PowerSettings:
    """Read settings of step motor power control.

    Used with stepper motor only.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: power settings
    :rtype: PowerSettings
    """
    _check_device_id(device_id)
    power_settings = power_settings_t()
    _check_result(lib.get_power_settings(device_id, byref(power_settings)))
    return PowerSettings(power_settings.HoldCurrent,
                         power_settings.CurrReductDelay,
                         power_settings.PowerOffDelay,
                         power_settings.CurrentSetTime,
                         power_settings.PowerFlags)


def set_secure_settings(device_id: DeviceT,
                        settings: SecureSettings) -> None:
    """Set protection settings.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: secure settings
    :type settings: SecureSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, SecureSettings):
        raise TypeError("settings must be of type SecureSettings."
                        " <{}> was got.".format(type(settings)))
    secure_settings = secure_settings_t(settings.LowUpwrOff,
                                        settings.CriticalIpwr,
                                        settings.CriticalUpwr,
                                        settings.CriticalT,
                                        settings.CriticalIusb,
                                        settings.CriticalUusb,
                                        settings.MinimumUusb,
                                        settings.Flags)
    _check_result(lib.set_secure_settings(device_id, byref(secure_settings)))


def get_secure_settings(device_id: DeviceT) -> SecureSettings:
    """Read protection settings.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: secure settings
    :rtype: SecureSettings
    """
    _check_device_id(device_id)
    secure_settings = secure_settings_t()
    _check_result(lib.get_secure_settings(device_id, byref(secure_settings)))
    return SecureSettings(secure_settings.LowUpwrOff,
                          secure_settings.CriticalIpwr,
                          secure_settings.CriticalUpwr,
                          secure_settings.CriticalT,
                          secure_settings.CriticalIusb,
                          secure_settings.CriticalUusb,
                          secure_settings.MinimumUusb,
                          secure_settings.Flags)


def set_edges_settings(device_id: DeviceT,
                       settings: EdgesSettings) -> None:
    """Set border and limit switches settings.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: edges settings
    :type settings: EdgesSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, EdgesSettings):
        raise TypeError("settings must be of type EdgesSettings."
                        " <{}> was got.".format(type(settings)))
    edges_settings = edges_settings_t(settings.BorderFlags,
                                      settings.EnderFlags,
                                      settings.LeftBorder,
                                      settings.uLeftBorder,
                                      settings.RightBorder,
                                      settings.uRightBorder)
    _check_result(lib.set_edges_settings(device_id, byref(edges_settings)))


def set_edges_settings_calb(device_id: DeviceT,
                            settings: EdgesSettingsCalb,
                            calibration: Calibration) -> None:
    """Set border and limit switches settings which use user units.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: calibration edges settings
    :type settings: EdgesSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, EdgesSettingsCalb):
        raise TypeError("settings must be of type EdgesSettingsCalb."
                        " <{}> was got.".format(type(settings)))
    if not isinstance(calibration, Calibration):
        raise TypeError("calibration must be of type Calibration. <{}>"
                        " was got.".format(type(calibration)))
    edges_settings = edges_settings_calb_t(settings.BorderFlags,
                                           settings.EnderFlags,
                                           settings.LeftBorder,
                                           settings.RightBorder)
    calib = calibration_t(calibration.A, calibration.MicrostepMode)
    _check_result(lib.set_edges_settings_calb(device_id,
                                              byref(edges_settings),
                                              byref(calib)))


def get_edges_settings(device_id: DeviceT) -> EdgesSettings:
    """Read border and limit switches settings.

    :param device_id: an identifier of devic
    :type device_id: DeviceT
    :return: edges settings
    :rtype: EdgesSettings
    """
    _check_device_id(device_id)
    edges_settings = edges_settings_t()
    _check_result(lib.get_edges_settings(device_id, byref(edges_settings)))
    return EdgesSettings(edges_settings.BorderFlags,
                         edges_settings.EnderFlags,
                         edges_settings.LeftBorder,
                         edges_settings.uLeftBorder,
                         edges_settings.RightBorder,
                         edges_settings.uRightBorder)


def get_edges_settings_calb(device_id: DeviceT,
                            calibration: Calibration) -> EdgesSettingsCalb:
    """Read border and limit switches settings.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: calibration edges settings
    :rtype: EdgesSettingsCalb
    """
    _check_device_id(device_id)
    if not isinstance(calibration, Calibration):
        raise TypeError("calibration must be of type Calibration. <{}>"
                        " was got.".format(type(calibration)))
    edges_settings = edges_settings_calb_t()
    calib = calibration_t(calibration.A, calibration.MicrostepMode)
    _check_result(lib.get_edges_settings_calb(device_id,
                                              byref(edges_settings),
                                              byref(calib)))
    return EdgesSettingsCalb(edges_settings.BorderFlags,
                             edges_settings.EnderFlags,
                             edges_settings.LeftBorder,
                             edges_settings.RightBorder)


def set_pid_settings(device_id: DeviceT,
                     settings: PidSettings) -> None:
    """Set PID settings.

    This function send structure with set of PID factors to controller's
    memory. These settings specify behaviour of PID routine for positioner.
    These factors are slightly different for different positioners. All boards
    are supplied with standard set of PID setting on controller's flash
    memory. Please use it for loading new PID settings when you change
    positioner. Please note that wrong PID settings lead to device malfunction.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: PID settings
    :type settings: PidSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, PidSettings):
        raise TypeError("settings must be of type PidSettings."
                        " <{}> was got.".format(type(settings)))
    pid_settings = pid_settings_t(settings.KpU,
                                  settings.KiU,
                                  settings.KdU,
                                  settings.Kpf,
                                  settings.Kif,
                                  settings.Kdf)
    _check_result(lib.set_pid_settings(device_id, byref(pid_settings)))


def get_pid_settings(device_id: DeviceT) -> PidSettings:
    """Read PID settings.

    This function fill structure with set of motor PID settings stored in
    controller's memory. These settings specify behaviour of PID routine
    for positioner. These factors are slightly different for different
    positioners. All boards are supplied with standard set of PID setting
    on controller's flash memory.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: PID settings
    :rtype: PidSettings
    """
    _check_device_id(device_id)
    pid_settings = pid_settings_t()
    _check_result(lib.get_pid_settings(device_id, byref(pid_settings)))
    return PidSettings(pid_settings.KpU,
                       pid_settings.KiU,
                       pid_settings.KdU,
                       pid_settings.Kpf,
                       pid_settings.Kif,
                       pid_settings.Kdf)


def set_sync_in_settings(device_id: DeviceT,
                         settings: SyncInSettings) -> None:
    """Set input synchronization settings.

    This function send structure with set of input synchronization settings,
    that specify behaviour of input synchronization, to controller's memory.
    All boards are supplied with standard set of these settings.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: sync in settings
    :type settings: SyncInSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, SyncInSettings):
        raise TypeError("settings must be of type SyncInSettings."
                        " <{}> was got.".format(type(settings)))
    sync_in_settings = sync_in_settings_t(settings.SyncInFlags,
                                          settings.ClutterTime,
                                          settings.Position,
                                          settings.uPosition,
                                          settings.Speed,
                                          settings.uSpeed)
    _check_result(lib.set_sync_in_settings(device_id, byref(sync_in_settings)))


def set_sync_in_settings_calb(device_id: DeviceT,
                              settings: SyncInSettingsCalb,
                              calibration: Calibration) -> None:
    """Set input synchronization settings.

    This function send structure with set of input synchronization settings,
    that specify behaviour of input synchronization, to controller's memory.
    All boards are supplied with standard set of these settings.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: sync in settings
    :type settings: SyncInSettings
    :param calibration: calibration
    :type calibration: Calibration
    """
    _check_device_id(device_id)
    if not isinstance(settings, SyncInSettingsCalb):
        raise TypeError("settings must be of type SyncInSettingsCalb."
                        " <{}> was got.".format(type(settings)))
    if not isinstance(calibration, Calibration):
        raise TypeError("calibration must be of type Calibration. <{}>"
                        " was got.".format(type(calibration)))
    sync_in_settings = sync_in_settings_calb_t(settings.SyncInFlags,
                                               settings.ClutterTime,
                                               settings.Position,
                                               settings.Speed)
    calib = calibration_t(calibration.A, calibration.MicrostepMode)
    _check_result(lib.set_sync_in_settings_calb(device_id,
                                                byref(sync_in_settings),
                                                byref(calib)))


def get_sync_in_settings(device_id: DeviceT) -> SyncInSettings:
    """Read input synchronization settings.

    This function fill structure with set of input synchronization settings,
    modes, periods and flags, that specify behaviour of input synchronization.
    All boards are supplied with standard set of these settings.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: sync in settings
    :rtype: SyncInSettings
    """
    _check_device_id(device_id)
    sync_in_settings = sync_in_settings_t()
    _check_result(lib.get_sinc_in_settings(device_id, byref(sync_in_settings)))
    return SyncInSettings(sync_in_settings.SyncInFlags,
                          sync_in_settings.ClutterTime,
                          sync_in_settings.Position,
                          sync_in_settings.uPosition,
                          sync_in_settings.Speed,
                          sync_in_settings.uSpeed)


def get_sync_in_settings_calb(device_id: DeviceT,
                              calibration: Calibration) -> SyncInSettingsCalb:
    """Read input synchronization settings which use user units.

    This function fill structure with set of input synchronization settings,
    modes, periods and flags, that specify behaviour of input synchronization.
    All boards are supplied with standard set of these settings.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param calibration: calibration
    :type calibration: Calibration
    :return: calibration sync in settings
    :rtype: SyncInSettingsCalb
    """
    _check_device_id(device_id)
    if not isinstance(calibration, Calibration):
        raise TypeError("calibration must be of type Calibration. <{}>"
                        " was got.".format(type(calibration)))
    sync_in_settings = sync_in_settings_calb_t()
    calib = calibration_t(calibration.A, calibration.MicrostepMode)
    _check_result(lib.get_sinc_in_settings_calb(device_id,
                                                byref(sync_in_settings),
                                                byref(calib)))
    return SyncInSettingsCalb(sync_in_settings.SyncInFlags,
                              sync_in_settings.ClutterTime,
                              sync_in_settings.Position,
                              sync_in_settings.Speed)


def set_sync_out_settings(device_id: DeviceT,
                          settings: SyncOutSettings) -> None:
    """Set output synchronization settings.

    This function send structure with set of output synchronization settings,
    that specify behaviour of output synchronization, to controller's memory.
    All boards are supplied with standard set of these settings.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: sync out settings
    :type settings: SyncOutSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, SyncOutSettings):
        raise TypeError("settings must be of type SyncOutSettings."
                        " <{}> was got.".format(type(settings)))
    sync_out_settings = sync_out_settings_t(settings.SyncOutFlags,
                                            settings.SyncOutPulseSteps,
                                            settings.SyncOutPeriod,
                                            settings.Accuracy,
                                            settings.uAccuracy)
    _check_result(lib.set_sync_out_settings(device_id,
                                            byref(sync_out_settings)))


def set_sync_out_settings_calb(device_id: DeviceT,
                               settings: SyncOutSettingsCalb,
                               calibration: Calibration) -> None:
    """Set output synchronization settings which use user units.

    This function send structure with set of output synchronization settings,
    that specify behaviour of output synchronization, to controller's memory.
    All boards are supplied with standard set of these settings.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: calibration sync out settings
    :type settings: SyncOutSettingsCalb
    :param calibration: calibration
    :type calibration: Calibration
    """
    _check_device_id(device_id)
    if not isinstance(settings, SyncOutSettingsCalb):
        raise TypeError("settings must be of type SyncOutSettingsCalb."
                        " <{}> was got.".format(type(settings)))
    if not isinstance(calibration, Calibration):
        raise TypeError("calibration must be of type Calibration. <{}>"
                        " was got.".format(type(calibration)))
    sync_out_settings = sync_out_settings_calb_t(settings.SyncOutFlags,
                                                 settings.SyncOutPulseSteps,
                                                 settings.SyncOutPeriod,
                                                 settings.Accuracy)
    calib = calibration_t(calibration.A, calibration.MicrostepMode)
    _check_result(lib.set_sync_out_settings_calb(device_id,
                                                 byref(sync_out_settings),
                                                 byref(calib)))


def get_sync_out_settings(device_id: DeviceT) -> SyncOutSettings:
    """Read output synchronization settings.

    This function fill structure with set of output synchronization settings,
    modes, periods and flags, that specify behaviour of output
    synchronization. All boards are supplied with standard set of these
    settings.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: sync out settings
    :rtype: SyncOutSettings
    """
    _check_device_id(device_id)
    sync_out_settings = sync_out_settings_t()
    _check_result(lib.get_sinc_out_settings(device_id,
                                            byref(sync_out_settings)))
    return SyncOutSettings(sync_out_settings.SyncOutFlags,
                           sync_out_settings.SyncOutPulseSteps,
                           sync_out_settings.SyncOutPeriod,
                           sync_out_settings.Accuracy,
                           sync_out_settings.uAccuracy)


def get_sync_out_settings_calb(
        device_id: DeviceT, calibration: Calibration) -> SyncOutSettingsCalb:
    """Read output synchronization settings which use user units.

    This function fill structure with set of output synchronization settings,
    modes, periods and flags, that specify behaviour of output
    synchronization. All boards are supplied with standard set of these
    settings.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param calibration: calibration
    :type calibration: Calibration
    :return: calibration sync out settings
    :rtype: SyncOutSettingsCalb
    """
    _check_device_id(device_id)
    if not isinstance(calibration, Calibration):
        raise TypeError("calibration must be of type Calibration. <{}>"
                        " was got.".format(type(calibration)))
    sync_out_settings = sync_out_settings_calb_t()
    calib = calibration_t(calibration.A, calibration.MicrostepMode)
    _check_result(lib.get_sinc_out_settings_calb(device_id,
                                                 byref(sync_out_settings),
                                                 byref(calib)))
    return SyncOutSettingsCalb(sync_out_settings.SyncOutFlags,
                               sync_out_settings.SyncOutPulseSteps,
                               sync_out_settings.SyncOutPeriod,
                               sync_out_settings.Accuracy)


def set_extio_settings(device_id: DeviceT,
                       settings: ExtioSettings) -> None:
    """Set EXTIO settings.

    This function writes a structure with a set of EXTIO settings to
    controller's memory. By default input event are signalled through rising
    front and output states are signalled by high logic state.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: extio settings
    :type settings: ExtioSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, ExtioSettings):
        raise TypeError("settings must be of type ExtioSettings."
                        " <{}> was got.".format(type(settings)))
    extio_settings = extio_settings_t(settings.EXTIOSetupFlags,
                                      settings.EXTIOModeFlags)
    _check_result(lib.set_extio_settings(device_id, byref(extio_settings)))


def get_extio_settings(device_id: DeviceT) -> ExtioSettings:
    """Read EXTIO settings.

    This function reads a structure with a set of EXTIO settings from
    controller's memory.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: extio settings
    :rtype: ExtioSettings
    """
    _check_device_id(device_id)
    extio_settings = extio_settings_t()
    _check_result(lib.get_extio_settings(device_id, byref(extio_settings)))
    return ExtioSettings(extio_settings.EXTIOSetupFlags,
                         extio_settings.EXTIOModeFlags)


def set_brake_settings(device_id: DeviceT,
                       settings: BrakeSettings) -> None:
    """Set settings of brake control.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: brake settings
    :type settings: BrakeSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, BrakeSettings):
        raise TypeError("settings must be of type BrakeSettings."
                        " <{}> was got.".format(type(settings)))
    brake_settings = brake_settings_t(settings.t1,
                                      settings.t2,
                                      settings.t3,
                                      settings.t4,
                                      settings.BrakeFlags)
    _check_result(lib.set_brake_settings(device_id, byref(brake_settings)))


def get_brake_settings(device_id: DeviceT) -> BrakeSettings:
    """Read settings of brake control.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: brake settings
    :rtype: BrakeSettings
    """
    _check_device_id(device_id)
    brake_settings = brake_settings_t()
    _check_result(lib.get_brake_settings(device_id, byref(brake_settings)))
    return BrakeSettings(brake_settings.t1,
                         brake_settings.t2,
                         brake_settings.t3,
                         brake_settings.t4,
                         brake_settings.BrakeFlags)


def set_control_settings(device_id: DeviceT,
                         settings: ControlSettings) -> None:
    """Set settings of motor control.

    When choosing CTL_MODE = 1 switches motor control with the joystick. In
    this mode, the joystick to the maximum engine tends Move at MaxSpeed [i],
    where i = 0 if the previous use This mode is not selected another i.
    Buttons switch the room rate i. When CTL_MODE = 2 is switched on motor
    control using the Left / right. When you click on the button motor starts
    to move in the appropriate direction at a speed MaxSpeed [0], at the end
    of time Timeout [i] motor move at a speed MaxSpeed [i+1]. at Transition
    from MaxSpeed [i] on MaxSpeed [i +1] to acceleration, as usual.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: control settings
    :type settings: ControlSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, ControlSettings):
        raise TypeError("settings must be of type ControlSettings."
                        " <{}> was got.".format(type(settings)))
    control_settings = control_settings_t(settings.MaxSpeed,
                                          settings.uMaxSpeed,
                                          settings.Timeout,
                                          settings.MaxClickTime,
                                          settings.Flags,
                                          settings.DeltaPosition,
                                          settings.uDeltaPosition)
    _check_result(lib.set_control_settings(device_id, byref(control_settings)))


def set_control_settings_calb(device_id: DeviceT,
                              settings: ControlSettingsCalb,
                              calibration: Calibration) -> None:
    """Set settings of motor control which use user units.

    When choosing CTL_MODE = 1 switches motor control with the joystick. In
    this mode, the joystick to the maximum engine tends Move at MaxSpeed [i],
    where i = 0 if the previous use This mode is not selected another i.
    Buttons switch the room rate i. When CTL_MODE = 2 is switched on motor
    control using the Left / right. When you click on the button motor starts
    to move in the appropriate direction at a speed MaxSpeed [0], at the end
    of time Timeout [i] motor move at a speed MaxSpeed [i+1]. at Transition
    from MaxSpeed [i] on MaxSpeed [i +1] to acceleration, as usual.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: calibration control settings
    :type settings: ControlSettingsCalb
    :param calibration: calibration
    :type calibration: Calibration
    """
    _check_device_id(device_id)
    if not isinstance(settings, ControlSettingsCalb):
        raise TypeError("settings must be of type ControlSettingsCalb."
                        " <{}> was got.".format(type(settings)))
    if not isinstance(calibration, Calibration):
        raise TypeError("calibration must be of type Calibration. <{}>"
                        " was got.".format(type(calibration)))
    control_settings = control_settings_calb_t(settings.MaxSpeed,
                                               settings.Timeout,
                                               settings.MaxClickTime,
                                               settings.Flags,
                                               settings.DeltaPosition)
    calib = calibration_t(calibration.A, calibration.MicrostepMode)
    _check_result(lib.set_control_settings_calb(device_id,
                                                byref(control_settings),
                                                byref(calib)))


def get_control_settings(device_id: DeviceT) -> ControlSettings:
    """Read settings of motor control.

    When choosing CTL_MODE = 1 switches motor control with the joystick. In
    this mode, the joystick to the maximum engine tends Move at MaxSpeed [i],
    where i = 0 if the previous use This mode is not selected another i.
    Buttons switch the room rate i. When CTL_MODE = 2 is switched on motor
    control using the Left / right. When you click on the button motor starts
    to move in the appropriate direction at a speed MaxSpeed [0], at the end
    of time Timeout [i] motor move at a speed MaxSpeed [i+1]. at Transition
    from MaxSpeed [i] on MaxSpeed [i +1] to acceleration, as usual.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: control settings
    :rtype: ControlSettings
    """
    _check_device_id(device_id)
    control_settings = control_settings_t()
    _check_result(lib.get_control_settings(device_id, byref(control_settings)))
    return ControlSettings(control_settings.MaxSpeed,
                           control_settings.uMaxSpeed,
                           control_settings.Timeout,
                           control_settings.MaxClickTime,
                           control_settings.Flags,
                           control_settings.DeltaPosition,
                           control_settings.uDeltaPosition)


def get_control_settings_calb(device_id: DeviceT,
                              calibration: Calibration) -> ControlSettingsCalb:
    """Read settings of motor control which use user units.

    When choosing CTL_MODE = 1 switches motor control with the joystick. In
    this mode, the joystick to the maximum engine tends Move at MaxSpeed [i],
    where i = 0 if the previous use This mode is not selected another i.
    Buttons switch the room rate i. When CTL_MODE = 2 is switched on motor
    control using the Left / right. When you click on the button motor starts
    to move in the appropriate direction at a speed MaxSpeed [0], at the end
    of time Timeout [i] motor move at a speed MaxSpeed [i+1]. at Transition
    from MaxSpeed [i] on MaxSpeed [i +1] to acceleration, as usual.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param calibration: calibration
    :type calibration: Calibration
    :return: calibration control settings
    :rtype: ControlSettingsCalb
    """
    _check_device_id(device_id)
    if not isinstance(calibration, Calibration):
        raise TypeError("calibration must be of type Calibration. <{}>"
                        " was got.".format(type(calibration)))
    control_settings = control_settings_calb_t()
    calib = calibration_t(calibration.A, calibration.MicrostepMode)
    _check_result(lib.get_control_settings_calb(device_id,
                                                byref(control_settings),
                                                byref(calib)))
    return ControlSettingsCalb(control_settings.MaxSpeed,
                               control_settings.Timeout,
                               control_settings.MaxClickTime,
                               control_settings.Flags,
                               control_settings.DeltaPosition)


def set_joystick_settings(device_id: DeviceT,
                          settings: JoystickSettings) -> None:
    """Set settings of joystick.

    If joystick position is outside DeadZone limits from the central position
    a movement with speed, defined by the joystick DeadZone edge to 100%
    deviation, begins. Joystick positions inside DeadZone limits correspond to
    zero speed (soft stop of motion) and positions beyond Low and High limits
    correspond MaxSpeed [i] or -MaxSpeed [i] (see command SCTL), where i = 0
    by default and can be changed with left/right buttons (see command SCTL).
    If next speed in list is zero (both integer and microstep parts), the
    button press is ignored. First speed in list shouldn't be zero. The
    DeadZone ranges are illustrated on the following picture.
    !/attachments/download/5563/range25p.png! The relationship between the
    deviation and the rate is exponential, allowing no switching speed combine
    high mobility and accuracy. The following picture illustrates this:
    !/attachments/download/3092/ExpJoystick.png! The nonlinearity parameter is
    adjustable. Setting it to zero makes deviation/speed relation linear.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: joystick settings
    :type settings: JoystickSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, JoystickSettings):
        raise TypeError("settings must be of type JoystickSettings."
                        " <{}> was got.".format(type(settings)))
    joystick_settings = joystick_settings_t(settings.JoyLowEnd,
                                            settings.JoyCenter,
                                            settings.JoyHighEnd,
                                            settings.ExpFactor,
                                            settings.DeadZone,
                                            settings.JoyFlags)
    _check_result(lib.set_joystick_settings(device_id,
                                            byref(joystick_settings)))


def get_joystick_settings(device_id: DeviceT) -> JoystickSettings:
    """Read settings of joystick.

    If joystick position is outside DeadZone limits from the central position
    a movement with speed, defined by the joystick DeadZone edge to 100%
    deviation, begins. Joystick positions inside DeadZone limits correspond to
    zero speed (soft stop of motion) and positions beyond Low and High limits
    correspond MaxSpeed [i] or -MaxSpeed [i] (see command SCTL), where i = 0
    by default and can be changed with left/right buttons (see command SCTL).
    If next speed in list is zero (both integer and microstep parts), the
    button press is ignored. First speed in list shouldn't be zero. The
    DeadZone ranges are illustrated on the following picture.
    !/attachments/download/5563/range25p.png! The relationship between the
    deviation and the rate is exponential, allowing no switching speed combine
    high mobility and accuracy. The following picture illustrates this:
    !/attachments/download/3092/ExpJoystick.png! The nonlinearity parameter is
    adjustable. Setting it to zero makes deviation/speed relation linear.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: joystick settings
    :rtype: JoystickSettings
    """
    _check_device_id(device_id)
    joystick_settings = joystick_settings_t()
    _check_result(lib.get_joystick_settings(device_id,
                                            byref(joystick_settings)))
    return JoystickSettings(joystick_settings.JoyLowEnd,
                            joystick_settings.JoyCenter,
                            joystick_settings.JoyHighEnd,
                            joystick_settings.ExpFactor,
                            joystick_settings.DeadZone,
                            joystick_settings.JoyFlags)


def set_ctp_settings(device_id: DeviceT,
                     settings: CtpSettings) -> None:
    """Set settings of control position(is only used with stepper motor).

    When controlling the step motor with encoder (CTP_BASE 0) it is possible
    to detect the loss of steps. The controller knows the number of steps per
    revolution (GENG :: StepsPerRev) and the encoder resolution (GFBS :: IPT).
    When the control (flag CTP_ENABLED), the controller stores the current
    position in the footsteps of SM and the current position of the encoder.
    Further, at each step of the position encoder is converted into steps and
    if the difference is greater CTPMinError, a flag STATE_CTP_ERROR. When
    controlling the step motor with speed sensor (CTP_BASE 1), the position is
    controlled by him. The active edge of input clock controller stores the
    current value of steps. Further, at each turn checks how many steps
    shifted. When a mismatch CTPMinError a flag STATE_CTP_ERROR.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: ctp settings
    :type settings: CtpSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, CtpSettings):
        raise TypeError("settings must be of type CtpSettings."
                        " <{}> was got.".format(type(settings)))
    ctp_settings = ctp_settings_t(settings.CTPMinError,
                                  settings.CTPFlags)
    _check_result(lib.set_ctp_settings(device_id, byref(ctp_settings)))


def get_ctp_settings(device_id: DeviceT) -> CtpSettings:
    """Read settings of control position(is only used with stepper motor).

    When controlling the step motor with encoder (CTP_BASE 0) it is possible
    to detect the loss of steps. The controller knows the number of steps per
    revolution (GENG :: StepsPerRev) and the encoder resolution (GFBS :: IPT).
    When the control (flag CTP_ENABLED), the controller stores the current
    position in the footsteps of SM and the current position of the encoder.
    Further, at each step of the position encoder is converted into steps and
    if the difference is greater CTPMinError, a flag STATE_CTP_ERROR. When
    controlling the step motor with speed sensor (CTP_BASE 1), the position is
    controlled by him. The active edge of input clock controller stores the
    current value of steps. Further, at each turn checks how many steps
    shifted. When a mismatch CTPMinError a flag STATE_CTP_ERROR.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: ctp settings
    :rtype: CtpSettings
    """
    _check_device_id(device_id)
    ctp_settings = ctp_settings_t()
    _check_result(lib.get_ctp_settings(device_id, byref(ctp_settings)))
    return CtpSettings(ctp_settings.CTPMinError,
                       ctp_settings.CTPFlags)


def set_uart_settings(device_id: DeviceT,
                      settings: UartSettings) -> None:
    """Set UART settings.

    This function send structure with UART settings to controller's memory.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: uart settings
    :type settings: UartSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, UartSettings):
        raise TypeError("settings must be of type UartSettings."
                        " <{}> was got.".format(type(settings)))
    uart_settings = uart_settings_t(settings.Speed,
                                    settings.UARTSetupFlags)
    _check_result(lib.set_uart_settings(device_id, byref(uart_settings)))


def get_uart_settings(device_id: DeviceT) -> UartSettings:
    """Read UART settings.

    This function fill structure with UART settings.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: uart settings
    :rtype: UartSettings
    """
    _check_device_id(device_id)
    uart_settings = uart_settings_t()
    _check_result(lib.get_uart_settings(device_id, byref(uart_settings)))
    return UartSettings(uart_settings.Speed,
                        uart_settings.UARTSetupFlags)


def set_network_settings(device_id: DeviceT,
                         settings: NetworkSettings) -> None:
    """Set network settings.

    This function sets desired network settings.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: network settings
    :type settings: NetworkSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, NetworkSettings):
        raise TypeError("settings must be of type NetworkSettings."
                        " <{}> was got.".format(type(settings)))
    network_settings = network_settings_t(settings.DHCPEnabled,
                                          settings.IPv4Address,
                                          settings.SubnetMask,
                                          settings.DefaultGateway)
    _check_result(lib.set_network_settings(device_id, byref(network_settings)))


def get_network_settings(device_id: DeviceT) -> NetworkSettings:
    """Read network settings.

    This function returns current network settings.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: network settings
    :rtype: NetworkSettings
    """
    _check_device_id(device_id)
    network_settings = network_settings_t()
    _check_result(lib.get_network_settings(device_id, byref(network_settings)))
    return NetworkSettings(network_settings.DHCPEnabled,
                           network_settings.IPv4Address,
                           network_settings.SubnetMask,
                           network_settings.DefaultGateway)


def set_password_settings(device_id: DeviceT,
                          settings: PasswordSettings) -> None:
    """Sets password settings.

    This function sets user password to the device web-page.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: password settings
    :type settings: PasswordSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, PasswordSettings):
        raise TypeError("settings must be of type PasswordSettings."
                        " <{}> was got.".format(type(settings)))
    password_settings = password_settings_t(settings.UserPassword)
    _check_result(lib.set_password_settings(device_id,
                                            byref(password_settings)))


def get_password_settings(device_id: DeviceT) -> PasswordSettings:
    """Read password settings.

    This function reads user password to the device web-page.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: password settings
    :rtype: PasswordSettings
    """
    _check_device_id(device_id)
    password_settings = password_settings_t()
    _check_result(lib.get_password_settings(device_id,
                                            byref(password_settings)))
    return PasswordSettings(password_settings.UserPassword)


def set_calibration_settings(device_id: DeviceT,
                             settings: CalibrationSettings) -> None:
    """Set calibration settings.

    This function send structure with calibration settings to controller's
    memory.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: calibration settings
    :type settings: CalibrationSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, CalibrationSettings):
        raise TypeError("settings must be of type CalibrationSettings."
                        " <{}> was got.".format(type(settings)))
    calibration_settings = calibration_settings_t(settings.CSS1_A,
                                                  settings.CSS1_B,
                                                  settings.CSS2_A,
                                                  settings.CSS2_B,
                                                  settings.FullCurrent_A,
                                                  settings.FullCurrent_B)
    _check_result(lib.set_calibration_settings(device_id,
                                               byref(calibration_settings)))


def get_calibration_settings(device_id: DeviceT) -> CalibrationSettings:
    """Read calibration settings.

    This function fill structure with calibration settings.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: calibration settings
    :rtype: CalibrationSettings
    """
    _check_device_id(device_id)
    calibration_settings = calibration_settings_t()
    _check_result(lib.get_calibration_settings(device_id,
                                               byref(calibration_settings)))
    return CalibrationSettings(calibration_settings.CSS1_A,
                               calibration_settings.CSS1_B,
                               calibration_settings.CSS2_A,
                               calibration_settings.CSS2_B,
                               calibration_settings.FullCurrent_A,
                               calibration_settings.FullCurrent_B)


def set_emf_settings(device_id: DeviceT,
                     settings: EmfSettings) -> None:
    """Set electromechanical coefficients.

    The settings are different for different stepper motors. Please download
    the new settings when you change the motor.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: emf settings
    :type settings: EmfSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, EmfSettings):
        raise TypeError("settings must be of type EmfSettings."
                        " <{}> was got.".format(type(settings)))
    emf_settings = emf_settings_t(settings.L,
                                  settings.R,
                                  settings.Km,
                                  settings.BackEMFFlags)
    _check_result(lib.set_emf_settings(device_id, byref(emf_settings)))


def get_emf_settings(device_id: DeviceT) -> EmfSettings:
    """Read electromechanical settings.

    The settings are different for different stepper motors.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: emf settings
    :rtype: EmfSettings
    """
    _check_device_id(device_id)
    emf_settings = emf_settings_t()
    _check_result(lib.get_emf_settings(device_id, byref(emf_settings)))
    return EmfSettings(emf_settings.L,
                       emf_settings.R,
                       emf_settings.Km,
                       emf_settings.BackEMFFlags)


def set_extended_settings(device_id: DeviceT,
                          settings: ExtendedSettings) -> None:
    """Set extended settings.

    Currently not in use.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: extended settings
    :type settings: ExtendedSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, ExtendedSettings):
        raise TypeError("settings must be of type ExtendedSettings."
                        " <{}> was got.".format(type(settings)))
    extended_settings = extended_settings_t(settings.Param1)
    _check_result(lib.set_extended_settings(device_id,
                                            byref(extended_settings)))


def get_extended_settings(device_id: DeviceT) -> ExtendedSettings:
    """Read extended settings.

    Currently not in use.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: extended settings
    :rtype: ExtendedSettings
    """
    _check_device_id(device_id)
    extended_settings = extended_settings_t()
    _check_result(lib.get_extended_settings(device_id,
                                            byref(extended_settings)))
    return ExtendedSettings(extended_settings.Param1)


def set_stage_settings(device_id: DeviceT,
                       settings: StageSettings) -> None:
    """Set stage settings to EEPROM.

    Can be used by manufacturer only

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: stage settings
    :type settings: StageSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, StageSettings):
        raise TypeError("sss must be of type ggg."
                        " <{}> was got.".format(type(settings)))
    stage_settings = stage_settings_t(settings.LeadScrewPitch,
                                      settings.Units,
                                      settings.MaxSpeed,
                                      settings.TravelRange,
                                      settings.SupplyVoltageMin,
                                      settings.SupplyVoltageMax,
                                      settings.MaxCurrentConsumption,
                                      settings.HorizontalLoadCapacity,
                                      settings.VerticalLoadCapacity)
    _check_result(lib.set_stage_settings(device_id, byref(stage_settings)))


def get_stage_settings(device_id: DeviceT) -> StageSettings:
    """Read stage settings from EEPROM.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: stage settings
    :rtype: StageSettings
    """
    _check_device_id(device_id)
    stage_settings = stage_settings_t()
    _check_result(lib.get_stage_settings(device_id, byref(stage_settings)))
    return StageSettings(stage_settings.LeadScrewPitch,
                         stage_settings.Units,
                         stage_settings.MaxSpeed,
                         stage_settings.TravelRange,
                         stage_settings.SupplyVoltageMin,
                         stage_settings.SupplyVoltageMax,
                         stage_settings.MaxCurrentConsumption,
                         stage_settings.HorizontalLoadCapacity,
                         stage_settings.VerticalLoadCapacity)


def set_motor_settings(device_id: DeviceT,
                       settings: MotorSettings) -> None:
    """Set motor settings to EEPROM.

    Can be used by manufacturer only.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: motor settings
    :type settings: MotorSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, MotorSettings):
        raise TypeError("settings must be of type MotorSettings."
                        " <{}> was got.".format(type(settings)))
    motor_settings = motor_settings_t(settings.MotorType,
                                      settings.ReservedField,
                                      settings.Poles,
                                      settings.Phases,
                                      settings.NominalVoltage,
                                      settings.NominalCurrent,
                                      settings.NominalSpeed,
                                      settings.NominalTorque,
                                      settings.NominalPower,
                                      settings.WindingResistance,
                                      settings.WindingInductance,
                                      settings.RotorInertia,
                                      settings.StallTorque,
                                      settings.DetentTorque,
                                      settings.TorqueConstant,
                                      settings.SpeedConstant,
                                      settings.SpeedTorqueGradient,
                                      settings.MechanicalTimeConstant,
                                      settings.MaxSpeed,
                                      settings.MaxCurrent,
                                      settings.MaxCurrentTime,
                                      settings.NoLoadCurrent,
                                      settings.NoLoadSpeed)
    _check_result(lib.set_motor_settings(device_id, byref(motor_settings)))


def get_motor_settings(device_id: DeviceT) -> MotorSettings:
    """Read motor settings from EEPROM.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: motor settings
    :rtype: MotorSettings
    """
    _check_device_id(device_id)
    motor_settings = motor_settings_t()
    _check_result(lib.get_motor_settings(device_id, byref(motor_settings)))
    return MotorSettings(motor_settings.MotorType,
                         motor_settings.ReservedField,
                         motor_settings.Poles,
                         motor_settings.Phases,
                         motor_settings.NominalVoltage,
                         motor_settings.NominalCurrent,
                         motor_settings.NominalSpeed,
                         motor_settings.NominalTorque,
                         motor_settings.NominalPower,
                         motor_settings.WindingResistance,
                         motor_settings.WindingInductance,
                         motor_settings.RotorInertia,
                         motor_settings.StallTorque,
                         motor_settings.DetentTorque,
                         motor_settings.TorqueConstant,
                         motor_settings.SpeedConstant,
                         motor_settings.SpeedTorqueGradient,
                         motor_settings.MechanicalTimeConstant,
                         motor_settings.MaxSpeed,
                         motor_settings.MaxCurrent,
                         motor_settings.MaxCurrentTime,
                         motor_settings.NoLoadCurrent,
                         motor_settings.NoLoadSpeed)


def set_encoder_settings(device_id: DeviceT,
                         settings: EncoderSettings) -> None:
    """Set encoder settings to EEPROM.

    Can be used by manufacturer only.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: encoder settings
    :type settings: EncoderSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, EncoderSettings):
        raise TypeError("settings must be of type EncoderSettings."
                        " <{}> was got.".format(type(settings)))
    encoder_settings = encoder_settings_t(settings.MaxOperatingFrequency,
                                          settings.SupplyVoltageMin,
                                          settings.SupplyVoltageMax,
                                          settings.MaxCurrentConsumption,
                                          settings.PPR,
                                          settings.EncoderSettings)
    _check_result(lib.set_encoder_settings(device_id, byref(encoder_settings)))


def get_encoder_settings(device_id: DeviceT) -> EncoderSettings:
    """Read encoder settings from EEPROM.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: encoder settings
    :rtype: EncoderSettings
    """
    _check_device_id(device_id)
    encoder_settings = encoder_settings_t()
    _check_result(lib.get_encoder_settings(device_id, byref(encoder_settings)))
    return EncoderSettings(encoder_settings.MaxOperatingFrequency,
                           encoder_settings.SupplyVoltageMin,
                           encoder_settings.SupplyVoltageMax,
                           encoder_settings.MaxCurrentConsumption,
                           encoder_settings.PPR,
                           encoder_settings.EncoderSettings)


def set_hallsensor_settings(device_id: DeviceT,
                            settings: HallsensorSettings) -> None:
    """Set hall sensor settings to EEPROM.

    Can be used by manufacturer only.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: hallsensor settings
    :type settings: HallsensorSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, HallsensorSettings):
        raise TypeError("settings must be of type HallsensorSettings."
                        " <{}> was got.".format(type(settings)))
    hallsensor_settings = hallsensor_settings_t(settings.MaxOperatingFrequency,
                                                settings.SupplyVoltageMin,
                                                settings.SupplyVoltageMax,
                                                settings.MaxCurrentConsumption,
                                                settings.PPR)
    _check_result(lib.set_hallsensor_settings(device_id,
                                              byref(hallsensor_settings)))


def get_hallsensor_settings(device_id: DeviceT) -> HallsensorSettings:
    """Read hall sensor settings from EEPROM.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: hallsensor settings
    :rtype: HallsensorSettings
    """
    _check_device_id(device_id)
    hallsensor_settings = hallsensor_settings_t()
    _check_result(lib.get_hallsensor_settings(device_id,
                                              byref(hallsensor_settings)))
    return HallsensorSettings(hallsensor_settings.MaxOperatingFrequency,
                              hallsensor_settings.SupplyVoltageMin,
                              hallsensor_settings.SupplyVoltageMax,
                              hallsensor_settings.MaxCurrentConsumption,
                              hallsensor_settings.PPR)


def set_gear_settings(device_id: DeviceT,
                      settings: GearSettings) -> None:
    """Set gear settings to EEPROM.

    Can be used by manufacturer only.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: gear settings
    :type settings: GearSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, GearSettings):
        raise TypeError("settings must be of type GearSettings."
                        " <{}> was got.".format(type(settings)))
    gear_settings = gear_settings_t(settings.ReductionIn,
                                    settings.ReductionOut,
                                    settings.RatedInputTorque,
                                    settings.RatedInputSpeed,
                                    settings.MaxOutputBacklash,
                                    settings.InputInertia,
                                    settings.Efficiency)
    _check_result(lib.set_gear_settings(device_id, byref(gear_settings)))


def get_gear_settings(device_id: DeviceT) -> GearSettings:
    """Read gear settings from EEPROM.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: gear settings
    :rtype: GearSettings
    """
    _check_device_id(device_id)
    gear_settings = gear_settings_t()
    _check_result(lib.get_gear_settings(device_id, byref(gear_settings)))
    return GearSettings(gear_settings.ReductionIn,
                        gear_settings.ReductionOut,
                        gear_settings.RatedInputTorque,
                        gear_settings.RatedInputSpeed,
                        gear_settings.MaxOutputBacklash,
                        gear_settings.InputInertia,
                        gear_settings.Efficiency)


def set_accessories_settings(device_id: DeviceT,
                             settings: AccessoriesSettings) -> None:
    """Set additional accessories information to EEPROM.

    Can be used by manufacturer only.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param settings: accessories settings
    :type settings: AccessoriesSettings
    """
    _check_device_id(device_id)
    if not isinstance(settings, AccessoriesSettings):
        raise TypeError("settings must be of type AccessoriesSettings."
                        " <{}> was got.".format(type(settings)))
    accessories_settings = accessories_settings_t(
                                settings.MagneticBrakeInfo,
                                settings.MBRatedVoltage,
                                settings.MBRatedCurrent,
                                settings.MBTorque,
                                settings.MBSettings,
                                settings.TemperatureSensorInfo,
                                settings.TSMin,
                                settings.TSMax,
                                settings.TSGrad,
                                settings.TSSettings,
                                settings.LimitSwitchesSettings)
    _check_result(lib.set_accessories_settings(device_id,
                                               byref(accessories_settings)))


def get_accessories_settings(device_id: DeviceT) -> AccessoriesSettings:
    """Read additional accessories information from EEPROM.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: accessories settings
    :rtype: AccessoriesSettings
    """
    _check_device_id(device_id)
    accessories_settings = accessories_settings_t()
    _check_result(lib.get_accessories_settings(device_id,
                                               byref(accessories_settings)))
    return AccessoriesSettings(accessories_settings.MagneticBrakeInfo,
                               accessories_settings.MBRatedVoltage,
                               accessories_settings.MBRatedCurrent,
                               accessories_settings.MBTorque,
                               accessories_settings.MBSettings,
                               accessories_settings.TemperatureSensorInfo,
                               accessories_settings.TSMin,
                               accessories_settings.TSMax,
                               accessories_settings.TSGrad,
                               accessories_settings.TSSettings,
                               accessories_settings.LimitSwitchesSettings)


def set_controller_name(device_id: DeviceT,
                        name: ControllerName) -> None:
    """Write user controller name and flags of setting from FRAM.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param name: controller name
    :type name: ControllerName
    """
    _check_device_id(device_id)
    if not isinstance(name, ControllerName):
        raise TypeError("name must be of type ControllerName."
                        " <{}> was got.".format(type(name)))
    controller_name = controller_name_t(name.ControllerName,
                                        name.CtrlFlags)
    _check_result(lib.set_controller_name(device_id, byref(controller_name)))


def get_controller_name(device_id: DeviceT) -> ControllerName:
    """Read user controller name and flags of setting from FRAM.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: controller name
    :rtype: ControllerName
    """
    _check_device_id(device_id)
    controller_name = controller_name_t()
    _check_result(lib.get_controller_name(device_id, byref(controller_name)))
    return ControllerName(controller_name.ControllerName,
                          controller_name.CtrlFlags)


def set_nonvolatile_memory(device_id: DeviceT,
                           memory: NonvolatileMemory) -> None:
    """Write userdata into FRAM.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param memory: nonvolatile memory
    :type memory: NonvolatileMemory
    """
    _check_device_id(device_id)
    if not isinstance(memory, NonvolatileMemory):
        raise TypeError("memory must be of type NonvolatileMemory."
                        " <{}> was got.".format(type(memory)))
    nonvolatile_memory = nonvolatile_memory_t(memory.UserData)
    _check_result(lib.set_nonvolatile_memory(device_id, nonvolatile_memory))


def get_nonvolatile_memory(device_id: DeviceT) -> NonvolatileMemory:
    """Read userdata from FRAM.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: nonvolatile memory
    :rtype: NonvolatileMemory
    """
    _check_device_id(device_id)
    nonvolatile_memory = nonvolatile_memory_t()
    _check_result(lib.get_nonvolatile_memory(device_id,
                                             byref(nonvolatile_memory)))
    return NonvolatileMemory(nonvolatile_memory.UserData)


def set_engine_advansed_setup(device_id: DeviceT,
                              setup: EngineAdvansedSetup) -> None:
    """Set engine advansed settings.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param setup: advanced engine params
    :type setup: EngineAdvansedSetup
    """
    _check_device_id(device_id)
    if not isinstance(setup, EngineAdvansedSetup):
        raise TypeError("setup must be of type EngineAdvansedSetup."
                        " <{}> was got.".format(type(setup)))
    engine_advanced_setup = engine_advansed_setup_t(
                                    setup.stepcloseloop_Kw,
                                    setup.stepcloseloop_Kp_low,
                                    setup.stepcloseloop_Kp_high)
    _check_result(lib.set_engine_advansed_setup(device_id,
                                                byref(engine_advanced_setup)))


def get_engine_advansed_setup(device_id: DeviceT) -> EngineAdvansedSetup:
    """Read engine advansed settings.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: advanced engine params
    :rtype: EngineAdvansedSetup
    """
    _check_device_id(device_id)
    engine_advanced_setup = engine_advansed_setup_t()
    _check_result(lib.get_engine_advansed_setup(device_id,
                                                byref(engine_advanced_setup)))
    return EngineAdvansedSetup(engine_advanced_setup.stepcloseloop_Kw,
                               engine_advanced_setup.stepcloseloop_Kp_low,
                               engine_advanced_setup.stepcloseloop_Kp_high)


def command_move_calb(device_id: DeviceT,
                      position: float,
                      calibration: Calibration) -> None:
    """Move to position which use user units.

    Upon receiving the command "move" the engine starts to move with pre-set
    parameters (speed, acceleration, retention), to the point specified to the
    Position.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param position: position
    :type position: float
    :param calibration: calibration
    :type calibration: Calibration
    """
    _check_device_id(device_id)
    if not isinstance(position, float):
        raise TypeError("position must be of type float."
                        " <{}> was got.".format(type(position)))
    if not isinstance(calibration, Calibration):
        raise TypeError("calibration must be of type Calibration. <{}>"
                        " was got.".format(type(calibration)))
    calib = calibration_t(calibration.A, calibration.MicrostepMode)
    _check_result(lib.command_move_calb(device_id,
                                        c_float(position),
                                        byref(calib)))


def command_movr(device_id: DeviceT,
                 delta_position: int,
                 udelta_position: int) -> None:
    """Move to offset.

    Upon receiving the command "movr" engine starts to move with pre-set
    parameters (speed, acceleration, hold), left or right (depending on the
    sign of DeltaPosition) by the number of pulses specified in the fields
    DeltaPosition, uDeltaPosition. For stepper motor uDeltaPosition sets the
    microstep, for DC motor this field is not used.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param delta_position: shift from initial position.
    :type delta_position: int
    :param udelta_position: part of the offset shift, microsteps. Microstep
    size and the range of valid values for this field depend on selected step
    division mode (see MicrostepMode field in engine_settings).
    :type udelta_position: int
    """
    _check_device_id(device_id)
    if not isinstance(delta_position, int):
        raise TypeError("delta_position must be of type int."
                        " <{}> was got.".format(type(delta_position)))
    if not isinstance(udelta_position, int):
        raise TypeError("udelta_position must be of type int."
                        " <{}> was got.".format(type(udelta_position)))
    _check_result(lib.command_movr(device_id, delta_position, udelta_position))


def command_movr_calb(device_id: DeviceT,
                      delta_position: float,
                      calibration: Calibration) -> None:
    """Move to offset using user units.

    Upon receiving the command "movr" engine starts to move with pre-set
    parameters (speed, acceleration, hold), left or right (depending on the
    sign of DeltaPosition) the distance specified in the field DeltaPosition.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param delta_position: shift from initial position.
    :type delta_position: float
    :param calibration: user unit settings
    :type calibration: Calibration
    """
    _check_device_id(device_id)
    if not isinstance(delta_position, float):
        raise TypeError("delta_position must be of type float."
                        " <{}> was got.".format(type(delta_position)))
    if not isinstance(calibration, Calibration):
        raise TypeError("calibration must be of type Calibration. <{}>"
                        " was got.".format(type(calibration)))
    calib = calibration_t(calibration.A, calibration.MicrostepMode)
    _check_result(lib.command_movr_calb(device_id,
                                        c_float(delta_position),
                                        byref(calib)))


def command_home(device_id: DeviceT) -> None:
    """The positive direction is to the right.

    A value of zero reverses the direction of the direction of the flag, the
    set speed. Restriction imposed by the trailer, act the same, except that
    the limit switch contact does not stop. Limit the maximum speed,
    acceleration and deceleration function. 1) moves the motor according to
    the speed FastHome, uFastHome and flag HOME_DIR_FAST until limit switch,
    if the flag is set HOME_STOP_ENDS, until the signal from the input
    synchronization if the flag HOME_STOP_SYNC (as accurately as possible is
    important to catch the moment of operation limit switch) or until the
    signal is received from the speed sensor, if the flag HOME_STOP_REV_SN 2)
    then moves according to the speed SlowHome, uSlowHome and flag
    HOME_DIR_SLOW until signal from the clock input, if the flag HOME_MV_SEC.
    If the flag HOME_MV_SEC reset skip this paragraph. 3) then move the motor
    according to the speed FastHome, uFastHome and flag HOME_DIR_SLOW a
    distance HomeDelta, uHomeDelta. description of flags and variable see in
    description for commands GHOM/SHOM

    :param device_id: an identifier of device
    :type device_id: DeviceT
    """
    _check_device_id(device_id)
    _check_result(lib.command_home(device_id))


def command_left(device_id: DeviceT) -> None:
    """Start continous moving to the left.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    """
    _check_device_id(device_id)
    _check_result(lib.command_left(device_id))


def command_right(device_id: DeviceT) -> None:
    """Start continous moving to the right.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    """
    _check_device_id(device_id)
    _check_result(lib.command_right(device_id))


def command_loft(device_id: DeviceT) -> None:
    """Upon receiving the command "loft" the engine is shifted from the
    current point to a distance GENG :: Antiplay, then move to the same point.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    """
    _check_device_id(device_id)
    _check_result(lib.command_loft(device_id))


def command_sstp(device_id: DeviceT) -> None:
    """Soft stop engine.

    The motor stops with deceleration speed.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    """
    _check_device_id(device_id)
    _check_result(lib.command_sstp(device_id))


def get_position_calb(device_id: DeviceT,
                      calibration: Calibration) -> GetPositionCalb:
    """Reads position value in user units for stepper motor and encoder steps
    all engines.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param calibration: 	user unit settings
    :type calibration: Calibration
    :return: structure contains move settings: speed, acceleration,
    deceleration etc.
    :rtype: GetPositionCalb
    """
    _check_device_id(device_id)
    if not isinstance(calibration, Calibration):
        raise TypeError("calibration must be of type Calibration. <{}>"
                        " was got.".format(type(calibration)))
    position = get_position_calb_t()
    calib = calibration_t(calibration.A, calibration.MicrostepMode)
    _check_result(lib.get_position_calb(device_id,
                                        byref(position),
                                        byref(calib)))
    return GetPositionCalb(position.Position,
                           position.EncPosition)


def set_position(device_id: DeviceT,
                 position: SetPosition) -> None:
    """Sets any position value in steps and micro for stepper motor and
    encoder steps of all engines.

    It means, that changing main indicator of position.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param position: structure contains move settings: speed, acceleration,
    deceleration etc.
    :type position: SetPosition
    """
    _check_device_id(device_id)
    if not isinstance(position, SetPosition):
        raise TypeError("position must be of type SetPosition."
                        " <{}> was got.".format(type(position)))
    _position = set_position_t(position.Position,
                               position.uPosition,
                               position.EncPosition,
                               position.PosFlags)
    _check_result(lib.set_position(device_id, byref(_position)))


def set_position_calb(device_id: DeviceT,
                      position: SetPositionCalb,
                      calibration: Calibration) -> None:
    """Sets any position value and encoder value of all engines which use user
    units.

    It means, that changing main indicator of position.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param position: structure contains move settings: speed, acceleration,
    deceleration etc.
    :type position: SetPosition
    :param calibration: user unit settings
    :type calibration: Calibration
    """
    _check_device_id(device_id)
    if not isinstance(position, SetPositionCalb):
        raise TypeError("position must be of type SetPositionCalb."
                        " <{}> was got.".format(type(position)))
    if not isinstance(calibration, Calibration):
        raise TypeError("calibration must be of type Calibration. <{}>"
                        " was got.".format(type(calibration)))
    _position = set_position_calb_t(position.Position,
                                    position.EncPosition,
                                    position.PosFlags)
    calib = calibration_t(calibration.A, calibration.MicrostepMode)
    _check_result(lib.set_position(device_id, byref(_position), byref(calib)))


def command_zero(device_id: DeviceT) -> None:
    """Sets the current position and the position in which the traffic moves
    by the move command and movr zero for all cases, except for movement to
    the target position.

    In the latter case, set the zero current position and the target position
    counted so that the absolute position of the destination is the same. That
    is, if we were at 400 and moved to 500, then the command Zero makes the
    current position of 0, and the position of the destination - 100. Does not
    change the mode of movement that is if the motion is carried, it
    continues, and if the engine is in the "hold", the type of retention
    remains.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    """
    _check_device_id(device_id)
    _check_result(lib.command_zero(device_id))


def command_save_settings(device_id: DeviceT) -> None:
    """Save all settings from controller's RAM to controller's flash memory,
    replacing previous data in controller's flash memory.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    """
    _check_device_id(device_id)
    _check_result(lib.command_save_settings(device_id))


def command_read_settings(device_id: DeviceT) -> None:
    """Read all settings from controller's flash memory to controller's RAM,
    replacing previous data in controller's RAM.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    """
    _check_device_id(device_id)
    _check_result(lib.command_read_settings(device_id))


def command_save_robust_settings(device_id: DeviceT) -> None:
    """Save important settings (calibration coefficients and etc.) from
    controller's RAM to controller's flash memory, replacing previous data in
    controller's flash memory.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    """
    _check_device_id(device_id)
    _check_result(lib.command_save_robust_settings(device_id))


def command_read_robust_settings(device_id: DeviceT) -> None:
    """Read important settings (calibration coefficients and etc.) from
    controller's flash memory to controller's RAM, replacing previous data in
    controller's RAM.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    """
    _check_device_id(device_id)
    _check_result(lib.command_read_robust_settings(device_id))


def command_eesave_settings(device_id: DeviceT) -> None:
    """Save settings from controller's RAM to stage's EEPROM memory, which
    spontaneity connected to stage and it isn`t change without it mechanical
    reconstruction.

    Can be used by manufacturer onl

    :param device_id: an identifier of device
    :type device_id: DeviceT
    """
    _check_device_id(device_id)
    _check_result(lib.command_eesave_settings(device_id))


def command_eeread_settings(device_id: DeviceT) -> None:
    """Read settings from controller's RAM to stage's EEPROM memory, which
    spontaneity connected to stage and it isn`t change without it mechanical
    reconstruction.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    """
    _check_device_id(device_id)
    _check_result(lib.command_eeread_settings(device_id))


def command_start_measurements(device_id: DeviceT) -> None:
    """Start measurements and buffering of speed, following error.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    """
    _check_device_id(device_id)
    _check_result(lib.command_start_measurements(device_id))


def get_measurements(device_id: DeviceT) -> Measurements:
    """A command to read the data buffer to build a speed graph and a sequence
    error.

    Filling the buffer starts with the command "start_measurements". The
    buffer holds 25 points, the points are taken with a period of 1 ms. To
    create a robust system, read data every 20 ms, if the buffer is completely
    full, then it is recommended to repeat the readings every 5 ms until the
    buffer again becomes filled with 20 points.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: structure with buffer and its length.

    :rtype: Measurements
    """
    _check_device_id(device_id)
    measurements = measurements_t()
    _check_result(lib.get_measurements(device_id, byref(measurements)))
    return Measurements(measurements.Speed,
                        measurements.Error,
                        measurements.Length)


def get_chart_data(device_id: DeviceT) -> ChartData:
    """Return device electrical parameters, useful for charts.

    Useful function that fill structure with snapshot of controller voltages
    and currents.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: structure with snapshot of controller parameters.
    :rtype: ChartData
    """
    _check_device_id(device_id)
    chart_data = chart_data_t()
    _check_result(lib.get_chart_data(device_id, byref(chart_data)))
    return ChartData(chart_data.WindingVoltageA,
                     chart_data.WindingVoltageB,
                     chart_data.WindingVoltageC,
                     chart_data.WindingCurrentA,
                     chart_data.WindingCurrentB,
                     chart_data.WindingCurrentC,
                     chart_data.Pot,
                     chart_data.Joy,
                     chart_data.DutyCycle)


def get_serial_number(device_id: DeviceT) -> SerialNumber:
    """Read device serial number.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: serial number
    :rtype: SerialNumber
    """
    _check_device_id(device_id)
    serial_number = serial_number_t()
    _check_result(lib.get_serial_number(device_id, byref(serial_number)))
    return SerialNumber(serial_number.SN,
                        serial_number.Key,
                        serial_number.Major,
                        serial_number.Minor,
                        serial_number.Release)


def get_firmware_version(device_id: DeviceT) -> 'tuple[int]':
    """Read controller's firmware version.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: tuple of major, minor and release versions
    :rtype: tuple[int]
    """
    _check_device_id(device_id)
    minor_version = c_uint32()
    major_version = c_uint32()
    release_version = c_uint32()
    _check_result(lib.get_firmware_version(device_id,
                                           byref(minor_version),
                                           byref(major_version),
                                           byref(release_version)))
    return (minor_version, major_version, release_version)


def service_command_updf(device_id: DeviceT) -> None:
    """Command puts the controller to update the firmware.

    After receiving this command, the firmware board sets a flag (for loader),
    sends echo reply and restarts the controller.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    """
    _check_device_id(device_id)
    _check_result(lib.service_command_updf(device_id))


def set_serial_number(device_id: DeviceT,
                      serial: SerialNumber) -> None:
    """Write device serial number and hardware version to controller's flash
    memory.

    Along with the new serial number and hardware version a "Key" is
    transmitted. The SN and hardware version are changed and saved when keys
    match. Can be used by manufacturer only.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param serial: structure contains new serial number and secret key.
    :type serial: SerialNumber
    """
    _check_device_id(device_id)
    if not isinstance(serial, SerialNumber):
        raise TypeError("serial must be of type SerialNumber."
                        " <{}> was got.".format(type(serial)))
    serial_number = serial_number_t(serial.SN,
                                    serial.Key,
                                    serial.Major,
                                    serial.Minor,
                                    serial.Release)
    _check_result(lib.set_serial_number(device_id, byref(serial_number)))


def get_analog_data(device_id: DeviceT) -> AnalogData:
    """Read analog data structure that contains raw analog data from ADC
    embedded on board.

    This function used for device testing and deep recalibraton by
    manufacturer only.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: 	analog data coefficients
    :rtype: AnalogData
    """
    _check_device_id(device_id)
    analog_data = analog_data_t()
    _check_result(lib.get_analog_data(device_id, byref(analog_data)))
    return AnalogData(analog_data.A1Voltage_ADC,
                      analog_data.A2Voltage_ADC,
                      analog_data.B1Voltage_ADC,
                      analog_data.B2Voltage_ADC,
                      analog_data.SupVoltage_ADC,
                      analog_data.ACurrent_ADC,
                      analog_data.BCurrent_ADC,
                      analog_data.FullCurrent_ADC,
                      analog_data.Temp_ADC,
                      analog_data.Joy_ADC,
                      analog_data.Pot_ADC,
                      analog_data.L5_ADC,
                      analog_data.H5_ADC,
                      analog_data.A1Voltage,
                      analog_data.A2Voltage,
                      analog_data.B1Voltage,
                      analog_data.B2Voltage,
                      analog_data.SupVoltage,
                      analog_data.ACurrent,
                      analog_data.BCurrent,
                      analog_data.FullCurrent,
                      analog_data.Temp,
                      analog_data.Joy,
                      analog_data.Pot,
                      analog_data.L5,
                      analog_data.H5,
                      analog_data.deprecated,
                      analog_data.R,
                      analog_data.L)


def set_stage_name(device_id: DeviceT,
                   name: StageName) -> None:
    """Write user stage name from EEPROM.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param name: structure contains previously set user stage name
    :type name: StageName
    """
    _check_device_id(device_id)
    if not isinstance(name, StageName):
        raise TypeError("name must be of type StageName."
                        " <{}> was got.".format(type(name)))
    stage_name = stage_name_t(name.PositionerName)
    _check_result(lib.set_stage_name(device_id, byref(stage_name)))


def get_stage_name(device_id: DeviceT) -> StageName:
    """Read user stage name from EEPROM.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: structure contains previously set user stage name
    :rtype: StageName
    """
    _check_device_id(device_id)
    stage_name = stage_name_t()
    _check_result(lib.get_stage_name(device_id, byref(stage_name)))
    return StageName(stage_name.PositionerName)


def set_stage_information(device_id: DeviceT,
                          information: StageInformation) -> None:
    """Set stage information to EEPROM.

    Can be used by manufacturer only.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param information: structure contains stage information
    :type information: StageInformation
    """
    _check_device_id(device_id)
    if not isinstance(information, StageInformation):
        raise TypeError("information must be of type StageInformation."
                        " <{}> was got.".format(type(information)))
    stage_information = stage_information_t(information.Manufacturer,
                                            information.PartNumber)
    _check_result(lib.set_stage_information(device_id,
                                            byref(stage_information)))


def get_stage_information(device_id: DeviceT) -> StageInformation:
    """Read stage information from EEPROM.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: structure contains stage information
    :rtype: StageInformation
    """
    _check_device_id(device_id)
    stage_information = stage_information_t()
    _check_result(lib.get_stage_information(device_id,
                                            byref(stage_information)))
    return StageInformation(stage_information.Manufacturer,
                            stage_information.PartNumber)


def set_motor_information(device_id: DeviceT,
                          information: MotorInformation) -> None:
    """Set motor information to EEPROM.

    Can be used by manufacturer only.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param information: structure contains motor information
    :type information: MotorInformation
    """
    _check_device_id(device_id)
    if not isinstance(information, MotorInformation):
        raise TypeError("information must be of type MotorInformation."
                        " <{}> was got.".format(type(information)))
    motor_information = motor_information_t(information.Manufacturer,
                                            information.PartNumber)
    _check_result(lib.set_motor_information(device_id,
                                            byref(motor_information)))


def get_motor_information(device_id: DeviceT) -> MotorInformation:
    """Read motor information from EEPROM.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: structure contains motor information
    :rtype: MotorInformation
    """
    _check_device_id(device_id)
    motor_information = motor_information_t()
    _check_result(lib.get_motor_information(device_id,
                                            byref(motor_information)))


def set_encoder_information(device_id: DeviceT,
                            information: EncoderInformation) -> None:
    """Set encoder information to EEPROM.

    Can be used by manufacturer only.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param information: structure contains information about encoder
    :type information: EncoderInformation
    """
    _check_device_id(device_id)
    if not isinstance(information, EncoderInformation):
        raise TypeError("information must be of type EncoderInformation."
                        " <{}> was got.".format(type(information)))
    encoder_information = encoder_information_t(information.Manufacturer,
                                                information.PartNumber)
    _check_result(lib.set_encoder_information(device_id,
                                              byref(encoder_information)))


def get_encoder_information(device_id: DeviceT) -> EncoderInformation:
    """Read encoder information from EEPROM.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: structure contains information about encoder
    :rtype: EncoderInformation
    """
    _check_device_id(device_id)
    encoder_information = encoder_information_t()
    _check_result(lib.get_encoder_information(device_id,
                                              byref(encoder_information)))
    return EncoderInformation(encoder_information.Manufacturer,
                              encoder_information.PartNumber)


def set_hallsensor_information(device_id: DeviceT,
                               information: HallsensorInformation) -> None:
    """Set hall sensor information to EEPROM.

    Can be used by manufacturer only.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param information: structure contains information about hall sensor
    :type information: HallsensorInformation
    """
    _check_device_id(device_id)
    if not isinstance(information, HallsensorInformation):
        raise TypeError("information must be of type HallsensorInformation."
                        " <{}> was got.".format(type(information)))
    hallsensor_information = hallsensor_information_t(information.Manufacturer,
                                                      information.PartNumber)
    _check_result(lib.set_hallsensor_information(
                                    device_id,
                                    byref(hallsensor_information)))


def get_hallsensor_information(device_id: DeviceT) -> HallsensorInformation:
    """Read hall sensor information from EEPROM.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: structure contains information about hall sensor
    :rtype: HallsensorInformation
    """
    _check_device_id(device_id)
    hallsensor_information = hallsensor_information_t()
    _check_result(
        lib.get_hallsensor_information(device_id,
                                       byref(hallsensor_information)))
    return HallsensorInformation(hallsensor_information.Manufacturer,
                                 hallsensor_information.PartNumber)


def set_gear_information(device_id: DeviceT,
                         information: GearInformation) -> None:
    """Set gear information to EEPROM.

    Can be used by manufacturer only

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param information: structure contains information about step gearhead
    :type information: GearInformation
    """
    _check_device_id(device_id)
    if not isinstance(information, GearInformation):
        raise TypeError("information must be of type GearInformation."
                        " <{}> was got.".format(type(information)))
    gear_information = gear_information_t(information.Manufacturer,
                                          information.PartNumber)
    _check_result(lib.set_gear_information(device_id, byref(gear_information)))


def get_gear_information(device_id: DeviceT) -> GearInformation:
    """Read gear information from EEPROM.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: structure contains information about step gearhead
    :rtype: GearInformation
    """
    _check_device_id(device_id)
    gear_information = gear_information_t()
    _check_result(lib.get_gear_information(device_id, byref(gear_information)))
    return GearInformation(gear_information.Manufacturer,
                           gear_information.PartNumber)


def get_bootloader_version(device_id: DeviceT) -> 'tuple[int]':
    """Read controller's firmware version.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: tuple of major, minor and release versions
    :rtype: tuple[int]
    """
    _check_device_id(device_id)
    minor_version = c_uint32()
    major_version = c_uint32()
    release_version = c_uint32()
    _check_result(lib.get_bootloader_version(device_id,
                                             byref(minor_version),
                                             byref(major_version),
                                             byref(release_version)))
    return (minor_version, major_version, release_version)


def get_init_random(device_id: DeviceT) -> InitRandom:
    """Read random number from controller.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: random sequence generated by the controlle
    :rtype: InitRandom
    """
    _check_device_id(device_id)
    init_random = init_random_t()
    _check_result(lib.get_init_random(device_id, byref(init_random)))
    return InitRandom(init_random.key)


def get_globally_unique_identifier(
        device_id: DeviceT) -> GloballyUniqueIdentifier:
    """This value is unique to each individual die but is not a random value.

    This unique device identifier can be used to initiate secure boot
    processes or as a serial number for USB or other end applications.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: the result of fields 0-3 concatenated defines the unique 128-bit
    device identifier.
    :rtype: GloballyUniqueIdentifier
    """
    _check_device_id(device_id)
    globally_unique_identifier = globally_unique_identifier_t()
    _check_result(
        lib.get_globally_unique_identifier(device_id,
                                           byref(globally_unique_identifier)))
    return GloballyUniqueIdentifier(globally_unique_identifier.UniqueID0,
                                    globally_unique_identifier.UniqueID1,
                                    globally_unique_identifier.UniqueID2,
                                    globally_unique_identifier.UniqueID3)


def goto_firmware(device_id: DeviceT) -> int:
    """Reboot to firmware.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: RESULT_OK, if reboot to firmware is possible. Reboot is done
    after reply to this command. RESULT_NO_FIRMWARE, if firmware is not found.
    RESULT_ALREADY_IN_FIRMWARE, if this command was sent when controller is
    already in firmware.
    :rtype: c_uint8
    """
    _check_device_id(device_id)
    ret = c_uint8()
    _check_result(lib.goto_firmware(device_id, byref(ret)))
    return int(ret)


def has_firmware(uri: str) -> int:
    """Check for firmware on device.

    :param uri: a uri of device
    :type uri: str
    :return: non-zero if firmware existed
    :rtype: int
    """
    if not isinstance(uri, str):
        raise TypeError("uri must be of type str."
                        " <{}> was got.".format(type(uri)))
    ret = c_uint8()
    _check_result(lib.has_firmware(uri, byref(ret)))
    return int(ret)


def command_update_firmware(uri: str,
                            data: str,
                            size: int) -> None:
    """Update firmware.

    Service command

    :param device_id: a uri of device
    :type device_id: DeviceT
    :param data: firmware byte stream
    :type data: str
    :param size: size of byte stream
    :type size: int
    """
    if not isinstance(uri, str):
        raise TypeError("uri must be of type str."
                        " <{}> was got.".format(type(uri)))
    if not isinstance(data, str):
        raise TypeError("data must be of type str."
                        " <{}> was got.".format(type(data)))
    if not isinstance(size, int):
        raise TypeError("size must be of type int."
                        " <{}> was got.".format(type(size)))
    data_size = c_uint32(size)
    _check_result(lib.command_update_firmware(uri, data, data_size))


def write_key(uri: str,
              key: str) -> None:
    """Write controller key.

    Can be used by manufacturer only

    :param uri: a uri of device
    :type uri: str
    :param key: protection key. Range: 0..4294967295
    :type key: str
    """
    if not isinstance(uri, str):
        raise TypeError("uri must be of type str."
                        " <{}> was got.".format(type(uri)))
    if not isinstance(key, str):
        raise TypeError("key must be of type str."
                        " <{}> was got.".format(type(key)))
    _check_result(lib.write_key(uri, key))


def load_correction_table(device_id: DeviceT,
                          namefile: str) -> None:
    """Command of loading a correction table from a text file (this function
    is deprecated).

    Use the function set_correction_table(device_t id, const char* namefile).
    The correction table is used for position correction in case of mechanical
    inaccuracies. It works for some parameters in _calb commands.

    :param device_id: an identifier the device
    :type device_id: DeviceT
    :param namefile: the file name must be fully qualified. If the short name
    is used, the file must be located in the application directory. If the
    file name is set to NULL, the correction table will be cleared. File
    format: two tab-separated columns. Column headers are string. Data is real,
    the point is a determiter. The first column is a coordinate. The second
    one is the deviation caused by a mechanical error. The maximum length of a
    table is 100 rows.
    :type namefile: str
    """
    _check_device_id(device_id)
    if not isinstance(namefile, str):
        raise TypeError("namefile must be of type str."
                        " <{}> was got.".format(type(namefile)))
    _check_result(lib.load_correction_table(device_id, namefile))


def probe_device(uri: str) -> int:
    """Check if a device with OS uri uri is XIMC device.

    Be carefuly with this call because it sends some data to the device.

    :param uri: a device uri
    :type uri: str
    :return: result of any operation.
    :rtype: Result
    """
    if not isinstance(uri, str):
        raise TypeError("uri must be of type str."
                        " <{}> was got.".format(type(uri)))
    return lib.probe_device(uri)


def enumerate_devices(enumerate_flags: int,
                      hints: str) -> POINTER(device_enumeration_t):
    """Enumerate all devices that looks like valid.

    :param enumerate_flags: enumerate devices flags
    :type enumerate_flags: int
    :param hints: extended information
    :type hints: str
    :return: value describing device enumeration structure.
    :rtype: POINTER(device_enumeration_t)

    hints is a string of form "key=value \n key2=value2". Unrecognized
    key-value pairs are ignored. Key list: addr - used together with
    ENUMERATE_NETWORK flag. Non-null value is a remote host name or a
    comma-separated list of host names which contain the devices to be found,
    absent value means broadcast discovery. adapter_addr - used together with
    ENUMERATE_NETWORK flag. Non-null value is a IP address of network adapter.
    Remote ximc device must be on the same local network as the adapter. When
    using the adapter_addr key, you must set the addr key. Example: "addr= \n
    adapter_addr=192.168.0.100".
    """
    if not isinstance(enumerate_flags, int):
        raise TypeError("enumerate_flags must be of type int."
                        " <{}> was got.".format(type(enumerate_flags)))
    if not isinstance(hints, str):
        raise TypeError("hints must be of type str."
                        " <{}> was got.".format(type(hints)))
    device_enumeration = lib.enumerate_devices(enumerate_flags, hints.encode())
    return device_enumeration


def free_enumerate_devices(
        device_enumeration: POINTER(device_enumeration_t)) -> None:
    """Free memory returned by enumerate_devices.

    :param device_id: opaque pointer to an enumeration device data
    :type device_id: POINTER(device_enumeration_t)
    """
    if not isinstance(device_enumeration, POINTER(device_enumeration_t)):
        raise TypeError("device_enumeration must be of type"
                        " POINTER(device_enumeration_t). <{}> was got."
                        .format(type(device_enumeration)))
    _check_result(lib.free_enumerate_devices(device_enumeration))


def set_correction_table(device_id: DeviceT,
                         namefile: str) -> None:
    """Command of loading a correction table from a text file.

    The correction table is used for position correction in case of mechanical
    inaccuracies. It works for some parameters in _calb commands.

    :param device_id: an identifier the device
    :type device_id: DeviceT
    :param namefile: the file name must be fully qualified. If the short name
    is used, the file must be located in the application directory. If the
    file name is set to NULL, the correction table will be cleared. File
    format: two tab-separated columns. Column headers are string. Data is real,
    the point is a determiter. The first column is a coordinate. The second
    one is the deviation caused by a mechanical error. The maximum length of a
    table is 100 rows.
    :type namefile: str
    """
    _check_device_id(device_id)
    if not isinstance(namefile, str):
        raise TypeError("namefile must be of type str."
                        " <{}> was got.".format(type(namefile)))
    _check_result(lib.set_correction_table(device_id, namefile))


def reset_locks() -> None:
    """Resets the error of incorrect data transmission.

    This function returns only 0 (OK). For example, sending the libximc
    command ends with an incorrect data transfer (error), any subsequent
    command always returns -1 (relevant for Windows).
    """
    lib.reset_locks()


def get_status(device_id: DeviceT) -> Status:
    """Return device state.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: tructure with snapshot of controller status Device state. Useful
    structure that contains current controller status, including speed,
    position and boolean flags.
    :rtype: Status
    """
    _check_device_id(device_id)
    status = status_t()
    _check_result(lib.get_status(device_id, byref(status)))
    return Status(status.MoveSts,
                  status.MvCmdSts,
                  status.PWRSts,
                  status.EncSts,
                  status.WindSts,
                  status.CurPosition,
                  status.uCurPosition,
                  status.EncPosition,
                  status.CurSpeed,
                  status.uCurSpeed,
                  status.Ipwr,
                  status.Upwr,
                  status.Iusb,
                  status.Uusb,
                  status.CurT,
                  status.Flags,
                  status.GPIOFlags,
                  status.CmdBufFreeSpace)


def get_device_information(device_id: DeviceT) -> DeviceInformation:
    """Return device information.

    All fields must point to allocated string buffers with at least 10 bytes.
    Works with both raw or initialized device

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: device information Device information.
    :rtype: DeviceInformation
    """
    _check_device_id(device_id)
    device_information = device_information_t()
    _check_result(lib.get_device_information(device_id,
                                             byref(device_information)))
    return DeviceInformation(device_information.Manufacturer,
                             device_information.ManufacturerId,
                             device_information.ProductDescription,
                             device_information.Major,
                             device_information.Minor,
                             device_information.Release)


def get_device_count(device_enumeration: POINTER(device_enumeration_t)) -> int:
    """Get device count.

    :param device_enumeration: opaque pointer to an enumeration device data
    :type device_enumeration: POINTER(device_enumeration_t)
    :return: device count
    :rtype: int
    """
    if not isinstance(device_enumeration, POINTER(device_enumeration_t)):
        raise TypeError("device_enumeration must be of type"
                        " POINTER(device_enumeration_t). <{}> was got."
                        .format(type(device_enumeration)))
    res = lib.get_device_count(device_enumeration)
    return res


def get_device_name(device_enumeration: POINTER(device_enumeration_t),
                    device_index: int) -> str:
    """Get device name from the device enumeration.

    Returns device_index device name.

    :param device_enumeration: opaque pointer to an enumeration device data
    :type device_enumeration: POINTER(device_enumeration_t)
    :param device_index: device index
    :type device_index: int
    :return: device name
    :rtype: str
    """
    if not isinstance(device_enumeration, POINTER(device_enumeration_t)):
        raise TypeError("device_enumeration must be of type"
                        " POINTER(device_enumeration_t). <{}> was got."
                        .format(type(device_enumeration)))
    if not isinstance(device_index, int):
        raise TypeError("device_index must be of type int."
                        " <{}> was got.".format(type(device_enumeration)))
    res = lib.get_device_name(device_enumeration, device_index)
    return str(res)


def ximc_version() -> str:
    """Returns a library version.

    :return: a buffer to hold a version string, 32 bytes is enough
    :rtype: str
    """
    res = lib.ximc_version()
    return str(res)


def ximc_fix_usbser_sys(device_uri: str) -> None:
    """Fixing a USB driver error in Windows.

    The USB-COM subsystem in the Windows OS does not always work correctly.
    During operation, the following malfunctions are possible: All attempts to
    open the device fail. The device can be opened and data can be sent to it,
    but the response data is not received. These problems are fixed by
    reconnecting the device or reinitializing it in the Device Manager. The
    ximc_fix_usbser_sys() function automates the deletion detection process.

    :param device_uri: device uri
    :type device_uri: str
    """
    if not isinstance(device_uri, str):
        raise TypeError("device_uri must be of type str."
                        " <{}> was got.".format(type(device_uri)))
    _check_result(lib.ximc_fix_usbser_sys(device_uri))


def get_enumerate_device_serial(
        device_enumeration: POINTER(device_enumeration_t),
        device_index: int) -> int:
    """Get device serial number from the device enumeration.

    Returns device_index device serial number.

    :param device_enumeration: opaque pointer to an enumeration device data
    :type device_enumeration: POINTER(device_enumeration_t)
    :param device_index: device index
    :type device_index: int
    :return: device serial number
    :rtype: int
    """
    if not isinstance(device_enumeration, POINTER(device_enumeration_t)):
        raise TypeError("device_enumeration must be of type"
                        " POINTER(device_enumeration_t). <{}> was got."
                        .format(type(device_enumeration)))
    if not isinstance(device_index, int):
        raise TypeError("device_index must be of type int."
                        " <{}> was got.".format(type(device_enumeration)))
    serial = c_uint32()
    _check_result(lib.get_enumerate_device_serial(device_enumeration,
                                                  device_index,
                                                  byref(serial)))
    return int(serial)


def get_enumerate_device_information(
        device_enumeration: POINTER(device_enumeration_t),
        device_index: int) -> DeviceInformation:
    """Get device information from the device enumeration.

    Returns device_index device information.

    :param device_enumeration: opaque pointer to an enumeration device data
    :type device_enumeration: POINTER(device_enumeration_t)
    :param device_index: device index
    :type device_index: int
    :return: device information data
    :rtype: DeviceInformation
    """
    if not isinstance(device_enumeration, POINTER(device_enumeration_t)):
        raise TypeError("device_enumeration must be of type"
                        " POINTER(device_enumeration_t). <{}> was got."
                        .format(type(device_enumeration)))
    if not isinstance(device_index, int):
        raise TypeError("device_index must be of type int."
                        " <{}> was got.".format(type(device_enumeration)))
    device_information = device_information_t()
    _check_result(
        lib.get_enumerate_device_information(device_enumeration,
                                             device_index,
                                             byref(device_information)))
    return DeviceInformation(device_information.Manufacturer,
                             device_information.ManufacturerId,
                             device_information.ProductDescription,
                             device_information.Major,
                             device_information.Minor,
                             device_information.Release)


def get_status_calb(device_id: DeviceT,
                    calibration: Calibration) -> StatusCalb:
    """Return device state.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param calibration: user unit settings Calibrated device state. Useful
    structure that contains current controller status, including speed,
    position and boolean flags
    :type calibration: Calibration
    :return: structure with snapshot of controller status
    :rtype: StatusCalb
    """
    _check_device_id(device_id)
    if not isinstance(calibration, Calibration):
        raise TypeError("calibration must be of type Calibration. <{}>"
                        " was got.".format(type(calibration)))
    status = status_calb_t()
    calib = calibration_t(calibration.A, calibration.MicrostepMode)
    _check_result(lib.get_status_calb(device_id, byref(status), byref(calib)))
    return StatusCalb(status.MoveSts,
                      status.MvCmdSts,
                      status.PWRSts,
                      status.EncSts,
                      status.WindSts,
                      status.CurPosition,
                      status.EncPosition,
                      status.CurSpeed,
                      status.Ipwr,
                      status.Upwr,
                      status.Iusb,
                      status.Uusb,
                      status.CurT,
                      status.Flags,
                      status.GPIOFlags,
                      status.CmdBufFreeSpace)


def get_enumerate_device_controller_name(
        device_enumeration: POINTER(device_enumeration_t),
        device_index: int) -> str:
    """Get controller name from the device enumeration.

    Returns device_index device controller name

    :param device_enumeration: opaque pointer to an enumeration device data
    :type device_enumeration: POINTER(device_enumeration_t)
    :param device_index: device index
    :type device_index: int
    :return: controller name
    :rtype: str
    """
    if not isinstance(device_enumeration, POINTER(device_enumeration_t)):
        raise TypeError("device_enumeration must be of type"
                        " POINTER(device_enumeration_t). <{}> was got."
                        .format(type(device_enumeration)))
    if not isinstance(device_index, int):
        raise TypeError("device_index must be of type int."
                        " <{}> was got.".format(type(device_enumeration)))
    name = c_char_p(r'\0'*128)
    _check_result(lib.get_enumerate_device_controller_name(device_enumeration,
                                                           device_index, name))
    return str(name)


def get_enumerate_device_stage_name(
        device_enumeration: POINTER(device_enumeration_t),
        device_index: int) -> str:
    """Get stage name from the device enumeration.

    Returns device_index device stage name.

    :param device_enumeration: opaque pointer to an enumeration device data
    :type device_enumeration: POINTER(device_enumeration_t)
    :param device_index: device index
    :type device_index: int
    :return: stage name
    :rtype: str
    """
    if not isinstance(device_enumeration, POINTER(device_enumeration_t)):
        raise TypeError("device_enumeration must be of type"
                        " POINTER(device_enumeration_t). <{}> was got."
                        .format(type(device_enumeration)))
    if not isinstance(device_index, int):
        raise TypeError("device_index must be of type int."
                        " <{}> was got.".format(type(device_enumeration)))
    name = c_char_p(r'\0'*128)
    _check_result(lib.get_enumerate_device_stage_name(device_enumeration,
                                                      device_index, name))
    return str(name)


def get_enumerate_device_network_information(
        device_enumeration: POINTER(device_enumeration_t),
        device_index: int) -> device_network_information_t:
    """Get device network information from the device enumeration.

    Returns device_index device network information.

    :param device_enumeration: 	opaque pointer to an enumeration device data
    :type device_enumeration: POINTER(device_enumeration_t)
    :param device_index: device index
    :type device_index: int
    :return: device network information data
    :rtype: device_network_information_t
    """
    if not isinstance(device_enumeration, POINTER(device_enumeration_t)):
        raise TypeError("device_enumeration must be of type"
                        " POINTER(device_enumeration_t). <{}> was got."
                        .format(type(device_enumeration)))
    if not isinstance(device_index, int):
        raise TypeError("device_index must be of type int."
                        " <{}> was got.".format(type(device_enumeration)))
    device_network_information = device_network_information_t()
    _check_result(
        lib.get_enumerate_device_network_information(
                                    device_enumeration,
                                    device_index,
                                    byref(device_network_information)))
    return device_network_information


def command_wait_for_stop(device_id: DeviceT,
                          refresh_interval_ms: int) -> None:
    """Wait for stop.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :param refresh_interval_ms: Status refresh interval. The function waits
    this number of milliseconds between get_status requests to the controller.
    Recommended value of this parameter is 10 ms. Use values of less than 3 ms
    only when necessary - small refresh interval values do not significantly
    increase response time of the function, but they create substantially more
    traffic in controller-computer data channel.
    :type refresh_interval_ms: int
    """
    _check_device_id(device_id)
    if not isinstance(refresh_interval_ms, int):
        raise TypeError("refresh_interval_ms must be of type int."
                        " <{}> was got.".format(type(refresh_interval_ms)))
    _check_result(lib.command_wait_for_stop(device_id,
                                            c_uint32(refresh_interval_ms)))


def command_homezero(device_id: DeviceT) -> None:
    """Make home command, wait until it is finished and make zero command.

    This is a convinient way to calibrate zero position.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    """
    _check_device_id(device_id)
    _check_result(lib.command_homezero(device_id))


def set_bindy_key(keyfilepath: str) -> None:
    """Set network encryption layer (bindy) key.

    :param keyfilepath: full path to the bindy keyfile When using
    network-attached devices this function must be called before
    enumerate_devices and open_device functions.
    :type keyfilepath: str
    """
    if not isinstance(keyfilepath, str):
        raise TypeError("keyfilepath must be of type str."
                        " <{}> was got.".format(type(keyfilepath)))
    _check_result(lib.set_bindy_key(keyfilepath))


def open_device(uri: str) -> DeviceT:
    """Open a device with OS uri uri and return identifier of the device which
    can be used in calls.

    :param uri: a device uri. Device uri has form "xi-com:port" or
    "xi-net://host/serial" or "xi-emu:///file". In case of USB-COM port the
    "port" is the OS device uri. For example "xi-com:\\\\.\\COM3" in Windows or
    "xi-com:/dev/tty.s123" in Linux/Mac. In case of network device the "host"
    is an IPv4 address or fully qualified domain uri (FQDN), "serial" is the
    device serial number in hexadecimal system. For example
    "xi-net://192.168.0.1/00001234" or "xi-net://hostname.com/89ABCDEF".
    In case of UDP protocol, use "xi-udp://<ip/host>:<port>. For example,
    "xi-udp://192.168.0.1:1818". Note: to open network device you must call
    set_bindy_key first. In case of virtual device the "file" is the full
    filename with device memory state, if it doesn't exist then it is
    initialized with default values. For example "xi-emu:///C:/dir/file.bin"
    in Windows or "xi-emu:///home/user/file.bin" in Linux/Mac.
    :type uri: str
    :raises ConnectionError:
    """
    if not isinstance(uri, str):
        raise TypeError("uri must be of type str."
                        " <{}> was got.".format(type(uri)))
    device_id = DeviceT(lib.open_device(uri.encode()))
    if (device_id < 0):
        raise ConnectionError(
            "Cannot connect to device via URI='{}'\n"
            "\t* check URI. For URI format see documentation for "
            "open_device() on https://libximc.xisupport.com/doc-en/"
            "\t* check whether it's connected to computer physically,"
            " powered and not occupied by another app\n"
            .format(uri)
        )
    return device_id


def close_device(device_id: DeviceT) -> None:
    """Close specified device.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    """
    _check_device_id(device_id)
    _check_result(lib.close_device(byref(cast(device_id, POINTER(c_int)))))


def get_position(device_id: DeviceT) -> GetPosition:
    """Reads the value position in steps and micro for stepper motor and
    encoder steps all engines.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    :return: GetPosition objects
    :rtype: GetPosition
    """
    _check_device_id(device_id)
    position = get_position_t()
    _check_result(lib.get_position(device_id, byref(position)))
    return GetPosition(position.Position,
                       position.uPosition,
                       position.EncPosition)


def command_move(device_id: DeviceT,
                 position: int,
                 uposition: int) -> None:
    _check_device_id(device_id)
    if not isinstance(position, int):
        raise TypeError("position must be of type int."
                        " <{}> was got.".format(type(position)))
    if not isinstance(uposition, int):
        raise TypeError("uposition must be of type int."
                        " <{}> was got.".format(type(uposition)))
    _check_result(lib.command_move(device_id, position, uposition))


def command_stop(device_id: DeviceT) -> None:
    """Immediately stop the engine, the transition to the STOP, mode key BREAK
    (winding short-circuited), the regime "retention" is deactivated for DC
    motors, keeping current in the windings for stepper motors (with Power
    management settings).

    When this command is called, the ALARM flag is reset.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    """
    _check_device_id(device_id)
    _check_result(lib.command_stop(device_id))


def command_power_off(device_id: DeviceT):
    """Immediately power off motor regardless its state.

    Shouldn't be used during motion as the motor could be power on again
    automatically to continue movement. The command is designed for manual
    motor power off. When automatic power off after stop is required, use
    power management system.

    :param device_id: an identifier of device
    :type device_id: DeviceT
    """
    _check_device_id(device_id)
    _check_result(lib.command_power_off(device_id))


# vim: set ft=python
