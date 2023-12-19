#include "common.h"
#include "ximc.h"
#include "util.h"
#include "loader.h"
#include "ximc-gen.h"
#include "metadata.h"
#include "platform.h"
#include "protosup.h"

#include "sglib.h"
#include <locale.h>

#ifdef _MSC_VER
#pragma warning( disable : 4311 ) // because we may cast 64-bit handle ptrs to uint32_t to use as pseudo-ids
#endif

/*
 * Forward declarations
 */

int command_port_send (device_metadata_t *metadata, const byte* command, size_t len);
int command_port_receive (device_metadata_t *metadata, byte* response, size_t len);
void remov_table(float** X, float** dX);
void creat_table(float** X, float** dX);

result_t open_port_virtual (device_metadata_t *metadata, const char* virtual_path, const char* serial);
result_t close_port_virtual (device_metadata_t *metadata);
ssize_t read_port_virtual (device_metadata_t *metadata, void *buf, size_t amount);
ssize_t write_port_virtual (device_metadata_t *metadata, const void *buf, size_t amount);


/*
 * Metadata implementation
 */

typedef struct device_metadata_node_t
{
	device_t id;
	device_metadata_t data;
	struct device_metadata_node_t *next_ptr;
} device_metadata_node_t;

#define DEVICE_METADATA_COMPARATOR(e1, e2) (e1->id == e2->id ? 0 : 1)

// Global variable that holds an opened devices list
// Could be different for different processes because we are a shared library
device_metadata_node_t* g_devices_metadata = NULL;

device_metadata_t* get_metadata(device_t device)
{
	device_metadata_t *result = NULL;
	device_metadata_node_t marker, *out = NULL;
	lock_metadata();
	marker.id = device;
	SGLIB_LIST_FIND_MEMBER(device_metadata_node_t, g_devices_metadata, &marker, DEVICE_METADATA_COMPARATOR, next_ptr, out);
	if (out)
		result = &(out->data);
	unlock_metadata();
	return result;
}

void remove_metadata(device_t device)
{
	device_metadata_node_t marker, *out = NULL;
	lock_metadata();
	marker.id = device;
	SGLIB_LIST_DELETE_IF_MEMBER(device_metadata_node_t, g_devices_metadata, &marker, DEVICE_METADATA_COMPARATOR, next_ptr, out);
	if (out)
		free( out );
	unlock_metadata();
}

device_t allocate_metadata(device_metadata_t **metadata)
{
	device_t device = 0;
	device_metadata_node_t *new_dm;
	lock_metadata();
	/* Determine next device id */
	SGLIB_LIST_MAP_ON_ELEMENTS(device_metadata_node_t, g_devices_metadata, out, next_ptr,{
			if (out->id > device)
				device = out->id;
	});
	device = device + 1;
 
	new_dm = (device_metadata_node_t*)malloc( sizeof(device_metadata_node_t) );
	new_dm->id = device;
	*metadata = &(new_dm->data);
	SGLIB_LIST_ADD(device_metadata_node_t, g_devices_metadata, new_dm, next_ptr);
	unlock_metadata();
	return device;
}


/*
 * Low-level I/O multiplexers
 */

result_t device_flush(device_metadata_t *metadata)
{
	filelog_text("-", metadata->type, (uint32_t)metadata->handle, "Flushing port...");
	switch (metadata->type)
	{
		case dtSerial:
			return flush_port_serial( metadata ) == result_serial_ok
				? result_ok : result_error;
		default:
			return result_ok;
	}
}

int command_port_send (device_metadata_t *metadata, const byte* command, size_t command_len)
{
	ssize_t n;
	unsigned int errcode;
	size_t k, amount;
	int failed;

	for (k = 0; k < command_len; )
	{
		failed = 0;
		amount = command_len - k;
		if (command_len < k)
			return result_serial_error;
		else if (amount == 0)
			break;
		#ifdef DEBUG_TRACE
		log_debug( L"writing %d ... ", (int)amount );
		dump_bytes( command+k, amount );
		#endif
		filelog_data("W", metadata->type, (uint32_t)metadata->handle, (char*)command + k, amount);

	    if (metadata->type == dtVirtual)
		{
			// Call writer function (that analyzes a buffer with request)
			n = write_port_virtual( metadata, command+k, amount );
			failed = n < 0;
		}
		else if (metadata->type == dtSerial)
		{
			n = write_port_serial( metadata, command+k, amount );
			failed = n < 0;
		}
		else if (metadata->type == dtUdp)
		{
			n = write_udp(metadata, command + k, amount);
			failed = n < 0;
		}
		else if (metadata->type == dtTcp)
		{
			n = write_tcp(metadata, command + k, amount);
			failed = n < 0;
		}
		if (failed)
		{
			errcode = get_system_error_code();
			log_system_error( L"write to port failed, write %d bytes instead of %d bytes, reason: ", n, amount );
			if (is_error_nodevice(errcode))
				return result_serial_nodevice;
			if (device_flush( metadata ) != result_ok)
			{
				if (is_error_nodevice(get_system_error_code()))
					return result_serial_nodevice;
				return result_serial_error;
			}
			return result_serial_error;
		}
		if (n == 0 && k < command_len)
		{
			#ifdef DEBUG_TRACE
			log_debug( L"no more bytes (%d left)... ", (int)(command_len-k) );
			#endif
			if (device_flush( metadata ) != result_ok)
			{
				if (is_error_nodevice(get_system_error_code()))
					return result_serial_nodevice;
			}
			return result_serial_timeout;
		}

		k += n;
	}

	return result_serial_ok;
}

