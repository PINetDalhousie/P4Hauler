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
import json
import pathlib
import string
from rank_bm25 import BM25Okapi



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
data_path = "../../datasets/datasets/scifact"

tokenized_corpus = []
with open(data_path+"/corpus.jsonl", 'r') as json_file:
        json_list = list(json_file)

for json_str in json_list:
        result = json.loads(json_str)
        tokenized_corpus.append(result["text"].translate(str.maketrans('', '', string.punctuation)).split(" "))

bm25 = BM25Okapi(tokenized_corpus)



class UDPServerMultiClient(udp_server.UDPServer):
	''' A simple UDP Server for handling multiple clients '''

	def __init__(self, host, port):
		super().__init__(host, port)
		self.socket_lock = threading.Lock()
	def handle_request(self, data, client_address):
		''' Handle the client '''
		global average_lat
		start = time.time()
		self.printwt('[ REQUEST from ' + str(client_address) + ' ]')
		# input_data = data.decode().translate(str.maketrans('', '', string.punctuation)).split(" ")
		input_data = data.decode()
		scores = bm25.get_scores(input_data)
		p = scores.argmax()
		response = str(16)
		self.printwt('[ RESPONSE: ' + str (p) + ' is send to ' + str(client_address) + ' ]')

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
