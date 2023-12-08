#ifndef INC_XIMC_H
#define INC_XIMC_H

/** @file ximc.h
	* \english
	*		@brief Header file for libximc library
	* \endenglish
	* \russian
	*		@brief Заголовочный файл для библиотеки libximc
	* \endrussian
	*/

/** @def XIMC_API
	* \english
	* 		@brief Library import macro.
	* 		Macros allows to automatically import function from shared library.
	* 		It automatically expands to dllimport on msvc when including header file.
	* \endenglish
	* \russian
	*		@brief Макрос импорта библиотеки.
	*		Макросы позволяют автоматически импортировать функцию из общей библиотеки.
	*		Он автоматически расширяется до dllimport на msvc при включении файла заголовка.
	* \endrussian
	*/
#if defined(_WIN32) || defined(LABVIEW64_IMPORT) || defined(LABVIEW32_IMPORT) || defined(MATLAB_IMPORT)
	#define XIMC_API __stdcall
#else
	#ifdef LIBXIMC_EXPORTS
	#define XIMC_API __attribute__((visibility("default")))
	#else
	#define XIMC_API
	#endif
#endif

/** @def XIMC_CALLCONV
	* \english
	*		@brief Library calling convention macros.
	* \endenglish
	* \russian
	*		@brief Библиотека вызывающая условные макросы.
	* \endrussian
	*/
#if defined(_WIN32) || defined(LABVIEW64_IMPORT) || defined(LABVIEW32_IMPORT) || defined(MATLAB_IMPORT)
	#define XIMC_CALLCONV __stdcall
#else
	#define XIMC_CALLCONV
#endif

/** @def XIMC_RETTYPE
	* \english
	* 		@brief Thread return type.
	* \endenglish
	* \russian
	*		@brief Возвращаеемый тип потока.
	* \endrussian
	*/
#if defined(_WIN32) || defined(LABVIEW64_IMPORT) || defined(LABVIEW32_IMPORT) || defined(MATLAB_IMPORT)
#define XIMC_RETTYPE unsigned int
#else
#define XIMC_RETTYPE void*
#endif


#if !defined(XIMC_NO_STDINT)

#if ( (defined(_MSC_VER) && (_MSC_VER < 1600)) || defined(LABVIEW64_IMPORT) || defined(LABVIEW32_IMPORT)) && !defined(MATLAB_IMPORT)
// msvc types burden
typedef __int8 int8_t;
typedef __int16 int16_t;
typedef __int32 int32_t;
typedef __int64 int64_t;
typedef unsigned __int8 uint8_t;
typedef unsigned __int16 uint16_t;
typedef unsigned __int32 uint32_t;
typedef unsigned __int64 uint64_t;
#else
#include <stdint.h>
#endif

/* labview doesn't speak C99 */
#if defined(LABVIEW64_IMPORT) || defined(LABVIEW32_IMPORT)
typedef unsigned __int64 ulong_t;
typedef __int64 long_t;
#else
typedef unsigned long long ulong_t;
typedef long long long_t;
#endif

#endif

#include <time.h>

