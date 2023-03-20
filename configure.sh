#!/bin/bash

source /home/carson/set_sde.sh
veth_setup.sh


ifconfig veth0 10.50.0.1 up
ifconfig veth2 10.50.0.6 up
ifconfig veth4 10.50.0.16 up
