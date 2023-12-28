Summary: Library for controlling DC brush motor
Name: libximc7
Version: 2.14.20
Release: 1
Source0: %{name}-%{version}.tar.gz
License: BSD
Packager: XIMC
URL: http://ximc.ru
Requires: glibc
Conflicts: libximc6
Group: Development/Libraries/C and C++
BuildRoot: %{_builddir}/%{name}-%{version}-root

%description
Library for controlling stepper and other motors.
It provides a simple C interface for controlling and configuring engine and controller.
It uses a common virtual serial port driver embedded in all OS.

%package devel
Summary: Development library for libximc
Requires: %{name} = %{version}-%{release}
Group: Development/Libraries/C and C++

%description devel
Development library for controlling stepper and other motors.
It provides a simple C interface for controlling and configuring engine and controller.
It uses a common virtual serial port driver embedded in all OS.

%define _udevrulesdir /lib/udev/rules.d
%define _resourcedir /usr/share/libximc

%prep
%setup -q

%build
%configure --with-docs %{_package_extra_configure}
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install-strip
install -d $RPM_BUILD_ROOT/%{_udevrulesdir}
install -m 0644 debian/%{name}.udev $RPM_BUILD_ROOT/%{_udevrulesdir}/50-%{name}.rules
rm -f %{buildroot}%{_libdir}/libximc.la %{buildroot}%{_libdir}/libjximc.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libximc.so.*
%{_libdir}/libjximc.so.*
%{_libdir}/libjximc.so
%{_libdir}/libbindy.so
%{_libdir}/libxiwrapper.so
%{_javadir}/libjximc.jar
%{_udevrulesdir}/50-%{name}.rules
%doc COPYING AUTHORS README NEWS
%{_datadir}/doc/%{name}/doc-ru/%{name}-ru.pdf
%{_datadir}/doc/%{name}/doc-ru/html/*
%{_datadir}/doc/%{name}/doc-en/%{name}-en.pdf
%{_datadir}/doc/%{name}/doc-en/html/*
%{_datadir}/doc/%{name}/doc-java/html/*

%files devel
%defattr(-,root,root)
%doc COPYING AUTHORS README NEWS
%{_includedir}/ximc.h
%{_libdir}/libximc.so

%changelog

* Thu Dec 28 2023 XIMC <info@ximc.ru> - 2.14.20
- version bump
- add new python binding
- fix docs

* Mon Nov 13 2023 XIMC <info@ximc.ru> - 2.14.19
- version bump
- remove PyPI builder out of the repo, #85896
- complete working on APIv2 binding, #86075
- fix english documentation, #87709
- change UserPassword type to char[]

* Tue Sep 12 2023 XIMC <info@ximc.ru> - 2.14.18
- version bump
- Feature #85091 Taking position calculation out to the place before
- all command execution (before switch statement)
- Feature #84179 Now use only absolute paths for virtual controllers

* Wed Aug 23 2023 XIMC <info@ximc.ru> - 2.14.17
- version bump
- Bug #84285 Incorrect virtual controllers

* Mon Aug 21 2023 XIMC <info@ximc.ru> - 2.14.16
- version bump
- Feature #83712 mDrive enumerate enumerate and discovery errors fixed 

* Tue Jul 25 2023 XIMC <info@ximc.ru> - 2.14.15
- version bump
- Feature #83712 mDrive enumerate and discovery added

* Thu Jun 22 2023 XIMC <info@ximc.ru> - 2.14.14
- version bump
- Feature #70712 jupiter libximc improved
- Feature #74546 readme added to the pypi libximc example
- Feature #75619 hints argument description corrected
- Feature #76913 Documentation start pages reviewed
- Feature #79128 libximc .sh scripts improved

* Thu May 11 2023 XIMC <info@ximc.ru> - 2.14.13
- version bump
- Feature #77391 Wrong position returned in virtual controllers fixed

* Tue Mar 07 2023 XIMC <info@ximc.ru> - 2.14.11
- version bump
- Feature #74036 additionally: set_bindy_key calls removed from examples

* Fri Feb 17 2023 XIMC <info@ximc.ru> - 2.14.10
- version bump
- Feature #74028 Updated wiring diagrams
- Feature #74036 keyfile.sqlite removed
- Feature #74552 Nagle algorithm off in xi-tcp
- Feature #74671 Unused files removed from example projects
- Feature #74594 Jupiter_demo added
- Feature #70732 Virtual controller updated
- Feature #74575 emumerate_device function made multithreaded
- Feature #74580 Miniupnpc using improved

* Fri Jan 20 2023 XIMC <info@ximc.ru> - 2.14.9
- version bump
- Feature #72852 XIMC-device net discovering added (miniupnpc used)

* Wed Dec 28 2022 XIMC <info@ximc.ru> - 2.14.8
- version bump
- Feature #53770 calibration_t struct description changed
- Feature #72516 C example moved to test_C directory
- Feature #71035 python jupiter example improved
- Feature #72241 libximc virtual controller updated
- Feature #65676 The same separator applied for all correction tables

* Wed Nov 09 2022 XIMC <info@ximc.ru> - 2.14.7
- version bump
- Feature #69053 extendtest example bug fixed
- Feature #67205 jupiter example added
- Feature #69542 extendspython example: netifaces module changed for ifaddr

* Wed Sep 07 2022 XIMC <info@ximc.ru> - 2.14.6
- version bump
- Feature #67711 Network settings control via USB added
- Feature #67712 Network settings control via web added

* Thu Sep 01 2022 XIMC <info@ximc.ru> - 2.14.5
- version bump
- Feature #64745 Code blocks examples refactoring made

* Thu Aug 18 2022 XIMC <info@ximc.ru> - 2.14.4
- version bump
- Feature #67844 Fix warnings issued on GCC 11.2

* Fri Jun 24 2022 XIMC <info@ximc.ru> - 2.14.3
- version bump
- Feature #64133 Distribute enumerate feature on tcp-, udp- connected devices

* Mon Apr 18 2022 XIMC <info@ximc.ru> - 2.14.2
- version bump
- Feature #50500 Organize the addition of UDP support to libximc
- Feature #58865 Bring XIMC network management with built-in Ethernet
- Feature #59871 Bring Windows 11 support to official status
- Bug #62093 The build on Jenkins does not work

* Wed Jan 26 2022 XIMC <info@ximc.ru> - 2.14.1
- version bump
- Feature #53786 Control of adding UDP support to libximc
- Feature #59317 Add tcp support to libximc

* Tue Dec 28 2021 XIMC <info@ximc.ru> - 2.14.0
- version bump
- Feature #54792 Change the description of the flags in the protocol
- Feature #56922 Add UDP support to libximc

* Mon Nov 29 2021 XIMC <info@ximc.ru> - 2.13.3
- version bump
- Feature #51788 Clean up the Bindy branches
- Bug #51208 Make examples on linux working
- Bug #51557 Fix the description of the BITS flag group
- Bug #52853 Fix comments on our matlab examples
- Bug #54266 Jenkins assembly on Cubieboard broke
- Bug #54677 The old driver gets into the archives with the library
- Bug #55439 The local libximc build from the GIT repository does not work
- Bug #55638 Fix the description of the "reset_locks" function
- Bug #55735 The Java example from the libximc library is not going to

* Wed Sep 08 2021 XIMC <info@ximc.ru> - 2.13.2
- version bump
- Bug #51208 Make the examples on linux working
- Bug #51557 Fix the description of the BITS flag group
- Feature #48562 Specify that libximc is thread-safe
- Feature #51971 Running examples out of the box for linux
- Feature #53139 Add unpacked libraries to the linux build

* Mon May 24 2021 XIMC <info@ximc.ru> - 2.13.1
- version bump
- Feature #46853 Try to fix the Python 3.9 examples on Win10
- Feature #49922 The python profile didn't include the wiring diagram

* Wed Mar 31 2021 XIMC <info@ximc.ru> - 2.13.0
- version bump
- Feature #48565 Implement compatibility of our examples for python 3.9
- Bug #47662 Fix typos in the libximc manual
- Bug #48141 Remove Makefile. mingw from testapp and testappeasy
- Bug #48266 Fix errors in the examples
- Bug #48272 Fix the header in the profile generator to work under Mac OS
- Bug #48582 Migrate Bindy socket leak fix to libximc
- Feature #46853 Try to fix the Python 3.9 examples on Win10
- Feature #47464 Rename the examples and add dependencies for labwindows
- Feature #48562 Specify on the main page libximc-thread-safe
- Feature #48564 Processing a missing library msvc120.dll/msvcp120.dll

* Mon Mar 22 2021 XIMC <info@ximc.ru> - 2.12.10
- version bump
- Feature #47473 Refine it testpythonprofile and fix the folder structure

* Tue Mar 02 2021 XIMC <info@ximc.ru> - 2.12.8
- version bump
- Feature #46939 Add dependencies to the collected libximc examples
- Feature #43812 Make a python profile
- Feature #42920 In bindi, make enumerate with the network adapter
- Feature #42234 To update the examples and the site
- Bug #46049 Rename the loader_correction_table function

* Wed Feb 10 2021 XIMC <info@ximc.ru> - 2.12.7
- version bump
- Feature #44374 Add an example on labwindows to the libximc library
- Feature #19483 Unified COM device addressing scheme
- Feature #42234 To update the examples and the site
- Feature #42275 Make a readme for our examples

* Fri Jan 22 2021 XIMC <info@ximc.ru> - 2.12.6
- version bump
- Bug #42246 Release a new version of bindi
- Bug #42286 In the SSNO and GSNO commands with ASIA
- Bug #42738 Fix the device_id parameter in the load_correction_table
- Feature #36618 Update the data types for the firmware in the xigen
- Feature #42234 Update examples and site
- Feature #42920 In bindi, make an enumerate with the address of network

* Tue Oct 20 2020 XIMC <info@ximc.ru> - 2.12.5
- version bump
- Feature #41682 added flag indicating that the speed is entered in mili rpm
- Bug #41221 remove the mention of detecting the motor connection
- Feature #40845 improved the extended Python example
- Feature #42275 added a description file for the extended example

* Mon Aug 17 2020 XIMC <info@ximc.ru> - 2.12.4
- version bump
- Bug #33899 Changing the Protocol description
- Bug #40925 command "command_add_sync_in_action" set private
- command "command_change_motor" delete

* Thu Jul 23 2020 XIMC <info@ximc.ru> - 2.12.2
- version bump
- Bug #28005: Add a file check to set_bindy_key
- Deploying libximc on Github
- Feature #40580: Added a detailed Python example

* Thu Mar 19 2020 XIMC <info@ximc.ru> - 2.12.1
- version bump
- Changed the Protocol version to 20.1

* Sun Dec 15 2019 XIMC <info@ximc.ru> - 2.12.0
- version bump
- Feature #35244: License changed to BSD 2-Clause
- Updated version of the Protocol
- Feature #36920: Create 2 new configuration structures in libximc

* Fri Sep 06 2019 XIMC <info@ximc.ru> - 2.11.4
- version bump
- Added processing of increments for the correction table.
- Added a description to the documentation for correction table.

* Fri Jul 05 2019 XIMC <info@ximc.ru> - 2.11.3
- version bump
- Feature #31347 Modification testapp
- Bug #31495 Fix the library

* Thu Jun 27 2019 XIMC <info@ximc.ru> - 2.11.2
- version bump
- Feature #29076: Adding a calibration table

* Thu Jun 06 2019 XIMC <info@ximc.ru> - 2.11.1
- version bump
- Feature #27133: Make flags for all alarms

* Mon May 20 2019 XIMC <info@ximc.ru> - 2.11.0
- version bump
- feature #26953: Encoder mediated flag added, documentation updates

* Fri Jun 08 2018 XIMC <info@ximc.ru> - 2.10.5
- version bump
- merge with 2.9
- fix codeblocks example, build codeblocks on Jenkins

* Thu Mar 01 2018 XIMC <info@ximc.ru> - 2.10.4
- version bump
- merge with 2.9

* Wed Sep 27 2017 XIMC <info@ximc.ru> - 2.10.3
- version bump
- add c-profiles
- Feature #8871
- get\start measurements command in protocol
- new protocol version

* Thu Aug 17 2017 XIMC <info@ximc.ru> - 2.10.2
- version bump

* Wed Jun 21 2017 XIMC <info@ximc.ru> - 2.10.1
- version bump
- feature #17319: Protocol 18.1 support


* Thu Jun 15 2017 XIMC <info@ximc.ru> - 2.10.0
- version bump
- feature #17221: Protocol 18.0 support

* Thu Mar 09 2017 XIMC <info@ximc.ru> - 2.9.8
- version bump
- feature #15152: New motor status flags added

* Tue Feb 21 2017 XIMC <info@ximc.ru> - 2.9.7
- version bump
- bug #15050: Updated cryptopp to cmake bindy build

* Wed Feb 15 2017 XIMC <info@ximc.ru> - 2.9.6
- version bump
- bug #14953: Hang or segfault in enumerate

* Thu Feb 02 2017 XIMC <info@ximc.ru> - 2.9.5
- version bump
- fixed bindy keyfile compatibility

* Thu Dec 15 2016 XIMC <info@ximc.ru> - 2.9.4
- version bump

* Thu Nov 17 2016 XIMC <info@ximc.ru> - 2.9.3
- version bump
- feature #13036: Protocol 17.2 support

* Mon Mar 28 2016 XIMC <info@ximc.ru> - 2.8.8
- version bump
- feature #9963: Option to enter Alarm on ExtIO
- feature #9968: Protocol 16.11 support

* Thu Feb 18 2016 XIMC <info@ximc.ru> - 2.9.2
- version bump
- feature #9423: added support for GNVM/SNVM in virtual controllers

* Thu Jan 28 2016 XIMC <info@ximc.ru> - 2.9.1
- version bump
- updated libximc to use bindy-sqlite

* Wed Dec 16 2015 XIMC <info@ximc.ru> - 2.8.7
- version bump
- bug #8651: Disconnect recovery

* Thu Dec 10 2015 XIMC <info@ximc.ru> - 2.9.0
- version bump
- bug #8651: Disconnect recovery
- bug #8714: Memory leak in open_device
- bug #8731: Memory leak on virtual controller open

* Mon Nov 02 2015 XIMC <info@ximc.ru> - 2.8.6
- version bump
- bug #7812: Doxygen java documentation
- bug #7813: Supported examples documentation
- bug #8275: Fixed broadcast discovery on MacOS
- bug #8571: Device discovery on OS X 10.11

* Tue Sep 29 2015 XIMC <info@ximc.ru> - 2.8.5
- version bump
- feature #6766: Labview simple example added
- feature #7778: Python support
- feature #8123: Disabled SSE to support very old CPUs
- bug #8275: Fixed broadcast discovery on Linux

* Wed Aug 19 2015 XIMC <info@ximc.ru> - 2.8.4
- version bump
- feature #6204: Added wait_for_stop function

* Mon Aug 17 2015 XIMC <info@ximc.ru> - 2.8.3
- version bump
- feature #7971: Network enumerate obeys library timeouts now

* Thu Jul 30 2015 XIMC <info@ximc.ru> - 2.8.2
- version bump
- feature #7971: Added multithreaded multiserver network enumerate

* Thu Jul 09 2015 XIMC <info@ximc.ru> - 2.8.1
- version bump
- feature #7017: Added broadcast discovery option for network controllers

* Thu Jun 04 2015 XIMC <info@ximc.ru> - 2.8.0
- version bump

* Mon Jun 01 2015 XIMC <info@ximc.ru> - 2.7.8
- version bump
- bug #7694: fix libximc memory allocation error

* Wed May 27 2015 XIMC <info@ximc.ru> - 2.7.7
- version bump
- feature #7024: fixed bindy (network controllers)

* Thu May 14 2015 XIMC <info@ximc.ru> - 2.7.6
- version bump
- feature #4863: virtual controllers
- feature #7292: binary version changed to 7

* Tue Apr 28 2015 XIMC <info@ximc.ru> - 2.7.5
- version bump

* Thu Apr 23 2015 XIMC <info@ximc.ru> - 2.7.4
- version bump
- feature #7015: transition to ximc network protocol v1

* Tue Apr 07 2015 XIMC <info@ximc.ru> - 2.7.3
- version bump
- feature #6737: File logging option added
- feature #7224: fwprotocol generator updated
- bug #7085: get_controller_name() call caused Access Violation

* Tue Mar 17 2015 XIMC <info@ximc.ru> - 2.7.2
- version bump
- feature #6738: API changes

* Wed Feb 25 2015 XIMC <info@ximc.ru> - 2.7.1
- version bump
- bug #6253: Matlab example fixed

* Fri Feb 13 2015 XIMC <info@ximc.ru> - 2.7.0
- version bump
- feature #6006: Bindy support
- bug #6735: Buffering inside libximc

* Tue Feb 10 2015 XIMC <info@ximc.ru> - 2.5.1
- version bump

* Tue Sep 02 2014 XIMC <info@ximc.ru> - 2.3.2
- version bump
- bug #5691: C# protected memory exception, revised

* Thu Aug 28 2014 XIMC <info@ximc.ru> - 2.3.1
- version bump
- bug #5691: C# protected memory exception

* Mon May 26 2014 XIMC <info@ximc.ru> - 2.5.0
- version bump
- bug #4624: Profile section deduplication
- feature #4730: Protocol 16.8 support

* Mon Mar 24 2014 XIMC <info@ximc.ru> - 2.4.0
- version bump
- bug #4323: Change ASIA command structure
- feature #4687: Add DBGW command

* Mon Jan 27 2014 XIMC <info@ximc.ru> - 2.3.0
- version bump
- feature #3508: Multithreading

* Fri Nov 29 2013 XIMC <info@ximc.ru> - 2.2.2
- version bump
- bug #4220: Support 64-bit types for LabVIEW

* Tue Nov 19 2013 XIMC <info@ximc.ru> - 2.2.1
- version bump
- bug #4143: Fixed synchronization function

* Sat Nov 02 2013 XIMC <info@ximc.ru> - 2.2.0
- version bump
- bug #2953: java generator support
- feature #4010: profile assembler update

* Thu Oct 17 2013 XIMC <info@ximc.ru> - 2.1.1
- version bump
- bug #3988: Fix typing errors

* Tue Oct 15 2013 XIMC <info@ximc.ru> - 2.1.0
- version bump
- bug #3959: _impl in wiki doc
- bug #3610: Calibrations for CSharp and Delphi
- bug #3573: Readibility of libximc doc
- bug #3318: Bugs with virtual macosx
- bug #2956: Build with build.sh / build-ci from different branches
- bug #2918: No links to flags from function docs
- feature #3446: Examples of calibrated functions usage

* Tue Sep 24 2013 XIMC <info@ximc.ru> - 2.0.9
- version bump
- feature #3785: Merged with protocol 16.4

* Fri Sep 20 2013 XIMC <info@ximc.ru> - 2.0.8
- version bump
- bug #3610: Calibration for c#, delphi wrappers
- feature #3499: Documentation with new block tags

* Thu Aug 15 2013 XIMC <info@ximc.ru> - 2.0.7
- version bump
- bug #3514: libximc is built differently
- feature #3497: Calibrated commands without microstep
- feature #3498: Arrays as calibrated fields
- feature #3501: Calibrated fields of velocities

* Wed Aug 07 2013 XIMC <info@ximc.ru> - 2.0.6
- version bump
- bug #3959: _impl in wiki doc
bug #3610: Calibrations for CSharp and Delphi
bug #3573: Readibility of libximc doc
feature #3446: Examples of calibrated functions usage
bug #3318: Bugs with virtual macosx
bug #2956: Build with build.sh / build-ci from different branches
bug #2918: No links to flags from function docs

* Wed Jul 17 2013 XIMC <info@ximc.ru> - 2.0.5
- version bump
- bug #3347: Firmware structs contains calibrated values
- feature #3022: Calibration to units
- feature #3286: Markers of documentation

* Sat Jun 22 2013 XIMC <info@ximc.ru> - 2.0.4
- version bump
- bug #3132: DEBUG_TRACE causes buffer overflow
- bug #1567: Hangs on start (on port query)
- bug #2722: Library 2.00 on linux
- feature #2937: Fix examples
- feature #2999: Virtual controllers support
- feature #2786: Open devices by serial number
- feature #2936: Rewrite examples
- feature #2934: Test flashing on Linux

* Sun May 19 2013 XIMC <info@ximc.ru> - 2.0.3
- version bump
- bug #1566: Connection loss after a hour of work
- feature #2786: Open devices by serial number

* Mon May 06 2013 XIMC <info@ximc.ru> - 2.0.2
- version bump

* Thu May 02 2013 XIMC <info@ximc.ru> - 2.0.1
- version bump
- feature #2275: Make a QScript generator
- feature #2450: Support ERRV answers
- feature #2842: Support 64-bit numbers in protocol

* Sun Mar 17 2013 XIMC <info@ximc.ru> - 2.0.0
- version bump
- bug #1566: Connection loss after a hour of work
- bug #1865: Formatting of doxygen pdf
- bug #2254: Windows example does not work
- bug #2465: Wiki autogen eats last dot
- bug #2573: Flashing works incorretly
- bug #2593: ximc.h is built differently
- feature #1708: Bootrstrap a build inftrastructure for libximc
- feature #1740: Generate wiki protocol by the protocol.xi
- feature #1903: Prettify doxygen
- feature #2255: Arguments of get_device_count() and get_device_name()
- feature #2275: Make an autogen for QScript
- feature #2284: Change a protocol and a library for the new bootloader
- feature #2450: Support of errv answers
- feature #2464: Wiki generator can not wrap strings
- feature #2476: Update wrappers for .net, delphi
- feature #2524: SSER should pass a large key
- feature #2543: Add a flt64 type to the protocol.xi
- feature #2546: Refactor service commands
- support #2470: Fix bootloading

* Sun Dec 30 2012 XIMC <info@ximc.ru> - 1.7.1
- version bump
- bug #1587: Device connection opens port four times and does not send init
- bug #1744: Russian languages in logs
- bug #1908: Strange behaviour of close_device
- bug #1974: Binary packaging on FreeBSD
- bug #2015: Unable to open device on the slow port
- bug #2179: Type mismatch in protocol.xi
- feature #1642: FreeBSD support
- feature #1904: Reboot of hanged usbser.sys (windows-only)
- feature #2180: Write PID to the log

* Tue Dec 18 2012 XIMC <info@ximc.ru> - 1.7.0
- version bump
- bug #2082: Deny multiple port open in OSX
- bug #2091: Trim endlines in log

* Wed Oct 10 2012 XIMC <info@ximc.ru> - 1.6.9
- version bump

* Fri Oct 05 2012 XIMC <info@ximc.ru> - 1.6.8
- version bump
- bug #1683: Library hangs with the hanged controller
- bug #1425: Problem with port opening in has_firmware
- feature #1409: Library adaptation for langs like LabVIEW
- bug #1242: Mac examples does not work
- feature #500: Update doxygen docs
- feature #1559: Update main doc description
- bug #1865: Doxygen PDFs
- feature #1867: Debian hardening support

* Wed Aug 01 2012 XIMC <info@ximc.ru> - 1.6.7
- version bump
- bug #1697: Port loss returns result_error
- bug #1691: save command sends wrong zero bytes
- bug #1685: Null cleanup works incorrect
- bug #1642: freebsd support

* Tue Jul 31 2012 XIMC <info@ximc.ru> - 1.6.6
- version bump

* Wed Jul 25 2012 XIMC <info@ximc.ru> - 1.6.5
- version bump
- bug #1447: Windows x64 build issue
- bug #1584: Add doxygen documentation for new functions
- bug #1604: Wrong GETS answer in ALARM
- feature #1247: XISM detetction
- feature #1641: Get library version string
- feature #500: Update doxygen documentation

* Fri Jun 22 2012 XIMC <info@ximc.ru> - 1.6.4
- version bump

* Wed Jun 13 2012 XIMC <info@ximc.ru> - 1.6.3
- version bump
- bug #1425: has_firmware port opening problem
- feature #1422: Protocol 15.0 support
- feature #1419: New synchronization protocol support
- feature #1409: Library adaptation for languages such as LabVIEW
- feature #1398: Correct errc and errd handling
- feature #1281: Protocol 14.4 support
- feature #1265: Logging to an user callback

* Wed May 16 2012 XIMC <info@ximc.ru> - 1.6.2
- Version bump
- bug #1345: 1.60 bugs - missing functions
- bug #1346: 1.60 bugs - problems with commands

* Sat May 12 2012 XIMC <info@ximc.ru> - 1.6.1
- Version bump
- bug #1344: 1.60 bugs - mistypes
- bug #1345: 1.60 bugs - missing functions
- bug #1346: 1.60 bugs - problems with commands
- feature #1347: Static commands constraints check

* Sat May 05 2012 XIMC <info@ximc.ru> - 1.6.0
- Version 1.6.0
- major API break
- feature #966: Automatic library generator based on protocol definition file

* Thu Apr 26 2012 XIMC <info@ximc.ru> - 1.5.9
- Version 1.5.9
- bug #1205: POWER_OFF_MODE is not introduced in ximc.h
- bug #1242: Mac example does not work
- feature #798: device_t value after close_device(device_t) call
- feature #1021: Implement a synchronization between controller and computer based on flushing zeroes method
- feature #1022: Protocol 14.1 support
- feature #1029: Improvements in command_update_firmware
- feature #1097: Protocol 14.2 support
- feature #1100: Bring back function open_raw_device()
- feature #1247: xism devices detection

* Tue Feb 21 2012 XIMC <info@ximc.ru> - 1.5.8
- Version 1.5.8
- Beta build 3

* Tue Feb 21 2012 XIMC <info@ximc.ru> - 1.5.7
- Version 1.5.7
- Beta build 2

* Sun Feb 19 2012 XIMC <info@ximc.ru> - 1.5.6
- Version 1.5.6
- Beta build 1

* Sat Oct 01 2011 XIMC <info@ximc.ru> - 1.5.5
- Version 1.5.5
- Fix for the UART problem with some XISM controllers

* Fri Sep 30 2011 XIMC <info@ximc.ru> - 1.5.4
- Version 1.5.4
- bug #426: [macos] Simultaneously work with 2 devices
- feature #784: Update commands GETS, GSEC, SSEC
- feature #809: Add positioner name

* Sat Aug 20 2011 XIMC <info@ximc.ru> - 1.5.3
- Version 1.5.3
- bug #655: enumerate_devices returns -1 if no devices found
- feature #255: Loader timeouts
- bug #561: enumerate_devices() problem with char ***names
- feature #649: new command_update_firmware

* Fri Jun 17 2011 XIMC <info@ximc.ru> - 1.5.2
- Version 1.5.2
- bug #625: Problem with timeouts
- feature #561: enumerate_devices() problem with char ***names
- feature #611: New commands in the v12.4

* Thu Jun 09 2011 XIMC <info@ximc.ru> - 1.5.1
- Version 1.5.1
- bug #426: [macos] Simultaneously work with 2 devices
- bug #539: Unable to open device in the ALARM state
- feature #241: Limits of all parameters
- feature #255: Loader timeouts
- feature #561: enumerate_devices() problem with char ***names
- feature #611: New commands in the v12.4

* Wed Mar 09 2011 XIMC <info@ximc.ru> - 1.5.0
- Version 1.5.0
- feature #477: Protocol v12.4 support
- feature #478: Example for С
- feature #479: Example for Matlab
- feature #499: Rename lib to libximc from libxidcusb

* Sun Dec 26 2010 XIMC <info@ximc.ru> - 1.4.1
- Version 1.4.1
- feature #425: linux version doesn't query ttyACM ttys

* Wed Nov 24 2010 XIMC <info@ximc.ru> - 1.4.0
- Version 1.4.0
- feature #358: Protocol v12 support

* Sat Oct 16 2010 XIMC <info@ximc.ru> - 1.3.0
- Version 1.3.0
- feature #94: Visual Basic support

* Wed Sep 29 2010 XIMC <info@ximc.ru> - 1.2.0
- Version 1.2.0
- bug #286: hang while accessing two different devices

* Fri Apr 02 2010 XIMC <info@ximc.ru> - 1.1.1
- Version 1.1.1
- bug #267: firmware update doesn't work
- feature #264: development kit

* Fri Feb 19 2010 XIMC <info@ximc.ru> - 1.1.0
- Version 1.1.0
- bug #34: COM port
- bug #258: uint8_t, uint32_t
- feature #125: device detection protocol
- feature #226: linux device detection
- feature #237: update documentation
- feature #261: change commands S005, G005

* Sun Dec 12 2009 XIMC <info@ximc.ru> - 1.0.0
- Version 1.0.0
- bug #215: check crc at answers
- feature #91: How to use with C#
- feature #92: How to use with C++ Builder
- feature #93: How to use with Delphi
- feature #173: new command G1

* Sat Aug 15 2009 XIMC <info@ximc.ru> - 0.9.0
- Version 0.9.0
- Bug #24: Bugs with access from two applications
- Bug #56: Wrong data in cdc_pwmlevel
- Bug #76: Misspell in settings_t::flags
- Feature #27: Performance problems
- Feature #98: Documentation update
- Feature #99: Test program update

* Thu Jul 23 2009 XIMC <info@ximc.ru> - 0.8.0
- Version 0.8.0
- Bug #11: Support DLL building with DEF-files
- Bug #41: TTL_SETUP_OUTSET can't be unset
- Bug #42: ENGINE_LIMIT_CURR, ENGINE_LIMIT_VOLT
- Bug #54: open_device() returns -1 on second open, win32
- Feature #21: MinGW support

* Wed Jul 08 2009 XIMC <info@ximc.ru> - 0.7.0
- Version 0.7.0
- Feature #39: Add firmware upload
- Bug #33: Flags TTL_SYNCIN_SINGLE_SHIFT и TTL_SYNCIN_MULTI_SHIFT
- Bug #35: write_key
- Bug #36: get_analog_data

* Tue Jun 30 2009 XIMC <info@ximc.ru> - 0.6.0
- Version 0.6.0
- Bug #12: Опечатка в названиях полей структуры pid_settings_t: kprpm, kiPRM, kdPRM
- Bug #13: Ошибка в функции set_pwm_freq
- Bug #14: Ошибка инициализации
- Bug #16: Ошибка в записи параметров синхронизации
- Bug #17: Ошибка в параметре синхронизации TTL_SETUP_FRONT
- Bug #25: Не считываются калибровочные коэффициенты
- Feature #32: To do

* Thu May 21 2009 XIMC <info@ximc.ru> - 0.5.0
- Version 0.5.0
- Updated documentation
- Fix memory problem
- Improve compatibility with C++ on windows

* Wed May 06 2009 XIMC <info@ximc.ru> - 0.4.0
- Version 0.4.0
- Added documentation

* Sat Apr 04 2009 XIMC <info@ximc.ru>
- Added deb and rpm packages building
- Mac OS X library is private framework now
- Add version numbers in win32 version

* Thu Apr 02 2009 XIMC <info@ximc.ru>
- Initial release. Basic functionality.

