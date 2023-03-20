#!/bin/bash

ip=$1
rate=$2
sudo killall python3
echo $((rate*4))
for i in {1..2}
do
    python3 client_udp_multi_ports.py -H $ip -N $((rate*10)) -R $rate &
done
