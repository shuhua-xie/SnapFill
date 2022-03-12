#!/bin/bash

cd benchmarks/
grep -lr 'constraint (= (f "[^"]*" "' | xargs -L1 rm
for f in *.sl
do
  python3 ../clean_sl.py $f
done
cd ..
