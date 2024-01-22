#!/bin/bash

WORKING_DIR=$(pwd) # current/working directory
LIBRARY_PATH=$WORKING_DIR/../../../ximc/crossplatform/wrappers/python/libximc/library-files/
LINUX_ARCH=$(uname -m)
echo Current architecture: $LINUX_ARCH
case $LINUX_ARCH in
x86_64) 
  FULL_LIBRARY_PATH=$LIBRARY_PATH/debian-amd64
  ;;

i386)
  FULL_LIBRARY_PATH=$LIBRARY_PATH/debian-i386
  ;;

i686)
  FULL_LIBRARY_PATH=$LIBRARY_PATH/debian-i386
  ;;
*)
  FULL_LIBRARY_PATH=None
  echo "There is no binaries for this architecture."
  echo "To run example you can try to build libximc from sources for your architecture (with no warranty):"
  echo "https://github.com/EPC-MSU/libximc"
  ;;
esac

if [ $FULL_LIBRARY_PATH != "None" ]
then
  echo "${FULL_LIBRARY_PATH}"
  export LD_LIBRARY_PATH=${FULL_LIBRARY_PATH}
  python3 Extendtestpython.py
fi
