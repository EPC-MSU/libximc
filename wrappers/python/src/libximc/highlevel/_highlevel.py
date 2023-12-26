""" Python binding for libximc
=======================================================================================================================

file: highlevel.py

Description: This file contains definition of Axis class and general functions such as enumerate_device.
"""
# Necessary ctypes imports
from ctypes import cast, byref, POINTER
from ctypes import c_int, c_uint, c_uint32, c_float, c_double, c_char_p

# ========================================= #
# Import necessary libximc.lowlevel objects #
# ========================================= #
# Import library object
from libximc.lowlevel._lowlevel import lib
# Import libximc.lowlevel
from libximc.lowlevel import _lowlevel as ll


# ================================== #
# Import necessary highlevel objects #
# ================================== #
from libximc.highlevel._structure_types import (feedback_settings_t,
                                                home_settings_t,
                                                home_settings_calb_t,
                                                move_settings_t,
                                                move_settings_calb_t,
                                                engine_settings_t,
                                                engine_settings_calb_t,
                                                entype_settings_t,
                                                power_settings_t,
                                                secure_settings_t,
                                                edges_settings_t,
                                                edges_settings_calb_t,
                                                pid_settings_t,
                                                sync_in_settings_t,
                                                sync_in_settings_calb_t,
                                                sync_out_settings_t,
                                                sync_out_settings_calb_t,
                                                extio_settings_t,
                                                brake_settings_t,
                                                control_settings_t,
                                                control_settings_calb_t,
                                                joystick_settings_t,
                                                ctp_settings_t,
                                                uart_settings_t,
                                                controller_name_t,
                                                nonvolatile_memory_t,
                                                emf_settings_t,
                                                engine_advansed_setup_t,
                                                engine_advanced_setup_t,
                                                get_position_t,
                                                get_position_calb_t,
                                                set_position_t,
                                                set_position_calb_t,
                                                status_t,
                                                status_calb_t,
                                                measurements_t,
                                                chart_data_t,
                                                device_information_t,
                                                stage_name_t,
                                                NOT_INITIALIZED)
from libximc.highlevel import _flag_enumerations as flag_enumerations


# =================== #
# Supporting routines #
# =================== #
def _check_result(result: int) -> None:
    if result == flag_enumerations.Result.Ok:
        return
    if result == flag_enumerations.Result.Error:
        raise RuntimeError("General Error")
    if result == flag_enumerations.Result.NotImplemented:
        raise NotImplementedError(
            "This function is not implemented in the device. Firmware update may be required: "
            "https://doc.xisupport.com/en/8smc5-usb/8SMCn-USB/XILab_application_Users_guide/Controller_Settings/"
            "About_controller.html"
        )
    if result == flag_enumerations.Result.ValueError:
        raise ValueError(
            "The input was rejected by the device. Some parameters may have incorrect values."
            "Check documentation: https://libximc.xisupport.com/doc-en/ximc_8h.html"
        )
    if result == flag_enumerations.Result.NoDevice:
        raise ConnectionError(
            "Cannot send command to the device. Check connection and power. To resume operation you should reopen"
            " the device."
        )


def _check_fullness(structure_object) -> None:
    for key_value_pair in structure_object.__dict__.items():
        if key_value_pair[1] is NOT_INITIALIZED:
            # All attributes of structure objects from structure_types.py are @properties and their actual names start
            # with underscore (_). So, the first symbol must be omitted -> that's why [1:] is used
            attribute_name = key_value_pair[0][1:]
            raise ValueError("{}.{} must be set!".format(structure_object.__class__.__name__, attribute_name))


