#!/bin/bash

if [[ $# -ne 1 ]] && [[ $# -ne 2 ]]
then
  echo "Usage: ./bnchmark_tester [dirname] [python_out_dir]"
  exit 1
fi

for f in $1/*.csv
do
  tmp=${f%.*}
  echo "----- $f start -----"
  echo "BlinkFill (Our Impl)"
  if [[ $# -eq 1 ]]
  then
    time timeout --foreground 10m python3 SnapFill.py $f -fd
  else
    time timeout --foreground 10m python3 SnapFill.py $f -fd -o "$2/Blink_${tmp##*/}.py"
  fi
  echo
  echo "SnapFill"
  if [[ $# -eq 1 ]]
  then
    time timeout --foreground 10m python3 SnapFill.py $f -d
  else
    time timeout --foreground 10m python3 SnapFill.py $f -d -o "$2/Snap_${tmp##*/}.py"
  fi
  echo "----- $f end -----"
  echo
done
