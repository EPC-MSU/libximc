Eng.
To use the libximc library, the example uses a wrapper module /ximc/crossplatform/wrappers/python/libximc.
You need Python2 or Python3 installed. Python version 3.9 IS NOT SUPPORTED!

For run:
Configuring dependencies:
 * On OS X: 
	-	before running the example, install the dependencies from requirements.txt . To do this, open terminal in the
		directory with the example and run the command: python -m pip install -r requirements.txt
	-	install getch. To do this, run: python -m pip install getch
   To run the example, you can go two ways:
	1.	run Extendtestpython.sh
	2.
		*	install packages from the /ximc/deb archive folder: libximc7_x.x.x and libximc7-dev_x.x.x. Install strictly
			in the specified order!
		*	you will also need to set LD_LIBRARY_PATH to let Python find libraries. For that use:
				# specify the correct path for installed packages.
				export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:usr/lib
		*	install the dependencies from requirements.txt. To do this, open terminal in the directory with the example
			and	run the command: python -m pip install -r requirements.txt
		* 	run the example with the command: python Extendtestpython.py

 
 * On Linux:
   To run the example, you can go two ways:
	1.	run Extendtestpython.sh
	2.
		*	install packages from the /ximc/deb archive folder: libximc7_x.x.x and libximc7-dev_x.x.x. Install strictly
			in the specified order.
		*	Set LD_LIBRARY_PATH to let Python find libraries using PATH. For that use:
				# specify the correct path for installed packages.
				export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:usr/lib
		*	install the dependencies from requirements.txt. To do this, open terminal in the directory with the example
			and	run the command: python -m pip install -r requirements.txt
		*	run the example with the command: python Extendtestpython.py
 
 * On Windows: 
	-	before running the example, install the dependencies from requirements.txt . To do this, on the command line in
		the directory with the example, run the command: python -m pip install -r requirements.txt
	-	run the example with the command: python Extendtestpython.py


For modify:
The example code can be modified in any text editor.
More detailed information about the example can be found in the file Readme_Extendtestpython.html.


Rus.
Для работы с библиотекой libximc в примере используется модуль-обёртка /ximc/crossplatform/wrappers/python/libximc.
Для запуска необходим установленный python 2 или 3 версии. Python версии 3.9 НЕ ПОДДЕРЖИВАЕТСЯ!
 
Для запуска примера:
 * В OS X: 
	-	перед запуском примера установите зависимости из requirements.txt. Для этого откройте терминал в директории с
		примером и выполните команду: python -m pip install -r requirements.txt
	-	установите getch. Для этого выполните: python -m pip install getch
   Для запуска примера можно пойти двумя путями:
	1.	запустить скрипт ./Extendtestpython.sh
	2.
		*	установить пакеты из папки /ximc/deb архива: libximc7_x.x.x и libximc7-dev_x.x.x. Устанавливать в указанном
			порядке! Так же потребуется установить LD_LIBRARY_PATH, чтобы Python мог находить библиотеки с помощью
			RPATH. Это можно сделать, Например, с помощью:
 				export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:usr/lib - указать правильный путь для установленных пакетов.
		*	установить зависимости из requirements.txt. Для этого в командой строке в директории с примером выполните команду:
				python -m pip install -r requirements.txt
		*	запустить пример командой: python Extendtestpython.py
 
 * В Linux:
   Для запуска примера можно пойти двумя путями:
	1. запустить скрипт ./Extendtestpython.sh
	2.
		*	установить пакеты, из папки /ximc/deb архива: libximc7_x.x.x и libximc7-dev_x.x.x. Устанавливать в указанном
			порядке! Установить LD_LIBRARY_PATH, чтобы Python мог находить библиотеки с помощью RPATH. Это можно сделать,
			Например, с помощью:
 				export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:usr/lib - указать правильный путь для установленных пакетов.
		*	установить зависимости из requirements.txt. Для этого в командой строке в директории с примером выполните команду:
				python -m pip install -r requirements.txt
		*	запустите пример командой: python Extendtestpython.py
 
 * В Windows:
	-	перед запуском примера установите зависимости из requirements.txt. Для этого в командой строке в директории с
		примером выполните команду:
 			python -m pip install -r requirements.txt
	-	запустите пример командой: python Extendtestpython.py

 
Для модификации примера:
Код примера можно модифицировать в любом текстовом редакторе.
Более подробную информацию о примере можно посмотреть в файле Readme_Extendtestpython.html.