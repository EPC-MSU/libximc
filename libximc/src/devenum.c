#include "common.h"

#include "ximc.h"
#include "util.h"
#include "loader.h"
#include "ximc-gen.h"
#include "metadata.h"
#include "platform.h"
#include "protosup.h"
#include <errno.h>

#if defined(WIN32) || defined(WIN64)
#include <io.h>
#include <winioctl.h>
#include <winsock2.h>
#include <Ws2tcpip.h>
#include <ws2def.h>
#include <ws2def.h>
#else
#include <unistd.h>

#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#endif

#ifdef __APPLE__
/* We need IOKit */
#include <CoreFoundation/CoreFoundation.h>
#include <IOKit/IOKitLib.h>
#include <IOKit/usb/IOUSBLib.h>
#include <sys/sysctl.h>
#endif
#define MINIUPNP_STATICLIB
#include <miniupnpc/miniupnpc.h>


/*
 * Types
 */

typedef struct enum_thread_state_t
{
    char* name;
    uint32_t serial;
    device_information_t* info;
    controller_name_t* controller_name;
    stage_name_t* stage_name;
    int status;
} enum_thread_state_t;

#ifdef _MSC_VER
#define PACK( __Declaration__ ) __pragma( pack(push, 1) ) __Declaration__ __pragma( pack(pop) )
#else
#define PACK( __Declaration__ ) __Declaration__ __attribute__((__packed__))
#endif

PACK(
struct my_device
{
    char Manufacturer[4];
    char ManufacturerId[2];
    char ProductDescription[8];
    uint8_t Major;
    uint8_t Minor;
    uint16_t Release;
    uint8_t reserved[12];
});
typedef struct my_device my_device_information_t;

PACK(
struct my_cname
{
    char ControllerName[16];
    uint8_t CtrlFlags;
    uint8_t reserved[7];
});
typedef struct my_cname my_controller_name_t;

PACK(
struct my_sname
{
    char PositionerName[16];
    uint8_t reserved[8];
});
typedef struct my_sname my_stage_name_t;

PACK(
struct device_desc {
    uint32_t serial;
    my_device_information_t my_device_information;
    my_controller_name_t my_cname;
    my_stage_name_t my_sname;
    uint32_t ipv4; // passed in network byte order
    uint32_t reserved1;
    char nodename[16];
    uint32_t axis_state;
    char locker_username[16];
    char locker_nodename[16];
    uint64_t locked_time;
    uint8_t reserved2[30];
});
typedef struct device_desc device_description;

/*
 * Device enumeration implementation
 */

/* doesn't lock, serial is optional
*/
int check_device_by_ximc_information (const char* name, device_information_t* info, uint32_t* serial, controller_name_t* cname, stage_name_t* sname)
{
    device_t device;
    device_information_t info_local;
    device_information_t* pinfo = info ? info : &info_local;

    controller_name_t cname_local;
    controller_name_t* pcname = cname ? cname : &cname_local;

    stage_name_t sname_local;
    stage_name_t* psname = sname ? sname : &sname_local;

    int is_ximc_device = 0;

    log_debug( L"enum thread: started, %hs", name );

    device = open_device_impl( name, ENUMERATE_TIMEOUT_TIME );
    if (device != device_undefined)
    {
        log_debug( L"enum thread: opened, starting GETI" );
        if (get_device_information_impl_unsynced( device, pinfo ) == result_ok)
        {
            log_debug( L"enum thread: successfully got GETI" );
            if (!strcmp(pinfo->Manufacturer, "XIMC") || !strcmp(pinfo->Manufacturer, "EPC "))
            {
                is_ximc_device = 1;
                if (serial)
                {
                    log_debug( L"enum thread: starting GSER" );
                    if (get_serial_number( device, serial ) != result_ok)
                    {
                        log_warning( L"Cannot get serial number from device %hs", name );
                        *serial = 0;
                    }
                    log_debug( L"enum thread: starting GNME" );
                    if (get_stage_name( device, psname ) != result_ok)
                    {
                        log_warning( L"Cannot get stage name from device %hs", name );
                    }
                    log_debug( L"enum thread: starting GNMF" );
                    if (get_controller_name( device, pcname ) != result_ok)
                    {
                        log_warning( L"Cannot get controller name from device %hs", name );
                    }
                }
            }
        }
        log_debug( L"enum thread: closing" );
        close_device_impl( &device );
        msec_sleep( ENUMERATE_CLOSE_TIMEOUT );
    }
    return is_ximc_device;
}

