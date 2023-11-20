protocol "v20.8"
defaults with crc, answer, public

/** \english
	@name Enumerate devices flags
	* This is a bit mask for bitwise operations.
	\endenglish
	\russian
	@name Флаги поиска устройств
	* Это битовая маска для побитовых операций.
	\endrussian
	*/
flagset EnumerateFlags:
ENUMERATE_PROBE		= 0x01	/**< \english Check if a device with an OS name is a XIMC device. Be careful with this flag because it sends some data to the device. \endenglish \russian Проверять, является ли устройство XIMC-совместимым. Будьте осторожны с этим флагом, т.к. он отправляет данные в устройство.  \endrussian */
ENUMERATE_ALL_COM	= 0x02	/**< \english Check all COM devices \endenglish \russian Проверять все COM-устройства \endrussian */
ENUMERATE_NETWORK	= 0x04	/**< \english Check network devices \endenglish \russian Проверять сетевые устройства \endrussian */

/**
	* \english
	* @name Flags of move state
	* This is a bit mask for bitwise operations.
	* Specify move states.
	* \endenglish
	* \russian
	* @name Флаги состояния движения
	* Это битовая маска для побитовых операций.
	* Возвращаются командой get_status.
	* \endrussian
	* @see get_status
	*/
flagset MoveState:
MOVE_STATE_MOVING		= 0x01	/**< \english This flag indicates that the controller is trying to move the motor. Don't use this flag to wait for the completion of the movement command. Use the MVCMD_RUNNING flag from the MvCmdSts field instead. \endenglish \russian Если флаг установлен, то контроллер пытается вращать двигателем. Не используйте этот флаг для ожидания завершения команды движения. Вместо него используйте MVCMD_RUNNING из поля MvCmdSts. \endrussian */
MOVE_STATE_TARGET_SPEED	= 0x02	/**< \english Target speed is reached, if flag set. \endenglish \russian Флаг устанавливается при достижении заданной скорости. \endrussian */
MOVE_STATE_ANTIPLAY		= 0x04	/**< \english Motor is playing compensation, if flag set. \endenglish \russian Выполняется компенсация люфта, если флаг установлен. \endrussian */

/**
	* \english
	* @name Flags of internal controller settings
	* This is a bit mask for bitwise operations.
	* \endenglish
	* \russian
	* @name Флаги настроек контроллера
	* Это битовая маска для побитовых операций.
	* \endrussian
	* @see set_controller_name
	* @see get_controller_name
	*/
flagset ControllerFlags:
EEPROM_PRECEDENCE		= 0x01	/**< \english If the flag is set, settings from external EEPROM override controller settings. \endenglish \russian Если флаг установлен, то настройки в EEPROM подвижки имеют приоритет над текущими настройками и заменяют их при обнаружении EEPROM. \endrussian */

/**
	* \english
	* @name Flags of power state of stepper motor
	* This is a bit mask for bitwise operations.
	* Specify power states.
	* \endenglish
	* \russian
	* @name Флаги состояния питания шагового мотора
	* Это битовая маска для побитовых операций.
	* Возвращаются командой get_status.
	* \endrussian
	* @see get_status
	*/
flagset PowerState:
PWR_STATE_UNKNOWN	= 0x00	/**< \english Unknown state, should never happen. \endenglish \russian Неизвестное состояние, которое не должно никогда реализовываться. \endrussian */
PWR_STATE_OFF		= 0x01	/**< \english Motor windings are disconnected from the driver. \endenglish \russian Обмотки мотора разомкнуты и не управляются драйвером. \endrussian */
PWR_STATE_NORM		= 0x03	/**< \english Motor windings are powered by nominal current. \endenglish \russian Обмотки запитаны номинальным током. \endrussian */
PWR_STATE_REDUCT	= 0x04	/**< \english Motor windings are powered by reduced current to lower power consumption. \endenglish \russian Обмотки намеренно запитаны уменьшенным током от рабочего для снижения потребляемой мощности. \endrussian */
PWR_STATE_MAX		= 0x05	/**< \english Motor windings are powered by the maximum current driver can provide at this voltage. \endenglish \russian Обмотки двигателя питаются от максимального тока, который драйвер может обеспечить при этом напряжении. \endrussian */

/**
	* \english
	* @name Status flags
	* This is a bit mask for bitwise operations.
	* Controller flags returned by device query.
	* Contains boolean part of controller state.
	* May be combined with bitwise OR.
	* \endenglish
	* \russian
	* @name Флаги состояния
	* Это битовая маска для побитовых операций.
	* Содержат бинарные значения состояния контроллера. Могут быть объединены с помощью логического ИЛИ.
	* \endrussian
	* @see get_status
	*/
flagset StateFlags:
STATE_CONTR						= 0x0000003F	/**< \english Flags of controller states. \endenglish \russian Флаги состояния контроллера. \endrussian */
STATE_ERRC						= 0x00000001	/**< \english Command error encountered. The command received is not in the list of controller known commands. The most possible reason is the outdated firmware. \endenglish \russian Недопустимая команда. Полученная команда отсутствует в списке известных команд контроллера. Наиболее вероятной причиной является устаревшая прошивка. \endrussian */
STATE_ERRD						= 0x00000002	/**< \english Data integrity error encountered. The data inside the command and its CRC code do not correspond. Therefore, the data can't be considered valid. This error may be caused by EMI in the UART/RS232 interface. \endenglish \russian Обнаружена ошибка целостности данных. Данные внутри команды и ее CRC-код не соответствуют, поэтому данные не могут считаться действительными. Эта ошибка может быть вызвана электромагнитными помехами в интерфейсе UART/RS232. \endrussian */
STATE_ERRV						= 0x00000004	/**< \english Value error encountered. The values in the command can't be applied without correction because they fall outside the valid range. Corrected values were used instead of the original ones. \endenglish \russian Недопустимое значение данных. Обнаружена ошибка в значении. Значения в команде не могут быть применены без коррекции, поскольку они выходят за допустимый диапазон. Вместо исходных значений были использованы исправленные значения. \endrussian */
STATE_EEPROM_CONNECTED  		= 0x00000010	/**< \english EEPROM with settings is connected. The built-in stage profile is uploaded from the EEPROM memory chip if the EEPROM_PRECEDENCE flag is set, allowing you to connect various stages to the controller with automatic setup. \endenglish \russian Подключена память EEPROM с настройками. Встроенный профиль подвижки загружается из микросхемы памяти EEPROM, что позволяет подключать различные подвижки к контроллеру с автоматической настройкой. \endrussian */
STATE_IS_HOMED          		= 0x00000020  	/**< \english Calibration performed. This means that the relative position scale is calibrated against a hardware absolute position sensor, like a limit switch. Drops after loss of calibration, like harsh stops and possibly skipped steps. \endenglish \russian Калибровка выполнена. Это означает, что шкала относительного положения откалибрована с помощью аппаратного датчика абсолютного положения, такого как концевой переключатель. \endrussian */
STATE_SECUR						= 0x01B3FFC0	/**< \english Security flags. \endenglish \russian Флаги опасности. \endrussian */
STATE_ALARM						= 0x00000040	/**< \english The controller is in an alarm state, indicating that something dangerous has happened. Most commands are ignored in this state. To reset the flag, a STOP command must be issued. \endenglish \russian Контроллер находится в состоянии ALARM, показывая, что случилась какая-то опасная ситуация. В состоянии ALARM все команды игнорируются пока не будет послана команда STOP и состояние ALARM деактивируется. \endrussian */
STATE_CTP_ERROR					= 0x00000080	/**< \english Control position error (is only used with stepper motor). The flag is set when the encoder position and step position are too far apart. \endenglish \russian Контроль позиции нарушен(используется только с шаговым двигателем). Флаг устанавливается, когда положение энкодера и положение шага слишком далеки друг от друга. \endrussian */
STATE_POWER_OVERHEAT			= 0x00000100	/**< \english Power driver overheat. Motor control is disabled until some cooldown occurs. This should not happen with boxed versions of the controller. This may happen with the bare-board version of the controller with a custom radiator. Redesign your radiator. \endenglish \russian Перегрев силового драйвера. Управление двигателем отключено до восстановления рабочей температуры драйвера. Этого не должно происходить в коробочных версиях контроллера. Это может произойти в версии контроллера с «голой» платой и с пользовательским радиатором. Решение: используйте другой радиатор. \endrussian */
STATE_CONTROLLER_OVERHEAT		= 0x00000200	/**< \english Controller overheat. \endenglish \russian Перегрелась микросхема контроллера. \endrussian */
STATE_OVERLOAD_POWER_VOLTAGE	= 0x00000400	/**< \english Power voltage exceeds safe limit. \endenglish \russian Превышено напряжение на силовой части. \endrussian */
STATE_OVERLOAD_POWER_CURRENT	= 0x00000800	/**< \english Power current exceeds safe limit. \endenglish \russian Превышен максимальный ток потребления силовой части. \endrussian */
STATE_OVERLOAD_USB_VOLTAGE		= 0x00001000	/**< \english USB voltage exceeds safe limit. \endenglish \russian Превышено напряжение на USB. \endrussian */
STATE_LOW_USB_VOLTAGE			= 0x00002000	/**< \english USB voltage is insufficient for normal operation. \endenglish \russian Слишком низкое напряжение на USB. \endrussian */
STATE_OVERLOAD_USB_CURRENT		= 0x00004000	/**< \english USB current exceeds safe limit. \endenglish \russian Превышен максимальный ток потребления USB. \endrussian */
STATE_BORDERS_SWAP_MISSET		= 0x00008000	/**< \english Engine stuck at the wrong edge. \endenglish \russian Достижение неверной границы. \endrussian */
STATE_LOW_POWER_VOLTAGE			= 0x00010000	/**< \english Power voltage is lower than Low Voltage Protection limit \endenglish \russian Напряжение на силовой части ниже чем напряжение Low Voltage Protection \endrussian */
STATE_H_BRIDGE_FAULT			= 0x00020000	/**< \english Signal from the driver that fault happened \endenglish \russian Получен сигнал от драйвера о неисправности \endrussian */
STATE_WINDING_RES_MISMATCH		= 0x00100000	/**< \english The difference between winding resistances is too large. This usually happens with a damaged stepper motor with partially short-circuited windings. \endenglish \russian Сопротивления обмоток слишком сильно отличаются друг от друга. Обычно это происходит с поврежденным шаговым двигателем у которого полностью или частично закорочены обмотки. \endrussian */
STATE_ENCODER_FAULT 			= 0x00200000	/**< \english Signal from the encoder that fault happened \endenglish \russian Получен сигнал от энкодера о неисправности \endrussian */
STATE_ENGINE_RESPONSE_ERROR		= 0x00800000	/**< \english Error response of the engine control action. Motor control algorithm failure means that it can't make the correct decisions with the feedback data it receives. A single failure may be caused by a mechanical problem. A repeating failure can be caused by incorrect motor settings. \endenglish \russian Ошибка реакции двигателя на управляющее воздействие. Отказ алгоритма управления двигателем означает, что он не может определять правильные решения с помощью полученных данных обратной связи. Единичный отказ может быть вызван механической проблемой. Повторяющийся сбой может быть вызван неправильной настройкой двигателя. \endrussian */
STATE_EXTIO_ALARM				= 0x01000000	/**< \english The error is caused by the external EXTIO input signal. \endenglish \russian Ошибка вызвана внешним входным сигналом EXTIO. \endrussian */

/**
	* \english
	* @name Status flags of the GPIO outputs
	* This is a bit mask for bitwise operations.
	* GPIO state flags returned by device query.
	* Contains boolean part of controller state.
	* May be combined with bitwise OR.
	* \endenglish
	* \russian
	* @name Флаги состояния GPIO входов
	* Это битовая маска для побитовых операций.
	* Содержат бинарные значения состояния контроллера. Могут быть объединены с помощью логического ИЛИ.
	* \endrussian
	* @see get_status
	*/
flagset GPIOFlags:
STATE_DIG_SIGNAL				= 0x0000FFFF	/**< \english Flags of digital signals. \endenglish \russian Флаги цифровых сигналов. \endrussian */
STATE_RIGHT_EDGE				= 0x00000001	/**< \english Engine stuck at the right edge. \endenglish \russian Достижение правой границы. \endrussian */
STATE_LEFT_EDGE					= 0x00000002	/**< \english Engine stuck at the left edge. \endenglish \russian Достижение левой границы. \endrussian */
STATE_BUTTON_RIGHT				= 0x00000004	/**< \english Button "right" state (1 if pressed). \endenglish \russian Состояние кнопки "вправо" (1, если нажата). \endrussian */
STATE_BUTTON_LEFT				= 0x00000008	/**< \english Button "left" state (1 if pressed). \endenglish \russian Состояние кнопки "влево" (1, если нажата). \endrussian */
STATE_GPIO_PINOUT				= 0x00000010	/**< \english External GPIO works as out if the flag is set; otherwise, it works as in. \endenglish \russian Если флаг установлен, ввод/вывод общего назначения работает как выход; если флаг сброшен, ввод/вывод работает как вход. \endrussian */
STATE_GPIO_LEVEL				= 0x00000020	/**< \english State of external GPIO pin. \endenglish \russian Состояние ввода/вывода общего назначения. \endrussian */
STATE_BRAKE						= 0x00000200	/**< \english State of Brake pin. Flag "1" - if the pin state brake is not powered (brake is clamped), "0" - if the pin state brake is powered (brake is unclamped). \endenglish \russian Состояние вывода управления тормозом. Флаг "1" - если тормоз не запитан(зажат), "0" - если на тормоз подаётся питание(разжат). \endrussian */
STATE_REV_SENSOR				= 0x00000400	/**< \english State of Revolution sensor pin. \endenglish \russian Состояние вывода датчика оборотов(флаг "1", если датчик активен). \endrussian */
STATE_SYNC_INPUT				= 0x00000800	/**< \english State of Sync input pin. \endenglish \russian Состояние входа синхронизации(1, если вход синхронизации активен). \endrussian */
STATE_SYNC_OUTPUT				= 0x00001000	/**< \english State of Sync output pin. \endenglish \russian Состояние выхода синхронизации(1, если выход синхронизации активен). \endrussian */
STATE_ENC_A						= 0x00002000	/**< \english State of encoder A pin. \endenglish \russian Состояние ножки A энкодера(флаг "1", если энкодер активен). \endrussian */
STATE_ENC_B						= 0x00004000	/**< \english State of encoder B pin. \endenglish \russian Состояние ножки B энкодера(флаг "1", если энкодер активен). \endrussian */


/**
	* \english
	* @name Encoder state
	* This is a bit mask for bitwise operations.
	* Encoder state returned by device query.
	* \endenglish
	* \russian
	* @name Состояние энкодера
	* Это битовая маска для побитовых операций.
	* Состояние энкодера, подключенного к контроллеру.
	* \endrussian
	* @see get_status
	*/
flagset EncodeStatus:
ENC_STATE_ABSENT	= 0x00	/**< \english Encoder is absent. \endenglish \russian Энкодер не подключен. \endrussian */
ENC_STATE_UNKNOWN	= 0x01	/**< \english Encoder state is unknown. \endenglish \russian Состояние энкодера неизвестно. \endrussian */
ENC_STATE_MALFUNC	= 0x02	/**< \english Encoder is connected and malfunctioning. \endenglish \russian Энкодер подключен и неисправен. \endrussian */
ENC_STATE_REVERS	= 0x03	/**< \english Encoder is connected and operational but counts in other direction. \endenglish \russian Энкодер подключен и исправен, но считает в другую сторону. \endrussian */
ENC_STATE_OK		= 0x04	/**< \english Encoder is connected and working properly. \endenglish \russian Энкодер подключен и работает должным образом. \endrussian */

/**
	* \english
	* @name Winding state
	* This is a bit mask for bitwise operations.
	* Motor winding state returned by device query.
	* \endenglish
	* \russian
	* @name Состояние обмоток
	* Это битовая маска для побитовых операций.
	* Состояние обмоток двигателя, подключенного к контроллеру.
	* \endrussian
	* @see get_status
	*/
flagset WindStatus:
WIND_A_STATE_ABSENT		= 0x00	/**< \english Winding A is disconnected. \endenglish \russian Обмотка A не подключена. \endrussian */
WIND_A_STATE_UNKNOWN	= 0x01	/**< \english Winding A state is unknown. \endenglish \russian Состояние обмотки A неизвестно. \endrussian */
WIND_A_STATE_MALFUNC	= 0x02	/**< \english Winding A is short-circuited. \endenglish \russian Короткое замыкание на обмотке A. \endrussian */
WIND_A_STATE_OK			= 0x03	/**< \english Winding A is connected and working properly. \endenglish \russian Обмотка A работает адекватно. \endrussian */
WIND_B_STATE_ABSENT		= 0x00	/**< \english Winding B is disconnected. \endenglish \russian Обмотка B не подключена. \endrussian */
WIND_B_STATE_UNKNOWN	= 0x10	/**< \english Winding B state is unknown. \endenglish \russian Состояние обмотки B неизвестно. \endrussian */
WIND_B_STATE_MALFUNC	= 0x20	/**< \english Winding B is short-circuited. \endenglish \russian Короткое замыкание на обмотке B. \endrussian */
WIND_B_STATE_OK			= 0x30	/**< \english Winding B is connected and working properly. \endenglish \russian Обмотка B работает адекватно. \endrussian */

/**
	* \english
	* @name Move command state
	* This is a bit mask for bitwise operations.
	* Move command (command_move, command_movr, command_left, command_right, command_stop, command_home, command_loft, command_sstp)
	* and its state (run, finished, error).
	* \endenglish
	* \russian
	* @name Состояние команды движения
	* Это битовая маска для побитовых операций.
	* Состояние команды движения (касается command_move, command_movr, command_left, command_right, command_stop, command_home, command_loft, command_sstp)
	* и статуса её выполнения (выполняется, завершено, ошибка)
	* \endrussian
	* @see get_status
	*/
flagset MvcmdStatus:
MVCMD_NAME_BITS	= 0x3F	/**< \english Move command bit mask. \endenglish \russian Битовая маска активной команды. \endrussian */
MVCMD_UKNWN		= 0x00	/**< \english Unknown command. \endenglish \russian Неизвестная команда. \endrussian */
MVCMD_MOVE		= 0x01	/**< \english Command move. \endenglish \russian Команда move. \endrussian */
MVCMD_MOVR		= 0x02	/**< \english Command movr. \endenglish \russian Команда movr. \endrussian */
MVCMD_LEFT		= 0x03	/**< \english Command left. \endenglish \russian Команда left. \endrussian */
MVCMD_RIGHT		= 0x04	/**< \english Command rigt. \endenglish \russian Команда rigt. \endrussian */
MVCMD_STOP		= 0x05	/**< \english Command stop. \endenglish \russian Команда stop. \endrussian */
MVCMD_HOME		= 0x06	/**< \english Command home. \endenglish \russian Команда home. \endrussian */
MVCMD_LOFT		= 0x07	/**< \english Command loft. \endenglish \russian Команда loft. \endrussian */
MVCMD_SSTP		= 0x08	/**< \english Command soft stop. \endenglish \russian Команда плавной остановки(SSTP). \endrussian */
MVCMD_ERROR		= 0x40	/**< \english Finish state (1 - move command has finished with an error, 0 - move command has finished correctly). This flag makes sense when MVCMD_RUNNING signals movement completion. \endenglish \russian Состояние завершения движения (1 - команда движения выполнена с ошибкой, 0 - команда движения выполнена корректно). Имеет смысл если MVCMD_RUNNING указывает на завершение движения. \endrussian */
MVCMD_RUNNING	= 0x80	/**< \english Move command state (0 - move command has finished, 1 - move command is being executed). \endenglish \russian Состояние команды движения (0 - команда движения выполнена, 1 - команда движения сейчас выполняется). \endrussian */

/**
	* \english
	* @name Flags of the motion parameters
	* This is a bit mask for bitwise operations.
	* Specify the motor shaft movement algorithm and list of limitations.
	* Flags returned by the query of get_move_settings.
	* \endenglish
	* \russian
	* @name Флаги параметров движения
	* Это битовая маска для побитовых операций.
	* Определяют настройки параметров движения.
	* Возвращаются командой get_move_settings.
	* \endrussian
	* @see set_move_settings
	* @see get_move_settings
	*/
flagset MoveFlags:
RPM_DIV_1000		= 0x01	/**< \english This flag indicates that the operating speed specified in the command is set in milliRPM. Applicable only for ENCODER feedback mode and only for BLDC motors. \endenglish \russian Флаг указывает на то что рабочая скорость указанная в команде задана в милли rpm. Применим только для режима обратной связи ENCODER и только для BLDC моторов. \endrussian */

/**
	* \english
	* @name Flags of engine settings
	* This is a bit mask for bitwise operations.
	* Specify the motor shaft movement algorithm and list of limitations.
	* Flags returned by query of engine settings. May be combined with bitwise OR.
	* \endenglish
	* \russian
	* @name Флаги параметров мотора
	* Это битовая маска для побитовых операций.
	* Определяют настройки движения и работу ограничителей.
	* Возвращаются командой get_engine_settings. Могут быть объединены с помощью логического ИЛИ.
	* \endrussian
	* @see set_engine_settings
	* @see get_engine_settings
	*/
flagset EngineFlags:
ENGINE_REVERSE		= 0x0001	/**< \english Reverse flag. It determines motor shaft rotation direction that corresponds to feedback counts increasing. If not set (default), motor shaft rotation direction under positive voltage corresponds to feedback counts increasing and vice versa. Change it if you see that positive directions on motor and feedback are opposite. \endenglish \russian Флаг реверса. Связывает направление вращения мотора с направлением счета текущей позиции. При сброшенном флаге (по умолчанию) прикладываемое к мотору положительное напряжение увеличивает счетчик позиции. И наоборот, при установленном флаге счетчик позиции увеличивается, когда к мотору приложено отрицательное напряжение. Измените состояние флага, если положительное вращение мотора уменьшает счетчик позиции. \endrussian */
ENGINE_CURRENT_AS_RMS	= 0x0002	/**< \english Engine current meaning flag. If the flag is unset, then the engine's current value is interpreted as the maximum amplitude value. If the flag is set, then the engine current value is interpreted as the root-mean-square current value (for stepper) or as the current value calculated from the maximum heat dissipation (BLDC). \endenglish \russian Флаг интерпретации значения тока. Если флаг снят, то задаваемое значение тока интерпретируется как максимальная амплитуда тока. Если флаг установлен, то задаваемое значение тока интерпретируется как среднеквадратичное значение тока (для шагового) или как значение тока, посчитанное из максимального тепловыделения (BLDC). \endrussian */
ENGINE_MAX_SPEED	= 0x0004	/**< \english Max speed flag. If it is set, the engine uses the maximum speed achievable with the present engine settings as its nominal speed. \endenglish \russian Флаг максимальной скорости. Если флаг установлен, движение происходит на максимальной скорости. \endrussian */
ENGINE_ANTIPLAY		= 0x0008	/**< \english Play compensation flag. If it is set, the engine makes backlash (play) compensation and reaches the predetermined position accurately at low speed. \endenglish \russian Компенсация люфта. Если флаг установлен, позиционер будет подходить к заданной точке всегда с одной стороны. Например, при подходе слева никаких дополнительных действий не совершается, а при подходе справа позиционер проходит целевую позицию на заданное расстояния и возвращается к ней опять же справа. \endrussian */
ENGINE_ACCEL_ON		= 0x0010	/**< \english Acceleration enable flag. If it set, motion begins with acceleration and ends with deceleration. \endenglish \russian Ускорение. Если флаг установлен, движение происходит с ускорением. \endrussian */
ENGINE_LIMIT_VOLT	= 0x0020	/**< \english Maximum motor voltage limit enable flag (is only used with DC motor). \endenglish \russian Номинальное напряжение мотора. Если флаг установлен, напряжение на моторе ограничивается заданным номинальным значением(используется только с DC двигателем). \endrussian */
ENGINE_LIMIT_CURR	= 0x0040	/**< \english Maximum motor current limit enable flag (is only used with DC motor). \endenglish \russian Номинальный ток мотора. Если флаг установлен, ток через мотор ограничивается заданным номинальным значением(используется только с DC двигателем). \endrussian */
ENGINE_LIMIT_RPM	= 0x0080	/**< \english Maximum motor speed limit enable flag. \endenglish \russian Номинальная частота вращения мотора. Если флаг установлен, частота вращения ограничивается заданным номинальным значением. \endrussian */

/**
	* \english
	* @name Flags of microstep mode
	* This is a bit mask for bitwise operations.
	* Specify settings for microstep mode. Used with step motors.
	* Flags returned by query of engine settings. May be combined with bitwise OR
	* \endenglish
	* \russian
	* @name Флаги параметров микрошагового режима
	* Это битовая маска для побитовых операций.
	* Определяют деление шага в микрошаговом режиме. Используются с шаговыми моторами.
	* Возвращаются командой get_engine_settings. Могут быть объединены с помощью логического ИЛИ.
	* \endrussian
	* @see engine_settings_t::flags
	* @see set_engine_settings
	* @see get_engine_settings
	*/
flagset MicrostepMode:
MICROSTEP_MODE_FULL		= 0x01	/**< \english Full step mode. \endenglish \russian Полношаговый режим. \endrussian */
MICROSTEP_MODE_FRAC_2	= 0x02	/**< \english 1/2-step mode. \endenglish \russian Деление шага 1/2. \endrussian */
MICROSTEP_MODE_FRAC_4	= 0x03	/**< \english 1/4-step mode. \endenglish \russian Деление шага 1/4. \endrussian */
MICROSTEP_MODE_FRAC_8	= 0x04	/**< \english 1/8-step mode. \endenglish \russian Деление шага 1/8. \endrussian */
MICROSTEP_MODE_FRAC_16	= 0x05	/**< \english 1/16-step mode. \endenglish \russian Деление шага 1/16. \endrussian */
MICROSTEP_MODE_FRAC_32	= 0x06	/**< \english 1/32-step mode. \endenglish \russian Деление шага 1/32. \endrussian */
MICROSTEP_MODE_FRAC_64	= 0x07	/**< \english 1/64-step mode. \endenglish \russian Деление шага 1/64. \endrussian */
MICROSTEP_MODE_FRAC_128	= 0x08	/**< \english 1/128-step mode. \endenglish \russian Деление шага 1/128. \endrussian */
MICROSTEP_MODE_FRAC_256	= 0x09	/**< \english 1/256-step mode. \endenglish \russian Деление шага 1/256. \endrussian */

/**
	* \english
	* @name Flags of engine type
	* This is a bit mask for bitwise operations.
	* Specify motor type.
	* Flags returned by query of engine settings.
	* \endenglish
	* \russian
	* @name Флаги, определяющие тип мотора
	* Это битовая маска для побитовых операций.
	* Определяют тип мотора.
	* Возвращаются командой get_entype_settings.
	* \endrussian
	* @see engine_settings_t::flags
	* @see set_entype_settings
	* @see get_entype_settings
	*/
flagset EngineType:
ENGINE_TYPE_NONE		= 0x00	/**< \english A value that shouldn't be used. \endenglish \russian Это значение не нужно использовать. \endrussian */
ENGINE_TYPE_DC			= 0x01	/**< \english DC motor. \endenglish \russian Мотор постоянного тока. \endrussian */
ENGINE_TYPE_2DC			= 0x02	/**< \english 2 DC motors. \endenglish \russian Два мотора постоянного тока, что приводит к эмуляции двух контроллеров. \endrussian */
ENGINE_TYPE_STEP		= 0x03	/**< \english Step motor. \endenglish \russian Шаговый мотор. \endrussian */
ENGINE_TYPE_TEST		= 0x04	/**< \english Duty cycle are fixed. Used only manufacturer. \endenglish \russian Продолжительность включения фиксирована. Используется только производителем. \endrussian */
ENGINE_TYPE_BRUSHLESS	= 0x05	/**< \english Brushless motor. \endenglish \russian Бесщеточный мотор. \endrussian */

/**
	* \english
	* @name Flags of driver type
	* This is a bit mask for bitwise operations.
	* Specify driver type.
	* Flags returned by query of engine settings.
	* \endenglish
	* \russian
	* @name Флаги, определяющие тип силового драйвера
	* Это битовая маска для побитовых операций.
	* Определяют тип силового драйвера.
	* Возвращаются командой get_entype_settings.
	* \endrussian
	* @see engine_settings_t::flags
	* @see set_entype_settings
	* @see get_entype_settings
	*/
flagset DriverType:
DRIVER_TYPE_DISCRETE_FET	= 0x01	/**< \english Driver with discrete FET keys. Default option. \endenglish \russian Силовой драйвер на дискретных мосфет-ключах. Используется по умолчанию. \endrussian */
DRIVER_TYPE_INTEGRATE		= 0x02	/**< \english Driver with integrated IC. \endenglish \russian Силовой драйвер с использованием ключей, интегрированных в микросхему. \endrussian */
DRIVER_TYPE_EXTERNAL		= 0x03	/**< \english External driver. \endenglish \russian Внешний силовой драйвер. \endrussian */


/**
	* \english
	* @name Flags of power settings of stepper motor
	* This is a bit mask for bitwise operations.
	* Flags returned by query of engine settings.
	* Specify power settings. Flags returned by query of power settings.
	* \endenglish
	* \russian
	* @name Флаги параметров питания шагового мотора
	* Это битовая маска для побитовых операций.
	* Возвращаются командой get_power_settings.
	* \endrussian
	* @see get_power_settings
	* @see set_power_settings
	*/
flagset PowerFlags:
POWER_REDUCT_ENABLED	= 0x01	/**< \english Current reduction is enabled after CurrReductDelay if this flag is set. \endenglish \russian Если флаг установлен, уменьшить ток по прошествии CurrReductDelay. Иначе - не уменьшать. \endrussian */
POWER_OFF_ENABLED		= 0x02	/**< \english Power off is enabled after PowerOffDelay if this flag is set. \endenglish \russian Если флаг установлен, снять напряжение с обмоток по прошествии PowerOffDelay. Иначе - не снимать. \endrussian */
POWER_SMOOTH_CURRENT	= 0x04	/**< \english Current ramp-up/down are performed smoothly during current_set_time if this flag is set. \endenglish \russian Если установлен, то запитывание обмоток, снятие питания или снижение/повышение тока происходят плавно со скоростью CurrentSetTime, а только потом выполняется та задача, которая вызвала это плавное изменение. \endrussian */

/**
	* \english
	* @name Flags of secure settings
	* This is a bit mask for bitwise operations.
	* Flags returned by query of engine settings.
	* Specify secure settings. Flags returned by query of secure settings.
	* \endenglish
	* \russian
	* @name Флаги критических параметров.
	* Это битовая маска для побитовых операций.
	* Возвращаются командой get_secure_settings.
	* \endrussian
	* @see get_secure_settings
	* @see set_secure_settings
	*/
flagset SecureFlags:
ALARM_ON_DRIVER_OVERHEATING	= 0x01	/**< \english If this flag is set, enter the alarm state on the driver overheat signal. \endenglish \russian Если флаг установлен, то войти в состояние Alarm при получении сигнала подступающего перегрева с драйвера. Иначе - игнорировать подступающий перегрев с драйвера. \endrussian */
LOW_UPWR_PROTECTION			= 0x02	/**< \english If this flag is set, turn off the motor when the voltage is lower than LowUpwrOff. \endenglish \russian Если установлен, то выключать силовую часть при напряжении меньшем LowUpwrOff. \endrussian */
H_BRIDGE_ALERT				= 0x04	/**< \english If this flag is set then turn off the power unit with a signal problem in one of the transistor bridge. \endenglish \russian Если установлен, то выключать силовую часть при сигнале неполадки в одном из транзисторных мостов.\endrussian */
ALARM_ON_BORDERS_SWAP_MISSET= 0x08	/**< \english If this flag is set, enter Alarm state on borders swap misset \endenglish \russian Если флаг установлен, то войти в состояние Alarm при получении сигнала c противоположного концевого выключателя.\endrussian */
ALARM_FLAGS_STICKING		= 0x10	/**< \english If this flag is set, only a STOP command can turn all alarms to 0 \endenglish \russian Если флаг установлен, то только по команде STOP возможен сброс всех флагов ALARM.\endrussian */
USB_BREAK_RECONNECT			= 0x20 /**< \english If this flag is set, the USB brake reconnect module will be enabled \endenglish \russian Если флаг установлен, то будет включен блок перезагрузки USB при поломке связи.\endrussian */
ALARM_WINDING_MISMATCH		= 0x40 /**< \english If this flag is set, enter Alarm state when windings mismatch \endenglish \russian Если флаг установлен, то войти в состояние Alarm при получении сигнала рассогласования обмоток \endrussian */
ALARM_ENGINE_RESPONSE		= 0x80 /**< \english If this flag is set, enter the Alarm state on response of the engine control action \endenglish \russian Если флаг установлен, то войти в состояние Alarm при получении сигнала ошибки реакции двигателя на управляющее воздействие  \endrussian */

