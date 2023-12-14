""" Python binding for libximc
=======================================================================================================================

file: structure_types.py

Description: This file contains definitions of structure types that are to be used as parameters and return values of
highlevel's functions and Axis's methods. Also the file includes inner routines for type and range checking.
"""
from ctypes import (c_float,
                    c_uint, c_uint8, c_uint16, c_uint32,
                    c_int, c_int16, c_int32, c_longlong,
                    c_char, c_char_p,
                    sizeof)
from libximc.highlevel import _flag_enumerations as flag_enumerations


# ================================================ #
#                     Routines                     #
# ================================================ #
NOT_INITIALIZED = "Not Initialized"

# Define type ranges
_UINT8_MIN = 0
_UINT8_MAX = 2**(8 * sizeof(c_uint8)) - 1

_UINT16_MIN = 0
_UINT16_MAX = 2**(8 * sizeof(c_uint16)) - 1

_UINT_MIN = 0
_UINT_MAX = 2**(8 * sizeof(c_uint)) - 1

_INT16_MIN = -2**(8 * sizeof(c_int16) - 1)
_INT16_MAX = 2**(8 * sizeof(c_int16) - 1) - 1

_INT_MIN = -2**(8 * sizeof(c_int) - 1)
_INT_MAX = 2**(8 * sizeof(c_int) - 1) - 1

_LONGLONG_MIN = -2**(8 * sizeof(c_longlong) - 1)
_LONGLONG_MAX = 2**(8 * sizeof(c_longlong) - 1) - 1

_FLOAT_ABS_MIN = 0
_FLOAT_ABS_MAX = 3.4E+38


def _check_integer_iteratively(container, container_name: str) -> None:
    for item_idx, item in enumerate(container):
        if not isinstance(item, int):
            raise TypeError("{}[{}] must be of type int. {} was got.".format(container_name, item_idx, type(item)))


def _check_float_iteratively(container, container_name: str) -> None:
    for item_idx, item in enumerate(container):
        if not isinstance(item, float):
            raise TypeError("{}[{}] must be of type float. {} was got.".format(container_name, item_idx, type(item)))


def _check_limits(val, _min, _max, varname: str) -> None:
    if val < _min or val > _max:
        raise TypeError("{} must be in range [{}; {}].".format(varname, _min, _max))


def _check_limits_iteratively(container, _min, _max, container_name):
    for item_idx, item in enumerate(container):
        _check_limits(item, _min, _max, "{}[{}]".format(container_name, item_idx))


def _check_len(container, _len: int, strictly_equal: bool, container_name: str) -> None:
    try:
        len(container)
    except Exception:
        raise TypeError("len() cannot be applied to {}. Check documentation and ensure {}'s type is correct. "
                        "type({})={} was got."
                        .format(container_name, container_name, container_name, type(container_name)))
    if strictly_equal:
        if len(container) != _len:
            raise ValueError("{} must be {} elements long. len({})={} was got."
                             .format(container_name, _len, container_name, len(container)))
    else:
        if len(container) > _len:
            raise ValueError("{} must be {} elements long. len({})={} was got."
                             .format(container_name, _len, container_name, len(container)))


def _try_cast(val, cast_type, varname: str) -> None:
    try:
        cast_type(val)
    except Exception:
        raise TypeError("Unable to cast {} of type {} to {}".format(varname, type(val), cast_type))


def _try_cast_container(container, cast_type, container_name: str) -> None:
    try:
        cast_type(*container)
    except Exception:
        raise TypeError("Unable to cast {} of type {} to {}".format(container_name, type(container), cast_type))


def _check_noncontainer_castability(val, cast_type, varname: str) -> None:
    """This routine is for container cast checking.

    Checks cast of one-element value of types int, float (or analogues) to corresponding ctypes'
    types

    :param val: value to cast
    :type val: Python int, float or analogues
    :param cast_type: type to cast to
    :type cast_type: ctype type
    :param varname: name of value
    :type varname: str
    :raises TypeError: In case of any cast errors, raises exception
    """
    if val == NOT_INITIALIZED:
        return

    # ctypes cannot cast its own type to the same type :_(
    # So in case of equal types, just return without an attempt to cast
    if type(val) is cast_type:
        return

    if cast_type is c_int16:
        _check_limits(val, _INT16_MIN, _INT16_MAX, varname)
    elif cast_type is c_int or cast_type is c_int32:
        _check_limits(val, _INT_MIN, _INT_MAX, varname)
    elif cast_type is c_longlong:
        _check_limits(val, _LONGLONG_MIN, _LONGLONG_MAX, varname)
    elif cast_type is c_uint8:
        _check_limits(val, _UINT8_MIN, _UINT8_MAX, varname)
    elif cast_type is c_uint16:
        _check_limits(val, _UINT16_MIN, _UINT16_MAX, varname)
    elif cast_type is c_uint or cast_type is c_uint32:
        _check_limits(val, _UINT_MIN, _UINT_MAX, varname)
    elif cast_type is c_float:
        _check_limits(abs(val), _FLOAT_ABS_MIN, _FLOAT_ABS_MAX, varname)
    else:
        raise TypeError("Usage of unrecognized type! {} was got.".format(type(val)))

    _try_cast(val, cast_type, varname)


def _check_container_castability(container, element_cast_type, length: int,
                                 strictly_equal: bool, container_name: str) -> None:
    """This routine is for container cast checking.

    Checks cast of lists and strings to corresponding ctypes types.

    :param container: container to cast
    :param element_cast_type: target array element type
    :type element_cast_type: ctypes' type
    :param length: length of target array type
    :type length: int
    :param strictly_equal: if True container is checked to be exactly length-element long
    :type strictly_equal: bool
    :param container_name: name of container
    :type container_name: str
    """
    if container is NOT_INITIALIZED:
        return

    # ctypes cannot cast its own type to the same type :_(
    # So in case of equal types, just return without an attempt to cast
    if type(container) is (element_cast_type * length):
        return

    _check_len(container, length, strictly_equal, container_name)

    if element_cast_type is c_int16:
        _check_integer_iteratively(container, container_name)
        _check_limits_iteratively(container, _UINT16_MIN, _UINT16_MAX, container_name)
    elif element_cast_type is c_int or element_cast_type is c_int32:
        _check_integer_iteratively(container, container_name)
        _check_limits_iteratively(container, _INT_MIN, _INT_MAX, container_name)
    elif element_cast_type is c_longlong:
        _check_integer_iteratively(container, container_name)
        _check_limits_iteratively(container, _LONGLONG_MIN, _LONGLONG_MAX, container_name)
    elif element_cast_type is c_uint8:
        _check_integer_iteratively(container, container_name)
        _check_limits_iteratively(container, _UINT8_MIN, _UINT8_MAX, container_name)
    elif element_cast_type is c_uint16:
        _check_integer_iteratively(container, container_name)
        _check_limits_iteratively(container, _UINT16_MIN, _UINT16_MAX, container_name)
    elif element_cast_type is c_uint or element_cast_type is c_uint32:
        _check_integer_iteratively(container, container_name)
        _check_limits_iteratively(container, _UINT_MIN, _UINT_MAX, container_name)
    elif element_cast_type is c_float:
        _check_float_iteratively(container, container_name)
        _check_limits_iteratively(list(map(abs, container)), _FLOAT_ABS_MIN, _FLOAT_ABS_MAX, container_name)
    elif element_cast_type is c_char:
        # Cast to C-string needs special treatment: highlevel structures contain Python strings which must be converted
        # to bytes before ctypes' cast.
        if not isinstance(container, str):
            raise TypeError("Cannot convert {} of type {} to {}. {}'s type must be str."
                            .format(container_name, type(container), element_cast_type * length, container_name))
        try:
            c_char_p(container.encode())
        except Exception:
            raise TypeError("Unable to cast {} of type {} to C-string.".format(container_name, type(container)))
        return
    else:
        raise TypeError("Usage of unrecognized type! {} was got.".format(type(container)))

    _try_cast_container(container, element_cast_type * length, container_name)


