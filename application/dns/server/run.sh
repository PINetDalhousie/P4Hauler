#!/bin/bash

sudo killall python3
sudo taskset -c 1 python3 oldserver.py
