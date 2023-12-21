#!/bin/sh
set -e

[ -n "$GIT" ] || GIT=git
BASEROOT=`pwd`
LOCAL=`pwd`/dist/local
DEPS=`pwd`/deps
DISTNAME=
MAKE=
DL=ximc
PKGROOT=$BASEROOT/pkgroot

VERSION_FILE=`dirname $0`/version
if [ ! -f "$VERSION_FILE" ] ; then
	echo No version file
fi
VER=`sed 'q' "$VERSION_FILE"`
SOVER=`sed '2q;d' "$VERSION_FILE"`
BINDYVER=`sed '3q;d' "$VERSION_FILE"`
XIWRAPPERVER=`sed '4q;d' "$VERSION_FILE"`
if [ -z "$XIWRAPPERVER" ] ; then
	XIWRAPPERVER=default
fi
MINIUPNPCVER=8ddbb71
SOVERMAJOR=`echo $SOVER | sed 's/\..*//'`
if [ -z "$SOVERMAJOR" ] ; then
	echo Version error
	exit 1
fi
echo Packaging version $VER

VNAME=libximc$SOVERMAJOR-$VER

exit_clean_up()
{
	if [ -f "$BASEROOT/configure.ac.bak" ] ; then
		sed -i.bak "s/^AC_INIT(\[libximc\], \(.*\)$/AC_INIT(\[libximc$SOVERMAJOR\], \1/" configure.ac
	fi
}

configure_dist()
{
	echo "Configure dist of uname" `uname -s`
	# all these platform-specific flags
	CONFIGURE_FLAGS=
	SPECIAL_ENV=
	DEPS_CMAKE_OPT=$DEPS_CMAKE_OPT
	if [ -z "$USE_CFLAGS" ] ; then
		USE_CFLAGS=
		echo Using default external CFLAGS
	fi
	if [ -z "$USE_CXXFLAGS" ] ; then
		USE_CXXFLAGS=
		echo Using default external CXXFLAGS
	fi
	DISTCHECK_CONFIGURE_FLAGS_EXTRA=
	PACKAGE_EXTRA_CONFIGURE="--with-xiwrapper=$DEPS/xiwrapper --with-miniupnpc=$DEPS/miniupnpc"
	case "`uname -s`" in
		Darwin)
			DISTNAME=macosx
			MAKE=make
			DEPS_CMAKE_OPT="-DCMAKE_CXX_COMPILER=clang++"
			# it is about deprecated sem_getvalue
			USE_CFLAGS="-Wno-deprecated-declarations"
			USE_CXXFLAGS="-Wno-tautological-compare"
			SPECIAL_ENV="CC=clang CXX=clang++ CC_FOR_BUILD=clang CXX_FOR_BUILD=clang++"
			if [ -z "$JAVA_HOME" ] ; then
				SPECIAL_ENV="$SPECIAL_ENV JAVA_HOME=`/usr/libexec/java_home -v 1.7`"
			fi
			;;
		Linux)
			DISTNAME=
			if [ -f "/etc/debian_version" ] ; then
				DISTNAME=deb
			fi
			LSB_RELEASE=`lsb_release -i -s`
			if [ "$LSB_RELEASE" = "SUSE LINUX" ] || [ "$LSB_RELEASE" = "openSUSE project" ] ||
				  [ "$LSB_RELEASE" = "ScientificCERNSLC" ] ; then
				PACKAGE_EXTRA_CONFIGURE="$PACKAGE_EXTRA_CONFIGURE --disable-static"
				DISTNAME=rpm
			fi
			# readdir_r is now deprecated. ignore
			USE_CFLAGS="-Wno-deprecated-declarations"
			MAKE=make
			;;
		FreeBSD)
			DISTNAME=freebsd
			MAKE=gmake
			CONFIGURE_FLAGS="LEX=/usr/local/bin/flex CXXFLAGS=-I/usr/local/include/flex"
			if [ -d "/usr/local/openjdk7" ] ; then
				SPECIAL_ENV="JAVA_HOME=/usr/local/openjdk7"
			elif [ -d "/usr/local/openjdk6" ] ; then
				SPECIAL_ENV="JAVA_HOME=/usr/local/openjdk6"
			fi
			DEPS_CMAKE_OPT="-DCMAKE_CXX_COMPILER=clang++"
			USE_CXXFLAGS="-Wno-tautological-compare"
			SPECIAL_ENV="$SPECIAL_ENV CC=clang CXX=clang++ CC_FOR_BUILD=clang CXX_FOR_BUILD=clang++"
			sed -i.bak "s/^AC_INIT(\[libximc$SOVERMAJOR\], \(.*\)$/AC_INIT(\[libximc\], \1/" configure.ac
			;;
		*)
			echo "Wrong distribution"
			exit 1
			;;
	esac
}

