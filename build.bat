@if 'x%GIT%'=='x' set GIT=git
:: reset errorrevel
@cmd /C exit 0

@set BASEDIR=%CD%
@set DISTDIR=ximc
@set DEPSDIR=deps

:: set by CI
:: @set GIT="%ProgramFiles%\Git\bin\git.exe"
@set CMAKE="%ProgramFiles(x86)%\CMake\bin\cmake.exe" 

:: avoid node reuse, flag is not enough to stop msbuildtaskhost so set env too
@set MSBUILD=msbuild /nr:false
@set MSBUILDDISABLENODEREUSE=1

@if "%1" == "cleandist" call :CLEAN ; exit /B 0

:: JDK_HOME must be set
@echo JDK home is %JDK_HOME%
@if "x%JDK_HOME%"=="x" goto FAIL

:: read vers
set BINDYVER=
set XIWRAPPERVER=
for /F %%i in (' c:\cygwin\bin\bash.exe --login -c "sed '3q;d' `cygpath '%BASEDIR%\version'`" ') do set BINDYVER=%%i
for /F %%i in (' c:\cygwin\bin\bash.exe --login -c "sed '4q;d' `cygpath '%BASEDIR%\version'`" ') do set XIWRAPPERVER=%%i
if "%BINDYVER%" == "" set BINDYVER=dev-1.0-libximc
if "%XIWRAPPERVER%" == "" set XIWRAPPERVER=default
set MINIUPNPCVER=8ddbb71
echo Found bindy ver %BINDYVER%
echo Found xiwrapper ver %XIWRAPPERVER%
echo Set miniupnpc ver %MINIUPNPCVER%

:: debug flag
@set CONFIGURATION=Debug
@if "x%DEBUG%"=="xtrue" goto :CONF_DEBUG
@set CONFIGURATION=Release
:CONF_DEBUG
echo Configuration %CONFIGURATION%

:: -------------------------------------
:: ---------- entry point --------------

@if "%VSINSTALLDIR%" == "" call "%VS120COMNTOOLS%/vsvars32.bat"
@if not %errorlevel% == 0 goto FAIL
@if "%VSINSTALLDIR%" == "" call "%VCINSTALLDIR%/vcvarsall.bat" x86_amd64
@if not %errorlevel% == 0 goto FAIL

call :CLEAN
@if not %errorlevel% == 0 goto FAIL
call :LIB
@if not %errorlevel% == 0 goto FAIL
call :EXAMPLES
@if not %errorlevel% == 0 goto FAIL

:: it is an exit
:SUCCESS
@echo SUCCESS
@goto :eof

:FAIL
@echo FAIL
exit /B 1

:: ----------------------------
:: ---------- clean -----------
:CLEAN
"%GIT%" clean -xdf --exclude %DEPSDIR%
@if not %errorlevel% == 0 goto FAIL
@if exist %DISTDIR% rmdir /S /Q %DISTDIR%
@if not %errorlevel% == 0 goto FAIL
goto :eof

:: ----------------------------------------
:: ---------- build entry point -----------
:LIB
::goto SKIP_DEPS
call :DEPS_BINDY win64 x64
@if not %errorlevel% == 0 goto FAIL
call :DEPS_XIWRAPPER win64 x64
@if not %errorlevel% == 0 goto FAIL
call :DEPS_BINDY win32 Win32
@if not %errorlevel% == 0 goto FAIL
call :DEPS_XIWRAPPER win32 Win32
@if not %errorlevel% == 0 goto FAIL
call :DEPS_MINIUPNPC win64 x64
@if not %errorlevel% == 0 goto FAIL
call :DEPS_MINIUPNPC win32 Win32
@if not %errorlevel% == 0 goto FAIL

:SKIP_DEPS
call :LIBXIMC win32 Win32
@if not %errorlevel% == 0 goto FAIL
call :LIBXIMC win64 x64
@if not %errorlevel% == 0 goto FAIL
call :WRAPPER_JAVA win32 Win32 "%JDK32_HOME%"
@if not %errorlevel% == 0 goto FAIL
call :WRAPPER_JAVA win64 x64 "%JDK_HOME%"
@if not %errorlevel% == 0 goto FAIL
call :WRAPPER_CSHARP win32 Win32
@if not %errorlevel% == 0 goto FAIL
call :WRAPPER_CSHARP win64 x64
@if not %errorlevel% == 0 goto FAIL
call :WRAPPER_DELPHI
@if not %errorlevel% == 0 goto FAIL
call :WRAPPER_MATLAB
@if not %errorlevel% == 0 goto FAIL
goto :eof

