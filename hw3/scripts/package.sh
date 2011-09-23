#!/bin/bash

SCRIPT_PATH="`dirname $0`"
TESTS_DIR="$SCRIPT_PATH/../tests"
BUILD_DIR="$SCRIPT_PATH/../build"
SRC_DIR="$SCRIPT_PATH/../src"

(
cd $SRC_DIR
zip -r $BUILD_DIR/hw2.zip *
)
(
cd $TESTS_DIR
zip -r $BUILD_DIR/hw2_tests.zip *
)