/* Concrete thread function to slowly check a device for beeing XIMC or mDrive */
void check_device_thread (void* arg)
{
    enum_thread_state_t* ts = (enum_thread_state_t*)arg;
    ts->status = check_device_by_ximc_information( ts->name, ts->info, &ts->serial, ts->controller_name, ts->stage_name ) ? 1 : 0;
}

/* Network enumeration thread function to do !!!*/
void network_enumerate_thread(void* arg)
{
    uint32_t count;
    netthread_state_t* ts = (netthread_state_t*)arg;
    count = 0;
#ifdef HAVE_XIBRIDGE
    xibridge_enumerate_adapter_devices(
        ts -> addr,
        ts -> adapter_addr,
        (char **)ts->pbuf,
        &count);
 #endif
    ts->devices_found = (unsigned int)count;
    ts->status = ts->devices_found ? 1 : 0;
}

/*
 * Launch device check threads
 * Remove non-passed device names from devenum
 */
void launch_check_threads(device_enumeration_opaque_t* devenum)
{
    /* Check all found devices in threads */
    enum_thread_state_t* tstates;
    int i, k;

    log_debug( L"precheck found %d devices, launching check threads", devenum->count );

    tstates = (enum_thread_state_t*)malloc( devenum->count*sizeof(enum_thread_state_t) );

    for (i = 0; i < devenum->count; ++i)
    {
        log_info( L"launch thread to probe device %hs", devenum->names[i] );
        tstates[i].name = devenum->names[i];
        tstates[i].info = &devenum->infos[i];
        tstates[i].controller_name = &devenum->controller_names[i];
        tstates[i].stage_name = &devenum->stage_names[i];
    }

    if (fork_join( check_device_thread, devenum->count, tstates, sizeof(enum_thread_state_t) ) != result_ok)
    {
        log_error( L"fork/join engine failed" );
        devenum->count = 0;
    }

    for (i = 0, k = 0; i < devenum->count; ++i)
    {
        log_debug( L"Check device %hs finished with %d", devenum->names[i], tstates[i].status );
        /* rewrite devenum array */
        if (tstates[i].status)
        {
            devenum->names[k] = tstates[i].name;
            devenum->serials[k] = tstates[i].serial;
            if (&devenum->infos[k] != tstates[i].info)
                memcpy( &devenum->infos[k], tstates[i].info, sizeof(device_information_t) );
            if (&devenum->controller_names[k] != tstates[i].controller_name)
                memcpy( &devenum->controller_names[k], tstates[i].controller_name, sizeof(controller_name_t) );
            if (&devenum->stage_names[k] != tstates[i].stage_name)
                memcpy( &devenum->stage_names[k], tstates[i].stage_name, sizeof(stage_name_t) );
            ++k;
        }
    }
    devenum->count = k;
    free( tstates );
}

/*
* Launch network enumerate threads
*/
XIMC_RETTYPE XIMC_CALLCONV launch_network_enumerate_threads(void* arg)
{
    net_enum_t* net_enum = (net_enum_t*)arg;
    /* Check all servers in threads */
    netthread_state_t* tstates;
    int i;

    log_debug(L"asked to enum %d servers, launching check threads", net_enum->server_count);

    tstates = (netthread_state_t*)malloc(net_enum->server_count * sizeof(netthread_state_t));

    for (i = 0; i < net_enum->server_count; ++i)
    {
        log_info(L"launch thread %d to enumerate address %hs", i, net_enum->addrs[i]);
        tstates[i].addr = net_enum->addrs[i];
        tstates[i].adapter_addr = net_enum->adapter_addr;
        tstates[i].pbuf = net_enum->pbufs[i];
        tstates[i].status = 0;
        tstates[i].devices_found = 0;
    }

    fork_join_with_timeout(network_enumerate_thread, net_enum->server_count, tstates, sizeof(netthread_state_t), DEFAULT_TIMEOUT_TIME, net_enum);
    free(tstates);
    return (XIMC_RETTYPE)0;
}

void single_thread_wrapper_function(void* arg)
{
    net_enum_t* net_enum = (net_enum_t*)arg;
    net_enum->mutex = mutex_init(0); // the nonce is unused on windows only
    mutex_t *mutex = net_enum->mutex;

    mutex_lock(mutex);
    single_thread_launcher(launch_network_enumerate_threads, (void*)net_enum);
    mutex_lock(mutex); // blocks this thread until enumerate controller thread unlocks the mutex after a timeout
    mutex_unlock(mutex);
    mutex_close(mutex);
}

