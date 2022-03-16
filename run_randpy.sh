#!/bin/bash

for f in benchmarks_rand_py/Blink_*
do
  echo "Testing $f ----------"
  tmp="${f##*/Blink_}"
  Snap_py="benchmarks_rand_py/Snap_${tmp}"
  t="${f%%_randlines*}_test.csv"
  s="${f%%_randlines*}_sol.csv"
  testfile="benchmarks_rand_tests/${t##*/Blink_}"
  outfile="benchmarks_rand_tests/snap-${t##*/Blink_}"
  solfile="benchmarks_rand_tests/${s##*/Blink_}"
  echo "Number of lines: `wc -l  $testfile`"
  python3 $f $testfile
  echo
  echo "File:"
  cat $solfile
  echo
  echo "# of examples BlinkFill failed: `diff $solfile $outfile -y --suppress-common-lines |wc -l` "
  python3 $Snap_py $testfile
  echo
  echo "File:"
  cat $solfile
  echo
  echo "# of examples BlinkFill failed: `diff $solfile $outfile -y --suppress-common-lines |wc -l` "
  echo "Done with $f ---------"
  echo
done