:: --------------------------------------
:: ------------ deps bindy --------------
:DEPS_BINDY
@set DISTARCH=%DEPSDIR%\%1
@set ARCH=%2
@echo Building bindy for %ARCH%...

rmdir /S /Q %DISTARCH%\bindy
mkdir %DISTARCH%\bindy

@if "x%URL_BINDY%" == "x" set URL_BINDY="https://github.com/EPC-MSU/Bindy.git"

"%GIT%" clone --recursive %URL_BINDY% %DISTARCH%\bindy
@if not %errorlevel% == 0 goto FAIL
cd %DISTARCH%\bindy
"%GIT%" checkout %BINDYVER%
@if not %errorlevel% == 0 goto FAIL
"%GIT%" submodule update --init --recursive
@if not %errorlevel% == 0 goto FAIL
"%GIT%" submodule update --recursive
@if not %errorlevel% == 0 goto FAIL

"%GIT%" --no-pager show --stat %BINDYVER%
@set GENERATOR=Visual Studio 12 2013
if %ARCH% == x64 @set GENERATOR=%GENERATOR% Win64
%CMAKE% -G "%GENERATOR%" .
@set LASTERR=%errorlevel%
cd %BASEDIR%
@if not %LASTERR% == 0 goto FAIL
%MSBUILD% %DISTARCH%\bindy\bindy.sln /p:Configuration=%CONFIGURATION% /p:Platform=%ARCH%
@if not %errorlevel% == 0 goto FAIL
if not exist %DISTARCH%\bindy\%CONFIGURATION%\bindy.dll goto FAIL
@if not exist %DISTDIR%\%1 mkdir %DISTDIR%\%1
@if not %errorlevel% == 0 goto FAIL
copy %DISTARCH%\bindy\%CONFIGURATION%\bindy.dll %DISTDIR%\%1
@if not %errorlevel% == 0 goto FAIL
copy %DISTARCH%\bindy\%CONFIGURATION%\bindy.lib %DISTDIR%\%1
@if not %errorlevel% == 0 goto FAIL

@if not "x%DEBUG%" == "xtrue" goto SKIP_PDB_COPY_BINDY
copy %DISTARCH%\bindy\%CONFIGURATION%\bindy.pdb %DISTDIR%\%1
@if not %errorlevel% == 0 goto FAIL
:SKIP_PDB_COPY_BINDY

@echo Building bindy for %ARCH% completed
@goto :eof

:: --------------------------------------
:: ------------ deps xiwrapper -------------
:DEPS_XIWRAPPER
@set DISTARCH=%DEPSDIR%\%1
@set ARCH=%2
@echo Building xiwrapper for %ARCH%...

rmdir /S /Q %DISTARCH%\xiwrapper
mkdir %DISTARCH%\xiwrapper

@if "x%URL_XIWRAPPER%" == "x" set URL_XIWRAPPER="https://gitlab.ximc.ru/ximc-public/libxiwrapper.git"

"%GIT%" clone %URL_XIWRAPPER% %DISTARCH%\xiwrapper
@if not %errorlevel% == 0 goto FAIL
cd %DISTARCH%\xiwrapper
%GIT% checkout %XIWRAPPERVER%
@if not %errorlevel% == 0 goto FAIL
"%GIT%" --no-pager show --stat %XIWRAPPERVER%
@if not %errorlevel% == 0 goto FAIL
@set GENERATOR=Visual Studio 12 2013
if %ARCH% == x64 @set GENERATOR=%GENERATOR% Win64
%CMAKE% -G "%GENERATOR%" -DBINDY_PATH=%BASEDIR%\%DISTARCH%\bindy .
@set LASTERR=%errorlevel%
cd %BASEDIR%
@if not %LASTERR% == 0 goto FAIL
%MSBUILD% %DISTARCH%\xiwrapper\xiwrapper.sln /p:Configuration=%CONFIGURATION% /p:Platform=%ARCH%
@if not %errorlevel% == 0 goto FAIL
if not exist %DISTARCH%\xiwrapper\%CONFIGURATION%\xiwrapper.dll goto FAIL
@if not exist %DISTDIR%\%1 mkdir %DISTDIR%\%1
@if not %errorlevel% == 0 goto FAIL
copy %DISTARCH%\xiwrapper\%CONFIGURATION%\xiwrapper.dll %DISTDIR%\%1
@if not %errorlevel% == 0 goto FAIL

