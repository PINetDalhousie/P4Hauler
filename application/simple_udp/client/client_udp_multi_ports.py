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
# print("The host is " + server_ip)
# print("The port is " + str(server_port))
# print("The buffer size is " + str(BUFFER_SIZE))
# print("The transmit rate is " + str(transmit_rate))
# print(str(number_of_requests) + " packets will be sent.")

lat = []
def send_pic(dst_ip, dst_port, filename, counter):
	start = time.time()
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# sock.connect((dst_ip, dst_port))
	f = open(filename, 'rb')
	l = f.read(BUFFER_SIZE)
	x = ''
	result = -1
	while (l):
		sock.sendto(l,(dst_ip, dst_port))
		l = f.read(BUFFER_SIZE)

	sock.sendto(l,(dst_ip, dst_port))
	f.close()
	# sock.shutdown(socket.SHUT_WR)
	input1 = [sock, sys.stdin]
	while time.time()-start < 10:
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
	if(end-start)<10:
		lat.append(1000*(end-start))
		print(str(1000*(end-start))[0:10] + "\t" + str(result) + "\t" + str(counter+1))


labels = ["Cat", "Dog"]
threads = []
list_of_files = []

for label in labels:
	d = os.listdir('../../datasets/PetImages/' + label)
	for i in range (2):
		x = d[i]
		list_of_files.append("../../datasets/PetImages/"+label+"/"+x)

random.Random(123).shuffle(list_of_files)





def send_pic_debug(dst_ip, dst_port, filename, counter):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	f = open(filename, 'rb')
	l = f.read(BUFFER_SIZE)
	x = ''
	result = -1
	packet = 1
	while (l):
		sock.sendto(l,(dst_ip, dst_port))
		l = f.read(BUFFER_SIZE)
		input("Packet #" +str(packet) + " is sent. Hit Enter to continue!")
		packet += 1

	sock.sendto(l,(dst_ip, dst_port))
	f.close()
	print("The last packet with the length of 0 is sent")
	# sock.shutdown(socket.SHUT_WR)
	input1 = [sock, sys.stdin]
	while 1:
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
	print("The recieved result is: " + str (result) + "\n")



if debug_mode == 1:
	for i in range(number_of_requests):
		send_pic_debug(server_ip, server_port[counter_requests%len(server_port)], list_of_files[index], counter_requests)
		index += 1
		if index == len(list_of_files): index = 0


else:
	overall_timer = time.time()
	while True:
		time.sleep(intervals[counter_requests]/1000)
		# print("Progress: " + str(100*counter_requests/number_of_requests)+"%", end="\r")
		# my_dict = {'dst_ip': server_ip, 'dst_port': server_port[counter_requests%len(server_port)],
		my_dict = {'dst_ip': server_ip, 'dst_port': server_port[counter_requests%len(server_port)],
					'filename':list_of_files[index],  "counter":counter_requests}
		newthread = Thread(target=send_pic,kwargs=my_dict)
		newthread.start()
		threads.append(newthread)
		index += 1
		counter_requests += 1
		if index == len(list_of_files): index = 0
		if counter_requests == number_of_requests: break


	for t in threads:
		t.join()
	overall_timer = time.time() - overall_timer
	lat = np.array(lat)
	#print(sum(lat)/len(lat), len(lat)
	print("avg: ", np.average(lat))
	print("std: ", np.std(lat))
	print("p95: ", np.percentile(lat,95))
	print("p99: ", np.percentile(lat,99))
	los = 100 - 100*len(lat)/(number_of_requests)
	# if los > 10:
	print("com: ", len(lat) / overall_timer)
	print("los: ", 100 - 100*len(lat)/(number_of_requests) )

	print("**********************")