/* Concrete callback function that saves provided device name into enumerator */
void store_device_name (char* name, void* arg)
{
    device_enumeration_opaque_t* devenum = (device_enumeration_opaque_t*)arg;
    int i;
    size_t max_name_len = 4096;
    char *encoded_name;

    for (i = 0; i < devenum->count; ++i)
    {
        if (is_same_device( name, devenum->raw_names[i] ))
        {
            log_debug( L"Skipping duplicate device %hs", name );
            return;
        }
    }

    log_debug( L"Storing port %hs", name );

    if (devenum->count >= devenum->allocated_count)
    {
        devenum->allocated_count = (int)(devenum->allocated_count * 1.5);
        devenum->names = (char**)realloc( devenum->names, devenum->allocated_count*sizeof(char*) );
        devenum->raw_names = (char**)realloc( devenum->raw_names, devenum->allocated_count*sizeof(char*) );
        devenum->serials = (uint32_t*)realloc( devenum->serials, devenum->allocated_count*sizeof(uint32_t) );
        devenum->infos = (device_information_t*)realloc( devenum->infos, devenum->allocated_count*sizeof(device_information_t) );
        devenum->controller_names = (controller_name_t*)realloc( devenum->controller_names, devenum->allocated_count*sizeof(controller_name_t) );
        devenum->stage_names = (stage_name_t*)realloc( devenum->stage_names, devenum->allocated_count*sizeof(stage_name_t) );
        devenum->dev_net_infos = (device_network_information_t*)realloc( devenum->dev_net_infos, devenum->allocated_count*sizeof(device_network_information_t) );
    }

    encoded_name = uri_copy(name);

    devenum->names[devenum->count] = (char*)malloc(max_name_len);
    if (*encoded_name && *encoded_name == '/')
    {
        /* absolute path - make file:// uri, like xi-com:///dev/tty */
        /* skip first slash for absolute pathes */
        portable_snprintf(devenum->names[devenum->count], max_name_len-1, "xi-com://%s", encoded_name);
    }
    else
    {
        /* simple name - make uri with empty host and path component, like xi-com:///COM42
         * use instead more clear URI without hier path, like xi-com:COM42, xi-com:%5C%5C.%5CCOM42 */
        portable_snprintf(devenum->names[devenum->count], max_name_len-1, "xi-com:%s", encoded_name);
    }
    devenum->names[devenum->count][max_name_len-1] = '\0';
    devenum->raw_names[devenum->count] = portable_strdup( name );
    free(encoded_name);
    ++devenum->count;
}


/* Concrete callback function that saves provided device name with some xi-prefix into enumerator */
void store_device_name_with_xi_prefix(char* name, void* arg)
{
    device_enumeration_opaque_t* devenum = (device_enumeration_opaque_t*)arg;
    int i;
    size_t max_name_len = 4096;
    char *encoded_name;

    for (i = 0; i < devenum->count; ++i)
    {
        if (is_same_device(name, devenum->raw_names[i]))
        {
            log_debug(L"Skipping duplicate device %hs", name);
            return;
        }
    }

    log_debug(L"Storing device uri %hs", name);

    if (devenum->count >= devenum->allocated_count)
    {
        devenum->allocated_count = (int)(devenum->allocated_count * 1.5);
        devenum->names = (char**)realloc(devenum->names, devenum->allocated_count*sizeof(char*));
        devenum->raw_names = (char**)realloc(devenum->raw_names, devenum->allocated_count*sizeof(char*));
        devenum->serials = (uint32_t*)realloc(devenum->serials, devenum->allocated_count*sizeof(uint32_t));
        devenum->infos = (device_information_t*)realloc(devenum->infos, devenum->allocated_count*sizeof(device_information_t));
        devenum->controller_names = (controller_name_t*)realloc(devenum->controller_names, devenum->allocated_count*sizeof(controller_name_t));
        devenum->stage_names = (stage_name_t*)realloc(devenum->stage_names, devenum->allocated_count*sizeof(stage_name_t));
        devenum->dev_net_infos = (device_network_information_t*)realloc(devenum->dev_net_infos, devenum->allocated_count*sizeof(device_network_information_t));
    }

    encoded_name = uri_copy(name);

    devenum->names[devenum->count] = (char*)malloc(max_name_len);
    portable_snprintf(devenum->names[devenum->count], max_name_len - 1, "%s", encoded_name);
    
    devenum->names[devenum->count][max_name_len - 1] = '\0';
    devenum->raw_names[devenum->count] = portable_strdup(name);
    free(encoded_name);
    ++devenum->count;
}


