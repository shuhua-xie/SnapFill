#!/bin/bash

for f in `cat results_conditionals_py.txt`
do
  echo "Testing $f ----------"
  t="${f%%_randlines*}_test.csv"
  s="${f%%_randlines*}_sol.csv"
  testfile="benchmarks_short_tests/${t##*/Snap_}"
  outfile="benchmarks_short_tests/snap-${t##*/Snap_}"
  solfile="benchmarks_short_tests/${s##*/Snap_}"
  echo "Number of lines: `wc -l  $testfile`"
  python3 $f $testfile
  echo
  echo "File:"
  cat $outfile
  echo
  echo "# of examples SnapFill failed: `diff $solfile $outfile -y --suppress-common-lines |wc -l` "
  echo "Done with $f ---------"
  echo
done
