#!/bin/bash

sudo killall python3
for port in {10001..10020}
do
	python3 server_knn_arm.py -H 10.50.1.16 -P $port &
done