/*
for finding key in libximc without using c++ functions.
*/
int find_key(const char* hints, const char* key, char* buf, size_t length)
{
    if (hints == NULL) return 0;
    char *s, *ptr, *ptoc, *eptr, *pbuf;
    int key_count, i;
    size_t len, final_len;
    char delim, eq;
    int ret;
    s = (char *)malloc(strlen(hints) + 1);
    memcpy(s, hints, strlen(hints));
    s[strlen(hints)] = 0;

    delim = '\n';
    eq = '=';
    key_count = 0;
    ret = 1;
    do
    { // exit when no new item is found in strrchr() function
        ptr = strrchr(s, eq);
        if (ptr == NULL) break;
        key_count++;
        while (ptr != s && *ptr != delim) // find the nearest left delimiter
            ptr--;
        if (ptr == s) break;
        *ptr-- = 0;
    } while (1);
    ptr = s;
    for (i = 0; i < key_count; i++)
    {
        len = strlen(ptr);
        ptoc = ptr;
        ptoc += strspn(ptoc, " \t");
        if (portable_strncasecmp(ptoc, key, strlen(key)) == 0 && strchr(ptoc, eq) != NULL)
        {
            ptoc += strlen(key);
            ptoc += strspn(ptoc, " \t");
            if (*ptoc++ == eq)
            {
                ptoc += strspn(ptoc, " \t");
                eptr = ptoc + strlen(ptoc) - 1;
                // trailng spaces to zero
                while (eptr != ptoc && (*eptr == ' ' || *eptr == '\t'))
                    *eptr-- = 0;
                final_len = 0;
                pbuf = buf;
                while (ptoc != NULL)
                {
                    ptoc += strspn(ptoc, " \t");
                    eptr = strchr(ptoc, ',');
                    if (eptr == NULL) eptr = strchr(ptoc, 0);
                    if (eptr != NULL)
                    {
                        eptr--;
                        while (eptr != ptoc && (*eptr == ' ' || *eptr == '\t'))
                            eptr--;
                        eptr++;
                        if (length >= (size_t)(final_len + eptr - ptoc + 1))
                        {
                            memcpy(pbuf, ptoc, eptr - ptoc);
                            final_len += (eptr - ptoc);
                            buf[final_len++] = ',';
                            pbuf += eptr - ptoc + 1;
                            ptoc = strchr(ptoc, ',');
                            if (ptoc) ptoc++;
                        }
                        else
                        {
                            // buffer size is not enough
                            ptoc = NULL;
                            ret = 0;
                        }
                    }
                    else
                    {
                        // some invalid data
                        ptoc = NULL;
                        ret = 0;
                    }
                }
                if (final_len) final_len--;
                buf[final_len] = 0;
                free(s);
                return ret;
            }
        }
        ptr += (len + 1);
    }
    free(s);
    return 0;
}


#ifdef HAVE_XIBRIDGE
/*
 * The next three  funcions are unavilable without wrapper library
*/
void get_addresses_from_hints_by_type(const char *hints, const char *xi_prefix, char **rel_data)
{
    char *addr, *ptr, *new_ptr, *p;
    int  i, n_count;
    size_t len_out, len, hint_length;

    *rel_data = NULL;
    n_count = 0;
    hint_length = len_out = len = 0;


    if (hints == NULL) return;
    hint_length = strlen(hints);
    addr = (char *)malloc(hint_length + 1);
    memset(addr, 0, hint_length + 1);

    
    if (!find_key(hints, "addr", addr, strlen(hints))) // addr is to be filled
    {

        free(addr);
        return;
    }
    ptr = addr;
    while (ptr != NULL)
    { // exit when no new item is found in strchr() function
        n_count++;
        new_ptr = strchr(ptr, ','); // Find location of the next comma or get NULL instead
        if (new_ptr != NULL)
        {   // NULL means there is no commas left and we must quit
            *new_ptr = 0;
        }
        len = strlen(ptr);
        if ((strlen(xi_prefix) == 0 && strstr(ptr, ":/") == NULL) ||
            (strlen(xi_prefix) != 0 && portable_strncasecmp(ptr, xi_prefix, strlen(xi_prefix)) == 0))
        {
            len_out += (len + 1);
        }

        if (new_ptr != NULL)
        {   // NULL means there is no commas left and we must quit
            ptr = new_ptr + 1; // Continue with string after the comma
        }
        else ptr = NULL;
    }
    if (len_out == 0) len_out++;
    *rel_data = p = (char *)malloc(len_out);
    memset(p, 0, len_out);
    ptr = addr;
    for (i = 0; i < n_count; i++)
    {
        len = strlen(ptr);
        if ((strlen(xi_prefix) == 0 && strstr(ptr, ":/") == NULL) ||
            (strlen(xi_prefix) != 0 && portable_strncasecmp(ptr, xi_prefix, strlen(xi_prefix)) == 0))
        {
            memcpy(p, ptr, len);
            memcpy(p + len, ",", 1);
            p += (len + 1);
        }
        ptr += (len + 1);
    }

    if (p > *rel_data) *(p - 1) = 0;
    free(addr);
}


