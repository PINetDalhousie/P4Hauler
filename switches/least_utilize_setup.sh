#!/bin/bash

rm -rf least_utilized.tofino

#Kill any running switch
pkill switchd


#Set environment vars
source /root/bin/set_sde.sh


#Compile the switch
bf-p4c least_utilized.p4
cp_p4 least_utilized


#Launch the switch
$SDE/run_switchd.sh -p least_utilized &

#Wait to it to get setup
sleep 60

#Add the ports
$SDE/run_bfshell.sh -b $SDE/port_setup.py

$SDE/run_bfshell.sh -b "config_least.py"
