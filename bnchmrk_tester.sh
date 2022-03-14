#!/bin/bash

for f in benchmarks/*.csv
do
  echo "----- $f start -----"
  echo "FlashFill (Our Impl)"
  time python3 SnapFill.py $f -fd
  echo "SnapFill"
  time python3 SnapFill.py $f -d
  echo "----- $f end -----"
  echo
done