# ================================================ #
#            High level structure types            #
# ================================================ #
class feedback_settings_t:
    def __init__(self, IPS: int = NOT_INITIALIZED,
                 FeedbackType: flag_enumerations.FeedbackType = NOT_INITIALIZED,
                 FeedbackFlags: flag_enumerations.FeedbackFlags = NOT_INITIALIZED,
                 CountsPerTurn: int = NOT_INITIALIZED):
        """Feedback settings.

        This structure contains feedback settings.

        :param IPS: The number of encoder counts per shaft revolution. Range: 1..655535. The field is obsolete, it is
            recommended to write 0 to IPS and use the extended CountsPerTurn field. You may need to update the
            controller firmware to the latest version.
        :type IPS: int
        :param FeedbackType: Type of feedback. This is a bit mask for bitwise operations.
        :type FeedbackType: libximc.highlevel.FeedbackType
        :param FeedbackFlags: Flags. This is a bit mask for bitwise operations.
        :type FeedbackFlags: libximc.highlevel.FeedbackFlags
        :param CountsPerTurn: The number of encoder counts per shaft revolution. Range: 1..4294967295. To use the
            CountsPerTurn field, write 0 in the IPS field, otherwise the value from the IPS field will be used.
        :type CountsPerTurn: int
        """
        self.IPS = IPS
        self.FeedbackType = FeedbackType
        self.FeedbackFlags = FeedbackFlags
        self.CountsPerTurn = CountsPerTurn

    # getters
    @property
    def IPS(self) -> int:
        return self._IPS

    @property
    def FeedbackType(self) -> flag_enumerations.FeedbackType:
        return self._FeedbackType

    @property
    def FeedbackFlags(self) -> flag_enumerations.FeedbackFlags:
        return self._FeedbackFlags

    @property
    def CountsPerTurn(self) -> int:
        return self._CountsPerTurn

    # setters
    @IPS.setter
    def IPS(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="IPS")
        self._IPS = val

    @FeedbackType.setter
    def FeedbackType(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._FeedbackType = flag_enumerations.FeedbackType(val)
        except Exception:
            raise ValueError("FeedbackType = {} cannot be decomposed into {}.FeedbackType's flags!"
                             .format(hex(val), __package__))

    @FeedbackFlags.setter
    def FeedbackFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._FeedbackFlags = flag_enumerations.FeedbackFlags(val)
        except Exception:
            raise ValueError("FeedbackFlags = {} cannot be decomposed into {}.FeedbackFlags' flags!"
                             .format(hex(val), __package__))

    @CountsPerTurn.setter
    def CountsPerTurn(self, val):
        _check_noncontainer_castability(val, c_uint32, varname="CountsPerTurn")
        self._CountsPerTurn = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class home_settings_t:
    def __init__(
            self,
            FastHome: int = NOT_INITIALIZED,
            uFastHome: int = NOT_INITIALIZED,
            SlowHome: int = NOT_INITIALIZED,
            uSlowHome: int = NOT_INITIALIZED,
            HomeDelta: int = NOT_INITIALIZED,
            uHomeDelta: int = NOT_INITIALIZED,
            HomeFlags: flag_enumerations.HomeFlags = NOT_INITIALIZED):
        """Position calibration settings.

        This structure contains settings used in position calibration. It specify behavior of calibration procedure.

        :param FastHome: Speed used for first motion (full steps). Range: 0..100000.
        :type FastHome: int
        :param uFastHome: Fractional part of the speed for first motion, microsteps. The microstep size and the range
            of valid values for this field depend on the selected step division mode (see the MicrostepMode field in
            engine_settings).
        :type uFastHome: int
        :param SlowHome: Speed used for second motion (full steps). Range: 0..100000.
        :type SlowHome: int
        :param uSlowHome: Part of the speed for second motion, microsteps. The microstep size and the range of valid
            values for this field depend on the selected step division mode (see the MicrostepMode field in
            engine_settings).
        :type uSlowHome: int
        :param HomeDelta: Distance from break point (full steps).
        :type HomeDelta: int
        :param uHomeDelta: Fractional part of the delta distance, microsteps. The microstep size and the range of valid
            values for this field depend on the selected step division mode (see the MicrostepMode field in
            engine_settings).
        :type uHomeDelta: int
        :param HomeFlags: Set of flags specifies the direction and stopping conditions. This is a bit mask for bitwise
            operations.
        :type HomeFlags: libximc.highlevel.HomeFlags
        """
        self.FastHome = FastHome
        self.uFastHome = uFastHome
        self.SlowHome = SlowHome
        self.uSlowHome = uSlowHome
        self.HomeDelta = HomeDelta
        self.uHomeDelta = uHomeDelta
        self.HomeFlags = HomeFlags

    # getters
    @property
    def FastHome(self) -> int:
        return self._FastHome

    @property
    def uFastHome(self) -> int:
        return self._uFastHome

    @property
    def SlowHome(self) -> int:
        return self._SlowHome

    @property
    def uSlowHome(self) -> int:
        return self._uSlowHome

    @property
    def HomeDelta(self) -> int:
        return self._HomeDelta

    @property
    def uHomeDelta(self) -> int:
        return self._uHomeDelta

    @property
    def HomeFlags(self) -> flag_enumerations.HomeFlags:
        return self._HomeFlags

    # setters
    @FastHome.setter
    def FastHome(self, val):
        _check_noncontainer_castability(val, c_uint32, varname="FastHome")
        self._FastHome = val

    @uFastHome.setter
    def uFastHome(self, val):
        _check_noncontainer_castability(val, c_uint8, varname="uFastHome")
        self._uFastHome = val

    @SlowHome.setter
    def SlowHome(self, val):
        _check_noncontainer_castability(val, c_uint32, varname="SlowHome")
        self._SlowHome = val

    @uSlowHome.setter
    def uSlowHome(self, val):
        _check_noncontainer_castability(val, c_uint8, varname="uSlowHome")
        self._uSlowHome = val

    @HomeDelta.setter
    def HomeDelta(self, val):
        _check_noncontainer_castability(val, c_int32, varname="HomeDelta")
        self._HomeDelta = val

    @uHomeDelta.setter
    def uHomeDelta(self, val):
        _check_noncontainer_castability(val, c_int16, varname="uHomeDelta")
        self._uHomeDelta = val

    @HomeFlags.setter
    def HomeFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._HomeFlags = flag_enumerations.HomeFlags(val)
        except Exception:
            raise ValueError("HomeFlags = {} cannot be decomposed into {}.HomeFlags' flags!"
                             .format(hex(val), __package__))

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class home_settings_calb_t:
    def __init__(
            self,
            FastHome: float = NOT_INITIALIZED,
            SlowHome: float = NOT_INITIALIZED,
            HomeDelta: float = NOT_INITIALIZED,
            HomeFlags: flag_enumerations.HomeFlags = NOT_INITIALIZED):
        """Position calibration settings which use user units.

        This structure contains settings used in position calibrating. It specify behavior of calibrating position.

        :param FastHome: Speed used for first motion.
        :type FastHome: float
        :param SlowHome: Speed used for second motion.
        :type SlowHome: float
        :param HomeDelta: Distance from break point.
        :type HomeDelta: float
        :param HomeFlags: Set of flags specifies the direction and stopping conditions. This is a bit mask for bitwise
            operations.
        :type HomeFlags: libximc.highlevel.HomeFlags
        """
        self.FastHome = FastHome
        self.SlowHome = SlowHome
        self.HomeDelta = HomeDelta
        self.HomeFlags = HomeFlags

    # getters
    @property
    def FastHome(self) -> float:
        return self._FastHome

    @property
    def SlowHome(self) -> float:
        return self._SlowHome

    @property
    def HomeDelta(self) -> float:
        return self._HomeDelta

    @property
    def HomeFlags(self) -> flag_enumerations.HomeFlags:
        return self._HomeFlags

    # setters
    @FastHome.setter
    def FastHome(self, val):
        _check_noncontainer_castability(val, c_float, varname="FastHome")
        self._FastHome = val

    @SlowHome.setter
    def SlowHome(self, val):
        _check_noncontainer_castability(val, c_float, varname="SlowHome")
        self._SlowHome = val

    @HomeDelta.setter
    def HomeDelta(self, val):
        _check_noncontainer_castability(val, c_float, varname="HomeDelta")
        self._HomeDelta = val

    @HomeFlags.setter
    def HomeFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._HomeFlags = flag_enumerations.HomeFlags(val)
        except Exception:
            raise ValueError("HomeFlags = {} cannot be decomposed into {}.HomeFlags' flags!"
                             .format(hex(val), __package__))

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class move_settings_t:
    def __init__(
            self,
            Speed: int = NOT_INITIALIZED,
            uSpeed: int = NOT_INITIALIZED,
            Accel: int = NOT_INITIALIZED,
            Decel: int = NOT_INITIALIZED,
            AntiplaySpeed: int = NOT_INITIALIZED,
            uAntiplaySpeed: int = NOT_INITIALIZED,
            MoveFlags: flag_enumerations.MoveFlags = NOT_INITIALIZED):
        """Move settings.

        :param Speed: Target speed (for stepper motor: steps/s, for DC: rpm). Range: 0..100000.
        :type Speed: int
        :param uSpeed: Target speed in microstep fractions/s. The microstep size and the range of valid values for this
            field depend on the selected step division mode (see the MicrostepMode field in engine_settings). Used with
            a stepper motor only.
        :type uSpeed: int
        :param Accel: Motor shaft acceleration, steps/s^2 (stepper motor) or RPM/s (DC). Range: 1..65535.
        :type Accel: int
        :param Decel: Motor shaft deceleration, steps/s^2 (stepper motor) or RPM/s (DC). Range: 1..65535.
        :type Decel: int
        :param AntiplaySpeed: Speed in antiplay mode, full steps/s (stepper motor) or RPM (DC). Range: 0..100000.
        :type AntiplaySpeed: int
        :param uAntiplaySpeed: Speed in antiplay mode, microsteps/s. The microstep size and the range of valid values
            for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings).
            Used with a stepper motor only.
        :type uAntiplaySpeed: int
        :param MoveFlags: Flags that control movement settings. This is a bit mask for bitwise operations.
        :type MoveFlags: libximc.highlevel.MoveFlags
        """
        self.Speed = Speed
        self.uSpeed = uSpeed
        self.Accel = Accel
        self.Decel = Decel
        self.AntiplaySpeed = AntiplaySpeed
        self.uAntiplaySpeed = uAntiplaySpeed
        self.MoveFlags = MoveFlags

    # getters
    @property
    def Speed(self) -> int:
        return self._Speed

    @property
    def uSpeed(self) -> int:
        return self._uSpeed

    @property
    def Accel(self) -> int:
        return self._Accel

    @property
    def Decel(self) -> int:
        return self._Decel

    @property
    def AntiplaySpeed(self) -> int:
        return self._AntiplaySpeed

    @property
    def uAntiplaySpeed(self) -> int:
        return self._uAntiplaySpeed

    @property
    def MoveFlags(self) -> flag_enumerations.MoveFlags:
        return self._MoveFlags

    # setters
    @Speed.setter
    def Speed(self, val):
        _check_noncontainer_castability(val, c_uint32, varname="Speed")
        self._Speed = val

    @uSpeed.setter
    def uSpeed(self, val):
        _check_noncontainer_castability(val, c_uint8, varname="uSpeed")
        self._uSpeed = val

    @Accel.setter
    def Accel(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="Accel")
        self._Accel = val

    @Decel.setter
    def Decel(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="Decel")
        self._Decel = val

    @AntiplaySpeed.setter
    def AntiplaySpeed(self, val):
        _check_noncontainer_castability(val, c_uint32, varname="AntiplaySpeed")
        self._AntiplaySpeed = val

    @uAntiplaySpeed.setter
    def uAntiplaySpeed(self, val):
        _check_noncontainer_castability(val, c_uint8, varname="uAntiplaySpeed")
        self._uAntiplaySpeed = val

    @MoveFlags.setter
    def MoveFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._MoveFlags = flag_enumerations.MoveFlags(val)
        except Exception:
            raise ValueError("MoveFlags = {} cannot be decomposed into {}.MoveFlags' flags!"
                             .format(hex(val), __package__))

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class move_settings_calb_t:
    def __init__(
            self,
            Speed: float = NOT_INITIALIZED,
            Accel: float = NOT_INITIALIZED,
            Decel: float = NOT_INITIALIZED,
            AntiplaySpeed: float = NOT_INITIALIZED,
            MoveFlags: flag_enumerations.MoveFlags = NOT_INITIALIZED):
        """User units move settings.

        :param Speed: Target speed.
        :type Speed: float
        :param Accel: Motor shaft acceleration, steps/s^2 (stepper motor) or RPM/s (DC).
        :type Accel: float
        :param Decel: Motor shaft deceleration, steps/s^2 (stepper motor) or RPM/s (DC).
        :type Decel: float
        :param AntiplaySpeed: Speed in antiplay mode.
        :type AntiplaySpeed: float
        :param MoveFlags: Flags that control movement settings. This is a bit mask for bitwise operations.
        :type MoveFlags: libximc.highlevel.MoveFlags
        """
        self.Speed = Speed
        self.Accel = Accel
        self.Decel = Decel
        self.AntiplaySpeed = AntiplaySpeed
        self.MoveFlags = MoveFlags

    # getters
    @property
    def Speed(self) -> float:
        return self._Speed

    @property
    def Accel(self) -> float:
        return self._Accel

    @property
    def Decel(self) -> float:
        return self._Decel

    @property
    def AntiplaySpeed(self) -> float:
        return self._AntiplaySpeed

    @property
    def MoveFlags(self) -> flag_enumerations.MoveFlags:
        return self._MoveFlags

    # setters
    @Speed.setter
    def Speed(self, val):
        _check_noncontainer_castability(val, c_float, varname="Speed")
        self._Speed = val

    @Accel.setter
    def Accel(self, val):
        _check_noncontainer_castability(val, c_float, varname="Accel")
        self._Accel = val

    @Decel.setter
    def Decel(self, val):
        _check_noncontainer_castability(val, c_float, varname="Decel")
        self._Decel = val

    @AntiplaySpeed.setter
    def AntiplaySpeed(self, val):
        _check_noncontainer_castability(val, c_float, varname="AntiplaySpeed")
        self._AntiplaySpeed = val

    @MoveFlags.setter
    def MoveFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._MoveFlags = flag_enumerations.MoveFlags(val)
        except Exception:
            raise ValueError("MoveFlags = {} cannot be decomposed into {}.MoveFlags' flags!"
                             .format(hex(val), __package__))

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class engine_settings_t:
    def __init__(
            self,
            NomVoltage: int = NOT_INITIALIZED,
            NomCurrent: int = NOT_INITIALIZED,
            NomSpeed: int = NOT_INITIALIZED,
            uNomSpeed: int = NOT_INITIALIZED,
            EngineFlags: flag_enumerations.EngineFlags = NOT_INITIALIZED,
            Antiplay: int = NOT_INITIALIZED,
            MicrostepMode: flag_enumerations.MicrostepMode = NOT_INITIALIZED,
            StepsPerRev: int = NOT_INITIALIZED):
        """Movement limitations and settings related to the motor.

        This structure contains useful motor settings. These settings specify the motor shaft movement algorithm, list
        of limitations and rated characteristics. All boards are supplied with the standard set of engine settings on
        the controller's flash memory. Please load new engine settings when you change the motor, encoder, positioner,
        etc. Please note that wrong engine settings may lead to device malfunction, which can lead to irreversible
        damage to the board.

        :param NomVoltage: Rated voltage in tens of mV. Controller will keep the voltage drop on motor below this value
            if ENGINE_LIMIT_VOLT flag is set (used with DC only).
        :type NomVoltage: int
        :param NomCurrent: Rated current (in mA). Controller will keep current consumed by motor below this value if
            ENGINE_LIMIT_CURR flag is set. Range: 15..8000
        :type NomCurrent: int
        :param NomSpeed: Nominal (maximum) speed (in whole steps/s or rpm for DC and stepper motor as a master encoder).
            Controller will keep motor shaft RPM below this value if ENGINE_LIMIT_RPM flag is set. Range: 1..100000.
        :type NomSpeed: int
        :param uNomSpeed: The fractional part of a nominal speed in microsteps (is only used with stepper motor).
            Microstep size and the range of valid values for this field depend on selected step division mode (see
            MicrostepMode field in engine_settings).
        :type uNomSpeed: int
        :param EngineFlags: Set of flags specify motor shaft movement algorithm and list of limitations. This is a bit
            mask for bitwise operations.
        :type EngineFlags: libximc.highlevel.EngineFlags
        :param Antiplay: Number of pulses or steps for backlash (play) compensation procedure. Used if ENGINE_ANTIPLAY
            flag is set.
        :type Antiplay: int
        :param MicrostepMode: Settings of microstep mode (Used with stepper motor only). Microstep size and the range of
            valid values for this field depend on selected step division mode (see MicrostepMode field in
            engine_settings). This is a bit mask for bitwise operations.
        :type MicrostepMode: libximc.highlevel.MicrostepMode
        :param StepsPerRev: Number of full steps per revolution (Used with stepper motor only). Range: 1..65535.
        :type StepsPerRev: int
        """
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
    def NomVoltage(self) -> int:
        return self._NomVoltage

    @property
    def NomCurrent(self) -> int:
        return self._NomCurrent

    @property
    def NomSpeed(self) -> int:
        return self._NomSpeed

    @property
    def uNomSpeed(self) -> int:
        return self._uNomSpeed

    @property
    def EngineFlags(self) -> flag_enumerations.EngineFlags:
        return self._EngineFlags

    @property
    def Antiplay(self) -> int:
        return self._Antiplay

    @property
    def MicrostepMode(self) -> flag_enumerations.MicrostepMode:
        return self._MicrostepMode

    @property
    def StepsPerRev(self) -> int:
        return self._StepsPerRev

    # setters
    @NomVoltage.setter
    def NomVoltage(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="NomVoltage")
        self._NomVoltage = val

    @NomCurrent.setter
    def NomCurrent(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="NomCurrent")
        self._NomCurrent = val

    @NomSpeed.setter
    def NomSpeed(self, val):
        _check_noncontainer_castability(val, c_uint32, varname="NomSpeed")
        self._NomSpeed = val

    @uNomSpeed.setter
    def uNomSpeed(self, val):
        _check_noncontainer_castability(val, c_uint8, varname="uNomSpeed")
        self._uNomSpeed = val

    @EngineFlags.setter
    def EngineFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._EngineFlags = flag_enumerations.EngineFlags(val)
        except Exception:
            raise ValueError("EngineFlags = {} cannot be decomposed into {}.EngineFlags' flags!"
                             .format(hex(val), __package__))

    @Antiplay.setter
    def Antiplay(self, val):
        _check_noncontainer_castability(val, c_int16, varname="Antiplay")
        self._Antiplay = val

    @MicrostepMode.setter
    def MicrostepMode(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._MicrostepMode = val
        except Exception:
            raise ValueError("MicrostepMode = {} cannot be decomposed into {}.MicrostepMode's flags!"
                             .format(hex(val), __package__))

    @StepsPerRev.setter
    def StepsPerRev(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="StepsPerRev")
        self._StepsPerRev = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class engine_settings_calb_t:
    def __init__(
            self,
            NomVoltage: int = NOT_INITIALIZED,
            NomCurrent: int = NOT_INITIALIZED,
            NomSpeed: float = NOT_INITIALIZED,
            EngineFlags: flag_enumerations.EngineFlags = NOT_INITIALIZED,
            Antiplay: float = NOT_INITIALIZED,
            MicrostepMode: flag_enumerations.MicrostepMode = NOT_INITIALIZED,
            StepsPerRev: int = NOT_INITIALIZED):
        """Movement limitations and settings, related to the motor. In user units.

        This structure contains useful motor settings. These settings specify the motor shaft movement algorithm, list
        of limitations and rated characteristics. All boards are supplied with the standard set of engine settings on
        the controller's flash memory. Please load new engine settings when you change the motor, encoder, positioner,
        etc. Please note that wrong engine settings may lead to the device malfunction, that may cause irreversible
        damage to the board.

        :param NomVoltage: Rated voltage in tens of mV. Controller will keep the voltage drop on motor below this value
            if ENGINE_LIMIT_VOLT flag is set (used with DC only).
        :type NomVoltage: int
        :param NomCurrent: Rated current (in mA). Controller will keep current consumed by motor below this value if
            ENGINE_LIMIT_CURR flag is set. Range: 15..8000
        :type NomCurrent: int
        :param NomSpeed: Nominal speed. Controller will keep motor speed below this value if ENGINE_LIMIT_RPM flag is
            set.
        :type NomSpeed: float
        :param EngineFlags: Set of flags specify motor shaft movement algorithm and a list of limitations. This is a
            bit mask for bitwise operations.
        :type EngineFlags: libximc.highlevel.EngineFlags
        :param Antiplay: Number of pulses or steps for backlash (play) compensation procedure. Used if ENGINE_ANTIPLAY
            flag is set.
        :type Antiplay: float
        :param MicrostepMode: Settings of microstep mode (Used with stepper motor only). the microstep size and the
            range of valid values for this field depend on the selected step division mode (see MicrostepMode field
            in engine_settings). This is a bit mask for bitwise operations.
        :type MicrostepMode: libximc.highlevel.MicrostepMode
        :param StepsPerRev: Number of full steps per revolution (Used with stepper motor only). Range: 1..65535.
        :type StepsPerRev: int
        """
        self.NomVoltage = NomVoltage
        self.NomCurrent = NomCurrent
        self.NomSpeed = NomSpeed
        self.EngineFlags = EngineFlags
        self.Antiplay = Antiplay
        self.MicrostepMode = MicrostepMode
        self.StepsPerRev = StepsPerRev

    # getters
    @property
    def NomVoltage(self) -> int:
        return self._NomVoltage

    @property
    def NomCurrent(self) -> int:
        return self._NomCurrent

    @property
    def NomSpeed(self) -> float:
        return self._NomSpeed

    @property
    def EngineFlags(self) -> flag_enumerations.EngineFlags:
        return self._EngineFlags

    @property
    def Antiplay(self) -> float:
        return self._Antiplay

    @property
    def MicrostepMode(self) -> flag_enumerations.MicrostepMode:
        return self._MicrostepMode

    @property
    def StepsPerRev(self) -> int:
        return self._StepsPerRev

    # setters
    @NomVoltage.setter
    def NomVoltage(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="NomVoltage")
        self._NomVoltage = val

    @NomCurrent.setter
    def NomCurrent(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="NomCurrent")
        self._NomCurrent = val

    @NomSpeed.setter
    def NomSpeed(self, val):
        _check_noncontainer_castability(val, c_float, varname="NomSpeed")
        self._NomSpeed = val

    @EngineFlags.setter
    def EngineFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._EngineFlags = flag_enumerations.EngineFlags(val)
        except Exception:
            raise ValueError("EngineFlags = {} cannot be decomposed into {}.EngineFlags' flags!"
                             .format(hex(val), __package__))

    @Antiplay.setter
    def Antiplay(self, val):
        _check_noncontainer_castability(val, c_float, varname="Antiplay")
        self._Antiplay = val

    @MicrostepMode.setter
    def MicrostepMode(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._MicrostepMode = val
        except Exception:
            raise ValueError("MicrostepMode = {} cannot be decomposed into {}.MicrostepMode's flags!"
                             .format(hex(val), __package__))

    @StepsPerRev.setter
    def StepsPerRev(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="StepsPerRev")
        self._StepsPerRev = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class entype_settings_t:
    def __init__(
            self,
            EngineType: flag_enumerations.EngineType = NOT_INITIALIZED,
            DriverType: flag_enumerations.DriverType = NOT_INITIALIZED):
        """Engine type and driver type settings.

        :param EngineType: Engine type. This is a bit mask for bitwise operations.
        :type EngineType: libximc.highlevel.EngineType
        :param DriverType: Driver type. This is a bit mask for bitwise operations.
        :type DriverType: libximc.highlevel.DriverType
        """
        self.EngineType = EngineType
        self.DriverType = DriverType

    # getters
    @property
    def EngineType(self) -> flag_enumerations.EngineType:
        return self._EngineType

    @property
    def DriverType(self) -> flag_enumerations.DriverType:
        return self._DriverType

    # setters
    @EngineType.setter
    def EngineType(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._EngineType = flag_enumerations.EngineType(val)
        except Exception:
            raise ValueError("EngineType = {} cannot be decomposed into {}.EngineType's flags!"
                             .format(hex(val), __package__))

    @DriverType.setter
    def DriverType(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._DriverType = flag_enumerations.DriverType(val)
        except Exception:
            raise ValueError("DriverType = {} cannot be decomposed into {}.DriverType's flags!"
                             .format(hex(val), __package__))

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class power_settings_t:
    def __init__(
            self,
            HoldCurrent: int = NOT_INITIALIZED,
            CurrReductDelay: int = NOT_INITIALIZED,
            PowerOffDelay: int = NOT_INITIALIZED,
            CurrentSetTime: int = NOT_INITIALIZED,
            PowerFlags: flag_enumerations.PowerFlags = NOT_INITIALIZED):
        """Step motor power settings.

        :param HoldCurrent: Holding current, as percent of the nominal current. Range: 0..100.
        :type HoldCurrent: int
        :param CurrReductDelay: Time in ms from going to STOP state to the end of current reduction.
        :type CurrReductDelay: int
        :param PowerOffDelay: Time in s from going to STOP state to turning power off.
        :type PowerOffDelay: int
        :param CurrentSetTime: Time in ms to reach the nominal current.
        :type CurrentSetTime: int
        :param PowerFlags: Flags with parameters of power control. This is a bit mask for bitwise operations.
        :type PowerFlags: libximc.highlevel.PowerFlags
        """
        self.HoldCurrent = HoldCurrent
        self.CurrReductDelay = CurrReductDelay
        self.PowerOffDelay = PowerOffDelay
        self.CurrentSetTime = CurrentSetTime
        self.PowerFlags = PowerFlags

    # getters
    @property
    def HoldCurrent(self) -> int:
        return self._HoldCurrent

    @property
    def CurrReductDelay(self) -> int:
        return self._CurrReductDelay

    @property
    def PowerOffDelay(self) -> int:
        return self._PowerOffDelay

    @property
    def CurrentSetTime(self) -> int:
        return self._CurrentSetTime

    @property
    def PowerFlags(self) -> flag_enumerations.PowerFlags:
        return self._PowerFlags

    # setters
    @HoldCurrent.setter
    def HoldCurrent(self, val):
        _check_noncontainer_castability(val, c_uint8, varname="HoldCurrent")
        self._HoldCurrent = val

    @CurrReductDelay.setter
    def CurrReductDelay(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="CurrReductDelay")
        self._CurrReductDelay = val

    @PowerOffDelay.setter
    def PowerOffDelay(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="PowerOffDelay")
        self._PowerOffDelay = val

    @CurrentSetTime.setter
    def CurrentSetTime(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="CurrentSetTime")
        self._CurrentSetTime = val

    @PowerFlags.setter
    def PowerFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._PowerFlags = flag_enumerations.PowerFlags(val)
        except Exception:
            raise ValueError("PowerFlags = {} cannot be decomposed into {}.PowerFlags' flags!"
                             .format(hex(val), __package__))

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class secure_settings_t:
    def __init__(
            self,
            LowUpwrOff: int = NOT_INITIALIZED,
            CriticalIpwr: int = NOT_INITIALIZED,
            CriticalUpwr: int = NOT_INITIALIZED,
            CriticalT: int = NOT_INITIALIZED,
            CriticalIusb: int = NOT_INITIALIZED,
            CriticalUusb: int = NOT_INITIALIZED,
            MinimumUusb: int = NOT_INITIALIZED,
            Flags: flag_enumerations.SecureFlags = NOT_INITIALIZED):
        """This structure contains raw analog data from ADC embedded on board.

        These data used for device testing and deep recalibration by manufacturer only.

        :param LowUpwrOff: Lower voltage limit to turn off the motor, in tens of mV.
        :type LowUpwrOff: int
        :param CriticalIpwr: Maximum motor current which triggers ALARM state, in mA.
        :type CriticalIpwr: int
        :param CriticalUpwr: Maximum motor voltage which triggers ALARM state, in tens of mV.
        :type CriticalUpwr: int
        :param CriticalT: Maximum temperature, which triggers ALARM state, in tenths of degrees Celsius.
        :type CriticalT: int
        :param CriticalIusb: Maximum USB current which triggers ALARM state, in mA.
        :type CriticalIusb: int
        :param CriticalUusb: Maximum USB voltage which triggers ALARM state, in tens of mV.
        :type CriticalUusb: int
        :param MinimumUusb: Minimum USB voltage which triggers ALARM state, in tens of mV.
        :type MinimumUusb: int
        :param Flags: Critical parameter flags. This is a bit mask for bitwise operations.
        :type Flags: libximc.highlevel.SecureFlags
        """
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
    def LowUpwrOff(self) -> int:
        return self._LowUpwrOff

    @property
    def CriticalIpwr(self) -> int:
        return self._CriticalIpwr

    @property
    def CriticalUpwr(self) -> int:
        return self._CriticalUpwr

    @property
    def CriticalT(self) -> int:
        return self._CriticalT

    @property
    def CriticalIusb(self) -> int:
        return self._CriticalIusb

    @property
    def CriticalUusb(self) -> int:
        return self._CriticalUusb

    @property
    def MinimumUusb(self) -> int:
        return self._MinimumUusb

    @property
    def Flags(self) -> flag_enumerations.SecureFlags:
        return self._Flags

    # setters
    @LowUpwrOff.setter
    def LowUpwrOff(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="LowUpwrOff")
        self._LowUpwrOff = val

    @CriticalIpwr.setter
    def CriticalIpwr(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="CriticalIpwr")
        self._CriticalIpwr = val

    @CriticalUpwr.setter
    def CriticalUpwr(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="CriticalUpwr")
        self._CriticalUpwr = val

    @CriticalT.setter
    def CriticalT(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="CriticalT")
        self._CriticalT = val

    @CriticalIusb.setter
    def CriticalIusb(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="CriticalIusb")
        self._CriticalIusb = val

    @CriticalUusb.setter
    def CriticalUusb(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="CriticalUusb")
        self._CriticalUusb = val

    @MinimumUusb.setter
    def MinimumUusb(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="MinimumUusb")
        self._MinimumUusb = val

    @Flags.setter
    def Flags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._Flags = flag_enumerations.SecureFlags(val)
        except Exception:
            raise ValueError("Flags = {} cannot be decomposed into {}.SecureFlags' flags!")

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class edges_settings_t:
    def __init__(
            self,
            BorderFlags: flag_enumerations.BorderFlags = NOT_INITIALIZED,
            EnderFlags: flag_enumerations.EnderFlags = NOT_INITIALIZED,
            LeftBorder: int = NOT_INITIALIZED,
            uLeftBorder: int = NOT_INITIALIZED,
            RightBorder: int = NOT_INITIALIZED,
            uRightBorder: int = NOT_INITIALIZED):
        """Edges settings.

        This structure contains border and limit switches settings. Please load new engine settings when you change
        positioner, etc. Please note that wrong engine settings may lead to device malfunction, which can cause
        irreversible damage to the board.

        :param BorderFlags: Border flags, specify types of borders and motor behavior at borders. This is a bit mask
            for bitwise operations.
        :type BorderFlags: libximc.highlevel.BorderFlags
        :param EnderFlags: Flags specify electrical behavior of limit switches like order and pulled positions. This is
            a bit mask for bitwise operations.
        :type EnderFlags: libximc.highlevel.EnderFlags
        :param LeftBorder: Left border position, used if BORDER_IS_ENCODER flag is set.
        :type LeftBorder: int
        :param uLeftBorder: Left border position in microsteps (used with stepper motor only). The microstep size and
            the range of valid values for this field depend on the selected step division mode (see the MicrostepMode
            field in engine_settings).
        :type uLeftBorder: int
        :param RightBorder: Right border position, used if BORDER_IS_ENCODER flag is set.
        :type RightBorder: int
        :param uRightBorder: Right border position in microsteps. Used with a stepper motor only. The microstep size
            and the range of valid values for this field depend on the selected step division mode (see the
            MicrostepMode field in engine_settings).
        :type uRightBorder: int
        """
        self.BorderFlags = BorderFlags
        self.EnderFlags = EnderFlags
        self.LeftBorder = LeftBorder
        self.uLeftBorder = uLeftBorder
        self.RightBorder = RightBorder
        self.uRightBorder = uRightBorder

    # getters
    @property
    def BorderFlags(self) -> flag_enumerations.BorderFlags:
        return self._BorderFlags

    @property
    def EnderFlags(self) -> flag_enumerations.EnderFlags:
        return self._EnderFlags

    @property
    def LeftBorder(self) -> int:
        return self._LeftBorder

    @property
    def uLeftBorder(self) -> int:
        return self._uLeftBorder

    @property
    def RightBorder(self) -> int:
        return self._RightBorder

    @property
    def uRightBorder(self) -> int:
        return self._uRightBorder

    # setters
    @BorderFlags.setter
    def BorderFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._BorderFlags = flag_enumerations.BorderFlags(val)
        except Exception:
            raise ValueError("BorderFlags = {} cannot be decomposed into {}.BorderFlags' flags!"
                             .format(hex(val), __package__))

    @EnderFlags.setter
    def EnderFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._EnderFlags = flag_enumerations.EnderFlags(val)
        except Exception:
            raise ValueError("EnderFlags = {} cannot be decomposed into {}.EnderFlags' flags!"
                             .format(hex(val), __package__))

    @LeftBorder.setter
    def LeftBorder(self, val):
        _check_noncontainer_castability(val, c_int32, varname="LeftBorder")
        self._LeftBorder = val

    @uLeftBorder.setter
    def uLeftBorder(self, val):
        _check_noncontainer_castability(val, c_int16, varname="uLeftBorder")
        self._uLeftBorder = val

    @RightBorder.setter
    def RightBorder(self, val):
        _check_noncontainer_castability(val, c_int32, varname="RightBorder")
        self._RightBorder = val

    @uRightBorder.setter
    def uRightBorder(self, val):
        _check_noncontainer_castability(val, c_int16, varname="uRightBorder")
        self._uRightBorder = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class edges_settings_calb_t:
    def __init__(
            self,
            BorderFlags: flag_enumerations.BorderFlags = NOT_INITIALIZED,
            EnderFlags: flag_enumerations.EnderFlags = NOT_INITIALIZED,
            LeftBorder: float = NOT_INITIALIZED,
            RightBorder: float = NOT_INITIALIZED):
        """Edges settings which use user units.

        This structure contains border and limit switches settings. Please load new engine settings when you change
        positioner, etc. Please note that wrong engine settings may lead to device malfunction, which can cause
        irreversible damage to the board.

        :param BorderFlags: Border flags, specify types of borders and motor behavior at borders. This is a bit mask
            for bitwise operations.
        :type BorderFlags: libximc.highlevel.BorderFlags
        :param EnderFlags: Flags specify electrical behavior of limit switches like order and pulled positions. This is
            a bit mask for bitwise operations.
        :type EnderFlags: libximc.highlevel.EnderFlags
        :param LeftBorder: Left border position, used if BORDER_IS_ENCODER flag is set. Corrected by the table.
        :type LeftBorder: float
        :param RightBorder: Right border position, used if BORDER_IS_ENCODER flag is set. Corrected by the table.
        :type RightBorder: float
        """
        self.BorderFlags = BorderFlags
        self.EnderFlags = EnderFlags
        self.LeftBorder = LeftBorder
        self.RightBorder = RightBorder

    # getters
    @property
    def BorderFlags(self) -> flag_enumerations.BorderFlags:
        return self._BorderFlags

    @property
    def EnderFlags(self) -> flag_enumerations.EnderFlags:
        return self._EnderFlags

    @property
    def LeftBorder(self) -> float:
        return self._LeftBorder

    @property
    def RightBorder(self) -> float:
        return self._RightBorder

    # setters
    @BorderFlags.setter
    def BorderFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._BorderFlags = flag_enumerations.BorderFlags(val)
        except Exception:
            raise ValueError("BorderFlags = {} cannot be decomposed into {}.BorderFlags' flags!"
                             .format(hex(val), __package__))

    @EnderFlags.setter
    def EnderFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._EnderFlags = flag_enumerations.EnderFlags(val)
        except Exception:
            raise ValueError("EnderFlags = {} cannot be decomposed into {}.EnderFlags' flags!"
                             .format(hex(val), __package__))

    @LeftBorder.setter
    def LeftBorder(self, val):
        _check_noncontainer_castability(val, c_float, varname="LeftBorder")
        self._LeftBorder = val

    @RightBorder.setter
    def RightBorder(self, val):
        _check_noncontainer_castability(val, c_float, varname="RightBorder")
        self._RightBorder = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class pid_settings_t:
    def __init__(
            self,
            KpU: int = NOT_INITIALIZED,
            KiU: int = NOT_INITIALIZED,
            KdU: int = NOT_INITIALIZED,
            Kpf: float = NOT_INITIALIZED,
            Kif: float = NOT_INITIALIZED,
            Kdf: float = NOT_INITIALIZED):
        """PID settings.

        This structure contains factors for PID routine. It specifies the behavior of the voltage PID routine. These
        factors are slightly different for different positioners. All boards are supplied with the standard set of PID
        settings in the controller's flash memory. Please load new PID settings when you change positioner. Please note
        that wrong PID settings lead to device malfunction.

        :param KpU: Proportional gain for voltage PID routine.
        :type KpU: int
        :param KiU: Integral gain for voltage PID routine.
        :type KiU: int
        :param KdU: Differential gain for voltage PID routine.
        :type KdU: int
        :param Kpf: Proportional gain for BLDC position PID routine.
        :type Kpf: float
        :param Kif: Integral gain for BLDC position PID routine.
        :type Kif: float
        :param Kdf: Differential gain for BLDC position PID routine.
        :type Kdf: float
        """
        self.KpU = KpU
        self.KiU = KiU
        self.KdU = KdU
        self.Kpf = Kpf
        self.Kif = Kif
        self.Kdf = Kdf

    # getters
    @property
    def KpU(self) -> int:
        return self._KpU

    @property
    def KiU(self) -> int:
        return self._KiU

    @property
    def KdU(self) -> int:
        return self._KdU

    @property
    def Kpf(self) -> float:
        return self._Kpf

    @property
    def Kif(self) -> float:
        return self._Kif

    @property
    def Kdf(self) -> float:
        return self._Kdf

    # setters
    @KpU.setter
    def KpU(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="KpU")
        self._KpU = val

    @KiU.setter
    def KiU(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="KiU")
        self._KiU = val

    @KdU.setter
    def KdU(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="KdU")
        self._KdU = val

    @Kpf.setter
    def Kpf(self, val):
        _check_noncontainer_castability(val, c_float, varname="Kpf")
        self._Kpf = val

    @Kif.setter
    def Kif(self, val):
        _check_noncontainer_castability(val, c_float, varname="Kif")
        self._Kif = val

    @Kdf.setter
    def Kdf(self, val):
        _check_noncontainer_castability(val, c_float, varname="Kdf")
        self._Kdf = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class sync_in_settings_t:
    def __init__(
            self,
            SyncInFlags: flag_enumerations.SyncInFlags = NOT_INITIALIZED,
            ClutterTime: int = NOT_INITIALIZED,
            Position: int = NOT_INITIALIZED,
            uPosition: int = NOT_INITIALIZED,
            Speed: int = NOT_INITIALIZED,
            uSpeed: int = NOT_INITIALIZED):
        """Synchronization settings.

        This structure contains all synchronization settings, modes, periods and flags. It specifies the behavior of
        the input synchronization. All boards are supplied with the standard set of these settings.

        :param SyncInFlags: Input synchronization flags. This is a bit mask for bitwise operations.
        :type SyncInFlags: libximc.highlevel.SyncInFlags
        :param ClutterTime: Input synchronization pulse dead time (us).
        :type ClutterTime: int
        :param Position: Desired position or shift (full steps)
        :type Position: int
        :param uPosition: The fractional part of a position or shift in microsteps. It is used with a stepper motor.
            The microstep size and the range of valid values for this field depend on the selected step division mode
            (see the MicrostepMode field in engine_settings).
        :type uPosition: int
        :param Speed: Target speed (for stepper motor: steps/s, for DC: rpm). Range: 0..100000.
        :type Speed: int
        :param uSpeed: Target speed in microsteps/s. Microstep size and the range of valid values for this field depend
            on the selected step division mode (see the MicrostepMode field in engine_settings). Used a stepper motor
            only.
        :type uSpeed: int
        """
        self.SyncInFlags = SyncInFlags
        self.ClutterTime = ClutterTime
        self.Position = Position
        self.uPosition = uPosition
        self.Speed = Speed
        self.uSpeed = uSpeed

    # getters
    @property
    def SyncInFlags(self) -> flag_enumerations.SyncInFlags:
        return self._SyncInFlags

    @property
    def ClutterTime(self) -> int:
        return self._ClutterTime

    @property
    def Position(self) -> int:
        return self._Position

    @property
    def uPosition(self) -> int:
        return self._uPosition

    @property
    def Speed(self) -> int:
        return self._Speed

    @property
    def uSpeed(self) -> int:
        return self._uSpeed

    # setters
    @SyncInFlags.setter
    def SyncInFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._SyncInFlags = flag_enumerations.SyncInFlags(val)
        except Exception:
            raise ValueError("SyncInFlags = {} cannot be decomposed into {}.SyncInFlags' flags!"
                             .format(hex(val), __package__))

    @ClutterTime.setter
    def ClutterTime(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="ClutterTime")
        self._ClutterTime = val

    @Position.setter
    def Position(self, val):
        _check_noncontainer_castability(val, c_int32, varname="Position")
        self._Position = val

    @uPosition.setter
    def uPosition(self, val):
        _check_noncontainer_castability(val, c_int16, varname="uPosition")
        self._uPosition = val

    @Speed.setter
    def Speed(self, val):
        _check_noncontainer_castability(val, c_uint32, varname="Speed")
        self._Speed = val

    @uSpeed.setter
    def uSpeed(self, val):
        _check_noncontainer_castability(val, c_uint8, varname="uSpeed")
        self._uSpeed = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class sync_in_settings_calb_t:
    def __init__(
            self,
            SyncInFlags: flag_enumerations.SyncInFlags = NOT_INITIALIZED,
            ClutterTime: int = NOT_INITIALIZED,
            Position: float = NOT_INITIALIZED,
            Speed: float = NOT_INITIALIZED):
        """User unit synchronization settings.

        This structure contains all synchronization settings, modes, periods and flags. It specifies behavior of the
        input synchronization. All boards are supplied with the standard set of these settings.

        :param SyncInFlags: Input synchronization flags. This is a bit mask for bitwise operations.
        :type SyncInFlags: libximc.highlevel.SyncInFlags
        :param ClutterTime: Input synchronization pulse dead time (us).
        :type ClutterTime: int
        :param Position: Desired position or shift.
        :type Position: float
        :param Speed: Target speed.
        :type Speed: float
        """
        self.SyncInFlags = SyncInFlags
        self.ClutterTime = ClutterTime
        self.Position = Position
        self.Speed = Speed

    # getters
    @property
    def SyncInFlags(self) -> flag_enumerations.SyncInFlags:
        return self._SyncInFlags

    @property
    def ClutterTime(self) -> int:
        return self._ClutterTime

    @property
    def Position(self) -> float:
        return self._Position

    @property
    def Speed(self) -> float:
        return self._Speed

    # setters
    @SyncInFlags.setter
    def SyncInFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._SyncInFlags = flag_enumerations.SyncInFlags(val)
        except Exception:
            raise ValueError("SyncInFlags = {} cannot be decomposed into {}.SyncInFlags' flags!"
                             .format(hex(val), __package__))

    @ClutterTime.setter
    def ClutterTime(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="ClutterTime")
        self._ClutterTime = val

    @Position.setter
    def Position(self, val):
        _check_noncontainer_castability(val, c_float, varname="Position")
        self._Position = val

    @Speed.setter
    def Speed(self, val):
        _check_noncontainer_castability(val, c_float, varname="Speed")
        self._Speed = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class sync_out_settings_t:
    def __init__(
            self,
            SyncOutFlags: flag_enumerations.SyncOutFlags = NOT_INITIALIZED,
            SyncOutPulseSteps: int = NOT_INITIALIZED,
            SyncOutPeriod: int = NOT_INITIALIZED,
            Accuracy: int = NOT_INITIALIZED,
            uAccuracy: int = NOT_INITIALIZED):
        """Synchronization settings.

        This structure contains all synchronization settings, modes, periods and flags. It specifies the behavior of
        the output synchronization. All boards are supplied with the standard set of these settings.

        :param SyncOutFlags: Output synchronization flags. This is a bit mask for bitwise operations.
        :type SyncOutFlags: libximc.highlevel.SyncOutFlags
        :param SyncOutPulseSteps: This value specifies the duration of output pulse. It is measured microseconds when
            SYNCOUT_IN_STEPS flag is cleared or in encoder pulses or motor steps when SYNCOUT_IN_STEPS is set.
        :type SyncOutPulseSteps: int
        :param SyncOutPeriod: This value specifies the number of encoder pulses or steps between two output
            synchronization pulses when SYNCOUT_ONPERIOD is set.
        :type SyncOutPeriod: int
        :param Accuracy: This is the neighborhood around the target coordinates, every point in which is treated as the
            target position. Getting in these points cause the stop impulse.
        :type Accuracy: int
        :param uAccuracy: This is the neighborhood around the target coordinates in microsteps (used with a stepper
            motor only). The microstep size and the range of valid values for this field depend on the selected step
            division mode (see the MicrostepMode field in engine_settings).
        :type uAccuracy: int
        """
        self.SyncOutFlags = SyncOutFlags
        self.SyncOutPulseSteps = SyncOutPulseSteps
        self.SyncOutPeriod = SyncOutPeriod
        self.Accuracy = Accuracy
        self.uAccuracy = uAccuracy

    # getters
    @property
    def SyncOutFlags(self) -> flag_enumerations.SyncOutFlags:
        return self._SyncOutFlags

    @property
    def SyncOutPulseSteps(self) -> int:
        return self._SyncOutPulseSteps

    @property
    def SyncOutPeriod(self) -> int:
        return self._SyncOutPeriod

    @property
    def Accuracy(self) -> int:
        return self._Accuracy

    @property
    def uAccuracy(self) -> int:
        return self._uAccuracy

    # setters
    @SyncOutFlags.setter
    def SyncOutFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._SyncOutFlags = flag_enumerations.SyncOutFlags(val)
        except Exception:
            raise ValueError("SyncOutFlags = {} cannot be decomposed into {}.SyncOutFlags' flags!"
                             .format(hex(val), __package__))

    @SyncOutPulseSteps.setter
    def SyncOutPulseSteps(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="SyncOutPulseSteps")
        self._SyncOutPulseSteps = val

    @SyncOutPeriod.setter
    def SyncOutPeriod(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="SyncOutPeriod")
        self._SyncOutPeriod = val

    @Accuracy.setter
    def Accuracy(self, val):
        _check_noncontainer_castability(val, c_uint32, varname="Accuracy")
        self._Accuracy = val

    @uAccuracy.setter
    def uAccuracy(self, val):
        _check_noncontainer_castability(val, c_uint8, varname="uAccuracy")
        self._uAccuracy = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class sync_out_settings_calb_t:
    def __init__(
            self,
            SyncOutFlags: flag_enumerations.SyncOutFlags = NOT_INITIALIZED,
            SyncOutPulseSteps: int = NOT_INITIALIZED,
            SyncOutPeriod: int = NOT_INITIALIZED,
            Accuracy: float = NOT_INITIALIZED):
        """Synchronization settings which use user units.

        This structure contains all synchronization settings, modes, periods and flags. It specifies the behavior of
        the output synchronization. All boards are supplied with the standard set of these settings.

        :param SyncOutFlags: Output synchronization flags. This is a bit mask for bitwise operations.
        :type SyncOutFlags: libximc.highlevel.SyncOutFlags
        :param SyncOutPulseSteps: This value specifies the duration of output pulse. It is measured microseconds when
            SYNCOUT_IN_STEPS flag is cleared or in encoder pulses or motor steps when SYNCOUT_IN_STEPS is set.
        :type SyncOutPulseSteps: int
        :param SyncOutPeriod: This value specifies the number of encoder pulses or steps between two output
            synchronization pulses when SYNCOUT_ONPERIOD is set.
        :type SyncOutPeriod: int
        :param Accuracy: This is the neighborhood around the target coordinates, every point in which is treated as the
            target position. Getting in these points cause the stop impulse.
        :type Accuracy: float
        """
        self.SyncOutFlags = SyncOutFlags
        self.SyncOutPulseSteps = SyncOutPulseSteps
        self.SyncOutPeriod = SyncOutPeriod
        self.Accuracy = Accuracy

    # getters
    @property
    def SyncOutFlags(self) -> flag_enumerations.SyncOutFlags:
        return self._SyncOutFlags

    @property
    def SyncOutPulseSteps(self) -> int:
        return self._SyncOutPulseSteps

    @property
    def SyncOutPeriod(self) -> int:
        return self._SyncOutPeriod

    @property
    def Accuracy(self) -> float:
        return self._Accuracy

    # setters
    @SyncOutFlags.setter
    def SyncOutFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._SyncOutFlags = flag_enumerations.SyncOutFlags(val)
        except Exception:
            raise ValueError("SyncOutFlags = {} cannot be decomposed into {}.SyncOutFlags' flags!"
                             .format(hex(val), __package__))

    @SyncOutPulseSteps.setter
    def SyncOutPulseSteps(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="SyncOutPulseSteps")
        self._SyncOutPulseSteps = val

    @SyncOutPeriod.setter
    def SyncOutPeriod(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="SyncOutPeriod")
        self._SyncOutPeriod = val

    @Accuracy.setter
    def Accuracy(self, val):
        _check_noncontainer_castability(val, c_float, varname="Accuracy")
        self._Accuracy = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class extio_settings_t:
    def __init__(
            self,
            EXTIOSetupFlags: flag_enumerations.ExtioSetupFlags = NOT_INITIALIZED,
            EXTIOModeFlags: flag_enumerations.ExtioModeFlags = NOT_INITIALIZED):
        """EXTIO settings.

        This structure contains all EXTIO settings. By default, input events are signaled through a rising front, and
        output states are signaled by a high logic state.

        :param EXTIOSetupFlags: Configuration flags of the external I-O. This is a bit mask for bitwise operations.
        :type EXTIOSetupFlags: libximc.highlevel.ExtioSetupFlags
        :param EXTIOModeFlags: Flags mode settings external I-O. This is a bit mask for bitwise operations.
        :type EXTIOModeFlags: libximc.highlevel.ExtioModeFlags
        """
        self.EXTIOSetupFlags = EXTIOSetupFlags
        self.EXTIOModeFlags = EXTIOModeFlags

    # getters
    @property
    def EXTIOSetupFlags(self) -> flag_enumerations.ExtioSetupFlags:
        return self._EXTIOSetupFlags

    @property
    def EXTIOModeFlags(self) -> flag_enumerations.ExtioModeFlags:
        return self._EXTIOModeFlags

    # setters
    @EXTIOSetupFlags.setter
    def EXTIOSetupFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._EXTIOSetupFlags = flag_enumerations.ExtioSetupFlags(val)
        except Exception:
            raise ValueError("EXTIOSetupFlags = {} cannot be decomposed into {}.ExtioSetupFlags' flags!"
                             .format(hex(val), __package__))

    @EXTIOModeFlags.setter
    def EXTIOModeFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._EXTIOModeFlags = flag_enumerations.ExtioModeFlags(val)
        except Exception:
            raise ValueError("EXTIOModeFlags = {} cannot be decomposed into {}.ExtioModeFlags' flags!"
                             .format(hex(val), __package__))

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class brake_settings_t:
    def __init__(
            self,
            t1: int = NOT_INITIALIZED,
            t2: int = NOT_INITIALIZED,
            t3: int = NOT_INITIALIZED,
            t4: int = NOT_INITIALIZED,
            BrakeFlags: flag_enumerations.BrakeFlags = NOT_INITIALIZED):
        """Brake settings.

        This structure contains brake control parameters.

        :param t1: Time in ms between turning on motor power and turning off the brake.
        :type t1: int
        :param t2: Time in ms between the brake turning off and moving readiness. All moving commands will execute
            after this interval.
        :type t2: int
        :param t3: Time in ms between motor stop and the brake turning on.
        :type t3: int
        :param t4: Time in ms between turning on the brake and turning off motor power.
        :type t4: int
        :param BrakeFlags: Flags. This is a bit mask for bitwise operations.
        :type BrakeFlags: libximc.highlevel.BrakeFlags
        """
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.t4 = t4
        self.BrakeFlags = BrakeFlags

    # getters
    @property
    def t1(self) -> int:
        return self._t1

    @property
    def t2(self) -> int:
        return self._t2

    @property
    def t3(self) -> int:
        return self._t3

    @property
    def t4(self) -> int:
        return self._t4

    @property
    def BrakeFlags(self) -> flag_enumerations.BrakeFlags:
        return self._BrakeFlags

    # setters
    @t1.setter
    def t1(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="t1")
        self._t1 = val

    @t2.setter
    def t2(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="t2")
        self._t2 = val

    @t3.setter
    def t3(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="t3")
        self._t3 = val

    @t4.setter
    def t4(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="t4")
        self._t4 = val

    @BrakeFlags.setter
    def BrakeFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._BrakeFlags = flag_enumerations.BrakeFlags(val)
        except Exception:
            raise ValueError("BraleFlags = {} cannot be decomposed into {}.BrakeFlags' flags!"
                             .format(hex(val), __package__))

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class control_settings_t:
    def __init__(
            self,
            MaxSpeed: 'list[int]' = NOT_INITIALIZED,
            uMaxSpeed: 'list[int]' = NOT_INITIALIZED,
            Timeout: 'list[int]' = NOT_INITIALIZED,
            MaxClickTime: int = NOT_INITIALIZED,
            Flags: flag_enumerations.ControlFlags = NOT_INITIALIZED,
            DeltaPosition: int = NOT_INITIALIZED,
            uDeltaPosition: int = NOT_INITIALIZED):
        """Control settings.

        This structure contains control parameters.

        In case of CTL_MODE=1, the joystick motor control is enabled. In this mode, while the joystick is maximally
        displaced, the engine tends to move at MaxSpeed[i]. i=0 if another value hasn't been set at the previous usage.
        To change the speed index "i", use the buttons.

        In case of CTL_MODE=2, the motor is controlled by the left/right buttons. When you click on the button, the
        motor starts moving in the appropriate direction at a speed MaxSpeed[0]. After Timeout[i], motor moves at speed
        MaxSpeed[i+1]. At the transition between MaxSpeed[i] and MaxSpeed[i+1] the motor just accelerates/decelerates
        as usual.

        :param MaxSpeed: Array of speeds (full step) used with the joystick and the button control. Range: 0..100000.
        :type MaxSpeed: list[int]
        :param uMaxSpeed: Array of speeds (in microsteps) used with the joystick and the button control. The microstep
            size and the range of valid values for this field depend on the selected step division mode (see the
            MicrostepMode field in engine_settings).
        :type uMaxSpeed: list[int]
        :param Timeout: Timeout[i] is timeout in ms. After that, max_speed[i+1] is applied. It's used with the button
            control only.
        :type Timeout: list[int]
        :param MaxClickTime: Maximum click time (in ms). Until the expiration of this time, the first speed isn't
            applied.
        :type MaxClickTime: int
        :param Flags: Control flags. This is a bit mask for bitwise operations.
        :type Flags: libximc.highlevel.ControlFlags
        :param DeltaPosition: Position shift (delta) (full step)
        :type DeltaPosition: int
        :param uDeltaPosition: Fractional part of the shift in micro steps. It's used with a stepper motor only. The
            microstep size and the range of valid values for this field depend on the selected step division mode (see
            the MicrostepMode field in engine_settings).
        :type uDeltaPosition: int
        """
        self.MaxSpeed = MaxSpeed
        self.uMaxSpeed = uMaxSpeed
        self.Timeout = Timeout
        self.MaxClickTime = MaxClickTime
        self.Flags = Flags
        self.DeltaPosition = DeltaPosition
        self.uDeltaPosition = uDeltaPosition

    # getters
    @property
    def MaxSpeed(self) -> 'list[int]':
        return self._MaxSpeed

    @property
    def uMaxSpeed(self) -> 'list[int]':
        return self._uMaxSpeed

    @property
    def Timeout(self) -> 'list[int]':
        return self._Timeout

    @property
    def MaxClickTime(self) -> int:
        return self._MaxClickTime

    @property
    def Flags(self) -> flag_enumerations.ControlFlags:
        return self._Flags

    @property
    def DeltaPosition(self) -> int:
        return self._DeltaPosition

    @property
    def uDeltaPosition(self) -> int:
        return self._uDeltaPosition

    # setters
    @MaxSpeed.setter
    def MaxSpeed(self, val):
        _check_container_castability(val, c_uint32, 10, strictly_equal=True, container_name="MaxSpeed")
        self._MaxSpeed = val

    @uMaxSpeed.setter
    def uMaxSpeed(self, val):
        _check_container_castability(val, c_uint8, 10, strictly_equal=True, container_name="uMaxSpeed")
        self._uMaxSpeed = val

    @Timeout.setter
    def Timeout(self, val):
        _check_container_castability(val, c_uint16, 9, strictly_equal=True, container_name="Timeout")
        self._Timeout = val

    @MaxClickTime.setter
    def MaxClickTime(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="MaxClickTime")
        self._MaxClickTime = val

    @Flags.setter
    def Flags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._Flags = flag_enumerations.ControlFlags(val)
        except Exception:
            raise ValueError("Flags = {} cannot be decomposed into {}.ControlFlags' flags!"
                             .format(hex(val), __package__))

    @DeltaPosition.setter
    def DeltaPosition(self, val):
        _check_noncontainer_castability(val, c_int32, varname="DeltaPosition")
        self._DeltaPosition = val

    @uDeltaPosition.setter
    def uDeltaPosition(self, val):
        _check_noncontainer_castability(val, c_int16, varname="uDeltaPosition")
        self._uDeltaPosition = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class control_settings_calb_t:
    def __init__(
            self,
            MaxSpeed: 'list[float]' = NOT_INITIALIZED,
            Timeout: 'list[int]' = NOT_INITIALIZED,
            MaxClickTime: int = NOT_INITIALIZED,
            Flags: flag_enumerations.ControlFlags = NOT_INITIALIZED,
            DeltaPosition: float = NOT_INITIALIZED):
        """Control settings which use user units.

        This structure contains control parameters.

        In case of CTL_MODE=1, the joystick motor control is enabled. In this mode, while the joystick is maximally
        displaced, the engine tends to move at MaxSpeed[i]. i=0 if another value hasn't been set at the previous usage.
        To change the speed index "i", use the buttons.

        In case of CTL_MODE=2, the motor is controlled by the left/right buttons. When you click on the button, the
        motor starts moving in the appropriate direction at a speed MaxSpeed[0]. After Timeout[i], the motor moves at
        speed MaxSpeed[i+1]. At the transition between MaxSpeed[i] and MaxSpeed[i+1] the motor just
        accelerates/decelerates as usual.

        :param MaxSpeed: Array of speeds used with the joystick and the button control.
        :type MaxSpeed: list[float]
        :param Timeout: Timeout[i] is timeout in ms. After that, max_speed[i+1] is applied. It's used with the button
            control only.
        :type Timeout: list[int]
        :param MaxClickTime: Maximum click time (in ms). Until the expiration of this time, the first speed isn't
            applied.
        :type MaxClickTime: int
        :param Flags: Control flags. This is a bit mask for bitwise operations.
        :type Flags: libximc.highlevel.ControlFlags
        :param DeltaPosition: Position shift (delta)
        :type DeltaPosition: float
        """
        self.MaxSpeed = MaxSpeed
        self.Timeout = Timeout
        self.MaxClickTime = MaxClickTime
        self.Flags = Flags
        self.DeltaPosition = DeltaPosition

    # getters
    @property
    def MaxSpeed(self) -> 'list[float]':
        return self._MaxSpeed

    @property
    def Timeout(self) -> 'list[int]':
        return self._Timeout

    @property
    def MaxClickTime(self) -> int:
        return self._MaxClickTime

    @property
    def Flags(self) -> flag_enumerations.ControlFlags:
        return self._Flags

    @property
    def DeltaPosition(self) -> float:
        return self._DeltaPosition

    # setters
    @MaxSpeed.setter
    def MaxSpeed(self, val):
        _check_container_castability(val, c_float, 10, strictly_equal=False, container_name="MaxSpeed")
        self._MaxSpeed = val

    @Timeout.setter
    def Timeout(self, val):
        _check_container_castability(val, c_uint16, 9, strictly_equal=False, container_name="Timeout")
        self._Timeout = val

    @MaxClickTime.setter
    def MaxClickTime(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="MaxClickTime")
        self._MaxClickTime = val

    @Flags.setter
    def Flags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._Flags = flag_enumerations.ControlFlags(val)
        except Exception:
            raise ValueError("Flags = {} cannot be decomposed into {}.ControlFlags' flags!"
                             .format(hex(val), __package__))

    @DeltaPosition.setter
    def DeltaPosition(self, val):
        _check_noncontainer_castability(val, c_float, varname="DeltaPosition")
        self._DeltaPosition = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class joystick_settings_t:
    def __init__(
            self,
            JoyLowEnd: int = NOT_INITIALIZED,
            JoyCenter: int = NOT_INITIALIZED,
            JoyHighEnd: int = NOT_INITIALIZED,
            ExpFactor: int = NOT_INITIALIZED,
            DeadZone: int = NOT_INITIALIZED,
            JoyFlags: flag_enumerations.JoyFlags = NOT_INITIALIZED):
        """Joystick settings.

        This structure contains joystick parameters. If joystick position falls outside the DeadZone limits, a movement
        begins. Speed is defined by the joystick position in the range of the DeadZone limit to the maximum deviation.
        Joystick positions inside the DeadZone limits correspond to zero speed (a soft stop of the motion), and
        positions beyond the Low and High limits correspond to MaxSpeed[i] or -MaxSpeed[i] (see command SCTL), where
        i = 0 by default and can be changed with left/right buttons (see command SCTL). If the next speed in the list
        is zero (both integer and microstep parts), the button press is ignored. The first speed in the list shouldn't
        be zero.

        The relationship between the deviation and the rate is exponential, which allows for high mobility and accuracy
        without speed mode switching.

        :param JoyLowEnd: Joystick lower end position. Range: 0..10000.
        :type JoyLowEnd: int
        :param JoyCenter: Joystick center position. Range: 0..10000.
        :type JoyCenter: int
        :param JoyHighEnd: Joystick upper end position. Range: 0..10000.
        :type JoyHighEnd: int
        :param ExpFactor: Exponential nonlinearity factor.
        :type ExpFactor: int
        :param DeadZone: Joystick dead zone.
        :type DeadZone: int
        :param JoyFlags: Joystick control flags. This is a bit mask for bitwise operations.
        :type JoyFlags: libximc.highlevel.JoyFlags
        """
        self.JoyLowEnd = JoyLowEnd
        self.JoyCenter = JoyCenter
        self.JoyHighEnd = JoyHighEnd
        self.ExpFactor = ExpFactor
        self.DeadZone = DeadZone
        self.JoyFlags = JoyFlags

    # getters
    @property
    def JoyLowEnd(self) -> int:
        return self._JoyLowEnd

    @property
    def JoyCenter(self) -> int:
        return self._JoyCenter

    @property
    def JoyHighEnd(self) -> int:
        return self._JoyHighEnd

    @property
    def ExpFactor(self) -> int:
        return self._ExpFactor

    @property
    def DeadZone(self) -> int:
        return self._DeadZone

    @property
    def JoyFlags(self) -> flag_enumerations.JoyFlags:
        return self._JoyFlags

    # setters
    @JoyLowEnd.setter
    def JoyLowEnd(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="JoyLowEnd")
        self._JoyLowEnd = val

    @JoyCenter.setter
    def JoyCenter(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="JoyCenter")
        self._JoyCenter = val

    @JoyHighEnd.setter
    def JoyHighEnd(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="JoyHighEnd")
        self._JoyHighEnd = val

    @ExpFactor.setter
    def ExpFactor(self, val):
        _check_noncontainer_castability(val, c_uint8, varname="ExpFactor")
        self._ExpFactor = val

    @DeadZone.setter
    def DeadZone(self, val):
        _check_noncontainer_castability(val, c_uint8, varname="DeadZone")
        self._DeadZone = val

    @JoyFlags.setter
    def JoyFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._JoyFlags = flag_enumerations.JoyFlags(val)
        except Exception:
            raise ValueError("JoyFlags = {} cannot be decomposed into {}.JoyFlags' flags!"
                             .format(hex(val), __package__))

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class ctp_settings_t:
    def __init__(
            self,
            CTPMinError: int = NOT_INITIALIZED,
            CTPFlags: flag_enumerations.CtpFlags = NOT_INITIALIZED):
        """Control position settings (used with stepper motor only)

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

        :param CTPMinError: The minimum difference between the SM position in steps and the encoder position that
            causes the setting of the STATE_CTP_ERROR flag. Measured in steps.
        :type CTPMinError: int
        :param CTPFlags: This is a bit mask for bitwise operations.
        :type CTPFlags: libximc.highlevel.CtpFlags
        """
        self.CTPMinError = CTPMinError
        self.CTPFlags = CTPFlags

    # getters
    @property
    def CTPMinError(self) -> int:
        return self._CTPMinError

    @property
    def CTPFlags(self) -> flag_enumerations.CtpFlags:
        return self._CTPFlags

    # setters
    @CTPMinError.setter
    def CTPMinError(self, val):
        _check_noncontainer_castability(val, c_uint8, varname="CTPMinError")
        self._CTPMinError = val

    @CTPFlags.setter
    def CTPFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._CTPFlags = flag_enumerations.CtpFlags(val)
        except Exception:
            raise ValueError("CTPFlags = {} cannot be decomposed into {}.CtpFlags' flags!"
                             .format(hex(val), __package__))

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class uart_settings_t:
    def __init__(
            self,
            Speed: int = NOT_INITIALIZED,
            UARTSetupFlags: flag_enumerations.UARTSetupFlags = NOT_INITIALIZED):
        """UART settings.

        This structure contains UART settings.

        :param Speed: UART speed (in bauds)
        :type Speed: int
        :param UARTSetupFlags: UART setup flags. This is a bit mask for bitwise operations.
        :type UARTSetupFlags: libximc.highlevel.UARTSetupFlags
        """
        self.Speed = Speed
        self.UARTSetupFlags = UARTSetupFlags

    # getters
    @property
    def Speed(self) -> int:
        return self._Speed

    @property
    def UARTSetupFlags(self) -> flag_enumerations.UARTSetupFlags:
        return self._UARTSetupFlags

    # setters
    @Speed.setter
    def Speed(self, val):
        _check_noncontainer_castability(val, c_uint32, varname="Speed")
        self._Speed = val

    @UARTSetupFlags.setter
    def UARTSetupFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._UARTSetupFlags = flag_enumerations.UARTSetupFlags(val)
        except Exception:
            raise ValueError("UARTSetupFlags = {} cannot be decomposed into {}.UARTSetupFlags' flags!"
                             .format(hex(val), __package__))

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class controller_name_t:
    def __init__(self,
                 ControllerName: str = NOT_INITIALIZED,
                 CtrlFlags: flag_enumerations.ControllerFlags = NOT_INITIALIZED):
        """Controller name and settings flags

        :param ControllerName: User controller name. It may be set by the user. Max string length: 16 characters.
        :type ControllerName: str
        :param CtrlFlags: Internal controller settings. This is a bit mask for bitwise operations.
        :type CtrlFlags: libximc.highlevel.ControllerFlags
        """
        self.ControllerName = ControllerName
        self.CtrlFlags = CtrlFlags

    # getters
    @property
    def ControllerName(self) -> str:
        return self._ControllerName

    @property
    def CtrlFlags(self) -> flag_enumerations.ControllerFlags:
        return self._CtrlFlags

    # setters
    @ControllerName.setter
    def ControllerName(self, val):
        _check_container_castability(val, c_char, 16, False, "ControllerName")
        self._ControllerName = val

    @CtrlFlags.setter
    def CtrlFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._CtrlFlags = flag_enumerations.ControllerFlags(val)
        except Exception:
            raise ValueError("CtrlFlags = {} cannot be decomposed into {}.ControllerFlags' flags!"
                             .format(hex(val), __package__))

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class nonvolatile_memory_t:
    def __init__(self, UserData: 'list[int]' = NOT_INITIALIZED):
        """Structure contains user data to save into the FRAM.

        :param UserData: User data. It may be set by the user. Each element of the list stores only 32 bits of user
            data. The maximum length is 7. Integers must be positive.
        :type UserData: list[int]
        """
        self.UserData = UserData

    # getters
    @property
    def UserData(self) -> 'list[int]':
        return self._UserData

    # setters
    @UserData.setter
    def UserData(self, val):
        _check_container_castability(val, c_uint32, 7, False, "UserData")
        self._UserData = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class emf_settings_t:
    def __init__(self,
                 L: float = NOT_INITIALIZED,
                 R: float = NOT_INITIALIZED,
                 Km: float = NOT_INITIALIZED,
                 BackEMFFlags: flag_enumerations.BackEMFFlags = NOT_INITIALIZED):
        """EMF settings.

        This structure contains the data for Electromechanical characteristics (EMF) of the motor. It determines the
        inductance, resistance, and Electromechanical coefficient of the motor. This data is stored in the flash memory
        of the controller. Please set new settings when you change the motor. Remember that improper EMF settings may
        damage the equipment.

        :param L: Motor winding inductance.
        :type L: float
        :param R: Motor winding resistance.
        :type R: float
        :param Km: Electromechanical ratio of the motor.
        :type Km: float
        :param BackEMFFlags: Flags of auto-detection of characteristics of windings of the engine.
        :type BackEMFFlags: libximc.highlevel.BackEMFFlags
        """
        self.L = L
        self.R = R
        self.Km = Km
        self.BackEMFFlags = BackEMFFlags

    # getters
    @property
    def L(self) -> float:
        return self._L

    @property
    def R(self) -> float:
        return self._R

    @property
    def Km(self) -> float:
        return self._Km

    @property
    def BackEMFFlags(self) -> flag_enumerations.BackEMFFlags:
        return self._BackEMFFlags

    # setters
    @L.setter
    def L(self, val):
        _check_noncontainer_castability(val, c_float, varname="L")
        self._L = val

    @R.setter
    def R(self, val):
        _check_noncontainer_castability(val, c_float, varname="R")
        self._R = val

    @Km.setter
    def Km(self, val):
        _check_noncontainer_castability(val, c_float, varname="Km")
        self._Km = val

    @BackEMFFlags.setter
    def BackEMFFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._BackEMFFlags = flag_enumerations.BackEMFFlags(val)
        except Exception:
            raise ValueError("BackEMFFlags = {} cannot be decomposed into {}.BackEMFFlags' flags!"
                             .format(hex(val), __package__))

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


# Legacy
class engine_advansed_setup_t:
    def __init__(
            self,
            stepcloseloop_Kw: int = NOT_INITIALIZED,
            stepcloseloop_Kp_low: int = NOT_INITIALIZED,
            stepcloseloop_Kp_high: int = NOT_INITIALIZED):
        """EAS settings.

        This structure is intended for setting parameters of algorithms that cannot be attributed to standard Kp, Ki,
        Kd, and L, R, Km.

        :param stepcloseloop_Kw: Mixing ratio of the actual and set speed, range [0, 100], default value 50.
        :type stepcloseloop_Kw: int
        :param stepcloseloop_Kp_low: Position feedback in the low-speed zone, range [0, 65535], default value 1000.
        :type stepcloseloop_Kp_low: int
        :param stepcloseloop_Kp_high: Position feedback in the high-speed zone, range [0, 65535], default value 33.
        :type stepcloseloop_Kp_high: int
        """
        self.stepcloseloop_Kw = stepcloseloop_Kw
        self.stepcloseloop_Kp_low = stepcloseloop_Kp_low
        self.stepcloseloop_Kp_high = stepcloseloop_Kp_high

    # getters
    @property
    def stepcloseloop_Kw(self) -> int:
        return self._stepcloseloop_Kw

    @property
    def stepcloseloop_Kp_low(self) -> int:
        return self._stepcloseloop_Kp_low

    @property
    def stepcloseloop_Kp_high(self) -> int:
        return self._stepcloseloop_Kp_high

    # setters
    @stepcloseloop_Kw.setter
    def stepcloseloop_Kw(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="stepcloseloop_Kw")
        self._stepcloseloop_Kw = val

    @stepcloseloop_Kp_low.setter
    def stepcloseloop_Kp_low(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="stepcloseloop_Kp_low")
        self._stepcloseloop_Kp_low = val

    @stepcloseloop_Kp_high.setter
    def stepcloseloop_Kp_high(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="stepcloseloop_Kp_high")
        self._stepcloseloop_Kp_high = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class engine_advanced_setup_t(engine_advansed_setup_t):
    pass


class get_position_t:
    def __init__(self,
                 Position: int = NOT_INITIALIZED,
                 uPosition: int = NOT_INITIALIZED,
                 EncPosition: int = NOT_INITIALIZED):
        """Position information.

        A useful structure that contains position value in steps and microsteps for stepper motor and encoder steps for
        all engines.

        :param Position: The position of the whole steps in the engine
        :type Position: int
        :param uPosition: Microstep position is only used with stepper motors. Microstep size and the range of valid
            values for this field depend on the selected step division mode (see MicrostepMode field in
            engine_settings).
        :type uPosition: int
        :param EncPosition: Encoder position.
        :type EncPosition: int
        """
        self.Position = Position
        self.uPosition = uPosition
        self.EncPosition = EncPosition

    # getters
    @property
    def Position(self) -> int:
        return self._Position

    @property
    def uPosition(self) -> int:
        return self._uPosition

    @property
    def EncPosition(self) -> int:
        return self._EncPosition

    # setters
    @Position.setter
    def Position(self, val):
        _check_noncontainer_castability(val, c_int32, varname="Position")
        self._Position = val

    @uPosition.setter
    def uPosition(self, val):
        _check_noncontainer_castability(val, c_int16, varname="uPosition")
        self._uPosition = val

    @EncPosition.setter
    def EncPosition(self, val):
        _check_noncontainer_castability(val, c_longlong, varname="EncPosition")
        self._EncPosition = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class get_position_calb_t:
    def __init__(
            self,
            Position: float = NOT_INITIALIZED,
            EncPosition: int = NOT_INITIALIZED):
        """Position information.

        A useful structure that contains position value in user units for stepper motor and encoder steps for all
        engines.

        :param Position: The position in the engine. Corrected by the table.
        :type Position: float
        :param EncPosition: Encoder position.
        :type EncPosition: int
        """
        self.Position = Position
        self.EncPosition = EncPosition

    # getters
    @property
    def Position(self) -> float:
        return self._Position

    @property
    def EncPosition(self) -> int:
        return self._EncPosition

    # setters
    @Position.setter
    def Position(self, val):
        _check_noncontainer_castability(val, c_float, varname="Position")
        self._Position = val

    @EncPosition.setter
    def EncPosition(self, val):
        _check_noncontainer_castability(val, c_longlong, varname="EncPosition")
        self._EncPosition = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class set_position_t:
    def __init__(
            self,
            Position: int = NOT_INITIALIZED,
            uPosition: int = NOT_INITIALIZED,
            EncPosition: int = NOT_INITIALIZED,
            PosFlags: flag_enumerations.PositionFlags = NOT_INITIALIZED):
        """Position information.

        A useful structure that contains position value in steps and microsteps for stepper motor and encoder steps for
        all engines.

        :param Position: The position of the whole steps in the engine
        :type Position: int
        :param uPosition: Microstep position is only used with stepper motors. Microstep size and the range of valid
            values for this field depend on the selected step division mode (see the MicrostepMode field in
            engine_settings).
        :type uPosition: int
        :param EncPosition: Encoder position.
        :type EncPosition: int
        :param PosFlags: Position flags. This is a bit mask for bitwise operations.
        :type PosFlags: libximc.highlevel.PositionFlags
        """
        self.Position = Position
        self.uPosition = uPosition
        self.EncPosition = EncPosition
        self.PosFlags = PosFlags

    # getters
    @property
    def Position(self) -> int:
        return self._Position

    @property
    def uPosition(self) -> int:
        return self._uPosition

    @property
    def EncPosition(self) -> int:
        return self._EncPosition

    @property
    def PosFlags(self) -> flag_enumerations.PositionFlags:
        return self._PosFlags

    # setters
    @Position.setter
    def Position(self, val):
        _check_noncontainer_castability(val, c_int32, varname="Position")
        self._Position = val

    @uPosition.setter
    def uPosition(self, val):
        _check_noncontainer_castability(val, c_int16, varname="uPosition")
        self._uPosition = val

    @EncPosition.setter
    def EncPosition(self, val):
        _check_noncontainer_castability(val, c_longlong, varname="EncPosition")
        self._EncPosition = val

    @PosFlags.setter
    def PosFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._PosFlags = flag_enumerations.PositionFlags(val)
        except Exception:
            raise ValueError("PosFlags = {} cannot be decomposed into {}.PositionFlags' flags!"
                             .format(hex(val), __package__))

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class set_position_calb_t:
    def __init__(
            self,
            Position: float = NOT_INITIALIZED,
            EncPosition: int = NOT_INITIALIZED,
            PosFlags: flag_enumerations.PositionFlags = NOT_INITIALIZED):
        """User unit position information.

        A useful structure that contains position value in steps and microsteps for stepper motor and encoder steps of
        all engines.

        :param Position: The position in the engine.
        :type Position: float
        :param EncPosition: Encoder position.
        :type EncPosition: int
        :param PosFlags: Position flags. This is a bit mask for bitwise operations.
        :type PosFlags: libximc.highlevel.PositionFlags
        """
        self.Position = Position
        self.EncPosition = EncPosition
        self.PosFlags = PosFlags

    # getters
    @property
    def Position(self) -> float:
        return self._Position

    @property
    def EncPosition(self) -> int:
        return self._EncPosition

    @property
    def PosFlags(self) -> flag_enumerations.PositionFlags:
        return self._PosFlags

    # setters
    @Position.setter
    def Position(self, val):
        _check_noncontainer_castability(val, c_float, varname="Position")
        self._Position = val

    @EncPosition.setter
    def EncPosition(self, val):
        _check_noncontainer_castability(val, c_longlong, varname="EncPosition")
        self._EncPosition = val

    @PosFlags.setter
    def PosFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._PosFlags = flag_enumerations.PositionFlags(val)
        except Exception:
            raise ValueError("PosFlags = {} cannot be decomposed into {}.PositionFlags' flags!"
                             .format(hex(val), __package__))

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class status_t:
    def __init__(
            self,
            MoveSts: flag_enumerations.MoveState = NOT_INITIALIZED,
            MvCmdSts: flag_enumerations.MvcmdStatus = NOT_INITIALIZED,
            PWRSts: flag_enumerations.PowerState = NOT_INITIALIZED,
            EncSts: flag_enumerations.EncodeStatus = NOT_INITIALIZED,
            WindSts: flag_enumerations.WindStatus = NOT_INITIALIZED,
            CurPosition: int = NOT_INITIALIZED,
            uCurPosition: int = NOT_INITIALIZED,
            EncPosition: int = NOT_INITIALIZED,
            CurSpeed: int = NOT_INITIALIZED,
            uCurSpeed: int = NOT_INITIALIZED,
            Ipwr: int = NOT_INITIALIZED,
            Upwr: int = NOT_INITIALIZED,
            Iusb: int = NOT_INITIALIZED,
            Uusb: int = NOT_INITIALIZED,
            CurT: int = NOT_INITIALIZED,
            Flags: flag_enumerations.StateFlags = NOT_INITIALIZED,
            GPIOFlags: flag_enumerations.GPIOFlags = NOT_INITIALIZED,
            CmdBufFreeSpace: int = NOT_INITIALIZED):
        """Device state.

        A useful structure that contains current controller state, including speed, position, and boolean flags.

        :param MoveSts: Move state. This is a bit mask for bitwise operations.
        :type MoveSts: libximc.highlevel.MoveState
        :param MvCmdSts: Move command state. This is a bit mask for bitwise operations.
        :type MvCmdSts: libximc.highlevel.MvcmdStatus
        :param PWRSts: Power state of the stepper motor (used with stepper motor only). This is a bit mask for bitwise
            operations.
        :type PWRSts: libximc.highlevel.PowerState
        :param EncSts: Encoder state. This is a bit mask for bitwise operations.
        :type EncSts: libximc.highlevel.EncodeStatus
        :param WindSts: Windings state. This is a bit mask for bitwise operations.
        :type WindSts: libximc.highlevel.WindStatus
        :param CurPosition: Current position.
        :type CurPosition: int
        :param uCurPosition: Step motor shaft position in microsteps. The microstep size and the range of valid values
            for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings).
            Used with stepper motors only.
        :type uCurPosition: int
        :param EncPosition: Current encoder position.
        :type EncPosition: int
        :param CurSpeed: Motor shaft speed in steps/s or rpm.
        :type CurSpeed: int
        :param uCurSpeed: Fractional part of motor shaft speed in microsteps. The microstep size and the range of valid
            values for this field depend on the selected step division mode (see the MicrostepMode field in
            engine_settings). Used with stepper motors only.
        :type uCurSpeed: int
        :param Ipwr: Engine current, mA.
        :type Ipwr: int
        :param Upwr: Power supply voltage, tens of mV.
        :type Upwr: int
        :param Iusb: USB current, mA.
        :type Iusb: int
        :param Uusb: USB voltage, tens of mV.
        :type Uusb: int
        :param CurT: Temperature, tenths of degrees Celsius.
        :type CurT: int
        :param Flags: A set of flags specifies the motor shaft movement algorithm and a list of limitations. This is a
            bit mask for bitwise operations.
        :type Flags: libximc.highlevel.StateFlags
        :param GPIOFlags: A set of flags of GPIO states. This is a bit mask for bitwise operations.
        :type GPIOFlags: libximc.highlevel.GPIOFlags
        :param CmdBufFreeSpace: This field is a service field. It shows the number of free synchronization chain buffer
            cells.
        :type CmdBufFreeSpace: int
        """
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
    def MoveSts(self) -> flag_enumerations.MoveState:
        return self._MoveSts

    @property
    def MvCmdSts(self) -> flag_enumerations.MvcmdStatus:
        return self._MvCmdSts

    @property
    def PWRSts(self) -> flag_enumerations.PowerState:
        return self._PWRSts

    @property
    def EncSts(self) -> flag_enumerations.EncodeStatus:
        return self._EncSts

    @property
    def WindSts(self) -> flag_enumerations.WindStatus:
        return self._WindSts

    @property
    def CurPosition(self) -> int:
        return self._CurPosition

    @property
    def uCurPosition(self) -> int:
        return self._uCurPosition

    @property
    def EncPosition(self) -> int:
        return self._EncPosition

    @property
    def CurSpeed(self) -> int:
        return self._CurSpeed

    @property
    def uCurSpeed(self) -> int:
        return self._uCurSpeed

    @property
    def Ipwr(self) -> int:
        return self._Ipwr

    @property
    def Upwr(self) -> int:
        return self._Upwr

    @property
    def Iusb(self) -> int:
        return self._Iusb

    @property
    def Uusb(self) -> int:
        return self._Uusb

    @property
    def CurT(self) -> int:
        return self._CurT

    @property
    def Flags(self) -> flag_enumerations.StateFlags:
        return self._Flags

    @property
    def GPIOFlags(self) -> flag_enumerations.GPIOFlags:
        return self._GPIOFlags

    @property
    def CmdBufFreeSpace(self) -> int:
        return self._CmdBufFreeSpace

    # setters
    @MoveSts.setter
    def MoveSts(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._MoveSts = flag_enumerations.MoveState(val)
        except Exception:
            raise ValueError("MoveSts = {} cannot be decomposed into {}.MoveState's flags!"
                             .format(hex(val), __package__))

    @MvCmdSts.setter
    def MvCmdSts(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._MvCmdSts = flag_enumerations.MvcmdStatus(val)
        except Exception:
            raise ValueError("MvCmdSts = {} cannot be decomposed into {}.MvcmdStatus's flags!"
                             .format(hex(val), __package__))

    @PWRSts.setter
    def PWRSts(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._PWRSts = flag_enumerations.PowerState(val)
        except Exception:
            raise ValueError("PWRSts = {} cannot be decomposed into {}.PowerState's flags!"
                             .format(hex(val), __package__))

    @EncSts.setter
    def EncSts(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._EncSts = flag_enumerations.EncodeStatus(val)
        except Exception:
            raise ValueError("EncSts = {} cannot be decomposed into {}.EncodeStatus's flags!"
                             .format(hex(val), __package__))

    @WindSts.setter
    def WindSts(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._WindSts = flag_enumerations.WindStatus(val)
        except Exception:
            raise ValueError("WindSts = {} cannot be decomposed into {}.WindStatus's flags!")

    @CurPosition.setter
    def CurPosition(self, val):
        _check_noncontainer_castability(val, c_int32, varname="CurPosition")
        self._CurPosition = val

    @uCurPosition.setter
    def uCurPosition(self, val):
        _check_noncontainer_castability(val, c_int16, varname="uCurPosition")
        self._uCurPosition = val

    @EncPosition.setter
    def EncPosition(self, val):
        _check_noncontainer_castability(val, c_longlong, varname="EncPosition")
        self._EncPosition = val

    @CurSpeed.setter
    def CurSpeed(self, val):
        _check_noncontainer_castability(val, c_int32, varname="CurSpeed")
        self._CurSpeed = val

    @uCurSpeed.setter
    def uCurSpeed(self, val):
        _check_noncontainer_castability(val, c_int16, varname="uCurSpeed")
        self._uCurSpeed = val

    @Ipwr.setter
    def Ipwr(self, val):
        _check_noncontainer_castability(val, c_int16, varname="Ipwr")
        self._Ipwr = val

    @Upwr.setter
    def Upwr(self, val):
        _check_noncontainer_castability(val, c_int16, varname="Upwr")
        self._Upwr = val

    @Iusb.setter
    def Iusb(self, val):
        _check_noncontainer_castability(val, c_int16, varname="Iusb")
        self._Iusb = val

    @Uusb.setter
    def Uusb(self, val):
        _check_noncontainer_castability(val, c_int16, varname="Uusb")
        self._Uusb = val

    @CurT.setter
    def CurT(self, val):
        _check_noncontainer_castability(val, c_int16, varname="CurT")
        self._CurT = val

    @Flags.setter
    def Flags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._Flags = flag_enumerations.StateFlags(val)
        except Exception:
            raise ValueError("Flags = {} cannot be decomposed into {}.StateFlags' flags!"
                             .format(hex(val), __package__))

    @GPIOFlags.setter
    def GPIOFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._GPIOFlags = flag_enumerations.GPIOFlags(val)
        except Exception:
            raise ValueError("GPIOFlags = {} cannot be decomposed into {}.GPIOFlags' flags!"
                             .format(hex(val), __package__))

    @CmdBufFreeSpace.setter
    def CmdBufFreeSpace(self, val):
        _check_noncontainer_castability(val, c_uint8, varname="CmdBufFreeSpace")
        self._CmdBufFreeSpace = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class status_calb_t:
    def __init__(
            self,
            MoveSts: flag_enumerations.MoveState = NOT_INITIALIZED,
            MvCmdSts: flag_enumerations.MvcmdStatus = NOT_INITIALIZED,
            PWRSts: flag_enumerations.PowerState = NOT_INITIALIZED,
            EncSts: flag_enumerations.EncodeStatus = NOT_INITIALIZED,
            WindSts: flag_enumerations.WindStatus = NOT_INITIALIZED,
            CurPosition: float = NOT_INITIALIZED,
            EncPosition: int = NOT_INITIALIZED,
            CurSpeed: float = NOT_INITIALIZED,
            Ipwr: int = NOT_INITIALIZED,
            Upwr: int = NOT_INITIALIZED,
            Iusb: int = NOT_INITIALIZED,
            Uusb: int = NOT_INITIALIZED,
            CurT: int = NOT_INITIALIZED,
            Flags: flag_enumerations.StateFlags = NOT_INITIALIZED,
            GPIOFlags: flag_enumerations.GPIOFlags = NOT_INITIALIZED,
            CmdBufFreeSpace: int = NOT_INITIALIZED):
        """User unit device's state.

        A useful structure that contains current controller state, including speed, position, and boolean flags.

        :param MoveSts: Move state. This is a bit mask for bitwise operations.
        :type MoveSts: libximc.highlevel.MoveState
        :param MvCmdSts: Move command state. This is a bit mask for bitwise operations.
        :type MvCmdSts: libximc.highlevel.MvcmdStatus
        :param PWRSts: Power state of the stepper motor (used with stepper motor only). This is a bit mask for bitwise
            operations.
        :type PWRSts: libximc.highlevel.PowerState
        :param EncSts: Encoder state. This is a bit mask for bitwise operations.
        :type EncSts: libximc.highlevel.EncodeStatus
        :param WindSts: Windings state. This is a bit mask for bitwise operations.
        :type WindSts: libximc.highlevel.WindStatus
        :param CurPosition: Current position. Corrected by the table.
        :type CurPosition: float
        :param EncPosition: Current encoder position.
        :type EncPosition: int
        :param CurSpeed: Motor shaft speed.
        :type CurSpeed: float
        :param Ipwr: Engine current, mA.
        :type Ipwr: int
        :param Upwr: Power supply voltage, tens of mV.
        :type Upwr: int
        :param Iusb: USB current, mA.
        :type Iusb: int
        :param Uusb: USB voltage, tens of mV.
        :type Uusb: int
        :param CurT: Temperature, tenths of degrees Celsius.
        :type CurT: int
        :param Flags: A set of flags specifies the motor shaft movement algorithm and a list of limitations. This is a
            bit mask for bitwise operations.
        :type Flags: libximc.highlevel.StateFlags
        :param GPIOFlags: A set of flags of GPIO states. This is a bit mask for bitwise operations.
        :type GPIOFlags: libximc.highlevel.GPIOFlags
        :param CmdBufFreeSpace: This field is a service field. It shows the number of free synchronization chain buffer
            cells.
        :type CmdBufFreeSpace: int
        """
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
    def MoveSts(self) -> flag_enumerations.MoveState:
        return self._MoveSts

    @property
    def MvCmdSts(self) -> flag_enumerations.MvcmdStatus:
        return self._MvCmdSts

    @property
    def PWRSts(self) -> flag_enumerations.PowerState:
        return self._PWRSts

    @property
    def EncSts(self) -> flag_enumerations.EncodeStatus:
        return self._EncSts

    @property
    def WindSts(self) -> flag_enumerations.WindStatus:
        return self._WindSts

    @property
    def CurPosition(self) -> float:
        return self._CurPosition

    @property
    def EncPosition(self) -> int:
        return self._EncPosition

    @property
    def CurSpeed(self) -> float:
        return self._CurSpeed

    @property
    def Ipwr(self) -> int:
        return self._Ipwr

    @property
    def Upwr(self) -> int:
        return self._Upwr

    @property
    def Iusb(self) -> int:
        return self._Iusb

    @property
    def Uusb(self) -> int:
        return self._Uusb

    @property
    def CurT(self) -> int:
        return self._CurT

    @property
    def Flags(self) -> flag_enumerations.StateFlags:
        return self._Flags

    @property
    def GPIOFlags(self) -> flag_enumerations.GPIOFlags:
        return self._GPIOFlags

    @property
    def CmdBufFreeSpace(self) -> int:
        return self._CmdBufFreeSpace

    # setters
    @MoveSts.setter
    def MoveSts(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._MoveSts = flag_enumerations.MoveState(val)
        except Exception:
            raise ValueError("MoveSts = {} cannot be decomposed into {}.MoveState's flags!"
                             .format(hex(val), __package__))

    @MvCmdSts.setter
    def MvCmdSts(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._MvCmdSts = flag_enumerations.MvcmdStatus(val)
        except Exception:
            raise ValueError("MvCmdSts = {} cannot be decomposed into {}.MvcmdStatus's flags!"
                             .format(hex(val), __package__))

    @PWRSts.setter
    def PWRSts(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._PWRSts = flag_enumerations.PowerState(val)
        except Exception:
            raise ValueError("PWRSts = {} cannot be decomposed into {}.PowerState's flags!"
                             .format(hex(val), __package__))

    @EncSts.setter
    def EncSts(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._EncSts = flag_enumerations.EncodeStatus(val)
        except Exception:
            raise ValueError("EncSts = {} cannot be decomposed into {}.EncodeStatus's flags!"
                             .format(hex(val), __package__))

    @WindSts.setter
    def WindSts(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._WindSts = flag_enumerations.WindStatus(val)
        except Exception:
            raise ValueError("WindSts = {} cannot be decomposed into {}.WindStatus's flags!")

    @CurPosition.setter
    def CurPosition(self, val):
        _check_noncontainer_castability(val, c_float, varname="CurPosition")
        self._CurPosition = val

    @EncPosition.setter
    def EncPosition(self, val):
        _check_noncontainer_castability(val, c_longlong, varname="EncPosition")
        self._EncPosition = val

    @CurSpeed.setter
    def CurSpeed(self, val):
        _check_noncontainer_castability(val, c_float, varname="CurSpeed")
        self._CurSpeed = val

    @Ipwr.setter
    def Ipwr(self, val):
        _check_noncontainer_castability(val, c_int16, varname="Ipwr")
        self._Ipwr = val

    @Upwr.setter
    def Upwr(self, val):
        _check_noncontainer_castability(val, c_int16, varname="Upwr")
        self._Upwr = val

    @Iusb.setter
    def Iusb(self, val):
        _check_noncontainer_castability(val, c_int16, varname="Iusb")
        self._Iusb = val

    @Uusb.setter
    def Uusb(self, val):
        _check_noncontainer_castability(val, c_int16, varname="Uusb")
        self._Uusb = val

    @CurT.setter
    def CurT(self, val):
        _check_noncontainer_castability(val, c_int16, varname="CurT")
        self._CurT = val

    @Flags.setter
    def Flags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._Flags = flag_enumerations.StateFlags(val)
        except Exception:
            raise ValueError("Flags = {} cannot be decomposed into {}.StateFlags' flags!"
                             .format(hex(val), __package__))

    @GPIOFlags.setter
    def GPIOFlags(self, val):
        if val is NOT_INITIALIZED:
            return
        try:
            self._GPIOFlags = flag_enumerations.GPIOFlags(val)
        except Exception:
            raise ValueError("GPIOFlags = {} cannot be decomposed into {}.GPIOFlags' flags!"
                             .format(hex(val), __package__))

    @CmdBufFreeSpace.setter
    def CmdBufFreeSpace(self, val):
        _check_noncontainer_castability(val, c_uint8, varname="CmdBufFreeSpace")
        self._CmdBufFreeSpace = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class measurements_t:
    def __init__(self, Speed: 'list[int]', Error: 'list[int]', Length: int):
        """The buffer holds no more than 25 points. The exact length of the received buffer is stored in the Length
        field.

        :param Speed: Current speed in microsteps per second (whole steps are recalculated taking into account the
            current step division mode) or encoder counts per second.
        :type Speed: list[int]
        :param Error: Current error in microsteps per second (whole steps are recalculated taking into account the
            current step division mode) or encoder counts per second.
        :type Error: list[int]
        :param Length: Length of actual data in buffer.
        :type Length: int
        """
        self.Length = Length
        self.Speed = Speed
        self.Error = Error

    # getters
    @property
    def Speed(self) -> 'list[int]':
        return self._Speed

    @property
    def Error(self) -> 'list[int]':
        return self._Error

    @property
    def Length(self) -> int:
        return self._Length

    # setters
    @Speed.setter
    def Speed(self, val):
        _check_container_castability(val, c_int32, 25, False, "Speed")
        self._Speed = val[:self.Length] + [None] * (25 - self.Length)

    @Error.setter
    def Error(self, val):
        _check_container_castability(val, c_int32, 25, False, "Error")
        self._Error = val[:self.Length] + [None] * (25 - self.Length)

    @Length.setter
    def Length(self, val):
        _check_noncontainer_castability(val, c_uint32, varname="Length")
        self._Length = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class chart_data_t:
    def __init__(
            self,
            WindingVoltageA: int = NOT_INITIALIZED,
            WindingVoltageB: int = NOT_INITIALIZED,
            WindingVoltageC: int = NOT_INITIALIZED,
            WindingCurrentA: int = NOT_INITIALIZED,
            WindingCurrentB: int = NOT_INITIALIZED,
            WindingCurrentC: int = NOT_INITIALIZED,
            Pot: int = NOT_INITIALIZED,
            Joy: int = NOT_INITIALIZED,
            DutyCycle: int = NOT_INITIALIZED):
        """Additional device state.

        This structure contains additional values such as winding's voltages, currents and temperature.

        :param WindingVoltageA: In case of a step motor, it contains the voltage across the winding A (in tens of mV);
            in case of a brushless motor, it contains the voltage on the first coil; in case of a DC motor, it contains
            the only winding current.
        :type WindingVoltageA: int
        :param WindingVoltageB: In case of a step motor, it contains the voltage across the winding B (in tens of mV);
            in case of a brushless motor, it contains the voltage on the second winding; and in case of a DC motor,
            this field is not used.
        :type WindingVoltageB: int
        :param WindingVoltageC: In case of a brushless motor, it contains the voltage on the third winding (in tens of
            mV); in the case of a step motor and a DC motor, the field is not used.
        :type WindingVoltageC: int
        :param WindingCurrentA: In case of a step motor, it contains the current in the winding A (in mA); in case of a
            brushless motor, it contains the current in the winding A; and in case of a DC motor, it contains the only
            winding current.
        :type WindingCurrentA: int
        :param WindingCurrentB: In case of a step motor, it contains the current in the winding B (in mA); in case of a
            brushless motor, it contains the current in the winding B; and in case of a DC motor, the field is not used.
        :type WindingCurrentB: int
        :param WindingCurrentC: In case of a brushless motor, it contains the current in the winding C (in mA); in case
            of a step motor and a DC motor, the field is not used.
        :type WindingCurrentC: int
        :param Pot: Analog input value, dimensionless. Range: 0..10000
        :type Pot: int
        :param Joy: The joystick position, dimensionless. Range: 0..10000
        :type Joy: int
        :param DutyCycle: PWM duty cycle.
        :type DutyCycle: int
        """
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
    def WindingVoltageA(self) -> int:
        return self._WindingVoltageA

    @property
    def WindingVoltageB(self) -> int:
        return self._WindingVoltageB

    @property
    def WindingVoltageC(self) -> int:
        return self._WindingVoltageC

    @property
    def WindingCurrentA(self) -> int:
        return self._WindingCurrentA

    @property
    def WindingCurrentB(self) -> int:
        return self._WindingCurrentB

    @property
    def WindingCurrentC(self) -> int:
        return self._WindingCurrentC

    @property
    def Pot(self) -> int:
        return self._Pot

    @property
    def Joy(self) -> int:
        return self._Joy

    @property
    def DutyCycle(self) -> int:
        return self._DutyCycle

    # setters
    @WindingVoltageA.setter
    def WindingVoltageA(self, val):
        _check_noncontainer_castability(val, c_int16, varname="WindingVoltageA")
        self._WindingVoltageA = val

    @WindingVoltageB.setter
    def WindingVoltageB(self, val):
        _check_noncontainer_castability(val, c_int16, varname="WindingVoltageB")
        self._WindingVoltageB = val

    @WindingVoltageC.setter
    def WindingVoltageC(self, val):
        _check_noncontainer_castability(val, c_int16, varname="WindingVoltageC")
        self._WindingVoltageC = val

    @WindingCurrentA.setter
    def WindingCurrentA(self, val):
        _check_noncontainer_castability(val, c_int16, varname="WindingCurrentA")
        self._WindingCurrentA = val

    @WindingCurrentB.setter
    def WindingCurrentB(self, val):
        _check_noncontainer_castability(val, c_int16, varname="WindingCurrentB")
        self._WindingCurrentB = val

    @WindingCurrentC.setter
    def WindingCurrentC(self, val):
        _check_noncontainer_castability(val, c_int16, varname="WindingCurrentC")
        self._WindingCurrentC = val

    @Pot.setter
    def Pot(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="Pot")
        self._Pot = val

    @Joy.setter
    def Joy(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="Joy")
        self._Joy = val

    @DutyCycle.setter
    def DutyCycle(self, val):
        _check_noncontainer_castability(val, c_int16, varname="DutyCycle")
        self._DutyCycle = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class device_information_t:
    def __init__(
            self,
            Manufacturer: str,
            ManufacturerId: str,
            ProductDescription: str,
            Major: int,
            Minor: int,
            Release: int):
        """Controller information structure.

        :param Manufacturer: Manufacturer.
        :type Manufacturer: str
        :param ManufacturerId: Manufacturer id.
        :type ManufacturerId: str
        :param ProductDescription: Product description.
        :type ProductDescription: str
        :param Major: The major number of the hardware version.
        :type Major: int
        :param Minor: Minor number of the hardware version.
        :type Minor: int
        :param Release: Release version.
        :type Release: int
        """
        self.Manufacturer = Manufacturer
        self.ManufacturerId = ManufacturerId
        self.ProductDescription = ProductDescription
        self.Major = Major
        self.Minor = Minor
        self.Release = Release

    # getters
    @property
    def Manufacturer(self) -> str:
        return self._Manufacturer

    @property
    def ManufacturerId(self) -> str:
        return self._ManufacturerId

    @property
    def ProductDescription(self) -> str:
        return self._ProductDescription

    @property
    def Major(self) -> int:
        return self._Major

    @property
    def Minor(self) -> int:
        return self._Minor

    @property
    def Release(self) -> int:
        return self._Release

    # setters
    @Manufacturer.setter
    def Manufacturer(self, val):
        _check_container_castability(val, c_char, 4, False, "Manufacturer")
        self._Manufacturer = val

    @ManufacturerId.setter
    def ManufacturerId(self, val):
        _check_container_castability(val, c_char, 2, False, "ManufacturerId")
        self._ManufacturerId = val

    @ProductDescription.setter
    def ProductDescription(self, val):
        _check_container_castability(val, c_char, 8, False, "ProductDescription")
        self._ProductDescription = val

    @Major.setter
    def Major(self, val):
        _check_noncontainer_castability(val, c_uint8, varname="Major")
        self._Major = val

    @Minor.setter
    def Minor(self, val):
        _check_noncontainer_castability(val, c_uint8, varname="Minor")
        self._Minor = val

    @Release.setter
    def Release(self, val):
        _check_noncontainer_castability(val, c_uint16, varname="Release")
        self._Release = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result


class stage_name_t:
    def __init__(self, PositionerName: str = NOT_INITIALIZED):
        """Stage username.

        :param PositionerName: User's positioner name. It can be set by a user. Max string length: 16 characters.
        :type PositionerName: str
        """
        self.PositionerName = PositionerName

    # getters
    @property
    def PositionerName(self) -> str:
        return self._PositionerName

    # setters
    @PositionerName.setter
    def PositionerName(self, val: str):
        _check_container_castability(val, c_char, 16, False, "PositionerName")
        self._PositionerName = val

    def __repr__(self) -> str:
        result = ""
        for key_value_pair in self.__dict__.items():
            result += "{}: {}\n".format(key_value_pair[0][1:], key_value_pair[1])
        return result