int command_port_receive (device_metadata_t *metadata, byte* response, size_t response_len)
{
	ssize_t n;
	unsigned int errcode;
	size_t k, amount;
	int failed;

	for (k = 0; k < response_len; )
	{
		failed = 0;
		amount = response_len - k;
		if (response_len < k)
			return result_serial_error;
		else if (amount == 0)
			break;
		
		if (metadata->type == dtVirtual)
		{
			// Call reader function (that analyzes a buffer with response)
			n = read_port_virtual( metadata, response+k, amount );
			failed = n < 0;
		}
		else if (metadata->type == dtSerial)
		{
			n = read_port_serial( metadata, response+k, amount );
			failed = n < 0;
		}
		else if (metadata->type == dtUdp)
		{
			n = read_udp(metadata, response + k, amount);
			failed = n < 0;
		}
		else if (metadata->type == dtTcp)
		{
			n = read_tcp(metadata, response + k, amount);
			failed = n < 0;
		}
		else
		{
			log_error( L"unknown device type %d", metadata->type );
			return result_serial_error;
		}

		if (failed)
		{
			errcode = get_system_error_code();
			log_system_error( L"read from port failed, read %d bytes instead of %d, reason: ", n, amount );
			if (is_error_nodevice(errcode))
				return result_serial_nodevice;
			if (device_flush( metadata ) != result_ok)
			{
				if (is_error_nodevice(get_system_error_code()))
					return result_serial_nodevice;
				return result_serial_error;
			}
			return result_serial_error;
		}

		#ifdef DEBUG_TRACE
		log_debug( L"reading %d/%d ... ", (int)n, (int)amount );
		dump_bytes( response+k, ximc_max( 0, n ) );
		#endif
		filelog_data("R", metadata->type, (uint32_t)metadata->handle, (char*)response + k, ximc_max(0, n));

		if (n == 0 && k < response_len)
		{
			#ifdef DEBUG_TRACE
			log_debug( L"no more bytes (%d left)... ", (int)(response_len-k) );
			#endif
			if (device_flush( metadata ) != result_ok)
			{
				if (is_error_nodevice(get_system_error_code()))
					return result_serial_nodevice;
				return result_serial_timeout;
			}
			return result_serial_timeout;
		}

		k += n;
	}
	#ifdef DEBUG_TRACE
	log_debug( L"total read... " );
	dump_bytes( response, response_len );
	#endif

	return result_serial_ok;
}

/* 
 * Protocol I/O implementation details
 */

// Returns 0 if synchronization succeeds
int send_synchronization_zeroes(device_metadata_t *metadata)
{
	byte zeroes[SYNC_ZERO_COUNT];
	int res;
	int received = SYNC_ZERO_COUNT;

	log_info(L"synchronize: sending sync zeroes");

	memset(zeroes, 0, SYNC_ZERO_COUNT);
	if (metadata->type == dtNet)
	{
#ifdef HAVE_XIBRIDGE
		res = (int)xibridge_device_request_response(&(metadata->xi_conn), (uint8_t *)zeroes, SYNC_ZERO_COUNT, (uint8_t *)zeroes, SYNC_ZERO_COUNT);
		log_info(res == 0 ? L"synchronize: got zeros, done" :L"synchronize: command_port_send sync failed");
	    return res == 0 ? 0 : 1;

#else
		log_error(L"network device support is not built");
        return result_serial_nodevice;
#endif
	}

	res = command_port_send( metadata, zeroes, SYNC_ZERO_COUNT );
	if (res < 0)
	{
		log_error( L"synchronize: command_port_send sync failed" );
		return result_nodevice;
	}

	for (; received > 0; --received)
	{
		res = command_port_receive( metadata, zeroes, 1 );
		if (res < 0)
		{
			log_error( L"synchronize: command_port_receive can't get bytes" );
			return 1;
		}
		if (zeroes[0] == 0)
		{
			log_info( L"synchronize: got a zero, done" );
			return 0;
		}
	}

	return 1;
}

result_t synchronize (device_metadata_t *metadata)
{
	int retry_counter = SYNC_RETRY_COUNT;

	log_info( L"synchronize: started" );

	for (; retry_counter > 0; --retry_counter)
	{
		if (send_synchronization_zeroes( metadata ) == 0)
		{
			log_info( L"synchronize: completed" );
			return result_error;
		}
	}
	log_error( L"synchronize: synchronization attempts failed, device is lost" );
	return result_nodevice;
}

int wallclock_diff(time_t sec_beg, int msec_beg, time_t sec_end, int msec_end)
{
	int delta = 0;
	if (sec_end > sec_beg) /* be cautious */
		delta = (int)(sec_end - sec_beg);
	delta *= 1000;
	delta += msec_end - msec_beg;
	if (delta < 0)
		delta = 0;
	return delta;
}