@if not "x%DEBUG%" == "xtrue" goto SKIP_PDB_COPY_XIWRAPPER
copy %DISTARCH%\xiwrapper\%CONFIGURATION%\xiwrapper.pdb %DISTDIR%\%1
@if not %errorlevel% == 0 goto FAIL
:SKIP_PDB_COPY_XIWRAPPER

@echo Building xiwrapper for %ARCH% completed
@goto :eof

:: --------------------------------------
:: ------------ deps miniupnpc ----------
:DEPS_MINIUPNPC
@set DISTARCH=%DEPSDIR%\%1
@set ARCH=%2
@echo Building miniupnpc for %ARCH%...

rmdir /S /Q %DISTARCH%\miniupnpc-dist
rmdir /S /Q %DISTARCH%\miniupnpc
mkdir %DISTARCH%\miniupnpc

@if "x%URL_MINIUPNPC%" == "x" set URL_MINIUPNPC="https://github.com/EPC-MSU/miniupnpc.git"

"%GIT%" clone --recursive %URL_MINIUPNPC% %DISTARCH%\miniupnpc-dist
@if not %errorlevel% == 0 goto FAIL
cd %DISTARCH%\miniupnpc-dist
"%GIT%" checkout %MINIUPNPCVER%
@if not %errorlevel% == 0 goto FAIL

@set GENERATOR=Visual Studio 12 2013
if %ARCH% == x64 @set GENERATOR=%GENERATOR% Win64
%CMAKE% -G "%GENERATOR%" -DUPNPC_BUILD_TESTS=OFF -DUPNPC_BUILD_SAMPLE=OFF -DUPNPC_BUILD_SHARED=OFF -DCMAKE_INSTALL_PREFIX=%BASEDIR%\%DISTARCH%\miniupnpc .
@set LASTERR=%errorlevel%
cd %BASEDIR%
@if not %LASTERR% == 0 goto FAIL

%MSBUILD% %DISTARCH%\miniupnpc-dist\ALL_BUILD.vcxproj
@if not %errorlevel% == 0 goto FAIL
%MSBUILD% %DISTARCH%\miniupnpc-dist\INSTALL.vcxproj
@if not %errorlevel% == 0 goto FAIL


@echo Building miniupnpc for %ARCH% completed
@goto :eof


:: --------------------------------------
:: -------------- libximc ---------------
:LIBXIMC
@set DISTARCH=%DISTDIR%\%1
@set ARCH=%2
@echo Building libximc for %ARCH%...
@set BINDIR=%CONFIGURATION%-%ARCH%

"%GIT%" clean -xdf --exclude %DEPSDIR% --exclude %DISTDIR%
@if not %errorlevel% == 0 goto FAIL
@if not exist %DISTARCH% mkdir %DISTARCH%
@if not %errorlevel% == 0 goto FAIL

%MSBUILD% libximc.sln /p:Configuration=%CONFIGURATION% /p:Platform=%ARCH% /t:xigen;libximc
@if not %errorlevel% == 0 goto FAIL
copy %BINDIR%\libximc.dll %DISTARCH%
@if not %errorlevel% == 0 goto FAIL
copy %BINDIR%\libximc.lib %DISTARCH%
@if not %errorlevel% == 0 goto FAIL
copy libximc\src\libximc.def %DISTARCH%
@if not %errorlevel% == 0 goto FAIL
copy libximc\include\ximc.h %DISTARCH%
@if not %errorlevel% == 0 goto FAIL
@if not "x%DEBUG%" == "xtrue" goto SKIP_PDB_COPY_LIBXIMC
copy %BINDIR%\*.pdb %DISTARCH%
@if not %errorlevel% == 0 goto FAIL
:SKIP_PDB_COPY_LIBXIMC

