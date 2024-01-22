Eng.

This example demonstrates loading python profiles into the controller.


For run:
1.	Change the current directory to examples/test_Python/profiletest. For libximc usage, the example uses a wrapper
	module /ximc/crossplatform/wrappers/python/libximc.
2. 	Configuring dependencies on Linux:
	- you can install all dependencies if you run the example using a script ./testpythonprofile.sh.
	- you may need to set LD_LIBRARY_PATH to let Python find libraries using RPATH. For that use:
		export LD_LIBRARY_PATH=$LD_LIBRARY_PATH: 'pwd'
3.	You need Python2 or Python3 installed.
4.	Run the example with the command:
		python testpythonprofile.py


For modify:
1.	The example code can be modified in any text editor.
2.	To use another profile, copy the required profile from the /ximc/python-profiles folder to
	examples/test_Python/profiletest. Replace the profile name with the required one in the example code.


Rus.

Этот пример демонстрирует загрузку профилей для питона в контроллер.

 
Для запуска примера:
1.	Перейдите в examples/test_Python/profiletest. Для использования библиотеки libximc в примере используется
	модуль-обёртка /ximc/crossplatform/wrappers/python/libximc.
2. 	Настройка зависимостей в Linux: 
	- можно ни чего не устанавливать, если запускать пример с помощью командного файла ./testpythonprofile.sh
	- возможно, вам потребуется установить LD_LIBRARY_PATH, чтобы Python смог найти библиотеки с помощью RPATH. Для этого воспользуйтесь командой:
		export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:'pwd'
3.	Для запуска необходим установленный Python2 или Python3.
4.	Запустите пример командой:
		python testpythonprofile.py

 
Для модификации примера:
1.	Код примера можно модифицировать в любом текстовом редакторе.
2.	Для использования другого профиля, скопируйте необходимый профиль из папки /ximc/python-profiles в
	examples/test_Python/profiletest. В коде примера замените имя профиля на необходимое.