#if defined(__cplusplus)
extern "C"
{
#endif


	/**
		\english
		* Type describes device identifier
		\endenglish
		\russian
		* Тип идентификатора устройства
		\endrussian
		*/
	typedef int device_t;

	/**
		\english
		* Type specifies result of any operation
		\endenglish
		\russian
		* Тип, определяющий результат выполнения команды.
		\endrussian
		*/
	typedef int result_t;

	/**
		\english
		* Type describes device enumeration structure
		\endenglish
		\russian
		* Тип, определяющий структуру данных о всех контроллерах, обнаруженных при опросе устройств.
		\endrussian
		*/
	#if defined(_WIN64) || defined(__LP64__) || defined(LABVIEW64_IMPORT)
	typedef uint64_t device_enumeration_t;
	#else
	typedef uint32_t device_enumeration_t;
	#endif
	//typedef device_enumeration_t* pdevice_enumeration_t;

	/**
		\english
		* Handle specified undefined device
		\endenglish
		\russian
		* Макрос, означающий неопределенное устройство
		\endrussian
		*/
#define device_undefined -1

	/** \english
		@name Result statuses
		\endenglish
		\russian
		@name Результаты выполнения команд
		\endrussian
		*/
	//@{

	/**
		\english
		* success
		\endenglish
		\russian
		* выполнено успешно
		\endrussian
		*/
#define result_ok 0

	/**
		\english
		* generic error
		\endenglish
		\russian
		* общая ошибка
		\endrussian
		*/
#define result_error -1

	/**
		\english
		* function is not implemented
		\endenglish
		\russian
		* функция не определена
		\endrussian
		*/
#define result_not_implemented -2

	/**
		\english
		* value error
		\endenglish
		\russian
		* ошибка записи значения
		\endrussian
		*/
#define result_value_error -3

	/**
		\english
		* device is lost
		\endenglish
		\russian
		* устройство не подключено
		\endrussian
		*/
#define result_nodevice -4

	//@}

	/** \english
		@name Logging level
		\endenglish
		\russian
		@name Уровень логирования
		\endrussian
		*/
	//@{

	/**
		\english
		* Logging level - error
		\endenglish
		\russian
		* Уровень логирования - ошибка
		\endrussian
		*/
#define LOGLEVEL_ERROR 		0x01
	/**
		\english
		* Logging level - warning
		\endenglish
		\russian
		* Уровень логирования - предупреждение
		\endrussian
		*/
#define LOGLEVEL_WARNING 	0x02
	/**
		\english
		* Logging level - info
		\endenglish
		\russian
		* Уровень логирования - информация
		\endrussian
		*/
#define LOGLEVEL_INFO		0x03
	/**
		\english
		* Logging level - debug
		\endenglish
		\russian
		* Уровень логирования - отладка
		\endrussian
		*/
#define LOGLEVEL_DEBUG		0x04
	//@}


	/**
		\english
		* Calibration structure
		\endenglish
		\russian
		* Структура калибровок
		\endrussian	 */
	typedef struct calibration_t
	{
		double A; 		/**< \english is a conversion factor which is equal number of millimeters (or other units) per one step  \endenglish \russian коэффициент преобразования, равный количеству миллиметров (или других единиц) на один шаг \endrussian */
		unsigned int MicrostepMode;			/**< \english is a controller setting which is determine a step division mode \endenglish \russian это настройка контроллера, определяющая режим пошагового деления \endrussian */
	} calibration_t;

	/**
		\english
		* Device network information structure.
		\endenglish
		\russian
		* Структура данных с информацией о сетевом устройстве.
		\endrussian	 */
	typedef struct device_network_information_t
	{
		uint32_t ipv4; 		/**< \english IPv4 address, passed in network byte order (big-endian byte order) \endenglish \russian IPv4-адрес, передаваемый в сетевом байтовом порядке (big-endian byte order) \endrussian */
		char nodename[16]; 		/**< \english name of the Bindy node which hosts the device \endenglish \russian имя узла Bindy, на котором размещено устройство \endrussian */
		
		uint32_t axis_state; 		/**< \english flags representing device state \endenglish \russian флаги, представляющие состояние устройства \endrussian */
		char locker_username[16]; 		/**< \english name of the user who locked the device (if any) \endenglish \russian имя пользователя, заблокировавшего устройство (если таковое имеется) \endrussian */
		char locker_nodename[16]; 		/**< \english Bindy node name, which was used to lock the device (if any) \endenglish \russian имя узла Bindy, которое использовалось для блокировки устройства (если таковое имеется) \endrussian */
		time_t locked_time; 		/**< \english time the lock was acquired at (UTC, microseconds since the epoch) \endenglish \russian время, в которое была получена блокировка (UTC, микросекунды с момента начала эпохи) \endrussian */
	} device_network_information_t;


/* @@GENERATED_CODE@@ */

/* hand-crafted functions begin */

	/**
		* \english
		* Reboot to firmware
		* @param id an identifier of device
		* @param[out] ret RESULT_OK, if reboot to firmware is possible. Reboot is done after reply to this command. RESULT_NO_FIRMWARE, if firmware is not found. RESULT_ALREADY_IN_FIRMWARE, if this command was sent when controller is already in firmware.
		* \endenglish
		* \russian
		* Перезагрузка в прошивку в контроллере
		* @param id идентификатор устройства
		* @param[out] ret RESULT_OK, если переход из загрузчика в прошивку возможен. После ответа на эту команду выполняется переход. RESULT_NO_FIRMWARE, если прошивка не найдена. RESULT_ALREADY_IN_FIRMWARE, если эта команда была вызвана из прошивки.
		* \endrussian
		*/
	result_t XIMC_API goto_firmware(device_t id, uint8_t* ret);

	/**
		* \english
		* Check for firmware on device
		* @param uri a uri of device
		* @param[out] ret non-zero if firmware existed
		* \endenglish
		* \russian
		* Проверка наличия прошивки в контроллере
		* @param uri уникальный идентификатор ресурса устройства
		* @param[out] ret ноль, если прошивка присутствует
		* \endrussian
		*/
	result_t XIMC_API has_firmware(const char* uri, uint8_t* ret);

	/**
		* \english
		* Update firmware. Manufacturer only.
		* Service command
		* @param uri a uri of device
		* @param data firmware byte stream
		* @param data_size size of byte stream
		* \endenglish
		* \russian
		* Обновление прошивки. Команда только для производителя.
		* @param uri идентификатор устройства
		* @param data указатель на массив байтов прошивки
		* @param data_size размер массива в байтах
		* \endrussian
		*/
	result_t XIMC_API command_update_firmware(const char* uri, const uint8_t* data, uint32_t data_size);

/**
	* \english
	* Write controller key.
	* Can be used by manufacturer only
	* @param uri a uri of device
	* @param[in] key protection key. Range: 0..4294967295
	* \endenglish
	* \russian
	* Запись ключа защиты
	* Функция используется только производителем.
	* @param uri идентификатор устройства
	* @param[in] key ключ защиты. Диапазон: 0..4294967295
	* \endrussian
	*/
	result_t XIMC_API write_key (const char* uri, uint8_t* key);

/**
	* \english
	* Reset controller.
	* Can be used by manufacturer only
	* @param id an identifier of device
	* \endenglish
	* \russian
	* Перезагрузка контроллера.
	* Функция используется только производителем.
	* @param id идентификатор устройства
	* \endrussian
	*/
	result_t XIMC_API command_reset(device_t id);

/**
	* \english
	* Clear controller FRAM.
	* Can be used by manufacturer only
	* @param id an identifier of device
	* \endenglish
	* \russian
	* Очистка FRAM памяти контроллера.
	* Функция используется только производителем.
	* @param id идентификатор устройства
	* \endrussian
	*/
	result_t XIMC_API command_clear_fram(device_t id);

	//@}

	// ------------------------------------

	/**
		\english
		@name Boards and drivers control
		* Functions for searching and opening/closing devices
		\endenglish
		\russian
		@name Управление устройством
		* Функции поиска и открытия/закрытия устройств
		\endrussian
		*/
	//@{

	/**
		* \english
		* Open a device with OS \a uri and return identifier of the device which can be used in calls.
		* @param[in] uri - a device URI.
		* Device URI has a form of "xi-com:port" or "xi-net://host/serial" or "xi-emu:///abs_path_to_file". For POSIX systems one can ommit root-slash in abs_path_to_file; for example, "xi-emu:///home/user/virt_controller.bin". 
		* In case of USB-COM port, the "port" is the OS device URI. For example, "xi-com:\\\\\.\\COM3" in Windows (note that double-backslash will be transformed to single-backslash) or "xi-com:///dev/ttyACM0" in Linux/Mac.
		* In case of network device, the "host" is an IPv4 address or fully qualified domain URI (FQDN), "serial" is the device serial number in hexadecimal system.
		* For example, "xi-net://192.168.0.1/00001234" or "xi-net://hostname.com/89ABCDEF".
		* In case of UDP protocol, use "xi-udp://<ip/host>:<port>.
		* For example, "xi-udp://192.168.0.1:1818".
		* In case of virtual device, the "abs_file_to_file" is the full path to the virtual device's file. If it doesn't exist, then it is created and initialized with default values.
		* For example, "xi-emu:///C:/dir/file.bin" in Windows or "xi-emu:///home/user/file.bin" in Linux/Mac.
		* \endenglish
		* \russian
		* Открывает устройство по имени \a uri и возвращает идентификатор, который будет использоваться для обращения к устройству.
		* @param[in] uri - уникальный идентификатор устройства.
		* URI устройства имеет вид "xi-com:port" или "xi-net://host/serial" или "xi-emu:///abs_path_to_file". На POSIX системах допускается пропуск "рутовского" слэша; например, "xi-emu:///home/user/virt_controller.bin".
		* Для USB-COM устройства "port" это URI устройства в ОС.
		* Например, "xi-com:\\\\\.\\COM3" в Windows (с учётом экранирования двойные обратные слэши преобразуются в одинарные) или "xi-com:///dev/ttyACM0" в Linux/Mac.
		* Для сетевого устройства "host" это IPv4 адрес или полностью определённое имя домена, "serial" это серийный номер устройства в шестнадцатеричной системе.
		* Например, "xi-net://192.168.0.1/00001234" или "xi-net://hostname.com/89ABCDEF".
		* Для работы по UDP протоколу используйте "xi-udp://<ip/host>:<port>.
		* Например, "xi-udp://192.168.0.1:1818".
		* Для виртуального устройства "abs_file_to_file" это путь к файлу с сохраненным состоянием устройства. Если файл не существует, он будет создан и инициализирован значениями по умолчанию.
		* Например, "xi-emu:///C:/dir/file.bin" в Windows или "xi-emu:///home/user/file.bin" в Linux/Mac.
		* \endrussian
		*/
	device_t XIMC_API open_device (const char* uri);

	/**
		* \english
		* Close specified device
		* @param id an identifier of device
		* \note
		* The id parameter in this function is a C pointer, unlike most library functions that use this parameter
		* \endenglish
		* \russian
		* Закрывает устройство
		* @param id - идентификатор устройства
		* \note
		* Параметр id в данной функции является Си указателем, в отличие от большинства функций библиотеки использующих данный параметр
		* \endrussian
		*/
	result_t XIMC_API close_device (device_t* id);

	/**
		* \english
		* Command of loading a correction table from a text file (this function is deprecated).
		* Use the function set_correction_table(device_t id, const char* namefile).
		* The correction table is used for position correction in case of mechanical inaccuracies.
		* It works for some parameters in _calb commands.
		* @param id an identifier the device
		* @param[in] namefile - the file name must be fully qualified.
		* If the short name is used, the file must be located in the application directory.
		* If the file name is set to NULL, the correction table will be cleared.
		* File format: two tab-separated columns.
		* Column headers are string.
		* Data is real, the point is a determiter.
		* The first column is a coordinate. The second one is the deviation caused by a mechanical error.
		* The maximum length of a table is 100 rows.
		* \note
		* The id parameter in this function is a C pointer, unlike most library functions that use this parameter
		* @see command_move
		* @see get_position_calb
		* @see get_position_calb_t
		* @see get_status_calb
		* @see status_calb_t
		* @see get_edges_settings_calb
		* @see set_edges_settings_calb
		* @see edges_settings_calb_t
		*
		* \endenglish
		* \russian
		* Команда загрузки корректирующей таблицы из текстового файла (данная функция устарела).
		* Используйте функцию set_correction_table(device_t id, const char* namefile).
		* Таблица используется для коррекции положения в случае механических неточностей.
		* Работает для некоторых параметров в _calb командах.
		* @param id - идентификатор устройства
		* @param[in] namefile - имя файла должно быть полным.
		* Если используется короткое имя, файл должен находится в директории приложения.
		* Если имя файла равно NULL таблица коррекции будет очищена.
		* Формат файла: два столбца разделенных табуляцией.
		* Заголовки столбцов строковые.
		* Данные действительные разделитель точка.
		* Первый столбец координата. Второй - отклонение вызванное ошибкой механики.
		* Между координатами отклонение расчитывается линейно. За диапазоном константа равная отклонению на границе.
		* Максимальная длина таблицы 100 строк.		
		* \note
		* Параметр id в данной функции является Си указателем, в отличие от большинства функций библиотеки использующих данный параметр
		* @see command_move
		* @see command_movr
		* @see get_position_calb
		* @see get_position_calb_t
		* @see get_status_calb
		* @see status_calb_t
		* @see get_edges_settings_calb
		* @see set_edges_settings_calb
		* @see edges_settings_calb_t
		* \endrussian
		*/
	result_t XIMC_API load_correction_table(device_t* id, const char* namefile);

	/**
	* \english
	* Command of loading a correction table from a text file.
	* The correction table is used for position correction in case of mechanical inaccuracies.
	* It works for some parameters in _calb commands.
	* @param id an identifier the device
	* @param[in] namefile - the file name must be either a full path or a relative path. If the file name is set to NULL,
	* the correction table will be cleared. File format: two tab-separated columns. Column headers are strings.
	* Data is real, the dot is a delimiter. The first column is a coordinate. The second one is the deviation
	* caused by a mechanical error. The maximum length of a table is 100 rows. Coordinate column must be sorted in
	* ascending order.
	* @see command_move
	* @see get_position_calb
	* @see get_position_calb_t
	* @see get_status_calb
	* @see status_calb_t
	* @see get_edges_settings_calb
	* @see set_edges_settings_calb
	* @see edges_settings_calb_t
	*
	* \endenglish
	* \russian
	* Команда загрузки корректирующей таблицы из текстового файла.
	* Таблица используется для коррекции положения в случае механических неточностей.
	* Работает для некоторых параметров в _calb командах.
	* @param id - идентификатор устройства
	* @param[in] namefile - путь до файла должен быть полным или относительным.
	* Если параметр равен NULL, таблица коррекции будет очищена.
	* Формат файла: два столбца, разделенных табуляцией.
	* Заголовки столбцов строковые.
	* Данные действительные, разделитель точка.
	* Первый столбец - координата. Второй - отклонение, вызванное ошибкой механики.
	* Максимальная длина таблицы 100 строк. Координаты должны быть отсортированы по возрастанию.
	* @see command_move
	* @see command_movr
	* @see get_position_calb
	* @see get_position_calb_t
	* @see get_status_calb
	* @see status_calb_t
	* @see get_edges_settings_calb
	* @see set_edges_settings_calb
	* @see edges_settings_calb_t
	* \endrussian
	*/
	result_t XIMC_API set_correction_table(device_t id, const char* namefile);

	/**
		* \english
		* Check if a device with OS uri \a uri is XIMC device.
		* Be carefuly with this call because it sends some data to the device.
		* @param[in] uri - a device uri
		* \endenglish
		* \russian
		* Проверяет, является ли устройство с уникальным идентификатором \a uri XIMC-совместимым.
		* Будьте осторожны с вызовом этой функции для неизвестных устройств, т.к. она отправляет данные.
		* @param[in] uri - уникальный идентификатор устройства
		* \endrussian
		*/
	result_t XIMC_API probe_device (const char* uri);

	/**
		* \english
		* Set network encryption layer (bindy) key.
		* @param[in] keyfilepath full path to the bindy keyfile
		* When using network-attached devices this function must be called before {@link enumerate_devices} and {@link open_device} functions.
		* \endenglish
		* \russian
		* Устанавливливает ключ шифрования сетевой подсистемы (bindy).
		* @param[in] keyfilepath полный путь к файлу ключа
		* В случае использования сетевых устройств эта функция должна быть вызвана до функций {@link enumerate_devices} и {@link open_device}.
		* \endrussian
	 */
	result_t XIMC_API set_bindy_key(const char* keyfilepath);

	/**
		* \english
		* Enumerate all devices that looks like valid.
		* @param[in] enumerate_flags enumerate devices flags
		* @param[in] hints extended information
		* \par
		* hints is a string of form "key=value \n key2=value2". <em>Unrecognized key-value pairs are ignored</em>.
		* Key list: addr - used together with ENUMERATE_NETWORK flag.
		* Non-null value is a remote host name or a comma-separated list of host names which contain the devices to be found, absent value means broadcast discovery.
		* adapter_addr - used together with ENUMERATE_NETWORK flag.
		* Non-null value is a IP address of network adapter. Remote ximc device must be on the same local network as the adapter.
		* When using the adapter_addr key, you <b>must set</b> the addr key. Example: "addr= \n adapter_addr=192.168.0.100".
		* \endenglish
		* \russian
		* Перечисляет все XIMC-совместимые устройства.
		* @param[in] enumerate_flags флаги поиска устройств
		* @param[in] hints дополнительная информация для поиска
		* \par
		* hints это строка вида "ключ=значение \n ключ2=значение2". <em>Неизвестные пары ключ-значение игнорируются</em>.
		* Список ключей: addr - используется вместе с флагом ENUMERATE_NETWORK.
		* Ненулевое значение это адрес или список адресов с перечислением через запятую удаленных хостов на которых происходит поиск устройств. 
		* Отсутствующее значение это подключение посредством широковещательного запроса.
		* adapter_addr - используется вместе с флагом ENUMERATE_NETWORK.
		* Ненулевое значение это IP адрес сетевого адаптера. Сетевое устройство ximc должно быть в локальной сети, к которой подключён этот адаптер.
		* При использование ключа adapter_addr <b>обязательно</b> установить ключ addr. Пример: "addr= \n adapter_addr=192.168.0.100".
		* \endrussian
	 */
	device_enumeration_t XIMC_API enumerate_devices(int enumerate_flags, const char *hints);

	/**
		* \english
		* Free memory returned by \a enumerate_devices.
		* @param[in] device_enumeration opaque pointer to an enumeration device data
		* \endenglish
		* \russian
		* Освобождает память, выделенную \a enumerate_devices.
		* @param[in] device_enumeration закрытый указатель на данные о перечисленных устойствах
		* \endrussian
	 */
	result_t XIMC_API free_enumerate_devices(device_enumeration_t device_enumeration);

	/**
		* \english
		* Get device count.
		* @param[in] device_enumeration opaque pointer to an enumeration device data
		* \endenglish
		* \russian
		* Возвращает количество подключенных устройств.
		* @param[in] device_enumeration закрытый указатель на данные о перечисленных устойствах
		* \endrussian
	 */
	int XIMC_API get_device_count(device_enumeration_t device_enumeration);

	/**
		* \english
		* Nevermind
		* \endenglish
		* \russian
		* Не обращайте на меня внимание
		* \endrussian
	*/
	typedef char* pchar;

	/**
		* \english
		* Get device name from the device enumeration.
		* Returns \a device_index device name.
		* @param[in] device_enumeration opaque pointer to an enumeration device data
		* @param[in] device_index device index
		* \endenglish
		* \russian
		* Возвращает имя подключенного устройства из перечисления устройств.
		* Возвращает имя устройства с номером \a device_index.
		* @param[in] device_enumeration закрытый указатель на данные о перечисленных устойствах
		* @param[in] device_index номер устройства
		* \endrussian
	 */
	pchar XIMC_API get_device_name(device_enumeration_t device_enumeration, int device_index);


	/**
		* \english
		* Get device serial number from the device enumeration.
		* Returns \a device_index device serial number.
		* @param[in] device_enumeration opaque pointer to an enumeration device data
		* @param[in] device_index device index
		* @param[out] serial device serial number
		* \endenglish
		* \russian
		* Возвращает серийный номер подключенного устройства из перечисления устройств.
		* Возвращает серийный номер устройства с номером \a device_index.
		* @param[in] device_enumeration закрытый указатель на данные о перечисленных устойствах
		* @param[in] device_index номер устройства
		* @param[in] serial серийный номер устройства
		* \endrussian
	 */
	result_t XIMC_API get_enumerate_device_serial(device_enumeration_t device_enumeration, int device_index, uint32_t* serial);

	/**
		* \english
		* Get device information from the device enumeration.
		* Returns \a device_index device information.
		* @param[in] device_enumeration opaque pointer to an enumeration device data
		* @param[in] device_index device index
		* @param[out] device_information device information data
		* \endenglish
		* \russian
		* Возвращает информацию о подключенном устройстве из перечисления устройств.
		* Возвращает информацию о устройстве с номером \a device_index.
		* @param[in] device_enumeration закрытый указатель на данные о перечисленных устойствах
		* @param[in] device_index номер устройства
		* @param[out] device_information информация об устройстве
		* \endrussian
	 */
	result_t XIMC_API get_enumerate_device_information(device_enumeration_t device_enumeration, int device_index, device_information_t* device_information);

	/**
		* \english
		* Get controller name from the device enumeration.
		* Returns \a device_index device controller name.
		* @param[in] device_enumeration opaque pointer to an enumeration device data
		* @param[in] device_index device index
		* @param[out] controller_name controller name
		* \endenglish
		* \russian
		* Возвращает имя подключенного устройства из перечисления устройств.
		* Возвращает имя устройства с номером \a device_index.
		* @param[in] device_enumeration закрытый указатель на данные о перечисленных устойствах
		* @param[in] device_index номер устройства
		* @param[out] controller name имя устройства
		* \endrussian
	 */
	result_t XIMC_API get_enumerate_device_controller_name(device_enumeration_t device_enumeration, int device_index, controller_name_t* controller_name);

	/**
		* \english
		* Get stage name from the device enumeration.
		* Returns \a device_index device stage name.
		* @param[in] device_enumeration opaque pointer to an enumeration device data
		* @param[in] device_index device index
		* @param[out] stage_name stage name
		* \endenglish
		* \russian
		* Возвращает имя подвижки для подключенного устройства из перечисления устройств.
		* Возвращает имя подвижки устройства с номером \a device_index.
		* @param[in] device_enumeration закрытый указатель на данные о перечисленных устойствах
		* @param[in] device_index номер устройства
		* @param[out] stage name имя подвижки
		* \endrussian
	 */
	result_t XIMC_API get_enumerate_device_stage_name(device_enumeration_t device_enumeration, int device_index, stage_name_t* stage_name);

	/**
		* \english
		* Get device network information from the device enumeration.
		* Returns \a device_index device network information.
		* @param[in] device_enumeration opaque pointer to an enumeration device data
		* @param[in] device_index device index
		* @param[out] device_network_information device network information data
		* \endenglish
		* \russian
		* Возвращает сетевую информацию о подключенном устройстве из перечисления устройств.
		* Возвращает сетевую информацию о устройстве с номером \a device_index.
		* @param[in] device_enumeration закрытый указатель на данные о перечисленных устойствах
		* @param[in] device_index номер устройства
		* @param[out] device_network_information сетевая информация об устройстве
		* \endrussian
	 */
	result_t XIMC_API get_enumerate_device_network_information(device_enumeration_t device_enumeration, int device_index, device_network_information_t* device_network_information);

	/** \english
		* Resets the error of incorrect data transmission. This function returns only 0 (OK). 
		* For example, sending the libximc command ends with an incorrect data transfer (error), any subsequent command always returns -1 (relevant for Windows).
		* \endenglish
		* \russian
		* Сбрасывает ошибку неправильной передачи данных. Эта функция возвращает только 0 (OK). 
		* Например, отправка команды libximc заканчивается неправильной передачей данных (ошибкой), любая последующая команда всегда возвращает -1 (актуально для Windows).
		* \endrussian
	*/
	result_t XIMC_API reset_locks ();

	/** \english
		* Fixing a USB driver error in Windows.
		* The USB-COM subsystem in the Windows OS does not always work correctly. During operation, the following malfunctions are possible:
		* All attempts to open the device fail. The device can be opened and data can be sent to it, but the response data is not received.
		* These problems are fixed by reconnecting the device or reinitializing it in the Device Manager.
		* The ximc_fix_usbser_sys() function automates the deletion detection process.
		* \endenglish
		* \russian
		* Исправление ошибки драйвера USB в Windows.
		* Подсистема USB-COM на OC Windows не всегда работает корректно. При работе возможны следующие неисправности:
		* Все попытки открыть устройство заканчиваются неудачно. Устройство можно открыть и отправить в него данные, но ответные данные не приходят.
		* Эти проблемы исправляются переподключением устройства или его переинециализацией в диспетчере устройств.
		* Функция ximc_fix_usbser_sys() автоматизирует процесс удаления-обнаружения.
		* \endrussian
		*/
	result_t XIMC_API ximc_fix_usbser_sys(const char* device_uri);


	/** \english
		* Sleeps for a specified amount of time
		* @param msec time in milliseconds
		* \endenglish
		* \russian
		* Приостанавливает работу на указанное время
		* @param msec время в миллисекундах
		* \endrussian
		*/
	void XIMC_API msec_sleep (unsigned int msec);

	/** \english
		* Returns a library version
		* @param version a buffer to hold a version string, 32 bytes is enough
		* \endenglish
		* \russian
		* Возвращает версию библиотеки
		* @param version буфер для строки с версией, 32 байт достаточно
		* \endrussian
		*/
	void XIMC_API ximc_version (char* version);

#if !defined(MATLAB_IMPORT) && !defined(LABVIEW64_IMPORT) && !defined(LABVIEW32_IMPORT)

	/** \english
		* Logging callback prototype
		* @param loglevel a loglevel
		* @param message a message
		* \endenglish
		* \russian
		* Прототип функции обратного вызова для логирования
		* @param loglevel уровень логирования
		* @param message сообщение
		* \endrussian
		*/
	typedef void (XIMC_CALLCONV *logging_callback_t)(int loglevel, const wchar_t* message, void* user_data);

	/** \english
		* Simple callback for logging to stderr in wide chars
		* @param loglevel a loglevel
		* @param message a message
		* \endenglish
		* \russian
		* Простая функция логирования на stderr в широких символах
		* @param loglevel уровень логирования
		* @param message сообщение
		* \endrussian
		*/
	void XIMC_API logging_callback_stderr_wide(int loglevel, const wchar_t* message, void* user_data);

	/** \english
		* Simple callback for logging to stderr in narrow (single byte) chars
		* @param loglevel a loglevel
		* @param message a message
		* \endenglish
		* \russian
		* Простая функция логирования на stderr в узких (однобайтных) символах
		* @param loglevel уровень логирования
		* @param message сообщение
		* \endrussian
		*/
	void XIMC_API logging_callback_stderr_narrow(int loglevel, const wchar_t* message, void* user_data);

	/**
		* \english
		* Sets a logging callback.
		* Call resets a callback to default (stderr, syslog) if NULL passed.
		* @param logging_callback a callback for log messages
		* \endenglish
		* \russian
		* Устанавливает функцию обратного вызова для логирования.
		* Вызов назначает стандартный логгер (stderr, syslog), если передан NULL
		* @param logging_callback указатель на функцию обратного вызова
		* \endrussian
		*/
	void XIMC_API set_logging_callback(logging_callback_t logging_callback, void* user_data);

#endif

/**
	* \english
	* Return device state.
	* @param id an identifier of device
	* @param[out] status structure with snapshot of controller status
	* \endenglish
	* \russian
	* Возвращает информацию о текущем состоянии устройства.
	* @param id идентификатор устройства
	* @param[out] status структура с информацией о текущем состоянии устройства
	* \endrussian
	*/
/**
	* \english
	* Device state.
	* Useful structure that contains current controller status, including speed, position and boolean flags.
	* \endenglish
	* \russian
	* Состояние устройства.
	* Эта структура содержит основные параметры текущего состояния контроллера, такие как скорость, позиция и флаги состояния.
	* \endrussian
	* @see get_status
	*/
	result_t XIMC_API get_status (device_t id, status_t* status);

/**
	* \english
	* Return device state.
	* @param id an identifier of device
	* @param[out] status structure with snapshot of controller status
	* @param calibration user unit settings
	* \endenglish
	* \russian
	* Возвращает информацию о текущем состоянии устройства.
	* @param id идентификатор устройства
	* @param[out] status структура с информацией о текущем состоянии устройства
	* @param calibration настройки пользовательских единиц
	* \endrussian
	*/
/**
	* \english
	* Calibrated device state.
	* Useful structure that contains current controller status, including speed, position and boolean flags.
	* \endenglish
	* \russian
	* Состояние устройства в калиброванных единицах.
	* Эта структура содержит основные параметры текущего состояния контроллера, такие как скорость, позиция и флаги состояния, размерные величины выводятся в калиброванных единицах.
	* \endrussian
	* @see get_status
	*/
	result_t XIMC_API get_status_calb (device_t id, status_calb_t* status, const calibration_t* calibration);

/**
	* \english
	* Return device information.
	* All fields must point to allocated string buffers with at least 10 bytes.
	* Works with both raw or initialized device.
	* @param id an identifier of device
	* @param[out] device_information device information
	* \endenglish
	* \russian
	* Возвращает информацию об устройстве.
	* Все входные параметры должны быть указателями на выделенные области памяти длиной не менее 10 байт.
	* Команда доступна как из инициализированного состояния, так и из исходного.
	* @param id идентификатор устройства.
	* @param[out] device_information информация об устройстве
	* \endrussian
	*/
/**
	* \english
	* Device information.
	* \endenglish
	* \russian
	* Информация об устройстве.
	* \endrussian
	* @see get_device_information
	*/
	result_t XIMC_API get_device_information (device_t id, device_information_t* device_information);

/**
	* \english
	* Wait for stop
	* @param id an identifier of device
	* @param refresh_interval_ms Status refresh interval. The function waits this number of milliseconds between get_status requests to the controller.
	* Recommended value of this parameter is 10 ms. Use values of less than 3 ms only when necessary - small refresh interval values do not significantly
	* increase response time of the function, but they create substantially more traffic in controller-computer data channel.
	* @param[out] ret RESULT_OK if controller has stopped and result of the first get_status command which returned anything other than RESULT_OK otherwise.
	* \endenglish
	* \russian
	* Ожидание остановки контроллера
	* @param id идентификатор устройства
	* @param refresh_interval_ms Интервал обновления. Функция ждет столько миллисекунд между отправками контроллеру запроса get_status для проверки статуса остановки.
	* Рекомендуемое значение интервала обновления - 10 мс. Используйте значения меньше 3 мс только если это необходимо - малые значения интервала обновления
	* незначительно ускоряют обнаружение остановки, но создают существенно больший поток данных в канале связи контроллер-компьютер.
	* @param[out] ret RESULT_OK, если контроллер остановился, в противном случае первый результат выполнения команды get_status со статусом отличным от RESULT_OK.
	* \endrussian
	*/
	result_t XIMC_API command_wait_for_stop(device_t id, uint32_t refresh_interval_ms);
	
	/**
	* \english
	* Make home command, wait until it is finished and make zero command. This is a convinient way to calibrate zero position.
	* @param id an identifier of device
	* @param[out] ret RESULT_OK if controller has finished home & zero correctly or result of first controller query that returned anything other than RESULT_OK.
	* \endenglish
	* \russian
	* Запустить процедуру поиска домашней позиции, подождать её завершения и обнулить позицию в конце. Это удобный путь для калибровки нулевой позиции.
	* @param id идентификатор устройства
	* @param[out] ret RESULT_OK, если контроллер завершил выполнение home и zero корректно или результат первого запроса к контроллеру со статусом отличным от RESULT_OK.
	* \endrussian
	*/
	result_t XIMC_API command_homezero(device_t id);
	//@}

#if defined(__cplusplus)
};
#endif

#endif

// vim: ts=4 shiftwidth=4

