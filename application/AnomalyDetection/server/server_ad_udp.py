import socket
import threading
import udp_server
from datetime import datetime
import argparse
import uuid
import random
import time
import os

import numpy as np
import string


import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

model_ = tf.keras.models.load_model('./models/anomaly_detection.h5')

parser = argparse.ArgumentParser()
parser.add_argument('-H', '--host',
					default='127.0.0.1',
					dest='host',
					help='Pass the IP of Host. Defaults is localhost',
					type=str
					)

parser.add_argument('-P', '--port',
					default=12345,
					dest='port',
					help='Provide the Host port number. Defaults to 12345',
					type=int
					)
parser.add_argument('-B', '--buffer',
					default=1024,
					dest='BS',
					help='The buffer size. Defaults to 1024',
					type=int
					)

args = parser.parse_args()


server_ip = args.host
server_port = args.port
BUFFER_SIZE = args.BS
conn_list = {}
name_list = {}

average_lat = 0


class UDPServerMultiClient(udp_server.UDPServer):
	''' A simple UDP Server for handling multiple clients '''

	def __init__(self, host, port):
		super().__init__(host, port)
		self.socket_lock = threading.Lock()
	def handle_request(self, data, client_address):
		''' Handle the client '''
		global average_lat

		input_data = data.decode()
		input_data = input_data[1:-1].split()
		data = []
		for i in input_data:
			data.append(float(i))
		# input_array = np.array([float(i) for i in input_data])
		data = np.array(data)
		# self.printwt(len(data))
		data = data.reshape(1,len(data))
		# self.printwt(data)

		p = model_(data)
		p = p[0][0]
		p = 1 if p>0.5 else 0
		response = str(6)


		response = str(6)
		self.printwt('[ RESPONSE: ' + str (response) + ' is send to ' + str(client_address) + ' ]')

		with self.socket_lock:
			self.sock.sendto(response.encode(), client_address)


	def wait_for_client(self):
		''' Wait for clients and handle their requests '''
		global BUFFER_SIZE
		global conn_list
		global name_list
		try:
			while True: # keep alive
				try: # receive request from client
					data, client_address = self.sock.recvfrom(BUFFER_SIZE)
					cli_key = client_address[0]+":"+str(client_address[1])
					if cli_key in conn_list:
						conn_list[cli_key] += data
						if data==b'':
							comp_data = conn_list.pop(cli_key)
							c_thread = threading.Thread(target = self.handle_request,
							 	args = (comp_data, client_address))
							c_thread.daemon = True
							c_thread.start()
					elif data != b'':
						conn_list[cli_key] = data

				except OSError as err:
					self.printwt(err)
					break
		except KeyboardInterrupt:
			self.shutdown_server()


def main():
	global server_ip, server_port, BUFFER_SIZE
	udp_server_multi_client = UDPServerMultiClient(server_ip, server_port)
	udp_server_multi_client.configure_server()
	udp_server_multi_client.wait_for_client()

if __name__ == '__main__':
	main()
