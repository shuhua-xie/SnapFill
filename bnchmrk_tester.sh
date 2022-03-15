#!/bin/bash

if [[ $# -ne 1 ]]
then
  echo "Usage: ./bnchmark_tester [dirname]"
  exit 1
fi

for f in $1/*.csv
do
  echo "----- $f start -----"
  echo "BlinkFill (Our Impl)"
  time timeout --foreground 20m python3 SnapFill.py $f -fd
  echo "SnapFill"
  time timeout --foreground 20m python3 SnapFill.py $f -d
  echo "----- $f end -----"
  echo
done