@echo Building for %ARCH% completed
@goto :eof

:: ------------------------------------
:: ---------- csharp wrapper ---------- 
:WRAPPER_CSHARP
@echo Building csharp wrapper
@set DISTARCH=%DISTDIR%\%1
@set BINDIR=wrappers\csharp\bin\%CONFIGURATION%-%2

:: allow msbuild processes to finish, sometimes they lock build dir
waitfor XimcBuildLock /t 30
@cmd /C exit 0

"%GIT%" clean -xdf --exclude %DEPSDIR% --exclude %DISTDIR%
@if not %errorlevel% == 0 goto FAIL
@if not exist %DISTARCH% mkdir %DISTARCH%
@if not %errorlevel% == 0 goto FAIL

%MSBUILD% libximc.sln /p:Configuration=%CONFIGURATION% /p:Platform=Win32 /t:xigen
@if not %errorlevel% == 0 goto FAIL
%MSBUILD% wrappers\csharp\ximcnet.sln /p:Configuration=%CONFIGURATION% /p:Platform=%2
@if not %errorlevel% == 0 goto FAIL
copy %BINDIR%\ximcnet.dll %DISTARCH%
@if not %errorlevel% == 0 goto FAIL
copy wrappers\csharp\src\ximcnet.cs %DISTARCH%
@if not %errorlevel% == 0 goto FAIL

waitfor XimcBuildLock /t 30
@cmd /C exit 0

@echo Building sharp wrapper completed
@goto :eof

:: ------------------------------------
:: ---------- delphi wrapper ---------- 
:WRAPPER_DELPHI
@echo Generating pascal wrapper
@set DISTARCH=%DISTDIR%\win32

"%GIT%" clean -xdf --exclude %DEPSDIR% --exclude %DISTDIR%
@if not %errorlevel% == 0 goto FAIL

%MSBUILD% libximc.sln /p:Configuration=%CONFIGURATION% /p:Platform=Win32 /t:xigen
@if not %errorlevel% == 0 goto FAIL
%CONFIGURATION%-Win32\xigen.exe --gen-pascal -x version -i libximc\src\protocol.xi -o wrappers\delphi\ximc.pas -t wrappers\delphi\ximc-template.pas
@if not %errorlevel% == 0 goto FAIL

copy wrappers\delphi\ximc.pas %DISTARCH%
@if not %errorlevel% == 0 goto FAIL

@echo Generating pascal wrapper completed
@goto :eof

:: ------------------------------------
:: ---------- java wrapper ---------- 
:WRAPPER_JAVA
@set DISTARCH=%DISTDIR%\%1
@set ARCH=%2
@set JPATH=%3
@echo Generating java wrapper for %ARCH% and %JPATH%
@set GENDIR=wrappers\java\gen
@set BINDIR=%CONFIGURATION%-%ARCH%\

"%GIT%" clean -xdf --exclude %DEPSDIR% --exclude %DISTDIR%
@if not %errorlevel% == 0 goto FAIL

@if not exist %GENDIR% mkdir %GENDIR%

%MSBUILD% libximc.sln /p:Configuration=%CONFIGURATION% /p:Platform=%ARCH% /t:xigen
@if not %errorlevel% == 0 goto FAIL

%CONFIGURATION%-%ARCH%\xigen.exe --gen-java -x version -i libximc\src\protocol.xi -o wrappers\java\src\java\ru\ximc\libximc\JXimc.java -t wrappers\java\src\java\\ru\ximc\libximc\JXimc-template.java
@if not %errorlevel% == 0 goto FAIL

%JPATH%\bin\javac -Xlint -d wrappers\java wrappers\java\src\java\ru\ximc\libximc\JXimc.java wrappers\java\src\java\ru\ximc\libximc\XimcError.java wrappers\java\src\java\ru\ximc\libximc\XimcNoDevice.java wrappers\java\src\java\ru\ximc\libximc\XimcNotImplemented.java wrappers\java\src\java\ru\ximc\libximc\XimcValueError.java
@if not %errorlevel% == 0 goto FAIL

