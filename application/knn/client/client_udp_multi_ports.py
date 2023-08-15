#!/usr/bin/python3

import argparse
import socket
import time
import select
import sys
from threading import Thread
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import random
import idx2numpy


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
					default=2,
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

args = parser.parse_args()


server_ip = args.host
# server_port = args.port
server_port = [10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009, 10010, 10011, 10012, 10013, 10014, 10015, 10016, 10017, 10018, 10019, 10020]

BUFFER_SIZE = args.buffer_size
transmit_rate = args.rate
number_of_packets = args.number_packets
distribution = args.distribution
intervals = []
if distribution == "poisson":
    intervals = np.random.poisson(lam=1000.0/transmit_rate, size=number_of_packets)
else:
    intervals = number_of_packets * [1000.0/transmit_rate]
index = 0
print(intervals)

counter_packets = 0
counter_corrects = 0
#print("The host is " + server_ip)
#print("The port is " + str(server_port))
#print("The buffer size is " + str(BUFFER_SIZE))
print("The transmit rate is " + str(transmit_rate))
#print(str(number_of_packets) + " packets will be sent.")

lat_server = []
lat_smartnic = []
END_timer = 0
def send_test(dst_ip, dst_port, X, counter):
	global END_timer
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
	while time.time()-start < 30:
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
	if (end-start)<30:
		END_timer = time.time()
		if result == 6: lat_server.append(1000*(end-start))
		else: lat_smartnic.append(1000*(end-start))
		print(str(1000*(end-start))[0:10] + "\t" + str(result) + "\t" + str(counter+1))

os.system("gzip -d ./mnist/*")

train_x_path = "mnist/train-images-idx3-ubyte"
train_y_path = "mnist/train-labels-idx1-ubyte"

test_x_path = "mnist/t10k-images-idx3-ubyte"
test_y_path = "mnist/t10k-labels-idx1-ubyte"

x_train = []
y_train = []

x_test = []
y_test = []


x_train = idx2numpy.convert_from_file(train_x_path)
y_train = idx2numpy.convert_from_file(train_y_path)
x_train = np.reshape(x_train, (60000, 28*28))
x_test = idx2numpy.convert_from_file(test_x_path)
y_test = idx2numpy.convert_from_file(test_y_path)
x_test = np.reshape(x_test, (10000,28*28))


threads = []
overall_timer = time.time()
while True:
	time.sleep(intervals[counter_packets]/1000)
	my_dict = {'dst_ip': server_ip, 'dst_port': server_port[counter_packets%len(server_port)],
				'X':x_test[index], "counter":counter_packets}
	# my_dict = {'dst_ip': server_ip, 'dst_port': server_port[counter_packets%len(server_port)],
	# 			'filename':list_of_files[index],  "counter":counter_packets}
	newthread = Thread(target=send_test,kwargs=my_dict)
	newthread.start()
	threads.append(newthread)
	index += 1
	counter_packets += 1
	if index == len(x_test): index = 0
	if counter_packets == number_of_packets: break


for t in threads:
	t.join()

overall_timer = END_timer - overall_timer
lat = lat_server + lat_smartnic
lat = np.array(lat)


print("avg: ", np.average(lat))
print("std: ", np.std(lat))
print("p95: ", np.percentile(lat,95))
print("p99: ", np.percentile(lat,99))
los = 100 - 100*len(lat)/(number_of_packets)
print("com: ", len(lat) / overall_timer)
print("thg: ", 3.11*len(lat) / overall_timer)
print("FCT: ", str(overall_timer))

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
print("los: ", 100 - 100*len(lat)/(number_of_packets) )
print(len(lat_server), len(lat_smartnic))
print("**********************")
