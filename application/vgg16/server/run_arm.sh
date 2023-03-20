#!/bin/bash

sudo killall python3
sudo rm -rf tmp 
mkdir tmp
for port in {10001..10020}
do
	python3 server_udp_arm.py -H 10.50.1.16 -P $port &
done
