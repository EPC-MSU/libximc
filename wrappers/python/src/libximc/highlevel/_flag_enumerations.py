""" Python binding for libximc
=======================================================================================================================

file: flag_enumerations.py

Description: This file contains definitions of flag enumerations that are to be used as parameters of highlevel's
functions and Axis's methods.
"""
from enum import IntEnum, Flag


class StrictIntFlag(Flag):
    """An enumeration flag class that uses STRICT boundary for out-of-range bits (see enum docs).

    Unfortunately almost ideal enum.IntFlag uses EJECT boundary, i.e. all out-of-range bits will be
    kept in the class instance and no exception will be raised. That's why it's difficult to check
    whether a given value consists only of allowed flags or it has extra ones :_(

    E.g. MyInheritedFromIntFlagClass is a enumeration consisting of two flags: A=1 and B=2. Line
        my_super_instance = MyInheritedFromIntFlagClass(1000)
    won't rise any exception.

    So, let's inherit from ordinary enum.Flag which uses STRICT boundary. It will be extended by
    an __int__() method allowing us to make direct conversion into ctypes' integers.
    (direct == without .value attribute call).
    """
    def __int__(self):
        return self.value


class Result(IntEnum):
    Ok = 0
    Error = -1
    NotImplemented = -2
    ValueError = -3
    NoDevice = -4


class EnumerateFlags(Flag):
    ENUMERATE_PROBE = 0x01
    ENUMERATE_ALL_COM = 0x02
    ENUMERATE_NETWORK = 0x04


class MoveState(StrictIntFlag):
    MOVE_STATE_MOVING = 0x01
    MOVE_STATE_TARGET_SPEED = 0x02
    MOVE_STATE_ANTIPLAY = 0x04


class ControllerFlags(StrictIntFlag):
    EEPROM_PRECEDENCE = 0x01


class PowerState(StrictIntFlag):
    PWR_STATE_UNKNOWN = 0x00
    PWR_STATE_OFF = 0x01
    PWR_STATE_NORM = 0x03
    PWR_STATE_REDUCT = 0x04
    PWR_STATE_MAX = 0x05


class StateFlags(StrictIntFlag):
    STATE_CONTR = 0x000003F
    STATE_ERRC = 0x0000001
    STATE_ERRD = 0x0000002
    STATE_ERRV = 0x0000004
    STATE_EEPROM_CONNECTED = 0x0000010
    STATE_IS_HOMED = 0x0000020
    STATE_SECUR = 0x1B3FFC0
    STATE_ALARM = 0x0000040
    STATE_CTP_ERROR = 0x0000080
    STATE_POWER_OVERHEAT = 0x0000100
    STATE_CONTROLLER_OVERHEAT = 0x0000200
    STATE_OVERLOAD_POWER_VOLTAGE = 0x0000400
    STATE_OVERLOAD_POWER_CURRENT = 0x0000800
    STATE_OVERLOAD_USB_VOLTAGE = 0x0001000
    STATE_LOW_USB_VOLTAGE = 0x0002000
    STATE_OVERLOAD_USB_CURRENT = 0x0004000
    STATE_BORDERS_SWAP_MISSET = 0x0008000
    STATE_LOW_POWER_VOLTAGE = 0x0010000
    STATE_H_BRIDGE_FAULT = 0x0020000
    STATE_WINDING_RES_MISMATCH = 0x0100000
    STATE_ENCODER_FAULT = 0x0200000
    STATE_ENGINE_RESPONSE_ERROR = 0x0800000
    STATE_EXTIO_ALARM = 0x1000000


class GPIOFlags(StrictIntFlag):
    STATE_DIG_SIGNAL = 0xFFFF
    STATE_RIGHT_EDGE = 0x0001
    STATE_LEFT_EDGE = 0x0002
    STATE_BUTTON_RIGHT = 0x0004
    STATE_BUTTON_LEFT = 0x0008
    STATE_GPIO_PINOUT = 0x0010
    STATE_GPIO_LEVEL = 0x0020
    STATE_BRAKE = 0x0200
    STATE_REV_SENSOR = 0x0400
    STATE_SYNC_INPUT = 0x0800
    STATE_SYNC_OUTPUT = 0x1000
    STATE_ENC_A = 0x2000
    STATE_ENC_B = 0x4000


class EncodeStatus(StrictIntFlag):
    ENC_STATE_ABSENT = 0x00
    ENC_STATE_UNKNOWN = 0x01
    ENC_STATE_MALFUNC = 0x02
    ENC_STATE_REVERS = 0x03
    ENC_STATE_OK = 0x04


