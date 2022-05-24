#!/bin/bash

PATTERN=$1
if [ "$#" -eq 3 ]; then
    MIN=$2
    MAX=$3
else
    MIN=0
    MAX=$2
fi

# Anything written to this file will be sent to the Bwb output named "sequence"
OUTPUT_FILE="/tmp/output/output_seq"

# For each number i in [MIN, MAX], call printf to format the pattern with
# i. Print brackets and commas to make the output a valid JSON array, allowing
# it to be parsed as a list by Bwb
printf "[" > $OUTPUT_FILE
for i in `seq $MIN $MAX`;
do
    printf "\"$PATTERN\"" $i >> $OUTPUT_FILE
    # Output a comma if this is not the last item
    if [ "$i" -lt "$MAX" ]; then
	printf  ", " >> $OUTPUT_FILE
    fi
done
echo "]" >> $OUTPUT_FILE