/**
	* \english
	* @name Position setting flags
	* This is a bit mask for bitwise operations.
	* Flags used in setting position.
	* \endenglish
	* \russian
	* @name Флаги установки положения
	* Это битовая маска для побитовых операций.
	* Возвращаются командой get_position.
	* \endrussian
	* @see get_position
	* @see set_position
	*/
flagset PositionFlags:
SETPOS_IGNORE_POSITION	= 0x01	/**< \english Will not reload position in steps/microsteps if this flag is set. \endenglish \russian Если установлен, то позиция в шагах и микрошагах не обновляется. \endrussian */
SETPOS_IGNORE_ENCODER	= 0x02	/**< \english Will not reload encoder state if this flag is set. \endenglish \russian Если установлен, то счётчик энкодера не обновляется. \endrussian */

/**
	* \english
	* @name Feedback type.
	* This is a bit mask for bitwise operations.
	* \endenglish
	* \russian
	* @name Тип обратной связи.
	* Это битовая маска для побитовых операций.
	* \endrussian
	* @see set_feedback_settings
	* @see get_feedback_settings
	*/
flagset FeedbackType:
FEEDBACK_ENCODER		= 0x01	/**< \english Feedback by encoder. \endenglish \russian Обратная связь с помощью энкодера. \endrussian */
FEEDBACK_EMF			= 0x04	/**< \english Feedback by EMF. \endenglish \russian Обратная связь по ЭДС. \endrussian */
FEEDBACK_NONE			= 0x05	/**< \english Feedback is absent. \endenglish \russian Обратная связь отсутствует. \endrussian */
FEEDBACK_ENCODER_MEDIATED	= 0x06	/**< \english Feedback by encoder mediated by mechanical transmission (for example leadscrew). \endenglish \russian Обратная связь по энкодеру, опосредованному относительно двигателя механической передачей (например, винтовой передачей). \endrussian */

/**
	* \english
	* @name Describes feedback flags.
	* This is a bit mask for bitwise operations.
	* \endenglish
	* \russian
	* @name Флаги обратной связи.
	* Это битовая маска для побитовых операций.
	* \endrussian
	* @see set_feedback_settings
	* @see get_feedback_settings
	*/
flagset FeedbackFlags:
FEEDBACK_ENC_REVERSE	= 0x01	/**< \english Reverse count of encoder. \endenglish \russian Обратный счет у энкодера. \endrussian */
FEEDBACK_ENC_TYPE_BITS	= 0xC0	/**< \english Bits of the encoder type. \endenglish \russian Биты, отвечающие за тип энкодера. \endrussian */
FEEDBACK_ENC_TYPE_AUTO	= 0x00	/**< \english Auto detect encoder type. \endenglish \russian Определяет тип энкодера автоматически. \endrussian */
FEEDBACK_ENC_TYPE_SINGLE_ENDED	= 0x40	/**< \english Single-ended encoder. \endenglish \russian Недифференциальный энкодер. \endrussian */
FEEDBACK_ENC_TYPE_DIFFERENTIAL	= 0x80	/**< \english Differential encoder. \endenglish \russian Дифференциальный энкодер. \endrussian */

/**
	* \english
	* @name Flags for synchronization input setup
	* This is a bit mask for bitwise operations.
	* \endenglish
	* \russian
	* @name Флаги настроек синхронизации входа
	* Это битовая маска для побитовых операций.
	* \endrussian
	*/
flagset SyncInFlags:
SYNCIN_ENABLED		= 0x01	/**< \english Synchronization in mode is enabled if this flag is set. \endenglish \russian Включение необходимости импульса синхронизации для начала движения. \endrussian */
SYNCIN_INVERT		= 0x02	/**< \english Trigger on falling edge if flag is set, on rising edge otherwise. \endenglish \russian Если установлен - срабатывает по переходу из 1 в 0. Иначе - из 0 в 1. \endrussian */
SYNCIN_GOTOPOSITION	= 0x04	/**< \english The engine is going to the position specified in Position and uPosition if this flag is set. And it is shifting on the Position and uPosition if this flag is unset \endenglish \russian Если флаг установлен, то двигатель смещается к позиции, установленной в Position и uPosition, иначе двигатель смещается на Position и uPosition \endrussian */

/**
	* \english
	* @name Flags of synchronization output
	* This is a bit mask for bitwise operations.
	* \endenglish
	* \russian
	* @name Флаги настроек синхронизации выхода
	* Это битовая маска для побитовых операций.
	* \endrussian
	*/
flagset SyncOutFlags:
SYNCOUT_ENABLED		= 0x01	/**< \english The synchronization out pin follows the synchronization logic if the flag is set. Otherwise, it is governed by the SYNCOUT_STATE flag. \endenglish \russian Синхронизация выхода работает согласно настройкам, если флаг установлен. В ином случае значение выхода фиксировано и подчиняется SYNCOUT_STATE. \endrussian */
SYNCOUT_STATE		= 0x02	/**< \english When the output state is fixed by the negative SYNCOUT_ENABLED flag, the pin state is in accordance with this flag state. \endenglish \russian Когда значение выхода управляется напрямую (см. флаг SYNCOUT_ENABLED), значение на выходе соответствует значению этого флага. \endrussian */
SYNCOUT_INVERT		= 0x04	/**< \english The low level is active if the flag is set. Otherwise,  the high level is active. \endenglish \russian Нулевой логический уровень является активным, если флаг установлен, а единичный - если флаг сброшен. \endrussian */
SYNCOUT_IN_STEPS	= 0x08	/**< \english Use motor steps or encoder pulses instead of milliseconds for output pulse generation if the flag is set. \endenglish \russian Если флаг установлен использовать шаги/импульсы энкодера для выходных импульсов синхронизации вместо миллисекунд. \endrussian */
SYNCOUT_ONSTART		= 0x10	/**< \english Generate a synchronization pulse when movement starts. \endenglish \russian Генерация синхронизирующего импульса при начале движения. \endrussian */
SYNCOUT_ONSTOP		= 0x20	/**< \english Generate a synchronization pulse when movement stops. \endenglish \russian Генерация синхронизирующего импульса при остановке. \endrussian */
SYNCOUT_ONPERIOD	= 0x40	/**< \english Generate a synchronization pulse every SyncOutPeriod encoder pulses. \endenglish \russian Выдает импульс синхронизации после прохождения SyncOutPeriod отсчётов. \endrussian */

/**
	* \english
	* @name External IO setup flags
	* This is a bit mask for bitwise operations.
	* \endenglish
	* \russian
	* @name Флаги настройки работы внешнего ввода/вывода
	* Это битовая маска для побитовых операций.
	* \endrussian
	* @see get_extio_settings
	* @see set_extio_settings
	*/
flagset ExtioSetupFlags:
EXTIO_SETUP_OUTPUT	= 0x01	/**< \english EXTIO works as output if the flag is set, works as input otherwise. \endenglish \russian Если флаг установлен, то ножка в состоянии вывода, иначе - ввода. \endrussian */
EXTIO_SETUP_INVERT	= 0x02	/**< \english Interpret EXTIO state inverted if the flag is set. A falling front is treated as an input event and a low logic level as an active state. \endenglish \russian Если флаг установлен, то нули считаются активным состоянием выхода, а спадающие фронты как момент подачи входного сигнала. \endrussian */

/**
	* \english
	* @name External IO mode flags
	* This is a bit mask for bitwise operations.
	* \endenglish
	* \russian
	* @name Флаги настройки режимов внешнего ввода/вывода
	* Это битовая маска для побитовых операций.
	* \endrussian
	* @see extio_settings_t::extio_mode_flags
	* @see get_extio_settings
	* @see set_extio_settings
	*/
flagset ExtioModeFlags:
EXTIO_SETUP_MODE_IN_BITS            = 0x0F  /**< \english Bits of the behavior selector when the signal on input goes to the active state. \endenglish \russian Биты, отвечающие за поведение при переходе сигнала в активное состояние. \endrussian */
EXTIO_SETUP_MODE_IN_NOP             = 0x00  /**< \english Do nothing. \endenglish \russian Ничего не делать. \endrussian */
EXTIO_SETUP_MODE_IN_STOP            = 0x01  /**< \english Issue STOP command, ceasing the engine movement. \endenglish \russian По переднему фронту входного сигнала делается остановка двигателя (эквивалент команды STOP). \endrussian */
EXTIO_SETUP_MODE_IN_PWOF            = 0x02  /**< \english Issue PWOF command, powering off all engine windings. \endenglish \russian Выполняет команду PWOF, обесточивая обмотки двигателя. \endrussian */
EXTIO_SETUP_MODE_IN_MOVR            = 0x03  /**< \english Issue MOVR command with last used settings. \endenglish \russian Выполняется команда MOVR с последними настройками. \endrussian */
EXTIO_SETUP_MODE_IN_HOME            = 0x04  /**< \english Issue HOME command. \endenglish \russian Выполняется команда HOME. \endrussian */
EXTIO_SETUP_MODE_IN_ALARM           = 0x05  /**< \english Set Alarm when the signal goes to the active state. \endenglish \russian Войти в состояние ALARM при переходе сигнала в активное состояние. \endrussian */
EXTIO_SETUP_MODE_OUT_BITS           = 0xF0  /**< \english Bits of the output behavior selection. \endenglish \russian Биты выбора поведения на выходе. \endrussian */
EXTIO_SETUP_MODE_OUT_OFF            = 0x00  /**< \english EXTIO pin always set in inactive state. \endenglish \russian Ножка всегда в неактивном состоянии. \endrussian */
EXTIO_SETUP_MODE_OUT_ON             = 0x10  /**< \english EXTIO pin always set in active state. \endenglish \russian Ножка всегда в активном состоянии. \endrussian */
EXTIO_SETUP_MODE_OUT_MOVING         = 0x20  /**< \english EXTIO pin stays active during moving state. \endenglish \russian Ножка находится в активном состоянии при движении. \endrussian */
EXTIO_SETUP_MODE_OUT_ALARM          = 0x30  /**< \english EXTIO pin stays active during the alarm state. \endenglish \russian Ножка находится в активном состоянии при нахождении в состоянии ALARM. \endrussian */
EXTIO_SETUP_MODE_OUT_MOTOR_ON       = 0x40  /**< \english EXTIO pin stays active when windings are powered. \endenglish \russian Ножка находится в активном состоянии при подаче питания на обмотки. \endrussian */

/**
	* \english
	* @name Border flags
	* This is a bit mask for bitwise operations.
	* Specify types of borders and motor behavior on borders.
	* May be combined with bitwise OR.
	* \endenglish
	* \russian
	* @name Флаги границ
	* Это битовая маска для побитовых операций.
	* Типы границ и поведение позиционера на границах.
	* Могут быть объединены с помощью побитового ИЛИ.
	* \endrussian
	* @see get_edges_settings
	* @see set_edges_settings
	*/
flagset BorderFlags:
BORDER_IS_ENCODER				= 0x01	/**< \english Borders are fixed by predetermined encoder values, if set; borders are placed on limit switches, if not set. \endenglish \russian Если флаг установлен, границы определяются предустановленными точками на шкале позиции. Если флаг сброшен, границы определяются концевыми выключателями. \endrussian */
BORDER_STOP_LEFT				= 0x02	/**< \english The motor should stop on the left border. \endenglish \russian Если флаг установлен, мотор останавливается при достижении левой границы. \endrussian */
BORDER_STOP_RIGHT				= 0x04	/**< \english Motor should stop on right border. \endenglish \russian Если флаг установлен, мотор останавливается при достижении правой границы. \endrussian */
BORDERS_SWAP_MISSET_DETECTION	= 0x08	/**< \english Motor should stop on both borders. Need to save motor then wrong border settings is set\endenglish \russian Если флаг установлен, мотор останавливается при достижении обоих границ. Нужен для предотвращения поломки двигателя при неправильных настройках концевых выключателей \endrussian */

/**
	* \english
	* @name Limit switches flags
	* This is a bit mask for bitwise operations.
	* Specify electrical behavior of limit switches like order and pulled positions.
	* May be combined with bitwise OR.
	* \endenglish
	* \russian
	* @name Флаги концевых выключателей
	* Это битовая маска для побитовых операций.
	* Определяют направление и состояние границ.
	* Могут быть объединены с помощью побитового ИЛИ.
	* \endrussian
	* @see get_edges_settings
	* @see set_edges_settings
	*/
flagset EnderFlags:
ENDER_SWAP				= 0x01	/**< \english First limit switch on the right side, if set; otherwise on the left side. \endenglish \russian Если флаг установлен, первый концевой выключатель находится справа; иначе - слева. \endrussian */
ENDER_SW1_ACTIVE_LOW	= 0x02	/**< \english 1 - Limit switch connected to pin SW1 is triggered by a low level on pin. \endenglish \russian 1 - Концевой переключатель, подключенный к ножке SW1, считается сработавшим по низкому уровню на контакте. \endrussian */
ENDER_SW2_ACTIVE_LOW	= 0x04	/**< \english 1 - Limit switch connected to pin SW2 is triggered by a low level on pin. \endenglish \russian 1 - Концевой переключатель, подключенный к ножке SW2, считается сработавшим по низкому уровню на контакте. \endrussian */

/**
	* \english
	* @name Brake settings flags
	* This is a bit mask for bitwise operations.
	* Specify behavior of brake.
	* May be combined with bitwise OR.
	* \endenglish
	* \russian
	* @name Флаги настроек тормоза
	* Это битовая маска для побитовых операций.
	* Определяют поведение тормоза.
	* Могут быть объединены с помощью побитового ИЛИ.
	* \endrussian
	* @see get_brake_settings
	* @see set_brake_settings
	*/
flagset BrakeFlags:
BRAKE_ENABLED			= 0x01	/**< \english Brake control is enabled if this flag is set. \endenglish \russian Управление тормозом включено, если флаг установлен. \endrussian */
BRAKE_ENG_PWROFF		= 0x02	/**< \english Brake turns the stepper motor power off if this flag is set. \endenglish \russian Тормоз отключает питание шагового мотора, если флаг установлен. \endrussian */

/**
	* \english
	* @name Control flags
	* This is a bit mask for bitwise operations.
	* Specify motor control settings by joystick or buttons.
	* May be combined with bitwise OR.
	* \endenglish
	* \russian
	* @name Флаги управления
	* Это битовая маска для побитовых операций.
	* Определяют параметры управления мотором с помощью джойстика или кнопок.
	* Могут быть объединены с помощью побитового ИЛИ.
	* \endrussian
	* @see get_control_settings
	* @see set_control_settings
	*/
flagset ControlFlags:
CONTROL_MODE_BITS				= 0x03	/**< \english Bits to control the engine by joystick or buttons. \endenglish \russian Биты управления мотором с помощью джойстика или кнопок влево/вправо. \endrussian */
CONTROL_MODE_OFF				= 0x00	/**< \english Control is disabled. \endenglish \russian Управление отключено. \endrussian */
CONTROL_MODE_JOY				= 0x01	/**< \english Control by joystick. \endenglish \russian Управление с помощью джойстика. \endrussian */
CONTROL_MODE_LR					= 0x02	/**< \english Control by left/right buttons. \endenglish \russian Управление с помощью кнопок влево/вправо. \endrussian */
CONTROL_BTN_LEFT_PUSHED_OPEN	= 0x04	/**< \english Pushed left button corresponds to the open contact if this flag is set. \endenglish \russian Нажатая левая кнопка соответствует открытому контакту, если этот флаг установлен. \endrussian */
CONTROL_BTN_RIGHT_PUSHED_OPEN	= 0x08	/**< \english Pushed right button corresponds to open contact if this flag is set. \endenglish \russian Нажатая правая кнопка соответствует открытому контакту, если этот флаг установлен. \endrussian */

/**
	* \english
	* @name Joystick flags
	* This is a bit mask for bitwise operations.
	* Control joystick states.
	* \endenglish
	* \russian
	* @name Флаги джойстика
	* Это битовая маска для побитовых операций.
	* Управляют состояниями джойстика.
	* \endrussian
	* @see set_joystick_settings
	* @see get_joystick_settings
	*/
flagset JoyFlags:
JOY_REVERSE				= 0x01	/**< \english Joystick action is reversed. The joystick deviation to the upper values corresponds to negative speed and vice versa. \endenglish \russian Реверс воздействия джойстика. Отклонение джойстика к большим значениям приводит к отрицательной скорости и наоборот. \endrussian */

/**
	* \english
	* @name Position control flags
	* This is a bit mask for bitwise operations.
	* Specify control position settings.
	* May be combined with bitwise OR.
	* \endenglish
	* \russian
	* @name Флаги контроля позиции
	* Это битовая маска для побитовых операций.
	* Определяют настройки контроля позиции.
	* Могут быть объединены с помощью побитового ИЛИ.
	* \endrussian
	* @see get_ctp_settings
	* @see set_ctp_settings
	*/
flagset CtpFlags:
CTP_ENABLED			    = 0x01	/**< \english The position control is enabled if the flag is set. \endenglish \russian Контроль позиции включен, если флаг установлен. \endrussian */
CTP_BASE			    = 0x02	/**< \english The position control is based on the revolution sensor if this flag is set; otherwise, it is based on the encoder. \endenglish \russian Управление положением основано на датчике вращения, если установлен этот флаг; в противном случае - на энкодере. \endrussian */
CTP_ALARM_ON_ERROR	    = 0x04	/**< \english Set ALARM on mismatch if the flag is set. \endenglish \russian Войти в состояние ALARM при расхождении позиции, если флаг установлен. \endrussian */
REV_SENS_INV	        = 0x08	/**< \english Typically, the sensor is active when it is at 0, and inversion makes active at 1. That is, if you do not invert, it is normal logic - 0 is the activation. \endenglish \russian Сенсор считается активным, когда на нём 0, инвертирование делает активным уровень 1. То есть если не инвертировать, то действует обычная логика - 0 это срабатывание/активация/активное состояние. \endrussian */
CTP_ERROR_CORRECTION    = 0x10 /**< \english Correct errors that appear when slippage occurs if the flag is set. It works only with the encoder. Incompatible with the flag CTP_ALARM_ON_ERROR. \endenglish \russian Корректировать ошибки, возникающие при проскальзывании, если флаг установлен. Работает только с энкодером. Несовместимо с флагом CTP_ALARM_ON_ERROR.\endrussian */

/**
	* \english
	* @name Home settings flags
	* This is a bit mask for bitwise operations.
	* Specify home command behavior.
	* May be combined with bitwise OR.
	* \endenglish
	* \russian
	* @name Флаги настроек команды home
	* Это битовая маска для побитовых операций.
	* Определяют поведение для команды home.
	* Могут быть объединены с помощью побитового ИЛИ.
	* \endrussian
	* @see get_home_settings
	* @see set_home_settings
	* @see command_home
	*/
flagset HomeFlags:
HOME_DIR_FIRST			= 0x0001	/**< \english The flag defines the direction of the 1st motion after execution of the home command. The direction is to the right if the flag is set, and to the left otherwise. \endenglish \russian Определяет направление первоначального движения мотора после поступления команды HOME. Если флаг установлен - вправо; иначе - влево. \endrussian */
HOME_DIR_SECOND			= 0x0002	/**< \english The flag defines the direction of the 2nd motion. The direction is to the right if the flag is set, and to the left otherwise. \endenglish \russian Определяет направление второго движения мотора. Если флаг установлен - вправо; иначе - влево. \endrussian */
HOME_MV_SEC_EN			= 0x0004	/**< \english Use the second phase of calibration to the home position, if set; otherwise the second phase is skipped. \endenglish \russian Если флаг установлен, реализуется второй этап доводки в домашнюю позицию; иначе - этап пропускается. \endrussian */
HOME_HALF_MV			= 0x0008	/**< \english If the flag is set, the stop signals are ignored during the first half-turn of the second movement. \endenglish \russian Если флаг установлен, в начале второго движения первые пол оборота сигналы завершения движения игнорируются. \endrussian */
HOME_STOP_FIRST_BITS	= 0x0030	/**< \english Bits of the first stop selector. \endenglish \russian Биты, отвечающие за выбор сигнала завершения первого движения. \endrussian */
HOME_STOP_FIRST_REV		= 0x0010	/**< \english First motion stops by  revolution sensor. \endenglish \russian Первое движение завершается по сигналу с Revolution sensor. \endrussian */
HOME_STOP_FIRST_SYN		= 0x0020	/**< \english First motion stops by synchronization input. \endenglish \russian Первое движение завершается по сигналу со входа синхронизации. \endrussian */
HOME_STOP_FIRST_LIM		= 0x0030	/**< \english First motion stops by limit switch. \endenglish \russian Первое движение завершается по сигналу с концевого переключателя. \endrussian */
HOME_STOP_SECOND_BITS	= 0x00C0	/**< \english Bits of the second stop selector. \endenglish \russian Биты, отвечающие за выбор сигнала завершения второго движения. \endrussian */
HOME_STOP_SECOND_REV	= 0x0040	/**< \english Second motion stops by  revolution sensor. \endenglish \russian Второе движение завершается по сигналу с Revolution sensor. \endrussian */
HOME_STOP_SECOND_SYN	= 0x0080	/**< \english Second motion stops by synchronization input. \endenglish \russian Второе движение завершается по сигналу со входа синхронизации. \endrussian */
HOME_STOP_SECOND_LIM	= 0x00C0	/**< \english Second motion stops by limit switch. \endenglish \russian Второе движение завершается по сигналу с концевого переключателя. \endrussian */
HOME_USE_FAST           = 0x0100	/**< \english Use the fast algorithm of calibration to the home position, if set; otherwise the traditional algorithm. \endenglish \russian Если флаг установлен, используется быстрый поиск домашней позиции; иначе - традиционный. \endrussian */

/**
	* \english
	* @name UART parity flags
	* This is a bit mask for bitwise operations.
	* \endenglish
	* \russian
	* @name Флаги настроек четности команды UART
	* Это битовая маска для побитовых операций.
	* \endrussian
	*/
flagset UARTSetupFlags:
UART_PARITY_BITS		= 0x03	/**< \english Bits of the parity. \endenglish \russian Биты, отвечающие за выбор четности. \endrussian */
UART_PARITY_BIT_EVEN	= 0x00	/**< \english Parity bit 1, if  even \endenglish \russian Бит 1, если четный \endrussian */
UART_PARITY_BIT_ODD		= 0x01	/**< \english Parity bit 1, if  odd \endenglish \russian Бит 1, если нечетный \endrussian */
UART_PARITY_BIT_SPACE	= 0x02	/**< \english Parity bit always 0 \endenglish \russian Бит четности всегда 0 \endrussian */
UART_PARITY_BIT_MARK	= 0x03	/**< \english Parity bit always 1 \endenglish \russian Бит четности всегда 1 \endrussian */
UART_PARITY_BIT_USE		= 0x04	/**< \english None parity \endenglish \russian Бит чётности не используется, если "0"; бит четности используется, если "1" \endrussian */
UART_STOP_BIT			= 0x08	/**< \english If set - one stop bit, else two stop bit \endenglish \russian Если установлен, один стоповый бит; иначе - 2 стоповых бита \endrussian */

/** 
 	* \english
	* @name Motor Type flags
	* This is a bit mask for bitwise operations.
	* \endenglish
	* \russian
	* @name Флаги типа двигателя
	* Это битовая маска для побитовых операций.
	* \endrussian
	*/
flagset MotorTypeFlags:
MOTOR_TYPE_UNKNOWN		= 0x00	/**< \english Unknown type of engine \endenglish \russian Неизвестный двигатель \endrussian */
MOTOR_TYPE_STEP			= 0x01	/**< \english Step engine \endenglish \russian Шаговый двигатель \endrussian */
MOTOR_TYPE_DC			= 0x02	/**< \english DC engine \endenglish \russian DC двигатель \endrussian */
MOTOR_TYPE_BLDC			= 0x03	/**< \english BLDC engine \endenglish \russian BLDC двигатель \endrussian */

/** 
 	* \english
	* @name Encoder settings flags
	* This is a bit mask for bitwise operations.
	* \endenglish
	* \russian
	* @name Флаги настроек энкодера
	* Это битовая маска для побитовых операций.
	* \endrussian
	*/
flagset EncoderSettingsFlags:
ENCSET_DIFFERENTIAL_OUTPUT			= 0x0001	/**< \english If the flag is set, the encoder has differential output, otherwise single-ended output \endenglish \russian Если флаг установлен, то энкодер имеет дифференциальный выход, иначе - несимметричный выход \endrussian */
ENCSET_PUSHPULL_OUTPUT				= 0x0004	/**< \english If the flag is set the encoder has push-pull output, otherwise open drain output \endenglish \russian Если флаг установлен, то энкодер имеет двухтактный выход, иначе - выход с открытым коллектором \endrussian */
ENCSET_INDEXCHANNEL_PRESENT 		= 0x0010	/**< \english If the flag is set, the encoder has an extra indexed channel \endenglish \russian Если флаг установлен, то энкодер имеет дополнительный индексный канал, иначе - он отсутствует \endrussian */
ENCSET_REVOLUTIONSENSOR_PRESENT 	= 0x0040	/**< \english If the flag is set, the encoder has the revolution sensor \endenglish \russian Если флаг установлен, то энкодер имеет датчик оборотов, иначе - он отсутствует \endrussian */
ENCSET_REVOLUTIONSENSOR_ACTIVE_HIGH = 0x0100	/**< \english If the flag is set, the revolution sensor's active state is high logic state; otherwise, the active state is low logic state \endenglish \russian Если флаг установлен, то активное состояние датчика оборотов соответствует логической 1, иначе - логическому 0 \endrussian */

/** 
 	* \english
	* @name Magnetic brake settings flags
	* This is a bit mask for bitwise operations.
	* \endenglish
	* \russian
	* @name Флаги настроек энкодера
	* Это битовая маска для побитовых операций.
	* \endrussian
	*/
flagset MBSettingsFlags:
MB_AVAILABLE					= 0x01	/**< \english If the flag is set, the magnetic brake is available \endenglish \russian Если флаг установлен, то магнитный тормоз доступен \endrussian */
MB_POWERED_HOLD					= 0x02	/**< \english If this flag is set, the magnetic brake is on when powered \endenglish \russian Если флаг установлен, то магнитный тормоз находится в режиме удержания (активен) при подаче питания \endrussian */

/** 
 	* \english
	* @name Temperature sensor settings flags
	* This is a bit mask for bitwise operations.
	* \endenglish
	* \russian
	* @name Флаги настроек температурного датчика
	* Это битовая маска для побитовых операций.
	* \endrussian
	*/
flagset TSSettingsFlags:
TS_TYPE_BITS					= 0x07	/**< \english Bits of the temperature sensor type \endenglish \russian Биты, отвечающие за тип температурного датчика. \endrussian */
TS_TYPE_UNKNOWN					= 0x00	/**< \english Unknown type of sensor \endenglish \russian Неизвестный сенсор \endrussian */
TS_TYPE_THERMOCOUPLE			= 0x01	/**< \english Thermocouple \endenglish \russian Термопара \endrussian */
TS_TYPE_SEMICONDUCTOR			= 0x02	/**< \english The semiconductor temperature sensor \endenglish \russian Полупроводниковый температурный датчик \endrussian */
TS_AVAILABLE					= 0x08	/**< \english If the flag is set, the temperature sensor is available \endenglish \russian Если флаг установлен, то датчик температуры доступен \endrussian */

/** 
 	* \english
	* @name Temperature sensor settings flags
	* This is a bit mask for bitwise operations.
	* \endenglish
	* \russian
	* @name Флаги настроек температурного датчика
	* Это битовая маска для побитовых операций.
	* \endrussian
	*/
flagset LSFlags:
LS_ON_SW1_AVAILABLE				= 0x01	/**< \english If the flag is set, the limit switch connected to pin SW1 is available \endenglish \russian Если флаг установлен, то концевой переключатель, подключенный к ножке SW1, доступен \endrussian */
LS_ON_SW2_AVAILABLE				= 0x02	/**< \english If the flag is set, the limit switch connected to pin SW2 is available \endenglish \russian Если флаг установлен, то концевой переключатель, подключенный к ножке SW2, доступен \endrussian */
LS_SW1_ACTIVE_LOW				= 0x04	/**< \english If the flag is set, the limit switch connected to pin SW1 is triggered by a low level on the pin \endenglish \russian Если флаг установлен, то концевой переключатель, подключенный к ножке SW1, считается сработавшим по низкому уровню на контакте \endrussian */
LS_SW2_ACTIVE_LOW				= 0x08	/**< \english If the flag is set, the limit switch connected to pin SW2 is triggered by a low level on pin \endenglish \russian Если флаг установлен, то концевой переключатель, подключенный к ножке SW2, считается сработавшим по низкому уровню на контакте \endrussian */
LS_SHORTED						= 0x10	/**< \english If the flag is set, the limit switches are shorted \endenglish \russian Если флаг установлен, то концевые переключатели замкнуты. \endrussian */

/**
	* \english
	* @name Flags of auto-detection of characteristics of windings of the engine.
	* This is a bit mask for bitwise operations.
	* \endenglish
	* \russian
	* @name Флаги автоопределения характеристик обмоток двигателя.
	* Это битовая маска для побитовых операций.
	* \endrussian
	* @see set_emf_settings
	* @see get_emf_settings
	*/
flagset BackEMFFlags:
BACK_EMF_INDUCTANCE_AUTO	= 0x01	/**< \english Flag of auto-detection of inductance of windings of the engine. \endenglish \russian Флаг автоопределения индуктивности обмоток двигателя. \endrussian */
BACK_EMF_RESISTANCE_AUTO	= 0x02	/**< \english Flag of auto-detection of resistance of windings of the engine. \endenglish \russian Флаг автоопределения сопротивления обмоток двигателя. \endrussian */
BACK_EMF_KM_AUTO			= 0x04	/**< \english Flag of auto-detection of electromechanical coefficient of the engine. \endenglish \russian Флаг автоопределения электромеханического коэффициента двигателя. \endrussian */

/**
	* \english
	* @name Controller settings setup
	* Read and write functions for almost all controller settings.
	* \endenglish
	* \russian
	* @name Группа команд настройки контроллера
	* Функции для чтения/записи большинства настроек контроллера.
	* \endrussian
	*/

//@{

/** $XIR
	* \english
	* Feedback settings.
	* @param id An identifier of a device
	* @param[out] IPS number of encoder counts per shaft revolution. Range: 1..65535. The field is obsolete, it is recommended to write 0 to IPS and use the extended CountsPerTurn field. You may need to update the controller firmware to the latest version.
	* @param[out] FeedbackType type of feedback
	* @param[out] FeedbackFlags flags of feedback
	* @param[out] CountsPerTurn number of encoder counts per shaft revolution. Range: 1..4294967295. To use the CountsPerTurn field, write 0 in the IPS field, otherwise the value from the IPS field will be used.
	* \endenglish
	* \russian
	* Чтение настроек обратной связи
	* @param id идентификатор устройства
	* @param[out] IPS количество отсчётов энкодера на оборот вала. Диапазон: 1..65535. Поле устарело, рекомендуется записывать 0 в IPS и использовать расширенное поле CountsPerTurn. Может потребоваться обновление микропрограммы контроллера до последней версии.
	* @param[out] FeedbackType тип обратной связи
	* @param[out] FeedbackFlags флаги обратной связи
	* @param[out] CountsPerTurn количество отсчётов энкодера на оборот вала. Диапазон: 1..4294967295. Для использования поля CountsPerTurn нужно записать 0 в поле IPS, иначе будет использоваться значение из поля IPS.
	* \endrussian
	*/
