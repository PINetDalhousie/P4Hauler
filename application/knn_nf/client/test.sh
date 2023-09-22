#!/bin/bash


rm -rf results
mkdir results

for rate in {20..40..5}
do
    for i in {1..10}
    do
        echo $rate $i
        python3 client_udp_multi_ports.py -H 10.50.1.100 -N 500 -R $rate  >> ./results/$rate.log
        sleep 15
    done
done
