#!/bin/bash

sudo killall python3
sudo taskset -c 1 python3 server_ad_udp.py -H 10.50.1.6 -P 10001 &
sudo taskset -c 1 python3 server_ad_udp.py -H 10.50.1.6 -P 10002 &
