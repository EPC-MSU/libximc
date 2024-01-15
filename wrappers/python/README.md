# libximc

This is a python binding for libximc - cross-platform library for [Standa  8SMC5-USB](https://www.standa.lt/products/catalog/motorised_positioners?item=525) motor controllers. 

![8SMC5-based devices](https://raw.githubusercontent.com/EPC-MSU/libximc/dev-2.14/libximc/docs/8SMC5_based_devices.png)

Libximc manages hardware using interfaces: USB 2.0, RS232 and Ethernet, also uses a common and proven virtual serial port interface, so you can work with motor control modules through this library under Windows and Linux. MacOS X isn't supported yet.

This library also supports virtual devices. So you can make some tests without real hardware.

## Installation

```shell
pip install libximc
```

### Minimal new API example

```python
import time
import libximc.highlevel as ximc

# Virtual device will be used by default.
# In case you have real hardware, set correct device URI here

device_uri = r"xi-emu:///ABS_PATH/virtual_controller.bin"  # Virtual device
# device_uri = r"xi-com:\\.\COM111"                        # Serial port
# device_uri = "xi-tcp://172.16.130.155:1820"              # Raw TCP connection
# device_uri = "xi-net://192.168.1.120/abcd"               # XiNet connection

axis = ximc.Axis(device_uri)
axis.open_device()

print("Launch movement...")
axis.command_right()

time.sleep(3)

print("Stop movement")
axis.command_stop()

print("Disconnect device")
axis.close_device()  # It's also called automatically by the garbage collector, so explicit closing is optional

print("Done")
```

### Full new API example

See Colab notebook for full example: https://colab.research.google.com/drive/1tGHFRcVwf0DmQOFm_JtOOr7fXsfKUSrg

# Detailed view on new API

We are glad to introduce new libximc *highlevel* API! You can access it via:

```python
import libximc.highlevel as ximc
```

## New API principles

* All controller related functions are methods of an Axis class:
  
  ```python
  # Axis constructor takes device URI as string (not bytes)
  axis = ximc.Axis("xi-emu:///home/user/virtual-device.bin")
  axis.device_open()  # Note: device must be opened manually
  
  axis.command_move(10, 0)
  
  # Note: device closing, axis.close_device(), is performed automatically by the garbage collector.
  ```
  
  Other libximc functions can be accessed via `ximc` itself, e.g. `ximc.ximc_version()`.

* As you could notice, there is no need to pass `device_id` to the commands any more. Axis class does it internally.

* You don't need to pass the `calibration_t` structure to the `*_calb` functions. Instead, set calibrations via `axis.set_calb(A, MicrostepMode)` and then use any  `*_calb` function:
  
  ```python
  axis.set_calb(0.048, ximc.MicrostepMode.MICROSTEP_MODE_FRAC_256)
  
  axis.command_move_calb(12.3)
  ```

* All flags' enumerations are placed in `ximc`. For example, to get `EnumerationFlags` use `ximc.EnumerateFlags.<desired-flag>`.

* All C-legacy exit status codes are transformed to Python exceptions.

* In case you want to get any available data structure from the controller, you don't need to create an empty data structure and pass it to corresponding function. Instead, use single-line instruction, like:
  
  ```python
  # Example for move_settings. You can use your desired get_*() command
  move_settings = axis.get_move_settings()
  ```

* `ximc.enumerate_devices()` returns list of dictionaries containing information about found devices. Hint: to get full information about devices, use flag `ximc.EnumerationFlags.EnumerateFlags.ENUMERATE_PROBE`:
  
  ```python
  # Get full information while enumerating
  ximc.enumerate_devices(ximc.EnumerateFlags.ENUMERATE_PROBE)
  ```

* Manufactures-only functions aren't supported.

* Logging functions aren't supported.

## I want to use the old version. What should I do?

If you want to use the old API (*lowlevel* libximc), don't worry. Just

```python
import libximc.lowlevel as ximc  # Such an import provides you with the old version of libximc binding
```

## More information

* Libximc library documentation: https://libximc.xisupport.com/doc-en/index.html

* Standa 8SMC5 motor controller user manual: https://doc.xisupport.com/en/8smc5-usb/

* Standa website: https://www.standa.lt/

If you have faced any issues while using the library and you have no idea how to solve them contact **technical support** via:

* Website: [en.xisupport.com](https://en.xisupport.com/account/register)
* E-mail: [8smc4@standa.lt](mailto:8smc4@standa.lt)
* Telegram: [@SMC5TechSupport](https://t.me/SMC5TechSupport)
* WhatsApp: [ +1 (530) 584 4117](https://wa.me/15305844117)