/** $XIW
	* \english
	* Feedback settings.
	* @param id An identifier of a device
	* @param[in] IPS number of encoder counts per shaft revolution. Range: 1..65535. The field is obsolete, it is recommended to write 0 to IPS and use the extended CountsPerTurn field. You may need to update the controller firmware to the latest version.
	* @param[in] FeedbackType type of feedback
	* @param[in] FeedbackFlags flags of feedback
	* @param[in] CountsPerTurn number of encoder counts per shaft revolution. Range: 1..4294967295. To use the CountsPerTurn field, write 0 in the IPS field, otherwise the value from the IPS field will be used.
	* \endenglish
	* \russian
	* Запись настроек обратной связи.
	* @param id идентификатор устройства
	* @param[in] IPS количество отсчётов энкодера на оборот вала. Диапазон: 1..65535. Поле устарело, рекомендуется записывать 0 в IPS и использовать расширенное поле CountsPerTurn. Может потребоваться обновление микропрограммы контроллера до последней версии.
	* @param[in] FeedbackType тип обратной связи
	* @param[in] FeedbackFlags флаги обратной связи
	* @param[in] CountsPerTurn количество отсчётов энкодера на оборот вала. Диапазон: 1..4294967295. Для использования поля CountsPerTurn нужно записать 0 в поле IPS, иначе будет использоваться значение из поля IPS.
	* \endrussian
	*/
/** $XIS
	* \english
	* Feedback settings.
	* This structure contains feedback settings.
	* \endenglish
	* \russian
	* Настройки обратной связи.
	* Эта структура содержит настройки обратной связи.
	* \endrussian
	*/
command "feedback_settings" universal "fbs" (18)
fields:
    int16u IPS                                  /**< \english The number of encoder counts per shaft revolution. Range: 1..655535. The field is obsolete, it is recommended to write 0 to IPS and use the extended CountsPerTurn field. You may need to update the controller firmware to the latest version. \endenglish \russian Количество отсчётов энкодера на оборот вала. Диапазон: 1..65535. Поле устарело, рекомендуется записывать 0 в IPS и использовать расширенное поле CountsPerTurn. Может потребоваться обновление микропрограммы контроллера до последней версии. \endrussian */
    int8u flag FeedbackType of FeedbackType     /**< \english Type of feedback. This is a bit mask for bitwise operations. \endenglish \russian Тип обратной связи. Это битовая маска для побитовых операций. \endrussian */
    int8u flag FeedbackFlags of FeedbackFlags   /**< \english Flags. This is a bit mask for bitwise operations. \endenglish \russian Флаги. Это битовая маска для побитовых операций. \endrussian */
    int32u CountsPerTurn                        /**< \english The number of encoder counts per shaft revolution. Range: 1..4294967295. To use the CountsPerTurn field, write 0 in the IPS field, otherwise the value from the IPS field will be used. \endenglish \russian Количество отсчётов энкодера на оборот вала. Диапазон: 1..4294967295. Для использования поля CountsPerTurn нужно записать 0 в поле IPS, иначе будет использоваться значение из поля IPS. \endrussian */
    reserved 4

/** $XIR
	* \english
	* Read home settings.
	* This function reads the structure with home position settings.
	* @see home_settings_t
	* @param id An identifier of a device
	* @param[out] home_settings calibrating position settings
	* \endenglish
	* \russian
	* Команда чтения настроек для подхода в home position.
	* Эта функция заполняет структуру настроек, использующихся для калибровки позиции, в память контроллера.
	* @see home_settings_t
	* @param id идентификатор устройства
	* @param[out] home_settings настройки калибровки позиции
	* \endrussian
	*/
/** $XIW
	* \english
	* Set home settings.
	* This function sends home position structure to the controller's memory.
	* @see home_settings_t
	* @param id An identifier of a device
	* @param[in] home_settings calibrating position settings
	* \endenglish
	* \russian
	* Команда записи настроек для подхода в home position.
	* Эта функция записывает структуру настроек, использующихся для калибровки позиции, в память контроллера.
	* @see home_settings_t
	* @param id идентификатор устройства
	* @param[out] home_settings настройки калибровки позиции
	* \endrussian
	*/
/** $XIS
	* \english
	* Position calibration settings.
	* This structure contains settings used in position calibration. It specify behavior of calibration procedure.
	* \endenglish
	* \russian
	* Настройки калибровки позиции.
	* Эта структура содержит настройки, использующиеся при калибровке позиции.
	* \endrussian
	* @see get_home_settings
	* @see set_home_settings
	* @see command_home
	*/
/** $XIRC
	* \english
	* Read user unit home settings.
	* This function reads the structure with home position settings.
	* @see home_settings_calb_t
	* @param id An identifier of a device
	* @param[out] home_settings_calb calibrating position settings
	* @param calibration user unit settings
	* \endenglish
	* \russian
	* Команда чтения настроек для подхода в home position с использованием пользовательских единиц.
	* Эта функция заполняет структуру настроек, использующихся для калибровки позиции, в память контроллера.
	* @see home_settings_calb_t
	* @param id идентификатор устройства
	* @param[out] home_settings_calb настройки калибровки позиции
	* @param calibration настройки пользовательских единиц
	* \endrussian
	*/
/** $XIWC
	* \english
	* Set user unit home settings.
	* This function sends home position structure to the controller's memory.
	* @see home_settings_calb_t
	* @param id An identifier of a device
	* @param[in] home_settings_calb calibrating position settings
	* @param calibration user unit settings
	* \endenglish
	* \russian
	* Команда записи настроек для подхода в home position с использованием пользовательских единиц.
	* Эта функция записывает структуру настроек, использующихся для калибровки позиции, в память контроллера.
	* @see home_settings_calb_t
	* @param id идентификатор устройства
	* @param[in] home_settings_calb настройки калибровки позиции
	* @param calibration настройки пользовательских единиц
	* \endrussian
	*/
/** $XISC
	* \english
	* Position calibration settings which use user units.
	* This structure contains settings used in position calibrating.
	* It specifies behavior of calibrating position.
	* \endenglish
	* \russian
	* Настройки калибровки позиции с использованием пользовательских единиц.
	* Эта структура содержит настройки, использующиеся при калибровке позиции.
	* \endrussian
	* @see get_home_settings_calb
	* @see set_home_settings_calb
	* @see command_home
	*/
command "home_settings" universal "hom" (33)
fields:
	calb float FastHome					/**< \english Speed used for first motion. \endenglish \russian Скорость первого движения. \endrussian */
	normal int32u FastHome				/**< \english Speed used for first motion (full steps). Range: 0..100000. \endenglish \russian Скорость первого движения (в полных шагах). Диапазон: 0..100000 \endrussian */
	normal int8u uFastHome				/**< \english Fractional part of the speed for first motion, microsteps. The microstep size and the range of valid values for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings). \endenglish \russian Дробная часть скорости первого движения в микрошагах (используется только с шаговым двигателем). Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). \endrussian */
	calb float SlowHome					/**< \english Speed used for second motion. \endenglish \russian Скорость второго движения. \endrussian */
	normal int32u SlowHome				/**< \english Speed used for second motion (full steps). Range: 0..100000. \endenglish \russian Скорость второго движения (в полных шагах). Диапазон: 0..100000. \endrussian */
	normal int8u uSlowHome				/**< \english Part of the speed for second motion, microsteps. The microstep size and the range of valid values for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings). \endenglish \russian Дробная часть скорости второго движения в микрошагах (используется только с шаговым двигателем). Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). \endrussian */
	calb float HomeDelta				/**< \english Distance from break point. \endenglish \russian Расстояние отхода от точки останова. \endrussian */
	normal int32s HomeDelta				/**< \english Distance from break point (full steps). \endenglish \russian Расстояние отхода от точки останова (в полных шагах). \endrussian */
	normal int16s uHomeDelta			/**< \english Fractional part of the delta distance, microsteps. The microstep size and the range of valid values for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings). \endenglish \russian Дробная часть расстояния отхода от точки останова в микрошагах (используется только с шаговым двигателем). Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). \endrussian */
	int16u flag HomeFlags of HomeFlags	/**< \english Set of flags specifies the direction and stopping conditions. This is a bit mask for bitwise operations. \endenglish \russian Набор флагов, определяющие такие параметры, как направление и условия останова. Это битовая маска для побитовых операций. \endrussian */
	reserved 9

/** $XIR
	* \english
	* Movement settings read command (speed, acceleration, threshold, etc.).
	* @param id An identifier of a device
	* @param[out] move_settings structure contains move settings: speed, acceleration, deceleration etc.
	* \endenglish
	* \russian
	* Команда чтения настроек перемещения (скорость, ускорение, threshold и скорость в режиме антилюфта).
	* @param id идентификатор устройства
	* @param[out] move_settings структура, содержащая настройки движения: скорость, ускорение, и т.д.
	* \endrussian
	*/
/** $XIW
	* \english
	* Movement settings set command (speed, acceleration, threshold, etc.).
	* @param id An identifier of a device
	* @param[in] move_settings structure contains move settings: speed, acceleration, deceleration etc.
	* \endenglish
	* \russian
	* Команда записи настроек перемещения (скорость, ускорение, threshold и скорость в режиме антилюфта).
	* @param id идентификатор устройства
	* @param[in] move_settings структура, содержащая настройки движения: скорость, ускорение, и т.д.
	* \endrussian
	*/
/** $XIS
	* \english
	* Move settings.
	* \endenglish
	* \russian
	* Настройки движения.
	* \endrussian
	* @see set_move_settings
	* @see get_move_settings
	*/
/** $XIRC
	* \english
	* User unit movement settings read command (speed, acceleration, threshold, etc.).
	* @param id An identifier of a device
	* @param[out] move_settings_calb structure contains move settings: speed, acceleration, deceleration etc.
	* @param calibration user unit settings
	* \endenglish
	* \russian
	* Команда чтения настроек перемещения с использованием пользовательских единиц(скорость, ускорение, threshold и скорость в режиме антилюфта).
	* @param id идентификатор устройства
	* @param[out] move_settings_calb структура, содержащая настройки движения: скорость, ускорение, и т.д.
	* @param calibration настройки пользовательских единиц
	* \endrussian
	*/
/** $XIWC
	* \english
	* User unit movement settings set command (speed, acceleration, threshold, etc.).
	* @param id An identifier of a device
	* @param[in] move_settings_calb structure contains move settings: speed, acceleration, deceleration etc.
	* @param calibration user unit settings
	* \endenglish
	* \russian
	* Команда записи настроек перемещения, с использованием пользовательских единиц (скорость, ускорение, threshold и скорость в режиме антилюфта).
	* @param id идентификатор устройства
	* @param[in] move_settings_calb структура, содержащая настройки движения: скорость, ускорение, и т.д.
	* @param calibration настройки пользовательских единиц
	* \endrussian
	*/
/** $XISC
	* \english
	* User units move settings.
	* \endenglish
	* \russian
	* Настройки движения с использованием пользовательских единиц.
	* \endrussian
	* @see set_move_settings_calb
	* @see get_move_settings_calb
	*/
command "move_settings" universal "mov" (30)
fields:
	calb float Speed					/**< \english Target speed. \endenglish \russian Заданная скорость. \endrussian */
	normal int32u Speed					/**< \english Target speed (for stepper motor: steps/s, for DC: rpm). Range: 0..100000. \endenglish \russian Заданная скорость (для ШД: шагов/c, для DC: rpm). Диапазон: 0..100000. \endrussian */
	normal int8u uSpeed					/**< \english Target speed in microstep fractions/s. The microstep size and the range of valid values for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings). Used with a stepper motor only. \endenglish \russian Заданная скорость в единицах деления микрошага в секунду. Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). Используется только с шаговым мотором. \endrussian */
	calb float Accel					/**< \english Motor shaft acceleration, steps/s^2 (stepper motor) or RPM/s (DC). \endenglish \russian Ускорение, заданное в шагах в секунду^2 (ШД) или в оборотах в минуту за секунду (DC). \endrussian */
	normal int16u Accel					/**< \english Motor shaft acceleration, steps/s^2 (stepper motor) or RPM/s (DC). Range: 1..65535. \endenglish \russian Ускорение, заданное в шагах в секунду^2 (ШД) или в оборотах в минуту за секунду (DC). Диапазон: 1..65535. \endrussian */
	calb float Decel					/**< \english Motor shaft deceleration, steps/s^2 (stepper motor) or RPM/s (DC). \endenglish \russian Торможение, заданное в шагах в секунду^2 (ШД) или в оборотах в минуту за секунду(DC). \endrussian */
	normal int16u Decel					/**< \english Motor shaft deceleration, steps/s^2 (stepper motor) or RPM/s (DC). Range: 1..65535. \endenglish \russian Торможение, заданное в шагах в секунду^2 (ШД) или в оборотах в минуту за секунду (DC). Диапазон: 1..65535. \endrussian */
	calb float AntiplaySpeed			/**< \english Speed in antiplay mode. \endenglish \russian Скорость в режиме антилюфта. \endrussian */
	normal int32u AntiplaySpeed			/**< \english Speed in antiplay mode, full steps/s (stepper motor) or RPM (DC). Range: 0..100000. \endenglish \russian Скорость в режиме антилюфта, заданная в целых шагах/c (ШД) или в оборотах/с(DC). Диапазон: 0..100000. \endrussian */
	normal int8u uAntiplaySpeed			/**< \english Speed in antiplay mode, microsteps/s. The microstep size and the range of valid values for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings). Used with a stepper motor only. \endenglish \russian Скорость в режиме антилюфта, выраженная в микрошагах в секунду. Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). Используется только с шаговым мотором. \endrussian */
	int8u flag MoveFlags of MoveFlags	/**< \english Flags that control movement settings. This is a bit mask for bitwise operations. \endenglish \russian Флаги, управляющие настройкой движения. Это битовая маска для побитовых операций. \endrussian */
	reserved 9

/** $XIR
	* \english
	* Read engine settings.
	* This function reads the structure containing a set of useful motor settings stored in the controller's memory. These settings specify motor shaft movement algorithm, list of limitations and rated characteristics.
	* @see set_engine_settings
	* @param id An identifier of a device
	* @param[out] engine_settings engine settings
	* \endenglish
	* \russian
	* Чтение настроек мотора.
	* Настройки определяют номинальные значения напряжения, тока, скорости мотора, характер движения и тип мотора.
	* Пожалуйста, загружайте новые настройки когда вы меняете мотор, энкодер или позиционер.
	* Помните, что неправильные настройки мотора могут повредить оборудование.
	* @see set_engine_settings
	* @param id идентификатор устройства
	* @param[out] engine_settings структура с настройками мотора
	* \endrussian
	*/
/** $XIW
	* \english
	* Set engine settings.
	* This function sends a structure with a set of engine settings to the controller's memory. These settings specify the motor shaft movement algorithm, list of limitations and rated characteristics. Use it when you change the motor, encoder, positioner, etc. Please note that wrong engine settings may lead to device malfunction, which can cause irreversible damage to the board.
	* @see get_engine_settings
	* @param id An identifier of a device
	* @param[in] engine_settings engine settings
	* \endenglish
	* \russian
	* Запись настроек мотора.
	* Настройки определяют номинальные значения напряжения, тока, скорости мотора, характер движения и тип мотора.
	* Пожалуйста, загружайте новые настройки когда вы меняете мотор, энкодер или позиционер.
	* Помните, что неправильные настройки мотора могут повредить оборудование.
	* @see get_engine_settings
	* @param id идентификатор устройства
	* @param[in] engine_settings структура с настройками мотора
	* \endrussian
	*/
/** $XIS
	* \english
	* Movement limitations and settings related to the motor.
	* This structure contains useful motor settings. These settings specify the motor shaft movement algorithm, list of limitations and rated characteristics. All boards are supplied with the standard set of engine settings on the controller's flash memory. Please load new engine settings when you change the motor, encoder, positioner, etc. Please note that wrong engine settings may lead to device malfunction, which can lead to irreversible damage to the board.
	* \endenglish
	* \russian
	* Ограничения и настройки движения, связанные с двигателем.
	* Эта структура содержит настройки мотора.
	* Настройки определяют номинальные значения напряжения, тока, скорости мотора, характер движения и тип мотора.
	* Пожалуйста, загружайте новые настройки когда вы меняете мотор, энкодер или позиционер.
	* Помните, что неправильные настройки мотора могут повредить оборудование.
	* \endrussian
	* @see set_engine_settings
	* @see get_engine_settings
	*/
/** $XIRC
	* \english
	* Read user unit engine settings.
	* This function reads the structure containing a set of useful motor settings stored in  the controller's memory. These settings specify the motor shaft movement algorithm, list of limitations and rated characteristics.
	* @see set_engine_settings
	* @param id An identifier of a device
	* @param[out] engine_settings_calb engine settings
	* @param calibration user unit settings
	* \endenglish
	* \russian
	* Чтение настроек мотора с использованием пользовательских единиц.
	* Настройки определяют номинальные значения напряжения, тока, скорости мотора, характер движения и тип мотора.
	* Пожалуйста, загружайте новые настройки когда вы меняете мотор, энкодер или позиционер.
	* Помните, что неправильные настройки мотора могут повредить оборудование.
	* @see set_engine_settings
	* @param id идентификатор устройства
	* @param[out] engine_settings_calb структура с настройками мотора
	* @param calibration настройки пользовательских единиц
	* \endrussian
	*/
/** $XIWC
	* \english
	* Set user unit engine settings.
	* This function sends a structure with a set of engine settings to the controller's memory. These settings specify the motor shaft movement algorithm, list of limitations and rated characteristics. Use it when you change the motor, encoder, positioner etc. Please note that wrong engine settings may lead to device malfunction, which can cause irreversible damage to the board.
	* @see get_engine_settings
	* @param id An identifier of a device
	* @param[in] engine_settings_calb engine settings
	* @param calibration user unit settings
	* \endenglish
	* \russian
	* Запись настроек мотора с использованием пользовательских единиц.
	* Настройки определяют номинальные значения напряжения, тока, скорости мотора, характер движения и тип мотора.
	* Пожалуйста, загружайте новые настройки когда вы меняете мотор, энкодер или позиционер.
	* Помните, что неправильные настройки мотора могут повредить оборудование.
	* @see get_engine_settings
	* @param id идентификатор устройства
	* @param[in] engine_settings_calb структура с настройками мотора
	* @param calibration настройки пользовательских единиц
	* \endrussian
	*/
/** $XISC
	* \english
	* Movement limitations and settings, related to the motor. In user units.
	*
	* This structure contains useful motor settings. These settings specify the motor shaft movement algorithm, list of limitations and rated characteristics. All boards are supplied with the standard set of engine settings on the controller's flash memory. Please load new engine settings when you change the motor, encoder, positioner, etc. Please note that wrong engine settings may lead to the device malfunction, that may cause irreversible damage to the board.
	* \endenglish
	* \russian
	* Ограничения и настройки движения, связанные с двигателем, с использованием пользовательских единиц.
	* Эта структура содержит настройки мотора.
	* Настройки определяют номинальные значения напряжения, тока, скорости мотора, характер движения и тип мотора.
	* Пожалуйста, загружайте новые настройки когда вы меняете мотор, энкодер или позиционер.
	* Помните, что неправильные настройки мотора могут повредить оборудование.
	* \endrussian
	* @see set_engine_settings_calb
	* @see get_engine_settings_calb
	*/
command "engine_settings" universal "eng" (34)
fields:
	int16u NomVoltage							/**< \english Rated voltage in tens of mV. Controller will keep the voltage drop on motor below this value if ENGINE_LIMIT_VOLT flag is set (used with DC only). \endenglish \russian Номинальное напряжение мотора в десятках мВ. Контроллер будет сохранять напряжение на моторе не выше номинального, если установлен флаг ENGINE_LIMIT_VOLT (используется только с DC двигателем). \endrussian */
	int16u NomCurrent							/**< \english Rated current (in mA). Controller will keep current consumed by motor below this value if ENGINE_LIMIT_CURR flag is set. Range: 15..8000 \endenglish \russian Номинальный ток через мотор (в мА). Ток стабилизируется для шаговых и может быть ограничен для DC(если установлен флаг ENGINE_LIMIT_CURR). Диапазон: 15..8000 \endrussian */
	calb float NomSpeed							/**< \english Nominal speed. Controller will keep motor speed below this value if ENGINE_LIMIT_RPM flag is set. \endenglish \russian Номинальная скорость. Контроллер будет сохранять скорость мотора не выше номинальной, если установлен флаг ENGINE_LIMIT_RPM. \endrussian */
	normal int32u NomSpeed						/**< \english Nominal (maximum) speed (in whole steps/s or rpm for DC and stepper motor as a master encoder). Controller will keep motor shaft RPM below this value if ENGINE_LIMIT_RPM flag is set. Range: 1..100000. \endenglish \russian Номинальная (максимальная) скорость (в целых шагах/с или rpm для DC и шагового двигателя в режиме ведущего энкодера). Контроллер будет сохранять скорость мотора не выше номинальной, если установлен флаг ENGINE_LIMIT_RPM. Диапазон: 1..100000. \endrussian */
	normal int8u uNomSpeed						/**< \english The fractional part of a nominal speed in microsteps (is only used with stepper motor). Microstep size and the range of valid values for this field depend on selected step division mode (see MicrostepMode field in engine_settings). \endenglish \russian Микрошаговая часть номинальной скорости мотора (используется только с шаговым двигателем). Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). \endrussian */
	int16u flag EngineFlags of EngineFlags		/**< \english Set of flags specify motor shaft movement algorithm and a list of limitations. This is a bit mask for bitwise operations. \endenglish \russian Флаги, управляющие работой мотора. Это битовая маска для побитовых операций. \endrussian */
	calb float Antiplay							/**< \english Number of pulses or steps for backlash (play) compensation procedure. Used if ENGINE_ANTIPLAY flag is set. \endenglish \russian Количество шагов двигателя или импульсов энкодера, на которое позиционер будет отъезжать от заданной позиции для подхода к ней с одной и той же стороны. Используется, если установлен флаг ENGINE_ANTIPLAY. \endrussian */
	normal int16s Antiplay						/**< \english Number of pulses or steps for backlash (play) compensation procedure. Used if ENGINE_ANTIPLAY flag is set. \endenglish \russian Количество шагов двигателя или импульсов энкодера, на которое позиционер будет отъезжать от заданной позиции для подхода к ней с одной и той же стороны. Используется, если установлен флаг ENGINE_ANTIPLAY. \endrussian */
	int8u flag MicrostepMode of MicrostepMode	/**< \english Settings of microstep mode (Used with stepper motor only). the microstep size and the range of valid values for this field depend on the selected step division mode (see MicrostepMode field in engine_settings). This is a bit mask for bitwise operations. \endenglish \russian Настройки микрошагового режима(используется только с шаговым двигателем). Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). Это битовая маска для побитовых операций. \endrussian */
	int16u StepsPerRev							/**< \english Number of full steps per revolution (Used with stepper motor only). Range: 1..65535. \endenglish \russian Количество полных шагов на оборот(используется только с шаговым двигателем). Диапазон: 1..65535. \endrussian */
	reserved 12

/** $XIR
	* \english
	* Return engine type and driver type.
	* @param id An identifier of a device
	* @param[out] entype_settings structure contains motor type and power driver type settings
	* \endenglish
	* \russian
	* Возвращает информацию о типе мотора и силового драйвера.
	* @param id идентификатор устройства
	* @param[out] entype_settings структура, содержащая настройки типа мотора и типа силового драйвера
	* \endrussian
	*/
/** $XIW
	* \english
	* Set engine type and driver type.
	* @param id An identifier of a device
	* @param[in] entype_settings structure contains motor type and power driver type settings
	* \endenglish
	* \russian
	* Запись информации о типе мотора и типе силового драйвера.
	* @param id идентификатор устройства
	* @param[in] entype_settings структура, содержащая настройки типа мотора и типа силового драйвера
	* \endrussian
	*/
/** $XIS
	* \english
	* Engine type and driver type settings.
	* @param id An identifier of a device
	* @param EngineType engine type
	* @param DriverType driver type
	* \endenglish
	* \russian
	* Настройки типа мотора и типа силового драйвера.
	* Эта структура содержит настройки типа мотора и типа силового драйвера.
	* @param id идентификатор устройства
	* @param EngineType тип мотора
	* @param DriverType тип силового драйвера
	* \endrussian
	*/
command "entype_settings" universal "ent" (14)
fields:
	int8u flag EngineType of EngineType	/**< \english Engine type. This is a bit mask for bitwise operations. \endenglish \russian Тип мотора. Это битовая маска для побитовых операций. \endrussian */
	int8u flag DriverType of DriverType	/**< \english Driver type. This is a bit mask for bitwise operations. \endenglish \russian Тип силового драйвера. Это битовая маска для побитовых операций. \endrussian */
	reserved 6

/** $XIR
	* \english
	* Read settings of step motor power control.
	* Used with a stepper motor only.
	* @param id An identifier of a device
	* @param[out] power_settings structure contains settings of step motor power control
	* \endenglish
	* \russian
	* Команда чтения параметров питания мотора. Используется только с шаговым двигателем.
	* Используется только с шаговым двигателем.
	* @param id идентификатор устройства
	* @param[out] power_settings структура, содержащая настройки питания шагового мотора
	* \endrussian
	*/
/** $XIW
	* \english
	* Set settings of step motor power control.
	* Used with a stepper motor only.
	* @param id An identifier of a device
	* @param[in] power_settings structure contains settings of step motor power control
	* \endenglish
	* \russian
	* Команда записи параметров питания мотора. Используется только с шаговым двигателем.
	* @param id идентификатор устройства
	* @param[in] power_settings структура, содержащая настройки питания шагового мотора
	* \endrussian
	*/
/** $XIS
	* \english
	* Step motor power settings.
	* \endenglish
	* \russian
	* Настройки питания шагового мотора.
	* \endrussian
	* @see set_move_settings
	* @see get_move_settings
	*/
command "power_settings" universal "pwr" (20)
fields:
	int8u HoldCurrent						/**< \english Holding current, as percent of the nominal current. Range: 0..100. \endenglish \russian Ток мотора в режиме удержания, в процентах от номинального. Диапазон: 0..100. \endrussian */
	int16u CurrReductDelay					/**< \english Time in ms from going to STOP state to the end of current reduction. \endenglish \russian Время в мс от перехода в состояние STOP до уменьшения тока. \endrussian */
	int16u PowerOffDelay					/**< \english Time in s from going to STOP state to turning power off. \endenglish \russian Время в с от перехода в состояние STOP до отключения питания мотора. \endrussian */
	int16u CurrentSetTime					/**< \english Time in ms to reach the nominal current. \endenglish \russian Время в мс, требуемое для набора номинального тока от 0% до 100%. \endrussian */
	int8u flag PowerFlags of PowerFlags		/**< \english Flags with parameters of power control. This is a bit mask for bitwise operations. \endenglish \russian Флаги параметров управления питанием. Это битовая маска для побитовых операций. \endrussian */
	reserved 6

/** $XIR
	* \english
	* Read protection settings.
	* @param id An identifier of a device
	* @param[out] secure_settings critical parameter settings to protect the hardware
	* \endenglish
	* \russian
	* Команда записи установок защит.
	* @param id идентификатор устройства
	* @param[out] secure_settings настройки, определяющие максимально допустимые параметры, для защиты оборудования
	* \endrussian
	* @see status_t::flags
	*/
/** $XIW
	* \english
	* Set protection settings.
	* @param id An identifier of a device
	* @param secure_settings structure with secure data
	* \endenglish
	* \russian
	* Команда записи установок защит.
	* @param id идентификатор устройства
	* @param secure_settings структура с настройками критических значений
	* \endrussian
	* @see status_t::flags
	*/
/** $XIS
	* \english
	* This structure contains raw analog data from ADC embedded on board.
	* These data are used for device testing and deep recalibration by the manufacturer only.
	* \endenglish
	* \russian
	* Эта структура содержит необработанные данные с АЦП и нормированные значения.
	* Эти данные используются в сервисных целях для тестирования и калибровки устройства.
	* \endrussian
	* @see get_secure_settings
	* @see set_secure_settings
	*/
command "secure_settings" universal "sec" (28)
fields:
	int16u LowUpwrOff					/**< \english Lower voltage limit to turn off the motor, in tens of mV. \endenglish \russian Нижний порог напряжения на силовой части для выключения, десятки мВ. \endrussian */
	int16u CriticalIpwr					/**< \english Maximum motor current which triggers ALARM state, in mA. \endenglish \russian Максимальный ток силовой части, вызывающий состояние ALARM, в мА. \endrussian */
	int16u CriticalUpwr					/**< \english Maximum motor voltage which triggers ALARM state, in tens of mV. \endenglish \russian Максимальное напряжение на силовой части, вызывающее состояние ALARM, десятки мВ. \endrussian */
	int16u CriticalT					/**< \english Maximum temperature, which triggers ALARM state, in tenths of degrees Celsius. \endenglish \russian Максимальная температура контроллера, вызывающая состояние ALARM, в десятых долях градуса Цельсия.\endrussian */
	int16u CriticalIusb					/**< \english Maximum USB current which triggers ALARM state, in mA. \endenglish \russian Максимальный ток USB, вызывающий состояние ALARM, в мА. \endrussian */
	int16u CriticalUusb					/**< \english Maximum USB voltage which triggers ALARM state, in tens of mV. \endenglish \russian Максимальное напряжение на USB, вызывающее состояние ALARM, десятки мВ. \endrussian */
	int16u MinimumUusb					/**< \english Minimum USB voltage which triggers ALARM state, in tens of mV. \endenglish \russian Минимальное напряжение на USB, вызывающее состояние ALARM, десятки мВ. \endrussian */
	int8u flag Flags of SecureFlags		/**< \english Critical parameter flags. This is a bit mask for bitwise operations. \endenglish \russian Флаги критических параметров. Это битовая маска для побитовых операций. \endrussian */
	reserved 7

/**  $XIR
	* \english
	* Read border and limit switches settings.
	* @see set_edges_settings
	* @param id An identifier of a device
	* @param[out] edges_settings edges settings, types of borders, motor behavior and electrical behavior of limit switches
	* \endenglish
	* \russian
	* Чтение настроек границ и концевых выключателей.
	* @see set_edges_settings
	* @param id идентификатор устройства
	* @param[out] edges_settings настройки, определяющие тип границ, поведение мотора при их достижении и параметры концевых выключателей
	* \endrussian
	*/
/** $XIW
	* \english
	* Set border and limit switches settings.
	* @see get_edges_settings
	* @param id An identifier of a device
	* @param[in] edges_settings edges settings, specify types of borders, motor behavior and electrical behavior of limit switches
	* \endenglish
	* \russian
	* Запись настроек границ и концевых выключателей.
	* @see get_edges_settings
	* @param id идентификатор устройства
	* @param[in] edges_settings настройки, определяющие тип границ, поведение мотора при их достижении и параметры концевых выключателей
	* \endrussian
	*/
/**  $XIS
	* \english
	* Edges settings.
	* This structure contains border and limit switches settings. Please load new engine settings when you change positioner, etc. Please note that wrong engine settings may lead to device malfunction, which can cause irreversible damage to the board.
	* \endenglish
	* \russian
	* Настройки границ.
	* Эта структура содержит настройки границ и концевых выключателей.
	* Пожалуйста, загружайте новые настройки когда вы меняете позиционер.
	* Помните, что неправильные настройки мотора могут повредить оборудование.
	* \endrussian
	* @see set_edges_settings
	* @see get_edges_settings
	*/
/**  $XIRC
	* \english
	* Read border and limit switches settings in user units.
	* @see set_edges_settings_calb
	* @param id An identifier of a device
	* @param[out] edges_settings_calb edges settings, types of borders, motor behavior and electrical behavior of limit switches
	* @param calibration user unit settings
	* 
	* \note
	* Attention! Some parameters of the edges_settings_calb structure are corrected by the coordinate correction table.
	*
	* \endenglish
	* \russian
	* Чтение настроек границ и концевых выключателей с использованием пользовательских единиц.
	* @see set_edges_settings_calb
	* @param id идентификатор устройства
	* @param[out] edges_settings_calb настройки, определяющие тип границ, поведение мотора при их достижении и параметры концевых выключателей
	* @param calibration настройки пользовательских единиц
	*
	* \note
	* Внимание! Некоторые параметры структуры edges_settings_calb корректируются таблицей коррекции координат.  
	*
	* \endrussian
	*/
