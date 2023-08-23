#!/bin/bash

sudo killall python3
for port in {10001..10020}
do
	#python3 server_knn_x86.py -P $port &
	python3 server_knn_x86.py -H 10.50.1.6 -P $port &
done