class WindStatus(StrictIntFlag):
    WIND_A_STATE_ABSENT = 0x00
    WIND_A_STATE_UNKNOWN = 0x01
    WIND_A_STATE_MALFUNC = 0x02
    WIND_A_STATE_OK = 0x03
    WIND_B_STATE_ABSENT = 0x00
    WIND_B_STATE_UNKNOWN = 0x10
    WIND_B_STATE_MALFUNC = 0x20
    WIND_B_STATE_OK = 0x30


class MvcmdStatus(StrictIntFlag):
    MVCMD_NAME_BITS = 0x3F
    MVCMD_UKNWN = 0x00
    MVCMD_MOVE = 0x01
    MVCMD_MOVR = 0x02
    MVCMD_LEFT = 0x03
    MVCMD_RIGHT = 0x04
    MVCMD_STOP = 0x05
    MVCMD_HOME = 0x06
    MVCMD_LOFT = 0x07
    MVCMD_SSTP = 0x08
    MVCMD_ERROR = 0x40
    MVCMD_RUNNING = 0x80


class MoveFlags(StrictIntFlag):
    RPM_DIV_1000 = 0x01


class EngineFlags(StrictIntFlag):
    ENGINE_REVERSE = 0x01
    ENGINE_CURRENT_AS_RMS = 0x02
    ENGINE_MAX_SPEED = 0x04
    ENGINE_ANTIPLAY = 0x08
    ENGINE_ACCEL_ON = 0x10
    ENGINE_LIMIT_VOLT = 0x20
    ENGINE_LIMIT_CURR = 0x40
    ENGINE_LIMIT_RPM = 0x80


class MicrostepMode(IntEnum):
    MICROSTEP_MODE_FULL = 0x01
    MICROSTEP_MODE_FRAC_2 = 0x02
    MICROSTEP_MODE_FRAC_4 = 0x03
    MICROSTEP_MODE_FRAC_8 = 0x04
    MICROSTEP_MODE_FRAC_16 = 0x05
    MICROSTEP_MODE_FRAC_32 = 0x06
    MICROSTEP_MODE_FRAC_64 = 0x07
    MICROSTEP_MODE_FRAC_128 = 0x08
    MICROSTEP_MODE_FRAC_256 = 0x09


class EngineType(StrictIntFlag):
    ENGINE_TYPE_NONE = 0x00
    ENGINE_TYPE_DC = 0x01
    ENGINE_TYPE_2DC = 0x02
    ENGINE_TYPE_STEP = 0x03
    ENGINE_TYPE_TEST = 0x04
    ENGINE_TYPE_BRUSHLESS = 0x05


class DriverType(StrictIntFlag):
    DRIVER_TYPE_DISCRETE_FET = 0x01
    DRIVER_TYPE_INTEGRATE = 0x02
    DRIVER_TYPE_EXTERNAL = 0x03


class PowerFlags(StrictIntFlag):
    POWER_REDUCT_ENABLED = 0x01
    POWER_OFF_ENABLED = 0x02
    POWER_SMOOTH_CURRENT = 0x04


class SecureFlags(StrictIntFlag):
    ALARM_ON_DRIVER_OVERHEATING = 0x01
    LOW_UPWR_PROTECTION = 0x02
    H_BRIDGE_ALERT = 0x04
    ALARM_ON_BORDERS_SWAP_MISSET = 0x08
    ALARM_FLAGS_STICKING = 0x10
    USB_BREAK_RECONNECT = 0x20
    ALARM_WINDING_MISMATCH = 0x40
    ALARM_ENGINE_RESPONSE = 0x80


class PositionFlags(StrictIntFlag):
    SETPOS_IGNORE_POSITION = 0x01
    SETPOS_IGNORE_ENCODER = 0x02


class FeedbackType(StrictIntFlag):
    FEEDBACK_ENCODER = 0x01
    FEEDBACK_EMF = 0x04
    FEEDBACK_NONE = 0x05
    FEEDBACK_ENCODER_MEDIATED = 0x06


class FeedbackFlags(StrictIntFlag):
    FEEDBACK_ENC_REVERSE = 0x01
    FEEDBACK_ENC_TYPE_BITS = 0xC0
    FEEDBACK_ENC_TYPE_AUTO = 0x00
    FEEDBACK_ENC_TYPE_SINGLE_ENDED = 0x40
    FEEDBACK_ENC_TYPE_DIFFERENTIAL = 0x80