result_t enumerate_udp_devices(
    enumerate_devices_directory_callback_t callback,
    device_enumeration_opaque_t *devenum,
    const char *hints
    )
{
    char *hints_udp, *ptr, *new_ptr;
    get_addresses_from_hints_by_type(hints, "xi-udp", &hints_udp);
    if (hints_udp == NULL)
    {
        // no addr key was found
        return result_ok;
    }
    ptr = hints_udp;

    if (strlen(hints_udp) ==  0)
    {
        // to do network enumerate (network discover)
        
    }
    else
    {
        while (ptr != NULL)
        { // exit when no new item is found in strchr() function
            new_ptr = strchr(ptr, ','); // Find location of the next comma or get NULL instead
            if (new_ptr != NULL)
            {   // NULL means there is no commas left and we must quit
                *new_ptr = 0;
            }
            callback(ptr, devenum);

            if (new_ptr != NULL)
            {   // NULL means there is no commas left and we must quit
                ptr = new_ptr + 1; // Continue with string after the comma
            }
            else ptr = NULL;
        }
    }
    free(hints_udp);
    return result_ok;
}

// discovers by ssdp, adds as xi-tcp-device
result_t discover_ssdp_add_as_tcp(
    enumerate_devices_directory_callback_t callback,
    device_enumeration_opaque_t *devenum
    )
{
    char *ip_start, *ip_end;
    struct UPNPDev * device;
    struct UPNPDev * devlist = 0;
    int error = 0;
    char discover_ip[64];
    size_t ip_len;
#ifdef _WIN32
    WSADATA wsaData;
#endif
    strcpy(discover_ip, "xi-tcp://");
   
#ifdef _WIN32
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != NO_ERROR)
    {
        return result_error;
    }
#endif
    if ((devlist = upnpDiscoverAll(2000, NULL, NULL, 0, 0, 2, &error)) != NULL)
    {
        for (device = devlist; device; device = device->pNext)
        {
            if (strstr(device->server, "8SMC5-USB") != NULL || strstr (device->server, "mDrive") != NULL)
            {
                ip_start = strstr(device->descURL, "://");
                if (ip_start == NULL) continue;
                ip_end = strchr(ip_start + 3, ':');
                if (ip_end == NULL) ip_end = strchr(ip_start, '/');
                if (ip_end == NULL) ip_end = strchr(ip_start, 0);
                if (ip_end == NULL || ip_end < (ip_start + 3)) continue;
                ip_len = ip_end - ip_start - 3;
                if (ip_end  < 3 + ip_start || ip_len > 63 - 9) continue; //"xi-tcp://"- len = 9
                memcpy(discover_ip + 9, ip_start + 3, ip_len);
                // add default port number for xi-tcp
                portable_snprintf(discover_ip + 9 + ip_len, 64 - 9 - ip_len, ":%u", XIMC_TCP_PORT);
                callback(discover_ip, devenum);
            }
        }
        freeUPNPDevlist(devlist); devlist = 0;
    }

#ifdef _WIN32
    WSACleanup();
#endif
    return result_ok;
}