# ========== #
# Axis class #
# ========== #
class Axis:
    """Class representing an axis

    :param uri: a device uri. Device uri has form "xi-com:port" or "xi-net://host/serial" or "xi-emu:///abs-file-path".
        In case of USB-COM port the "port" is the OS device uri. For example "xi-com:\\\\.\\COM3" in Windows or
        "xi-com:/dev/tty.s123" in Linux/Mac. In case of network device the "host" is an IPv4 address or fully
        qualified domain uri (FQDN), "serial" is the device serial number in hexadecimal system. For example
        "xi-net://192.168.0.1/00001234" or "xi-net://hostname.com/89ABCDEF". In case of UDP protocol, use
        "xi-udp://<ip/host>:<port>. For example, "xi-udp://192.168.0.1:1818". Note: to open network device you
        must call set_bindy_key first. In case of virtual device the "file" is the full filename with device
        memory state, if it doesn't exist then it is initialized with default values. For example
        "xi-emu:///C:/dir/file.bin" in Windows or "xi-emu:///home/user/file.bin" in Linux/Mac.
    :type uri: str
    """
    def __init__(self, uri: str) -> None:
        self._is_opened = False
        self._is_calibration_set = False
        try:
            uri.encode()
        except Exception:
            raise TypeError("Wrong uri type! Expected string, but {} was got.".format(type(uri)))
        self.uri = uri
        self._lowlevel_calib = ll.calibration_t()

    def _check_device_opened(self) -> None:
        if not self._is_opened:
            raise RuntimeError("Device must be opened! Have you forgotten Axis.open_device()?")

    @property
    def _calib(self) -> ll.calibration_t:
        if not self._is_calibration_set:
            raise RuntimeError("Calibration settings haven't been set! Use Axis.set_calb() to set it.")
        return self._lowlevel_calib

    @_calib.setter
    def _calib(self, value):
        raise RuntimeError("Axis._calib cannot be set this way. Use Axis.set_calb() instead.")

    def set_calb(self, A: float, MicrostepMode: flag_enumerations.MicrostepMode) -> None:
        """Sets units calibration settings.

        To use user units instead of [steps] calibration parameters needs to be set. It allows the library to convert
        its internal step-units to desired user units. Conversion formula:

        user_units = A * (steps + u_steps / 2**(MicrostepRegime - 1))

        :param A: factor
        :type A: float
        :param MicrostepMode: flag describing the microstep mode used.
        :type MicrostepMode: MicrostepMode
        """
        try:
            c_double(A)
        except Exception:
            raise TypeError("Unable to cast A to ctypes' c_double. Try A of float type.")
        if MicrostepMode not in flag_enumerations.MicrostepMode._value2member_map_:
            allowed_flags = "\tMicrostepMode." + "\n\tMicrostepMode.".join((flag._name_ for flag in MicrostepMode))
            raise TypeError("MicrostepMode must be of type MicrostepMode. Allowed values are:\n{}"
                            .format(allowed_flags))
        self._lowlevel_calib = ll.calibration_t(A, MicrostepMode)
        self._is_calibration_set = True

    def get_calb(self) -> tuple:
        """Returns units calibration settings as a dict.

        :return: units calibration settings.
        :rtype: tuple
        """
        return (self._calib.A, flag_enumerations.MicrostepMode(self._calib.MicrostepMode))

    def set_feedback_settings(self, settings: feedback_settings_t) -> None:
        """Feedback settings.

        :param: feedback settings
        :type settings: feedback_settings_t
        """
        self._check_device_opened()
        if not isinstance(settings, feedback_settings_t):
            raise TypeError("settings must be of type feedback_settings_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        feedback_settings = ll.feedback_settings_t(settings.IPS,
                                                   int(settings.FeedbackType),
                                                   int(settings.FeedbackFlags),
                                                   settings.CountsPerTurn)
        _check_result(lib.set_feedback_settings(self._device_id, byref(feedback_settings)))

    def get_feedback_settings(self) -> feedback_settings_t:
        """Feedback settings.

        :return: feedback settings
        :rtype: feedback_settings_t
        """
        self._check_device_opened()
        feedback_settings = ll.feedback_settings_t()
        _check_result(lib.get_feedback_settings(self._device_id, byref(feedback_settings)))
        return feedback_settings_t(feedback_settings.IPS,
                                   feedback_settings.FeedbackType,
                                   feedback_settings.FeedbackFlags,
                                   feedback_settings.CountsPerTurn)

    def set_home_settings(self, settings: home_settings_t) -> None:
        """Set home settings.

        This function sends home position structure to the controller's memory.

        :param settings: home settings
        :type settings: home_settings_t
        """
        self._check_device_opened()
        if not isinstance(settings, home_settings_t):
            raise TypeError("settings must be of type home_settings_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        home_settings = ll.home_settings_t(settings.FastHome,
                                           settings.uFastHome,
                                           settings.SlowHome,
                                           settings.uSlowHome,
                                           settings.HomeDelta,
                                           settings.uHomeDelta,
                                           int(settings.HomeFlags))
        _check_result(lib.set_home_settings(self._device_id, byref(home_settings)))

    def get_home_settings(self) -> home_settings_t:
        """Read home settings.

        This function reads the structure with home position settings.

        :return: home settings
        :rtype: home_settings_t
        """
        self._check_device_opened()
        home_settings = ll.home_settings_t()
        _check_result(lib.get_home_settings(self._device_id, byref(home_settings)))
        return home_settings_t(home_settings.FastHome,
                               home_settings.uFastHome,
                               home_settings.SlowHome,
                               home_settings.uSlowHome,
                               home_settings.HomeDelta,
                               home_settings.uHomeDelta,
                               home_settings.HomeFlags)

    def set_home_settings_calb(self, settings: home_settings_calb_t) -> None:
        """Set home settings which use user units.

        This function sends home position structure to the controller's memory.

        :param settings: calibration home settings
        :type settings: home_settings_calb_t
        """
        self._check_device_opened()
        if not isinstance(settings, home_settings_calb_t):
            raise TypeError("settings must be of type home_settings_calb_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        home_settings = ll.home_settings_calb_t(settings.FastHome,
                                                settings.SlowHome,
                                                settings.HomeDelta,
                                                int(settings.HomeFlags))
        _check_result(lib.set_home_settings_calb(self._device_id, byref(home_settings), byref(self._calib)))

    def get_home_settings_calb(self) -> home_settings_calb_t:
        """Read user unit home settings.

        This function reads the structure with home position settings.

        :return: calibration home settings
        :rtype: home_settings_calb_t
        """
        self._check_device_opened()
        home_settings = ll.home_settings_calb_t()
        _check_result(lib.get_home_settings_calb(self._device_id, byref(home_settings), byref(self._calib)))
        return home_settings_calb_t(home_settings.FastHome,
                                    home_settings.SlowHome,
                                    home_settings.HomeDelta,
                                    home_settings.HomeFlags)

    def set_move_settings(self, settings: move_settings_t) -> None:
        """Movement settings set command (speed, acceleration, threshold, etc.).

        :param settings: structure contains move settings: speed, acceleration, deceleration etc.
        :type settings: move_settings_t
        """
        self._check_device_opened()
        if not isinstance(settings, move_settings_t):
            raise TypeError("settings must be of type MoveSettings. {} was MoveSettings.".format(type(settings)))
        _check_fullness(settings)
        move_settings = ll.move_settings_t(settings.Speed,
                                           settings.uSpeed,
                                           settings.Accel,
                                           settings.Decel,
                                           settings.AntiplaySpeed,
                                           settings.uAntiplaySpeed,
                                           int(settings.MoveFlags))
        _check_result(lib.set_move_settings(self._device_id, byref(move_settings)))

    def set_move_settings_calb(self, settings: move_settings_calb_t) -> None:
        """User unit movement settings set command (speed, acceleration, threshold, etc.).

        :param settings: structure contains move settings: speed, acceleration, deceleration etc.
        :type settings: move_settings_calb_t
        """
        self._check_device_opened()
        if not isinstance(settings, move_settings_calb_t):
            raise TypeError("settings must be of type move_settings_calb_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        move_settings = ll.move_settings_calb_t(settings.Speed,
                                                settings.Accel,
                                                settings.Decel,
                                                settings.AntiplaySpeed,
                                                int(settings.MoveFlags))
        _check_result(lib.set_move_settings_calb(self._device_id, byref(move_settings), byref(self._calib)))

    def get_move_settings(self) -> move_settings_t:
        """Movement settings read command (speed, acceleration, threshold, etc.).

        :return: move settings
        :rtype: move_settings_t
        """
        self._check_device_opened()
        move_settings = ll.move_settings_t()
        _check_result(lib.get_move_settings(self._device_id, byref(move_settings)))
        return move_settings_t(move_settings.Speed,
                               move_settings.uSpeed,
                               move_settings.Accel,
                               move_settings.Decel,
                               move_settings.AntiplaySpeed,
                               move_settings.uAntiplaySpeed,
                               move_settings.MoveFlags)

    def get_move_settings_calb(self) -> move_settings_calb_t:
        """User unit movement settings read command

        :return: calibration move settings
        :rtype: move_settings_calb_t
        """
        self._check_device_opened()
        move_settings = ll.move_settings_calb_t()
        _check_result(lib.get_move_settings_calb(self._device_id, byref(move_settings), byref(self._calib)))
        return move_settings_calb_t(move_settings.Speed,
                                    move_settings.Accel,
                                    move_settings.Decel,
                                    move_settings.AntiplaySpeed,
                                    move_settings.MoveFlags)

    def set_engine_settings(self, settings: engine_settings_t) -> None:
        """Set engine settings.

        This function sends a structure with a set of engine settings to the controller's memory. These settings
        specify the motor shaft movement algorithm, list of limitations and rated characteristics. Use it when you
        change the motor, encoder, positioner, etc. Please note that wrong engine settings may lead to device
        malfunction, which can cause irreversible damage to the board.

        :param settings: engine settings
        :type settings: engine_settings_t
        """
        self._check_device_opened()
        if not isinstance(settings, engine_settings_t):
            raise TypeError("settings must be of type engine_settings_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        engine_settings = ll.engine_settings_t(settings.NomVoltage,
                                               settings.NomCurrent,
                                               settings.NomSpeed,
                                               settings.uNomSpeed,
                                               int(settings.EngineFlags),
                                               settings.Antiplay,
                                               int(settings.MicrostepMode),
                                               settings.StepsPerRev)
        _check_result(lib.set_engine_settings(self._device_id, byref(engine_settings)))

    def set_engine_settings_calb(self, settings: engine_settings_calb_t) -> None:
        """Set user unit engine settings.

        This function sends a structure with a set of engine settings to the controller's memory. These settings
        specify the motor shaft movement algorithm, list of limitations and rated characteristics. Use it when you
        change the motor, encoder, positioner etc. Please note that wrong engine settings may lead to device
        malfunction, which can cause irreversible damage to the board.

        :param settings: calibration engine settings
        :type settings: engine_settings_calb_t
        """
        self._check_device_opened()
        if not isinstance(settings, engine_settings_calb_t):
            raise TypeError("settings must be of type engine_settings_calb_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        engine_settings = ll.engine_settings_calb_t(settings.NomVoltage,
                                                    settings.NomCurrent,
                                                    settings.NomSpeed,
                                                    int(settings.EngineFlags),
                                                    settings.Antiplay,
                                                    int(settings.MicrostepMode),
                                                    settings.StepsPerRev)
        _check_result(lib.set_engine_settings_calb(self._device_id, byref(engine_settings), byref(self._calib)))

    def get_engine_settings(self) -> engine_settings_t:
        """Read engine settings.

        This function reads the structure containing a set of useful motor settings stored in the controller's memory.
        These settings specify motor shaft movement algorithm, list of limitations and rated characteristics.

        :return: engine settings
        :rtype: engine_settings_t
        """
        self._check_device_opened()
        engine_settings = ll.engine_settings_t()
        _check_result(lib.get_engine_settings(self._device_id, byref(engine_settings)))
        return engine_settings_t(engine_settings.NomVoltage,
                                 engine_settings.NomCurrent,
                                 engine_settings.NomSpeed,
                                 engine_settings.uNomSpeed,
                                 engine_settings.EngineFlags,
                                 engine_settings.Antiplay,
                                 engine_settings.MicrostepMode,
                                 engine_settings.StepsPerRev)

    def get_engine_settings_calb(self) -> engine_settings_calb_t:
        """Read user unit engine settings.

        This function reads the structure containing a set of useful motor settings stored in  the controller's memory.
        These settings specify the motor shaft movement algorithm, list of limitations and rated characteristics.

        :return: calibrated engine settings
        :rtype: engine_settings_calb_t
        """
        self._check_device_opened()
        engine_settings = ll.engine_settings_calb_t()
        _check_result(lib.get_engine_settings_calb(self._device_id, byref(engine_settings), byref(self._calib)))
        return engine_settings_calb_t(engine_settings.NomVoltage,
                                      engine_settings.NomCurrent,
                                      engine_settings.NomSpeed,
                                      engine_settings.EngineFlags,
                                      engine_settings.Antiplay,
                                      engine_settings.MicrostepMode,
                                      engine_settings.StepsPerRev)

    def set_entype_settings(self, settings: entype_settings_t) -> None:
        """Set engine type and driver type.

        :param settings: structure contains motor type and power driver type settings
        :type settings: entype_settings_t
        """
        self._check_device_opened()
        if not isinstance(settings, entype_settings_t):
            raise TypeError("settings must be of type entype_settings_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        entype_settings = ll.entype_settings_t(int(settings.EngineType), int(settings.DriverType))
        _check_result(lib.set_entype_settings(self._device_id, byref(entype_settings)))

    def get_entype_settings(self) -> entype_settings_t:
        """Return engine type and driver type.

        :return: entype settings
        :rtype: entype_settings_t
        """
        self._check_device_opened()
        entype_settings = ll.entype_settings_t()
        _check_result(lib.get_entype_settings(self._device_id, byref(entype_settings)))
        return entype_settings_t(entype_settings.EngineType, entype_settings.DriverType)

    def set_power_settings(self, settings: power_settings_t) -> None:
        """Set settings of step motor power control.

        Used with stepper motor only.

        :param settings: structure contains settings of step motor power control
        :type settings: power_settings_t
        """
        self._check_device_opened()
        if not isinstance(settings, power_settings_t):
            raise TypeError("settings must be of type power_settings_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        power_settings = ll.power_settings_t(settings.HoldCurrent,
                                             settings.CurrReductDelay,
                                             settings.PowerOffDelay,
                                             settings.CurrentSetTime,
                                             int(settings.PowerFlags))
        _check_result(lib.set_power_settings(self._device_id, byref(power_settings)))

    def get_power_settings(self) -> power_settings_t:
        """Read settings of step motor power control.

        Used with stepper motor only.

        :return: A structure containing settings of step motor power control
        :rtype: power_settings_t
        """
        self._check_device_opened()
        power_settings = ll.power_settings_t()
        _check_result(lib.get_power_settings(self._device_id, byref(power_settings)))
        return power_settings_t(power_settings.HoldCurrent,
                                power_settings.CurrReductDelay,
                                power_settings.PowerOffDelay,
                                power_settings.CurrentSetTime,
                                power_settings.PowerFlags)

    def set_secure_settings(self, settings: secure_settings_t) -> None:
        """Set protection settings.

        :param settings: structure with secure data
        :type settings: secure_settings_t
        """
        self._check_device_opened()
        if not isinstance(settings, secure_settings_t):
            raise TypeError("settings must be of type secure_settings_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        secure_settings = ll.secure_settings_t(settings.LowUpwrOff,
                                               settings.CriticalIpwr,
                                               settings.CriticalUpwr,
                                               settings.CriticalT,
                                               settings.CriticalIusb,
                                               settings.CriticalUusb,
                                               settings.MinimumUusb,
                                               int(settings.Flags))
        _check_result(lib.set_secure_settings(self._device_id, byref(secure_settings)))

    def get_secure_settings(self) -> secure_settings_t:
        """Read protection settings.

        :return: critical parameter settings to protect the hardware
        :rtype: secure_settings_t
        """
        self._check_device_opened()
        secure_settings = ll.secure_settings_t()
        _check_result(lib.get_secure_settings(self._device_id, byref(secure_settings)))
        return secure_settings_t(secure_settings.LowUpwrOff,
                                 secure_settings.CriticalIpwr,
                                 secure_settings.CriticalUpwr,
                                 secure_settings.CriticalT,
                                 secure_settings.CriticalIusb,
                                 secure_settings.CriticalUusb,
                                 secure_settings.MinimumUusb,
                                 secure_settings.Flags)

    def set_edges_settings(self, settings: edges_settings_t) -> None:
        """Set border and limit switches settings.

        :param settings: edges settings, specify types of borders, motor behavior and electrical behavior of limit
            switches
        :type settings: edges_settings_t
        """
        self._check_device_opened()
        if not isinstance(settings, edges_settings_t):
            raise TypeError("settings must be of type edges_settings_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        edges_settings = ll.edges_settings_t(int(settings.BorderFlags),
                                             int(settings.EnderFlags),
                                             settings.LeftBorder,
                                             settings.uLeftBorder,
                                             settings.RightBorder,
                                             settings.uRightBorder)
        _check_result(lib.set_edges_settings(self._device_id, byref(edges_settings)))

    def set_edges_settings_calb(self, settings: edges_settings_calb_t) -> None:
        """Set border and limit switches settings in user units.

        :param settings: edges settings, specify types of borders, motor behavior and electrical behavior of limit
            switches
        :type settings: edges_settings_calb_t
        """
        self._check_device_opened()
        if not isinstance(settings, edges_settings_calb_t):
            raise TypeError("settings must be of type edges_settings_calb_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        edges_settings = ll.edges_settings_calb_t(int(settings.BorderFlags),
                                                  int(settings.EnderFlags),
                                                  settings.LeftBorder,
                                                  settings.RightBorder)
        _check_result(lib.set_edges_settings_calb(self._device_id, byref(edges_settings), byref(self._calib)))

    def get_edges_settings(self) -> edges_settings_t:
        """Read border and limit switches settings.

        :return: edges settings, types of borders, motor behavior and electrical behavior of limit switches
        :rtype: edges_settings_t
        """
        self._check_device_opened()
        edges_settings = ll.edges_settings_t()
        _check_result(lib.get_edges_settings(self._device_id, byref(edges_settings)))
        return edges_settings_t(edges_settings.BorderFlags,
                                edges_settings.EnderFlags,
                                edges_settings.LeftBorder,
                                edges_settings.uLeftBorder,
                                edges_settings.RightBorder,
                                edges_settings.uRightBorder)

    def get_edges_settings_calb(self) -> edges_settings_calb_t:
        """Read border and limit switches settings in user units.

        :return: edges settings, types of borders, motor behavior and electrical behavior of limit switches
        :rtype: edges_settings_calb_t
        """
        self._check_device_opened()
        edges_settings = ll.edges_settings_calb_t()
        _check_result(lib.get_edges_settings_calb(self._device_id, byref(edges_settings), byref(self._calib)))
        return edges_settings_calb_t(edges_settings.BorderFlags,
                                     edges_settings.EnderFlags,
                                     edges_settings.LeftBorder,
                                     edges_settings.RightBorder)

    def set_pid_settings(self, settings: pid_settings_t) -> None:
        """Set PID settings.

        This function sends the structure with a set of PID factors to the controller's memory. These settings specify
        the behavior of the PID routine for the positioner. These factors are slightly different for different
        positioners. All boards are supplied with the standard set of PID settings in the controller's flash memory.
        Please use it for loading new PID settings when you change positioner. Please note that wrong PID settings
        lead to device malfunction.

        :param settings: PID settings
        :type settings: pid_settings_t
        """
        self._check_device_opened()
        if not isinstance(settings, pid_settings_t):
            raise TypeError("settings must be of type pid_settings_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        pid_settings = ll.pid_settings_t(settings.KpU,
                                         settings.KiU,
                                         settings.KdU,
                                         settings.Kpf,
                                         settings.Kif,
                                         settings.Kdf)
        _check_result(lib.set_pid_settings(self._device_id, byref(pid_settings)))

    def get_pid_settings(self) -> pid_settings_t:
        """Read PID settings.

        This function reads the structure containing a set of motor PID settings stored in the controller's memory.
        These settings specify the behavior of the PID routine for the positioner. These factors are slightly
        different for different positioners. All boards are supplied with the standard set of PID settings in the
        controller's flash memory.

        :return: PID settings
        :rtype: pid_settings_t
        """
        self._check_device_opened()
        pid_settings = ll.pid_settings_t()
        _check_result(lib.get_pid_settings(self._device_id, byref(pid_settings)))
        return pid_settings_t(pid_settings.KpU,
                              pid_settings.KiU,
                              pid_settings.KdU,
                              pid_settings.Kpf,
                              pid_settings.Kif,
                              pid_settings.Kdf)

    def set_sync_in_settings(self, settings: sync_in_settings_t) -> None:
        """Set input synchronization settings.

        This function sends the structure with a set of input synchronization settings that specify the behavior of
        input synchronization to the controller's memory. All boards are supplied with the standard set of these
        settings.

        :param settings: synchronization settings
        :type settings: sync_in_settings_t
        """
        self._check_device_opened()
        if not isinstance(settings, sync_in_settings_t):
            raise TypeError("settings must be of type sync_in_settings_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        sync_in_settings = ll.sync_in_settings_t(int(settings.SyncInFlags),
                                                 settings.ClutterTime,
                                                 settings.Position,
                                                 settings.uPosition,
                                                 settings.Speed,
                                                 settings.uSpeed)
        _check_result(lib.set_sync_in_settings(self._device_id, byref(sync_in_settings)))

    def set_sync_in_settings_calb(self, settings: sync_in_settings_calb_t) -> None:
        """Set input synchronization settings.

        This function sends the structure with a set of input synchronization settings that specify the behavior of
        input synchronization to the controller's memory. All boards are supplied with the standard set of these
        settings.

        :param settings: synchronization settings in user units
        :type settings: sync_in_settings_calb_t
        """
        self._check_device_opened()
        if not isinstance(settings, sync_in_settings_calb_t):
            raise TypeError("settings must be of type sync_in_settings_calb_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        sync_in_settings = ll.sync_in_settings_calb_t(int(settings.SyncInFlags),
                                                      settings.ClutterTime,
                                                      settings.Position,
                                                      settings.Speed)
        _check_result(lib.set_sync_in_settings_calb(self._device_id, byref(sync_in_settings), byref(self._calib)))

    def get_sync_in_settings(self) -> sync_in_settings_t:
        """Read input synchronization settings.

        This function reads the structure with a set of input synchronization settings, modes, periods and flags that
        specify the behavior of input synchronization. All boards are supplied with the standard set of these settings.

        :return: synchronization settings
        :rtype: sync_in_settings_t
        """
        self._check_device_opened()
        sync_in_settings = ll.sync_in_settings_t()
        _check_result(lib.get_sync_in_settings(self._device_id, byref(sync_in_settings)))
        return sync_in_settings_t(sync_in_settings.SyncInFlags,
                                  sync_in_settings.ClutterTime,
                                  sync_in_settings.Position,
                                  sync_in_settings.uPosition,
                                  sync_in_settings.Speed,
                                  sync_in_settings.uSpeed)

    def get_sync_in_settings_calb(self) -> sync_in_settings_calb_t:
        """Read input user unit synchronization settings.

        This function reads the structure with a set of input synchronization settings, modes, periods and flags that
        specify the behavior of input synchronization. All boards are supplied with the standard set of these settings.

        :return: synchronization settings in user units
        :rtype: sync_in_settings_calb_t
        """
        self._check_device_opened()
        sync_in_settings = ll.sync_in_settings_calb_t()
        _check_result(lib.get_sync_in_settings_calb(self._device_id, byref(sync_in_settings), byref(self._calib)))
        return sync_in_settings_calb_t(sync_in_settings.SyncInFlags,
                                       sync_in_settings.ClutterTime,
                                       sync_in_settings.Position,
                                       sync_in_settings.Speed)

    def set_sync_out_settings(self, settings: sync_out_settings_t) -> None:
        """Set output synchronization settings.

        This function sends the structure with a set of output synchronization settings that specify the behavior of
        output synchronization to the controller's memory. All boards are supplied with the standard set of these
        settings.

        :param settings: synchronization settings
        :type settings: sync_out_settings_t
        """
        self._check_device_opened()
        if not isinstance(settings, sync_out_settings_t):
            raise TypeError("settings must be of type sync_out_settings_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        sync_out_settings = ll.sync_out_settings_t(int(settings.SyncOutFlags),
                                                   settings.SyncOutPulseSteps,
                                                   settings.SyncOutPeriod,
                                                   settings.Accuracy,
                                                   settings.uAccuracy)
        _check_result(lib.set_sync_out_settings(self._device_id, byref(sync_out_settings)))

    def set_sync_out_settings_calb(self, settings: sync_out_settings_calb_t) -> None:
        """Set output user unit synchronization settings.

        This function sends the structure with a set of output synchronization settings that specify the behavior of
        output synchronization to the controller's memory. All boards are supplied with the standard set of these
        settings.

        :param settings: synchronization settings in user units
        :type settings: sync_out_settings_calb_t
        """
        self._check_device_opened()
        if not isinstance(settings, sync_out_settings_calb_t):
            raise TypeError("settings must be of type sync_out_settings_calb_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        sync_out_settings = ll.sync_out_settings_calb_t(int(settings.SyncOutFlags),
                                                        settings.SyncOutPulseSteps,
                                                        settings.SyncOutPeriod,
                                                        settings.Accuracy)
        _check_result(lib.set_sync_out_settings_calb(self._device_id, byref(sync_out_settings), byref(self._calib)))

    def get_sync_out_settings(self) -> sync_out_settings_t:
        """Read output synchronization settings.

        This function reads the structure containing a set of output synchronization settings, modes, periods and flags
        that specify the behavior of output synchronization. All boards are supplied with the standard set of these
        settings.

        :return: synchronization settings
        :rtype: sync_out_settings_t
        """
        self._check_device_opened()
        sync_out_settings = ll.sync_out_settings_t()
        _check_result(lib.get_sync_out_settings(self._device_id, byref(sync_out_settings)))
        return sync_out_settings_t(sync_out_settings.SyncOutFlags,
                                   sync_out_settings.SyncOutPulseSteps,
                                   sync_out_settings.SyncOutPeriod,
                                   sync_out_settings.Accuracy,
                                   sync_out_settings.uAccuracy)

    def get_sync_out_settings_calb(self) -> sync_out_settings_calb_t:
        """ead output user unit synchronization settings.

        This function reads the structure containing a set of output synchronization settings, modes, periods and flags
        that specify the behavior of output synchronization. All boards are supplied with the standard set of these
        settings.

        :return: synchronization settings in user units
        :rtype: sync_out_settings_calb_t
        """
        self._check_device_opened()
        sync_out_settings = ll.sync_out_settings_calb_t()
        _check_result(lib.get_sync_out_settings_calb(self._device_id, byref(sync_out_settings), byref(self._calib)))
        return sync_out_settings_calb_t(sync_out_settings.SyncOutFlags,
                                        sync_out_settings.SyncOutPulseSteps,
                                        sync_out_settings.SyncOutPeriod,
                                        sync_out_settings.Accuracy)

    def set_extio_settings(self, settings: extio_settings_t) -> None:
        """Set EXTIO settings.

        This function sends the structure with a set of EXTIO settings to the controller's memory. By default, input
        events are signaled through a rising front, and output states are signaled by a high logic state.

        :param settings: EXTIO settings
        :type settings: extio_settings_t
        """
        self._check_device_opened()
        if not isinstance(settings, extio_settings_t):
            raise TypeError("settings must be of type extio_settings_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        extio_settings = ll.extio_settings_t(int(settings.EXTIOSetupFlags), int(settings.EXTIOModeFlags))
        _check_result(lib.set_extio_settings(self._device_id, byref(extio_settings)))

    def get_extio_settings(self) -> extio_settings_t:
        """Read EXTIO settings.

        This function reads a structure with a set of EXTIO settings from controller's memory.

        :return: EXTIO settings
        :rtype: extio_settings_t
        """
        self._check_device_opened()
        extio_settings = ll.extio_settings_t()
        _check_result(lib.get_extio_settings(self._device_id, byref(extio_settings)))
        return extio_settings_t(extio_settings.EXTIOSetupFlags, extio_settings.EXTIOModeFlags)

    def set_brake_settings(self, settings: brake_settings_t) -> None:
        """Set brake control settings.

        :param settings: structure contains brake control settings
        :type settings: brake_settings_t
        """
        self._check_device_opened()
        if not isinstance(settings, brake_settings_t):
            raise TypeError("settings must be of type brake_settings_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        brake_settings = ll.brake_settings_t(settings.t1,
                                             settings.t2,
                                             settings.t3,
                                             settings.t4,
                                             int(settings.BrakeFlags))
        _check_result(lib.set_brake_settings(self._device_id, byref(brake_settings)))

    def get_brake_settings(self) -> brake_settings_t:
        """Read break control settings.

        :return: structure contains brake control settings
        :rtype: brake_settings_t
        """
        self._check_device_opened()
        brake_settings = ll.brake_settings_t()
        _check_result(lib.get_brake_settings(self._device_id, byref(brake_settings)))
        return brake_settings_t(brake_settings.t1,
                                brake_settings.t2,
                                brake_settings.t3,
                                brake_settings.t4,
                                brake_settings.BrakeFlags)

    def set_control_settings(self, settings: control_settings_t) -> None:
        """Set motor control settings.

        In case of CTL_MODE=1,  joystick motor control is enabled. In this mode, the joystick is maximally displaced,
        the engine tends to move at MaxSpeed[i]. i=0 if another value hasn't been set at the previous usage. To change
        the speed index "i", use the buttons.

        In case of CTL_MODE=2, the motor is controlled by the left/right buttons. When you click on the button, the
        motor starts moving in the appropriate direction at a speed MaxSpeed[0]. After Timeout[i], motor moves at speed
        MaxSpeed[i+1]. At the transition between MaxSpeed[i] and MaxSpeed[i+1] the motor just accelerates/decelerates
        as usual.

        :param settings: structure contains motor control settings
        :type settings: control_settings_t
        """
        self._check_device_opened()
        if not isinstance(settings, control_settings_t):
            raise TypeError("settings must be of type control_settings_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        control_settings = ll.control_settings_t((c_uint * 10)(*settings.MaxSpeed),
                                                 (c_uint * 10)(*settings.uMaxSpeed),
                                                 (c_uint * 9)(*settings.Timeout),
                                                 settings.MaxClickTime,
                                                 int(settings.Flags),
                                                 settings.DeltaPosition,
                                                 settings.uDeltaPosition)
        _check_result(lib.set_control_settings(self._device_id, byref(control_settings)))

    def set_control_settings_calb(self, settings: control_settings_calb_t) -> None:
        """Set calibrated motor control settings.

        In case of CTL_MODE=1, the joystick motor control is enabled. In this mode, while the joystick is maximally
        displaced, the engine tends to move at MaxSpeed[i]. i=0 if another value hasn't been set at the previous usage.
        To change the speed index "i", use the buttons.

        In case of CTL_MODE=2, the motor is controlled by the left/right buttons. When you click on the button, the
        motor starts moving in the appropriate direction at a speed MaxSpeed[0]. After Timeout[i], motor moves at speed
        MaxSpeed[i+1]. At the transition between MaxSpeed[i] and MaxSpeed[i+1] the motor just accelerates/decelerates
        as usual.

        :param settings: structure contains user unit motor control settings.
        :type settings: control_settings_calb_t
        """
        self._check_device_opened()
        if not isinstance(settings, control_settings_calb_t):
            raise TypeError("settings must be of type control_settings_calb_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        control_settings = ll.control_settings_calb_t((c_float * 10)(*settings.MaxSpeed),
                                                      (c_uint * 9)(*settings.Timeout),
                                                      settings.MaxClickTime,
                                                      int(settings.Flags),
                                                      settings.DeltaPosition)
        _check_result(lib.set_control_settings_calb(self._device_id, byref(control_settings), byref(self._calib)))

    def get_control_settings(self) -> control_settings_t:
        """Read motor control settings.

        In case of CTL_MODE=1, joystick motor control is enabled. In this mode, while the joystick is maximally
        displaced, the engine tends to move at MaxSpeed[i]. i=0 if another value hasn't been set at the previous usage.
        To change the speed index "i", use the buttons.

        In case of CTL_MODE=2, the motor is controlled by the left/right buttons. When you click on the button, the
        motor starts moving in the appropriate direction at a speed MaxSpeed[0]. After Timeout[i], motor moves at speed
        MaxSpeed[i+1]. At the transition between MaxSpeed[i] and MaxSpeed[i+1] the motor just accelerates/decelerates
        as usual.

        :return: structure contains motor control settings.
        :rtype: control_settings_t
        """
        self._check_device_opened()
        control_settings = ll.control_settings_t()
        _check_result(lib.get_control_settings(self._device_id, byref(control_settings)))
        return control_settings_t(list(control_settings.MaxSpeed),
                                  list(control_settings.uMaxSpeed),
                                  list(control_settings.Timeout),
                                  control_settings.MaxClickTime,
                                  control_settings.Flags,
                                  control_settings.DeltaPosition,
                                  control_settings.uDeltaPosition)

    def get_control_settings_calb(self) -> control_settings_calb_t:
        """Read calibrated motor control settings.

        In case of CTL_MODE=1, the joystick motor control is enabled. In this mode, while the joystick is maximally
        displaced, the engine tends to move at MaxSpeed[i]. i=0 if another value hasn't been set at the previous usage.
        To change the speed index "i", use the buttons.

        In case of CTL_MODE=2, the motor is controlled by the left/right buttons. When you click on the button, the
        motor starts moving in the appropriate direction at a speed MaxSpeed[0]. After Timeout[i], motor moves at speed
        MaxSpeed[i+1]. At the transition between MaxSpeed[i] and MaxSpeed[i+1] the motor just accelerates/decelerates
        as usual.

        :return: structure contains user unit motor control settings.
        :rtype: control_settings_calb_t
        """
        self._check_device_opened()
        control_settings = ll.control_settings_calb_t()
        _check_result(lib.get_control_settings_calb(self._device_id, byref(control_settings), byref(self._calib)))
        return control_settings_calb_t(list(control_settings.MaxSpeed),
                                       list(control_settings.Timeout),
                                       control_settings.MaxClickTime,
                                       control_settings.Flags,
                                       control_settings.DeltaPosition)

    def set_joystick_settings(self, settings: joystick_settings_t) -> None:
        """Set joystick settings.

        If joystick position falls outside DeadZone limits, a movement begins. The speed is defined by the joystick's
        position in the range of the DeadZone limit to the maximum deviation. Joystick positions inside DeadZone limits
        correspond to zero speed (a soft stop of motion), and positions beyond Low and High limits correspond to
        MaxSpeed[i] or -MaxSpeed[i] (see command SCTL), where i = 0 by default and can be changed with the left/right
        buttons (see command SCTL). If the next speed in the list is zero (both integer and microstep parts), the
        button press is ignored. The first speed in the list shouldn't be zero. See the Joystick control section on
        https://doc.xisupport.com for more information.

        :param settings: structure contains joystick settings
        :type settings: joystick_settings_t
        """
        self._check_device_opened()
        if not isinstance(settings, joystick_settings_t):
            raise TypeError("settings must be of type joystick_settings_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        joystick_settings = ll.joystick_settings_t(settings.JoyLowEnd,
                                                   settings.JoyCenter,
                                                   settings.JoyHighEnd,
                                                   settings.ExpFactor,
                                                   settings.DeadZone,
                                                   int(settings.JoyFlags))
        _check_result(lib.set_joystick_settings(self._device_id, byref(joystick_settings)))

    def get_joystick_settings(self) -> joystick_settings_t:
        """Read joystick settings.

        If joystick position falls outside DeadZone limits, a movement begins. The speed is defined by the joystick's
        position in the range of the DeadZone limit to the maximum deviation. Joystick positions inside DeadZone limits
        correspond to zero speed (a soft stop of the motion), and positions beyond Low and High limits correspond to
        MaxSpeed[i] or -MaxSpeed[i] (see command SCTL), where i = 0 by default and can be changed with the left/right
        buttons (see command SCTL). If the next speed in the list is zero (both integer and microstep parts), the
        button press is ignored. The first speed in the list shouldn't be zero. See the Joystick control section on
        https://doc.xisupport.com for more information.

        :return: structure contains joystick settings
        :rtype: joystick_settings_t
        """
        self._check_device_opened()
        joystick_settings = ll.joystick_settings_t()
        _check_result(lib.get_joystick_settings(self._device_id, byref(joystick_settings)))
        return joystick_settings_t(joystick_settings.JoyLowEnd,
                                   joystick_settings.JoyCenter,
                                   joystick_settings.JoyHighEnd,
                                   joystick_settings.ExpFactor,
                                   joystick_settings.DeadZone,
                                   joystick_settings.JoyFlags)

    def set_ctp_settings(self, settings: ctp_settings_t) -> None:
        """Set control position settings (used with stepper motor only).

        When controlling the step motor with the encoder (CTP_BASE=0), it is possible to detect the loss of steps. The
        controller knows the number of steps per revolution (GENG::StepsPerRev) and the encoder resolution (GFBS::IPT).
        When the control is enabled (CTP_ENABLED is set), the controller stores the current position in the steps of SM
        and the current position of the encoder. Next, the encoder position is converted into steps at each step, and
        if the difference between the current position in steps and the encoder position is greater than CTPMinError,
        the flag STATE_CTP_ERROR is set.

        Alternatively, the stepper motor may be controlled with the speed sensor (CTP_BASE 1). In this mode, at the
        active edges of the input clock, the controller stores the current value of steps. Then, at each revolution,
        the controller checks how many steps have been passed. When the difference is over the CTPMinError, the
        STATE_CTP_ERROR flag is set.

        :param settings: structure contains position control settings.
        :type settings: ctp_settings_t
        """
        self._check_device_opened()
        if not isinstance(settings, ctp_settings_t):
            raise TypeError("settings must be of type ctp_settings_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        ctp_settings = ll.ctp_settings_t(settings.CTPMinError, int(settings.CTPFlags))
        _check_result(lib.set_ctp_settings(self._device_id, byref(ctp_settings)))

    def get_ctp_settings(self) -> ctp_settings_t:
        """Read control position settings (used with stepper motor only).

        When controlling the step motor with an encoder (CTP_BASE=0), it is possible to detect the loss of steps. The
        controller knows the number of steps per revolution (GENG::StepsPerRev) and the encoder resolution (GFBS::IPT).
        When the control is enabled (CTP_ENABLED is set), the controller stores the current position in the steps of SM
        and the current position of the encoder. Next, the encoder position is converted into steps at each step, and
        if the difference between the current position in steps and the encoder position is greater than CTPMinError,
        the flag STATE_CTP_ERROR is set.

        Alternatively, the stepper motor may be controlled with the speed sensor (CTP_BASE 1). In this mode, at the
        active edges of the input clock, the controller stores the current value of steps. Then, at each revolution,
        the controller checks how many steps have been passed. When the difference is over the CTPMinError, the
        STATE_CTP_ERROR flag is set.

        :return: structure contains position control settings.
        :rtype: ctp_settings_t
        """
        self._check_device_opened()
        ctp_settings = ll.ctp_settings_t()
        _check_result(lib.get_ctp_settings(self._device_id, byref(ctp_settings)))
        return ctp_settings_t(ctp_settings.CTPMinError, ctp_settings.CTPFlags)

    def set_uart_settings(self, settings: uart_settings_t) -> None:
        """Set UART settings.

        This function sends the structure with UART settings to the controller's memory.

        :param settings: UART settings
        :type settings: uart_settings_t
        """
        self._check_device_opened()
        if not isinstance(settings, uart_settings_t):
            raise TypeError("settings must be of type uart_settings_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        uart_settings = ll.uart_settings_t(settings.Speed, int(settings.UARTSetupFlags))
        _check_result(lib.set_uart_settings(self._device_id, byref(uart_settings)))

    def get_uart_settings(self) -> uart_settings_t:
        """Read UART settings.

        This function reads the structure containing UART settings.

        :return: UART settings
        :rtype: uart_settings_t
        """
        self._check_device_opened()
        uart_settings = ll.uart_settings_t()
        _check_result(lib.get_uart_settings(self._device_id, byref(uart_settings)))
        return uart_settings_t(uart_settings.Speed, uart_settings.UARTSetupFlags)

    def set_emf_settings(self, settings: emf_settings_t) -> None:
        """Set electromechanical coefficients.

        The settings are different for different stepper motors. Please set new settings when you change the motor.

        :param settings: EMF settings
        :type settings: emf_settings_t
        """
        self._check_device_opened()
        if not isinstance(settings, emf_settings_t):
            raise TypeError("settings must be of type emf_settings_t. {} was got.".format(type(settings)))
        _check_fullness(settings)
        emf_settings = ll.emf_settings_t(settings.L, settings.R, settings.Km, int(settings.BackEMFFlags))
        _check_result(lib.set_emf_settings(self._device_id, byref(emf_settings)))

    def get_emf_settings(self) -> emf_settings_t:
        """Read electromechanical settings.

        The settings are different for different stepper motors.

        :return: EMF settings
        :rtype: emf_settings_t
        """
        self._check_device_opened()
        emf_settings = ll.emf_settings_t()
        _check_result(lib.get_emf_settings(self._device_id, byref(emf_settings)))
        return emf_settings_t(emf_settings.L, emf_settings.R, emf_settings.Km, emf_settings.BackEMFFlags)

    def set_controller_name(self, name: controller_name_t) -> None:
        """Write user's controller name and internal settings to the FRAM.

        :param name: structure contains the previously set user's controller name
        :type name: controller_name_t
        """
        self._check_device_opened()
        if not isinstance(name, controller_name_t):
            raise TypeError("name must be of type controller_name_t. {} was got.".format(type(name)))
        _check_fullness(name)
        controller_name = ll.controller_name_t(name.ControllerName.encode(), int(name.CtrlFlags))
        _check_result(lib.set_controller_name(self._device_id, byref(controller_name)))

    def get_controller_name(self) -> controller_name_t:
        """Read user's controller name and internal settings from the FRAM.

        :return: controller name
        :rtype: controller_name_t
        """
        self._check_device_opened()
        controller_name = ll.controller_name_t()
        _check_result(lib.get_controller_name(self._device_id, byref(controller_name)))
        return controller_name_t(controller_name.ControllerName.decode(), controller_name.CtrlFlags)

    def set_nonvolatile_memory(self, memory: nonvolatile_memory_t) -> None:
        """Write user data into the FRAM.

        :param memory: user data.
        :type memory: nonvolatile_memory_t
        """
        self._check_device_opened()
        if not isinstance(memory, nonvolatile_memory_t):
            raise TypeError("memory must be of type nonvolatile_memory_t. {} was got.".format(type(memory)))
        _check_fullness(memory)
        nonvolatile_memory = ll.nonvolatile_memory_t((c_uint * 7)(*memory.UserData))
        _check_result(lib.set_nonvolatile_memory(self._device_id, byref(nonvolatile_memory)))

    def get_nonvolatile_memory(self) -> nonvolatile_memory_t:
        """Read userdata from the FRAM.

        :return: structure contains previously set user data.
        :rtype: nonvolatile_memory_t
        """
        self._check_device_opened()
        nonvolatile_memory = ll.nonvolatile_memory_t()
        _check_result(lib.get_nonvolatile_memory(self._device_id, byref(nonvolatile_memory)))
        return nonvolatile_memory_t(list(nonvolatile_memory.UserData))

    # Legacy
    def set_engine_advansed_setup(self, setup: engine_advansed_setup_t) -> None:
        """Set engine advanced settings.

        :param setup: EAS settings
        :type setup: engine_advansed_setup_t
        """
        self._check_device_opened()
        if not isinstance(setup, engine_advansed_setup_t):
            raise TypeError("setup must be of type engine_advansed_setup_t. {} was got.".format(type(setup)))
        _check_fullness(setup)
        engine_advanced_setup = ll.engine_advansed_setup_t(
                                        setup.stepcloseloop_Kw,
                                        setup.stepcloseloop_Kp_low,
                                        setup.stepcloseloop_Kp_high)
        _check_result(lib.set_engine_advansed_setup(self._device_id, byref(engine_advanced_setup)))

    def set_engine_advanced_setup(self, setup: engine_advanced_setup_t) -> None:
        """Set engine advanced settings.

        :param setup: EAS settings
        :type setup: engine_advanced_setup_t
        """
        self._check_device_opened()
        if not isinstance(setup, engine_advanced_setup_t):
            raise TypeError("setup must be of type engine_advanced_setup_t. {} was got.".format(type(setup)))
        _check_fullness(setup)
        engine_advanced_setup = ll.engine_advansed_setup_t(
                                        setup.stepcloseloop_Kw,
                                        setup.stepcloseloop_Kp_low,
                                        setup.stepcloseloop_Kp_high)
        _check_result(lib.set_engine_advansed_setup(self._device_id, byref(engine_advanced_setup)))

    # Legacy
    def get_engine_advansed_setup(self) -> engine_advansed_setup_t:
        """Read engine advanced settings.

        :return: EAS settings
        :rtype: engine_advansed_setup_t
        """
        self._check_device_opened()
        engine_advanced_setup = ll.engine_advansed_setup_t()
        _check_result(lib.get_engine_advansed_setup(self._device_id, byref(engine_advanced_setup)))
        return engine_advansed_setup_t(engine_advanced_setup.stepcloseloop_Kw,
                                       engine_advanced_setup.stepcloseloop_Kp_low,
                                       engine_advanced_setup.stepcloseloop_Kp_high)

    def get_engine_advanced_setup(self) -> engine_advanced_setup_t:
        """Read engine advanced settings.

        :return: EAS settings
        :rtype: engine_advanced_setup_t
        """
        self._check_device_opened()
        engine_advanced_setup = ll.engine_advansed_setup_t()
        _check_result(lib.get_engine_advansed_setup(self._device_id, byref(engine_advanced_setup)))
        return engine_advanced_setup_t(engine_advanced_setup.stepcloseloop_Kw,
                                       engine_advanced_setup.stepcloseloop_Kp_low,
                                       engine_advanced_setup.stepcloseloop_Kp_high)

    def command_move_calb(self, position: float) -> None:
        """Move to position using user units.

        Upon receiving the command "move" the engine starts to move with preset parameters (speed, acceleration,
        retention), to the point specified by Position.

        :param position: position to move.
        :type position: float
        """
        self._check_device_opened()
        try:
            c_float(position)
        except Exception:
            raise TypeError("position must be of type float. {} was got.".format(type(position)))
        _check_result(lib.command_move_calb(self._device_id, c_float(position), byref(self._calib)))

    def command_movr(self, delta_position: int, udelta_position: int) -> None:
        """Shift by a set offset.

        Upon receiving the command "movr", the engine starts to move with preset parameters (speed, acceleration, hold)
        left or right (depending on the sign of DeltaPosition). It moves by the number of steps specified in the fields
        DeltaPosition and uDeltaPosition. uDeltaPosition sets the microstep offset for a stepper motor. In the case of
        a DC motor, this field is ignored.

        :param delta_position: shift from initial position.
        :type delta_position: int
        :param udelta_position: the fractional part of the offset shift, in microsteps. The microstep size and the
            range of valid values for this field depend on the selected step division mode (see the MicrostepMode field
            in engine_settings).
        :type udelta_position: int
        """
        self._check_device_opened()
        try:
            c_int(delta_position)
        except Exception:
            raise TypeError("delta_position must be of integer type. {} was got.".format(type(delta_position)))
        try:
            c_int(udelta_position)
        except Exception:
            raise TypeError("udelta_position must be of integer type. {} was got.".format(type(udelta_position)))
        _check_result(lib.command_movr(self._device_id, delta_position, udelta_position))

    def command_movr_calb(self, delta_position: float) -> None:
        """Shift by a set offset using user units.

        Upon receiving the command "movr", the engine starts to move with preset parameters (speed, acceleration, hold)
        left or right (depending on the sign of DeltaPosition). It moves by the distance specified in the field
        DeltaPosition.

        :param delta_position: shift from initial position.
        :type delta_position: float
        """
        self._check_device_opened()
        try:
            c_float(delta_position)
        except Exception:
            raise TypeError("delta_position must be of floating point type. {} was got.".format(type(delta_position)))
        _check_result(lib.command_movr_calb(self._device_id, c_float(delta_position), byref(self._calib)))

    def command_home(self) -> None:
        """Moving to home position.

        Moving algorithm:

        1) Moves the motor according to the speed FastHome, uFastHome and flag HOME_DIR_FAST until the limit switch if
        the HOME_STOP_ENDS flag is set. Or moves the motor until the input synchronization signal occurs if the flag
        HOME_STOP_SYNC is set. Or moves until the revolution sensor signal occurs if the flag HOME_STOP_REV_SN is set.

        2) Then moves according to the speed SlowHome, uSlowHome and flag HOME_DIR_SLOW until the input clock signal
        occurs if the flag HOME_MV_SEC is set. If the flag HOME_MV_SEC is reset, skip this step.

        3) Then shifts the motor according to the speed FastHome, uFastHome and the flag HOME_DIR_SLOW by HomeDelta
        distance, uHomeDelta.

        See GHOM/SHOM commands' description for details on home flags.

        Moving settings can be set by set_home_settings/set_home_settings_calb.
        """
        self._check_device_opened()
        _check_result(lib.command_home(self._device_id))

    def command_left(self) -> None:
        """Start continuous moving to the left."""
        self._check_device_opened()
        _check_result(lib.command_left(self._device_id))

    def command_right(self) -> None:
        """Start continuous moving to the right."""
        self._check_device_opened()
        _check_result(lib.command_right(self._device_id))

    def command_loft(self) -> None:
        """Upon receiving the command "loft", the engine is shifted from the current position to a distance
        Antiplay defined in engine settings. Then moves to the initial position.
        """
        self._check_device_opened()
        _check_result(lib.command_loft(self._device_id))

    def command_sstp(self) -> None:
        """Soft stop the engine. The motor is slowing down with the deceleration specified in move_settings."""
        self._check_device_opened()
        _check_result(lib.command_sstp(self._device_id))

    def get_position_calb(self) -> get_position_calb_t:
        """Reads position value in user units for stepper motor and encoder steps for all engines.

        :return: structure contains motor position.
        :rtype: get_position_calb_t
        """
        self._check_device_opened()
        position = ll.get_position_calb_t()
        _check_result(lib.get_position_calb(self._device_id, byref(position), byref(self._calib)))
        return get_position_calb_t(position.Position, position.EncPosition)

    def set_position(self, position: set_position_t) -> None:
        """Sets position in steps and microsteps for stepper motor. Sets encoder position for all engines.

        :param position: structure contains motor position.
        :type position: set_position_t
        """
        self._check_device_opened()
        if not isinstance(position, set_position_t):
            raise TypeError("position must be of type set_position_t. {} was got.".format(type(position)))
        _check_fullness(position)
        _position = ll.set_position_t(position.Position,
                                      position.uPosition,
                                      position.EncPosition,
                                      int(position.PosFlags))
        _check_result(lib.set_position(self._device_id, byref(_position)))

    def set_position_calb(self, position: set_position_calb_t) -> None:
        """Sets any position value and encoder value of all engines. In user units.

        :param position: structure contains motor position.
        :type position: set_position_calb_t
        """
        self._check_device_opened()
        if not isinstance(position, set_position_calb_t):
            raise TypeError("position must be of type set_position_calb_t. {} was got.".format(type(position)))
        _check_fullness(position)
        _position = ll.set_position_calb_t(position.Position, position.EncPosition, int(position.PosFlags))
        _check_result(lib.set_position_calb(self._device_id, byref(_position), byref(self._calib)))

    def command_zero(self) -> None:
        """Sets the current position to 0. Sets the target position of the move command and the movr command to zero
        for all cases except for movement to the target position. In the latter case, the target position is calculated
        so that the absolute position of the destination stays the same. For example, if we were at 400 and moved to
        500, then the command Zero makes the current position 0 and the position of the destination 100. It does not
        change the mode of movement. If the motion is carried, it continues, and if the engine is in the "hold", the
        type of retention remains.
        """
        self._check_device_opened()
        _check_result(lib.command_zero(self._device_id))

    def command_save_settings(self) -> None:
        """Save all settings from the controller's RAM to the controller's flash memory, replacing previous data in the
        flash memory.
        """
        self._check_device_opened()
        _check_result(lib.command_save_settings(self._device_id))

    def command_read_settings(self) -> None:
        """Read all settings from the controller's flash memory to the controller's RAM, replacing previous data in the
        RAM.
        """
        self._check_device_opened()
        _check_result(lib.command_read_settings(self._device_id))

    def command_start_measurements(self) -> None:
        """Start measurements and buffering of speed and the speed error (target speed minus real speed)."""
        self._check_device_opened()
        _check_result(lib.command_start_measurements(self._device_id))

    def get_measurements(self) -> measurements_t:
        """A command to read the data buffer to build a speed graph and a position error (desired position minus real
        position).

        Filling the buffer starts with the command "start_measurements". The buffer holds 25 points; the points are
        taken with a period of 1 ms. To create a robust system, read data every 20 ms. If the buffer is full, it is
        recommended to repeat the readings every 5 ms until the buffer again becomes filled with 20 points.

        To stop measurements just stop reading data. After buffer overflow measurements will stop automatically.

        :return: structure with buffer and its length.
        :rtype: measurements_t
        """
        self._check_device_opened()
        measurements = ll.measurements_t()
        _check_result(lib.get_measurements(self._device_id, byref(measurements)))
        return measurements_t(list(measurements.Speed), list(measurements.Error), measurements.Length)

    def get_chart_data(self) -> chart_data_t:
        """Return device electrical parameters, useful for charts.

        A useful function that fills the structure with a snapshot of the controller voltages and currents.

        :return: structure with a snapshot of controller parameters.
        :rtype: chart_data_t
        """
        self._check_device_opened()
        chart_data = ll.chart_data_t()
        _check_result(lib.get_chart_data(self._device_id, byref(chart_data)))
        return chart_data_t(chart_data.WindingVoltageA,
                            chart_data.WindingVoltageB,
                            chart_data.WindingVoltageC,
                            chart_data.WindingCurrentA,
                            chart_data.WindingCurrentB,
                            chart_data.WindingCurrentC,
                            chart_data.Pot,
                            chart_data.Joy,
                            chart_data.DutyCycle)

    def get_serial_number(self) -> int:
        """Read device serial number.

        :return: serial number
        :rtype: int
        """
        self._check_device_opened()
        serial_number = c_uint()
        _check_result(lib.get_serial_number(self._device_id, byref(serial_number)))
        return serial_number.value

    def get_firmware_version(self) -> 'tuple[int]':
        """Read the controller's firmware version.

        :return: tuple of major, minor and release versions
        :rtype: tuple[int]
        """
        self._check_device_opened()
        minor_version = c_uint32()
        major_version = c_uint32()
        release_version = c_uint32()
        _check_result(lib.get_firmware_version(self._device_id,
                                               byref(minor_version),
                                               byref(major_version),
                                               byref(release_version)))
        return (minor_version.value, major_version.value, release_version.value)

    def set_stage_name(self, name: stage_name_t) -> None:
        """Write the user's stage name to the EEPROM.

        :param name: structure contains the previously set user's stage name
        :type name: stage_name_t
        """
        self._check_device_opened()
        if not isinstance(name, stage_name_t):
            raise TypeError("name must be of type stage_name_t. {} was got.".format(type(name)))
        _check_fullness(name)
        stage_name = ll.stage_name_t(name.PositionerName.encode())
        _check_result(lib.set_stage_name(self._device_id, byref(stage_name)))

    def get_stage_name(self) -> stage_name_t:
        """Read the user's stage name from the EEPROM.

        :return: structure contains the previously set user's stage name
        :rtype: stage_name_t
        """
        self._check_device_opened()
        stage_name = ll.stage_name_t()
        _check_result(lib.get_stage_name(self._device_id, byref(stage_name)))
        return stage_name_t(stage_name.PositionerName.decode())

    def get_bootloader_version(self) -> 'tuple[int]':
        """Read the controller's bootloader version.

        :return: tuple of major, minor and release versions
        :rtype: tuple[int]
        """
        self._check_device_opened()
        minor_version = c_uint32()
        major_version = c_uint32()
        release_version = c_uint32()
        _check_result(lib.get_bootloader_version(self._device_id,
                                                 byref(minor_version),
                                                 byref(major_version),
                                                 byref(release_version)))
        return (minor_version.value, major_version.value, release_version.value)

    def set_correction_table(self, namefile: str) -> None:
        """Command of loading a correction table from a text file.

        The correction table is used for position correction in case of mechanical inaccuracies. It works for some
        parameters in _calb commands.

        :param namefile: the file name must be either a full path or a relative path. If the file name is set to None,
            the correction table will be cleared. File format: two tab-separated columns. Column headers are strings.
            Data is real, the dot is a delimiter. The first column is a coordinate. The second one is the deviation
            caused by a mechanical error. The maximum length of a table is 100 rows. Coordinate column must be sorted
            in ascending order.
        :type namefile: str
        """
        self._check_device_opened()
        if not isinstance(namefile, str) and namefile is not None:
            raise TypeError("namefile must be of type str. {} was got.".format(type(namefile)))
        _check_result(lib.set_correction_table(self._device_id, namefile.encode() if namefile is not None else None))

    def get_status(self) -> status_t:
        """Return device state.

        A useful function that fills the structure with a snapshot of the controller state, including speed, position,
        and boolean flags.

        :return: structure with a snapshot of the controller state
        :rtype: status_t
        """
        self._check_device_opened()
        status = ll.status_t()
        _check_result(lib.get_status(self._device_id, byref(status)))
        return status_t(status.MoveSts,
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

    def get_device_information(self) -> device_information_t:
        """Return device information. It's available in the firmware and the bootloader.

        :return: device information Device information.
        :rtype: device_information_t
        """
        self._check_device_opened()
        device_information = ll.device_information_t()
        _check_result(lib.get_device_information(self._device_id, byref(device_information)))
        return device_information_t(device_information.Manufacturer.decode(),
                                    device_information.ManufacturerId.decode(),
                                    device_information.ProductDescription.decode(),
                                    device_information.Major,
                                    device_information.Minor,
                                    device_information.Release)

    def get_status_calb(self) -> status_calb_t:
        """Return the device's user unit state.

        :return: structure with snapshot of controller status
        :rtype: status_calb_t
        """
        self._check_device_opened()
        status = ll.status_calb_t()
        _check_result(lib.get_status_calb(self._device_id, byref(status), byref(self._calib)))
        return status_calb_t(status.MoveSts,
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

    def command_wait_for_stop(self, refresh_interval_ms: int) -> None:
        """Wait for stop.

        :param refresh_interval_ms: status refresh interval. The function waits this number of milliseconds between
            get_status requests to the controller. Recommended value of this parameter is 10 ms. Use values of less
            than 3 ms only when necessary - small refresh interval values do not significantly increase response time
            of the function, but they create substantially more traffic in controller-computer data channel.
        :type refresh_interval_ms: int
        """
        self._check_device_opened()
        try:
            c_int(refresh_interval_ms)
        except Exception:
            raise TypeError("refresh_interval_ms must be of integer type. {} was got."
                            .format(type(refresh_interval_ms)))
        _check_result(lib.command_wait_for_stop(self._device_id, c_uint32(refresh_interval_ms)))

    def command_homezero(self) -> None:
        """Make home command, wait until it is finished and make zero command.

        This is a convenient way to calibrate zero position.
        """
        self._check_device_opened()
        _check_result(lib.command_homezero(self._device_id))

    def set_bindy_key(self, keyfilepath: str) -> None:
        """Set network encryption layer (bindy) key.

        :param keyfilepath: full path to the bindy keyfile When using network-attached devices this function must be
            called before enumerate_devices and open_device functions.
        :type keyfilepath: str
        """
        self._check_device_opened()
        if not isinstance(keyfilepath, str):
            raise TypeError("keyfilepath must be of type str. {} was got.".format(type(keyfilepath)))
        _check_result(lib.set_bindy_key(keyfilepath.encode()))

    def open_device(self) -> None:
        """Open a device"""
        device_id = lib.open_device(self.uri.encode())
        if (device_id < 0):
            raise ConnectionError(
                "Cannot connect to device via URI='{}'\n"
                "\t* check URI. For URI format see documentation for open_device() on "
                "https://libximc.xisupport.com/doc-en/\n"
                "\t* check whether it's connected to computer physically, powered and not occupied by another app\n"
                .format(self.uri)
            )
        self._device_id: int = device_id
        self._is_opened: bool = True

    def close_device(self) -> None:
        """Close device"""
        if not self._is_opened:
            return
        _check_result(lib.close_device(byref(cast(self._device_id, POINTER(c_int)))))
        self._is_opened = False

    def get_position(self) -> get_position_t:
        """Reads position value in user units for stepper motor and encoder steps for all engines.

        :return: structure contains motor position.
        :rtype: get_position_t
        """
        self._check_device_opened()
        position = ll.get_position_t()
        _check_result(lib.get_position(self._device_id, byref(position)))
        return get_position_t(position.Position, position.uPosition, position.EncPosition)

    def command_move(self, position: int, uposition: int) -> None:
        """Move to position.

        Upon receiving the command "move" the engine starts to move with pre-set parameters (speed, acceleration,
        retention), to the point specified by  Position and uPosition. uPosition sets the microstep position of a
        stepper motor. In the case of DC motor, this field is ignored.

        :param position: position to move.
        :type position: int
        :param uposition: the fractional part of the position to move, in microsteps. The microstep size and the range
            of valid values for this field depend on the selected step division mode (see the MicrostepMode field in
            engine_settings).
        :type uposition: int
        """
        self._check_device_opened()
        try:
            c_int(position)
        except Exception:
            raise TypeError("position must be of integer type. {} was got.".format(type(position)))
        try:
            c_int(uposition)
        except Exception:
            raise TypeError("uposition must be of integer type. {} was got.".format(type(uposition)))
        _check_result(lib.command_move(self._device_id, position, uposition))

    def command_stop(self) -> None:
        """Immediately stops the engine, moves it to the STOP state, and sets switches to BREAK mode (windings are
        short-circuited). The holding regime is deactivated for DC motors, keeping current in the windings for stepper
        motors (to control it, see Power management settings).

        When this command is called, the ALARM flag is reset.
        """
        self._check_device_opened()
        _check_result(lib.command_stop(self._device_id))

    def command_power_off(self) -> None:
        """Immediately power off motor regardless its state.

        Shouldn't be used during motion as the motor could be powered on again automatically to continue movement. The
        command is designed to manually power off the motor. When automatic power off after stop is required, use the
        power management system.
        """
        self._check_device_opened()
        _check_result(lib.command_power_off(self._device_id))

    def __del__(self):
        if self._is_opened:
            self.close_device()


# ================= #
# General functions #
# ================= #
def enumerate_devices(enumerate_flags: flag_enumerations.EnumerateFlags, hints: str = "") -> 'list[dict]':
    """Enumerate all devices that looks like valid.

    :param enumerate_flags: enumeration flags.
    :type enumerate_flags: EnumerateFlags
    :param hints: a string of form "key=value \\n key2=value2". Unrecognized key-value pairs are ignored.
        Key list: addr - used together with ENUMERATE_NETWORK flag. Non-null value is a remote host name or a
        comma-separated list of host names which contain the devices to be found, absent value means broadcast
        discovery. adapter_addr - used together with ENUMERATE_NETWORK flag. Non-null value is a IP address of
        network adapter. Remote ximc device must be on the same local network as the adapter. When using the
        adapter_addr key, you must set the addr key. Example: "addr= \\n adapter_addr=192.168.0.100".
    :type hints: str
    :return: list of enumeration dictionaries.
    :rtype: list[dict]
    """
    if not isinstance(enumerate_flags, flag_enumerations.EnumerateFlags):
        raise TypeError("enumerate_flags must be a bitwise combination of EnumerateFlags flags. Thus the expected type"
                        " is {}. But {} was got."
                        .format(type(flag_enumerations.EnumerateFlags.ENUMERATE_ALL_COM), type(enumerate_flags)))
    if not isinstance(hints, str):
        raise TypeError("hints must be of type str. {} was got.".format(type(hints)))
    # Device enumeration is allocated at C level. So at the end it should be freed
    device_enumeration = lib.enumerate_devices(enumerate_flags.value, hints.encode())
    device_count = lib.get_device_count(device_enumeration)

    enumeration_list = []
    for device_index in range(device_count):
        device_name = lib.get_device_name(device_enumeration, device_index)

        if enumerate_flags & flag_enumerations.EnumerateFlags.ENUMERATE_PROBE:
            device_serial = c_uint32(0)
            _check_result(lib.get_enumerate_device_serial(device_enumeration,
                                                          device_index,
                                                          byref(device_serial)))

            device_information = ll.device_information_t()
            _check_result(lib.get_enumerate_device_information(device_enumeration,
                                                               device_index,
                                                               byref(device_information)))

            controller_name = ll.controller_name_t()
            _check_result(lib.get_enumerate_device_controller_name(device_enumeration,
                                                                   device_index,
                                                                   byref(controller_name)))

            stage_name = ll.stage_name_t()
            _check_result(lib.get_enumerate_device_stage_name(device_enumeration,
                                                              device_index,
                                                              byref(stage_name)))

        if enumerate_flags & flag_enumerations.EnumerateFlags.ENUMERATE_PROBE:
            device_dict = {'uri': device_name.decode(),
                           'device_serial': device_serial.value,

                           'Manufacturer': device_information.Manufacturer.decode(),
                           'ManufacturerId': device_information.ManufacturerId.decode(),
                           'ProductDescription': device_information.ProductDescription.decode(),
                           'Major': device_information.Major,
                           'Minor': device_information.Minor,
                           'Release': device_information.Release,

                           'ControllerName': controller_name.ControllerName.decode(),
                           'CtrlFlags': controller_name.CtrlFlags,

                           'PositionerName': stage_name.PositionerName.decode()
                           }
        else:
            device_dict = {'uri': device_name.decode(),
                           'device_serial': None,

                           'Manufacturer': None,
                           'ManufacturerId': None,
                           'ProductDescription': None,
                           'Major': None,
                           'Minor': None,
                           'Release': None,

                           'ControllerName': None,
                           'CtrlFlags': None,

                           'PositionerName': None
                           }
        enumeration_list.append(device_dict)

    # Free allocated memory
    _check_result(lib.free_enumerate_devices(device_enumeration))
    return enumeration_list


def probe_device(uri: str) -> flag_enumerations.Result:
    """Check if a device with OS uri uri is XIMC device.

    Be carefully with this call because it sends some data to the device.

    :param uri: a device uri
    :type uri: str
    :return: result of any operation
    :rtype: Result
    """
    if not isinstance(uri, str):
        raise TypeError("uri must be of type str. {} was got.".format(type(uri)))
    return flag_enumerations.Result(lib.probe_device(uri.encode()))


def reset_locks() -> None:
    """Resets the error of incorrect data transmission."""
    lib.reset_locks()


def ximc_version() -> str:
    """Returns a library version.

    :return: a buffer to hold a version string, 32 bytes is enough
    :rtype: str
    """
    res_str = "b\0" * 32
    c_res_str = c_char_p(res_str.encode())
    lib.ximc_version(c_res_str)
    return c_res_str.value.decode()
