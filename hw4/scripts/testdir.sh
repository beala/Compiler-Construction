#!/bin/bash

SCRIPT_PATH="`dirname $0`"
TESTS_DIR="$SCRIPT_PATH/../tests"
BUILD_DIR="$SCRIPT_PATH/../build"
SRC_DIR="$SCRIPT_PATH/../src"

TESTS_DIR="$SCRIPT_PATH/$1"

rm $TESTS_DIR/*.s
rm $BUILD_DIR/*

for FILE in $TESTS_DIR/*.py
do
	NOEXT=${FILE%.py}
	NOEXT_BASE=`basename $NOEXT`
	EXE=$BUILD_DIR/`basename $NOEXT`
	
	# Compile each file and run through gcc
	python $SRC_DIR/compile.py $FILE

	# Note: WARNING MESSAGES ARE OFF
	gcc -m32 -lm -w "$NOEXT.s" $SRC_DIR/*.c -o $EXE
	if [ $? != 0 ]; then
		echo "$NOEXT_BASE gcc compile failed!"
		break
	fi

	#Compare the output of the compiled filed to the
	#output of the python interpreter
	cat "$NOEXT.in" | $EXE > $EXE.a.out
	cat "$NOEXT.in" | python $FILE > $EXE.py.out
	diff $EXE.a.out $EXE.py.out
	if [ $? != 0 ]; then
		echo "$NOEXT_BASE failed!"
		#break
	else
		echo "$NOEXT_BASE passed!"
	fi
done