makedist()
{
	DIST=dist/ximc-$VER
	DISTLIB=$DIST/ximc
	DISTEXAM=$DIST/examples

	COPYFILE_DISABLE=true
	export COPYFILE_DISABLE

	if [ -d "$DIST" ] ; then
		echo "Dist already exists"
		exit 1
	fi
	mkdir -p $DISTLIB $DL

	echo Copying docs
	cp -R $DL/doc-en $DISTLIB/
	cp -R $DL/doc-ru $DISTLIB/
	cp -R $DL/doc-java $DISTLIB/
	
	echo Copying driver
	cp -R driver $DIST/

	echo Copying crossplatform data
	if [ -d "$DL/crossplatform" ] ; then
		cp -R $DL/crossplatform $DISTLIB/
	fi
	rm -r $DISTLIB/crossplatform/python/*
	cp $DL/crossplatform/python/dist/* $DISTLIB/crossplatform/python/

	echo Copying c-profiles
	if [ -d "$DL/../c-profiles" ] ; then
		cp -R $DL/../c-profiles $DISTLIB/
	fi
	
	echo Copying python-profiles
	if [ -d "$DL/../python-profiles" ] ; then
		cp -R $DL/../python-profiles $DISTLIB/
	fi

	echo Copying libraries
	for arch in deb rpm macosx win32 win64 ; do
		mkdir -p $DISTLIB/$arch
	done

	cp -R $DL/deb/*.deb $DISTLIB/deb/
	ls $DL/deb/
	for arch in amd64 i386 armhf ; do
		lib_dir=$(find $DL -name "debian-$arch")
		echo $arch
		if [ -n "$lib_dir" ]
		then
			mkdir -p $DISTLIB/debian-$arch
			cp -R $lib_dir/ $DISTLIB/debian-$arch/
		else
			echo No corresponding files
		fi
	done

	cp -R $DL/rpm/*.rpm $DISTLIB/rpm/

	cp -R $DL/macosx/libximc.framework $DISTLIB/macosx
	cp -R $DL/macosx/libjximc.jar $DISTLIB/macosx
	cp -R $DL/macosx/libjximc*dylib $DISTLIB/macosx

	for arch in win32 win64 ; do
		cp -R $DL/$arch/libximc.* $DISTLIB/$arch/
		cp -R $DL/$arch/bindy.dll $DISTLIB/$arch/
		cp -R $DL/$arch/bindy.lib $DISTLIB/$arch/
		cp -R $DL/$arch/xiwrapper.dll $DISTLIB/$arch/
		if [ -f $DL/$arch/libjximc.dll ] ; then
			cp -R $DL/$arch/libjximc.* $DISTLIB/$arch/
		fi
	done

	for arch in win32 win64 ; do
		mkdir -p $DISTLIB/$arch/wrappers/csharp
		cp $DL/$arch/ximcnet.cs $DISTLIB/$arch/wrappers/csharp
		cp $DL/$arch/ximcnet.dll $DISTLIB/$arch/wrappers/csharp
	done

	for arch in win32 win64 macosx ; do
		mkdir -p $DISTLIB/$arch/wrappers/matlab
		cp $DL/win64/wrappers/matlab/ximcm.h $DISTLIB/$arch/wrappers/matlab
	done

	mkdir -p $DISTLIB/win32/wrappers/delphi
	cp -R $DL/win32/ximc.pas $DISTLIB/win32/wrappers/delphi

	cp -R $DL/win64/wrappers/matlab/* $DISTLIB/win64/wrappers/matlab

	cp -R third-party/vcredist/vcredist_x86.exe $DISTLIB/win32/
	cp -R third-party/vcredist/vcredist_x64.exe $DISTLIB/win64/

	echo Copying ximc.h
	cp $DL/macosx/ximc.h $DISTLIB/
	
	echo Copying license
	cp COPYING $DISTLIB/LICENSE.txt

	mkdir $DISTEXAM
	for example in test_C test_CSharp test_VBNET test_Delphi test_MATLAB test_Python test_LabWindows; do
		echo Copying example $example
		cp -R examples/$example $DISTEXAM/
	done

	for example in testapp_C testappeasy_C testprofile_C; do
		echo Cleaning example $example
		rm -f $DISTEXAM/test_C/$example/Makefile.am
		echo Copying compiled example $example
		for arch in macosx win32 win64 ; do
			mkdir $DISTEXAM/test_C/$example/compiled-$arch
		done
		
		cp -R $DL/macosx/$example.app $DISTEXAM/test_C/$example/compiled-macosx/
		cp -R $DL/win32/$example-compiled-win32/* $DISTEXAM/test_C/$example/compiled-win32/
		cp -R $DL/win64/$example-compiled-win64/* $DISTEXAM/test_C/$example/compiled-win64/
	done
	
	for example in testapp_C testappeasy_C; do
		echo Copying compiled example for codeblocks $example
		for arch in macosx win32 win64 ; do
			mkdir $DISTEXAM/test_C/$example/cb_compiled-$arch
		done
		
		cp -R $DL/macosx/$example.app $DISTEXAM/test_C/$example/cb_compiled-macosx/
		cp -R $DL/win32/$example-cb_compiled-win32/* $DISTEXAM/test_C/$example/cb_compiled-win32/
		cp -R $DL/win64/$example-cb_compiled-win64/* $DISTEXAM/test_C/$example/cb_compiled-win64/
	done
	rm -f $DISTEXAM/test_Python/Makefile
		
	for example in test_CSharp test_VBNET; do
		echo Copying compiled example $example
		for arch in win32 win64 ; do
			mkdir -p $DISTEXAM/$example/compiled-$arch
			cp -R $DL/$arch/$example-compiled-$arch/* $DISTEXAM/$example/compiled-$arch/
		done
	done

	for example in test_Delphi ; do
		echo Copying compiled example $example
		mkdir -p $DISTEXAM/$example/compiled-win32
		cp $DL/win32/$example.exe $DISTEXAM/$example/compiled-win32
		cp -R $DL/win32/libximc.* $DISTEXAM/$example/compiled-win32
		cp -R $DL/win32/bindy.dll $DISTEXAM/$example/compiled-win32
		cp -R $DL/win32/bindy.lib $DISTEXAM/$example/compiled-win32
		cp -R $DL/win32/xiwrapper.dll $DISTEXAM/$example/compiled-win32
	done
	
	for example in test_LabWindows ; do
		for namexample in testcli testgui ; do
			echo Copying example $example/$namexample
			cp -R $DL/win32/libximc.* $DISTEXAM/$example/$namexample
			cp -R $DL/win32/bindy.dll $DISTEXAM/$example/$namexample
			cp -R $DL/win32/bindy.lib $DISTEXAM/$example/$namexample
			cp -R $DL/win32/xiwrapper.dll $DISTEXAM/$example/$namexample
		done
	done

	for example in test_Java ; do
		echo Copying compiled example $example
		mkdir -p $DISTEXAM/$example/compiled
		mkdir -p $DISTEXAM/$example/compiled-win32
		mkdir -p $DISTEXAM/$example/compiled-win64
		# it's okay to get one of these jars but -source/-target was not specified
		cp $DL/macosx/$example.jar $DISTEXAM/$example/compiled
		cp $DL/macosx/$example.jar $DISTEXAM/$example/compiled-win32
		cp $DL/macosx/$example.jar $DISTEXAM/$example/compiled-win64
		cp $DL/macosx/java-README.txt $DISTEXAM/$example/README.txt
		for arch in win32 win64 ; do
			cp -R $DL/$arch/libximc.* $DISTEXAM/$example/compiled-$arch
			cp -R $DL/$arch/bindy.dll $DISTEXAM/$example/compiled-$arch
			cp -R $DL/$arch/bindy.lib $DISTEXAM/$example/compiled-$arch
			cp -R $DL/$arch/xiwrapper.dll $DISTEXAM/$example/compiled-$arch
			if [ -f $DL/$arch/libjximc.dll ] ; then
				cp -R $DL/$arch/libjximc.* $DISTEXAM/$example/compiled-$arch
			fi
		done		
	done

	echo Fetching sources
	CURREV=`$GIT show-ref --hash --head HEAD`
	if [ -z "$CURREV" ] ; then
		echo Can\'t determine current revision
		exit 1
	fi
	echo Using revision $CURREV
	$GIT clone . dist/ximc-$VER-src
	$GIT -C dist/ximc-$VER-src checkout $CURREV
	rm -rf dist/ximc-$VER-src/.hg* dist/ximc-$VER-src/.git* dist/ximc-$VER-src/docs

	find dist/ximc-$VER* \( -name .DS_Store -or -name \*.swp -or -name '._*' \) -print -delete

	tar -C dist -czf dist/ximc-$VER.tar.gz ximc-$VER
	tar -C dist -czf dist/ximc-$VER-src.tar.gz ximc-$VER-src

	unset COPYFILE_DISABLE
}

clean()
{
	./clean_all.sh
}

clean_all_modified()
{
	echo ATTENTION! Cleaning all modified and new files!
	$GIT reset --hard
	$GIT clean -xdf
	echo Dumping stat...
	$GIT status
}

build_to_local()
{
	DL=ximc
	DISTLATEST=$DL/$DISTNAME
	#USE_CPPFLAGS="-I$DEPS/xiwrapper"
	USE_CFLAGS="$USE_CFLAGS -Wall -Werror -Wextra -Wshadow -Wno-switch"
	USE_CXXFLAGS="$USE_CXXFLAGS -Wall -Werror -Wextra -Wshadow -Wno-switch -Wno-unused-parameter -Wno-parentheses"

	echo Using env $SPECIAL_ENV

	# prevent copying os x extended attributes
	COPYFILE_DISABLE=true
	export COPYFILE_DISABLE

	rm -rf $DISTLATEST
	clean
	rm -rf $LOCAL
	mkdir -p $LOCAL $DL $DISTLATEST

	./autogen.sh
	echo Invoke ./configure CFLAGS="$USE_CFLAGS" CXXFLAGS="$USE_CXXFLAGS" \
		CPPFLAGS="$USE_CPPFLAGS" LDFLAGS="$USE_LDFLAGS" \
		$CONFIGURE_FLAGS --prefix=$LOCAL --with-xiwrapper=$DEPS/xiwrapper --with-miniupnpc=$DEPS/miniupnpc $*

	env $SPECIAL_ENV ./configure CFLAGS="$USE_CFLAGS" CXXFLAGS="$USE_CXXFLAGS" \
		CPPFLAGS="$USE_CPPFLAGS" LDFLAGS="$USE_LDFLAGS" \
		$CONFIGURE_FLAGS --prefix=$LOCAL --with-xiwrapper=$DEPS/xiwrapper --with-miniupnpc=$DEPS/miniupnpc $*
	
	if [ -d "$VNAME" ] ; then
		chmod -R 777 "$VNAME"
		rm -rf $VNAME
	fi

	if [ -z "$TARGETS" ] ; then
		TARGETS="all distcheck install"
	fi

	env $SPECIAL_ENV $MAKE $TARGETS DISTCHECK_CONFIGURE_FLAGS="$PACKAGE_EXTRA_CONFIGURE"
	unset COPYFILE_DISABLE
	rm -rf $VNAME

	copydist
}

copydist()
{
	DL=ximc
	DISTLATEST=$DL/$DISTNAME

	rm -rf $DISTLATEST
	mkdir -p $DISTLATEST
	cp -a $LOCAL/include/* $LOCAL/lib*/* $DISTLATEST
	if [ -d "$LOCAL/share/doc" ] ; then
		cp -a $LOCAL/share/doc/libximc*/* $DISTLATEST
	fi
	if [ -d "$LOCAL/share/java" ] ; then
		cp -a $LOCAL/share/java/*.jar $DISTLATEST
	fi
}

build_dep_bindy()
{
	if [ -z "$URL_BINDY" ] ; then
	  URL_BINDY="https://github.com/EPC-MSU/Bindy.git"
	fi
	echo "--- Building bindy ---"
	if [ "x$SKIP_DEPS_CHECKOUT" != "xyes" ] ; then
		rm -rf $DEPS/bindy
		(cd $DEPS && git clone --recursive $URL_BINDY bindy)
		(cd $DEPS/bindy && git checkout $BINDYVER)
		(cd $DEPS/bindy && git submodule update --init --recursive)
		(cd $DEPS/bindy && git submodule update --recursive)
	fi
	(cd $DEPS/bindy && git --no-pager show --stat $BINDYVER)
	(cd $DEPS/bindy && cmake $DEPS_CMAKE_OPT $* .)
	$MAKE -C $DEPS/bindy
}

build_dep_xiwrapper()
{
	if [ -z "$URL_XIWRAPPER" ] ; then
	  URL_XIWRAPPER="https://gitlab.ximc.ru/ximc-public/libxiwrapper.git"
	fi
	echo "--- Building xiwrapper ---"
	if [ "x$SKIP_DEPS_CHECKOUT" != "xyes" ] ; then
		rm -rf $DEPS/xiwrapper
		(cd $DEPS && git clone $URL_XIWRAPPER xiwrapper) || false
		(cd $DEPS/xiwrapper && git checkout $XIWRAPPERVER) || false
	fi
	(cd $DEPS/xiwrapper && git --no-pager show --stat $XIWRAPPERVER) || false
	(cd $DEPS/xiwrapper && cmake -DBINDY_PATH=$DEPS/bindy $DEPS_CMAKE_OPT $* .) || false
	$MAKE -C $DEPS/xiwrapper
	cp -a $DEPS/bindy/libbindy.* $DEPS/xiwrapper/
}

build_dep_miniupnpc()
{
	if [ -z "$URL_MINIUPNPC" ] ; then
	  URL_MINIUPNPC="https://github.com/EPC-MSU/miniupnpc"
	fi

	echo "--- Building miniupnpc ---"
	if [ "x$SKIP_DEPS_CHECKOUT" != "xyes" ] ; then
		rm -rf $DEPS/miniupnpc-dist $DEPS/miniupnpc
		(cd $DEPS && git clone $URL_MINIUPNPC miniupnpc-dist)
		(cd $DEPS/miniupnpc-dist && git checkout $MINIUPNPCVER)
	fi
	# cmake 3.5 is needed
	(cd $DEPS/miniupnpc-dist && cmake $DEPS_CMAKE_OPT \
		-DUPNPC_BUILD_TESTS=OFF -DUPNPC_BUILD_SAMPLE=OFF -DUPNPC_BUILD_SHARED=OFF \
		-DCMAKE_INSTALL_LIBDIR=lib \
		-DCMAKE_INSTALL_PREFIX=$DEPS/miniupnpc $* .)
	(cd $DEPS/miniupnpc-dist && cmake --build .)
	(cd $DEPS/miniupnpc-dist && cmake --build . --target install)
}


build_depends()
{
	echo Building depends with flags $*
	mkdir -p $DEPS
	build_dep_bindy $*
	build_dep_xiwrapper $*
	build_dep_miniupnpc $*
}

build_deb_package()
{
	export PACKAGE_EXTRA_CONFIGURE

	mkdir -p $PKGROOT
	tar -C $PKGROOT -xf $BASEROOT/$VNAME.tar.gz
	cd $PKGROOT/$VNAME
	dpkg-buildpackage -D -tc -us -uc -rfakeroot $*

	echo Copying dist...
	LDIST=$BASEROOT/$DL/deb/
	mkdir -p $LDIST
	rm -rf $LDIST/*
	cp $PKGROOT/libximc*deb $LDIST

	find $LDIST -name '*.deb' | xargs -L1 lintian -v --fail-on-warnings

	rm -rf $PKGROOT $BASEROOT/$VNAME.tar.gz
	cd $BASEROOT
}

build_rpm_package()
{
	rm -rf $PKGROOT
	mkdir -p $PKGROOT $PKGROOT/BUILD $PKGROOT/RPMS $PKGROOT/SOURCES $PKGROOT/SPECS $PKGROOT/SRPMS
	cp rpm/libximc.spec $PKGROOT/SPECS
	cp $VNAME.tar.gz $PKGROOT/SOURCES

	echo Using archive `pwd`/$VNAME.tar.gz
	rpmbuild -bb --clean -D "%_topdir $PKGROOT" -D "%_package_extra_configure $PACKAGE_EXTRA_CONFIGURE" $PKGROOT/SPECS/libximc.spec

	echo Copying dist...
	LDIST=$BASEROOT/$DL/rpm/
	mkdir -p $LDIST
	rm -rf $LDIST/*
	cp $PKGROOT/RPMS/**/*rpm $LDIST

	find $LDIST -name '*.rpm' | xargs -L1 rpmlint

	rm -rf $PKGROOT $BASEROOT/$VNAME.tar.gz
	cd $BASEROOT
}