class SyncInFlags(StrictIntFlag):
    SYNCIN_ENABLED = 0x01
    SYNCIN_INVERT = 0x02
    SYNCIN_GOTOPOSITION = 0x04


class SyncOutFlags(StrictIntFlag):
    SYNCOUT_ENABLED = 0x01
    SYNCOUT_STATE = 0x02
    SYNCOUT_INVERT = 0x04
    SYNCOUT_IN_STEPS = 0x08
    SYNCOUT_ONSTART = 0x10
    SYNCOUT_ONSTOP = 0x20
    SYNCOUT_ONPERIOD = 0x40


class ExtioSetupFlags(StrictIntFlag):
    EXTIO_SETUP_OUTPUT = 0x01
    EXTIO_SETUP_INVERT = 0x02


class ExtioModeFlags(StrictIntFlag):
    EXTIO_SETUP_MODE_IN_BITS = 0x0F
    EXTIO_SETUP_MODE_IN_NOP = 0x00
    EXTIO_SETUP_MODE_IN_STOP = 0x01
    EXTIO_SETUP_MODE_IN_PWOF = 0x02
    EXTIO_SETUP_MODE_IN_MOVR = 0x03
    EXTIO_SETUP_MODE_IN_HOME = 0x04
    EXTIO_SETUP_MODE_IN_ALARM = 0x05
    EXTIO_SETUP_MODE_OUT_BITS = 0xF0
    EXTIO_SETUP_MODE_OUT_OFF = 0x00
    EXTIO_SETUP_MODE_OUT_ON = 0x10
    EXTIO_SETUP_MODE_OUT_MOVING = 0x20
    EXTIO_SETUP_MODE_OUT_ALARM = 0x30
    EXTIO_SETUP_MODE_OUT_MOTOR_ON = 0x40


class BorderFlags(StrictIntFlag):
    BORDER_IS_ENCODER = 0x01
    BORDER_STOP_LEFT = 0x02
    BORDER_STOP_RIGHT = 0x04
    BORDERS_SWAP_MISSET_DETECTION = 0x08


class EnderFlags(StrictIntFlag):
    ENDER_SWAP = 0x01
    ENDER_SW1_ACTIVE_LOW = 0x02
    ENDER_SW2_ACTIVE_LOW = 0x04


class BrakeFlags(StrictIntFlag):
    BRAKE_ENABLED = 0x01
    BRAKE_ENG_PWROFF = 0x02


class ControlFlags(StrictIntFlag):
    CONTROL_MODE_BITS = 0x03
    CONTROL_MODE_OFF = 0x00
    CONTROL_MODE_JOY = 0x01
    CONTROL_MODE_LR = 0x02
    CONTROL_BTN_LEFT_PUSHED_OPEN = 0x04
    CONTROL_BTN_RIGHT_PUSHED_OPEN = 0x08


class JoyFlags(StrictIntFlag):
    JOY_REVERSE = 0x01


class CtpFlags(StrictIntFlag):
    CTP_ENABLED = 0x01
    CTP_BASE = 0x02
    CTP_ALARM_ON_ERROR = 0x04
    REV_SENS_INV = 0x08
    CTP_ERROR_CORRECTION = 0x10


class HomeFlags(StrictIntFlag):
    HOME_DIR_FIRST = 0x001
    HOME_DIR_SECOND = 0x002
    HOME_MV_SEC_EN = 0x004
    HOME_HALF_MV = 0x008
    HOME_STOP_FIRST_BITS = 0x030
    HOME_STOP_FIRST_REV = 0x010
    HOME_STOP_FIRST_SYN = 0x020
    HOME_STOP_FIRST_LIM = 0x030
    HOME_STOP_SECOND_BITS = 0x0C0
    HOME_STOP_SECOND_REV = 0x040
    HOME_STOP_SECOND_SYN = 0x080
    HOME_STOP_SECOND_LIM = 0x0C0
    HOME_USE_FAST = 0x100


class UARTSetupFlags(StrictIntFlag):
    UART_PARITY_BITS = 0x03
    UART_PARITY_BIT_EVEN = 0x00
    UART_PARITY_BIT_ODD = 0x01
    UART_PARITY_BIT_SPACE = 0x02
    UART_PARITY_BIT_MARK = 0x03
    UART_PARITY_BIT_USE = 0x04
    UART_STOP_BIT = 0x08


class BackEMFFlags(StrictIntFlag):
    BACK_EMF_INDUCTANCE_AUTO = 0x01
    BACK_EMF_RESISTANCE_AUTO = 0x02
    BACK_EMF_KM_AUTO = 0x04
