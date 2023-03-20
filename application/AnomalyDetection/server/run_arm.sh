#!/bin/bash

sudo killall python3
sudo taskset -c 1 python3 server_ad_arm.py -H 10.50.1.16 -P 10001 &
sudo taskset -c 2 python3 server_ad_arm.py -H 10.50.1.16 -P 10002 &
