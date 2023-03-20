from status_header import *

import subprocess as sub
from threading import Thread, Timer
from datetime import datetime
import sys
import re
import time
import os
import random
import argparse
import socket
import struct
import psutil

from scapy.all import sendp, send, get_if_list, get_if_hwaddr
from scapy.all import Packet
from scapy.all import Ether, IP, UDP, TCP

# from getmac import get_mac_address
import binascii



parser = argparse.ArgumentParser()
parser.add_argument('--deviceID',"--id",
                    default=1,
                    dest='deviceID',
                    help='Device ID',
                    type=int
                    )

parser.add_argument('--interface',
                    # default='enp101s0f0',
                    # default='p0',
                    default='lo0',
                    dest='interface',
                    help='network interface\'s name',
                    type=str
                    )

parser.add_argument('-i', '--interval',
                    default=1,
                    dest='interval',
                    help='Interval between checking the status',
                    type=float
                    )

parser.add_argument('-s', '--networm-bw',
                    default=25000,
                    dest='bandwidth',
                    help='Network bandwidth',
                    type=int
                    )

parser.add_argument('--debug',
                    default=0,
                    dest='debug',
                    help='Debug Mode',
                    type=int
                    )
parser.add_argument('-t', '--threshold',
                    default=0,
                    dest='threshold',
                    help='Threhsold',
                    type=int
                    )
args = parser.parse_args()
device_id = args.deviceID
interface = args.interface
interval = args.interval
bandwidth = args.bandwidth
debug_mode = args.debug
threshold = args.threshold

cpu_cores = psutil.cpu_count()

IP_REGEX = re.compile('[0-9\.]+\s>\s[0-9\.]+')
TS_REGEX = re.compile('[0-9\.]+:[0-9\.]+:[0-9\.]+\s')

CPU_UTIL_MEM = [0 for i in range(10)]
LAT_MEM = [0 for i in range(10)]



def printwt(msg):
    current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{current_date_time}] {msg}')


def send_status(dst_id, cpu_util, cpu_load, mem_usage, disk_util, net_util):
    iface = interface
    cpu_util = int(cpu_util)
    cpu_load = int(cpu_load)
    mem_usage = int(mem_usage)
    disk_util = int(disk_util)
    net_util = int(net_util)
    # print(get_if_hwaddr(iface), iface)
    pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff', type=0x1234) / status(device_ip = dst_id, cpu_util=cpu_util, cpu_load = cpu_load, mem_usage=mem_usage, disk_util=disk_util, net_util=net_util)
    # pkt.show()
    sendp(pkt, iface=iface, verbose=False)


def Average(lst):
    return sum(lst) / len(lst)


def bite():
    send_status(1, 100, 0, 0, 0, 0)
    send_status(1, 0, 0, 0, 0, 0)
    time.sleep(0.4)

def biting_loop():
    while True:
        x = ""
        try:
            f = open("report.log","r")
            x = f.readline()
        except:
            x = "0"
        x = x.strip()
        x = int(x)
        if x==1:
            bite()
            os.system("rm report.log")
        printwt("checking")
        time.sleep(interval)

def biting_loop_tcpdump():
    connection_list = {}
    p = sub.Popen(('tcpdump', '-l', '-n', '--immediate-mode','-i', interface, 'dst', 'portrange', '10001-10020', 'or', 'src', 'portrange', '10001-10020'), stdout=sub.PIPE)
    for row in iter(p.stdout.readline, b''):
    	l = str(row.rstrip()).strip().split()
    	if l[-1] == "0'":
    		key = l[2]
    		connection_list[l[2]] = time.time()
    	elif l[-1] == "1'" or l[-1] == "2'":
            key = l[4][:-1]
            try:
                lat = (time.time() - connection_list[key])*1000
                if lat > 120: bite()
                printwt("Biting")
            except:
                pass

