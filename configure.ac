AC_PREREQ(2.59)
AC_INIT([libximc7], [2.14.19])

AC_CONFIG_MACRO_DIR([m4])
AC_CONFIG_AUX_DIR(config)
AC_CONFIG_HEADER([config.h])
AC_CANONICAL_HOST
AC_CANONICAL_BUILD

AC_CONFIG_FILES([Makefile
								 libximc/Makefile
								 libximc/src/Makefile
								 libximc/docs/Makefile
								 libximc/docs/doc-en/Doxyfile
								 libximc/docs/doc-en/Makefile
								 libximc/docs/doc-ru/Doxyfile
								 libximc/docs/doc-ru/Makefile
								 xigen/Makefile
								 xigen/src/Makefile
								 xigen/tests/Makefile
								 wrappers/Makefile
								 wrappers/java/Makefile
								 wrappers/java/src/Makefile
								 wrappers/java/src/c/Makefile
								 wrappers/java/src/java/Makefile
								 wrappers/python/Makefile
								])

AM_INIT_AUTOMAKE([-Wall -Werror])

# libtool requirement, non-posix
AC_PROG_EGREP

# check xcodebuild

case "$host_os" in
	darwin*)
	AC_MSG_CHECKING([for xcode build])
	AC_ARG_WITH([xcode-build],
							[AS_HELP_STRING([--with-xcode-build], [build project with xcode (default no)])],
							[with_xcode_build=$withval],
							[with_xcode_build=no])
	AC_MSG_RESULT([$with_xcode_build])

	AC_MSG_CHECKING([for xcode compiler])
	AC_ARG_WITH([xcode-compiler],
							[AS_HELP_STRING([--with-xcode-compiler], [XCode compiler to use])],
							[with_xcode_compiler=$withval],
							[with_xcode_compiler=])
	AC_MSG_RESULT([$with_xcode_compiler])
	;;
esac

AM_CONDITIONAL([HAVE_XCODE_BUILD], [test "x$with_xcode_build" = "xyes"])

AC_SUBST([XCODE_COMPILER],["$with_xcode_compiler"])

# init doxygen 

AC_MSG_CHECKING([for docs])
AC_ARG_WITH([docs],
						[AS_HELP_STRING([--with-docs], [generate doxygen docs (default no)])],
						[with_docs=$withval],
						[with_docs=no])
AC_MSG_RESULT([$with_docs])

AM_CONDITIONAL([HAVE_DOCS], [test "x$with_docs" = "xyes"])

if test "x$with_docs" = "xyes" ; then
	DX_INIT_DOXYGEN([$PACKAGE_NAME], [Doxyfile], [docs] )
else
	DX_INIT_DOXYGEN([$PACKAGE_NAME], [DO_NOT_WANT], [docs] )
fi

# Check for locks feature

AC_MSG_CHECKING([for locks support])
AC_ARG_WITH([locks],
						[AS_HELP_STRING([--with-locks], [use pthread locks (default no)])],
						[with_locks=$withval],
						[with_locks=yes])
AC_MSG_RESULT([$with_locks])

if test "x$with_locks" = "xyes" ; then
	AC_DEFINE([HAVE_LOCKS], [1], [Use locking mechanism])
fi

# Check for java

AC_MSG_CHECKING([for java])
AC_ARG_WITH([java],
						[AS_HELP_STRING([--with-java], [generate Java bindings (default yes)])],
						[with_java=$withval],
						[with_java=yes])
AC_MSG_RESULT([$with_java])

AM_CONDITIONAL([HAVE_JAVA], [test "x$with_java" = "xyes"])

# Check for static deps

AC_MSG_CHECKING([for static deps])
AC_ARG_WITH([staticdeps],
						[AS_HELP_STRING([--with-staticdeps], [use static xiwrapper and bindy dependencies (default no)])],
						[with_staticdeps=$withval],
						[with_staticdeps=no])
AC_MSG_RESULT([$with_staticdeps])

AM_CONDITIONAL([HAVE_STATICDEPS], [test "x$with_staticdeps" = "xyes"])

# detect OS X and add framework flags

case "$host_os" in
	darwin*)
		extra_ldflags_iokit='-framework CoreFoundation -framework IOKit'
	;;
esac
AC_SUBST(extra_ldflags_iokit)

# Checks for programs.
AC_PROG_CC
# AC_PROG_CC_C99 available only for autoconf 2.60
m4_ifdef([AC_PROG_CC_C99], [AC_PROG_CC_C99]) 
AC_PROG_CXX

# save build compiler
AC_PROG_CC_FOR_BUILD
AC_PROG_CXX_FOR_BUILD

AC_PROG_LEX
AC_PROG_YACC
# AM_PROG_AR available only for automake 1.12
m4_ifdef([AM_PROG_AR], [AM_PROG_AR])

AC_SEARCH_LIBS([clock_gettime], [rt], [], [])

# Check support
AC_MSG_CHECKING([for unit testing])
AC_ARG_WITH([unittests],
						[AS_HELP_STRING([--with-unittests], [use unit tests with check framework (default no)])],
						[with_unittests=$withval],
						[with_unittests=no])
