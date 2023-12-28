# libximc

This is a python binding for libximc - cross-platform library for [Standa  8SMC5-USB](https://www.standa.lt/products/catalog/motorised_positioners?item=525) motor controllers. 

![8SMC5-based devices](https://raw.githubusercontent.com/EPC-MSU/libximc/dev-2.14/libximc/docs/8SMC5_based_devices.png)

Libximc manages hardware using interfaces: USB 2.0, RS232 and Ethernet, also uses a common and proven virtual serial port interface, so you can work with motor control modules through this library under Windows and Linux. MacOS X isn't supported yet.

This library also supports virtual devices. So you can make some tests without real hardware.

## Installation

```shell
pip install libximc
```

### Minimal example

```python
import time
import libximc.highlevel as ximc

# Virtual device will be used by default.
# In case you have real hardware set correct device URI here

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
axis.close_device()  # It's also called automatically by garbage collector, so explicit closing is optional

print("Done")
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