/** $XIWC
	* \english
	* Set border and limit switches settings in user units.
	* @see get_edges_settings_calb
	* @param id An identifier of a device
	* @param[in] edges_settings_calb edges settings, specify types of borders, motor behavior and electrical behavior of limit switches
	* @param calibration user unit settings
	* 
	* \note
	* Attention! Some parameters of the edges_settings_calb structure are corrected by the coordinate correction table.
	*
	* \endenglish
	* \russian
	* Запись настроек границ и концевых выключателей с использованием пользовательских единиц.
	* @see get_edges_settings_calb
	* @param id идентификатор устройства
	* @param[in] edges_settings_calb настройки, определяющие тип границ, поведение мотора при их достижении и параметры концевых выключателей
	* @param calibration настройки пользовательских единиц
	*
	* \note
	* Внимание! Некоторые параметры структуры edges_settings_calb корректируются таблицей коррекции координат.  
	*
	* \endrussian
	*/
/**  $XISC
	* \english
	* User unit edges settings.
	* This structure contains border and limit switches settings. Please load new engine settings when you change positioner, etc. Please note that wrong engine settings may lead to device malfunction, which can cause irreversible damage to the board.
	* \endenglish
	* \russian
	* Настройки границ с использованием пользовательских единиц.
	* Эта структура содержит настройки границ и концевых выключателей.
	* Пожалуйста, загружайте новые настройки когда вы меняете позиционер.
	* Помните, что неправильные настройки мотора могут повредить оборудование.
	* \endrussian
	* @see set_edges_settings_calb
	* @see get_edges_settings_calb
	*/
command "edges_settings" universal "eds" (26)
fields:
	int8u flag BorderFlags of BorderFlags	/**< \english Border flags, specify types of borders and motor behavior at borders. This is a bit mask for bitwise operations. \endenglish \russian Флаги, определяющие тип границ и поведение мотора при их достижении. Это битовая маска для побитовых операций. \endrussian */
	int8u flag EnderFlags of EnderFlags		/**< \english Flags specify electrical behavior of limit switches like order and pulled positions. This is a bit mask for bitwise operations. \endenglish \russian Флаги, определяющие настройки концевых выключателей. Это битовая маска для побитовых операций. \endrussian */
	calb cfloat LeftBorder					/**< \english Left border position, used if BORDER_IS_ENCODER flag is set. Corrected by the table. \endenglish \russian Позиция левой границы, используется если установлен флаг BORDER_IS_ENCODER. Корректируется таблицей. \endrussian */
	normal int32s LeftBorder				/**< \english Left border position, used if BORDER_IS_ENCODER flag is set. \endenglish \russian Позиция левой границы, используется если установлен флаг BORDER_IS_ENCODER. \endrussian */
	normal int16s uLeftBorder				/**< \english Left border position in microsteps (used with stepper motor only). The microstep size and the range of valid values for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings). \endenglish \russian Позиция левой границы в микрошагах (используется только с шаговым двигателем). Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). \endrussian */
	calb cfloat RightBorder					/**< \english Right border position, used if BORDER_IS_ENCODER flag is set. Corrected by the table. \endenglish \russian Позиция правой границы, используется если установлен флаг BORDER_IS_ENCODER. Корректируется таблицей. \endrussian */
	normal int32s RightBorder				/**< \english Right border position, used if BORDER_IS_ENCODER flag is set. \endenglish \russian Позиция правой границы, используется если установлен флаг BORDER_IS_ENCODER. \endrussian */
	normal int16s uRightBorder				/**< \english Right border position in microsteps. Used with a stepper motor only. The microstep size and the range of valid values for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings). \endenglish \russian Позиция правой границы в микрошагах (используется только с шаговым двигателем). Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). \endrussian */
	reserved 6

/**  $XIR
	* \english
	* Read PID settings.
	* This function reads the structure containing a set of motor PID settings stored in the controller's memory. These settings specify the behavior of the PID routine for the positioner. These factors are slightly different for different positioners. All boards are supplied with the standard set of PID settings in the controller's flash memory.
	* @see set_pid_settings
	* @param id An identifier of a device
	* @param[out] pid_settings PID settings
	* \endenglish
	* \russian
	* Чтение ПИД коэффициентов.
	* Эти коэффициенты определяют поведение позиционера.
	* Коэффициенты различны для разных позиционеров.
	* @see set_pid_settings
	* @param id идентификатор устройства
	* @param[out] pid_settings настройки ПИД
	* \endrussian
	*/
/**  $XIW
	* \english
	* Set PID settings.
	* This function sends the structure with a set of PID factors to the controller's memory. These settings specify the behavior of the PID routine for the positioner. These factors are slightly different for different positioners. All boards are supplied with the standard set of PID settings in the controller's flash memory. Please use it for loading new PID settings when you change positioner. Please note that wrong PID settings lead to device malfunction.
	* @see get_pid_settings
	* @param id An identifier of a device
	* @param[in] pid_settings PID settings
	* \endenglish
	* \russian
	* Запись ПИД коэффициентов.
	* Эти коэффициенты определяют поведение позиционера.
	* Коэффициенты различны для разных позиционеров.
	* Пожалуйста, загружайте новые настройки, когда вы меняете мотор или позиционер.
	* @see get_pid_settings
	* @param id идентификатор устройства
	* @param[in] pid_settings настройки ПИД
	* \endrussian
	*/
/**  $XIS
	* \english
	* PID settings.
	* This structure contains factors for PID routine. It specifies the behavior of the voltage PID routine. These factors are slightly different for different positioners. All boards are supplied with the standard set of PID settings in the controller's flash memory. Please load new PID settings when you change positioner. Please note that wrong PID settings lead to device malfunction.
	* \endenglish
	* \russian
	* Настройки ПИД.
	* Эта структура содержит коэффициенты для ПИД регулятора.
	* Они определяют работу ПИД контура напряжения.
	* Эти коэффициенты хранятся во flash памяти контроллера.
	* Пожалуйста, загружайте новые настройки, когда вы меняете мотор или позиционер.
	* Помните, что неправильные настройки ПИД контуров могут повредить оборудование.
	* \endrussian
	* @see set_pid_settings
	* @see get_pid_settings
	*/
command "pid_settings" universal "pid" (48)
fields:
	int16u KpU		/**< \english Proportional gain for voltage PID routine \endenglish \russian Пропорциональный коэффициент ПИД контура по напряжению \endrussian */
	int16u KiU		/**< \english Integral gain for voltage PID routine \endenglish \russian Интегральный коэффициент ПИД контура по напряжению \endrussian */
	int16u KdU		/**< \english Differential gain for voltage PID routine \endenglish \russian Дифференциальный коэффициент ПИД контура по напряжению \endrussian */
	float Kpf		/**< \english Proportional gain for BLDC position PID routine \endenglish \russian Пропорциональный коэффициент ПИД контура по позиции для BLDC \endrussian */
	float Kif		/**< \english Integral gain for BLDC position PID routine \endenglish \russian Интегральный коэффициент ПИД контура по позиции для BLDC \endrussian */
	float Kdf		/**< \english Differential gain for BLDC position PID routine \endenglish \russian Дифференциальный коэффициент ПИД контура по позиции для BLDC \endrussian */
	reserved 24

/**  $XIR
	* \english
	* Read input synchronization settings.
	* This function reads the structure with a set of input synchronization settings, modes, periods and flags that specify the behavior of input synchronization. All boards are supplied with the standard set of these settings.
	* @see set_sync_in_settings
	* @param id An identifier of a device
	* @param[out] sync_in_settings synchronization settings
	* \endenglish
	* \russian
	* Чтение настроек для входного импульса синхронизации.
	* Эта функция считывает структуру с настройками синхронизации, определяющими поведение входа синхронизации, в память контроллера.
	* @see set_sync_in_settings
	* @param id идентификатор устройства
	* @param[out] sync_in_settings настройки синхронизации
	* \endrussian
	*/
/**  $XIW
	* \english
	* Set input synchronization settings.
	* This function sends the structure with a set of input synchronization settings that specify the behavior of input synchronization to the controller's memory. All boards are supplied with the standard set of these settings.
	* @see get_sync_in_settings
	* @param id An identifier of a device
	* @param[in] sync_in_settings synchronization settings
	* \endenglish
	* \russian
	* Запись настроек для входного импульса синхронизации.
	* Эта функция записывает структуру с настройками входного импульса синхронизации, определяющими поведение входа синхронизации, в память контроллера.
	* @see get_sync_in_settings
	* @param id идентификатор устройства
	* @param[in] sync_in_settings настройки синхронизации
	* \endrussian
	*/
/** $XIS
	* \english
	* Synchronization settings.
	*
	* This structure contains all synchronization settings, modes, periods and flags. It specifies the behavior of the input synchronization. All boards are supplied with the standard set of these settings.
	* \endenglish
	* \russian
	* Настройки входной синхронизации.
	* Эта структура содержит все настройки, определяющие поведение входа синхронизации.
	* \endrussian
	* @see get_sync_in_settings
	* @see set_sync_in_settings
	*/
/**  $XIRC
	* \english
	* Read input user unit synchronization settings.
	* This function reads the structure with a set of input synchronization settings, modes, periods and flags that specify the behavior of input synchronization. All boards are supplied with the standard set of these settings.
	* @see set_sync_in_settings_calb
	* @param id An identifier of a device
	* @param[out] sync_in_settings_calb synchronization settings
	* @param calibration user unit settings
	* \endenglish
	* \russian
	* Чтение настроек для входного импульса синхронизации с использованием пользовательских единиц.
	* Эта функция считывает структуру с настройками синхронизации, определяющими поведение входа синхронизации, в память контроллера.
	* @see set_sync_in_settings_calb
	* @param id идентификатор устройства
	* @param[out] sync_in_settings_calb настройки синхронизации
	* @param calibration настройки пользовательских единиц
	* \endrussian
	*/
/**  $XIWC
	* \english
	* Set input user unit synchronization settings.
	* This function sends the structure with a set of input synchronization settings that specify the behavior of input synchronization to the controller's memory. All boards are supplied with the standard set of these settings.
	* @see get_sync_in_settings_calb
	* @param id An identifier of a device
	* @param[in] sync_in_settings_calb synchronization settings
	* @param calibration user unit settings
	* \endenglish
	* \russian
	* Запись настроек для входного импульса синхронизации с использованием пользовательских единиц.
	* Эта функция записывает структуру с настройками входного импульса синхронизации, определяющими поведение входа синхронизации, в память контроллера.
	* @see get_sync_in_settings_calb
	* @param id идентификатор устройства
	* @param[in] sync_in_settings_calb настройки синхронизации
	* @param calibration настройки пользовательских единиц
	* \endrussian
	*/
/** $XISC
	* \english
	* User unit synchronization settings.
	* This structure contains all synchronization settings, modes, periods and flags. It specifies behavior of input synchronization. All boards are supplied with the standard set of these settings.
	* \endenglish
	* \russian
	* Настройки входной синхронизации с использованием пользовательских единиц.
	* Эта структура содержит все настройки, определяющие поведение входа синхронизации.
	* \endrussian
	* @see get_sync_in_settings_calb
	* @see set_sync_in_settings_calb
	*/

command "sync_in_settings" universal "sni" (28)
fields:
	int8u flag SyncInFlags of SyncInFlags		/**< \english Input synchronization flags. This is a bit mask for bitwise operations. \endenglish \russian Флаги синхронизации входа. Это битовая маска для побитовых операций. \endrussian */
	int16u ClutterTime							/**< \english Input synchronization pulse dead time (us). \endenglish \russian Минимальная длительность входного импульса синхронизации для защиты от дребезга (мкс). \endrussian */
	calb float Position							/**< \english Desired position or shift. \endenglish \russian Желаемая позиция или смещение. \endrussian */
	normal int32s Position						/**< \english Desired position or shift (full steps) \endenglish \russian Желаемая позиция или смещение (в полных шагах) \endrussian */
	normal int16s uPosition						/**< \english The fractional part of a position or shift in microsteps. It is used with a stepper motor. The microstep size and the range of valid values for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings). \endenglish \russian Дробная часть позиции или смещения в микрошагах. Используется только с шаговым двигателем. Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). \endrussian */
	calb float Speed							/**< \english Target speed. \endenglish \russian Заданная скорость. \endrussian */
	normal int32u Speed							/**< \english Target speed (for stepper motor: steps/s, for DC: rpm). Range: 0..100000. \endenglish \russian Заданная скорость (для ШД: шагов/c, для DC: rpm). Диапазон: 0..100000. \endrussian */
	normal int8u uSpeed							/**< \english Target speed in microsteps/s. Microstep size and the range of valid values for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings). Used a stepper motor only. \endenglish \russian Заданная скорость в микрошагах в секунду. Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). Используется только с шаговым мотором. \endrussian */
	reserved 8

/** $XIR
	* \english
	* Read output synchronization settings.
	* This function reads the structure containing a set of output synchronization settings, modes, periods and flags that specify the behavior of output synchronization.
	* All boards are supplied with the standard set of these settings.
	* @see set_sync_out_settings
	* @param id An identifier of a device
	* @param[out] sync_out_settings synchronization settings
	* \endenglish
	* \russian
	* Чтение настроек для выходного импульса синхронизации.
	* Эта функция считывает структуру с настройками синхронизации, определяющими поведение выхода синхронизации, в память контроллера.
	* \endrussian
	*/
/** $XIW
	* \english
	* Set output synchronization settings.
	* This function sends the structure with a set of output synchronization settings that specify the behavior of output synchronization to the controller's memory. All boards are supplied with the standard set of these settings.
	* @see get_sync_out_settings
	* @param id An identifier of a device
	* @param[in] sync_out_settings synchronization settings
	* \endenglish
	* \russian
	* Запись настроек для выходного импульса синхронизации.
	* Эта функция записывает структуру с настройками выходного импульса синхронизации, определяющими поведение вывода синхронизации, в память контроллера.
	* @see get_sync_in_settings
	* @param id идентификатор устройства
	* @param[in] sync_out_settings настройки синхронизации
	* \endrussian
	*/
/** $XIS
	* \english
	* Synchronization settings.
	* This structure contains all synchronization settings, modes, periods and flags. It specifies the behavior of the output synchronization. All boards are supplied with the standard set of these settings.
	* \endenglish
	* \russian
	* Настройки выходной синхронизации.
	* Эта структура содержит все настройки, определяющие поведение выхода синхронизации.
	* \endrussian
	* @see get_sync_out_settings
	* @see set_sync_out_settings
	*/
/** $XIRC
	* \english
	* Read output user unit synchronization settings.
	* This function reads the structure containing a set of output synchronization settings, modes, periods and flags that specify the behavior of output synchronization. All boards are supplied with the standard set of these settings.
	* @see set_sync_in_settings_calb
	* @param id An identifier of a device
	* @param[out] sync_out_settings_calb synchronization settings
	* @param calibration user unit settings
	* \endenglish
	* \russian
	* Чтение настроек для выходного импульса синхронизации с использованием пользовательских единиц.
	* Эта функция считывает структуру с настройками синхронизации, определяющими поведение выхода синхронизации, в память контроллера.
	* @see set_sync_in_settings_calb
	* @param id идентификатор устройства
	* @param[in] sync_out_settings_calb настройки синхронизации
	* @param calibration настройки пользовательских единиц
	* \endrussian
	*/
/** $XIWC
	* \english
	* Set output user unit synchronization settings.
	* This function sends the structure with a set of output synchronization settings that specify the behavior of output synchronization to the controller's memory. All boards are supplied with the standard set of these settings.
	* @see get_sync_in_settings_calb
	* @param id An identifier of a device
	* @param[in] sync_out_settings_calb synchronization settings
	* @param calibration user unit settings
	* \endenglish
	* \russian
	* Запись настроек для выходного импульса синхронизации с использованием пользовательских единиц.
	* Эта функция записывает структуру с настройками выходного импульса синхронизации, определяющими поведение вывода синхронизации, в память контроллера.
	* @see get_sync_in_settings_calb
	* @param id идентификатор устройства
	* @param[in] sync_out_settings_calb настройки синхронизации
	* @param calibration настройки пользовательских единиц
	* \endrussian
	*/
/** $XISC
	* \english
	* Synchronization settings which use user units.
	*
	* This structure contains all synchronization settings, modes, periods and flags. It specifies the behavior of the output synchronization. All boards are supplied with the standard set of these settings.
	* \endenglish
	* \russian
	* Настройки выходной синхронизации с использованием пользовательских единиц.
	* Эта структура содержит все настройки, определяющие поведение выхода синхронизации.
	* \endrussian
	* @see get_sync_out_settings_calb
	* @see set_sync_out_settings_calb
	*/

command "sync_out_settings" universal "sno" (16)
fields:
	int8u flag SyncOutFlags of SyncOutFlags	/**< \english Output synchronization flags. This is a bit mask for bitwise operations. \endenglish \russian Флаги синхронизации выхода. Это битовая маска для побитовых операций. \endrussian */
	int16u SyncOutPulseSteps				/**< \english This value specifies the duration of output pulse. It is measured microseconds when SYNCOUT_IN_STEPS flag is cleared or in encoder pulses or motor steps when SYNCOUT_IN_STEPS is set. \endenglish \russian Определяет длительность выходных импульсов в шагах/импульсах энкодера, когда установлен флаг SYNCOUT_IN_STEPS, или в микросекундах если флаг сброшен. \endrussian */
	int16u SyncOutPeriod					/**< \english This value specifies the number of encoder pulses or steps between two output synchronization pulses when SYNCOUT_ONPERIOD is set. \endenglish \russian Период генерации импульсов (в шагах/отсчетах энкодера), используется при установленном флаге SYNCOUT_ONPERIOD. \endrussian */
	calb float Accuracy						/**< \english This is the neighborhood around the target coordinates, every point in which is treated as the target position. Getting in these points cause the stop impulse. \endenglish \russian Это окрестность вокруг целевой координаты (в шагах/отсчетах энкодера), попадание в которую считается попаданием в целевую позицию и генерируется импульс по остановке. \endrussian */
	normal int32u Accuracy					/**< \english This is the neighborhood around the target coordinates, every point in which is treated as the target position. Getting in these points cause the stop impulse. \endenglish \russian Это окрестность вокруг целевой координаты, попадание в которую считается попаданием в целевую позицию и генерируется импульс по остановке. \endrussian */
	normal int8u uAccuracy					/**< \english This is the neighborhood around the target coordinates in microsteps (used with a stepper motor only). The microstep size and the range of valid values for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings). \endenglish \russian Это окрестность вокруг целевой координаты в микрошагах (используется только с шаговым двигателем). Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). \endrussian */

/** $XIR
	* \english
	* Read EXTIO settings.
	* This function reads a structure with a set of EXTIO settings from the controller's memory.
	* @see set_extio_settings
	* @param id An identifier of a device
	* @param[out] extio_settings EXTIO settings
	* \endenglish
	* \russian
	* Команда чтения параметров настройки режимов внешнего ввода/вывода.
	* @see set_extio_settings
	* @param id идентификатор устройства
	* @param[out] extio_settings настройки EXTIO
	* \endrussian
	*/
/** $XIW
	* \english
	* Set EXTIO settings.
	* This function sends the structure with a set of EXTIO settings to the controller's memory. By default, input events are signaled through a rising front, and output states are signaled by a high logic state.
	* @see get_extio_settings
	* @param id An identifier of a device
	* @param[in] extio_settings EXTIO settings
	* \endenglish
	* \russian
	* Команда записи параметров настройки режимов внешнего ввода/вывода.
	* Входные события обрабатываются по фронту. Выходные состояния сигнализируются логическим состоянием.
	* По умолчанию нарастающий фронт считается моментом подачи входного сигнала, а единичное состояние считается активным выходом.
	* @see get_extio_settings
	* @param id идентификатор устройства
	* @param[in] extio_settings настройки EXTIO
	* \endrussian
	*/
/** $XIS
	* \english
	* EXTIO settings.
	*
	* This structure contains all EXTIO settings. By default, input events are signaled through a rising front, and output states are signaled by a high logic state.
	* \endenglish
	* \russian
	* Настройки EXTIO.
	* Эта структура содержит все настройки, определяющие поведение ножки EXTIO.
	* Входные события обрабатываются по фронту. Выходные состояния сигнализируются логическим состоянием.
	* По умолчанию нарастающий фронт считается моментом подачи входного сигнала, а единичное состояние считается активным выходом.
	* \endrussian
	* @see get_extio_settings
	* @see set_extio_settings
	*/

command "extio_settings" universal "eio" (18)
fields:
	int8u flag EXTIOSetupFlags of ExtioSetupFlags	/**< \english Configuration flags of the external I-O. This is a bit mask for bitwise operations. \endenglish \russian Флаги настройки работы внешнего ввода-вывода. Это битовая маска для побитовых операций. \endrussian */
	int8u flag EXTIOModeFlags of ExtioModeFlags		/**< \english Flags mode settings external I-O. This is a bit mask for bitwise operations. \endenglish \russian Флаги настройки режимов внешнего ввода-вывода. Это битовая маска для побитовых операций. \endrussian */
	reserved 10

/** $XIR
	* \english
	* Read break control settings.
	* @param id An identifier of a device
	* @param[out] brake_settings structure contains settings of brake control
	* \endenglish
	* \russian
	* Чтение настроек управления тормозом.
	* @param id идентификатор устройства
	* @param[out] brake_settings структура, содержащая настройки управления тормозом
	* \endrussian
	*/
/** $XIW
	* \english
	* Set brake control settings.
	* @param id An identifier of a device
	* @param[in] brake_settings structure contains brake control settings
	* \endenglish
	* \russian
	* Запись настроек управления тормозом.
	* @param id идентификатор устройства
	* @param[in] brake_settings структура, содержащая настройки управления тормозом
	* \endrussian
	*/
/** $XIS
	* \english
	* Brake settings.
	*
	* This structure contains brake control parameters.
	* \endenglish
	* \russian
	* Настройки тормоза.
	* Эта структура содержит параметры управления тормозом.
	* \endrussian
	* @see set_brake_settings
	* @see get_brake_settings
	*/
command "brake_settings" universal "brk" (25)
fields:
	int16u t1							/**< \english Time in ms between turning on motor power and turning off the brake. \endenglish \russian Время в мс между включением питания мотора и отключением тормоза. \endrussian */
	int16u t2							/**< \english Time in ms between the brake turning off and moving readiness. All moving commands will execute after this interval. \endenglish \russian Время в мс между отключением тормоза и готовностью к движению. Все команды движения начинают выполняться только по истечении этого времени. \endrussian */
	int16u t3							/**< \english Time in ms between motor stop and the brake turning on. \endenglish \russian Время в мс между остановкой мотора и включением тормоза. \endrussian */
	int16u t4							/**< \english Time in ms between turning on the brake and turning off motor power. \endenglish \russian Время в мс между включением тормоза и отключением питания мотора. \endrussian */
	int8u flag BrakeFlags of BrakeFlags	/**< \english Flags. This is a bit mask for bitwise operations. \endenglish \russian Флаги. Это битовая маска для побитовых операций. \endrussian */
	reserved 10

/** $XIR
	* \english
	* Read motor control settings.
	*
    * In case of CTL_MODE=1, joystick motor control is enabled. In this mode, while the joystick is maximally displaced, the engine tends to move at MaxSpeed[i]. i=0 if another value hasn't been set at the previous usage. To change the speed index "i", use the buttons.
	*
    * In case of CTL_MODE=2, the motor is controlled by the left/right buttons. When you click on the button, the motor starts moving in the appropriate direction at a speed MaxSpeed[0]. After Timeout[i], motor moves at speed MaxSpeed[i+1]. At the transition between MaxSpeed[i] and MaxSpeed[i+1] the motor just accelerates/decelerates as usual.
	* @param id An identifier of a device
	* @param[out] control_settings structure contains settings motor control by joystick or buttons left/right.
	* \endenglish
	* \russian
	* Чтение настроек управления мотором.
	* При выборе CTL_MODE=1 включается управление мотором с помощью джойстика.
	* В этом режиме при отклонении джойстика на максимум двигатель стремится
	* двигаться со скоростью MaxSpeed [i], где i=0, если предыдущим использованием
	* этого режима не было выбрано другое i. Кнопки переключают номер скорости i.
	* При выборе CTL_MODE=2 включается управление мотором с помощью кнопок
	* left/right. При нажатии на кнопки двигатель начинает двигаться в соответствующую сторону со скоростью MaxSpeed [0], по истечении времени Timeout[i] мотор
	* двигается со скоростью MaxSpeed [i+1]. При
	* переходе от MaxSpeed [i] на MaxSpeed [i+1] действует ускорение, как обычно.
	* @param id идентификатор устройства
	* @param[out] control_settings структура, содержащая настройки управления мотором с помощью джойстика или кнопок влево/вправо.
	* \endrussian
	*/
/** $XIW
	* \english
	* Read motor control settings.
	*
    * In case of CTL_MODE=1,  joystick motor control is enabled. In this mode, the joystick is maximally displaced, the engine tends to move at MaxSpeed[i]. i=0 if another value hasn't been set at the previous usage. To change the speed index "i", use the buttons.
	*
    * In case of CTL_MODE=2, the motor is controlled by the left/right buttons. When you click on the button, the motor starts moving in the appropriate direction at a speed MaxSpeed[0]. After Timeout[i], motor moves at speed MaxSpeed[i+1]. At the transition between MaxSpeed[i] and MaxSpeed[i+1] the motor just accelerates/decelerates as usual.
	* @param id An identifier of a device
	* @param[in] control_settings structure contains motor control settings.
	* \endenglish
	* \russian
	* Запись настроек управления мотором.
	* При выборе CTL_MODE=1 включается управление мотором с помощью джойстика.
	* В этом режиме при отклонении джойстика на максимум двигатель стремится
	* двигаться со скоростью MaxSpeed [i], где i=0, если предыдущим использованием
	* этого режима не было выбрано другое i. Кнопки переключают номер скорости i.
	* При выборе CTL_MODE=2 включается управление мотором с помощью кнопок
	* left/right. При нажатии на кнопки двигатель начинает двигаться в соответствующую сторону со скоростью MaxSpeed[0], по истечении времени Timeout[i] мотор
	* двигается со скоростью MaxSpeed [i+1]. При
	* переходе от MaxSpeed [i] на MaxSpeed [i+1] действует ускорение, как обычно.
	* @param id идентификатор устройства
	* @param[in] control_settings структура, содержащая настройки управления мотором с помощью джойстика или кнопок влево/вправо.
	* \endrussian
	*/
/** $XIS
	* \english
	* Control settings.
	*
	* This structure contains control parameters.
	*
    * In case of CTL_MODE=1, the joystick motor control is enabled. In this mode, while the joystick is maximally displaced, the engine tends to move at MaxSpeed[i]. i=0 if another value hasn't been set at the previous usage. To change the speed index "i", use the buttons.
	*
    * In case of CTL_MODE=2, the motor is controlled by the left/right buttons. When you click on the button, the motor starts moving in the appropriate direction at a speed MaxSpeed[0]. After Timeout[i], motor moves at speed MaxSpeed[i+1]. At the transition between MaxSpeed[i] and MaxSpeed[i+1] the motor just accelerates/decelerates as usual.
	* \endenglish
	* \russian
	* Настройки управления.
	* При выборе CTL_MODE=1 включается управление мотором с помощью джойстика.
	* В этом режиме при отклонении джойстика на максимум двигатель стремится
	* двигаться со скоростью MaxSpeed [i], где i=0, если предыдущим использованием
	* этого режима не было выбрано другое i. Кнопки переключают номер скорости i.
	* При выборе CTL_MODE=2 включается управление мотором с помощью кнопок
	* left/right. При нажатии на кнопки двигатель начинает двигаться в соответствующую сторону со скоростью MaxSpeed [0], по истечении времени Timeout[i] мотор
	* двигается со скоростью MaxSpeed [i+1]. При
	* переходе от MaxSpeed [i] на MaxSpeed [i+1] действует ускорение, как обычно.
	* \endrussian
	* @see set_control_settings
	* @see get_control_settings
	*/
/** $XIRC
	* \english
	* Set calibrated motor control settings.
	*
    * In case of CTL_MODE=1, the joystick motor control is enabled. In this mode, while the joystick is maximally displaced, the engine tends to move at MaxSpeed[i]. i=0 if another value hasn't been set at the previous usage. To change the speed index "i", use the buttons.
	*
    * In case of CTL_MODE=2, the motor is controlled by the left/right buttons. When you click on the button, the motor starts moving in the appropriate direction at a speed MaxSpeed[0]. After Timeout[i], motor moves at speed MaxSpeed[i+1]. At the transition between MaxSpeed[i] and MaxSpeed[i+1] the motor just accelerates/decelerates as usual.
	* @param id An identifier of a device
	* @param[out] control_settings_calb structure contains user unit motor control settings.
	* @param calibration user unit settings
	* \endenglish
	* \russian
	* Чтение настроек управления мотором с использованием пользовательских единиц.
	* При выборе CTL_MODE=1 включается управление мотором с помощью джойстика.
	* В этом режиме при отклонении джойстика на максимум двигатель стремится
	* двигаться со скоростью MaxSpeed [i], где i=0, если предыдущим использованием
	* этого режима не было выбрано другое i. Кнопки переключают номер скорости i.
	* При выборе CTL_MODE=2 включается управление мотором с помощью кнопок
	* left/right. При нажатии на кнопки двигатель начинает двигаться в соответствующую сторону со скоростью MaxSpeed [0], по истечении времени Timeout[i] мотор
	* двигается со скоростью MaxSpeed [i+1]. При
	* переходе от MaxSpeed [i] на MaxSpeed [i+1] действует ускорение, как обычно.
	* @param id идентификатор устройства
	* @param[out] control_settings_calb структура, содержащая настройки управления мотором с помощью джойстика или кнопок влево/вправо.
	* @param calibration настройки пользовательских единиц
	* \endrussian
	*/
/** $XIWC
	* \english
	* Set motor control settings.
	*
    * In case of CTL_MODE=1, joystick motor control is enabled. In this mode, while the joystick is maximally displaced, the engine tends to move at MaxSpeed[i]. i=0 if another value hasn't been set at the previous usage. To change the speed index "i", use the buttons.
	*
    * In case of CTL_MODE=2, the motor is controlled by the left/right buttons. When you click on the button, the motor starts moving in the appropriate direction at a speed MaxSpeed[0]. After Timeout[i], motor moves at speed MaxSpeed[i+1]. At the transition between MaxSpeed[i] and MaxSpeed[i+1] the motor just accelerates/decelerates as usual.
	* @param id An identifier of a device
	* @param[in] control_settings_calb structure contains motor control settings.
	* @param calibration user unit settings
	* \endenglish
	* \russian
	* Запись настроек управления мотором с использованием пользовательских единиц.
	* При выборе CTL_MODE=1 включается управление мотором с помощью джойстика.
	* В этом режиме при отклонении джойстика на максимум двигатель стремится
	* двигаться со скоростью MaxSpeed [i], где i=0, если предыдущим использованием
	* этого режима не было выбрано другое i. Кнопки переключают номер скорости i.
	* При выборе CTL_MODE=2 включается управление мотором с помощью кнопок
	* left/right. При нажатии на кнопки двигатель начинает двигаться в соответствующую сторону со скоростью MaxSpeed [0], по истечении времени Timeout[i] мотор
	* двигается со скоростью MaxSpeed [i+1]. При
	* переходе от MaxSpeed [i] на MaxSpeed [i+1] действует ускорение, как обычно.
	* @param id идентификатор устройства
	* @param[in] control_settings_calb структура, содержащая настройки управления мотором с помощью джойстика или кнопок влево/вправо.
	* @param calibration настройки пользовательских единиц
	* \endrussian
	*/
