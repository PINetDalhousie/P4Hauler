#!/bin/bash

rm -rf log
mkdir log
for rate in {60..200..20}
do
    echo host $rate
    python3 client_udp_multi_ports.py -H 10.50.1.6 -N $((30*rate)) -R $rate > ./log/$rate.log
    sleep 10
done
