/*!
 * \mainpage Библиотека libximc
 *
 * Документация для библиотеки libximc.
 *
 * \image html 8SMC4.png
 * \image html 8SMC5.png
 *
 * Libximc - <b>потокобезопасная,</b> кросс-платформенная библиотека для работы с контроллерами 8SMC4-USB и 8SMC5-USB.
 *
 * Полная документация по контроллерам доступна по <a href="https://doc.xisupport.com">ссылке</a>
 *
 * Полная документация по API libximc доступна на странице <a href="https://libximc.xisupport.com/doc-ru/ximc_8h.html"> ximc.h.</a>
 * 
 * \section what_the_controller_does Что делает контроллер 8SMC4-USB и 8SMC5-USB
 *
 * - Поддерживает входные и выходные сигналы синхронизации для обеспечения совместной работы нескольких устройств в рамках сложной системы;
 * - Работает со всеми компактными шаговыми двигателями с током обмотки до 3 А, без обратной связи, а так же с шаговыми двигателями, оснащенными энкодером в цепи обратной связи, в том числе линейным энкодером на позиционере;
 * - Управляет контроллером с помощью готового ПО <a href="https://files.xisupport.com/Software.ru.html#xilab">XILab</a> или с помощью примеров, которые позволяют быстро начать программирование с использованием C++, C#, .NET, Delphi, Visual Basic, Xcode, Python, Matlab, Java, LabWindows и LabVIEW.
 *
 * \section what_can_do_library Что умеет библиотека libximc
 *
 * - Libximc управляет контроллером с использованием интерфейсов: USB 2.0, RS232 и Ethernet, также использует распространенный и проверенный интерфейс виртуального последовательного порта, поэтому вы можете работать с модулями управления моторами через эту библиотеку практически под всеми ОС, в том числе под Windows, Linux и Mac OS X. 
 * - Библиотека libximc поддерживает подключение и отключение устройств "на лету". C одним устройством в каждый момент может работать не более одного экземпляра управляющей программы - <b>множественный доступ управляющих программ к одному и тому же устройству не допускается!</b> 
 *
 * \warning
 * Библиотека открывает контроллер в режиме эксклюзивного доступа. Каждый контроллер, открытый библиотекой libximc (XiLab тоже использует эту библиотеку) должен быть закрыт, прежде чем может быть использован другим процессом. Поэтому прежде чем попытаться открыть контроллер заново, проверьте, что XILab или другое программное обеспечение, взаимодействующее с контроллером, закрыто.
 *
 * Пожалуйста, прочитайте <a href="https://libximc.xisupport.com/doc-ru/intro_sec.html">Введение</a> для начала работы с библиотекой.
 *
 * Для того, чтобы использовать libximc в проекте, ознакомьтесь со страницей <a href="https://libximc.xisupport.com/doc-ru/howtouse_sec.html">Как использовать с...</a>
 *
 * \section assistance Содействие
 *
 * Большое спасибо всем, кто отправляет нам <a href="https://en.xisupport.com">ошибки</a> и <a href="mailto:8smc4@standa.lt">предложения</a>. Мы ценим ваше время и стараемся сделать наш продукт лучше! 
 *
 * \page intro_sec Введение
 *
 * \section about_sec О библиотеке
 *
 * Этот документ содержит всю необходимую информацию о библиотеке libximc. 
 * Библиотека libximc использует распространенный и проверенный интерфейс виртуального последовательного порта, поэтому вы можете работать с модулями управления моторами через эту библиотеку практически под всеми ОС: Windows, Linux, MacOS X для Intel и Apple Silicon (с использованием Rosetta 2), в том числе с 64-битными версиями.
 * Библиотека поддерживает подключение и отключение устройств "на лету". <br>
 * <b>C одним устройством в каждый момент может работать не более одного экземпляра управляющей программы - множественный доступ управляющих программ к одному и тому же устройству не допускается!</b>
 *
 * \subsection sysreq_usage Поддерживаемые операционные системы и требования к окружению:
 *
 * - MacOS X 10.6 или новее
 * - Windows 2000 или новее
 * - Linux на основе debian. DEB собирается на Debian Squeeze 7
 * - Linux на основе debian ARM. DEB собирается кросс-компилятором на Ubuntu 14.04
 * - Linux на основе rpm. RPM собирается на OpenSUSE 12
 *
 * Требования сборки:
 * - Windows: Microsoft Visual C++ 2013 или новее, MATLAB, Code::Blocks, Delphi, Java, Python, cygwin с tar, bison, flex, curl, 7z. mingw
 * - UNIX: gcc 4 или новее, gmake, doxygen, LaTeX, flex 2.5.30+, bison 2.3+, autotools (autoconf, autoheader, aclocal, automake, autoreconf, libtool)
 * - Mac OS X: XCode 4 или новее, doxygen, mactex, autotools (autoconf, autoheader, aclocal, automake, autoreconf, libtool)
 * - JDK 7 - 9
 *
 * \page building_sec Как пересобрать библиотеку
 *
 * \section building_win Сборка для ОС Windows
 *
 * Требования: 64-битный windows (сборочный скрипт собирает обе архитектуры), cygwin (должен быть установлен в пути по умолчанию).
 * 
 * Запустите скрипт:
 * \code
 * $ ./build.bat
 * \endcode
 * 
 * Собранные файлы располагаются в ./ximc/win32 и ./ximc/win64
 *
 * Если вы хотите собрать отладочную версию библиотеки, то перед запуском скрипта сборки установите переменную окружения "DEBUG" в значение "true".
 *
 * \section building_unix_deb Сборка для Linux на основе Debian
 * Полный набор пакетов: 
 * \code
 * 	sudo apt-get install build-essential make cmake curl git ruby1.9.1 autotools-dev automake autoconf libtool doxygen bison flex debhelper lintian texlive texlive-latex-extra texlive-latex texlive-fonts-extra texlive-lang-cyrillic java-1_7_0-openjdk java-1_7_0-openjdk-devel default-jre-headless default-jdk openjdk-6-jdk rpm-build rpm-devel rpmlint pkg-config check dh-autoreconf hardening-wrapper libfl-dev lsb-release 
 * \endcode
 *
 * Для кросс-компиляции ARM установите gcc-arm-linux-gnueabihf из вашего инструментария ARM.
 *
 * Необходимо соблюдать парность архитектуры библиотеки и системы: 32-битная библиотека может быть собрана только на 32-битной системе,
 * а 64-битная - только на 64-битной. Библиотека под ARM собирается кросс-компилятором gcc-arm-linux-gnueabihf.
 *
 * Для сборки библиотеки и пакета запустите скрипт:
 * \code
 * 	./build.sh libdeb
 * \endcode
 * 
 * Для библиотеки ARM замените 'libdeb' на 'libdebarm'. <br>
 * Пакеты располагаются в ./ximc/deb, локально установленные файлы - в ./dist/local.
 *
 * \section building_osx_framework Сборка для MacOS X
 *
 * Для сборки библиотеки и пакета запустите скрипт:
 * \code
 * 	./build.sh libosx
 * \endcode
 *
 * Собранная библиотека (классическая и фреймворк), приложения (классическая и фреймворк) и документация
 * располагаются в ./ximc/macosx, локально установленные файлы - в ./dist/local.
 *
 * \section building_unix Сборка для UNIX
 *
 * Обобщенная версия собирается обычными autotools.
 * \code
 *   ./build.sh lib
 * \endcode
 * Собранные файлы (библиотека, заголовочные файлы, документация) устанавливаются в локальную директорию  ./dist/local.
 * Это сборка для разработчика, при необходимости можно указать дополнительные параметры командной строки для вашей системы.
 *
 * \section building_unix_rpm Сборка на Linux на основе RedHat
 * Требования: 64-битная система на основе redhat (Fedora, Red Hat, SUSE)
 *
 * Полный набор пакетов: 
 * \code
 * 	sudo apt-get install build-essential make cmake curl git ruby1.9.1 autotools-dev automake autoconf libtool doxygen bison flex debhelper lintian texlive texlive-latex-extra texlive-latex texlive-fonts-extra texlive-lang-cyrillic java-1_7_0-openjdk java-1_7_0-openjdk-devel default-jre-headless default-jdk openjdk-6-jdk rpm-build rpm-devel rpmlint pkg-config check dh-autoreconf hardening-wrapper libfl-dev lsb-release 
 * \endcode
 *
 * Возможно собрать 32-битную и 64-битную библиотеки на 64-битной системе, однако 64-битная
 * библиотека не может быть собрана на 32-битной системе.
 *
 * Для сборки библиотеки и пакета запустите скрипт:
 * \code
 * 	./build.sh librpm
 * \endcode
 * 
 * Пакеты располагаются в ./ximc/rpm, локально установленные файлы - в ./dist/local.
 *
 * \section building_src Доступ к исходным кодам
 * Исходные коды библиотеки libximc можно найти на <a href="https://github.com/EPC-MSU/libximc">github</a>.
 *
 * \page howtouse_sec Как использовать с...
 *
 * Для приобретения первых навыков использования библиотеки создано простое тестовое приложение testappeasy_C. <br>
 * Языки, отличные от C-подобных, поддерживаются с помощью вызовов с преобразованием аргументов типа stdcall.
 *
 * \note
 * Для работы с SDK требуется Microsoft Visual C++ Redistributable Package (поставляется с SDK, файлы vcredist_x86 или vcredist_x64).
 *
 * \note
 * Для работы на Linux требуется установить оба пакета libximc7_x.x.x и libximc7-dev_x.x.x целевой архитектуры в указанном порядке. Для установки пакетов можно воспользоваться .deb командой: 
 * \code
 * 	sudo dpkg -i <имя_пакета>.deb 
 * \endcode
 *
 * \subsection howtouse_c_vcpp_sec Visual C++
 *
 * Тестовое приложение может быть собрано с помощью testapp.sln. 
 * Для компиляции необходимо использовать также MS Visual C++, mingw-library. 
 * 
 * Убедитесь, что Microsoft Visual C++ Redistributable Package установлен.
 * Откройте проект examples/test_C/testapp_C/testapp.sln, выполните сборку и запустите приложение из среды разработки.
 * 
 * В случае, если планируется использовать Ethernet-адаптер 8Eth1, в файле testapp.c перед сборкой нужно прописать IP адрес Ethernet-адаптера (переменная enumerate_hints).
 *
 * \subsection howtouse_c_codeblocks CodeBlocks
 *
 * Тестовое приложение может быть собрано с помощью testappeasy_C.cbp или testapp_C.cbp.
 * Для компиляции необходимо использовать также MS Visual C++, mingw-library. 
 * 
 * Убедитесь, что Microsoft Visual C++ Redistributable Package установлен.
 * Откройте проект examples/test_C/testappeasy_C/testappeasy_C/testappeasy_C.cbp или examples/test_C/testapp_C/testapp_C.cbp, выполните сборку и запустите приложение из среды разработки.
 *
 * \subsection howtouse_c_mingw_sec MinGW
 *
 * MinGW это вариант GCC для платформы win32. Требует установки пакета MinGW.
 *
 * testapp, скомпилированный с помощью MinGW, может быть собран с MS Visual C++ или библиотеками mingw:
 * \code
 * 	mingw32-make -f Makefile.mingw all
 * \endcode
 *
 * Далее скопируйте libximc.dll в текущую директорию и запустите testapp.exe.
 * 
 * В случае, если планируется использовать Ethernet-адаптер 8Eth1, в файле testapp.c перед сборкой нужно прописать IP адрес Ethernet-адаптера (переменная enumerate_hints).
 *
 * \subsection howtouse_c_bcb_sec C++ Builder
 *
 * В первую очередь вы должны создать подходящую для C++ Builder библиотеку. <b>Библиотеки Visual C++ и Builder не совместимы</b>. 
 * Выполните: 
 * \code
 * 	implib libximc.lib libximc.def
 * \endcode
 *
 * Затем скомпилируйте тестовое приложение:
 * \code
 * 	bcc32 -I..\..\ximc\win32 -L..\..\ximc\win32 -DWIN32 -DNDEBUG -D_WINDOWS testapp.c libximc.lib
 * \endcode
 *
 * В случае, если планируется использовать Ethernet-адаптер 8Eth1, в файле testapp.c перед сборкой нужно прописать IP адрес Ethernet-адаптера (переменная enumerate_hints).
 * 
 * Также существует <a href="https://github.com/EPC-MSU/ximc_embarcaderro_builder_example">пример использования библиотеки libximc</a> в проекте С++ Builder, <b>но он не поддерживается</b>.
 *
 * \subsection howtouse_c_xcode_sec XCode
 *
 * testapp должен быть собран проектом XCode testapp.xcodeproj. Используйте конфигурацию Release.
 * Библиотека поставляется в формате MacOS X framework, в той же директории находится собранное тестовое приложение testapp.app.
 *
 * Запустите приложение testapp.app проверьте его работу в Console.app.
 * 
 * В случае, если планируется использовать Ethernet-адаптер 8Eth1, в файле testapp.c перед сборкой нужно прописать IP адрес Ethernet-адаптера (переменная enumerate_hints).
 *
 * \subsection howtouse_c_gcc_sec GCC
 *
 * Убедитесь, что libximc (с помощью rpm или deb) установлена на вашей системе. 
 * Пакеты должны устанавливаться с помощью package manager'а вашей ОС.
 * Для MacOS X предоставляется фреймворк.
 *
 * Убедитесь, что пользователь принадлежит к группе, позволяющей доступ к COM-порту (например, dip или serial).
 *
 * testapp может быть собран следующим образом с установленной библиотекой:
 * \code
 * 	make
 * \endcode
 *
 * Для кросс-компиляции (архитектура целевой системы отличается от архитектуры хоста) следует передать флаг -m64 или -m32
 * компилятору. Для сборки universal binary на MacOS X необходимо использовать вместо этого флаг -arch. 
 * Обратитесь к документации компилятора.
 *
 * Затем запустите приложение с помощью:
 * \code
 * 	make run
 * \endcode
 *
 * Примечание: make run на MacOS X копирует библиотеку в текущую директорию. 
 * Если вы хотите использовать библиотеку из другой директории, пожалуйста укажите в LD_LIBRARY_PATH или DYLD_LIBRARY_PATH 
 * путь к директории с библиотекой.
 *
 * В случае, если планируется использовать Ethernet-адаптер 8Eth1, в файле testapp.c перед сборкой нужно прописать IP адрес Ethernet-адаптера (переменная enumerate_hints).
 * 
 * \subsection howtouse_dotnet_sec .NET
 * 
 * Для использования в .NET предлагается обертка ximc/winX/wrappers/csharp/ximcnet.dll.
 * Она распространяется в двух различных архитектурах. Тестировалось на платформах .NET от 2.0 до 4.5.1.
 *
 * Тестовые приложения на языке C# для Visual Studio 2013 расположены в директориях test_CSharp (для C#) и test_VBNET (для VB.NET).
 * Откройте проекты и соберите их.
 * 
 * В случае, если планируется использовать Ethernet-адаптер 8Eth1, в файле testapp.cs или testapp.vb (в зависимости от языка) перед сборкой нужно прописать IP адрес Ethernet-адаптера (переменная enumerate_hints для C#, переменная enum_hints для VB).
 *
 * \subsection howtouse_delphi_sec Delphi
 *
 * Обертка для использования в Delphi libximc.dll предлагается как модуль ximc/winX/wrappers/pascal/ximc.pas
 *
 * Консольное тестовое приложение размещено в директории 'test_Delphi'. Тестировалось с Delphi 6 на 32-битной системе.
 *
 * Просто скомпилируйте, разместите .dll в директории с исполняемым примером и запустите его.
 *
 * В случае, если планируется использовать Ethernet-адаптер 8Eth1, в файле test_Delphi.dpr перед сборкой нужно прописать IP адрес Ethernet-адаптера (переменная enum_hints).
 * 
 * \subsection howtouse_java_sec Java
 *
 * Как запустить пример на Linux. Перейдите в examples/test_Java/compiled-winX/ и выполните
 * \code
 * 	java -cp /usr/share/java/libjximc.jar:test_Java.jar ru.ximc.TestJava
 * \endcode
 *
 * Как запустить пример на Windows. Перейдите в examples/test_Java/compiled-winX/.
 * Запустите:
 * \code
 * 	java -classpath libjximc.jar -classpath test_Java.jar ru.ximc.TestJava
 * \endcode
 *
 * Как модифицировать и пересобрать пример.
 * Исходный текст расположен внутри test_Java.jar. Перейдите в examples/test_Java/compiled.
 * Распакуйте jar:
 * \code
 * 	jar xvf test_Java.jar ru META-INF
 * \endcode
 * Затем пересоберите исходные тексты:
 * \code
 * 	javac -classpath /usr/share/java/libjximc.jar -Xlint ru/ximc/TestJava.java
 * \endcode
 * или для Windows или MacOS X:
 * \code
 * 	javac -classpath libjximc.jar -Xlint ru/ximc/TestJava.java
 * \endcode
 * Затем соберите jar:
 * \code
 * 	jar cmf MANIFEST.MF test_Java.jar ru
 * \endcode
 *
 * В случае, если планируется использовать Ethernet-адаптер 8Eth1, в файле TestJava.java перед сборкой нужно прописать IP адрес Ethernet-адаптера (переменная ENUM_HINTS).
 * 
 * \subsection howtouse_python_sec Python
 *
 * Измените текущую директорию на examples/test_Python/xxxxtest.
 * NB: Для работы с библиотекой libximc в примере используется модуль-обёртка ximc/crossplatform/wrappers/python/libximc.
 *
 * Для запуска:
 * \code
 * 	python xxxx.py
 * \endcode
 * 
 * В случае, если планируется использовать Ethernet-адаптер 8Eth1, в файле test_Python.py перед запуском нужно прописать IP адрес Ethernet-адаптера (переменная enum_hints).
 *
 * \subsection howtouse_matlab_sec MATLAB
 *
 * Тестовая программа на MATLAB testximc.m располагается в директории examples/test_MATLAB.
 *
 * Перед запуском:
 *
 * На MacOS X: скопируйте ximc/macosx/libximc.framework, ximc/macosx/wrappers/ximcm.h,
 * ximc/ximc.h в директорию examples/test_MATLAB. Установите XCode, совместимый с Matlab
 *
 * На Linux: установите libximc*deb и libximc-dev*deb нужной архитектуры.
 * Далее скопируйте ximc/macosx/wrappers/ximcm.h в директорию examples/matlab. Установите gcc, совместимый с Matlab.
 *
 * Для проверки совместимых XCode и gcc проверьте документы
 * https://www.mathworks.com/content/dam/mathworks/mathworks-dot-com/support/sysreq/files/SystemRequirements-Release2014a_SupportedCompilers.pdf или похожие.
 *
 * На Windows: перед запуском ничего делать не нужно
 *
 * Измените текущую директорию в MATLAB на examples/test_MATLAB.
 * Затем запустите в MATLAB:
 * \code
 * 	testximc
 * \endcode
 *
 * В случае, если планируется использовать Ethernet-адаптер 8Eth1, в файле testximc.m перед запуском нужно прописать IP адрес Ethernet-адаптера (переменная enum_hints).
 * 
 * \section howtouse_log Логирование в файл
 *
 * Если программа, использующая libximc, запущена с установленной переменной окружения XILOG, то это включит логирование в файл.
 * Значение переменной XILOG будет использовано как имя файла. Файл будет открыт на запись при первом событии лога и закрыт при завершении программы, использующей libximc.
 * В лог записываются события отправки данных в контроллер и приема данных из контроллера, а также открытия и закрытия порта.
 *
 * \section howtouse_perm Требуемые права доступа
 *
 * Библиотеке не требуются особые права для выполнения, но нужены права доступа на чтение-запись в USB-COM устройства в системе.
 * Исключением из этого правила является функция только для ОС Windows "fix_usbser_sys()" - если процесс использующий библиотеку
 * не имеет повышенных прав, то при вызове этой функции программная переустановка устройства не будет работать.
 *
 * \section howtouse_cprofiles Си-профили
 *
 * Си-профили это набор заголовочных файлов, распространяемых вместе с библиотекой libximc. Они позволяют в программе на языке C/C++ загрузить в контроллер настройки одной из поддерживаемых подвижек вызовом всего одной функции.
 * Пример использования си-профилей вы можете посмотреть в директории примеров "examples/test_C/testprofile_C".
 *
 * \section howtouse_pyprofiles Python-профили
 *
 * Python-профили - это набор конфигурационных функций, распространяемых вместе с библиотекой libximc. Они позволяют в программе на языке Python загрузить в контроллер настройки одной из поддерживаемых подвижек вызовом всего одной функции. <br>
 * Пример использования python-профилей вы можете посмотреть в директории примеров "examples/test_Python/profiletest/testpythonprofile.py".
 *
 * \page userunit_sec Работа с пользовательскими единицами
 *
 * Кроме работы в основных единицах(шагах, отчетах энкодера) библиотека позволяет работать с пользовательскими единицами. 
 * Для этого используются: 
 * - Cтруктура пересчета единиц calibration_t
 * - Функции дублеры для работы с пользовательскими единицами и структуры данных для них
 * - Таблица коррекции координат для более точного позиционирования
 *
 * \section userunit_calb1 Cтруктура пересчета единиц calibration_t
 *
 * Для задания пересчета из основных единиц в пользовательские и обратно используется структура calibration_t. 
 * С помощью коэффициентов A и MicrostepMode, заданных в этой структуре, происходит пересчет из шагов и микрошагов являющихся целыми числами в пользовательское значение действительного типа и обратно.
 *
 * Формулы пересчета:
 * - Пересчет в пользовательские единицы. 
 * \verbatim
	user_value = A*(step + mstep/pow(2,MicrostepMode-1))
	\endverbatim
 * - Пересчет из пользовательских единиц. 
 * \verbatim
	step = (int)(user_value/A)
	mstep = (user_value/A - step)*pow(2,MicrostepMode-1)
	\endverbatim
 *
 * \section userunit_calb2 Функции дублеры для работы с пользовательскими единицами и структуры данных для них
 *
 * Структуры и функции для работы с пользовательскими единицами имеют постфикc _calb. 
 * Пользователь используя данные функции может выполнять все действия в собственных единицах не беспокоясь о том, что и как считает контроллер.
 * Для _calb функций отдельных описаний нет. Они выполняют теже действия, что и базовые функции. 
 * Разница между ними и базовыми функциями в типах данных положения, скоростей и ускорений определенных как пользовательские. Если требуются уточнения для _calb функций они оформлены в виде примечаний в описании базовых функций.
 *
 * \section userunit_corr Таблица коррекции координат для более точного позиционирования
 *
 * Некоторые функции для работы с пользовательскими единицами поддерживают преобразование координат с использованием корректировочной таблицы.
 * Для загрузки таблицы из файла используется функция load_correction_table(). В ее описании описаны функции и их данные поддерживающие коррекцию движения.
 *
 * \note
 * Для полей данных которые корректируются в случае загрузки таблицы в описании поля записано - корректируется таблицей.
 *
 * Формат файла: 
 * - два столбца разделенных табуляцией; 
 * - заголовки столбцов строковые; 
 * - данные действительные, разделитель - точка; 
 * - первый столбец координата, второй - отклонение вызванное ошибкой механики; 
 * - между координатами отклонение расчитывается линейно; 
 * - за диапазоном - константа равная отклонению на границе; 
 * - максимальная длина таблицы 100 строк.
 *
 * Пример файла:
 * \verbatim
	X	dX
	0	0
	5.0	0.005
	10.0	-0.01
    \endverbatim
 * 
 *
 */
