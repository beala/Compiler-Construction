#!/bin/bash

SCRIPT_PATH="`dirname $0`"
TESTS_DIR="$SCRIPT_PATH/../tests"
BUILD_DIR="$SCRIPT_PATH/../build"
SRC_DIR="$SCRIPT_PATH/../src"

rm $TESTS_DIR/*.s
rm $BUILD_DIR/*
rm $SRC_DIR/*.pyc
