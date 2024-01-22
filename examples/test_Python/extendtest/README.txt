Eng.
To use the libximc library, the example uses a wrapper module /ximc/crossplatform/wrappers/python/libximc.
You need Python3.6+ installed.

===== RUN =====
 * On Linux/MacOS:
   To run the example, you can go two ways:
	1.	run ./Extendtestpython.sh
	2.
		*	install packages from the /ximc/deb archive folder: libximc7_x.x.x and libximc7-dev_x.x.x. Install strictly
			in the specified order.
		*	Set LD_LIBRARY_PATH to let Python find libraries using PATH. For that use:
				# specify the correct path for installed packages.
				export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:usr/lib
		*	run the example with the command: python Extendtestpython.py
 
 * On Windows: 
	*	run the example with the command: python Extendtestpython.py


Rus.
Для работы с библиотекой libximc в примере используется модуль-обёртка /ximc/crossplatform/wrappers/python/libximc.
Для запуска необходим установленный python 2 или 3 версии. Python версии 3.9 НЕ ПОДДЕРЖИВАЕТСЯ!
 
===== ЗАПУСК =====
 * В Linux/MacOS:
   Для запуска примера можно пойти двумя путями:
	1.	запустить скрипт ./Extendtestpython.sh
	2.
		*	установить пакеты из папки /ximc/deb архива: libximc7_x.x.x и libximc7-dev_x.x.x. Устанавливать в указанном
			порядке! Так же потребуется установить LD_LIBRARY_PATH, чтобы Python мог находить библиотеки с помощью
			RPATH. Это можно сделать, например, с помощью:
 				export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:usr/lib - указать правильный путь для установленных пакетов.
		*	запустить пример командой: python Extendtestpython.py

  * В Windows:
	-	запустите пример командой: python Extendtestpython.py