%JPATH%\bin\jar cf wrappers\java\libjximc.jar -C wrappers\java ru 
@if not %errorlevel% == 0 goto FAIL

%JPATH%\bin\javah -classpath wrappers\java\libjximc.jar -jni -d %GENDIR% ru.ximc.libximc.JXimc
@if not %errorlevel% == 0 goto FAIL

%CONFIGURATION%-%ARCH%\xigen.exe --gen-jni -x version -i libximc\src\protocol.xi -o wrappers\java\src\c\ru_ximc_libximc_JXimc-gen.c -t wrappers\java\src\c\ru_ximc_libximc_JXimc-template.c
@if not %errorlevel% == 0 goto FAIL

%MSBUILD% libximc.sln /p:Configuration=%CONFIGURATION% /p:Platform=%ARCH% /t:libjximc
@if not %errorlevel% == 0 goto FAIL

copy wrappers\java\libjximc.jar %DISTARCH%
@if not %errorlevel% == 0 goto FAIL

copy %BINDIR%\libjximc.dll %DISTARCH%
@if not %errorlevel% == 0 goto FAIL

@echo Generating java wrapper completed
@goto :eof


:: ------------------------------------
:: ---------- matlab wrapper ---------- 
:WRAPPER_MATLAB
@echo Building matlab wrapper
@set DISTARCH=%DISTDIR%\win64
@set BINDIR=%DISTARCH%\wrappers\matlab

@if not exist %BINDIR% mkdir %BINDIR%
@if not %errorlevel% == 0 goto FAIL

copy %DISTARCH%\bindy.dll wrappers\matlab\
copy %DISTARCH%\xiwrapper.dll wrappers\matlab\
copy %DISTARCH%\libximc.dll wrappers\matlab\

@if not %errorlevel% == 0 goto FAIL
cd wrappers\matlab
matlab.exe -nodesktop -wait -r buildm -logfile buildm.log
@set LASTERR=%errorlevel%
cd %BASEDIR%
@if not %LASTERR% == 0 goto FAIL

move wrappers\matlab\ximcm.m %BINDIR%
@if not %errorlevel% == 0 goto FAIL

move wrappers\matlab\libximc_thunk_pcwin64.dll %BINDIR%
@if not %errorlevel% == 0 goto FAIL

copy wrappers\matlab\ximcm.h %BINDIR%
@if not %errorlevel% == 0 goto FAIL

@echo Building matlab wrapper completed
@goto :eof

:: ------------------------------
:: ---------- examples ---------- 
:EXAMPLES
:: allow msbuild processes to finish, sometimes they lock build dir
waitfor XimcBuildLock /t 30
@cmd /C exit 0

"%GIT%" clean -xdf --exclude %DEPSDIR% --exclude %DISTDIR%
@if not %errorlevel% == 0 goto FAIL
:: -----
@set NAME=testapp_C
@echo Building example %NAME%...
%MSBUILD% examples\test_C\%NAME%\%NAME%.sln /p:Configuration=%CONFIGURATION% /p:Platform=Win32
@if not %errorlevel% == 0 goto FAIL
mkdir %DISTDIR%\win32\%NAME%-compiled-win32
copy examples\test_C\%NAME%\compiled-win32\* %DISTDIR%\win32\%NAME%-compiled-win32\*
copy examples\test_C\%NAME%\Corr_table_example.tbl %DISTDIR%\win32\%NAME%-compiled-win32\Corr_table_example.tbl
@if not %errorlevel% == 0 goto FAIL
%MSBUILD% examples\test_C\%NAME%\%NAME%.sln /p:Configuration=%CONFIGURATION% /p:Platform=x64
@if not %errorlevel% == 0 goto FAIL
mkdir %DISTDIR%\win64\%NAME%-compiled-win64
copy examples\test_C\%NAME%\compiled-win64\* %DISTDIR%\win64\%NAME%-compiled-win64\*
copy examples\test_C\%NAME%\Corr_table_example.tbl %DISTDIR%\win64\%NAME%-compiled-win64\Corr_table_example.tbl
@if not %errorlevel% == 0 goto FAIL