build_osx_impl()
{
	clean
	build_depends
	build_to_local --with-xcode-build $*
	# Override JNI lib with a jni library linked to framework
	make -C wrappers/java/src/c framework-build
	rm -f $DL/$DISTNAME/libjximc*dylib $DL/$DISTNAME/libjximc*a
	cp $LOCAL/lib/libjximc.dylib $DL/$DISTNAME/
	for exam in testapp_C testappeasy_C testprofile_C; do
		(cd examples/test_C/$exam && xcodebuild LIBXIMC_LIB_PATH=../../$DL/$DISTNAME) || false
		cp -a examples/test_C/$exam/build/Release/$exam.app $DL/$DISTNAME/
	done
	(cd examples/test_Java && $MAKE) || false
	cp -a examples/test_Java/test_Java.jar $DL/$DISTNAME/
	cp -a examples/test_Java/README.txt $DL/$DISTNAME/java-README.txt
	mkdir -p $DL/crossplatform/wrappers/
	cp -r wrappers/python $DL/crossplatform/wrappers/
}

echo XIMC build script
trap exit_clean_up EXIT INT TERM
ACTION=$1
shift

# configure env
if [ "$ACTION" != "cleandist" ] && [ "$ACTION" != "clean" ] ; then
	configure_dist
	if [ -z "$DISTNAME" ] ; then
		echo Unknown dist
		exit 1
	fi
