#!/bin/bash

# remove multiple input sl constraints and make csvs
./benchmark_cleaner.sh benchmarks_short/
./benchmark_cleaner.sh benchmarks_long/
# process long files
./bnchmrk_condenser.sh benchmarks_large/ benchmarks_randlines
# test
./bnchmrk_tester.sh benchmarks_short &> results_benchmarks_short.txt
./bnchmrk_tester.sh benchmarks_randlines &> results_benchmarks_randlines.txt
