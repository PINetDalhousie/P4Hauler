#!/bin/bash


rm -rf results
mkdir results

for rate in 8 10 12 14 16 18 20
do
    for i in {1..10}
    do
        echo $rate $i
        python3 client_udp_multi_ports.py -H 10.50.1.6 -N 500 -R $rate  >> ./results/$rate.log
        sleep 15
    done
done