/** $XISC
	* \english
	* User unit control settings.
	*
	* This structure contains control parameters.
	*
    * In case of CTL_MODE=1, the joystick motor control is enabled. In this mode, while the joystick is maximally displaced, the engine tends to move at MaxSpeed[i]. i=0 if another value hasn't been set at the previous usage. To change the speed index "i", use the buttons.
	*
    * In case of CTL_MODE=2, the motor is controlled by the left/right buttons. When you click on the button, the motor starts moving in the appropriate direction at a speed MaxSpeed[0]. After Timeout[i], the motor moves at speed MaxSpeed[i+1]. At the transition between MaxSpeed[i] and MaxSpeed[i+1] the motor just accelerates/decelerates as usual.
	* \endenglish
	* \russian
	* Настройки управления с использованием пользовательских единиц.
	* При выборе CTL_MODE=1 включается управление мотором с помощью джойстика.
	* В этом режиме при отклонении джойстика на максимум двигатель стремится
	* двигаться со скоростью MaxSpeed [i], где i=0, если предыдущим использованием
	* этого режима не было выбрано другое i. Кнопки переключают номер скорости i.
	* При выборе CTL_MODE=2 включается управление мотором с помощью кнопок
	* left/right. При нажатии на кнопки двигатель начинает двигаться в соответствующую сторону со скоростью MaxSpeed [0], по истечении времени Timeout[i] мотор
	* двигается со скоростью MaxSpeed [i+1]. При
	* переходе от MaxSpeed [i] на MaxSpeed [i+1] действует ускорение, как обычно.
	* \endrussian
	* @see set_control_settings_calb
	* @see get_control_settings_calb
	*/
command "control_settings" universal "ctl"(93)
fields:
	calb float MaxSpeed [10]			/**< \english Array of speeds used with the joystick and the button control. \endenglish \russian Массив скоростей, использующийся при управлении джойстиком или кнопками влево/вправо. \endrussian */
	normal int32u MaxSpeed [10]			/**< \english Array of speeds (full step) used with the joystick and the button control. Range: 0..100000. \endenglish \russian Массив скоростей (в полных шагах), использующийся при управлении джойстиком или кнопками влево/вправо. Диапазон: 0..100000. \endrussian */
	normal int8u uMaxSpeed [10]			/**< \english Array of speeds (in microsteps) used with the joystick and the button control. The microstep size and the range of valid values for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings). \endenglish \russian Массив скоростей (в микрошагах), использующийся при управлении джойстиком или кнопками влево/вправо. Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). \endrussian */
	int16u Timeout [9]					/**< \english Timeout[i] is timeout in ms. After that, max_speed[i+1] is applied. It's used with the button control only. \endenglish \russian timeout[i] - время в мс, по истечении которого устанавливается скорость max_speed[i+1] (используется только при управлении кнопками). \endrussian */
	int16u MaxClickTime					/**< \english Maximum click time (in ms). Until the expiration of this time, the first speed isn't applied. \endenglish \russian Максимальное время клика (в мс). До истечения этого времени первая скорость не включается. \endrussian */
	int16u flag Flags of ControlFlags	/**< \english Control flags. This is a bit mask for bitwise operations. \endenglish \russian Флаги. Это битовая маска для побитовых операций. \endrussian */
	calb float DeltaPosition			/**< \english Position shift (delta) \endenglish \russian Смещение (дельта) позиции \endrussian */
	normal int32s DeltaPosition			/**< \english Position Shift (delta) (full step) \endenglish \russian Смещение (дельта) позиции (в полных шагах) \endrussian */
	normal int16s uDeltaPosition		/**< \english Fractional part of the shift in micro steps. It's used with a stepper motor only. The microstep size and the range of valid values for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings). \endenglish \russian Дробная часть смещения в микрошагах. Используется только с шаговым двигателем. Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). \endrussian */
	reserved 9

/** $XIR
	* \english
	* Read joystick settings.
	* If joystick position falls outside DeadZone limits, a movement begins. The speed is defined by the joystick's position in the range of the DeadZone limit to the maximum deviation. Joystick positions inside DeadZone limits correspond to zero speed (a soft stop of the motion), and positions beyond Low and High limits correspond to MaxSpeed[i] or -MaxSpeed[i] (see command SCTL), where i = 0 by default and can be changed with the left/right buttons (see command SCTL). If the next speed in the list is zero (both integer and microstep parts), the button press is ignored. The first speed in the list shouldn't be zero. See the Joystick control section on https://doc.xisupport.com for more information.
	* @param id An identifier of a device
	* @param[out] joystick_settings structure contains joystick settings
	* \endenglish
	* \russian
	* Чтение настроек джойстика.
	* При отклонении джойстика более чем на DeadZone от центрального положения начинается движение со скоростью,
	* определяемой отклонением джойстика от DeadZone до 100% отклонения, причем отклонению DeadZone соответствует
	* нулевая скорость, а 100% отклонения соответствует MaxSpeed [i] (см. команду SCTL), где i=0, если предыдущим
	* использованием этого режима не было выбрано другое i.
	* Если следующая скорость в таблице скоростей нулевая (целая и микрошаговая части), то перехода на неё не происходит.
	* DeadZone вычисляется в десятых долях процента отклонения
	* от центра (JoyCenter) до правого или левого максимума. Подробнее см. раздел "Управление с помощью джойстика" на сайте
	* https://doc.xisupport.com.
	* @param id идентификатор устройства
	* @param[out] joystick_settings структура, содержащая настройки джойстика
	* \endrussian
	*/
/** $XIW
	* \english
	* Set joystick position.
	* If joystick position falls outside DeadZone limits, a movement begins. The speed is defined by the joystick's position in the range of the DeadZone limit to the maximum deviation. Joystick positions inside DeadZone limits correspond to zero speed (a soft stop of motion), and positions beyond Low and High limits correspond to MaxSpeed[i] or -MaxSpeed[i] (see command SCTL), where i = 0 by default and can be changed with the left/right buttons (see command SCTL). If the next speed in the list is zero (both integer and microstep parts), the button press is ignored. The first speed in the list shouldn't be zero. See the Joystick control section on https://doc.xisupport.com for more information.
	* @param id An identifier of a device
	* @param[in] joystick_settings structure contains joystick settings
	* \endenglish
	* \russian
	* Запись настроек джойстика.
	* При отклонении джойстика более чем на DeadZone от центрального положения начинается движение со скоростью,
	* определяемой отклонением джойстика от DeadZone до 100% отклонения, причем отклонению DeadZone соответствует
	* нулевая скорость, а 100% отклонения соответствует MaxSpeed [i] (см. команду SCTL), где i=0, если предыдущим
	* использованием этого режима не было выбрано другое i.
	* Если следующая скорость в таблице скоростей нулевая (целая и микрошаговая части), то перехода на неё не происходит.
	* DeadZone вычисляется в десятых долях процента отклонения
	* от центра (JoyCenter) до правого или левого максимума. Подробнее см. раздел "Управление с помощью джойстика" на сайте
	* https://doc.xisupport.com.
	* @param id идентификатор устройства
	* @param[in] joystick_settings структура, содержащая настройки джойстика
	* \endrussian
	*/
/** $XIS
	* \english
	* Joystick settings.
	*
	* This structure contains joystick parameters. If joystick position falls outside the DeadZone limits, a movement begins. Speed is defined by the joystick position in the range of the DeadZone limit to the maximum deviation. Joystick positions inside the DeadZone limits correspond to zero speed (a soft stop of the motion), and positions beyond the Low and High limits correspond to MaxSpeed[i] or -MaxSpeed[i] (see command SCTL), where i = 0 by default and can be changed with left/right buttons (see command SCTL). If the next speed in the list is zero (both integer and microstep parts), the button press is ignored. The first speed in the list shouldn't be zero.
	*
	* The relationship between the deviation and the rate is exponential, which allows for high mobility and accuracy without speed mode switching.
	* \endenglish
	* \russian
	* Настройки джойстика.
	* Команда чтения настроек и калибровки джойстика.
	* При отклонении джойстика более чем на DeadZone от центрального положения начинается движение со скоростью,
	* определяемой отклонением джойстика от DeadZone до 100% отклонения, причем отклонению DeadZone соответствует
	* нулевая скорость, а 100% отклонения соответствует MaxSpeed [i] (см. команду SCTL), где i=0, если предыдущим
	* использованием этого режима не было выбрано другое i.
	* Если следующая скорость в таблице скоростей нулевая (целая и микрошаговая части), то перехода на неё не происходит.
	* DeadZone вычисляется в десятых долях процента отклонения
	* от центра (JoyCenter) до правого или левого максимума. Зависимость между отклонением и скоростью экспоненциальная,
	* что позволяет без переключения режимов скорости сочетать высокую подвижность и точность.
	* \endrussian
	* @see set_joystick_settings
	* @see get_joystick_settings
	*/
command "joystick_settings" universal "joy"(22)
fields:
	int16u JoyLowEnd					/**< \english Joystick lower end position. Range: 0..10000. \endenglish \russian Значение в шагах джойстика, соответствующее нижней границе диапазона отклонения устройства. Должно лежать в пределах. Диапазон: 0..10000. \endrussian */
	int16u JoyCenter					/**< \english Joystick center position. Range: 0..10000. \endenglish \russian Значение в шагах джойстика, соответствующее неотклонённому устройству. Должно лежать в пределах. Диапазон: 0..10000. \endrussian */
	int16u JoyHighEnd					/**< \english Joystick upper end position. Range: 0..10000. \endenglish \russian Значение в шагах джойстика, соответствующее верхней границе диапазона отклонения устройства. Должно лежать в пределах. Диапазон: 0..10000. \endrussian */
	int8u ExpFactor						/**< \english Exponential nonlinearity factor. \endenglish \russian Фактор экспоненциальной нелинейности отклика джойстика. \endrussian */
	int8u DeadZone						/**< \english Joystick dead zone. \endenglish \russian Отклонение от среднего положения, которое не вызывает начала движения (в десятых долях процента). Максимальное мёртвое отклонение +-25.5%, что составляет половину рабочего диапазона джойстика. \endrussian */
	int8u flag JoyFlags of JoyFlags		/**< \english Joystick control flags. This is a bit mask for bitwise operations. \endenglish \russian Флаги управления джойстиком. Это битовая маска для побитовых операций. \endrussian */
	reserved 7

/** $XIR
	* \english
	* Read control position settings (used with stepper motor only).
	* When controlling the step motor with an encoder (CTP_BASE=0), it is possible to detect the loss of steps. The controller knows the number of steps per revolution (GENG::StepsPerRev) and the encoder resolution (GFBS::IPT). When the control is enabled (CTP_ENABLED is set), the controller stores the current position in the steps of SM and the current position of the encoder. Next, the encoder position is converted into steps at each step, and if the difference between the current position in steps and the encoder position is greater than CTPMinError, the flag STATE_CTP_ERROR is set.
    *
    * Alternatively, the stepper motor may be controlled with the speed sensor (CTP_BASE 1). In this mode, at the active edges of the input clock, the controller stores the current value of steps. Then, at each revolution, the controller checks how many steps have been passed. When the difference is over the CTPMinError, the STATE_CTP_ERROR flag is set.
	* @param id An identifier of a device
	* @param[out] ctp_settings structure contains position control settings.
	* \endenglish
	* \russian
	* Чтение настроек контроля позиции(для шагового двигателя).
	* При управлении ШД с энкодером (CTP_BASE 0) появляется возможность обнаруживать потерю шагов. Контроллер знает кол-во шагов на оборот (GENG::StepsPerRev) и разрешение энкодера (GFBS::IPT). При включении контроля (флаг CTP_ENABLED), контроллер запоминает текущую позицию в шагах ШД и текущую позицию энкодера. Далее, на каждом шаге позиция энкодера преобразовывается в шаги и, если разница оказывается больше CTPMinError, устанавливается флаг STATE_CTP_ERROR.
    * При управлении ШД с датчиком оборотов (CTP_BASE 1), позиция контролируется по нему. По активному фронту на входе синхронизации контроллер запоминает текущее значение шагов. Далее, при каждом обороте проверяет, на сколько шагов сместились. При рассогласовании более CTPMinError устанавливается флаг STATE_CTP_ERROR.
	* @param id идентификатор устройства
	* @param[out] ctp_settings структура, содержащая настройки контроля позиции
	* \endrussian
	*/
/** $XIW
	* \english
	* Set control position settings (used with stepper motor only).
	* When controlling the step motor with the encoder (CTP_BASE=0), it is possible to detect the loss of steps. The controller knows the number of steps per revolution (GENG::StepsPerRev) and the encoder resolution (GFBS::IPT). When the control is enabled (CTP_ENABLED is set), the controller stores the current position in the steps of SM and the current position of the encoder. Next, the encoder position is converted into steps at each step, and if the difference between the current position in steps and the encoder position is greater than CTPMinError, the flag STATE_CTP_ERROR is set.
    *
	* Alternatively, the stepper motor may be controlled with the speed sensor (CTP_BASE 1). In this mode, at the active edges of the input clock, the controller stores the current value of steps. Then, at each revolution, the controller checks how many steps have been passed. When the difference is over the CTPMinError, the STATE_CTP_ERROR flag is set.
	* @param id An identifier of a device
	* @param[in] ctp_settings structure contains position control settings.
	* \endenglish
	* \russian
	* Запись настроек контроля позиции(для шагового двигателя).
	* При управлении ШД с энкодером
	* (CTP_BASE 0) появляется возможность обнаруживать потерю шагов. Контроллер знает кол-во шагов на оборот (GENG::StepsPerRev) и разрешение энкодера (GFBS::IPT). При включении контроля (флаг CTP_ENABLED), контроллер запоминает текущую позицию в шагах ШД и текущую позицию энкодера. Далее, на каждом шаге позиция энкодера преобразовывается в шаги и если разница оказывается больше CTPMinError, устанавливается флаг STATE_CTP_ERROR.
    *
	* При управлении ШД с датчиком оборотов (CTP_BASE 1), позиция контролируется по нему. По активному фронту на входе синхронизации контроллер запоминает текущее значение шагов. Далее, при каждом обороте проверяет, на сколько шагов сместились. При рассогласовании более CTPMinError устанавливается флаг STATE_CTP_ERROR.
	* @param id идентификатор устройства
	* @param[in] ctp_settings структура, содержащая настройки контроля позиции
	* \endrussian
	*/
/** $XIS
	* \english
	* Control position settings (used with stepper motor only)
	*
	* When controlling the step motor with the encoder (CTP_BASE=0), it is possible to detect the loss of steps. The controller knows the number of steps per revolution (GENG::StepsPerRev) and the encoder resolution (GFBS::IPT). When the control is enabled (CTP_ENABLED is set), the controller stores the current position in the steps of SM and the current position of the encoder. Next, the encoder position is converted into steps at each step, and if the difference between the current position in steps and the encoder position is greater than CTPMinError, the flag STATE_CTP_ERROR is set.
    *
	* Alternatively, the stepper motor may be controlled with the speed sensor (CTP_BASE 1). In this mode, at the active edges of the input clock, the controller stores the current value of steps. Then, at each revolution, the controller checks how many steps have been passed. When the difference is over the CTPMinError, the STATE_CTP_ERROR flag is set.
	* \endenglish
	* \russian
	* Настройки контроля позиции(для шагового двигателя).
	* При управлении ШД с энкодером (CTP_BASE 0) появляется возможность обнаруживать потерю шагов. Контроллер знает кол-во шагов на оборот (GENG::StepsPerRev) и разрешение энкодера (GFBS::IPT). При включении контроля (флаг CTP_ENABLED), контроллер запоминает текущую позицию в шагах ШД и текущую позицию энкодера. Далее, на каждом шаге позиция энкодера преобразовывается в шаги и если разница оказывается больше CTPMinError, устанавливается флаг STATE_CTP_ERROR и устанавливается состояние ALARM.
    *
	* При управлении ШД с датчиком оборотов (CTP_BASE 1), позиция контролируется по нему. По активному фронту на входе синхронизации контроллер запоминает текущее значение шагов. Далее, при каждом обороте проверяет, на сколько шагов сместились. При рассогласовании более CTPMinError устанавливается флаг STATE_CTP_ERROR и устанавливается состояние ALARM.
	* \endrussian
	* @see set_ctp_settings
	* @see get_ctp_settings
	*/
command "ctp_settings" universal "ctp" (18)
fields:
	int8u CTPMinError				/**< \english The minimum difference between the SM position in steps and the encoder position that causes the setting of the STATE_CTP_ERROR flag. Measured in steps. \endenglish \russian Минимальное отличие шагов ШД от положения энкодера, устанавливающее флаг STATE_RT_ERROR. Измеряется в шагах ШД. \endrussian */
	int8u flag CTPFlags of CtpFlags	/**< \english This is a bit mask for bitwise operations. \endenglish \russian Флаги. Это битовая маска для побитовых операций. \endrussian */
	reserved 10

/** $XIR
	* \english
	* Read UART settings.
	* This function reads the structure containing UART settings.
	* @see uart_settings_t
	* @param Speed UART speed
	* @param[out] uart_settings UART settings
	* \endenglish
	* \russian
	* Команда чтения настроек UART.
	* Эта функция заполняет структуру настроек UART.
	* @see uart_settings_t
	* @param Speed Cкорость UART
	* @param[out] uart_settings настройки UART
	* \endrussian
	*/
/** $XIW
	* \english
	* Set UART settings.
	* This function sends the structure with UART settings to the controller's memory.
	* @see uart_settings_t
	* @param Speed UART speed
	* @param[in] uart_settings UART settings
	* \endenglish
	* \russian
	*  Команда записи настроек UART.
	* Эта функция записывает структуру настроек UART в память контроллера.
	* @see uart_settings_t
	* @param Speed Cкорость UART
	* @param[in] uart_settings настройки UART
	* \endrussian
	*/
/** $XIS
	* \english
	* UART settings.
	*
	* This structure contains UART settings.
	* \endenglish
	* \russian
	* Настройки UART.
	* Эта структура содержит настройки UART.
	* \endrussian
	* @see get_uart_settings
	* @see set_uart_settings
	*/
command "uart_settings" universal "urt" (16)
fields:
	int32u Speed									/**< \english UART baudrate (in bauds) \endenglish \russian Cкорость UART (в бодах) \endrussian */
	int16u flag UARTSetupFlags of UARTSetupFlags	/**< \english UART setup flags. This is a bit mask for bitwise operations. \endenglish \russian Флаги настройки UART. Это битовая маска для побитовых операций. \endrussian */
	reserved 4

/** $XIR
	* \english
	* Read network settings.
	* This function returns the current network settings.
	* @see net_settings_t
	* @param DHCPEnabled DHCP enabled (1) or not (0)
	* @param IPv4Address[4] Array[4] with an IP address
	* @param SubnetMask[4] Array[4] with a subnet mask address
	* @param DefaultGateway[4] Array[4] with a default gateway address
	* \endenglish
	* \russian
	* Команда чтения сететвых настроек.
	* Эта функция возвращает текущие сетевые настройки.
	* @param DHCPEnabled DHCP включен (1) или нет (0)
	* @param IPv4Address[4] Массив[4] с IP-адресом
	* @param SubnetMask[4] Массив[4] с маской подсети
	* @param DefaultGateway[4] Массив[4] со шлюзом сети
	* \endrussian
	*/
/** $XIW
	* \english
	* Set network settings.
	* This function sets the desired network settings.
	* @see net_settings_t
	* @param DHCPEnabled DHCP enabled (1) or not (0)
	* @param IPv4Address[4] Array[4] with an IP address
	* @param SubnetMask[4] Array[4] with a subnet mask address
	* @param DefaultGateway[4] Array[4] with a default gateway address
	* \endenglish
	* \russian
	* Команда записи сететвых настроек.
	* Эта функция меняет сетевые настройки на заданные.
	* @param DHCPEnabled DHCP включен (1) или нет (0)
	* @param IPv4Address[4] Массив[4] с IP-адресом
	* @param SubnetMask[4] Массив[4] с маской подсети
	* @param DefaultGateway[4] Массив[4] со шлюзом сети
	* \endrussian
	*/
/** $XIS
	* \english
	* Network settings.
	* This structure contains network settings.
	* \endenglish
	* \russian
	* Настройки сети.
	* Эта структура содержит настройки сети.
	* \endrussian
	* @see get_network_settings
	* @see set_network_settings
	*/
command "network_settings" universal "net" (38)
fields:
	int8u DHCPEnabled			/**< \english Indicates the method to get the IP-address. It can be either 0 (static) or 1 (DHCP). \endenglish \russian Определяет способ получения IP-адреса каналов. Может принимать значения: 0 — статически, 1 — через DHCP \endrussian */
	int8u IPv4Address[4]		/**< \english IP-address of the device in format x.x.x.x. \endenglish \russian IP-адрес устройства в формате x.x.x.x. \endrussian */
	int8u SubnetMask[4]			/**< \english The mask of the subnet in format x.x.x.x. \endenglish \russian Маска подсети в формате x.x.x.x. \endrussian */
	int8u DefaultGateway[4]		/**< \english Default value of the gateway in format x.x.x.x. \endenglish \russian Шлюз сети по умолчанию в формате x.x.x.x. \endrussian */
	reserved 19

/** $XIR
	* \english
	* Read the password.
	* This function reads the user password for the device's web-page.
	* @see pwd_settings_t
	* @param UserPassword[20] Password for web-page
	* \endenglish
	* \russian
	* Команда чтения пароля к веб-странице.
	* Эта функция пользователяет прочитать пользовательский пароль к веб-странице из памяти контроллера.
	* @param UserPassword[20] Строчка-пароль для доступа к веб-странице
	* \endrussian
	*/
/** $XIW
	* \english
	* Sets the password.
	* This function sets the user password for the device's web-page.
	* @see pwd_settings_t
	* @param UserPassword[20] Password for web-page
	* \endenglish
	* \russian
	* Команда записи пароля к веб-странице.
	* Эта функция меняет пользовательский пароль к веб-странице.
	* @param UserPassword[20] Строчка-пароль для доступа к веб-странице
	* \endrussian
	*/
/** $XIS
	* \english
	* The web-page user password
	* This structure contains the user password.
	* \endenglish
	* \russian
	* Пароль.
	* Эта структура содержит пароль к веб-странице.
	* \endrussian
	* @see get_password_settings
	* @see set_password_settings
	*/
command "password_settings" universal "pwd" (36)
fields:
	char UserPassword[20]		/**< \english Password for the web-page that the user can change with a USB command or via web-page. \endenglish \russian Строчка-пароль для доступа к веб-странице, который пользователь может поменять с помощью USB команды или на веб-странице. \endrussian */
	reserved 10

/** $XIR
	* \english
	* Read calibration settings. Manufacturer only. 
	* This function reads the structure with calibration settings. These settings are used to convert bare ADC values to winding currents in mA and the full current in mA. Parameters are grouped into pairs, XXX_A and XXX_B, representing linear equation coefficients. The first one is the slope, the second one is the constant term. Thus, XXX_Current[mA] = XXX_A[mA/ADC]*XXX_ADC_CODE[ADC] + XXX_B[mA].
	* @see calibration_settings_t
	* @param id An identifier of a device
	* @param[out] calibration_settings calibration settings
	* \endenglish
	* \russian
	* Команда чтения калибровочных коэффициентов. Команда только для производителя.
	* Эта функция заполняет структуру калибровочных коэффициентов. Эти коэффициенты используются для пересчёта кодов АЦП в токи обмоток и полный ток потребления. Коэффициенты сгруппированы в пары, XXX_A и XXX_B; пары представляют собой коэффициенты линейного уравнения. Первый коэффициент - тангенс угла наклона, второй - постоянное смещение. Таким образом, XXX_Current[mA] = XXX_A[mA/ADC]*XXX_ADC_CODE[ADC] + XXX_B[mA].
	* @see calibration_settings_t
	* @param id идентификатор устройства
	* @param[out] calibration_settings калибровочные коэффициенты
	* \endrussian
	*/
/** $XIW
	* \english
	* Set calibration settings. Manufacturer only.
	* This function sends the structure with calibration settings to the controller's memory. These settings are used to convert bare ADC values to winding currents in mA and the full current in mA. Parameters are grouped into pairs, XXX_A and XXX_B, representing linear equation coefficients. The first one is the slope, the second one is the constant term. Thus, XXX_Current[mA] = XXX_A[mA/ADC]*XXX_ADC_CODE[ADC] + XXX_B[mA].
	* @see calibration_settings_t
	* @param id An identifier of a device
	* @param[in] calibration_settings calibration settings
	* \endenglish
	* \russian
	* Команда записи калибровочных коэффициентов. Команда только для производителя.
	* Эта функция записывает структуру калибровочных коэффициентов в память контроллера. Эти коэффициенты используются для пересчёта кодов АЦП в токи обмоток и полный ток потребления. Коэффициенты сгруппированы в пары, XXX_A и XXX_B; пары представляют собой коэффициенты линейного уравнения. Первый коэффициент - тангенс угла наклона, второй - постоянное смещение. Таким образом, XXX_Current[mA] = XXX_A[mA/ADC]*XXX_ADC_CODE[ADC] + XXX_B[mA].
	* @see calibration_settings_t
	* @param id идентификатор устройства
	* @param[in] calibration_settings калибровочные коэффициенты
	* \endrussian
	*/
/** $XIS
	* \english
	* Calibration settings.
	*
	* This structure contains calibration settings. These settings are used to convert bare ADC values to winding currents in mA and the full current in mA. Parameters are grouped into pairs, XXX_A and XXX_B, representing linear equation coefficients. The first one is the slope, the second one is the constant term. Thus, XXX_Current[mA] = XXX_A[mA/ADC]*XXX_ADC_CODE[ADC] + XXX_B[mA].
	* \endenglish
	* \russian
	* Калибровочные коэффициенты.
	* Эта структура содержит калибровочные коэффициенты. Эти коэффициенты используются для пересчёта кодов АЦП в токи обмоток и полный ток потребления. Коэффициенты сгруппированы в пары, XXX_A и XXX_B; пары представляют собой коэффициенты линейного уравнения. Первый коэффициент - тангенс угла наклона, второй - постоянное смещение. Таким образом, XXX_Current[mA] = XXX_A[mA/ADC]*XXX_ADC_CODE[ADC] + XXX_B[mA].
	* \endrussian
	* @see get_calibration_settings
	* @see set_calibration_settings
	*/
command "calibration_settings" universal "cal" (118)
fields:
	float CSS1_A              /**< \english Scaling factor for the analog measurements of the A winding current. \endenglish \russian Коэффициент масштабирования для аналоговых измерений тока в обмотке A. \endrussian */
	float CSS1_B              /**< \english Offset for the analog measurements of the A winding current. \endenglish \russian Коэффициент сдвига для аналоговых измерений тока в обмотке A. \endrussian */
	float CSS2_A              /**< \english Scaling factor for the analog measurements of the B winding current. \endenglish \russian Коэффициент масштабирования для аналоговых измерений тока в обмотке B. \endrussian */
	float CSS2_B              /**< \english Offset for the analog measurements of the B winding current. \endenglish \russian Коэффициент сдвига для аналоговых измерений тока в обмотке B. \endrussian */
	float FullCurrent_A       /**< \english Scaling factor for the analog measurements of the full current. \endenglish \russian Коэффициент масштабирования для аналоговых измерений полного тока. \endrussian */
	float FullCurrent_B       /**< \english Offset for the analog measurements of the full current. \endenglish \russian Коэффициент сдвига для аналоговых измерений полного тока. \endrussian */
	reserved 88

/** $XIR
	* \english
	* Read user's controller name and internal settings from the FRAM.
	* @param id An identifier of a device
	* @param[out] controller_name structure contains previously set user controller name
	* \endenglish
	* \russian
	* Чтение пользовательского имени контроллера и настроек из FRAM.
	* @param id идентификатор устройства
	* @param[out] controller_name структура, содержащая установленное пользовательское имя контроллера и флаги настроек
	* \endrussian
	*/
/** $XIW
	* \english
	* Write user's controller name and internal settings to the FRAM.
	* @param id An identifier of a device
	* @param[in] controller_name structure contains the previously set user's controller name
	* \endenglish
	* \russian
	* Запись пользовательского имени контроллера и настроек в FRAM.
	* @param id идентификатор устройства
	* @param[in] controller_information структура, содержащая информацию о контроллере
	* \endrussian
	*/
/** $XIS
	* \english
	* Controller name and settings flags
	* \endenglish
	* \russian
	* Пользовательское имя контроллера и флаги настройки.
	* \endrussian
	*/
command "controller_name" universal "nmf" (30)
fields:
	char ControllerName[16]					/**< \english User controller name. It may be set by the user. Max string length: 16 characters. \endenglish \russian Пользовательское имя контроллера. Может быть установлено пользователем для его удобства. Максимальная длина строки: 16 символов. \endrussian */
	int8u flag CtrlFlags of ControllerFlags	/**< \english Internal controller settings. This is a bit mask for bitwise operations. \endenglish \russian Настройки контроллера. Это битовая маска для побитовых операций. \endrussian */
	reserved 7

/** $XIR
	* \english
	* Read user data from FRAM.
	* @param id An identifier of a device
	* @param[out] nonvolatile_memory structure contains previously set user data.
	* \endenglish
	* \russian
	* Чтение пользовательских данных из FRAM.
	* @param id идентификатор устройства
	* @param[out] nonvolatile_memory структура, содержащая установленные пользовательские данные
	* \endrussian
	*/
/** $XIW
	* \english
	* Write user data into the FRAM.
	* @param id An identifier of a device
	* @param[in] nonvolatile_memory user data.
	* \endenglish
	* \russian
	* Запись пользовательских данных во FRAM.
	* @param id идентификатор устройства
	* @param[in] nonvolatile_memory структура, содержащая установленные пользовательские данные
	* \endrussian
	*/
/** $XIS
	* \english
	* Structure contains user data to save into the FRAM.
	* \endenglish
	* \russian
	* Пользовательские данные для сохранения во FRAM.
	* \endrussian
	*/
command "nonvolatile_memory" universal "nvm" (36)
fields:
	int32u UserData[7]					/**< \english User data. It may be set by the user. Each element of the array stores only 32 bits of user data. This is important on systems where an int type contains more than 4 bytes. For example, on all amd64 systems. \endenglish \russian Пользовательские данные. Могут быть установлены пользователем для его удобства. Каждый элемент массива хранит только 32 бита пользовательских данных. Это важно на системах где тип int содержит больше чем 4 байта. Например это все системы amd64.\endrussian */
    reserved 2
	
/**  $XIR
	* \english
	* Read electromechanical settings.
	* The settings are different for different stepper motors.
	* @see set_emf_settings
	* @param id An identifier of a device
	* @param[out] emf_settings EMF settings
	* \endenglish
	* \russian
	* Чтение электромеханических настроек шагового двигателя. 
	* Настройки различны для разных двигателей.
	* @see set_emf_settings
	* @param id идентификатор устройства
	* @param[out] emf_settings настройки EMF
	* \endrussian
	*/
/**  $XIW
	* \english
	* Set electromechanical coefficients.
	* The settings are different for different stepper motors. Please set new settings when you change the motor.
	* @see get_emf_settings
	* @param id An identifier of a device
	* @param[in] emf_settings EMF settings
	* \endenglish
	* \russian
	* Запись электромеханических настроек шагового двигателя. 
	* Настройки различны для разных двигателей.
	* Пожалуйста, загружайте новые настройки, когда вы меняете мотор.
	* @see get_emf_settings
	* @param id идентификатор устройства
	* @param[in] emf_settings настройки EMF
	* \endrussian
	*/
/**  $XIS
	* \english
	* EMF settings.
	*
	* This structure contains the data for Electromechanical characteristics (EMF) of the motor. It determines the inductance, resistance, and Electromechanical coefficient of the motor. This data is stored in the flash memory of the controller. Please set new settings when you change the motor. Remember that improper EMF settings may damage the equipment.
	* \endenglish
	* \russian
	* Настройки EMF.
	* Эта структура содержит данные электромеханических характеристик(EMF) двигателя.
	* Они определяют индуктивность, сопротивление и электромеханический коэффициент двигателя.
	* Эти данные хранятся во flash памяти контроллера.
	* Пожалуйста, загружайте новые настройки, когда вы меняете мотор.
	* Помните, что неправильные настройки EMF могут повредить оборудование.
	* \endrussian
	* @see set_emf_settings
	* @see get_emf_settings
	*/
