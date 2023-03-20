#!/bin/bash

rm *.pdf

for file in *.py;
do
  python3 $file -s 1;
done
