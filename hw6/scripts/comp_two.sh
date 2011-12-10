#!/bin/bash

SCRIPT_PATH="`dirname $0`"
TESTS_DIR="$SCRIPT_PATH/../tests"
BUILD_DIR="$SCRIPT_PATH/../build"
SRC_DIR="$SCRIPT_PATH/../src"

rm $(dirname $TESTS_DIR/$1)/*.s
rm $BUILD_DIR/*

FILE=$TESTS_DIR/$1

#for FILE in $TESTS_DIR/*.py
#do
	NOEXT=${FILE%.py}
	NOEXT_BASE=`basename $NOEXT`
	EXE=$BUILD_DIR/`basename $NOEXT`
	
	# Compile each file and run through gcc
	python $SRC_DIR/compile.py -O $FILE
	mv $NOEXT.s $NOEXT-opt.s
	
	python $SRC_DIR/compile.py $FILE
	mv $NOEXT.s $NOEXT-unopt.s

	# Note: WARNING MESSAGES ARE OFF
	gcc -m32 -lm -w "$NOEXT-opt.s" $SRC_DIR/*.c -o $EXE-opt -g
	if [ $? != 0 ]; then
		echo "$NOEXT_BASE-opt.s gcc compile failed!"
		break
	fi
	# Note: WARNING MESSAGES ARE OFF
	gcc -m32 -lm -w "$NOEXT-unopt.s" $SRC_DIR/*.c -o $EXE-unopt -g
	if [ $? != 0 ]; then
		echo "$NOEXT_BASE-unopt.s gcc compile failed!"
		break
	fi

#done