command "emf_settings" universal "emf" (48)
fields:	
	float L									/**< \english Motor winding inductance. \endenglish \russian Индуктивность обмоток двигателя. \endrussian */
	float R									/**< \english Motor winding resistance. \endenglish \russian Сопротивление обмоток двигателя. \endrussian */
	float Km								/**< \english Electromechanical ratio of the motor. \endenglish \russian Электромеханический коэффициент двигателя. \endrussian */
	int8u flag BackEMFFlags of BackEMFFlags	/**< \english Auto-settings stepper motor flags. This is a bit mask for bitwise operations. \endenglish \russian Флаги автонастроек шагового двигателя. Это битовая маска для побитовых операций. \endrussian */
	reserved 29

/**  $XIR
	* \english
	* Read engine advanced settings.
	* @see set_engine_advansed_setup
	* @param id An identifier of a device
	* @param[out] engine_advansed_setup EAS settings
	* \endenglish
	* \russian
	* Чтение расширенных настроек.
	* @see set_engine_advansed_setup
	* @param id идентификатор устройства
	* @param[out] engine_advansed_setup настройки EAS
	* \endrussian
	*/
/**  $XIW
	* \english
	* Set engine advanced settings.
	* @see get_engine_advansed_setup
	* @param id An identifier of a device
	* @param[in] engine_advansed_setup EAS settings
	* \endenglish
	* \russian
	* Запись расширенных настроек. 
	* @see get_engine_advansed_setup
	* @param id идентификатор устройства
	* @param[in] engine_advansed_setup настройки EAS
	* \endrussian
	*/
/**  $XIS
	* \english
	* EAS settings.
	*
	* This structure is intended for setting parameters of algorithms that cannot be attributed to standard Kp, Ki, Kd, and L, R, Km.
	* \endenglish
	* \russian
	* Настройки EAS.
	* Эта структура предназначена для настройки параметров алгоритмов, которые невозможно отнести к стандартным Kp, Ki, Kd и L, R, Km.
	* Эти данные хранятся во flash памяти контроллера.
	* \endrussian
	* @see set_engine_advansed_setup
	* @see get_engine_advansed_setup
	*/
command "engine_advansed_setup" universal "eas" (54)
fields:	
	int16u stepcloseloop_Kw			/**< \english Mixing ratio of the actual and set speed, range [0, 100], default value 50. \endenglish \russian Коэффициент смешения реальной и заданной скорости, диапазон [0, 100], значение по умолчанию 50. \endrussian */
	int16u stepcloseloop_Kp_low		/**< \english Position feedback in the low-speed zone, range [0, 65535], default value 1000. \endenglish \russian Обратная связь по позиции в зоне малых скоростей, диапазон [0, 65535], значение по умолчанию 1000. \endrussian */
	int16u stepcloseloop_Kp_high	/**< \english Position feedback in the high-speed zone, range [0, 65535], default value 33. \endenglish \russian Обратная связь по позиции в зоне больших скоростей, диапазон [0, 65535], значение по умолчанию 33. \endrussian */
	reserved 42

/**  $XIR
	* \english
	* Read extended settings. Currently, it is not in use.
	* @see set_extended_settings 
	* @param id An identifier of a device
	* @param[out] extended_settings EST settings
	* \endenglish
	* \russian
	* Чтение расширенных настроек. В настоящее время не используется.
	* @see set_extended_settings
	* @param id идентификатор устройства
	* @param[out] extended_settings настройки EST
	* \endrussian
	*/
/**  $XIW
	* \english
	* Set extended settings. Currently, it is not in use.
	* @see get_extended_settings
	* @param id An identifier of a device
	* @param[in] extended_settings EST settings
	* \endenglish
	* \russian
	* Запись расширенных настроек. В настоящее время не используется.
	* @see get_extended_settings
	* @param id идентификатор устройства
	* @param[in] extended_settings настройки EST
	* \endrussian
	*/
/**  $XIS
	* \english
	* EST settings
	* This data is stored in the controller's flash memory.
	* This structure is designed for the future. Currently, it is not in use.
	* \endenglish
	* \russian
	* Настройки EST.
	* Эти данные хранятся во flash памяти контроллера.
	* Эта структура на будущее. В настоящее время не используется.
	* \endrussian
	* @see set_extended_settings
	* @see get_extended_settings
	*/
command "extended_settings" universal "est" (46)
fields:	
	int16u Param1				/**< \english \endenglish \russian \endrussian */
	reserved 38

//@}

/**
	* \english
	* @name Group of commands movement control
	*
	* \endenglish
	* \russian
	* @name Группа команд управления движением
	*
	* \endrussian
	*/

//@{

/**  $XIW
	* \english
	* Immediately stops the engine, moves it to the STOP state, and sets switches to BREAK mode (windings are short-circuited). The holding regime is deactivated for DC motors, keeping current in the windings for stepper motors (to control it, see Power management settings).
	*
    * When this command is called, the ALARM flag is reset.
	* @param id An identifier of a device
	* \endenglish
	* \russian
	* Немедленная остановка двигателя, переход в состояние STOP,
	* ключи в режиме BREAK (обмотки накоротко замкнуты), режим
	* "удержания" дезактивируется для DC двигателей, удержание тока
	* в обмотках для шаговых двигателей (с учётом Power management
	* настроек).
	* При вызове этой команды сбрасывается флаг ALARM.
	* @param id идентификатор устройства
	* \endrussian
	*/
command "command_stop" writer "stop" (4)

/** $XIW
	* \english
	* This command adds one element to the FIFO command buffer. Commands are executed at an input clock pulse. Each synchronization pulse launches the action described in SSNI if the buffer is empty. Otherwise, the pulse launches the first  command from the FIFO. In the latter case, the command is erased from the buffer. The number of remaining empty buffer elements can be found in the GETS.
	* @param id An identifier of a device
	* \endenglish
	* \russian
	* Это команда добавляет один элемент в буфер FIFO команд, выполняемых при получении входного импульса синхронизации. Каждый импульс синхронизации либо выполнится то действие, которое описано в SSNI, если буфер пуст, либо самое старое из загруженных в буфер действий временно подменяет скорость и координату в SSNI. В последнем случае это действие стирается из буфера. Количество оставшихся пустыми элементов буфера можно узнать в структуре GETS.
	* @param id идентификатор устройства
	* \endrussian
	*/
/** $XIS
	* \english
	* This command adds one element to the FIFO command buffer.
	* \endenglish
	* \russian
	* Это команда добавляет один элемент в буфер FIFO команд.
	* \endrussian
	*/
/** $XIWC
	* \english
	* This command adds one element to the FIFO command buffer. Commands are executed at an input clock pulse. Each synchronization pulse launches the action described in SSNI if the buffer is empty. Otherwise, the pulse launches the first  command from the FIFO. In the latter case, the command is erased from the buffer. The number of remaining empty buffer elements can be found in the GETS.
	* @param id An identifier of a device
	* @param calibration user unit settings
	* \endenglish
	* \russian
	* Это команда добавляет один элемент в буфер FIFO команд с использованием пользовательских единиц, выполняемых при получении входного импульса синхронизации. Каждый импульс синхронизации либо выполнится то действие, которое описано в SSNI, если буфер пуст, либо самое старое из загруженных в буфер действий временно подменяет скорость и координату в SSNI. В последнем случае это действие стирается из буфера. Количество оставшихся пустыми элементов буфера можно узнать в структуре GETS.
	* @param id идентификатор устройства
	* @param calibration настройки пользовательских единиц
	* \endrussian
	*/
/** $XISC
	* \english
	* This command adds one element to the FIFO commands. Uses user units.
	* \endenglish
	* \russian
	* Это команда добавляет один элемент в буфер FIFO команд с использованием пользовательских единиц.
	* \endrussian
	*/

command "command_add_sync_in_action" writer "asia" (22)
without public
fields:
	calb float Position							/**< \english Desired position or shift. \endenglish \russian Желаемая позиция или смещение. \endrussian */
	normal int32s Position						/**< \english Desired position or shift (full steps) \endenglish \russian Желаемая позиция или смещение (в полных шагах) \endrussian */
	normal int16s uPosition						/**< \english The fractional part of a position or shift in microsteps. Used with stepper motor only. The microstep size and the range of valid values for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings). \endenglish \russian Дробная часть позиции или смещения в микрошагах. Используется только с шаговым двигателем. Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). \endrussian */
	int32u Time									/**< \english Time period in which you want to achieve the desired position in microseconds. \endenglish \russian Время, за которое требуется достичь требуемой позиции, в микросекундах. \endrussian */
	reserved 6

/** $XIW
	* \english
	* Immediately power off the motor regardless its state.
	*
	* Shouldn't be used during motion as the motor could be powered on again automatically to continue movement. The command is designed to manually power off the motor. When automatic power off after stop is required, use the power management system.
	* @param id An identifier of a device
	* \endenglish
	* \russian
	* Немедленное отключение питания двигателя вне зависимости от его состояния. Команда предназначена для ручного управления питанием двигателя. Не следует использовать эту команду для отключения двигателя во время движения, так как питание может снова включиться для завершения движения. Для автоматического управления питанием двигателя и его отключения после остановки следует использовать систему управления электропитанием.
	* @param id идентификатор устройства
	* \endrussian
	* @see get_power_settings
	* @see set_power_settings
	*/
command "command_power_off" writer "pwof" (4)

/** $XIW
	* \english
	* Move to position.
	* Upon receiving the command "move" the engine starts to move with pre-set parameters (speed, acceleration, retention), to the point specified by  Position and uPosition. uPosition sets the microstep position of a stepper motor. In the case of DC motor, this field is ignored.
	* @param id An identifier of a device
	* @param Position position to move.
	* @param uPosition the fractional part of the position to move, in microsteps. The microstep size and the range of valid values for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings).
	* \endenglish
	* \russian
	* При получении команды "move" двигатель начинает перемещаться (если не используется
	* режим "ТТЛСинхроВхода"), с заранее установленными параметрами (скорость, ускорение,
	* удержание), к точке указанной в полях Position, uPosition. Для шагового мотора
	* uPosition задает значение микрошага, для DC мотора это поле не используется.
	* @param id идентификатор устройства
	* @param Position заданная позиция.
	* @param uPosition часть позиции в микрошагах. Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings).	
	* \endrussian
	*/
/** $XIWC
	* \english
	* Move to position using user units.
	* Upon receiving the command "move" the engine starts to move with preset parameters (speed, acceleration, retention), to the point specified by Position.
	* @param id An identifier of a device
	* @param Position position to move.
	* @param calibration user unit settings
	* 
	* \note
	* The parameter Position is adjusted by the correction table.
	*
	* \endenglish
	* \russian
	* Перемещение в позицию  с использованием пользовательских единиц.
	* При получении команды "move" двигатель начинает перемещаться (если не используется
	* режим "ТТЛСинхроВхода"), с заранее установленными параметрами (скорость, ускорение,
	* удержание), к точке указанной в поле Position. 
	* @param id идентификатор устройства
	* @param Position позиция для перемещения
	* @param calibration настройки пользовательских единиц
	*
	* \note
	* Параметр Position корректируется таблицей коррекции.
	*
	* \endrussian
	*/
command "command_move" writer "move" (18)
with inline
fields:
	calb cfloat Position			/**< \english Desired position. Corrected by the table. \endenglish \russian Желаемая позиция. Корректируется таблицей. \endrussian */
	normal int32s Position		/**< \english Desired position (full steps or encoder counts). \endenglish \russian Желаемая позиция (в целых шагах или отсчетах энкодера). \endrussian */
	normal int16s uPosition		/**< \english The fractional part of a position in microsteps. The microstep size and the range of valid values for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings). Used with stepper motor only. \endenglish \russian Дробная часть позиции в микрошагах. Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). Используется только с шаговым двигателем. \endrussian */
	reserved 6

/** $XIW
	* \english
	* Shift by a set offset.
	* Upon receiving the command "movr", the engine starts to move with preset parameters (speed, acceleration, hold) left or right (depending on the sign of DeltaPosition). It moves by the number of steps specified in the fields DeltaPosition and uDeltaPosition. uDeltaPosition sets the microstep offset for a stepper motor. In the case of a DC motor, this field is ignored.
	* @param DeltaPosition shift from initial position.
	* @param uDeltaPosition the fractional part of the offset shift, in microsteps. The microstep size and the range of valid values for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings).
	* @param id An identifier of a device
	* \endenglish
	* \russian
	* Перемещение на заданное смещение.
	* При получении команды "movr" двигатель начинает смещаться (если не используется режим "ТТЛСинхроВхода"), с заранее установленными параметрами (скорость, ускорение, удержание), влево или вправо (зависит от знака DeltaPosition) на количество импульсов указанное в полях DeltaPosition, uDeltaPosition. Для шагового мотора uDeltaPosition задает значение микрошага, для DC мотора это поле не используется.
	* @param DeltaPosition смещение.
	* @param uDeltaPosition часть смещения в микрошагах. Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings).
	* @param id идентификатор устройства
	* \endrussian
	*/
/** $XIWC
	* \english
	* Shift by a set offset using user units.
	* Upon receiving the command "movr", the engine starts to move with preset parameters (speed, acceleration, hold) left or right (depending on the sign of DeltaPosition). It moves by the distance specified in the field DeltaPosition.
	* @param DeltaPosition shift from initial position.
	* @param id An identifier of a device
	* @param user unit calibration settings 
	*
	* \note
	* The final coordinate is calculated using DeltaPosition and adjusted by the correction table. However, the correction cannot be done if the motor moves. movr sets the target position equal to the current target position, shifted by delta. But the library can't determine the current target position while moving. So there is no possibility of calculating the final position and correcting it with the correction table.
	*
	* \endenglish
	* \russian
	* Перемещение на заданное смещение с использованием пользовательских единиц.
	* При получении команды "movr" двигатель начинает смещаться (если не используется режим "ТТЛСинхроВхода"), с заранее установленными параметрами (скорость, ускорение, удержание), влево или вправо (зависит от знака DeltaPosition) на расстояние указанное в поле DeltaPosition.
	* @param DeltaPosition смещение.
	* @param id идентификатор устройства
	* @param calibration настройки пользовательских единиц
	*
	* \note
	* Конечная координата вычисляемая с помощью DeltaPosition, корректируется таблицей коррекции. Однако корректировка не может быть применена в случае поступления команды movr во время движения. Команда movr устанавливает целевую позицию равной текущей целевой плюс дельта. Но точно определить текущую целевую координату во время движения библиотека не может. Поэтому она не может рассчитать конечную позицию и соответсвующую ей коррекцию.
	*
	* \endrussian
	*/
command "command_movr" writer "movr" (18)
with inline
fields:
	calb cdfloat DeltaPosition		/**< \english Position shift (delta). Corrected by the table. \endenglish \russian Смещение (дельта) позиции. Корректируется таблицей. \endrussian */
	normal int32s DeltaPosition		/**< \english Position shift (delta) (full steps or encoder counts) \endenglish \russian Смещение (дельта) позиции (в целых шагах или отсчетах энкодера) \endrussian */
	normal int16s uDeltaPosition	/**< \english Fractional part of the shift in microsteps. Used with stepper motor only. The microstep size and the range of valid values for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings). \endenglish \russian Дробная часть смещения в микрошагах, используется только с шаговым двигателем. Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). \endrussian */
	reserved 6

/** $XIW
	* \english
	* Moving to home position.
	*
    * Moving algorithm:
	*
    * 1) Moves the motor according to the speed FastHome, uFastHome and flag HOME_DIR_FAST until the limit switch if the HOME_STOP_ENDS flag is set. Or moves the motor until the input synchronization signal occurs if the flag HOME_STOP_SYNC is set. Or moves until the revolution sensor signal occurs if the flag HOME_STOP_REV_SN is set.
	*
    * 2) Then moves according to the speed SlowHome, uSlowHome and flag HOME_DIR_SLOW until the input clock signal occurs if the flag HOME_MV_SEC is set. If the flag HOME_MV_SEC is reset, skip this step.
	*
    * 3) Then shifts the motor according to the speed FastHome, uFastHome and the flag HOME_DIR_SLOW by HomeDelta distance, uHomeDelta.
    * 
    * See GHOM/SHOM commands' description for details on home flags.
	*
    * Moving settings can be set by set_home_settings/set_home_settings_calb.
	* @param id An identifier of a device
	* \endenglish
	* \russian
	* Движение в домашнюю позицию.
	*
	* Алгоритм движения:
	*
	* 1) Двигает мотор согласно скоростям FastHome, uFastHome и флагу HOME_DIR_FAST до достижения концевого выключателя, если флаг HOME_STOP_ENDS установлен. Или двигает  до достижения сигнала с входа синхронизации, если установлен флаг HOME_STOP_SYNC. Или до поступления сигнала с датчика оборотов, если установлен флаг HOME_STOP_REV_SN
	*
	* 2) далее двигает согласно скоростям SlowHome, uSlowHome и флагу HOME_DIR_SLOW до достижения сигнала с входа синхронизации, если установлен флаг HOME_MV_SEC. Если флаг HOME_MV_SEC сброшен, пропускаем этот пункт.
	*
	* 3) далее двигает мотор согласно скоростям FastHome, uFastHome и флагу HOME_DIR_SLOW на расстояние HomeDelta, uHomeDelta.
	*
	* Описание флагов и переменных см. описание команд GHOM/SHOM
	* @param id идентификатор устройства
	* \endrussian
	@see home_settings_t
	@see get_home_settings
	@see set_home_settings
	*/
command "command_home" writer "home" (4)

/** $XIW
	* \english
	* Start continuous moving to the left.
	* @param id An identifier of a device
	* \endenglish
	* \russian
	* При получении команды "left" двигатель начинает смещаться, с заранее установленными параметрами (скорость, ускорение), влево.
	* @param id идентификатор устройства
	* \endrussian
	*/
command "command_left" writer "left" (4)

/** $XIW
	* \english
	* Start continuous moving to the right.
	* @param id An identifier of a device
	* \endenglish
	* \russian
	* При получении команды "rigt" двигатель начинает смещаться, с заранее установленными параметрами (скорость, ускорение), вправо.
	* @param id идентификатор устройства
	* \endrussian
	*/
command "command_right" writer "rigt" (4)

/** $XIW
	* \english
	* Upon receiving the command "loft", the engine is shifted from the current position to a distance GENG::Antiplay. Then moves to the initial position.
	* @param id An identifier of a device
	* \endenglish
	* \russian
	* При получении команды "loft" двигатель смещается из текущей точки на
	* расстояние GENG::Antiplay, затем двигается в ту же точку.
	* @param id идентификатор устройства
	* \endrussian
	*/
command "command_loft" writer "loft" (4)

/** $XIW
	* \english
	* Soft stop the engine. The motor is slowing down with the deceleration specified in move_settings.
	* @param id An identifier of a device
	* \endenglish
	* \russian
	* Плавная остановка. Двигатель останавливается с ускорением замедления.
	* @param id идентификатор устройства
	* \endrussian
	*/
command "command_sstp" writer "sstp" (4)

//@}

/**
	* \english
	* @name Group of commands set the current position
	*
	* \endenglish
	* \russian
	* @name Группа команд установки текущей позиции
	*
	* \endrussian
	*/

//@{

/** $XIR
	* \english
	* Reads the value position in steps and microsteps for stepper motor and encoder steps for all engines.
	* @param id An identifier of a device
	* @param[out] get_position structure contains motor position.
	* \endenglish
	* \russian
	* Считывает значение положения в шагах и микрошагах для шагового двигателя и в шагах энкодера
	* всех двигателей.
	* @param id идентификатор устройства
	* @param[out] position структура, содержащая позицию мотора.
	* \endrussian
	*/
/** $XIS
	* \english
	* Position information.
	*
	* A useful structure that contains position value in steps and microsteps for stepper motor and encoder steps for all engines.
	* \endenglish
	* \russian
	* Данные о позиции.
	* Структура содержит значение положения в шагах и
	* микрошагах для шагового двигателя и в шагах энкодера всех
	* двигателей.
	* \endrussian
	*/
/** $XIRC
	* \english
	* Reads position value in user units for stepper motor and encoder steps for all engines.
	* @param id An identifier of a device
	* @param[out] get_position_calb structure contains motor position.
	* @param calibration user unit settings
	* 
	* \note
	* Attention! Some parameters of the get_position_calb structure are corrected by the coordinate correction table.
	*
	* \endenglish
	* \russian
	* Считывает значение положения в пользовательских единицах для шагового двигателя и в шагах энкодера всех двигателей.
	* @param id идентификатор устройства
	* @param[out] get_position_calb структура, содержащая позицию мотора.
	* @param calibration настройки пользовательских единиц
	*
	* \note
	* Внимание! Некоторые параметры структуры get_position_calb корректируются таблицей коррекции координат.  
	*
	* \endrussian
	*/
/** $XISC
	* \english
	* Position information.
	*
	* A useful structure that contains position value in user units for stepper motor and encoder steps for all engines.
	* \endenglish
	* \russian
	* Данные о позиции.
	* Структура содержит значение положения в пользовательских единицах для шагового двигателя и в шагах энкодера всех
	* двигателей.
	* \endrussian
	*/
command "get_position" reader "gpos" (26)
fields:
	calb cfloat Position				/**< \english The position in the engine. Corrected by the table. \endenglish \russian Позиция двигателя. Корректируется таблицей. \endrussian */
	normal int32s Position				/**< \english The position of the whole steps in the engine \endenglish \russian Позиция в основных шагах двигателя \endrussian */
	normal int16s uPosition				/**< \english Microstep position is only used with stepper motors. Microstep size and the range of valid values for this field depend on the selected step division mode (see MicrostepMode field in engine_settings). \endenglish \russian Позиция в микрошагах (используется только с шаговыми двигателями). Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). \endrussian */
	int64s EncPosition					/**< \english Encoder position.  \endenglish \russian Позиция энкодера. \endrussian */
	reserved 6

/** $XIW
	* \english
	* Sets position in steps and microsteps for stepper motor. Sets encoder position for all engines.
	* @param id An identifier of a device
	* @param[out] set_position structure contains motor position.
	* \endenglish
	* \russian
	* Устанавливает произвольное значение положения в шагах и
	* микрошагах для шагового двигателя и в шагах энкодера для всех
	* двигателей.
	* @param id идентификатор устройства
	* @param[out] position структура, содержащая позицию мотора.
	* \endrussian
	*/
/** $XIS
	* \english
	* Position information.
	*
	* A useful structure that contains position value in steps and microsteps for stepper motor and encoder steps for all engines.
	* \endenglish
	* \russian
	* Данные о позиции.
	* Структура содержит значение положения в шагах и микрошагах для шагового двигателя и в шагах энкодера всех двигателей.
	* \endrussian
	*/
/** $XIWC
	* \english
	* Sets any position value and encoder value of all engines. In user units.
	* @param id An identifier of a device
	* @param[out] set_position_calb structure contains motor position.
	* @param calibration user unit settings
	* \endenglish
	* \russian
	* Устанавливает произвольное значение положения и значение энкодера всех двигателей с использованием пользовательских единиц.
	* @param id идентификатор устройства
	* @param[out] set_position_calb структура, содержащая позицию мотора.
	* @param calibration настройки пользовательских единиц
	* \endrussian
	*/
/** $XISC
	* \english
	* User unit position information.
	*
	* A useful structure that contains position value in steps and microsteps for stepper motor and encoder steps of all engines.
	* \endenglish
	* \russian
	* Данные о позиции с использованием пользовательских единиц.
	* Структура содержит значение положения в шагах и микрошагах для шагового двигателя и в шагах энкодера всех двигателей.
	* \endrussian
	*/
command "set_position" writer "spos" (26)
fields:
	calb float Position						/**< \english The position in the engine. \endenglish \russian Позиция двигателя. \endrussian */
	normal int32s Position					/**< \english The position of the whole steps in the engine \endenglish \russian Позиция в основных шагах двигателя \endrussian */
	normal int16s uPosition					/**< \english Microstep position is only used with stepper motors. Microstep size and the range of valid values for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings). \endenglish \russian Позиция в микрошагах (используется только с шаговыми двигателями). Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). \endrussian */
	int64s EncPosition						/**< \english Encoder position.  \endenglish \russian Позиция энкодера. \endrussian */
	int8u flag PosFlags of PositionFlags	/**< \english Position flags. This is a bit mask for bitwise operations. \endenglish \russian Флаги. Это битовая маска для побитовых операций. \endrussian */
	reserved 5

/** $XIW
	* \english
	* Sets the current position to 0. Sets the target position of the move command and the movr command to zero for all cases except for movement to the target position. In the latter case, the target position is calculated so that the absolute position of the destination stays the same. For example, if we were at 400 and moved to 500, then the command Zero makes the current position 0 and the position of the destination 100. It does not change the mode of movement. If the motion is carried, it continues, and if the engine is in the "hold", the type of retention remains.
	* @param id An identifier of a device
	* \endenglish
	* \russian
	* Устанавливает текущую позицию равной 0. Устанавливает позицию, в которую осуществляется движение по командам move и movr, равной нулю во всех случаев, кроме движения к позиции назначения. В последнем случае позиция назначения пересчитывается так, что в абсолютном положении точка назначения не меняется. То есть если мы находились в точке 400 и двигались к 500, то команда Zero делает текущую позицию 0, а позицию назначения - 100. Не изменяет режим движения т.е. если движение осуществлялось, то оно продолжается; если мотор находился в режиме "удержания", то тип удержания сохраняется.
	* @param id идентификатор устройства
	* \endrussian
	*/
command "command_zero" writer "zero" (4)

//@}

/**
	* \english
	* @name Group of save settings and load settings commands
	*
	* \endenglish
	* \russian
	* @name Группа команд сохранения и загрузки настроек
	*
	* \endrussian
	*/

//@{

/** $XIW
	* \english
	* Save all settings from the controller's RAM to the controller's flash memory, replacing previous data in the flash memory.
	* @param id An identifier of a device
	* \endenglish
	* \russian
	* При получении команды контроллер выполняет операцию сохранения текущих настроек во встроенную энергонезависимую память контроллера.
	* @param id идентификатор устройства
	* \endrussian
	*/
command "save_settings" writer "save" (4)

/** $XIW
	* \english
	* Read all settings from the controller's flash memory to the controller's RAM, replacing previous data in the RAM.
	* @param id An identifier of a device
	* \endenglish
	* \russian
	* Чтение всех настроек контроллера из flash памяти в оперативную, заменяя текущие настройки.
	* @param id идентификатор устройства
	* \endrussian
	*/
command "read_settings" writer "read" (4)

/** $XIW
	* \english
	* Save important settings (calibration coefficients, etc.) from the controller's RAM to the controller's flash memory, replacing previous data in the flash memory.
	* @param id An identifier of a device
	* \endenglish
	* \russian
	* При получении команды контроллер выполняет операцию сохранения важных настроек (калибровочные коэффициенты и т.п.) во встроенную энергонезависимую память контроллера.
	* @param id идентификатор устройства
	* \endrussian
	*/
command "save_robust_settings" writer "sars" (4)

/** $XIW
	* \english
	* Read important settings (calibration coefficients, etc.) from the controller's flash memory to the controller's RAM, replacing previous data in the RAM.
	* @param id An identifier of a device
	* \endenglish
	* \russian
	* Чтение важных настроек (калибровочные коэффициенты и т.п.) контроллера из flash памяти в оперативную, заменяя текущие настройки.
	* @param id идентификатор устройства
	* \endrussian
	*/
command "read_robust_settings" writer "rers" (4)

/** $XIW
	* \english
	* Save settings from the controller's RAM to the stage's EEPROM.
	* Can be used by the manufacturer only.
	* @param id An identifier of a device
	* \endenglish
	* \russian
	* Запись настроек контроллера в EEPROM память позиционера
	* Функция должна использоваться только производителем.
	* @param id идентификатор устройства
	* \endrussian
	*/
command "eesave_settings" writer "eesv" (4)

/** $XIW
	* \english
	* Read settings from the stage's EEPROM to the controller's RAM. This operation is performed automatically at the connection of the stage with an EEPROM to the controller. Can be used by the manufacturer only.
	* @param id An identifier of a device
	* \endenglish
	* \russian
	* Чтение настроек контроллера из EEPROM памяти позиционера. Эта операция также автоматически выполняется при подключении позиционера с EEPROM памятью. Функция должна использоваться только производителем.
	* @param id идентификатор устройства
	* \endrussian
	*/
command "eeread_settings" writer "eerd" (4)

//@}

/**
	* \english
	* @name A group of get status commands
	*
	* \endenglish
	* \russian
	* @name Группа команд получения статуса контроллера
	*
	* \endrussian
	*/

//@{

/** $XIR
	* \english
	* Return device state.
	* A useful function that fills the structure with a snapshot of the controller state, including speed, position, and boolean flags.
	* @param id An identifier of a device
	* @param[out] status structure with a snapshot of the controller state
	* \endenglish
	* \russian
	* Возвращает информацию о текущем состоянии устройства.
	* @param id идентификатор устройства
	* @param[out] status структура с информацией о текущем состоянии устройства
	* \endrussian
	*/
/** $XIS
	* \english
	* Device state.
	*
	* A useful structure that contains current controller state, including speed, position, and boolean flags.
	* \endenglish
	* \russian
	* Состояние устройства.
	* Эта структура содержит основные параметры текущего состоянии контроллера такие как скорость, позиция и флаги состояния.
	* \endrussian
	*/
/** $XIRC
	* \english
	* Return the device's user unit state.
	* A useful function that fills the structure with a snapshot of controller state, including speed, position, and boolean flags.
	* @param id An identifier of a device
	* @param[out] status structure with snapshot of controller state
	* @param calibration user unit settings
	* \endenglish
	* \russian
	* Возвращает информацию о текущем состоянии устройства с использованием пользовательских единиц.
	* @param id идентификатор устройства
	* @param[out] status структура с информацией о текущем состоянии устройства
	* @param calibration настройки пользовательских единиц
	* \endrussian
	*/
/** $XISC
	* \english
	* User unit device's state.
	*
	* A useful structure that contains current controller state, including speed, position, and boolean flags.
	* \endenglish
	* \russian
	* Состояние устройства с использованием пользовательских единиц.
	* Эта структура содержит основные параметры текущего состоянии контроллера такие как скорость, позиция и флаги состояния.
	* \endrussian
	*/