fi

# determine action
case $ACTION in
depends)
	build_depends $*
	;;

lib)
	build_depends
	build_to_local --with-docs $*
	;;

libfast)
	build_depends
	TARGETS="all install" build_to_local --without-docs $*
	;;

onlydocs)
	build_depends
	build_to_local --with-docs $*
	mkdir -p _tmp
	mv $DL/$DISTNAME/doc-* _tmp/
	rm -rf $DL/*
	mv _tmp/doc-* $DL/
	rm -rf _tmp
	;;

onlydist)
	copydist
	;;

makedist)
	makedist
	;;

libosxci)
	# do not call distcheck target for osx CI build
	# to avoid building docs, #48562
	TARGETS="all dist install" \
		build_osx_impl --without-docs $*
	;;

libosx)
	build_osx_impl --with-docs $*
	;;

libdeb)
	clean
	# need to clean deps because something could be left

	build_depends	-DNO_RPATH_PACKAGING=TRUE
	if uname -m | grep -q arm ; then
		# do not call distcheck target, only dist
		TARGETS="all dist install" build_to_local --with-docs
	else
		build_to_local --with-docs
	fi
	build_deb_package
	;;

librpm)
	clean
	build_depends	-DNO_RPATH_PACKAGING=TRUE
	build_to_local --with-docs
	build_rpm_package
	;;

libfreebsd)
	echo Packaging FreeBSD is not supported
	exit 1
	;;

genfwheader)
	./xigen/src/xigen -i libximc/src/protocol.xi --gen-fw-header -x version -o fwprotocol.h  -t ./xigen/src/fwprotocol-template.h
	;;

genfwlib)
	./xigen/src/xigen -i libximc/src/protocol.xi --gen-fw-lib -x version -o fwprotocol.c -t ./xigen/src/fwprotocol-template.c
	;;

genwikiru)
	./xigen/src/xigen -i libximc/src/protocol.xi --gen-wiki -x version --language russian -o protocol_ru.wiki
	;;

genwikien)
	./xigen/src/xigen -i libximc/src/protocol.xi --gen-wiki -x version --language english -o protocol_en.wiki
	;;

abicc-dump)
	DUMP_VER=`hg identify -t`
	if [ "$DUMP_VER" = "tip" ] || [ -z "$DUMP_VER" ] ; then
		DUMP_VER=`hg identify -i | sed 's/\+/m/'`
	fi
	echo Using dump version $DUMP_VER
cat <<EOF > $BASEROOT/abicc-"$DUMP_VER".xml
<?xml version=\"1.0\" encoding=\"utf-8\"?>
<descriptor>
<version>$DUMP_VER</version>
<headers>$BASEROOT/dist/local/include/ximc.h</headers>
<libs>$BASEROOT/dist/local/lib/libximc.so</libs>
<skip_constants>LIBXIMC_VERSION</skip_constants>
</descriptor>
EOF
	build_depends
	TARGETS="all install" USE_CFLAGS=-g build_to_local --without-docs $*
	abi-compliance-checker -lib ximc -dump abicc-"$DUMP_VER".xml -dump-path ximc_"$DUMP_VER".abi.tar.gz
	;;

clean)
	clean
	;;

cleandist)
	clean
	clean_all_modified
	rm -rf $DL/* $LOCAL
	;;

*)
	echo "Usage: $0 {depends | lib | libfast | onlydocs | onlydist | makedist |"
		echo "   libosx | libdeb | librpm |"
		echo "   genfwheader | genfwlib | genwikiru | genwikien |"
		echo "   assemblyprofile | assemblywikipageen | assemblywikipageru |"
		echo "   clean | cleandist }"
	exit 1
esac
# vim: noet
