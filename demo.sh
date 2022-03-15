#!/bin/bash

echo "Goal: Format phone numbers as ###-###-####"
echo
echo "Start with BlinkFill implementation"
echo 'python3 SnapFill.py demo/phone-nums-easy.csv -f'
read
python3 SnapFill.py demo/phone-nums-easy.csv -f
read
echo "SnapFill can do the same"
read
echo 'python3 SnapFill.py demo/phone-nums-easy.csv'
python3 SnapFill.py demo/phone-nums-easy.csv
read

echo "Now let this process some inputs"
read
echo "python3 SnapFill.py demo/phone-nums-easy.csv -o nums-easy.py"
python3 SnapFill.py demo/phone-nums-easy.csv -o nums-easy.py
echo "python3 nums-easy.py demo/empty-phone-nums-easy.csv"
python3 nums-easy.py demo/empty-phone-nums-easy.csv
echo "The output is at demo/snap-empty-phone-nums-easy.csv"
read

echo "Let's try again with correct examples"
read
echo 'python3 SnapFill.py demo/phone-nums.csv -f'
python3 SnapFill.py demo/phone-nums.csv -f
read
echo "SnapFill can solve it!"
read
echo 'python3 SnapFill.py demo/phone-nums.csv'
python3 SnapFill.py demo/phone-nums.csv
read

echo "Now let's try on even more inputs"
read
echo "python3 SnapFill.py demo/phone-nums.csv -o nums.py"
python3 SnapFill.py demo/phone-nums.csv -o nums.py
echo "python3 nums.py demo/empty-phone-nums.csv"
python3 nums.py demo/empty-phone-nums.csv
echo "The output is at demo/snap-empty-phone-nums.csv"
read
echo "We can see that it's not ideal, the regex matches for alphanumeric characters instead of just numeric ones"
echo "To fix small issues like this, we have a shell!"
read
echo "python3 SnapFill.py demo/phone-nums.csv -s" 
python3 SnapFill.py demo/phone-nums.csv -s