result_t enumerate_tcp_devices(
    enumerate_devices_directory_callback_t callback,
    device_enumeration_opaque_t *devenum,
    const char *hints
    )
{
    char *hints_tcp, *ptr, *new_ptr;
    get_addresses_from_hints_by_type(hints, "xi-tcp", &hints_tcp);
    if (hints_tcp == NULL)
    {
        // no addr key was found
        return result_ok;
    }
    if (strlen(hints_tcp) == 0)
    {
        // to do network enumerate (network discover)
    }
    else
    {
        ptr = hints_tcp;
        while (ptr != NULL)
        { // exit when no new item is found in strchr() function
            new_ptr = strchr(ptr, ','); // Find location of the next comma or get NULL instead
            if (new_ptr != NULL)
            {   // NULL means there is no commas left and we must quit
                *new_ptr = 0;
            }
            callback(ptr, devenum);

            if (new_ptr != NULL)
            {   // NULL means there is no commas left and we must quit
                ptr = new_ptr + 1; // Continue with string after the comma
            }
            else ptr = NULL;
        }
    }
    free(hints_tcp);
    return result_ok;
}

void enumerate_ssdp(void *arg)
{
    device_enumeration_opaque_t *devenum;
    int enumresult;
    devenum = (device_enumeration_opaque_t *)arg;
    if ((enumresult = discover_ssdp_add_as_tcp(store_device_name_with_xi_prefix, devenum)) != result_ok)
    {
        log_debug(L"network discover failed with error %d", enumresult);
    }
 }

result_t enumerate_xinet_devices_enumerate_ssdp(
    enumerate_devices_directory_callback_t callback,
    device_enumeration_opaque_t *devenum,
    const char *hints
    )
{
    uint32_t count;
    char *hints_net, *adapter,  *token, *pdev;
    net_enum_t net_enum;
    int items, i, server, nitems;
    size_t hint_length;

    get_addresses_from_hints_by_type(hints, "", &hints_net);
    if (hints_net == NULL)
    {
        // no addr key was found
        return result_ok;
    }
    hint_length = strlen(hints);
    adapter = (char *)malloc(hint_length + 1);
    memset(adapter, 0, hint_length + 1);
    find_key(hints, "adapter_addr", adapter, hint_length);
    items = 0; // may be only ,
    token = hints_net;
    if (*token != 0 && *token != ',')
    {
        items++; // = 1, at least one item presents
    }
    while (*token != 0)
    {
        if (*token++ == ',' && *token != ',' && *token != 0) items++;
    }

    nitems = items == 0 ? 1 : items;   // either brodcast enumerate or enumerate servers
    
    // prepare net_enum data
    net_enum.server_count = nitems;
    net_enum.device_count = (int*)malloc(sizeof (int)* nitems);
    net_enum.addrs = (char**)malloc(sizeof (char*)* nitems);
    net_enum.pbufs = (uint8_t***)malloc(sizeof(uint8_t**)* nitems);
    net_enum.adapter_addr = adapter;
    
    if (items == 0) // only one item for broadcast enumerate
    {
        // some broadcast enumerate
        net_enum.addrs[0] = "";
        net_enum.pbufs[0] = (uint8_t**)malloc(sizeof(uint8_t*));  // allocation for pointer to buffer, not the buffer itself
        *(net_enum.pbufs[0]) = NULL;
        net_enum.device_count[0] = 0;
    }
    else 
    {
        token = strtok(hints_net, ",");
        i = 0;
        while (i < items)
        {
			if (strlen(token) > 0)
			{
                net_enum.addrs[i] = token;
                net_enum.pbufs[i] = (uint8_t**)malloc(sizeof(uint8_t*));  // allocation for pointer to buffer, not the buffer itself
                *(net_enum.pbufs[i]) = NULL;
                net_enum.device_count[i] = 0;
                i++;
			}	
           
            token = strtok(NULL, ",");
        }
    }
    // instead of single_thread_wrapper_function(&net_enum)
    // enumerate ssdp and xi-net enumerate(single_thread_wrapper_function) to be called concurrently
    fork_join_2_threads(enumerate_ssdp, devenum, 1,
        single_thread_wrapper_function, &net_enum, 1
        );
    for (server = 0; server < net_enum.server_count; server++)
    {
        pdev = (char *)*net_enum.pbufs[server];
        count = net_enum.device_count[server];
        while (count--)
        {
            callback(pdev, devenum);
            pdev = strchr(pdev, 0) + 1;
        }
        xibridge_free_enumerate_devices((char *)*net_enum.pbufs[server]); // free the buffer allocations from xibridge_enumerate
    }
    free(hints_net); 
    free(adapter);
    // also free the net_enum
    free(net_enum.device_count);
    free(net_enum.addrs);
    free(net_enum.pbufs);
    return result_ok;
}

#endif 

