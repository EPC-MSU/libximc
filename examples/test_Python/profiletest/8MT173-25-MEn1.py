import libximc.highlevel as ximc


def set_profile_8MT173_25_MEn1(axis: ximc.Axis) -> None:
    feedback_settings = ximc.feedback_settings_t()
    feedback_settings.IPS = 4000
    feedback_settings.FeedbackType = ximc.FeedbackType.FEEDBACK_EMF
    feedback_settings.FeedbackFlags = ximc.FeedbackFlags.FEEDBACK_ENC_TYPE_SINGLE_ENDED | \
        ximc.FeedbackFlags.FEEDBACK_ENC_REVERSE
    feedback_settings.CountsPerTurn = 4000
    axis.set_feedback_settings(feedback_settings)

    home_settings = ximc.home_settings_t()
    home_settings.FastHome = 500
    home_settings.uFastHome = 0
    home_settings.SlowHome = 500
    home_settings.uSlowHome = 0
    home_settings.HomeDelta = 542
    home_settings.uHomeDelta = 0
    home_settings.HomeFlags = ximc.HomeFlags.HOME_USE_FAST | ximc.HomeFlags.HOME_STOP_SECOND_REV | \
        ximc.HomeFlags.HOME_STOP_FIRST_BITS | ximc.HomeFlags.HOME_DIR_SECOND
    axis.set_home_settings(home_settings)

    move_settings = ximc.move_settings_t()
    move_settings.Speed = 2000
    move_settings.uSpeed = 0
    move_settings.Accel = 2000
    move_settings.Decel = 5000
    move_settings.AntiplaySpeed = 2000
    move_settings.uAntiplaySpeed = 0
    move_settings.MoveFlags = 0
    axis.set_move_settings(move_settings)

    engine_settings = ximc.engine_settings_t()
    engine_settings.NomVoltage = 360
    engine_settings.NomCurrent = 670
    engine_settings.NomSpeed = 4000
    engine_settings.uNomSpeed = 0
    engine_settings.EngineFlags = ximc.EngineFlags.ENGINE_LIMIT_RPM | ximc.EngineFlags.ENGINE_ACCEL_ON | \
        ximc.EngineFlags.ENGINE_REVERSE
    engine_settings.Antiplay = 1800
    engine_settings.MicrostepMode = ximc.MicrostepMode.MICROSTEP_MODE_FRAC_256
    engine_settings.StepsPerRev = 200
    axis.set_engine_settings(engine_settings)

    entype_settings = ximc.entype_settings_t()
    entype_settings.EngineType = ximc.EngineType.ENGINE_TYPE_STEP
    entype_settings.DriverType = ximc.DriverType.DRIVER_TYPE_INTEGRATE
    axis.set_entype_settings(entype_settings)

    power_settings = ximc.power_settings_t()
    power_settings.HoldCurrent = 50
    power_settings.CurrReductDelay = 1000
    power_settings.PowerOffDelay = 60
    power_settings.CurrentSetTime = 300
    power_settings.PowerFlags = ximc.PowerFlags.POWER_SMOOTH_CURRENT | ximc.PowerFlags.POWER_REDUCT_ENABLED
    axis.set_power_settings(power_settings)

    secure_settings = ximc.secure_settings_t()
    secure_settings.LowUpwrOff = 800
    secure_settings.CriticalIpwr = 4000
    secure_settings.CriticalUpwr = 5500
    secure_settings.CriticalT = 800
    secure_settings.CriticalIusb = 450
    secure_settings.CriticalUusb = 520
    secure_settings.MinimumUusb = 420
    secure_settings.Flags = ximc.SecureFlags.ALARM_ENGINE_RESPONSE | ximc.SecureFlags.ALARM_FLAGS_STICKING | \
        ximc.SecureFlags.ALARM_ON_BORDERS_SWAP_MISSET | ximc.SecureFlags.H_BRIDGE_ALERT | \
        ximc.SecureFlags.ALARM_ON_DRIVER_OVERHEATING
    axis.set_secure_settings(secure_settings)

    edges_settings = ximc.edges_settings_t()
    edges_settings.BorderFlags = ximc.BorderFlags.BORDER_STOP_RIGHT | ximc.BorderFlags.BORDER_STOP_LEFT
    edges_settings.EnderFlags = ximc.EnderFlags.ENDER_SW2_ACTIVE_LOW | ximc.EnderFlags.ENDER_SW1_ACTIVE_LOW | \
        ximc.EnderFlags.ENDER_SWAP
    edges_settings.LeftBorder = -42
    edges_settings.uLeftBorder = 0
    edges_settings.RightBorder = 18958
    edges_settings.uRightBorder = 0
    axis.set_edges_settings(edges_settings)

    pid_settings = ximc.pid_settings_t()
    pid_settings.KpU = 0
    pid_settings.KiU = 0
    pid_settings.KdU = 0
    pid_settings.Kpf = 0.006
    pid_settings.Kif = 0.05
    pid_settings.Kdf = 2.8e-05
    axis.set_pid_settings(pid_settings)

    sync_in_settings = ximc.sync_in_settings_t()
    sync_in_settings.SyncInFlags = 0
    sync_in_settings.ClutterTime = 4
    sync_in_settings.Position = 0
    sync_in_settings.uPosition = 0
    sync_in_settings.Speed = 0
    sync_in_settings.uSpeed = 0
    axis.set_sync_in_settings(sync_in_settings)

    sync_out_settings = ximc.sync_out_settings_t()
    sync_out_settings.SyncOutFlags = ximc.SyncOutFlags.SYNCOUT_ONSTOP | ximc.SyncOutFlags.SYNCOUT_ONSTART
    sync_out_settings.SyncOutPulseSteps = 100
    sync_out_settings.SyncOutPeriod = 2000
    sync_out_settings.Accuracy = 0
    sync_out_settings.uAccuracy = 0
    axis.set_sync_out_settings(sync_out_settings)

    extio_settings = ximc.extio_settings_t()
    extio_settings.EXTIOSetupFlags = ximc.ExtioSetupFlags.EXTIO_SETUP_OUTPUT
    extio_settings.EXTIOModeFlags = ximc.ExtioModeFlags.EXTIO_SETUP_MODE_IN_STOP | \
        ximc.ExtioModeFlags.EXTIO_SETUP_MODE_OUT_OFF
    axis.set_extio_settings(extio_settings)

    brake_settings = ximc.brake_settings_t()
    brake_settings.t1 = 300
    brake_settings.t2 = 500
    brake_settings.t3 = 300
    brake_settings.t4 = 400
    brake_settings.BrakeFlags = ximc.BrakeFlags.BRAKE_ENG_PWROFF
    axis.set_brake_settings(brake_settings)

    control_settings = ximc.control_settings_t()
    control_settings.MaxSpeed = [20, 200, 2000, 0, 0, 0, 0, 0, 0, 0]
    control_settings.uMaxSpeed = [0 for _ in range(10)]
    control_settings.Timeout = [1000 for _ in range(9)]
    control_settings.MaxClickTime = 300
    control_settings.Flags = ximc.ControlFlags.CONTROL_MODE_OFF
    control_settings.DeltaPosition = 1
    control_settings.uDeltaPosition = 0
    axis.set_control_settings(control_settings)

    joystick_settings = ximc.joystick_settings_t()
    joystick_settings.JoyLowEnd = 0
    joystick_settings.JoyCenter = 5000
    joystick_settings.JoyHighEnd = 10000
    joystick_settings.ExpFactor = 100
    joystick_settings.DeadZone = 50
    joystick_settings.JoyFlags = 0
    axis.set_joystick_settings(joystick_settings)

    ctp_settings = ximc.ctp_settings_t()
    ctp_settings.CTPMinError = 3
    ctp_settings.CTPFlags = ximc.CtpFlags.CTP_ERROR_CORRECTION
    axis.set_ctp_settings(ctp_settings)

    uart_settings = ximc.uart_settings_t()
    uart_settings.Speed = 115200
    uart_settings.UARTSetupFlags = ximc.UARTSetupFlags.UART_PARITY_BIT_EVEN
    axis.set_uart_settings(uart_settings)

    controller_name = ximc.controller_name_t()
    controller_name.ControllerName = ""
    controller_name.CtrlFlags = 0
    axis.set_controller_name(controller_name)

    emf_settings = ximc.emf_settings_t()
    emf_settings.L = 0.0054
    emf_settings.R = 7.4
    emf_settings.Km = 0.0025
    emf_settings.BackEMFFlags = ximc.BackEMFFlags.BACK_EMF_INDUCTANCE_AUTO | \
        ximc.BackEMFFlags.BACK_EMF_RESISTANCE_AUTO | \
        ximc.BackEMFFlags.BACK_EMF_KM_AUTO
    axis.set_emf_settings(emf_settings)

    engine_advansed_setup = ximc.engine_advansed_setup_t()
    engine_advansed_setup.stepcloseloop_Kw = 50
    engine_advansed_setup.stepcloseloop_Kp_low = 1000
    engine_advansed_setup.stepcloseloop_Kp_high = 33
    axis.set_engine_advansed_setup(engine_advansed_setup)

    stage_name = ximc.stage_name_t()
    stage_name.PositionerName = ""
    axis.set_stage_name(stage_name)