result_t receive_synchronized (device_metadata_t *metadata, byte* response, size_t len, int need_sync)
{
	result_t result;
	int serial_result;
	int logical_timeout;
	int delta_time = 0;

	time_t sec_beg, sec_cur, sec_prev;
	int msec_beg, msec_cur, msec_prev;

	logical_timeout = metadata->timeout;
	if (logical_timeout <= 0)
		log_error( L"receive_synchronized: logical timeout is not properly saved at device open: %d", logical_timeout );

	get_wallclock( &sec_beg, &msec_beg );
	sec_prev = sec_beg;
	msec_prev = msec_beg;
	do
	{
		serial_result = command_port_receive( metadata, response, len );
		get_wallclock( &sec_cur, &msec_cur );

		switch (serial_result)
		{
			case result_serial_ok:
				return result_ok;

			case result_serial_timeout:
				log_info( L"receive_synchronized: receive timed out, requesting data from buffer one more time" );
				if (wallclock_diff( sec_prev, msec_prev, sec_cur, msec_cur ) < WAIT_BEFORE_RETRY_TIME)
				{
					log_info( L"receive_synchronized: timed out too fast, wait a little" );
					msec_sleep( WAIT_BEFORE_RETRY_TIME );
				}
				break;

			case result_serial_error:
				log_error( L"receive_synchronized: failed" );
				/* new behaviour, do not sync */
				return result_nodevice;

			case result_serial_nodevice:
				log_error( L"receive_synchronized: device lost" );
				return result_nodevice;
		}
		delta_time = wallclock_diff( sec_beg, msec_beg, sec_cur, msec_cur );
		sec_prev = sec_beg;
		msec_prev = msec_beg;
		log_info( L"receive_synchronized: passed %d msec, needed at least %d msec", delta_time, logical_timeout );
	}
	while (delta_time < logical_timeout);

	// All retries
	log_error( L"receive_synchronized: receive finally timed out" );
	if (need_sync)
	{
		if ((result = synchronize( metadata )) != result_ok)
		{
			log_warning( L"receive_synchronized: synchronize failed, nevermind" );
		}
	}
	else
		result = result_error;
	return result;
}