/* Enumerate devices main function */
result_t enumerate_devices_impl(device_enumeration_opaque_t** device_enumeration, int enumerate_flags, const char * hints)
{
    device_enumeration_opaque_t* devenum;
#ifdef HAVE_XIBRIDGE
    result_t enumresult;
#else
    XIMC_UNUSED(hints)
#endif

    /* ensure one-thread mutex init */
    lock_metadata();
    unlock_metadata();

    /* alloc mem */
    *device_enumeration = (device_enumeration_opaque_t*)malloc(sizeof(device_enumeration_opaque_t));
    devenum = *device_enumeration;
    devenum->flags = enumerate_flags;
    devenum->count = 0;
    devenum->allocated_count = 40;
    devenum->names = (char**)malloc(devenum->allocated_count * sizeof(char*));
    devenum->raw_names = (char**)malloc(devenum->allocated_count * sizeof(char*));
    devenum->serials = (uint32_t*)malloc(devenum->allocated_count * sizeof(uint32_t));
    devenum->infos = (device_information_t*)malloc(devenum->allocated_count * sizeof(device_information_t));
    devenum->controller_names = (controller_name_t*)malloc(devenum->allocated_count * sizeof(controller_name_t));
    devenum->stage_names = (stage_name_t*)malloc(devenum->allocated_count * sizeof(stage_name_t));
    devenum->dev_net_infos = (device_network_information_t*)malloc(devenum->allocated_count * sizeof(device_network_information_t));
    memset(devenum->infos, 0, devenum->allocated_count * sizeof(device_information_t));
    memset(devenum->controller_names, 0, devenum->allocated_count * sizeof(controller_name_t));
    memset(devenum->stage_names, 0, devenum->allocated_count * sizeof(stage_name_t));
    memset(devenum->dev_net_infos, 0, devenum->allocated_count * sizeof(device_network_information_t));

    /* Call implementation-specific directory enumerator */
    if (enumerate_devices_directory(store_device_name, devenum,
        enumerate_flags) != result_ok)
    {
        log_debug(L"enumerate_devices_directory failed");
        devenum->count = 0;
        return result_error;
    }

    if (enumerate_flags & ENUMERATE_NETWORK)
    {
#ifdef HAVE_XIBRIDGE
        enumresult = enumerate_tcp_devices(store_device_name_with_xi_prefix, devenum, hints);
        if (enumresult != result_ok)
        {
            log_debug(L"enumerate_tcp_devices failed with error %d", enumresult);
        }

        enumresult = enumerate_udp_devices(store_device_name_with_xi_prefix, devenum, hints);
        if (enumresult != result_ok)
        {
            log_debug(L"enumerate_udp_devices failed with error %d", enumresult);
        }
        enumresult = enumerate_xinet_devices_enumerate_ssdp(store_device_name_with_xi_prefix, devenum, hints);
        if (enumresult != result_ok)
        {
            log_debug(L"enumerate_xinet_devices failed with error %d", enumresult);
        }

#else
        return result_error;
#endif
    }

    /* Check all found devices in threads */
    if ((enumerate_flags & ENUMERATE_PROBE) && devenum->count > 0)
    {
        launch_check_threads(devenum);
    }

    log_debug(L"found %d devices", devenum->count);
    return result_ok;
}
/*
 * Exported device enumeration functions
 */

/* we do not have read/write lock so lock all DE functions with one global lock */

result_t XIMC_API set_bindy_key(const char* keyfilepath)
{
    log_warning(L"set_bindy_key() CALLED, which is deprecated, '%s' ignored.", keyfilepath);
    return result_ok;
}


device_enumeration_t XIMC_API enumerate_devices(int enumerate_flags, const char *hints)
{
    device_enumeration_opaque_t* de;
    result_t result;
    lock_global();
    result = enumerate_devices_impl( &de, enumerate_flags, hints );
    unlock_global();
    return result == result_ok ? (device_enumeration_t)de : 0;
}

result_t XIMC_API free_enumerate_devices(device_enumeration_t device_enumeration)
{
    device_enumeration_opaque_t* de = (device_enumeration_opaque_t*)device_enumeration;
    int i;
    lock_global();
    if (de)
    {
        if (de->names)
        {
            for (i = 0; i < de->count; ++i)
                if (de->names[i])
                    free( de->names[i] );
            free(de->names);
        }
        if (de->raw_names)
        {
            for (i = 0; i < de->count; ++i)
                if (de->raw_names[i])
                    free( de->raw_names[i] );
            free(de->raw_names);
        }
        if (de->serials)
            free( de->serials );
        if (de->infos)
            free( de->infos );
        if (de->controller_names)
            free( de->controller_names );
        if (de->stage_names)
            free( de->stage_names );
        if (de->dev_net_infos)
            free( de->dev_net_infos );
        /* just to be sure */
        de->names = NULL;
        de->raw_names = NULL;
        de->serials = NULL;
        de->infos = NULL;
        de->controller_names = NULL;
        de->stage_names = NULL;
        de->dev_net_infos = NULL;
        de->count = 0;
        free(de);
    }
    unlock_global();
    return result_ok;
}

