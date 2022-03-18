#!/bin/bash

# remove multiple input sl constraints and make csvs
#echo "cleaning directories"
#./benchmark_cleaner.sh benchmarks_micro/
#./benchmark_cleaner.sh benchmarks_short/
#./benchmark_cleaner.sh benchmarks_long/

# remove pre-processed files
echo "removing pre-existing randomly generated data"
for f in benchmarks_*_randlines/*
do
	rm $f
done
for f in benchmarks_rand_tests/*
do
	rm $f
done
for f in benchmarks_rand_py/*
do
	rm $f
done

# process long files
echo "Generating random samples"
./bnchmrk_condenser.sh benchmarks_short benchmarks_short_randlines/
./bnchmrk_condenser.sh benchmarks_long benchmarks_long_randlines/ benchmarks_rand_tests/
# test
rm results_benchmarks_*.txt
echo "Running micro benchmarks"
./bnchmrk_tester.sh benchmarks_micro &> results_benchmarks_micro.txt
echo "Running short benchmarks"
./bnchmrk_tester.sh benchmarks_short_randlines &> results_benchmarks_short.txt
echo "Running long benchmarks"
./bnchmrk_tester.sh benchmarks_long_randlines benchmarks_rand_py &> results_benchmarks_long.txt
