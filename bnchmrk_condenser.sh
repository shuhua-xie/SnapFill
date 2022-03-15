#!/bin/bash

if [[ $# -ne 2 ]]
then
  echo "Usage: ./bnchmark_condenser [dir_in_name] [dir_out_name]"
  exit 1
fi

for f in benchmarks_randlines/*:
do
	rm $f
done

for f in $1/*.csv
do
  python3 rand_lines.py $f 10 $2
  echo $f done
done