command "status_impl" reader "gets" (54)
without lock, public
with publicstruct
fields:
	int8u flag MoveSts of MoveState		/**< \english Move state. This is a bit mask for bitwise operations. \endenglish \russian Состояние движения. Это битовая маска для побитовых операций. \endrussian */
	int8u flag MvCmdSts of MvcmdStatus	/**< \english Move command state. This is a bit mask for bitwise operations. \endenglish \russian Состояние команды движения (касается command_move, command_movr, command_left, command_right, command_stop, command_home, command_loft). Это битовая маска для побитовых операций. \endrussian */
	int8u flag PWRSts of PowerState		/**< \english Power state of the stepper motor (used with stepper motor only). This is a bit mask for bitwise operations. \endenglish \russian Состояние питания шагового двигателя (используется только с шаговым двигателем). Это битовая маска для побитовых операций. \endrussian */
	int8u flag EncSts of EncodeStatus	/**< \english Encoder state. This is a bit mask for bitwise operations. \endenglish \russian Состояние энкодера. Это битовая маска для побитовых операций. \endrussian */
	int8u flag WindSts of WindStatus	/**< \english Windings state. This is a bit mask for bitwise operations. \endenglish \russian Состояние обмоток. Это битовая маска для побитовых операций. \endrussian */
	calb cfloat CurPosition				/**< \english Current position. Corrected by the table. \endenglish \russian Первичное поле, в котором хранится текущая позиция, как бы ни была устроена обратная связь. В случае работы с DC-мотором в этом поле находится текущая позиция по данным с энкодера, в случае работы с ШД-мотором в режиме, когда первичными являются импульсы, подаваемые на мотор. Корректируется таблицей. \endrussian */
	normal int32s CurPosition			/**< \english Current position. \endenglish \russian Первичное поле, в котором хранится текущая позиция, как бы ни была устроена обратная связь. В случае работы с DC-мотором в этом поле находится текущая позиция по данным с энкодера, в случае работы с ШД-мотором в режиме, когда первичными являются импульсы, подаваемые на мотор, в этом поле содержится целое значение шагов текущей позиции. \endrussian */
	normal int16s uCurPosition			/**< \english Step motor shaft position in microsteps. The microstep size and the range of valid values for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings). Used with stepper motors only. \endenglish \russian Дробная часть текущей позиции в микрошагах. Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). Используется только с шаговым двигателем. \endrussian */
	int64s EncPosition					/**< \english Current encoder position. \endenglish \russian Текущая позиция по данным с энкодера в импульсах энкодера, используется только если энкодер установлен, активизирован и не является основным датчиком положения, например при использовании энкодера совместно с шаговым двигателем для контроля проскальзования. \endrussian */
	calb float CurSpeed					/**< \english Motor shaft speed. \endenglish \russian Текущая скорость. \endrussian */
	normal int32s CurSpeed				/**< \english Motor shaft speed in steps/s or rpm. \endenglish \russian Текущая скорость. \endrussian */
	normal int16s uCurSpeed				/**< \english Fractional part of motor shaft speed in microsteps. The microstep size and the range of valid values for this field depend on the selected step division mode (see the MicrostepMode field in engine_settings). Used with stepper motors only. \endenglish \russian Дробная часть текущей скорости в микрошагах. Величина микрошага и диапазон допустимых значений для данного поля зависят от выбранного режима деления шага (см. поле MicrostepMode в engine_settings). Используется только с шаговым двигателем. \endrussian */
	int16s Ipwr							/**< \english Engine current, mA. \endenglish \russian Ток потребления силовой части, мА. \endrussian */
	int16s Upwr							/**< \english Power supply voltage, tens of mV. \endenglish \russian Напряжение на силовой части, десятки мВ. \endrussian */
	int16s Iusb							/**< \english USB current, mA. \endenglish \russian Ток потребления по USB, мА. \endrussian */
	int16s Uusb							/**< \english USB voltage, tens of mV. \endenglish \russian Напряжение на USB, десятки мВ. \endrussian */
	int16s CurT							/**< \english Temperature, tenths of degrees Celsius. \endenglish \russian Температура процессора в десятых долях градусов Цельсия. \endrussian */
	int32u flag Flags of StateFlags		/**< \english A set of flags specifies the motor shaft movement algorithm and a list of limitations. This is a bit mask for bitwise operations. \endenglish \russian Флаги состояний. Это битовая маска для побитовых операций. \endrussian */
	int32u flag GPIOFlags of GPIOFlags	/**< \english A set of flags of GPIO states. This is a bit mask for bitwise operations. \endenglish \russian Флаги состояний GPIO входов. Это битовая маска для побитовых операций. \endrussian */
	int8u CmdBufFreeSpace				/**< \english This field is a service field. It shows the number of free synchronization chain buffer cells. \endenglish \russian Данное поле служебное. Оно показывает количество свободных ячеек буфера цепочки синхронизации. \endrussian */
	reserved 4

/** $XIW
	* \english
	* Start measurements and buffering of speed and the speed error (target speed minus real speed).
	* @param id An identifier of a device
	* \endenglish
	* \russian
	* Начать измерения и буферизацию скорости, ошибки следования.
	* @param id идентификатор устройства
	* \endrussian
	*/
command "start_measurements" writer "stms" (4)

/** $XIR
	* \english
	* A command to read the data buffer to build a speed graph and a speed error graph.
	* 
	* Filling the buffer starts with the command "start_measurements". The buffer holds 25 points; the points are taken with a period of 1 ms. To create a robust system, read data every 20 ms. If the buffer is full, it is recommended to repeat the readings every 5 ms until the buffer again becomes filled with 20 points.
	*
	* To stop measurements just stop reading data. After buffer overflow measurements will stop automatically.
	* @see measurements_t
	* @param id An identifier of a device
	* @param[out] measurements structure with buffer and its length.
	* \endenglish
	* \russian
	* Команда чтения буфера данных для построения графиков скорости и ошибки следования. Заполнение буфера начинается по команде "start_measurements". Буфер вмещает 25 точек, точки снимаются с периодом 1 мс. Для создания устойчивой системы следует считывать данные каждые 20 мс, если буфер полностью заполнен, то рекомендуется повторять считывания каждые 5 мс до момента пока буфер вновь не станет заполнен 20-ю точками.
	* @see measurements_t
	* @param id идентификатор устройства
	* @param[out] measurements структура с буфером и его длинной.
	* \endrussian
	*/
/** $XIS
	* \english
	* The buffer holds no more than 25 points. The exact length of the received buffer is stored in the Length field.
	* \endenglish
	* \russian
	* Буфер вмещает не более 25и точек. Точная длина полученного буфера отражена в поле Length.
	* \endrussian
	* @see measurements
	*/
command "measurements" reader "getm" (216)
fields:
  int32s Speed [25]   /**< \english Current speed in microsteps per second (whole steps are recalculated considering the current step division mode) or encoder counts per second. \endenglish \russian Текущая скорость в микрошагах в секунду (целые шаги пересчитываются с учетом текущего режима деления шага) или отсчетах энкодера в секунду. \endrussian */
  int32s Error [25]   /**< \english Current error in microsteps per second (whole steps are recalculated considering the current step division mode) or encoder counts per second. \endenglish \russian Текущая скорость в микрошагах в секунду (целые шаги пересчитываются с учетом текущего режима деления шага) или отсчетах энкодера в секунду. \endrussian */
  int32u Length       /**< \english Length of actual data in buffer. \endenglish \russian Длина фактических данных в буфере. \endrussian */
  reserved 6

/** $XIR
	* \english
	* Return device electrical parameters, useful for charts.
	*
	* A useful function that fills the structure with a snapshot of the controller voltages and currents.
	* @see chart_data_t
	* @param id An identifier of a device
	* @param[out] chart_data structure with a snapshot of controller parameters.
	* \endenglish
	* \russian
	* Команда чтения состояния обмоток и других не часто используемых данных. Предназначена в первую очередь для получения данных для построения графиков в паре с командой GETS.
	* @see chart_data_t
	* @param id идентификатор устройства
	* @param[out] chart_data структура chart_data.
	* \endrussian
	*/
/** $XIS
	* \english
	* Additional device state.
	*
	* This structure contains additional values such as winding's voltages, currents, and temperature.
	* \endenglish
	* \russian
	* Дополнительное состояние устройства.
	* Эта структура содержит основные дополнительные параметры текущего состоянии контроллера, такие напряжения и токи обмоток и температуру.
	* \endrussian
	* @see get_chart_data
	*/
command "chart_data" reader "getc" (38)
fields:
	int16s WindingVoltageA		/**< \english In case of a step motor, it contains the voltage across the winding A (in tens of mV); in case of a brushless motor, it contains the voltage on the first coil; in case of a DC motor, it contains the only winding current. \endenglish \russian В случае ШД, напряжение на обмотке A (в десятках мВ); в случае бесщеточного, напряжение на первой обмотке; в случае DC - на единственной. \endrussian */
	int16s WindingVoltageB		/**< \english In case of a step motor, it contains the voltage across the winding B (in tens of mV); in case of a brushless motor, it contains the voltage on the second winding; and in case of a DC motor, this field is not used. \endenglish \russian В случае ШД, напряжение на обмотке B (в десятках мВ); в случае бесщеточного, напряжение на второй обмотке; в случае DC не используется. \endrussian */
	int16s WindingVoltageC		/**< \english In case of a brushless motor, it contains the voltage on the third winding (in tens of mV); in the case of a step motor and a DC motor, the field is not used. \endenglish \russian В случае бесщеточного, напряжение на третьей обмотке (в десятках мВ); в случае ШД и DC не используется. \endrussian */
	int16s WindingCurrentA		/**< \english In case of a step motor, it contains the current in the winding A (in mA); in case of a brushless motor, it contains the current in the winding A; and in case of a DC motor, it contains the only winding current. \endenglish \russian В случае ШД, ток в обмотке A (в мA); в случае бесщеточного, ток в первой обмотке; в случае DC в единственной. \endrussian */
	int16s WindingCurrentB		/**< \english In case of a step motor, it contains the current in the winding B (in mA); in case of a brushless motor, it contains the current in the winding B; and in case of a DC motor, the field is not used. \endenglish \russian В случае ШД, ток в обмотке B (в мА); в случае бесщеточного, ток в второй обмотке; в случае DC не используется. \endrussian */
	int16s WindingCurrentC		/**< \english In case of a brushless motor, it contains the current in the winding C (in mA); in case of a step motor and a DC motor, the field is not used. \endenglish \russian В случае бесщеточного, ток в третьей обмотке (в мА); в случае ШД и DC не используется. \endrussian */
	int16u Pot					/**< \english Analog input value, dimensionless. Range: 0..10000 \endenglish \russian Значение на аналоговом входе. Диапазон: 0..10000 \endrussian */
	int16u Joy					/**< \english The joystick position, dimensionless. Range: 0..10000 \endenglish \russian Положение джойстика в десятитысячных долях. Диапазон: 0..10000 \endrussian */
	int16s DutyCycle			/**< \english PWM duty cycle. \endenglish \russian Коэффициент заполнения ШИМ. \endrussian */
	reserved 14

/** $XIR
	* \english
	* Return device information. It's available in the firmware and the bootloader.
	* @param id An identifier of a device
	* @param[out] device_information device information
	* \endenglish
	* \russian
	* Возвращает информацию об устройстве. Доступна как из прошивки, так и из бутлоадера.
	* @param id идентификатор устройства.
	* @param[out] device_information информация об устройстве
	* \endrussian
	*/
/** $XIS
	* \english
	* Controller information structure.
	* \endenglish
	* \russian
	* Информации о контроллере.
	* \endrussian
	* @see get_device_information
	*/
command "device_information_impl" reader "geti" (36)
without lock, public
with dualsync, publicstruct
fields:
	char Manufacturer[4]		/**< \english Manufacturer \endenglish \russian Производитель \endrussian */
	char ManufacturerId[2]		/**< \english Manufacturer id \endenglish \russian Идентификатор производителя \endrussian */
	char ProductDescription[8]	/**< \english Product description \endenglish \russian Описание продукта \endrussian */
	int8u Major					/**< \english The major number of the hardware version. \endenglish \russian Основной номер версии железа. \endrussian */
	int8u Minor					/**< \english The minor number of the hardware version. \endenglish \russian Второстепенный номер версии железа. \endrussian */
	int16u Release				/**< \english Release version. \endenglish \russian Номер правок этой версии железа. \endrussian */
	reserved 12

/** $XIR
	* \english
	* Read device serial number.
	* @param id An identifier of a device
	* @param[out] SerialNumber serial number
	* \endenglish
	* \russian
	* Чтение серийного номера контроллера.
	* @param id идентификатор устройства
	* @param[out] SerialNumber серийный номер контроллера
	* \endrussian
	*/
command "serial_number" reader "gser" (10)
with inline
fields:
	int32u SerialNumber		/**< \english Board serial number. \endenglish \russian Серийный номер платы. \endrussian */

//@}

/**
	* \english
	* @name Group of commands to work with the controller firmware
	*
	* \endenglish
	* \russian
	* @name Группа команд для работы с прошивкой контроллера
	*
	* \endrussian
	*/

//@{

/** $XIR
	* \english
	* Read the controller's firmware version.
	* @param id An identifier of a device
	* @param[out] Major major version
	* @param[out] Minor minor version
	* @param[out] Release release version
	* \endenglish
	* \russian
	* Чтение номера версии прошивки контроллера.
	* @param id идентификатор устройства
	* @param[out] Major номер основной версии
	* @param[out] Minor номер дополнительной версии
	* @param[out] Release номер релиза
	* \endrussian
	*/
command "firmware_version" reader "gfwv" (10)
with inline
fields:
	int8u Major		/**< \english Firmware major version number \endenglish \russian Мажорный номер версии прошивки \endrussian */
	int8u Minor		/**< \english Firmware minor version number \endenglish \russian Минорный номер версии прошивки \endrussian */
	int16u Release	/**< \english Firmware release version number \endenglish \russian Номер релиза версии прошивки \endrussian */

/** $XIW
	* \english
	* The command switches the controller to update the firmware state.
	* After receiving this command, the firmware board sets a flag (for loader), sends an echo reply, and restarts the controller.
	* \endenglish
	* \russian
	* Команда переводит контроллер в режим обновления прошивки.
	* Получив такую команду, прошивка платы устанавливает флаг (для загрузчика), отправляет эхо-ответ и перезагружает контроллер.
	* \endrussian
	*/
command "service_command_updf" writer "updf" (4)
without crc, lock

//@}

/**
	* \english
	* @name Service commands
	*
	* \endenglish
	* \russian
	* @name Группа сервисных команд
	*
	* \endrussian
	*/

//@{

/** $XIW
	* \english
	* Write device serial number and hardware version to the controller's flash memory.
	* Along with the new serial number and hardware version, a "Key" is transmitted.
	* The SN and hardware version are changed and saved when keys match.
	* Can be used by the manufacturer only.
	* @param id An identifier of a device
	* @param[in] serial_number structure contains new serial number and secret key.
	* \endenglish
	* \russian
	* Запись серийного номера и версии железа во flash память контроллера.
	* Вместе с новым серийным номером и версией железа передаётся "Ключ",
	* только при совпадении которого происходит изменение и сохранение.
	* Функция используется только производителем.
	* @param id идентификатор устройства
	* @param[in] serial_number структура, содержащая серийный номер, версию железа и ключ.
	* \endrussian
	*/
/**  $XIS
	* \english
	* The structure contains a new serial number, hardware version, and valid key. The SN and hardware version are changed and saved when the transmitted key matches the stored key. It can be used by the manufacturer only.
	* \endenglish
	* \russian
	* Структура с серийным номером и версией железа.
	* Вместе с новым серийным номером и версией железа передаётся "Ключ", только при совпадении которого происходит изменение и сохранение. Функция используется только производителем.
	* \endrussian
	*/
command "serial_number" writer "sser" (50)
fields:
	int32u SN		/**< \english New board serial number. \endenglish \russian Новый серийный номер платы. \endrussian */
	byte Key[32]	/**< \english Protection key (256 bit). \endenglish \russian Ключ защиты для установки серийного номера (256 бит). \endrussian */
	int8u Major		/**< \english The major number of the hardware version. \endenglish \russian Основной номер версии железа. \endrussian */
	int8u Minor		/**< \english The minor number of the hardware version. \endenglish \russian Второстепенный номер версии железа. \endrussian */
	int16u Release	/**< \english Number of edits this release of hardware. \endenglish \russian Номер правок этой версии железа. \endrussian */
	reserved 4

/** $XIR
	* \english
	* Read the analog data structure that contains raw analog data from the embedded ADC. This function is used for device testing and deep recalibration by the manufacturer only.
	* @param id An identifier of a device
	* @param[out] analog_data analog data coefficients
	* \endenglish
	* \russian
	* Чтение аналоговых данных, содержащих данные с АЦП и нормированные значения величин. Эта функция используется для тестирования и калибровки устройства.
	* @param id идентификатор устройства
	* @param[out] analog_data аналоговые данные
	* \endrussian
	*/
/** $XIS
	* \english
	* Analog data.
	*
	* This structure contains raw analog data from the embedded ADC. These data are used for device testing and deep recalibration by the manufacturer only.
	* \endenglish
	* \russian
	* Аналоговые данные.
	* Эта структура содержит необработанные данные с АЦП и нормированные значения. Эти данные используются в сервисных целях для тестирования и калибровки устройства.
	* \endrussian
	* @see get_analog_data
	*/
command "analog_data" reader "rdan" (76)
fields:
	int16u A1Voltage_ADC	/**< \english "Voltage on pin 1 winding A" raw data from ADC. \endenglish \russian "Выходное напряжение на 1 выводе обмотки А" необработанные данные с АЦП. \endrussian */
	int16u A2Voltage_ADC	/**< \english "Voltage on pin 2 winding A" raw data from ADC. \endenglish \russian "Выходное напряжение на 2 выводе обмотки А" необработанные данные с АЦП. \endrussian */
	int16u B1Voltage_ADC	/**< \english "Voltage on pin 1 winding B" raw data from ADC. \endenglish \russian "Выходное напряжение на 1 выводе обмотки B" необработанные данные с АЦП. \endrussian */
	int16u B2Voltage_ADC	/**< \english "Voltage on pin 2 winding B" raw data from ADC. \endenglish \russian "Выходное напряжение на 2 выводе обмотки B" необработанные данные с АЦП. \endrussian */
	int16u SupVoltage_ADC	/**< \english "Supply voltage of H-bridge's MOSFETs" raw data from ADC. \endenglish \russian "Напряжение питания ключей Н-моста" необработанные данные с АЦП. \endrussian */
	int16u ACurrent_ADC		/**< \english "Winding A current" raw data from ADC. \endenglish \russian "Ток через обмотку А" необработанные данные с АЦП. \endrussian */
	int16u BCurrent_ADC		/**< \english "Winding B current" raw data from ADC. \endenglish \russian "Ток через обмотку B" необработанные данные с АЦП. \endrussian */
	int16u FullCurrent_ADC	/**< \english "Full current" raw data from ADC. \endenglish \russian "Полный ток" необработанные данные с АЦП. \endrussian */
	int16u Temp_ADC			/**< \english Voltage from temperature sensor, raw data from ADC. \endenglish \russian Напряжение с датчика температуры, необработанные данные с АЦП. \endrussian */
	int16u Joy_ADC			/**< \english Joystick raw data from ADC. \endenglish \russian Джойстик, необработанные данные с АЦП. \endrussian */
	int16u Pot_ADC			/**< \english Voltage on analog input, raw data from ADC \endenglish \russian Напряжение на аналоговом входе, необработанные данные с АЦП \endrussian */
	int16u L5_ADC			/**< \english USB supply voltage after the current sense resistor, raw data from ADC. \endenglish \russian Напряжение питания USB после current sense резистора, необработанные данные с АЦП. \endrussian */
	int16u H5_ADC			/**< \english USB Power supply from ADC \endenglish \russian Напряжение питания USB, необработанные данные с АЦП \endrussian */
	int16s A1Voltage		/**< \english "Voltage on pin 1 winding A" calibrated data (in tens of mV). \endenglish \russian "Выходное напряжение на 1 выводе обмотки А" откалиброванные данные (в десятках мВ). \endrussian */
	int16s A2Voltage		/**< \english "Voltage on pin 2 winding A" calibrated data (in tens of mV). \endenglish \russian "Выходное напряжение на 2 выводе обмотки А" откалиброванные данные (в десятках мВ). \endrussian */
	int16s B1Voltage		/**< \english "Voltage on pin 1 winding B" calibrated data (in tens of mV). \endenglish \russian "Выходное напряжение на 1 выводе обмотки B" откалиброванные данные (в десятках мВ). \endrussian */
	int16s B2Voltage		/**< \english "Voltage on pin 2 winding B" calibrated data (in tens of mV). \endenglish \russian "Выходное напряжение на 2 выводе обмотки B" откалиброванные данные (в десятках мВ). \endrussian */
	int16s SupVoltage		/**< \english "Supply voltage on the top of H-bridge's MOSFETs" calibrated data (in tens of mV). \endenglish \russian "Напряжение питания ключей Н-моста" откалиброванные данные (в десятках мВ). \endrussian */
	int16s ACurrent			/**< \english "Winding A current" calibrated data (in mA). \endenglish \russian "Ток через обмотку А" откалиброванные данные (в мА). \endrussian */
	int16s BCurrent			/**< \english "Winding B current" calibrated data (in mA). \endenglish \russian "Ток через обмотку B" откалиброванные данные (в мА). \endrussian */
	int16s FullCurrent		/**< \english "Full current" calibrated data (in mA). \endenglish \russian "Полный ток" откалиброванные данные (в мА). \endrussian */
	int16s Temp				/**< \english Temperature, calibrated data (in tenths of degrees Celsius). \endenglish \russian Температура, откалиброванные данные (в десятых долях градуса Цельсия). \endrussian */
	int16s Joy				/**< \english Joystick, calibrated data. Range: 0..10000 \endenglish \russian Джойстик во внутренних единицах. Диапазон: 0..10000 \endrussian */
	int16s Pot				/**< \english Analog input, calibrated data. Range: 0..10000 \endenglish \russian Аналоговый вход во внутренних единицах. Диапазон: 0..10000 \endrussian */
	int16s L5				/**< \english USB supply voltage after the current sense resistor (in tens of mV). \endenglish \russian Напряжение питания USB после current sense резистора (в десятках мВ). \endrussian */
	int16s H5				/**< \english USB power supply (in tens of mV). \endenglish \russian Напряжение питания USB (в десятках мВ). \endrussian */
	int16u deprecated
	int32s R				/**< \english Motor winding resistance in mOhms (is only used with stepper motors). \endenglish \russian Сопротивление обмоток двигателя(для шагового двигателя),  в мОм \endrussian */
	int32s L				/**< \english Motor winding pseudo inductance in uH (is only used with stepper motors). \endenglish \russian Псевдоиндуктивность обмоток двигателя(для шагового двигателя),  в мкГн \endrussian */
	reserved 8

/** $XIR
	* \english
	* Read data from firmware for debug purpose. Manufacturer only.
	* Its use depends on context, firmware version and previous history.
	* @param id An identifier of a device
	* @param[out] debug_read Debug data.
	* \endenglish
	* \russian
	* Чтение данных из прошивки для отладки и поиска неисправностей. Команда только для производителя.
	* Получаемые данные зависят от версии прошивки, истории и контекста использования.
	* @param id идентификатор устройства
	* @param[out] debug_read Данные для отладки.
	* \endrussian
	*/
/** $XIS
	* \english
	* Debug data.
	* These data are used for device debugging by the manufacturer.
	* \endenglish
	* \russian
	* Отладочные данные.
	* Эти данные используются в сервисных целях для тестирования и отладки устройства.
	* \endrussian
	*/
command "debug_read" reader "dbgr" (142)
fields:
	byte DebugData[128]		/**< \english Arbitrary debug data. \endenglish \russian Отладочные данные. \endrussian */
	reserved 8

/** $XIW
	* \english
	* Write data to firmware for debug purpose. Manufacturer only.
	* @param id An identifier of a device
	* @param[in] debug_write Debug data.
	* \endenglish
	* \russian
	* Запись данных в прошивку для отладки и поиска неисправностей. Команда только для производителя.
	* @param id идентификатор устройства
	* @param[in] debug_write Данные для отладки.
	* \endrussian
	*/
/** $XIS
	* \english
	* Debug data.
	* These data are used for device debugging by the manufacturer.
	* \endenglish
	* \russian
	* Отладочные данные.
	* Эти данные используются в сервисных целях для тестирования и отладки устройства.
	* \endrussian
	*/
command "debug_write" writer "dbgw" (142)
fields:
	byte DebugData[128]		/**< \english Arbitrary debug data. \endenglish \russian Отладочные данные. \endrussian */
	reserved 8

/** $XIW
	* \english
	* The command to clear the controller's FRAM.
	* The memory is cleared by filling the whole memory bytes with 0x00. After cleaning, the controller restarts. There is no response to this command.
	* @param id An identifier of a device
	* \endenglish
	* \russian
	* Команда очистки FRAM контроллера.
	* Память очищается путем заполнения всего объема памяти байтами 0x00. После очистки контроллер перезагружается. Ответа на эту команду нет.
	* @param id идентификатор устройства
	* \endrussian
	*/
command "service_command_clear_fram_impl" writer "clfr" (4) reader "clfr" (0)
without answer, public, crc

//@}

/**
	* \english
	* @name A group of EEPROM commands
	*
	* \endenglish
	* \russian
	* @name Группа команд работы с EEPROM подвижки
	*
	* \endrussian
	*/

//@{

/** $XIR
	* \english
	* Read the user's stage name from the EEPROM.
	* @param id An identifier of a device
	* @param[out] stage_name structure contains the previously set user's stage name.
	* \endenglish
	* \russian
	* Чтение пользовательского имени подвижки из EEPROM.
	* @param id идентификатор устройства
	* @param[out] stage_name структура, содержащая установленное пользовательское имя позиционера
	* \endrussian
	*/
/** $XIW
	* \english
	* Write the user's stage name to EEPROM.
	* @param id An identifier of a device
	* @param[in] stage_name structure contains the previously set user's stage name.
	* \endenglish
	* \russian
	* Запись пользовательского имени подвижки в EEPROM.
	* @param id идентификатор устройства
	* @param[in] stage_name структура, содержащая установленное пользовательское имя позиционера
	* \endrussian
	*/
/** $XIS
	* \english
	* Stage username.
	* \endenglish
	* \russian
	* Пользовательское имя подвижки.
	* \endrussian
	*/
command "stage_name" universal "nme" (30)
fields:
	char PositionerName[16]			/**< \english User's positioner name. It can be set by a user. Max string length: 16 characters. \endenglish \russian Пользовательское имя подвижки. Может быть установлено пользователем для его удобства. Максимальная длина строки: 16 символов. \endrussian */
	reserved 8

/** $XIR
	* \english
	* Deprecated. Read stage information from the EEPROM.
	* @param id An identifier of a device
	* @param[out] stage_information structure contains stage information
	* \endenglish
	* \russian
	* Чтение информации о позиционере из EEPROM. Не поддерживается.
	* @param id идентификатор устройства
	* @param[out] stage_information структура, содержащая информацию о позиционере
	* \endrussian
	*/
/** $XIW
	* \english
	* Deprecated. Set stage information to the EEPROM.
	* Can be used by the manufacturer only.
	* @param id An identifier of a device
	* @param[in] stage_information structure contains stage information
	* \endenglish
	* \russian
	* Запись информации о позиционере в EEPROM. Не поддерживается.
	* Функция должна использоваться только производителем.
	* @param id идентификатор устройства
	* @param[in] stage_information структура, содержащая информацию о позиционере
	* \endrussian
	*/
/** $XIS
	* \english
	* Deprecated. Stage information. Deprecated.
	* \endenglish
	* \russian
	* Информация о позиционере.
	* \endrussian
	* @see set_stage_information
	* @see get_stage_information
	*/
command "stage_information" universal "sti" (70)
fields:
	char Manufacturer[16]			/**< \english Manufacturer. Max string length: 16 chars. \endenglish \russian Производитель. Максимальная длина строки: 16 символов. \endrussian */
	char PartNumber[24]				/**< \english Series and PartNumber. Max string length: 24 chars. \endenglish \russian Серия и номер модели. Максимальная длина строки: 24 символа. \endrussian */	
	reserved 24

/** $XIR 
	* \english
	* Deprecated. Read stage settings from the EEPROM.
	* @param id An identifier of a device
	* @param[out] stage_settings structure contains stage settings
	* \endenglish
	* \russian
	* Чтение настроек позиционера из EEPROM.
	* @param id идентификатор устройства
	* @param[out] stage_settings структура, содержащая настройки позиционера
	* \endrussian
	*/
/** $XIW
	* \english
	* Deprecated. Set stage settings to the EEPROM.
	* Can be used by the manufacturer only
	* @param id An identifier of a device
	* @param[in] stage_settings structure contains stage settings
	* \endenglish
	* \russian
	* Запись настроек позиционера в EEPROM.
	* Функция должна использоваться только производителем.
	* @param id идентификатор устройства
	* @param[in] stage_settings структура, содержащая настройки позиционера
	* \endrussian
	*/
/** $XIS
	* \english
	* Deprecated. Stage settings.
	* \endenglish
	* \russian
	* Настройки позиционера.
	* \endrussian
	* @see set_stage_settings
	* @see get_stage_settings
	*/
command "stage_settings" universal "sts" (70)
fields:
	float LeadScrewPitch			/**< \english Lead screw pitch (mm). Data type: float. \endenglish \russian Шаг ходового винта в мм. Тип данных: float. \endrussian */	
	char Units[8]					/**< \english Units for MaxSpeed and TravelRange fields of the structure (steps, degrees, mm, ...). Max string length: 8 chars. \endenglish \russian Единицы измерения расстояния, используемые в полях MaxSpeed и TravelRange (шаги, градусы, мм, ...), Максимальная длина строки: 8 символов. \endrussian */	
	float MaxSpeed					/**< \english Maximum speed (Units/c). Data type: float. \endenglish \russian Максимальная скорость (Units/с). Тип данных: float. \endrussian */	
	float TravelRange				/**< \english Travel range (Units). Data type: float. \endenglish \russian Диапазон перемещения (Units). Тип данных: float. \endrussian */	
	float SupplyVoltageMin			/**< \english Minimum supply voltage (V). Data type: float. \endenglish \russian Минимальное напряжение питания (В). Тип данных: float. \endrussian */	
	float SupplyVoltageMax			/**< \english Maximum supply voltage (V). Data type: float. \endenglish \russian Максимальное напряжение питания (В). Тип данных: float. \endrussian */	
	float MaxCurrentConsumption		/**< \english Maximum current consumption (A). Data type: float. \endenglish \russian Максимальный ток потребления (А). Тип данных: float. \endrussian */	
	float HorizontalLoadCapacity	/**< \english Horizontal load capacity (kg). Data type: float. \endenglish \russian Горизонтальная грузоподъемность (кг). Тип данных: float. \endrussian */	
	float VerticalLoadCapacity		/**< \english Vertical load capacity (kg). Data type: float. \endenglish \russian Вертикальная грузоподъемность (кг). Тип данных: float. \endrussian */	
	reserved 24	
	
/** $XIR 
	* \english
	* Deprecated. Read motor information from the EEPROM.
	* @param id An identifier of a device
	* @param[out] motor_information structure contains motor information
	* \endenglish
	* \russian
	* Чтение информации о двигателе из EEPROM.
	* @param id идентификатор устройства
	* @param[out] motor_information структура, содержащая информацию о двигателе
	* \endrussian
	*/
/** $XIW
	* \english
	* Deprecated. Set motor information to the EEPROM.
	* Can be used by the manufacturer only.
	* @param id An identifier of a device
	* @param[in] motor_information structure contains motor information
	* \endenglish
	* \russian
	* Запись информации о двигателе в EEPROM.
	* Функция должна использоваться только производителем.
	* @param id идентификатор устройства
	* @param[in] motor_information структура, содержащая информацию о двигателе
	* \endrussian
	*/
/** $XIS
	* \english
	* Deprecated. motor information.
	* \endenglish
	* \russian
	* Информация о двигателе.
	* \endrussian
	* @see set_motor_information
	* @see get_motor_information
	*/
command "motor_information" universal "mti" (70)
fields:
	char Manufacturer[16]			/**< \english Manufacturer. Max string length: 16 chars. \endenglish \russian Производитель. Максимальная длина строки: 16 символов. \endrussian */	
	char PartNumber[24]				/**< \english Series and PartNumber. Max string length: 24 chars. \endenglish \russian Серия и номер модели. Максимальная длина строки: 24 символа. \endrussian */	
	reserved 24

/** $XIR 
	* \english
	* Deprecated. Read motor settings from the EEPROM.
	* @param id An identifier of a device
	* @param[out] motor_settings structure contains motor settings
	* \endenglish
	* \russian
	* Чтение настроек двигателя из EEPROM.
	* @param id идентификатор устройства
	* @param[out] motor_settings структура, содержащая настройки двигателя
	* \endrussian
	*/
/** $XIW
	* \english
	* Deprecated. Set motor settings to the EEPROM.
	* Can be used by the manufacturer only.
	* @param id An identifier of a device
	* @param[in] motor_settings structure contains motor information
	* \endenglish
	* \russian
	* Запись настроек двигателя в EEPROM.
	* Функция должна использоваться только производителем.
	* @param id идентификатор устройства
	* @param[in] motor_settings структура, содержащая настройки двигателя
	* \endrussian
	*/
/** $XIS
	* \english
	* Deprecated. Physical characteristics and limitations of the motor.
	* \endenglish
	* \russian
	* Физический характеристики и ограничения мотора.
	* \endrussian
	* @see set_motor_settings
	* @see get_motor_settings
	*/
