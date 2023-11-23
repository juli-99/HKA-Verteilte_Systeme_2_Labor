import pickle
import zmq

import re

import const_address

def run():
	context = zmq.Context()

	pull_socket = context.socket(zmq.PULL)
	pull_socket.connect(const_address.SPLITTER)

	push_socket1 = context.socket(zmq.PUSH)
	push_socket1.connect(const_address.REDUCER1)

	push_socket2 = context.socket(zmq.PUSH)
	push_socket2.connect(const_address.REDUCER2)

	while True:
		line = pickle.loads(pull_socket.recv())

		pattern = r'[^\w ]' ##r'[^a-zäöü ]'
		words = re.sub(pattern, '', line.lower()).split()

		for word in words:
			num_code = ord(word[0])
			if ord("a") <= num_code <= ord("m"):
				push_socket1.send(pickle.dumps(word))
			else:
				push_socket2.send(pickle.dumps(word))
