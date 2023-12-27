/*!
 * \mainpage libximc library
 *
 * Documentation for libximc library.
 *
 * \image html 8SMC4.png
 * \image html 8SMC5.png
 *
 * Libximc is **thread safe**, cross-platform library for working with 8SMC4-USB and 8SMC5-USB controllers.
 *
 * Full documentation about controllers is <a href="https://doc.xisupport.com">there</a>
 *
 * Full documentation about libximc API is available on the page <a href="https://libximc.xisupport.com/doc-en/ximc_8h.html">ximc.h.</a>
 *
 * \section what_the_controller_does What the controller does
 *
 * - Supports input and output synchronization signals to ensure the joint operation of multiple devices within a complex system ;.
 * - Works with all compact stepper motors with a winding current of up to 3 A, without feedback, as well as with stepper motors equipped with an encoder in the feedback circuit, including a linear encoder on the positioner.
 * - Manages controller using ready-made <a href="https://files.xisupport.com/Software.en.html#xilab">xilab software</a> or using examples which allow rapid development using C++, C#, .NET, Delphi, Visual Basic, Xcode, Python, Matlab, Java, LabWindows and LabVIEW.
 *
 * \section what_can_do_library What can do libximc library
 *
 * - Libximc manages controller using interfaces: USB 2.0, RS232 and Ethernet, also uses a common and proven virtual serial port interface, so you can work with motor control modules through this library under almost all operating systems, including Windows, Linux and MacOS X
 * - Libximc library supports plug/unplug on the fly. Each device can be controlled only by one program at once. <b>Multiple processes (programs) that control one device simultaneously are not allowed!</b>
 *
 * \warning
 * Libximc library opens the controller in exclusive access mode. Any controller opened with libximc (XiLab also uses this library) needs to be closed before it may be used by another process. So at first check that you have closed XILab or other software dealing with the controller before trying to reopen the controller.
 *
 * Please read the <a href="https://libximc.xisupport.com/doc-en/intro_sec.html">Introduction</a> to start work with library.
 *
 * To use libximc in your project please consult with <a href="https://libximc.xisupport.com/doc-en/howtouse_sec.html"> How to use with...</a>
 *
 * \section assistance Assistance
 *
 * Many thanks to everyone who sends us <a href="https://en.xisupport.com">errors</a> and <a href="mailto:8smc4@standa.lt">suggestions</a>. We appreciate your suggestions and try to make our product better!
 *
 * \page intro_sec Introduction
 *
 * \section about_sec About library
 *
 * This document contains all information about libximc library.
 * It utilizes well known virtual COM-port interface, so you can use it on Windows, Linux, MacOS X for Intel and Apple Silicon (via Rosetta 2) including 64-bit versions.
 * Multi-platform programming library supports plug/unplug on the fly. <br>
 * <b>Each device can be controlled only by one program at once. Multiple processes (programs) that control one device simultaneously are not allowed.</b>
 *
 * \subsection sysreq_usage Supported OS and environment requirements:
 * - MacOS X 10.6 or newer
 * - Windows 2000 or newer
 * - Linux debian-based. DEB package is built against Debian Squeeze 7
 * - Linux debian-based ARM. DEB package is built on Ubuntu 14.04
 * - Linux rpm-based. RPM is built against OpenSUSE 12
 *
 * Build requirements:
 * - Windows: Microsoft Visual C++ 2013 or newer, MATLAB, Code::Blocks, Delphi, Java, Python, cygwin with tar, bison, flex, curl, 7z mingw
 * - UNIX: gcc 4 or newer, gmake, doxygen, LaTeX, flex 2.5.30+, bison 2.3+, autotools (autoconf, autoheader, aclocal, automake, autoreconf, libtool)
 * - MacOS X: XCode 4 or newer, doxygen, mactex, autotools (autoconf, autoheader, aclocal, automake, autoreconf, libtool)
 *
 * \page building_sec How to rebuild library
 *
 * \section building_win Building on Windows
 *
 * Requirements: 64-bit windows (build script builds both architectures), cygwin (must be installed to a default path).
 *
 * Invoke a script:
 * \code
 * 	./build.bat
 * \endcode
 *
 * Grab packages from ./deb/win32 and ./deb/win64 
 *
 * To build debug version of the library set environment variable "DEBUG" to "true" before running the build script.
 *
 * \section building_unix_deb Building on debian-based linux systems
 * Requirement: 64-bit and 32-bit debian system, ubuntu
 * Typical set of packages: 
 * \code
 * 	sudo apt-get install build-essential make cmake curl git ruby1.9.1 autotools-dev automake autoconf libtool doxygen bison flex debhelper lintian texlive texlive-latex-extra texlive-latex texlive-fonts-extra texlive-lang-cyrillic java-1_7_0-openjdk java-1_7_0-openjdk-devel default-jre-headless default-jdk openjdk-6-jdk rpm-build rpm-devel rpmlint pkg-config check dh-autoreconf hardening-wrapper libfl-dev lsb-release 
 * \endcode
 *
 * For ARM cross-compiling install gcc-arm-linux-gnueabihf from your ARM toolchain.
 *
 * It's required to match library and host architecture: 32-bit library can be built only at 32-bit host,
 * 64-bit library - only at 64-bit host. ARM library is built with armhf cross-compiler gcc-arm-linux-gnueabihf.
 *
 * To build library and package invoke a script:
 * \code
 * 	./build.sh libdeb
 * \endcode
 * 
 * For ARM library replace 'libdeb' with 'libdebarm'.
 *
 * Grab packages from ./ximc/deb and locally installed binaries from ./dist/local.
 *
 * \section building_osx_generic Building on MacOS X
 *
 * To build and package a script invoke a script:
 * \code
 * 	./build.sh libosx
 * \endcode
 *
 * Built library (classical and framework), examples (classical and .app), documentation
 * are located at ./ximc/macosx, locally installed binaries from ./dist/local.
 *
 * \section building_unix Building on generic UNIX
 *
 * Generic version could be built with standard autotools.
 * \code
 * 	./build.sh lib
 * \endcode
 * Built files (library, headers, documentation) are installed to ./dist/local directory.
 * It is a generic developer build. Sometimes you need to specify additional parameters to
 * command line for your machine. Please look to following OS sections.
 *
 * \section building_unix_rpm Building on redhat-based linux systems
 * Requirement: 64-bit redhat-based system (Fedora, Red Hat, SUSE)
 * Typical set of packages: 
 * \code
 * 	sudo apt-get install build-essential make cmake curl git ruby1.9.1 autotools-dev automake autoconf libtool doxygen bison flex debhelper lintian texlive texlive-latex-extra texlive-latex texlive-fonts-extra texlive-lang-cyrillic java-1_7_0-openjdk java-1_7_0-openjdk-devel default-jre-headless default-jdk openjdk-6-jdk rpm-build rpm-devel rpmlint pkg-config check dh-autoreconf hardening-wrapper libfl-dev lsb-release 
 * \endcode
 *
 * It's possible to build both 32- and 64-bit libraries on 64-bit host system.
 * 64-bit library can't be built on 32-bit system.
 *
 * To build library and package invoke a script:
 * \code
 * 	./build.sh librpm
 * \endcode
 * 
 * Grab packages from ./ximc/rpm and locally installed binaries from ./dist/local.
 *
 * \section building_src Source code access
 * The source codes of the libximc library can be found on <a href="https://github.com/EPC-MSU/libximc">github</a>.
 *
 * \page howtouse_sec How to use with...
 *
 * To acquire the first skills of using the library, a simple testappeasy_C test application has been created. 
 * Languages other than C are supported using calls with conversion of arguments of the stdcall type.
 * A simple C test application is located in the 'examples/test_C' directory, a C# project is located in 'examples/test_CSharp',
 * on VB.NET - in 'examples/test_VBNET', for delphi 6 - in 'example/test_Delphi', for matlab - 'examples/test_MATLAB',
 * for Java - 'examples/test_Java', for Python - 'examples/test_Python', for LabWindows - 'examples/test_LabWindows'.
 * Libraries, header files and other necessary files are located in the directories 'ximc/win32', 'ximc/win64','ximc/macosx' and the like.
 * The developer kit also includes already compiled examples: testapp and testappeasy x32 and x64 bits for windows and only x64 bits for macOS X,
 * test_CSharp, test_VBNET, test_Delphi - only x32 bits, test_Java - cross-platform, test_MATLAB and test_Python do not require compilation,
 * test_LabWindows - 64-bit build is installed by default.
 *
 * \note
 * SDK requires Microsoft Visual C++ Redistributable Package (provided with SDK - vcredist_x86 or vcredist_x64)
 *
 * \note
 * On Linux both the libximc7_x.x.x and libximc7-dev_x.x.x target architecture in the specified order. For install packages, you can use the .deb command: dpkg -i filename.deb, where filename.deb is the name of the package (packages in Debian have the extension .deb). You must run dpkg with superuser privileges (root).
 *
 * \subsection howtouse_c_vcpp_sec Visual C++
 *
 * Testapp can be built using testapp.sln. 
 * Library must be compiled with MS Visual C++ too, mingw-library.
 * Make sure that Microsoft Visual C++ Redistributable Package is installed. 
 *
 * Open solution examples/testapp/testapp.sln, build and run from the IDE.
 * 
 * In case of the 8SMC4-USB-Eth1 Ethernet adapter usage it is necessary to set correct IP address of the Ethernet adapter in testapp.c file before build (see enumerate_hints variable).
 *
 * \subsection howtouse_c_codeblocks CodeBlocks
 *
 * Testappeasy_C and testapp_C can be built using testappeasy_C.cbp and testapp_C.cbp respectively.
 * Library must be compiled with MS Visual C++ too, mingw-library.
 * Make sure that Microsoft Visual C++ Redistributable Package is installed.  *
 *
 * Open solution examples/test_C/testappeasy_C/testappeasy_C/testappeasy_C.cbp or examples/test_C/testapp_C/testapp_C.cbp, build and run from the IDE.
 *
 * \subsection howtouse_c_mingw_sec MinGW
 *
 * MinGW is a port of GCC to win32 platform.
 * It's required to install MinGW package.
 *
 * MinGW-compiled testapp can be built with MS Visual C++ or mingw library.
 * \code
 * 	mingw32-make -f Makefile.mingw all
 * \endcode
 *
 * Then copy library libximc.dll to current directory and launch testapp.exe.
 *
 * In case of the 8Eth1 Ethernet adapter usage it is necessary to set correct IP address of the Ethernet adapter in testapp.c file before build (see enumerate_hints variable).
 * 
 * \subsection howtouse_c_bcb_sec C++ Builder
 *
 * First of all, you should create a library suitable for C++ Builder. <b>Visual C++ and Builder libraries are not compatible</b>
 * Invoke:
 * \code
 * 	implib libximc.lib libximc.def
 * \endcode
 *
 * Then compile test application:
 * \code
 * 	bcc32 -I..\..\ximc\win32 -L..\..\ximc\win32 -DWIN32 -DNDEBUG -D_WINDOWS testapp.c libximc.lib
 * \endcode
 *
 * In case of the 8Eth1 Ethernet adapter usage it is necessary to set correct IP address of the Ethernet adapter in testapp.c file before build (see enumerate_hints variable).
 * 
 * There is also an <a href="https://github.com/EPC-MSU/ximc_embarcaderro_builder_example">unsupported example</a> of using libximc in a C++ Builder project
 *
 * \subsection howtouse_c_xcode_sec XCode
 *
 * testapp should be built with XCode project testapp.xcodeproj. 
 * Library is a MacOS X framework, and at example application it's bundled inside testapp.app
 *
 * Then launch application testapp.app and check activity output in Console.app.
 * 
 * In case of the 8Eth1 Ethernet adapter usage it is necessary to set correct IP address of the Ethernet adapter in testapp.c file before build (see enumerate_hints variable).
 * There is also <a href="https://github.com/EPC-MSU/ximc_embarcaderro_builder_example">an example of using the libximc library</a> in a C++ Builder project, <b>but it is not supported</b>.
 *
 * \subsection howtouse_c_gcc_sec GCC
 *
 * Make sure that libximc (rpm or deb) is installed at your system.
 * Installation of package should be performed with a package manager of operating system.
 * On MacOS X a framework is provided.
 *
 * Note that user should belong to system group which allows access to a serial port (dip or serial, for example).
 *
 * Test application can be built with the installed library with the following script:
 * \code
 * 	make
 * \endcode
 *
 * In case of cross-compilation (target architecture differs from the current system architecture)
 * feed -m64 or -m32 flag to compiler. On MacOS X it's needed to use -arch flag instead to build an universal binary.
 * Please consult a compiler documentation.
 *
 * Then launch the application as:
 * \code
 * 	make run
 * \endcode
 *
 * Note: make run on MacOS X copies a library to the current directory.
 * If you want to use library from
 * the custom directory please be sure to specify LD_LIBRARY_PATH or DYLD_LIBRARY_PATH to
 * the directory with the library. 
 *
 * In case of the 8SMC4-USB-Eth1 Ethernet adapter usage it is necessary to set correct IP address of the Ethernet adapter in testapp.c file before build (see enumerate_hints variable).
 * 
 * \subsection howtouse_dotnet_sec .NET
 * 
 * Wrapper assembly for libximc.dll is ximc/winX/wrappers/csharp/ximcnet.dll.
 * It is provided with two different architectures. Tested on platforms .NET from 2.0 to 4.5.1
 *
 * Test .NET applications for Visual Studio 2013 is located at test_CSharp (for C#) and test_VBNET (for VB.NET) respectively.
 * Open solutions and build it.
 * 
 * In case of the 8SMC4-USB-Eth1 Ethernet adapter usage it is necessary to set correct IP address of the Ethernet adapter in testapp.cs or testapp.vb file (depending on programming language) before build (see enumerate_hints variable for C# or enum_hints variable for VB).
 *
 * \subsection howtouse_delphi_sec Delphi
 *
 * Wrapper for libximc.dll is a unit ximc/winX/wrappers/delphi/ximc.pas
 *
 * Console test application for is located at test_Delphi. Tested on Delphi 6 and only 32-bit version.
 *
 * Just compile, place .dll near the executable and run program.
 * 
 * In case of the 8Eth1 Ethernet adapter usage it is necessary to set correct IP address of the Ethernet adapter in test_Delphi.dpr file before build (see enum_hints variable).
 *
 * \subsection howtouse_java_sec Java
 *
 * How to run example on Linux. Go to to examples/test_Java/compiled-winX/ and run:
 * \code
 * 	java -cp /usr/share/java/libjximc.jar:test_Java.jar ru.ximc.TestJava
 * \endcode
 *
 * How to run example on Windows. Go to to examples/test_Java/compiled-winX/.
 * Then run:
 * \code
 * 	java -classpath libjximc.jar -classpath test_Java.jar ru.ximc.TestJava
 * \endcode
 
 * How to modify and recompile an example.
 * Go to to examples/test_Java/compiled. Sources are embedded in a test_Java.jar.
 * Extract them:
 * \code
 * 	jar xvf test_Java.jar ru META-INF
 * \endcode
 * Then rebuild sources:
 * \code
 * 	javac -classpath /usr/share/java/libjximc.jar -Xlint ru/ximc/TestJava.java
 * \endcode
 * or for Windows or MacOS X
 * \code
 * 	javac -classpath libjximc.jar -Xlint ru/ximc/TestJava.java
 * \endcode
 * Then build a jar:
 * \code
 * 	jar cmf META-INF/MANIFEST.MF test_Java.jar ru
 * \endcode
 * 
 * In case of the 8Eth1 Ethernet adapter usage it is necessary to set correct IP address of the Ethernet adapter in TestJava.java file before build (see ENUM_HINTS variable).
 *
 * \subsection howtouse_python_sec Python
 *
 * Change current directory to the examples/test_Python/xxxxtest.
 * NB: For libximc usage, the example uses the wrapper module ximc/crossplatform/wrappers/python/libximc.
 *
 * To run:
 * \code
 * python xxxx.py
 * \endcode
 * 
 * In case of the 8Eth1 Ethernet adapter usage, it's necessary to set correct IP address of the Ethernet adapter in test_Python.py file before launch (see enum_hints variable).
 *
 * \subsection howtouse_matlab_sec MATLAB
 *
 * Sample MATLAB program testximc.m is provided at the directory examples/test_MATLAB.
 * On windows copy ximc.h, libximc.dll, bindy.dll, xiwrapper.dll and contents of ximc/(win32,win64)/wrappers/matlab/ directory to the current directory.
 *
 * Before launch:
 *
 * On MacOS X: copy ximc/macosx/libximc.framework, ximc/macosx/wrappers/ximcm.h,
 * ximc/ximc.h to the directory examples/test_MATLAB. Install XCode compatible with Matlab.
 *
 * On Linux: install libximc*deb and libximc-dev*dev of target architecture.
 * Then copy ximc/macosx/wrappers/ximcm.h to the directory examples/matlab. Install gcc compatible with Matlab.
 *
 * For XCode and gcc version compatibility check document 
 * https://www.mathworks.com/content/dam/mathworks/mathworks-dot-com/support/sysreq/files/SystemRequirements-Release2014a_SupportedCompilers.pdf or similar.
 *
 * On Windows before the start nothing needs to be done
 *
 * Change current directory in the MATLAB to the examples/test_MATLAB.
 * Then launch in MATLAB prompt:
 * \code
 * testximc
 * \endcode
 *
 * In case of the 8Eth1 Ethernet adapter usage it is necessary to set correct IP address of the Ethernet adapter in testximc.m file before launch (see enum_hints variable).
 * 
 * \section howtouse_log Generic logging facility
 *
 * If you want to turn on file logging, you should run the program that uses libximc library with the "XILOG" environment variable set to desired file name.
 * This file will be opened for writing on the first log event and will be closed when the program which uses libximc terminates.
 * Data which is sent to/received from the controller is logged along with port open and close events.
 *
 * \section howtouse_perm Required permissions
 *
 * libximc generally does not require special permissions to work, it only needs read/write access to USB-serial ports on the system.
 * An exception to this rule is a Windows-only "fix_usbser_sys()" function - it needs elevation and will produce null result if run as a regular user.
 *
 * \section howtouse_cprofiles C-profiles
 * 
 * C-profiles are header files distributed with the libximc library. They enable one to set all controller settings for any of the supported stages with a single function call in a C/C++ program. <br>
 * You may see how to use C-profiles in the example directory "examples/test_C/testprofile_C".
 *
 * \section howtouse_pyprofiles Python-profiles
 *
 * Python-profiles are sets of configuration functions distributed with the libximc library. They allow to load the controller with settings of one of the supported stages using a single function call in a Python program. <br>
 * You may see how to use Python-profiles in the example "examples/test_Python/profiletest/testpythonprofile.py".
 *
 * \page userunit_sec Working with user units
 *
 * In addition to working in basic units(steps, encoder value), the library allows you to work with user units.
 * For this purpose are used: 
 * - The structure of the conversion units calibration_t
 * - The functions of which have doubles for working with user units, data structures for these functions
 * - Coordinate correction table for more accurate positioning
 * 
 * \section userunit_calb1 The structure of the conversion units calibration_t
 *
 * To specify conversion of the basic units in the user and back, calibration_t structure is used.
 * With the help of coefficients A and MicrostepMode, specified in this structure, steps and microsteps which are integers are converted into the user value of the real type and back.
 *
 * Conversion formulas:
 * - The conversion to user units.
 * \verbatim
	user_value = A*(step + mstep/pow(2,MicrostepMode-1))
	\endverbatim
 * - Conversion from user units.
 * \verbatim
	step = (int)(user_value/A)
	mstep = (user_value/A - step)*pow(2,MicrostepMode-1)
	\endverbatim
 *
 * \section userunit_calb2 Alternative functions for working with user units and data structures for them
 * Structures and functions for working with user units have the _calb postfix.
 * The user using these functions can perform all actions in their own units without worrying about the computations of the controller.
 * The data format of _calb structures is described in detail. For _calb functions particular descriptions are not used. They perform the same actions as the basic functions do.
 * The difference between them and the basic functions is in the position, velocity, and acceleration of the data types defined as user-defined. If clarification for _calb functions is necessary, they are provided as notes in the description of the basic functions.
 *
 * \section userunit_corr Coordinate correction table for more accurate positioning
 *
 * Some functions for working with user units support coordinate transformation using a correction table.
 * To load a table from a file, the load_correction_table() function is used. Its description contains the functions and their data supporting correction.
 *
 * \note
 * For data fields which are corrected in case of loading of the table in the description of the field is written - corrected by the table.
 *
 * File format: 
 * - two columns separated by tabs; 
 * - column headers are string; 
 * - real type data, point is a separator; 
 * - the first column is the coordinate, the second is the deviation caused by a mechanical error; 
 * - the deviation between coordinates is calculated linearly; 
 * - constant is equal to the deviation at the boundary beyond the range; 
 * - maximum length of the table is 100 lines.
 *
 * Sample file:
 * \verbatim
	X	dX
	0	0
	5.0	0.005
	10.0	-0.01
    \endverbatim
 *
 * 
 */