result_t command_checked_impl (device_t id, const void* command, size_t command_len, byte* response, size_t response_len, int need_sync)
{
	result_t result;
	uint32_t res;
	byte errv[4] = { 'e', 'r', 'r', 'v' };
	byte errd[4] = { 'e', 'r', 'r', 'd' };
	device_metadata_t* dm;

	if (command_len < 4)
		return result_error;

	dm = get_metadata( id );
	if (!dm)
	{
		log_error( L"command_checked_impl cannot get metadata" );
		return result_error;
	}
	if (dm->type == dtUnknown)
	{
		log_error( L"command_checked_impl got metadata with fake device" );
		return result_error;
	}

	if (response_len && !response)
	{
		log_error( L"command_checked can't read to empty buffer" );
	}

	if (dm->type == dtNet)
#ifdef HAVE_XIBRIDGE
	{
		filelog_data("W", dm->type, (uint32_t)dm->handle, (char*)command, command_len);
		res = (int)xibridge_device_request_response(&(dm->xi_conn), (uint8_t *)command, (uint32_t)command_len, (uint8_t *)response, (uint32_t)response_len);
		filelog_data("R", dm->type, (uint32_t)dm->handle, (char*)response, response_len);
		if (res)
		{
			// error type of xibridge does not matter
            log_error(L"command_checked device lost: %hs", xibridge_get_err_expl(res));
			return result_nodevice;
		}

#else
	{
		log_error(L"network device support is not built");
	    return result_serial_nodevice;
#endif
    }
	else
	{
		// send command
		res = command_port_send(dm, command, command_len);
		switch (res)
		{
		case result_ok:
			break;
		case result_serial_nodevice:
			log_error(L"command_checked device lost");
			return result_nodevice;
		case result_serial_timeout:
		case result_serial_error:
			log_error(L"command_checked failed");
			return result_nodevice;
		}
	}
	if (response)
	{
		// read first byte until it's non-zero
		if (dm->type != dtNet)
		{
			do
			{
				if ((result = receive_synchronized(dm, response, 1, need_sync)) != result_ok)
					return result;
			} while (response[0] == 0);

			// read three bytes
			if ((result = receive_synchronized(dm, response + 1, 3, need_sync)) != result_ok)
				return result;
		}
		// check is it an errv answer
		if (memcmp( errv, response, (size_t)4 ) == 0)
		{
			log_warning( L"Response 'errv' received" );
			device_flush( dm );
			return result_value_error;
		}

		// check is it an errd answer
		if (memcmp( errd, response, (size_t)4 ) == 0)
		{
			log_warning( L"Response 'errd' received" );
			// flood the controller with zeroes
			synchronize( dm );
			device_flush( dm );
			return result_error;
		}

		// check command bytes
		if (memcmp( command, response, (size_t)4 ) != 0)
		{
			// flood the controller with zeroes
			synchronize( dm );
			device_flush( dm );
			return result_error;
		}

		// receive remaining bytes
		
		if (dm->type != dtNet && (result = receive_synchronized( dm, response+4, response_len-4, need_sync )) != result_ok)
			return result;
	}

	return result_ok;
}

/*
 * High-level I/O library accessors
 */

result_t command_checked (device_t id, const void* command, size_t command_len, byte* response, size_t response_len)
{
	return command_checked_impl( id, command, command_len, response, response_len, 1 );
}

result_t command_checked_unsynced (device_t id, const void* command, size_t command_len, byte* response, size_t response_len)
{
	return command_checked_impl( id, command, command_len, response, response_len, 0 );
}

/* Send command as a 4-byte string and return answer. Echo is checked */
result_t command_checked_str (device_t id, const char* command, byte* response, size_t response_len)
{
	return command_checked( id, command, 4, response, response_len );
}

/* same as command_checked_str but without sync */
result_t command_checked_str_unsynced (device_t id, const char* command, byte* response, size_t response_len)
{
	return command_checked_impl( id, command, 4, response, response_len, 0 );
}

/* Send command and expect exact echo command answer */
result_t command_checked_echo (device_t id, const void* command, size_t command_len)
{
	byte response[4];
	return command_checked( id, command, command_len, response, sizeof(response) );
}

/* same as command_checked_echo but without sync */
result_t command_checked_echo_unsynced (device_t id, const void* command, size_t command_len)
{
	byte response[4];
	return command_checked_impl( id, command, command_len, response, sizeof(response), 0 );
}

/* Send command as a 4-byte string and expect exact echo command answer */
result_t command_checked_echo_str (device_t id, const char* command)
{
	return command_checked_echo( id, command, 4 );
}

result_t command_checked_echo_str_unsynced (device_t id, const char* command)
{
	return command_checked_echo_unsynced( id, command, 4 );
}

result_t command_checked_echo_str_locked (device_t id, const char* command)
{
	result_t result;
	lock( id );
	result = command_checked_echo_str( id, command );
	unlock( id );
	return result;
}


/*
 * Bounds checkers
 */

result_t check_in_overrun_raw(size_t data_count, size_t buf_size)
{
	result_t result = result_ok;;
	if (data_count != buf_size)
	{
		log_error( L"buffer incoming overrun %d vs buf size %d", data_count, buf_size );
		result = result_error;
	}
	return result;
}

// layout is following:
// before PROTO14:	data(size bytes) + crc(2 bytes) + cmd(4bytes)
// PROTO14:			cmd(4bytes) + data(size bytes-4) + crc(2 bytes)
// cmd is checked at request sent
result_t check_in_overrun(device_t id, size_t data_count, size_t buf_size, const byte* response)
{
	uint16_t crc, crc_actual;
	result_t result;
	device_metadata_t* dm;

	// please note: -4 is because of p+=4 shift, very hackish client code
	if ((result = check_in_overrun_raw( data_count+6-4, buf_size )) != result_ok)
		return result;
	crc = get_crc( response+4, data_count-4 );
	memcpy( &crc_actual, response+data_count, 2 );
	if (crc != crc_actual)
	{
		log_error( L"buffer crc check failed, real %x, in buffer %x", crc, crc_actual );
		// flood the controller with zeroes
		dm = get_metadata( id );
		if (!dm)
			return result_error;
		synchronize( dm );
		device_flush( dm );
		return result_error;
	}
	return result_ok;
}

result_t check_in_overrun_without_crc(device_t id, size_t data_count, size_t buf_size, const byte* response)
{
	XIMC_UNUSED(id);
	XIMC_UNUSED(response);
	return check_in_overrun_raw( data_count+6-4, buf_size );
}

result_t check_out_overrun (size_t data_count, size_t buf_size)
{
	if (data_count != buf_size)
	{
		log_error( L"buffer outgoing overrun %d vs buf size %d", data_count, buf_size );
		return result_error;
	}
	return result_ok;
}

result_t check_out_atleast_overrun (size_t data_count, size_t buf_size)
{
	if (data_count > buf_size)
	{
		log_error( L"buffer outgoing overrun %d vs buf size %d", data_count, buf_size );
		return result_error;
	}
	return result_ok;
}

/*
 * Data accessors
 */

void push_data(byte** where, const void* data, size_t size)
{
	memcpy( *where, data, size );
	*where += size;
}

void push_garbage(byte** where, size_t size)
{
	memset( *where, 0xCC, size );
	*where += size;
}

// exclude four lead bytes
void push_crc (byte** where, const void* data, size_t size)
{
	uint16_t crc;
	crc = get_crc( (byte*)data + 4, size - 4 );
	memcpy( *where, &crc, 2 );
	*where += 2;
}

// include lead bytes
void push_crc_with_command (byte** where, const void* data, size_t size)
{
	uint16_t crc;
	crc = get_crc( (byte*)data, size );
	memcpy( *where, &crc, 2 );
	*where += 2;
}

void push_str (byte** where, const char* str)
{
	push_data( where, str, strlen( str ) );
}

void push_float (byte** where, float value)
{
	push_data( where, &value, sizeof(value) );
}

void push_double (byte** where, double value)
{
	push_data( where, &value, sizeof(value) );
}

void pop_data(byte** where, void* data, size_t size)
{
	memcpy( data, *where, size );
	*where += size;
}

void pop_str(byte** where, void* data, size_t size)
{
	memcpy( data, *where, size );
	((char*)data)[size] = '\0';
	*where += size;
}

void pop_garbage(byte** where, size_t size)
{
	*where += size;
}

float pop_float(byte** where)
{
	float result;
	memcpy( &result, *where, sizeof(result) );
	*where += sizeof(result);
	return result;
}

double pop_double(byte** where)
{
	double result;
	memcpy( &result, *where, sizeof(result) );
	*where += sizeof(result);
	return result;
}

#define GENERATE_PUSH(Type) \
void push_ ## Type (byte** where, Type ## _t value) \
{ \
	push_data( where, &value, sizeof(value) ); \
}

#define GENERATE_UPOP(Type) \
unsigned int pop_## Type (byte** where)\
{\
	Type ## _t result;\
	memcpy( &result, *where, sizeof(result) );\
	*where += sizeof(result);\
	return (unsigned int)result;\
}

#define GENERATE_IPOP(Type) \
int pop_## Type (byte** where)\
{\
	Type ## _t result;\
	memcpy( &result, *where, sizeof(result) );\
	*where += sizeof(result);\
	return (int)result;\
}

/* manual pop 64-bit types definitions because default int return type is not enough */
#define GENERATE_EXACTPOP(Type) \
Type ## _t pop_## Type (byte** where)\
{\
	Type ## _t result;\
	memcpy( &result, *where, sizeof(result) );\
	*where += sizeof(result);\
	return result;\
}

GENERATE_PUSH(uint64)
GENERATE_PUSH(uint32)
GENERATE_PUSH(uint16)
GENERATE_PUSH(uint8)
GENERATE_PUSH(int64)
GENERATE_PUSH(int32)
GENERATE_PUSH(int16)
GENERATE_PUSH(int8)

GENERATE_UPOP(uint32)
GENERATE_UPOP(uint16)
GENERATE_UPOP(uint8)
GENERATE_IPOP(int32)
GENERATE_IPOP(int16)
GENERATE_IPOP(int8)

GENERATE_EXACTPOP(uint64)
GENERATE_EXACTPOP(int64)

/* 
 * File log
 */

void filelog_text(const char* direction, device_type_t type,
		uint32_t serial, const char* line)
{
	filelog_data(direction, type, serial, line, strlen(line));
}

void filelog_data(const char* direction, device_type_t type,
		uint32_t serial, const char* ptr, size_t length)
{
	static FILE * fp = NULL;
	char* filename = getenv("XILOG");
	uint64_t us;
	unsigned int i;
	char* type_str;

	if (filename == NULL) { // If the variable is not set then don't log
		return;
	}
	if (fp == NULL) { // If this is the first call, then open file and add a header
		fp = fopen(filename, "a");
		if (fp)
		{
			fprintf(fp, "TIME\tDIR\tTYPE\tID\tCOMMAND\n");
		}
	}
	if (fp == NULL) { // If we failed to open file then we can't log
		return;
	}

	get_wallclock_us(&us);

	switch (type)
	{
	case dtSerial:
		type_str = "com";
		break;
	case dtVirtual:
		type_str = "emu";
		break;
	case dtNet:
		type_str = "net";
		break;
	case dtUdp:
		type_str = "udp";
		break;
	default:
		type_str = "---";
		break;
	}
	fprintf(fp, "%llu\t%s\t%s\t%u\t", (unsigned long long)us, direction, type_str, serial);
	for (i=0; i<length; i++) {
		if (*(ptr+i) > 32)
			fprintf(fp, "%c", *(ptr+i));
		else
			fprintf(fp, "%c", '.');
	}
	fprintf(fp, "\n");
}




#ifdef HAVE_LOCKS

/*
 * Global mutex support
 */

/* truly global mutex */
static mutex_t* g_mutex_global = NULL;

mutex_t* mutex_global()
{
	if (!g_mutex_global)
		g_mutex_global = mutex_init( UINT_MAX );
	return g_mutex_global;
}

/* metadata mutex
 * Metadata list is protected with one mutex.
 * It's better to migrate to read/write lock later*/
static mutex_t* g_mutex_global_metadata = NULL;

/*
 * Fine-grained locks
 */
mutex_t* mutex_global_metadata()
{
	if (!g_mutex_global_metadata)
		g_mutex_global_metadata = mutex_init( UINT_MAX-1 );
	return g_mutex_global_metadata;
}

/* Fine-grained lock */
mutex_t* mutex_by_device_id(device_t id)
{
	device_metadata_t* dm;
	if (id != device_undefined)
	{
		dm = get_metadata( id );
		if (dm && dm->device_mutex)
			return dm->device_mutex;
	}
	return NULL;
}


void lock(device_t id)
{
	mutex_t* m = mutex_by_device_id(id);
	if (m)
		mutex_lock( m );
}

void unlock(device_t id)
{
	mutex_t* m = mutex_by_device_id(id);
	if (m)
		mutex_unlock( m );
}

result_t unlocker (device_t id, result_t res)
{
	mutex_t* m = mutex_by_device_id(id);
	if (m)
		mutex_unlock( m );
	return res;
}

void lock_global()
{
	mutex_lock( mutex_global() );
}

void unlock_global ()
{
	mutex_unlock( mutex_global() );
}

result_t unlocker_global (result_t res)
{
	mutex_unlock( mutex_global() );
	return res;
}

void lock_metadata()
{
	mutex_lock( mutex_global_metadata() );
}

void unlock_metadata ()
{
	mutex_unlock( mutex_global_metadata() );
}

#else

void lock(device_t id)
{
	XIMC_UNUSED(id);
}

void unlock(device_t id)
{
	XIMC_UNUSED(id);
}

result_t unlocker (device_t id, result_t res)
{
	XIMC_UNUSED(id);
	return res;
}

void lock_global()
{
}

void unlock_global ()
{
}

result_t unlocker_global (result_t res)
{
	return res;
}

void lock_metadata()
{
}

void unlock_metadata ()
{
}

#endif

/*
 * Open xibridge port
 */
#ifdef HAVE_XIBRIDGE
result_t open_port_net_xibridge(device_metadata_t *metadata, const char* xi_uri)
{
    uint32_t err = xibridge_open_device_connection(xi_uri, &(metadata->xi_conn));
	if (err)
	{
		log_system_error(L"can't open net device %hs due to network error: %hs", xi_uri, xibridge_get_err_expl(err));
		return result_error;
	}

	/* save metadata */
	metadata->handle = (handle_t)metadata -> xi_conn.conn_id; // serves as unique id for unified file logging interface
	metadata->type = dtNet;
	return result_ok;
}
#endif

/* Open a port by URI
 * examples:
 *   xi-com:///COM3
 *   xi-com:///\\.\COM12
 *   xi-com:COM3
 *   xi-com:\\.\COM12
 *   xi-com:///dev/tty/ttyACM34
 *   xi-emu:///var/lib/ximc/virtual56.dat
 *   xi-emu:///c:/temp/virtual56.dat
 *   xi-emu:///c:/temp/virtual56.dat?serial=123
 *   xi-net://127.0.0.1/7890ABCD
 *   xi-net://remote.ximc.ru/7890ABCD
 */
result_t open_port (device_metadata_t *metadata, const char* name)
{
#ifdef HAVE_XIBRIDGE
	char uri_scheme[1024], uri_host[1024], uri_path[1024], decoded_path[1024],
		 uri_paramname[1024], uri_paramvalue[1024],
		 abs_path[1024], *tmp, *serial;
	filelog_text("-", dtUnknown, 0, "Opening port...");
	if (parse_uri(name, uri_scheme, sizeof(uri_scheme),
				uri_host, sizeof(uri_host), uri_path, sizeof(uri_path),
				uri_paramname, sizeof(uri_paramname),
				uri_paramvalue, sizeof(uri_paramvalue)))
	{
		log_error( L"unknown device URI %hs", name);
		return result_error;
	}
	tmp = uri_copy(uri_path);
	strncpy(decoded_path, tmp, sizeof(decoded_path));
	decoded_path[sizeof(decoded_path)-1] = 0;
	uri_path_to_absolute(tmp, abs_path, sizeof(abs_path));
	free(tmp);

	log_debug( L"Name %hs resolved to dt '%hs', host '%hs' and path '%hs' "
			L"param '%hs'='%hs' "
			L"decoded path '%hs', abs path '%hs'",
			name, uri_scheme, uri_host, uri_path,
			uri_paramname, uri_paramvalue,
			decoded_path, abs_path);
	if (!portable_strcasecmp(uri_scheme, "xi-com"))
	{
		if (strlen(uri_host) != 0 || strlen(abs_path) == 0)
		{
			log_error( L"Unknown device URI, only path should be specified" );
			return result_error;
		}
		return open_port_serial( metadata, abs_path );
	}
	else if (!portable_strcasecmp(uri_scheme, "xi-net"))
	{
		return open_port_net_xibridge( metadata, name );
	}
	else if (!portable_strcasecmp(uri_scheme, "xi-emu"))
	{
		if (strlen(uri_host) != 0 || strlen(abs_path) == 0)
		{
			log_error( L"Unknown device URI, only path should be specified" );
			return result_error;
		}
		serial = NULL;
		if (!strcmp(uri_paramname, "serial") && strlen(uri_paramvalue) > 0)
			serial = uri_paramvalue;
		return open_port_virtual( metadata, abs_path, serial );
	}

	else if (!portable_strcasecmp(uri_scheme, "xi-udp"))
	{
		
		return open_udp(metadata, uri_host);
	}
	else if (!portable_strcasecmp(uri_scheme, "xi-tcp"))
	{
	
		return open_tcp(metadata, uri_host);
	}

	else
	{
		log_error( L"unknown device type" );
		return result_error;
	}
#else
	XIMC_UNUSED(metadata);
	XIMC_UNUSED(name);
	log_error( L"network device support is not built" );
	return result_error;
#endif
}

result_t close_port (device_metadata_t *metadata)
{
#ifdef HAVE_XIBRIDGE
	filelog_text("-", metadata->type, (uint32_t)metadata->handle, "Closing port...");
	switch (metadata->type)
	{
		case dtSerial:
			return close_port_serial( metadata ) == result_serial_ok 
				? result_ok : result_error;
		case dtNet:
			xibridge_close_device_connection( &(metadata->xi_conn));
			return result_ok;
		case dtVirtual:
			return close_port_virtual( metadata );
		
		case dtUdp:
			return close_udp(metadata);

		case dtTcp:
			return close_tcp(metadata);

		default:
			return result_ok;
	}
#else
	XIMC_UNUSED(metadata);
	log_error( L"network device support is not built" );
	return result_error;
#endif
}



/*
 * Opening device
 */

device_t open_device_impl (const char* name, int timeout)
{
	device_t device;
	result_t result;
	device_metadata_t* dm;

	device = allocate_metadata(&dm);
	memset(dm, 0, sizeof(device_metadata_t));
	/* Port timeout must be set before device open */
	dm->port_timeout = PORT_TIMEOUT_TIME;
	/* Logical library timeout */
	dm->timeout = timeout;

#ifdef HAVE_LOCKS
	dm->device_mutex = mutex_init( (unsigned int)device );
	if (!dm->device_mutex)
	{
		remove_metadata(device);
		return device_undefined;
	}
#endif

	result = open_port( dm, name );
	if (result != result_ok)
	{
#ifdef HAVE_LOCKS
		mutex_close( dm->device_mutex );
#endif
		remove_metadata(device);
		return device_undefined;
	}

	return device;
}

result_t close_device_impl (device_t* id)
{
	result_t result;
	device_metadata_t* dm;
	if (*id == device_undefined)
	{
		log_error( L"attempting to close already closed device" );
		return result_error;
	}
	dm = get_metadata( *id );
	if (!dm)
	{
		log_error( L"could not extract metadata for device" );
		*id = device_undefined;
		return result_error;
	}
#ifdef HAVE_LOCKS
	if (dm->device_mutex)
		mutex_close( dm->device_mutex );
#endif

	result = close_port( dm ) == 0 ? result_ok : result_error;
	remove_metadata( *id );

	*id = device_undefined;
	return result;
}

/*The transformation of coordinates from the user to the controller.*/
result_t normal_correction(device_t* id, float* newPosition)
{	
	float curr_pos = 0;
	unsigned int ind;
	float cPosition;
	uint32_t indL, indR, indCur;
	device_metadata_t* dm;
	device_corr_table_t* correction;
	// FILE* fl1;

	cPosition = *newPosition;
	dm = get_metadata(*id);
	correction = &(dm->table);	
	
	if ((dm->table.X == NULL) || (dm->table.dX == NULL))
	{
		return 1;
	}	
	
	if ((correction->len_table > 1) && (correction->len_table < 100))
	{
		/*Sets the value to the left of the extreme position.*/
		if (cPosition <= *(correction->X+0))
		{
			curr_pos = cPosition + *(correction->dX+0);
			*newPosition = curr_pos;
			return 1;
		}

		/*Sets the value to the right of the extreme position.*/
		ind = (unsigned int) (correction->len_table - 1);
		if (cPosition >= *(correction->X+ind))
		{
			curr_pos = cPosition + *(correction->dX+ind);
			*newPosition = curr_pos;
			return 1;
		}

		// fl1 = fopen("report.txt", "w");
		/*Brute force search*/
		indL = 0;
		indR = correction->len_table - 1;
		do
		{
			indCur = indL + ((indR - indL)>>1);
			// fprintf(fl1, "\n %d %d %d", indL, indR, indCur);
			if (cPosition >= *(correction->X + indCur)) indL = indCur;
			else indR = indCur;			
			if (indR - indL <= 1)
			{
				// fprintf(fl1, "\n %d %d", indL, indR);
				curr_pos = cPosition + (*(correction->dX + indL + 1) - *(correction->dX + indL)) / 
					(*(correction->X + indL + 1) - *(correction->X + indL))*
					(cPosition - *(correction->X + indL + 1)) + *(correction->dX + indL + 1);
				*newPosition = curr_pos;
				// fprintf(fl1, "\n %f", curr_pos);
				return 1;
			}
		} while (true); 
		// fclose(fl1);
	}
	return 0;
}

/*The transformation of coordinates from the controller to the user.*/
result_t rewers_correction(device_t* id, float* newPosition)
{
	float curr_pos = 0, pos1, pos2;
	unsigned int ind;
	float cPosition;
	uint32_t indL, indR, indCur;
	device_metadata_t* dm;
	device_corr_table_t* correction;

	cPosition = *newPosition;
	dm = get_metadata(*id);
	correction = &(dm->table);

	if ((dm->table.X == NULL) || (dm->table.dX == NULL))
	{
		return 1;
	}
	
	if ((correction->len_table > 1) && (correction->len_table < 100))
	{
		if (cPosition <= (*(correction->X + 0) + *(correction->dX + 0)))
		{
			curr_pos = cPosition - *(correction->dX + 0);
			*newPosition = curr_pos;
			return 1;
		}
		ind = (unsigned int)(correction->len_table - 1);
		if (cPosition >= (*(correction->X + ind) + *(correction->dX + ind)))
		{
			curr_pos = cPosition - *(correction->dX + ind);
			*newPosition = curr_pos;
			return 1;
		}

		/*Brute force search*/
		indL = 0;
		indR = correction->len_table - 1;
		do
		{
			indCur = indL + ((indR - indL) >> 1);
			if (cPosition >= *(correction->X + indCur)) indL = indCur;
			else indR = indCur;

			if (indR - indL <= 1)
			{
				pos1 = *(correction->X + indL) + *(correction->dX + indL);
				pos2 = *(correction->X + indL + 1) + *(correction->dX + indL + 1);

				curr_pos = cPosition + (*(correction->dX + indL) - *(correction->dX + indL + 1)) /
					(pos2 - pos1)*(cPosition - pos2) - *(correction->dX + indL + 1);
				*newPosition = curr_pos;
				return 1;
			}
		} while (true);
	}
	return 0;
}

/* X Coordinate of the grid. */
/* dX Deviation. */
void remov_table(float** X, float** dX)
{
	free(*X);
	*X = NULL;
	free(*dX);
	*dX = NULL;
}

void creat_table(float** X, float** dX)
{	
	*X = (float *)malloc(100 * sizeof(float));
	//memset(X, 0, 100 * sizeof(float));
	*dX = (float *)malloc(100 * sizeof(float));
	//memset(dX, 0, 100 * sizeof(float));
}

/*
 * Exported core functions begins
 */

#if defined(__cplusplus)
extern "C" {
#endif

result_t XIMC_API load_correction_table(device_t* id, const char* namefile)
{
	setlocale(LC_NUMERIC, "C");
	
	device_metadata_t* dm;
	FILE * fp = NULL;

	if (*id == device_undefined)
	{
		log_error(L"attempting to close already closed device");
		return result_error;
	}
	dm = get_metadata(*id);
	if (!dm)
	{
		log_error(L"could not extract metadata for device");
		*id = device_undefined;
		return result_error;
	}

	if (namefile == NULL)
	{
		if (dm->table.X != NULL)
		{
			CLEAR_TABLE;
		}
		return result_ok;
	}
	if (dm->table.X != NULL)
	{
		CLEAR_TABLE;
	}

	fp = fopen(namefile, "r");
	if (fp == NULL)
	{
		log_error(L"error opening calibration table file");
		return result_error;
	}
	dm->table.X = (float *)malloc(100 * sizeof(float));
	dm->table.dX = (float *)malloc(100 * sizeof(float));

	char c1[100], c2[100];
	uint32_t i = 0;
	float f1, f2;
	int err;

	if (fscanf(fp, "%s%s", c1, c2) != 2)
	{
		CLEAR_TABLE_CLOSE_FILE;
		log_error(L"data error in calibration table file");
		return result_error;
	};

	while (true) 
	{
		err = fscanf(fp, "%f%f", &f1, &f2);
		if (err == EOF)
		{
			if (i >= 2)
			{
				dm->table.len_table = i;
				fclose(fp);
				return result_ok;
			}
			else
			{
				CLEAR_TABLE_CLOSE_FILE;
				log_error(L"error little data");
				return result_error;
			}
		}
		if (err != 2)
		{
			CLEAR_TABLE_CLOSE_FILE;
			log_error(L"data error in calibration table file");
			return result_error;
		}
		
		*(dm->table.X + i) = f1;
		*(dm->table.dX + i) = f2;
		if (i >= 1) 
			if ( (f1 - *(dm->table.X + i - 1) <= 0) || ((f1 + f2) - (*(dm->table.X + i - 1) + *(dm->table.dX + i - 1)) <= 0))
		{
				CLEAR_TABLE_CLOSE_FILE;
				log_error(L"error the data in the table is not monotonous.");
				return result_error;
		}

		i++;
		if (i > 99)
		{
			CLEAR_TABLE_CLOSE_FILE;
			log_error(L"error file contains more than 100 rows of data.");
			return result_error;
		}
	}
}

result_t XIMC_API set_correction_table(device_t id, const char* namefile)
{
	setlocale(LC_NUMERIC, "C");
	
	device_metadata_t* dm;
	FILE * fp = NULL;

	if (id == device_undefined)
	{
		log_error(L"attempting to close already closed device");
		return result_error;
	}
	dm = get_metadata(id);
	if (!dm)
	{
		log_error(L"could not extract metadata for device");
		id = device_undefined;
		return result_error;
	}

	if (namefile == NULL)
	{
		if (dm->table.X != NULL)
		{
			CLEAR_TABLE;
		}
		return result_ok;
	}
	if (dm->table.X != NULL)
	{
		CLEAR_TABLE;
	}

	fp = fopen(namefile, "r");
	if (fp == NULL)
	{
		log_error(L"error opening calibration table file");
		return result_error;
	}
	dm->table.X = (float *)malloc(100 * sizeof(float));
	dm->table.dX = (float *)malloc(100 * sizeof(float));

	char c1[100], c2[100];
	uint32_t i = 0;
	float f1, f2;
	int err;

	if (fscanf(fp, "%s%s", c1, c2) != 2)
	{
		CLEAR_TABLE_CLOSE_FILE;
		log_error(L"data error in calibration table file");
		return result_error;
	};

	while (true)
	{
		err = fscanf(fp, "%f%f", &f1, &f2);
		if (err == EOF)
		{
			if (i >= 2)
			{
				dm->table.len_table = i;
				fclose(fp);
				return result_ok;
			}
			else
			{
				CLEAR_TABLE_CLOSE_FILE;
				log_error(L"error little data");
				return result_error;
			}
		}
		if (err != 2)
		{
			CLEAR_TABLE_CLOSE_FILE;
			log_error(L"data error in calibration table file");
			return result_error;
		}

		*(dm->table.X + i) = f1;
		*(dm->table.dX + i) = f2;
		if (i >= 1)
		if ((f1 - *(dm->table.X + i - 1) <= 0) || ((f1 + f2) - (*(dm->table.X + i - 1) + *(dm->table.dX + i - 1)) <= 0))
		{
			CLEAR_TABLE_CLOSE_FILE;
			log_error(L"error the data in the table is not monotonous.");
			return result_error;
		}

		i++;
		if (i > 99)
		{
			CLEAR_TABLE_CLOSE_FILE;
			log_error(L"error file contains more than 100 rows of data.");
			return result_error;
		}
	}
}


device_t XIMC_API open_device (const char* uri)
{
	device_t device;
	lock_global();
	device = open_device_impl( uri, DEFAULT_TIMEOUT_TIME );
	unlock_global();
	return device;
}

result_t XIMC_API close_device (device_t* id)
{
	result_t result;
	lock_global();
	if (id == NULL || *id == device_undefined)
		result = result_error;
	else
		result = close_device_impl( id );
	return unlocker_global( result );
}

result_t XIMC_API reset_locks()
{
	/* nop */
	return result_ok;
}

result_t XIMC_API ximc_fix_usbser_sys(const char* device_uri)
{
	fix_usbser_sys( device_uri );
	return result_ok;
}

result_t XIMC_API get_status (device_t id, status_t* state)
{
	lock( id );
	return unlocker( id, get_status_impl( id, state ) );
}

result_t XIMC_API get_status_calb (device_t id, status_calb_t* state, const calibration_t* calibration)
{
	lock( id );
	return unlocker( id, get_status_impl_calb( id, state, calibration ) );
}

#if defined(__cplusplus)
};
#endif

// vim: syntax=c tabstop=4 shiftwidth=4

