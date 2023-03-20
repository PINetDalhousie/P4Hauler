#!/usr/bin/python3

import argparse
import socket
import time
import select
import sys
from threading import Thread
import os
import numpy as np
import random
import pathlib
import string
import json



parser = argparse.ArgumentParser()
parser.add_argument('-H', '--host',
					default='127.0.0.1',
					dest='host',
					help='Provide destination host. Defaults to localhost',
					type=str
					)

parser.add_argument('-P', '--port',
					default=12345,
					dest='port',
					help='Provide destination port number. Defaults to 12345',
					type=int
					)
parser.add_argument('-B', '--buffer',
					default=1024,
					dest='buffer_size',
					help='The buffer size. Defaults is 1024',
					type=int
					)
parser.add_argument('-R', '--rate',
					default=1,
					dest='rate',
					help='The transmit rate (request/sec). Defaults is 1',
					type=float
					)

parser.add_argument('-N', '--number_packets',
					default=10,
					dest='number_packets',
					help='The number of packets(requests)',
					type=int
					)

parser.add_argument('-D', '--distribution',
                    default="poisson",
                    dest='distribution',
                    help='distribution: constant or poisson',
                    type=str
                    )
parser.add_argument('--debug',
                    default=0,
                    dest='debug',
                    help='Debug Mode',
                    type=int
                    )


args = parser.parse_args()


server_ip = args.host
# server_port = args.port
server_port = [10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009, 10010,
               10011, 10012, 10013, 10014, 10015, 10016, 10017, 10018, 10019, 10020]
BUFFER_SIZE = args.buffer_size
transmit_rate = args.rate
number_of_requests = args.number_packets
distribution = args.distribution
debug_mode = args.debug


intervals = []
if distribution == "poisson":
    intervals = np.random.poisson(lam=1000.0/transmit_rate, size=number_of_requests)
else:
    intervals = number_of_requests * [1000.0/transmit_rate]
index = 0
print(intervals)
counter_requests = 0
counter_corrects = 0

lat = []
lat_server = []
lat_smartnic = []
END_timer = 0


def send_test(dst_ip, dst_port, X, counter):
	x = ''
	start = time.time()
	X = str(X)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	result = -1
	chunks = [X[i:i+BUFFER_SIZE] for i in range(0, len(X), BUFFER_SIZE)]
	for chunk in chunks:
		sock.sendto(chunk.encode(),(dst_ip, dst_port))
	sock.sendto(x.encode(),(dst_ip, dst_port))
	input1 = [sock, sys.stdin]
	while time.time()-start < 20:
		try:
			readyInput, readyOutput, readyException = select.select (input1, [], [],0)
			for x in readyInput:
				if x == sock:
					while True:
						data = sock.recv(BUFFER_SIZE)
						result = int(data.decode())
						sock.close()
						break
		except:
			break
	end = time.time()
	if (end-start)<20:
		END_timer = time.time()
		if result == 6: lat_server.append(1000*(end-start))
		else: lat_smartnic.append(1000*(end-start))
		print(str(1000*(end-start))[0:10] + "\t" + str(result) + "\t" + str(counter+1))


data_path = "../../datasets/datasets/scifact"

queries = []
with open(data_path+"/queries.jsonl", 'r') as json_file:
	json_list = list(json_file)

for json_str in json_list:
	result = json.loads(json_str)
	queries.append(result["text"].translate(str.maketrans('', '', string.punctuation)))


threads = []

overall_timer = time.time()
while True:
	time.sleep(1/transmit_rate)
	my_dict = {'dst_ip': server_ip, 'dst_port': server_port[counter_requests%len(server_port)],
	            'X':queries[index], "counter":counter_requests}
	newthread = Thread(target=send_test,kwargs=my_dict)
	newthread.start()
	threads.append(newthread)
	index += 1
	counter_requests += 1
	if index == len(queries): index = 0
	if counter_requests == number_of_requests: break

for t in threads:
	t.join()

duration = time.time() - overall_timer
duration2 = END_timer - overall_timer
lat = lat_server + lat_smartnic
lat = np.array(lat)


print("avg: ", np.average(lat))
print("std: ", np.std(lat))
print("p95: ", np.percentile(lat,95))
print("p99: ", np.percentile(lat,99))
los = 100 - 100*len(lat)/(number_of_requests)
# if los > 10:
print("com: ", len(lat) / duration)
print("thg: ", 50*len(lat) / duration)
print("FCT: ", str(duration))
lat_server = np.array(lat_server)
lat_smartnic = np.array(lat_smartnic)


min_lat_server = 0
q1 = 0
queue_server = np.array([])

if len(lat_server>0):
	min_lat_server = np.min(lat_server)
	queue_server = lat_server - min_lat_server
	q1 = np.average(queue_server)

min_lat_smartnic = 0
queue_smartnic = np.array([])
q2 = 0
if len(lat_smartnic) > 0:
	min_lat_smartnic = np.min(lat_smartnic)
	queue_smartnic = lat_smartnic - min_lat_smartnic
	q2 = np.average(queue_smartnic)
queue = (q1*len(lat_server) + q2*len(lat_smartnic))/(len(lat_server) + len(lat_smartnic))
print("que: ", queue)
print("los: ", 100 - 100*len(lat)/(number_of_requests) )
print(len(lat_server), len(lat_smartnic))
print("**********************")