AC_MSG_RESULT([$with_unittests])

if test "x$with_unittests" = "xyes" ; then
	AM_PROG_CC_C_O
	AC_PROG_CC_C_O

	PKG_CHECK_MODULES([CHECK], [check >= 0.9.0])
fi
AM_CONDITIONAL([HAVE_CHECK], [test "x$with_unittests" = "xyes"])

# Java programs
if test "x$with_java" = "xyes" ; then
	AX_CHECK_CLASSPATH
	AX_JAVA_OPTIONS
	AX_PROG_JAVAC
	AX_PROG_JAVA
	AX_PROG_JAVAH
	AX_PROG_JAR
	AX_PROG_JAVADOC
	AX_JNI_INCLUDE_DIR

	for JNI_INCLUDE_DIR in $JNI_INCLUDE_DIRS ; do
		CPPJNIFLAGS="$CPPJNIFLAGS -I$JNI_INCLUDE_DIR"
	done
	AC_SUBST([CPPJNIFLAGS],["$CPPJNIFLAGS"])
fi

AC_FUNC_STRERROR_R

AC_PROG_INSTALL
AC_PROG_LIBTOOL

# init libtool
LT_INIT
LT_SYS_MODULE_EXT

if test "x$libltdl_cv_shrext" = "x"; then
	# ancient libtool?
	AC_SUBST([SHARED_EXT], [".so"])
else
	AC_SUBST([SHARED_EXT], ["$libltdl_cv_shrext"])
fi
AC_SUBST([STATIC_EXT], [".a"])

# Checks for header files.
AC_HEADER_STDC
AC_CHECK_HEADERS([fcntl.h string.h sys/ioctl.h termios.h unistd.h strings.h syslog.h stdint.h])
if test "x$with_locks" = "xyes" ; then
	AC_CHECK_HEADERS([semaphore.h])
fi
# Use pthreads anyway
AC_CHECK_LIB([pthread], [pthread_create])
AC_CHECK_FUNCS([strstr strerror_r nanosleep flock realloc realpath])

# xiwrapper support


AC_MSG_CHECKING([for xiwrapper support])
AC_ARG_WITH([xiwrapper],
						[AS_HELP_STRING([--with-xiwrapper], [use xiwrapper at path])],
						[with_xiwrapper=$withval],
						[with_xiwrapper=no])
AC_MSG_RESULT([$with_xiwrapper])

if test "x$with_xiwrapper" != "xno" ; then
	CPPFLAGS="$CPPFLAGS -I$with_xiwrapper"
	LDFLAGS="$LDFLAGS -L$with_xiwrapper"
	AC_SUBST([XIWRAPPER_PATH], [$with_xiwrapper])
	AC_DEFINE([HAVE_XIWRAPPER], [1], [Use xiwrapper])
fi
AM_CONDITIONAL([HAVE_XIWRAPPER], [test "x$with_xiwrapper" != "xno"])

AC_CHECK_HEADERS([wrapper.h])

# miniupnpc support
AC_MSG_CHECKING([for miniupnpc support])
AC_ARG_WITH([miniupnpc],
						[AS_HELP_STRING([--with-miniupnpc], [use miniupnpc at path])],
						[with_miniupnpc=$withval],
						[with_miniupnpc=no])
AC_MSG_RESULT([$with_miniupnpc])

if test "x$with_miniupnpc" != "xno" ; then
	CPPFLAGS="$CPPFLAGS -I$with_miniupnpc/include"
	LDFLAGS="$LDFLAGS -L$with_miniupnpc/lib"
fi


# Checks for typedefs, structures, and compiler characteristics.

AC_OUTPUT

echo "
  $PACKAGE_NAME version $PACKAGE_VERSION
  Prefix..............: $prefix
  C Compiler..........: $CC $CFLAGS $CPPFLAGS
  C++ Compiler........: $CXX $CXXFLAGS $CPPFLAGS
  Linker..............: $LD $LDFLAGS $LIBS
  Yacc................: $YACC (`$YACC --version | head -n1`)
  Lex.................: $LEX (`$LEX --version | head -n1`)
  Doxygen.............: ${DX_DOXYGEN:-NO}
  Docs support........: ${with_docs:-NO}
  Locks support.......: ${with_locks:-NO}
  Java support........: ${with_java:-NO}
  XCode build.........: ${with_xcode_build:-NO} ${with_xcode_compiler}
  Xiwrapper support...: ${with_xiwrapper}
  Miniupnpc support...: ${with_miniupnpc}
  Unit testing........: ${with_unittests}"
if test "x$with_java" = "xyes" ; then
JAVAC_VERSION=`javac -version 2>&1`
echo "\
  Java compiler.......: ${JAVAC}
  Java version........: ${JAVAC_VERSION}
  JNI include path....: ${JNI_INCLUDE_DIRS}"
fi
if test "x$cross_compiling" = "xyes" ; then
echo "\
  Build C++ compiler..: ${CXX_FOR_BUILD} ${CXXFLAGS_FOR_BUILD} ${CPPFLAGS_FOR_BUILD}
  Build linker........: $LD ${LDFLAGS_FOR_BUILD}"
fi
