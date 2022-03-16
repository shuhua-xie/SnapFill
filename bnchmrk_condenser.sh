#!/bin/bash

if [[ $# -ne 2 ]] && [[ $# -ne 3 ]]
then
  echo "Usage: ./bnchmark_condenser [dir_in_name] [dir_out_name] [test_dir_out_name]"
  exit 1
fi

for f in $1/*.csv
do
  if [[ $# -eq 3 ]]
  then
    python3 rand_lines.py $f 3 $2 $3
  else
    python3 rand_lines.py $f 3 $2 -n
  fi
  echo $f done
done
