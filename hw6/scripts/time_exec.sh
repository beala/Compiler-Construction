#!/bin/bash
# Desc: ./script prog1 prog2 data_file
# Executes prog1 and prog2 100 times and prints the wall time of execution to data_file

# Init
PROG1="$1"
PROG2="$2"
echo $PROG1 , $PROG2
DATA_FILE="$3"
# If you don't specify the number of trails, set it to 100
if [ $# -eq 4 ]; then
	TRIALS="$4"
else
	TRIALS=100
fi

# Functions
# Execute the first arg and return the wall time of execution
function get_wall_exec_time(){
	PROG_PATH="$1"
	#Awk grabs the 1st line of the 2nd column
	#'time' sends info to stderr
	#'2>$1 > /dev/null' sends stdout to null and redirects stderr to stdout
	(time -p "$PROG_PATH") 2>&1 | awk '{if (NR == 1) print $2}'
}

# MAIN PROGRAM
for i in $( seq 1 "$TRIALS" ); do 
	P1_TIME=$(get_wall_exec_time "$PROG1")
	P2_TIME=$(get_wall_exec_time "$PROG2")
	echo "$P1_TIME , $P2_TIME" >> "$DATA_FILE"
	echo "$P1_TIME , $P2_TIME"
done