@if not "x%DEBUG%" == "xtrue" goto SKIP_PDB_COPY_TESTAPP
:: TODO: Bug will be here
::copy examples\test_C\%NAME%\%CONFIGURATION%-Win32\%NAME%.pdb %DISTDIR%\win32\test_C
::@if not %errorlevel% == 0 goto FAIL
::copy examples\test_C\%NAME%\%CONFIGURATION%-x64\%NAME%.pdb %DISTDIR%\win64\test_C
::@if not %errorlevel% == 0 goto FAIL
:SKIP_PDB_COPY_TESTAPP
:: ----- in CodeBlocks
@echo Building example CodeBlocks %NAME%...
@SET MINGW32=C:\Program Files (x86)\mingw-w64\i686-7.3.0-posix-dwarf-rt_v5-rev0\mingw32\bin
@SET MINGW64=C:\Program Files\mingw-w64\x86_64-7.3.0-posix-seh-rt_v5-rev0\mingw64\bin
@SET CBP=C:\Program Files (x86)\CodeBlocks\cbp2make.exe
@SET PATH_BASE=%PATH%;
:: Win32
@SET PATH=%PATH_BASE%;%MINGW32%
"%CBP%" -in examples\test_C\%NAME%\%NAME%.cbp -out examples\test_C\%NAME%\makefile -windows -targets "win32" 
@if not %errorlevel% == 0 goto FAIL
mingw32-make --directory examples\test_C\%NAME%
@if not %errorlevel% == 0 goto FAIL
del examples\test_C\%NAME%\cb_obj /Q
mkdir %DISTDIR%\win32\%NAME%-cb_compiled-win32
copy examples\test_C\%NAME%\cb_compiled-win32\* %DISTDIR%\win32\%NAME%-cb_compiled-win32\*
copy examples\test_C\%NAME%\Corr_table_example.tbl %DISTDIR%\win32\%NAME%-cb_compiled-win32\Corr_table_example.tbl
@if not %errorlevel% == 0 goto FAIL
:: Win64
@SET PATH=%PATH_BASE%;%MINGW64%
"%CBP%" -in examples\test_C\%NAME%\%NAME%.cbp -out examples\test_C\%NAME%\makefile -windows -targets "win64"
@if not %errorlevel% == 0 goto FAIL
mingw32-make --directory examples\test_C\%NAME%
@if not %errorlevel% == 0 goto FAIL
del examples\test_C\%NAME%\cb_obj /Q
mkdir %DISTDIR%\win64\%NAME%-cb_compiled-win64
copy examples\test_C\%NAME%\cb_compiled-win64\* %DISTDIR%\win64\%NAME%-cb_compiled-win64\*
copy examples\test_C\%NAME%\Corr_table_example.tbl %DISTDIR%\win64\%NAME%-cb_compiled-win64\Corr_table_example.tbl
@if not %errorlevel% == 0 goto FAIL

del %DISTDIR%\win32\%NAME%-compiled-win32\testapp_C.pdb
del %DISTDIR%\win64\%NAME%-compiled-win64\testapp_C.pdb
::   clear env
@SET PATH=%PATH_BASE%

