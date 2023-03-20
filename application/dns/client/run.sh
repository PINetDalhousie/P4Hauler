#!/bin/bash

rate=$1
sudo killall python3
echo $((rate*8))
for i in {1..8}
do
    python3 oldclient.py --server 10.50.1.6:5053 -R $rate example.com &
done