command "motor_settings" universal "mts" (112)
fields:
	int8u flag MotorType of MotorTypeFlags	/**< \english Motor type. This is a bit mask for bitwise operations. \endenglish \russian Тип двигателя. Это битовая маска для побитовых операций. \endrussian */
	int8u ReservedField						/**< \english Reserved \endenglish \russian Зарезервировано \endrussian */
	int16u Poles							/**< \english Number of pole pairs for DC or BLDC motors or number of steps per rotation for stepper motors. \endenglish \russian Кол-во пар полюсов у DС или BLDC двигателя или кол-во шагов на оборот для шагового двигателя. \endrussian */
	int16u Phases							/**< \english Number of phases for BLDC motors. \endenglish \russian Кол-во фаз у BLDC двигателя. \endrussian */
	float NominalVoltage					/**< \english Nominal voltage on winding (B). Data type: float \endenglish \russian Номинальное напряжение на обмотке (В). Тип данных: float. \endrussian */
	float NominalCurrent					/**< \english Maximum direct current in winding for DC and BLDC engines, nominal current in windings for stepper motors (A). Data type: float.  \endenglish \russian Максимальный постоянный ток в обмотке для DC и BLDC двигателей, номинальный ток в обмотке для шаговых двигателей (А). Тип данных: float. \endrussian */
	float NominalSpeed						/**< \english Not used. Nominal speed (rpm). Used for DC and BLDC engines. Data type: float. \endenglish \russian Не используется. Номинальная скорость (об/мин). Применяется для DC и BLDC двигателей. Тип данных: float. \endrussian */
	float NominalTorque						/**< \english Nominal torque (mN * m). Used for DC and BLDC engines. Data type: float. \endenglish \russian Номинальный крутящий момент (мН * м). Применяется для DC и BLDC двигателей. Тип данных: float. \endrussian */
	float NominalPower						/**< \english Nominal power (W). Used for DC and BLDC engines. Data type: float. \endenglish \russian Номинальная мощность(Вт). Применяется для DC и BLDC двигателей. Тип данных: float. \endrussian */	
	float WindingResistance					/**< \english Resistance of windings for DC engines, of each of two windings for stepper motors, or of each of three windings for BLDC engines (Ohm). Data type: float.\endenglish \russian Сопротивление обмотки DC двигателя, каждой из двух обмоток шагового двигателя или каждой из трёх обмоток BLDC двигателя (Ом). Тип данных: float. \endrussian */
	float WindingInductance					/**< \english Inductance of windings for DC engines, inductance of each of two windings for stepper motors, or inductance of each of three windings for BLDC engines (mH). Data type: float.\endenglish \russian Индуктивность обмотки DC двигателя, каждой из двух обмоток шагового двигателя или каждой из трёх обмоток BLDC двигателя (мГн). Тип данных: float. \endrussian */
	float RotorInertia						/**< \english Rotor inertia (g * cm2). Data type: float.\endenglish \russian Инерция ротора (г cм2). Тип данных: float. \endrussian */
	float StallTorque						/**< \english Torque hold position for a stepper motor or torque at a motionless rotor for other types of engines (mN * m). Data type: float. \endenglish \russian Крутящий момент удержания позиции для шагового двигателя или крутящий момент при неподвижном роторе для других типов двигателей (мН м). Тип данных: float. \endrussian */
	float DetentTorque						/**< \english Holding torque position with unpowered windings (mN * m). Data type: float. \endenglish \russian Момент удержания позиции с незапитанными обмотками (мН м). Тип данных: float. \endrussian */
	float TorqueConstant					/**< \english Torque constant that determines the proportionality constant between the maximum rotor torque and current flowing in the winding (mN * m / A). Used mainly for DC motors. Data type: float. \endenglish \russian Константа крутящего момента, определяющая коэффициент пропорциональности максимального момента силы ротора от протекающего в обмотке тока (мН м/А). Используется в основном для DC двигателей. Тип данных: float. \endrussian */
	float SpeedConstant						/**< \english Velocity constant, which determines the value or the amplitude of the induced voltage on the motion of DC or BLDC motors (rpm / V) or stepper motors (steps/s / V). Data type: float. \endenglish \russian Константа скорости, определяющая значение или амплитуду напряжения наведённой индукции при вращении ротора DC или BLDC двигателя (об/мин / В) или шагового двигателя (шаг/с / В). Тип данных: float. \endrussian */
	float SpeedTorqueGradient				/**< \english Speed torque gradient (rpm / mN * m). Data type: float. \endenglish \russian Градиент крутящего момента (об/мин / мН м). Тип данных: float. \endrussian */
	float MechanicalTimeConstant			/**< \english Mechanical time constant (ms). Data type: float. \endenglish \russian Механическая постоянная времени (мс). Тип данных: float. \endrussian */
	float MaxSpeed							/**< \english The maximum speed for stepper motors (steps/s) or DC and BLDC motors (rmp). Data type: float. \endenglish \russian Максимальная разрешённая скорость для шаговых двигателей (шаг/с) или для DC и BLDC двигателей (об/мин). Тип данных: float. \endrussian */
	float MaxCurrent						/**< \english The maximum current in the winding (A). Data type: float. \endenglish \russian Максимальный ток в обмотке (А). Тип данных: float. \endrussian */
	float MaxCurrentTime					/**< \english Safe duration of overcurrent in the winding (ms). Data type: float. \endenglish \russian Безопасная длительность максимального тока в обмотке (мс). Тип данных: float. \endrussian */
	float NoLoadCurrent						/**< \english The current consumption in idle mode (A). Used for DC and BLDC motors. Data type: float. \endenglish \russian Ток потребления в холостом режиме (А). Применяется для DC и BLDC двигателей. Тип данных: float. \endrussian */
	float NoLoadSpeed						/**< \english Idle speed (rpm). Used for DC and BLDC motors. Data type: float. \endenglish \russian Скорость в холостом режиме (об/мин). Применяется для DC и BLDC двигателей. Тип данных: float. \endrussian */
	reserved 24

/** $XIR
	* \english
	* Deprecated. Read encoder information from the EEPROM.
	* @param id An identifier of a device
	* @param[out] encoder_information structure contains information about encoder
	* \endenglish
	* \russian
	* Чтение информации об энкодере из EEPROM.
	* @param id идентификатор устройства
	* @param[out] encoder_information структура, содержащая информацию об энкодере
	* \endrussian
	*/
/** $XIW
	* \english
	* Deprecated. Set encoder information to the EEPROM.
	* Can be used by the manufacturer only.
	* @param id An identifier of a device
	* @param[in] encoder_information structure contains information about encoder
	* \endenglish
	* \russian
	* Запись информации об энкодере в EEPROM.
	* Функция должна использоваться только производителем.
	* @param id идентификатор устройства
	* @param[in] encoder_information структура, содержащая информацию об энкодере
	* \endrussian
	*/
/** $XIS
	* \english
	* Deprecated. Encoder information.
	* \endenglish
	* \russian
	* Информация об энкодере.
	* \endrussian
	* @see set_encoder_information
	* @see get_encoder_information
	*/
command "encoder_information" universal "eni" (70)
fields:
	char Manufacturer[16]			/**< \english Manufacturer. Max string length: 16 chars. \endenglish \russian Производитель. Максимальная длина строки: 16 символов. \endrussian */	
	char PartNumber[24]				/**< \english Series and PartNumber. Max string length: 24 chars. \endenglish \russian Серия и номер модели. Максимальная длина строки: 24 символа. \endrussian */	
	reserved 24

/** $XIR
	* \english
	* Deprecated. Read encoder settings from the EEPROM.
	* @param id An identifier of a device
	* @param[out] encoder_settings structure contains encoder settings
	* \endenglish
	* \russian
	* Чтение настроек энкодера из EEPROM.
	* @param id идентификатор устройства
	* @param[out] encoder_settings структура, содержащая настройки энкодера
	* \endrussian
	*/
/** $XIW
	* \english
	* Deprecated. Set encoder settings to the EEPROM.
	* Can be used by the manufacturer only.
	* @param id An identifier of a device
	* @param[in] encoder_settings structure contains encoder settings
	* \endenglish
	* \russian
	* Запись настроек энкодера в EEPROM.
	* Функция должна использоваться только производителем.
	* @param id идентификатор устройства
	* @param[in] encoder_settings структура, содержащая настройки энкодера
	* \endrussian
	*/
/** $XIS
	* \english
	* Deprecated. Encoder settings.
	* \endenglish
	* \russian
	* Настройки энкодера.
	* \endrussian
	* @see set_encoder_settings
	* @see get_encoder_settings
	*/
command "encoder_settings" universal "ens" (54)
fields:
	float MaxOperatingFrequency		/**< \english Maximum operation frequency (kHz). Data type: float. \endenglish \russian Максимальная частота (кГц). Тип данных: float. \endrussian */
	float SupplyVoltageMin			/**< \english Minimum supply voltage (V). Data type: float. \endenglish \russian Минимальное напряжение питания (В). Тип данных: float. \endrussian */
	float SupplyVoltageMax			/**< \english Maximum supply voltage (V). Data type: float. \endenglish \russian Максимальное напряжение питания (В). Тип данных: float. \endrussian */
	float MaxCurrentConsumption		/**< \english Max current consumption (mA). Data type: float. \endenglish \russian Максимальное потребление тока (мА). Тип данных: float. \endrussian */
	int32u PPR						/**< \english The number of counts per revolution \endenglish \russian Количество отсчётов на оборот \endrussian */
	int32u flag EncoderSettings of EncoderSettingsFlags /**< \english Encoder settings flags. This is a bit mask for bitwise operations. \endenglish \russian Флаги настроек энкодера. Это битовая маска для побитовых операций. \endrussian */
	reserved 24

/** $XIR
	* \english
	* Deprecated. Read hall sensor information from the EEPROM.
	* @param id An identifier of a device
	* @param[out] hallsensor_information structure contains information about hall sensor
	* \endenglish
	* \russian
	* Чтение информации о датчиках Холла из EEPROM.
	* @param id идентификатор устройства
	* @param[out] hallsensor_information структура, содержащая информацию о датчиках Холла
	* \endrussian
	*/
/** $XIW
	* \english
	* Deprecated. Set hall sensor information to the EEPROM.
	* Can be used by the manufacturer only.
	* @param id An identifier of a device
	* @param[in] hallsensor_information structure contains information about hall sensor
	* \endenglish
	* \russian
	* Запись информации о датчиках Холла в EEPROM.
	* Функция должна использоваться только производителем.
	* @param id идентификатор устройства
	* @param[in] hallsensor_information структура, содержащая информацию о датчиках Холла
	* \endrussian
	*/
/** $XIS
	* \english
	* Deprecated. Hall sensor information.
	* \endenglish
	* \russian
	* Информация о датчиках Холла.
	* \endrussian
	* @see set_hallsensor_information
	* @see get_hallsensor_information
	*/
command "hallsensor_information" universal "hsi" (70)
fields:
	char Manufacturer[16]			/**< \english Manufacturer. Max string length: 16 chars. \endenglish \russian Производитель. Максимальная длина строки: 16 символов. \endrussian */	
	char PartNumber[24]				/**< \english Series and PartNumber. Max string length: 24 chars. \endenglish \russian Серия и номер модели. Максимальная длина строки: 24 символа. \endrussian */	
	reserved 24

/** $XIR
	* \english
	* Deprecated. Read hall sensor settings from the EEPROM.
	* @param id An identifier of a device
	* @param[out] hallsensor_settings structure contains hall sensor settings
	* \endenglish
	* \russian
	* Чтение настроек датчиков Холла из EEPROM.
	* @param id идентификатор устройства
	* @param[out] hallsensor_settings структура, содержащая настройки датчиков Холла
	* \endrussian
	*/
/** $XIW
	* \english
	* Deprecated. Set hall sensor settings to the EEPROM.
	* Can be used by the manufacturer only.
	* @param id An identifier of a device
	* @param[in] hallsensor_settings structure contains hall sensor settings
	* \endenglish
	* \russian
	* Запись настроек датчиков Холла в EEPROM.
	* Функция должна использоваться только производителем.
	* @param id идентификатор устройства
	* @param[in] hallsensor_settings структура, содержащая настройки датчиков Холла
	* \endrussian
	*/
/** $XIS
	* \english
	* Deprecated. Hall sensor settings.
	* \endenglish
	* \russian
	* Настройки датчиков Холла.
	* \endrussian
	* @see set_hallsensor_settings
	* @see get_hallsensor_settings
	*/
command "hallsensor_settings" universal "hss" (50)
fields:
	float MaxOperatingFrequency		/**< \english Maximum operation frequency (kHz). Data type: float. \endenglish \russian Максимальная частота (кГц). Тип данных: float. \endrussian */
	float SupplyVoltageMin			/**< \english Minimum supply voltage (V). Data type: float. \endenglish \russian Минимальное напряжение питания (В). Тип данных: float. \endrussian */
	float SupplyVoltageMax			/**< \english Maximum supply voltage (V). Data type: float. \endenglish \russian Максимальное напряжение питания (В). Тип данных: float. \endrussian */
	float MaxCurrentConsumption		/**< \english Maximum current consumption (mA). Data type: float. \endenglish \russian Максимальное потребление тока (мА). Тип данных: float. \endrussian */
	int32u PPR						/**< \english The number of counts per revolution \endenglish \russian Количество отсчётов на оборот \endrussian */
	reserved 24	
	
/** $XIR
	* \english
	* Deprecated. Read gear information from the EEPROM.
	* @param id An identifier of a device
	* @param[out] gear_information structure contains information about step gearhead
	* \endenglish
	* \russian
	* Чтение информации о редукторе из EEPROM.
	* @param id идентификатор устройства
	* @param[out] gear_information структура, содержащая информацию о редукторе
	* \endrussian
	*/
/** $XIW
	* \english
	* Deprecated. Set gear information to the EEPROM.
	* Can be used by the manufacturer only.
	* @param id An identifier of a device
	* @param[in] gear_information structure contains information about step gearhead
	* \endenglish
	* \russian
	* Запись информации о редукторе в EEPROM.
	* Функция должна использоваться только производителем.
	* @param id идентификатор устройства
	* @param[in] gear_information структура, содержащая информацию о редукторе
	* \endrussian
	*/
/** $XIS
	* \english
	* Deprecated. Gear information.
	* \endenglish
	* \russian
	* Информация о редукторе.
	* \endrussian
	* @see set_gear_information
	* @see get_gear_information
	*/
command "gear_information" universal "gri" (70)
fields:
	char Manufacturer[16]			/**< \english Manufacturer. Max string length: 16 chars. \endenglish \russian Производитель. Максимальная длина строки: 16 символов. \endrussian */	
	char PartNumber[24]				/**< \english Series and PartNumber. Max string length: 24 chars. \endenglish \russian Серия и номер модели. Максимальная длина строки: 24 символа. \endrussian */	
	reserved 24

/** $XIR
	* \english
	* Deprecated. Read gear settings from the EEPROM.
	* @param id An identifier of a device
	* @param[out] gear_settings structure contains step gearhead settings
	* \endenglish
	* \russian
	* Чтение настроек редуктора из EEPROM.
	* @param id идентификатор устройства
	* @param[out] gear_settings структура, содержащая настройки редуктора
	* \endrussian
	*/
/** $XIW
	* \english
	* Deprecated. Set gear settings to the EEPROM.
	* Can be used by the manufacturer only.
	* @param id An identifier of a device
	* @param[in] gear_settings structure contains step gearhead settings
	* \endenglish
	* \russian
	* Запись настроек редуктора в EEPROM.
	* Функция должна использоваться только производителем.
	* @param id идентификатор устройства
	* @param[in] gear_settings структура, содержащая настройки редуктора
	* \endrussian
	*/
/** $XIS
	* \english
	* Deprecated. Gear settings.
	* \endenglish
	* \russian
	* Настройки редуктора.
	* \endrussian
	* @see set_gear_settings
	* @see get_gear_settings
	*/
command "gear_settings" universal "grs" (58)
fields:
	float ReductionIn			/**< \english Input reduction coefficient. (Output = (ReductionOut / ReductionIn) * Input) Data type: float. \endenglish \russian Входной коэффициент редуктора. (Выход = (ReductionOut/ReductionIn) * вход) Тип данных: float. \endrussian */
	float ReductionOut			/**< \english Output reduction coefficient. (Output = (ReductionOut / ReductionIn) * Input) Data type: float. \endenglish \russian Выходной коэффициент редуктора. (Выход = (ReductionOut/ReductionIn) * вход) Тип данных: float. \endrussian */
	float RatedInputTorque		/**< \english Maximum continuous torque (N * m). Data type: float. \endenglish \russian Максимальный крутящий момент (Н * м). Тип данных: float. \endrussian */
	float RatedInputSpeed		/**< \english Maximum speed on the input shaft (rpm). Data type: float. \endenglish \russian Максимальная скорость на входном валу редуктора (об/мин). Тип данных: float. \endrussian */
	float MaxOutputBacklash		/**< \english Output backlash of the reduction gear (degree). Data type: float. \endenglish \russian Выходной люфт редуктора (градус). Тип данных: float.\endrussian */
	float InputInertia			/**< \english Equivalent input gear inertia (g * cm2). Data type: float. \endenglish \russian Эквивалентная входная инерция редуктора(г * см2). Тип данных: float. \endrussian */
	float Efficiency			/**< \english Reduction gear efficiency (%). Data type: float. \endenglish \russian КПД редуктора (%). Тип данных: float. \endrussian */
	reserved 24

/** $XIR
	* \english
	* Deprecated. Read additional accessory information from the EEPROM.
	* @param id An identifier of a device
	* @param[out] accessories_settings structure contains information about additional accessories
	* \endenglish
	* \russian
	* Чтение информации о дополнительных аксессуарах из EEPROM.
	* @param id идентификатор устройства
	* @param[out] accessories_settings структура, содержащая информацию о дополнительных аксессуарах
	* \endrussian
	*/
/** $XIW
	* \english
	* Deprecated. Set additional accessories' information to the EEPROM.
	* Can be used by the manufacturer only.
	* @param id An identifier of a device
	* @param[in] accessories_settings structure contains information about additional accessories
	* \endenglish
	* \russian
	* Запись информации о дополнительных аксессуарах в EEPROM.
	* Функция должна использоваться только производителем.
	* @param id идентификатор устройства
	* @param[in] accessories_settings структура, содержащая информацию о дополнительных аксессуарах
	* \endrussian
	*/
/** $XIS
	* \english
	* Deprecated. Additional accessories' information.
	* \endenglish
	* \russian
	* Информация о дополнительных аксессуарах.
	* \endrussian
	* @see set_accessories_settings
	* @see get_accessories_settings
	*/
	
command "accessories_settings" universal "acc" (114)
fields:
	char MagneticBrakeInfo[24]		/**< \english The manufacturer and the part number of magnetic brake, the maximum string length is 24 characters. \endenglish \russian Производитель и номер магнитного тормоза, Максимальная длина строки: 24 символов. \endrussian */ 
	float MBRatedVoltage			/**< \english Rated voltage for controlling the magnetic brake (V). Data type: float. \endenglish \russian Номинальное напряжение для управления магнитным тормозом (В). Тип данных: float. \endrussian */
	float MBRatedCurrent			/**< \english Rated current for controlling the magnetic brake (A). Data type: float. \endenglish \russian Номинальный ток для управления магнитным тормозом (А). Тип данных: float. \endrussian */ 
	float MBTorque					/**< \english Retention moment (mN * m). Data type: float. \endenglish \russian Удерживающий момент (мН * м). Тип данных: float. \endrussian */ 
	int32u flag MBSettings of MBSettingsFlags 	/**< \english Flags of magnetic brake settings. This is a bit mask for bitwise operations. \endenglish \russian Флаги настроек магнитного тормоза. Это битовая маска для побитовых операций. \endrussian */ 
	char TemperatureSensorInfo[24]	/**< \english The manufacturer and the part number of the temperature sensor, the maximum string length: 24 characters. \endenglish \russian Производитель и номер температурного датчика, Максимальная длина строки: 24 символов. \endrussian */ 
	float TSMin						/**< \english The minimum measured temperature (degrees Celsius) Data type: float. \endenglish \russian Минимальная измеряемая температура (град Цельсия). Тип данных: float. \endrussian */ 
	float TSMax						/**< \english The maximum measured temperature (degrees Celsius) Data type: float. \endenglish \russian Максимальная измеряемая температура (град Цельсия) Тип данных: float. \endrussian */ 
	float TSGrad					/**< \english The temperature gradient (V/degrees Celsius). Data type: float. \endenglish \russian Температурный градиент (В/град Цельсия). Тип данных: float. \endrussian */ 
	int32u flag TSSettings of TSSettingsFlags 	/**< \english Flags of temperature sensor settings. This is a bit mask for bitwise operations. \endenglish \russian Флаги настроек температурного датчика. Это битовая маска для побитовых операций. \endrussian */ 
	int32u flag LimitSwitchesSettings of LSFlags	/**< \english Flags of limit switches settings. This is a bit mask for bitwise operations. \endenglish \russian Флаги настроек концевых выключателей. Это битовая маска для побитовых операций. \endrussian */ 
	reserved 24	
	
//@}
/**
	* \english
	* @name Bootloader commands
	*
	* \endenglish
	* \russian
	* @name Команды загрузчика
	*
	* \endrussian
	*/

//@{

/** $XIR
	* \english
	* Read the controller's bootloader version.
	* @param id An identifier of a device
	* @param[out] Major major version
	* @param[out] Minor minor version
	* @param[out] Release release version
	* \endenglish
	* \russian
	* Чтение номера версии загрузчика контроллера.
	* @param id идентификатор устройства
	* @param[out] Major номер основной версии
	* @param[out] Minor номер дополнительной версии
	* @param[out] Release номер релиза
	* \endrussian
	*/
command "bootloader_version" reader "gblv" (10)
with inline
fields:
	int8u Major		/**< \english Bootloader major version number \endenglish \russian Мажорный номер версии загрузчика \endrussian */
	int8u Minor		/**< \english Bootloader minor version number \endenglish \russian Минорный номер версии загрузчика \endrussian */
	int16u Release	/**< \english Bootloader release version number \endenglish \russian Номер релиза версии загрузчика \endrussian */

/** $XIW
		* \english
		* Command initiates the transfer of control to firmware. This command is also available in the firmware for compatibility.
		* Result = RESULT_OK, if the transition from the loader to the firmware is possible. After the response to this command, the transition is executed.
		* Result = RESULT_NO_FIRMWARE if the firmware is not found.
		* Result = RESULT_ALREADY_IN_FIRMWARE if this command is called from the firmware.
		* @param id An identifier of a device
		* @param[out] sresult command result
		* \endenglish
		* \russian
		* Команда инициирует передачу управления прошивке. Эта команда так же доступна из прошивки, для совместимости.
		* Result = RESULT_OK, если переход из загрузчика в прошивку возможен. После ответа на эту команду выполняется переход.
		* Result = RESULT_NO_FIRMWARE, если прошивка не найдена.
		* Result = RESULT_ALREADY_IN_FIRMWARE, если эта команда была вызвана из прошивки.
		* @param id идентификатор устройства
		* @param[out] sresult результат выполнения команды
		* \endrussian
*/
command "service_command_goto_firmware_impl" writer "gofw" (4) reader "gofw" (15)
with inline
without public, crc
answer:
	int8u serviceanswer sresult	/**< \english Result of the command. \endenglish \russian Результат выполнения команды. \endrussian */
	reserved 8

/** $XIR
	* \english
	* Read a random number from the controller.
	* @param id An identifier of a device
	* @param[out] init_random random sequence generated by the controller
	* \endenglish
	* \russian
	* Чтение случайного числа из контроллера.
	* @param id идентификатор устройства
	* @param[out] init_random случайная последовательность, сгенерированная контроллером
	* \endrussian
	*/
/** $XIS
	* \english
	* Random key.
	*
	* Structure that contains a random key. It is used in the encryption of WKEY and SSER command contents.
	* \endenglish
	* \russian
	* Случайный ключ.
	* Структура которая содержит случайный ключ, использующийся для шифрования содержимого команд WKEY и SSER.
	* \endrussian
	*/
command "init_random" reader "irnd" (24)
with public
fields:
	byte key[16] /**< \english Random key. \endenglish \russian Случайный ключ. \endrussian */
	reserved 2

/** $XIR
  * \english
  * This value is unique to each individual device, but is not a random value.
  * This unique device identifier can be used to initiate secure boot processes or as a serial number for USB or other end applications.
  * @param id An identifier of a device
  * @param[out] globally_unique_identifier the result of fields 0-3 concatenated defines the unique 128-bit device identifier.
  * \endenglish
  * \russian
  * Считывает уникальный идентификатор каждого чипа, это значение не является случайным.
  * Уникальный идентификатор может быть использован в качестве инициализационного вектора
  * для операций шифрования бутлоадера или в качестве серийного номера для USB и других применений.
  * @param id идентификатор устройства
  * @param[out] globally_unique_identifier результат полей 0-3 определяет уникальный 128-битный идентификатор.
  * \endrussian
  */
/** $XIS
  * \english
  * Globally unique identifier.
  * \endenglish
  * \russian
  * Глобальный уникальный идентификатор.
  * \endrussian
  */
command "globally_unique_identifier" reader "guid" (40)
with public
fields:
  int32u UniqueID0 /**< \english Unique ID 0. \endenglish \russian Уникальный ID 0. \endrussian */
  int32u UniqueID1 /**< \english Unique ID 1. \endenglish \russian Уникальный ID 1. \endrussian */
  int32u UniqueID2 /**< \english Unique ID 2. \endenglish \russian Уникальный ID 2. \endrussian */
  int32u UniqueID3 /**< \english Unique ID 3. \endenglish \russian Уникальный ID 3. \endrussian */
  reserved 18

/** $XIR
	* \english
	* Check for firmware on device.
	* Result = RESULT_NO_FIRMWARE if the firmware is not found.
	* Result = RESULT_HAS_FIRMWARE if the firmware has been found.
	* @param name a name of device
	* @param[out] ret non-zero if the firmware existed
	* \endenglish
	* \russian
	* Команда определяет наличие в контроллере ПО.
	* Данная команда доступна так же из прошивки.
	* Result = RESULT_NO_FIRMWARE, если прошивка не найдена.
	* Result = RESULT_HAS_FIRMWARE, если прошивка найдена.
	* @param name имя устройства
	* @param[out] ret не ноль, если прошивка присутствует
	* \endrussian
	*/
command "service_command_has_firmware_impl" writer "hasf" (4) reader "hasf" (15)
with inline
without public, crc
answer:
	int8u serviceanswer sresult	/**< \english Result of command. \endenglish \russian Результат выполнения команды. \endrussian */
	reserved 8

/** $XIW
	* \english
	* Write command key to decrypt the firmware.
	* Result = RESULT_OK, if the command loader.
	* Result = RESULT_HARD_ERROR if there was a mistake at the time of the command.
	* The Result is not available through the library write_key(). The function processes it internally.
	* Can be used by the manufacturer only.
	* @param Name a name of device
	* @param[in] Key protection key.
	* \endenglish
	* \russian
	* Команда записи ключа для расшифровки прошивки.
	* Result = RESULT_OK, если команда выполнена загрузчиком.
	* Result = RESULT_HARD_ERROR, если во время выполнения команды произошла ошибка.
	* Result не доступен через функцию библиотеки write_key, значение поля обрабатывается внутри функции.
	* Функция используется только производителем.
	* @param Name имя устройства
	* @param[in] Key ключ защиты.
	* \endrussian
	*/
command "service_command_write_key_impl" writer "wkey" (46) reader "wkey" (15)
with inline
without public
fields:
	byte Key[32]	/**< \english Protection key (256 bit). \endenglish \russian Ключ защиты (256 бит). \endrussian */
	reserved 8
answer:
	int8u serviceresult sresult	/**< \english Command result. \endenglish \russian Результат выполнения команды. \endrussian */
	reserved 8

/** $XIR
	* \english
	* Command to open a ISP session (in-system programming) when downloading the firmware.
	* Result = RESULT_OK if the command loader.
	* Result = RESULT_SOFT_ERROR if an error occurred at the time of the command.
	* The Result is not available through the library command_update_firmware(). The function processes it internally.
	* @param name a name of device
	* @param[out] ret non-zero if the loader completes the command.
	* \endenglish
	* \russian
	* Команда служит для открытия сеанса ISP (in-system programming) при загрузке прошивки.
	* Result = RESULT_OK, если команда выполнена загрузчиком.
	* Result = RESULT_SOFT_ERROR, если во время выполнения команды произошла ошибка.
	* Result не доступен через функцию библиотеки command_update_firmware, значение
	* поля обрабатывается внутри функции.
	* @param name имя устройства
	* @param[out] ret не ноль, если команда выполнена загрузчиком.
	* \endrussian
	*/
command "service_command_connect_impl" writer "conn" (14) reader "conn" (15)
without public
with inline
fields:
	reserved 8
answer:
	int8u serviceresult sresult	/**< \english Command result. \endenglish \russian Результат выполнения команды. \endrussian */
	reserved 8

/** $XIR
	* \english
	* Command to close the ISP session (in-system programming) when loading firmware.
	* Result = RESULT_OK if the command loader.
	* Result = RESULT_HARD_ERROR if a hardware error occurred at the time of the command.
	* Result = RESULT_SOFT_ERROR if a software error occurred at the time of the command.
	* The Result is not available through the library command_update_firmware(). The function processes it internally.
	* @param name a name of device
	* @param[out] ret non-zero if the loader completed the command.
	* \endenglish
	* \russian
	* Команда служит для закрытия сеанса ISP (in-system programming) при загрузке прошивки.
	* Result = RESULT_OK, если команда выполнена загрузчиком.
	* Result = RESULT_HARD_ERROR, если во время выполнения команды произошла аппаратная ошибка.
	* Result = RESULT_SOFT_ERROR, если во время выполнения команды произошла программная ошибка.
	* Result не доступен через функцию библиотеки command_update_firmware,
	* значение поля обрабатывается внутри функции.
	* @param name имя устройства
	* @param[out] ret не ноль, если команда выполнена загрузчиком.
	* \endrussian
	*/
command "service_command_disconnect_impl" writer "disc" (14) reader "disc" (15)
with inline
without public
fields:
	reserved 8
answer:
	int8u serviceresult sresult	/**< \english Command result. \endenglish \russian Результат выполнения команды. \endrussian */
	reserved 8

/** $XIW
	* \english
	* Writes encoded firmware to the controller's flash memory.
	* The result of each packet write is not available. The overall result is available when the firmware upload is finished.
	* @param[in] Data[128] Encoded firmware
	* \endenglish
	* \russian
	* Записывает данные (прошивку) во Flash память контроллера.
	* Не возвращает результат выполнения, хотя может завершаться ошибкой.
	* Ошибочность заливки и тип ошибки можно узнать при завершении заливки.
	* @param[in] Data[128] Закодированная прошивка
	* \endrussian
	*/
command "service_command_write_data_impl" writer "wdat" (142) reader "wdat" (4)
without public
with inline
fields:
	byte Data[128]	metalen	/**< \english Encoded firmware. \endenglish \russian Закодированная прошивка. \endrussian */
	reserved 8

/** $XIW
	* \english
	* The controller reset command. After the reset, the controller goes into bootloader mode.  The command is added for compatibility with the loader exchange protocol.
	* There is no response to this command.
	* \endenglish
	* \russian
	* Команда сброса контроллера и перехода в режим загрузчика, добавлена для
	* совместимости с Протоколом Обмена Загрузчика. Ответа на эту команду нет.
	* \endrussian
	*/
command "service_command_reset_impl" writer "rest" (4) reader "rest" (0)
without answer, public, crc


//@}


/**
	* \english
	* @name Service functions
	* Functions are intended for deep controller setup.
	* There is no necessity to use it during normal operation.
	* These functions have to be used by skilled engineers only.
	* If you want to use it, please consult the manufacturer.
	* Wrong usage may lead to device malfunction, which can lead to irreversible damage to the board.
	* \endenglish
	* \russian
	* @name Сервисные функции
	* Эти функции необходимы для начального конфигурирования, тестирования и обновления устройства.
	* Не применяйте их при обычной работе с контроллером.
	* При необходимости, проконсультируйтесь пожалуйста с производителем.
	* Неправильное использование этих функций может привести к неработоспособности устройства.
	* \endrussian
	*/























/** vim: set ft=xi ts=4 sw=4: */