def monitor_latency():
    global LAT_MEM
    connection_list = {}
    p = sub.Popen(('tcpdump', '-l', '-n', '--immediate-mode','-i', interface, 'dst', 'portrange', '10001-10020', 'or', 'src', 'portrange', '10001-10020'), stdout=sub.PIPE)
    for row in iter(p.stdout.readline, b''):
    	l = str(row.rstrip()).strip().split()
    	if l[-1] == "0'":
    		key = l[2]
    		connection_list[l[2]] = time.time()
    	elif l[-1] == "1'" or l[-1] == "2'":
            key = l[4][:-1]
            try:
                lat = (time.time() - connection_list[key])*1000
                LAT_MEM.remove(LAT_MEM[0])
                LAT_MEM.append(lat)
                printwt("Latency: " + str(lat) + " " + str(Average(LAT_MEM)) + " " + str(len(LAT_MEM)))
            except:
                pass

def send_lat_loop():
    global LAT_MEM
    while True:
        send_status(device_id, Average(LAT_MEM), 0, 0, 0, 0)
        printwt("Second Loop : " + str(Average(LAT_MEM)))
        time.sleep(interval)
        LAT_MEM = LAT_MEM[-9:]
        LAT_MEM.append(0)

def monitor():
    global cpu_cores
    global CPU_UTIL_MEM
    global threshold
    while 1:
        disk_tmp = 0
        net_tmp = 0
        #while True:
        # CPU metrics
        cpu_util = psutil.cpu_percent(interval)                                 # 1
        cpu_load = psutil.getloadavg()[0]                                       # 2

        # Memory metric
        mem_usage = psutil.virtual_memory()[2]                                  # 3

        # Disk Metric
        # disk_busy = psutil.disk_io_counters(perdisk=False, nowrap=True)[-1]
        disk_busy = random.randint(1,100)
        disk_util = (disk_busy-disk_tmp)/interval/10                            # 4
        disk_tmp = disk_busy

        # Network
        net_stat = psutil.net_io_counters(pernic=False, nowrap=True)
        net_NB = 8*(net_stat[0] + net_stat[1])/1024**2
        net_util = 100*(net_NB - net_tmp)/bandwidth                             #5
        net_tmp = net_NB

        CPU_UTIL_MEM.remove(CPU_UTIL_MEM[0])
        CPU_UTIL_MEM.append(cpu_util)
        average_ = Average(CPU_UTIL_MEM)
        printwt(average_)
        if average_ > threshold:
            send_status(device_id, Average(CPU_UTIL_MEM), cpu_load, mem_usage, disk_util, net_util)
        else:
            send_status(device_id, 0, cpu_load, mem_usage, disk_util, net_util)


def debug_function():
    while 1:
        x = int(input("Enter the value you want to send to the switch from Device " + str(device_id) + "\n"))
        send_status(device_id, x, 0, 0, 0, 0)

def loop_monitor():
    while 1:
        send_status(device_id, 100, 0, 0, 0, 0)
        time.sleep(interval)
        send_status(device_id, 0, 0, 0, 0, 0)
        time.sleep(interval)



if __name__=="__main__":
    os.system("sudo ip link set " +  interface + " promisc on")
    send_status(3, 100, 100, 100, 100, 100)
    if debug_mode == 0:
        top_thread = Thread(target = monitor, args =())
        top_thread.start()
    elif debug_mode == 1:
        top_thread = Thread(target = debug_function, args =())
        top_thread.start()
    elif debug_mode == 2:
        top_thread = Thread(target = loop_monitor, args =())
        top_thread.start()
    elif debug_mode == 3:
        top_thread = Thread(target = biting_loop, args =())
        top_thread.start()
    elif debug_mode == 4:
        top_thread = Thread(target = biting_loop_tcpdump, args =())
        top_thread.start()
    elif debug_mode == 5:
        top_thread = Thread(target = monitor_latency, args =())
        top_thread.start()
        second_thread = Thread(target = send_lat_loop, args = {})
        second_thread.start()