:: -----
@set NAME=testappeasy_C
@echo Building example %NAME%...
%MSBUILD% examples\test_C\%NAME%\%NAME%.sln /p:Configuration=%CONFIGURATION% /p:Platform=Win32
@if not %errorlevel% == 0 goto FAIL
mkdir %DISTDIR%\win32\%NAME%-compiled-win32
copy examples\test_C\%NAME%\compiled-win32\* %DISTDIR%\win32\%NAME%-compiled-win32\*
@if not %errorlevel% == 0 goto FAIL
%MSBUILD% examples\test_C\%NAME%\%NAME%.sln /p:Configuration=%CONFIGURATION% /p:Platform=x64
@if not %errorlevel% == 0 goto FAIL
mkdir %DISTDIR%\win64\%NAME%-compiled-win64
copy examples\test_C\%NAME%\compiled-win64\* %DISTDIR%\win64\%NAME%-compiled-win64\*
@if not %errorlevel% == 0 goto FAIL
:: ----- in CodeBlocks
@echo Building example CodeBlocks %NAME%...
@SET MINGW32=C:\Program Files (x86)\mingw-w64\i686-7.3.0-posix-dwarf-rt_v5-rev0\mingw32\bin
@SET MINGW64=C:\Program Files\mingw-w64\x86_64-7.3.0-posix-seh-rt_v5-rev0\mingw64\bin
@SET CBP=C:\Program Files (x86)\CodeBlocks\cbp2make.exe
@SET PATH_BASE=%PATH%;
:: Win32
@SET PATH=%PATH_BASE%;%MINGW32%
"%CBP%" -in examples\test_C\%NAME%\%NAME%.cbp -out examples\test_C\%NAME%\makefile -windows -targets "win32" 
@if not %errorlevel% == 0 goto FAIL
mingw32-make --directory examples\test_C\%NAME%
@if not %errorlevel% == 0 goto FAIL
del examples\test_C\%NAME%\cb_obj /Q
mkdir %DISTDIR%\win32\%NAME%-cb_compiled-win32
copy examples\test_C\%NAME%\cb_compiled-win32\* %DISTDIR%\win32\%NAME%-cb_compiled-win32\*
@if not %errorlevel% == 0 goto FAIL
:: Win64
@SET PATH=%PATH_BASE%;%MINGW64%
"%CBP%" -in examples\test_C\%NAME%\%NAME%.cbp -out examples\test_C\%NAME%\makefile -windows -targets "win64"
@if not %errorlevel% == 0 goto FAIL
mingw32-make --directory examples\test_C\%NAME%
@if not %errorlevel% == 0 goto FAIL
del examples\test_C\%NAME%\cb_obj /Q
mkdir %DISTDIR%\win64\%NAME%-cb_compiled-win64
copy examples\test_C\%NAME%\cb_compiled-win64\* %DISTDIR%\win64\%NAME%-cb_compiled-win64\*
@if not %errorlevel% == 0 goto FAIL

del %DISTDIR%\win32\%NAME%-compiled-win32\testappeasy_C.pdb
del %DISTDIR%\win64\%NAME%-compiled-win64\testappeasy_C.pdb
::   clear env
@SET PATH=%PATH_BASE%

:: -----
@set NAME=testprofile_C
@echo Building example %NAME%...
%MSBUILD% examples\test_C\%NAME%\%NAME%.sln /p:Configuration=%CONFIGURATION% /p:Platform=Win32
@if not %errorlevel% == 0 goto FAIL
mkdir %DISTDIR%\win32\%NAME%-compiled-win32
copy examples\test_C\%NAME%\compiled-win32\* %DISTDIR%\win32\%NAME%-compiled-win32\*
@if not %errorlevel% == 0 goto FAIL
%MSBUILD% examples\test_C\%NAME%\%NAME%.sln /p:Configuration=%CONFIGURATION% /p:Platform=x64
@if not %errorlevel% == 0 goto FAIL
mkdir %DISTDIR%\win64\%NAME%-compiled-win64
copy examples\test_C\%NAME%\compiled-win64\* %DISTDIR%\win64\%NAME%-compiled-win64\*
@if not %errorlevel% == 0 goto FAIL

del %DISTDIR%\win32\%NAME%-compiled-win32\testprofile_C.pdb
del %DISTDIR%\win64\%NAME%-compiled-win64\testprofile_C.pdb

:: -----
@set NAME=test_CSharp
@echo Building example %NAME%...
:: Win32
copy %DISTDIR%\win32\ximcnet.dll examples\%NAME%\
%MSBUILD% examples\%NAME%\%NAME%.sln /p:Configuration=%CONFIGURATION% /p:Platform=Win32
@if not %errorlevel% == 0 goto FAIL
mkdir %DISTDIR%\win32\%NAME%-compiled-win32
copy examples\%NAME%\compiled-win32\* %DISTDIR%\win32\%NAME%-compiled-win32\*
@if not %errorlevel% == 0 goto FAIL
:: x64
copy %DISTDIR%\win64\ximcnet.dll examples\%NAME%
%MSBUILD% examples\%NAME%\%NAME%.sln /p:Configuration=%CONFIGURATION% /p:Platform=x64
@if not %errorlevel% == 0 goto FAIL
mkdir %DISTDIR%\win64\%NAME%-compiled-win64
copy examples\%NAME%\compiled-win64\* %DISTDIR%\win64\%NAME%-compiled-win64\*
@if not %errorlevel% == 0 goto FAIL