int XIMC_API get_device_count(device_enumeration_t device_enumeration)
{
    device_enumeration_opaque_t* de = (device_enumeration_opaque_t*)device_enumeration;
    if (!de)
        return result_error;
    lock_global();
    return unlocker_global( de->count );
}

pchar XIMC_API get_device_name(device_enumeration_t device_enumeration, int device_index)
{
    device_enumeration_opaque_t* de = (device_enumeration_opaque_t*)device_enumeration;
    char* device_name = NULL;
    if (!de)
        return NULL;
    lock_global();
    if (device_index >= 0 && device_index < de->count)
        device_name = de->names[device_index];
    unlock_global();
    return device_name;
}

result_t XIMC_API get_enumerate_device_serial(device_enumeration_t device_enumeration, int device_index, uint32_t* serial)
{
    device_enumeration_opaque_t* de = (device_enumeration_opaque_t*)device_enumeration;
    result_t result = result_ok;
    if (!de)
        return result_error;
    lock_global();
    if ((de->flags & ENUMERATE_PROBE) &&
            device_index >= 0 && device_index < de->count)
        *serial = de->serials[device_index];
    else
        result = result_error;
    return unlocker_global(result);
}

result_t XIMC_API get_enumerate_device_information(device_enumeration_t device_enumeration, int device_index, device_information_t* device_information)
{
    device_enumeration_opaque_t* de = (device_enumeration_opaque_t*)device_enumeration;
    result_t result = result_ok;
    if (!de)
        return result_error;
    lock_global();
    if ((de->flags & ENUMERATE_PROBE) &&
            device_index >= 0 && device_index < de->count)
        memcpy( device_information, &de->infos[device_index], sizeof(device_information_t) );
    else
        result = result_error;
    return unlocker_global(result);
}

result_t XIMC_API get_enumerate_device_controller_name(device_enumeration_t device_enumeration, int device_index, controller_name_t* controller_name)
{
    device_enumeration_opaque_t* de = (device_enumeration_opaque_t*)device_enumeration;
    result_t result = result_ok;
    if (!de)
        return result_error;
    lock_global();
    if ((de->flags & ENUMERATE_PROBE) &&
            device_index >= 0 && device_index < de->count)
        memcpy( controller_name, &de->controller_names[device_index], sizeof(controller_name_t) );
    else
        result = result_error;
    return unlocker_global(result);
}

result_t XIMC_API get_enumerate_device_stage_name(device_enumeration_t device_enumeration, int device_index, stage_name_t* stage_name)
{
    device_enumeration_opaque_t* de = (device_enumeration_opaque_t*)device_enumeration;
    result_t result = result_ok;
    if (!de)
        return result_error;
    lock_global();
    if ((de->flags & ENUMERATE_PROBE) &&
            device_index >= 0 && device_index < de->count)
        memcpy( stage_name, &de->stage_names[device_index], sizeof(stage_name_t) );
    else
        result = result_error;
    return unlocker_global(result);
}

result_t XIMC_API get_enumerate_device_network_information(device_enumeration_t device_enumeration, int device_index, device_network_information_t* device_network_information)
{
    device_enumeration_opaque_t* de = (device_enumeration_opaque_t*)device_enumeration;
    result_t result = result_ok;
    if (!de)
        return result_error;
    lock_global();
    if ((de->flags & ENUMERATE_PROBE) &&
            device_index >= 0 && device_index < de->count)
        memcpy( device_network_information, &de->dev_net_infos[device_index], sizeof(device_network_information_t) );
    else
        result = result_error;
    return unlocker_global(result);
}

result_t XIMC_API probe_device (const char* uri)
{
    result_t result;
    lock_global();
    result = check_device_by_ximc_information( uri, NULL, NULL, NULL, NULL ) ? result_ok : result_nodevice;
    return unlocker_global( result );
}



// vim: syntax=c tabstop=4 shiftwidth=4
