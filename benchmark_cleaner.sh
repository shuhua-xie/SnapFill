#!/bin/bash

if [[ $# -ne 1 ]]
then
  echo "Usage: ./bnchmark_tester [dirname]"
  exit 1
fi

cd $1
grep -lr 'constraint (= (f "[^"]*" "' | xargs -L1 rm
for f in *.sl
do
  python3 ../clean_sl.py $f
done
cd ..