del %DISTDIR%\win32\%NAME%-compiled-win32\test_CSharp.exe.config
del %DISTDIR%\win32\%NAME%-compiled-win32\test_CSharp.pdb
del %DISTDIR%\win64\%NAME%-compiled-win64\test_CSharp.exe.config
del %DISTDIR%\win64\%NAME%-compiled-win64\test_CSharp.pdb
:: -----
@set NAME=test_VBNET
@echo Building example %NAME%...
:: Win32
copy %DISTDIR%\win32\ximcnet.dll examples\%NAME%
%MSBUILD% examples\%NAME%\%NAME%.sln /p:Configuration=%CONFIGURATION% /p:Platform=Win32
@if not %errorlevel% == 0 goto FAIL
mkdir %DISTDIR%\win32\%NAME%-compiled-win32
copy examples\%NAME%\compiled-win32\* %DISTDIR%\win32\%NAME%-compiled-win32\*
@if not %errorlevel% == 0 goto FAIL

del %DISTDIR%\win32\%NAME%-compiled-win32\test_VBNET.pdb
del %DISTDIR%\win32\%NAME%-compiled-win32\test_VBNET.xml
:: x64
copy %DISTDIR%\win64\ximcnet.dll examples\%NAME%
%MSBUILD% examples\%NAME%\%NAME%.sln /p:Configuration=%CONFIGURATION% /p:Platform=x64
@if not %errorlevel% == 0 goto FAIL
mkdir %DISTDIR%\win64\%NAME%-compiled-win64
copy examples\%NAME%\compiled-win64\* %DISTDIR%\win64\%NAME%-compiled-win64\*
@if not %errorlevel% == 0 goto FAIL

del %DISTDIR%\win64\%NAME%-compiled-win64\test_VBNET.pdb
del %DISTDIR%\win64\%NAME%-compiled-win64\test_VBNET.xml
:: -----
@set NAME=test_Delphi
@echo Building example %NAME%...
"%PROGRAMFILES(x86)%\Borland\Delphi6\Bin\DCC32.EXE" -U%DISTDIR%\win32 examples\%NAME%\%NAME%.dpr
@if not %errorlevel% == 0 goto FAIL
copy examples\%NAME%\%NAME%.exe %DISTDIR%\win32
@if not %errorlevel% == 0 goto FAIL

:: -----
@set NAME=test_Java
@echo Building example %NAME% 64-bit...
"%JDK_HOME%\bin\javac" -Xlint -classpath %DISTDIR%\win64\libjximc.jar -d examples\%NAME% examples\%NAME%\ru\ximc\TestJava.java
@if not %errorlevel% == 0 goto FAIL
"%JDK_HOME%\bin\jar" cmf examples\%NAME%\MANIFEST.MF examples\%NAME%\%NAME%.jar -C examples\%NAME% ru 
@if not %errorlevel% == 0 goto FAIL
copy examples\%NAME%\%NAME%.jar %DISTDIR%\win64
@if not %errorlevel% == 0 goto FAIL
:: -----
@set NAME=test_Java
@echo Building example %NAME% 32-bit...
"%JDK32_HOME%\bin\javac" -Xlint -classpath %DISTDIR%\win32\libjximc.jar -d examples\%NAME% examples\%NAME%\ru\ximc\TestJava.java
@if not %errorlevel% == 0 goto FAIL
"%JDK32_HOME%\bin\jar" cmf examples\%NAME%\MANIFEST.MF examples\%NAME%\%NAME%.jar -C examples\%NAME% ru 
@if not %errorlevel% == 0 goto FAIL
copy examples\%NAME%\%NAME%.jar %DISTDIR%\win32
@if not %errorlevel% == 0 goto FAIL
:: -----
@goto :eof

